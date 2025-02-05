import requests
import os
from dotenv import load_dotenv
from rest_framework.authentication import BaseAuthentication
import jwt
from django.contrib.auth.models import User
from authapp.models import UserToken
from datetime import datetime

load_dotenv()

class AzureADAuthentication(BaseAuthentication):
    def authenticate(self, request):
        """
        Authenticate the user by verifying the token with Azure AD first and then authenticating the user.
        """
        auth_header = request.headers.get("Authorization", None)

        if not auth_header:
            return None

        token = auth_header.split(" ")[1] if " " in auth_header else None

        if not token:
            return None

        try:
            # Verify the token with Azure AD
            self.verify_token_with_azure_ad(token)

            # Check if the token is already blacklisted
            token_exists, user_token = self.is_token_blacklisted(token)
            if token_exists and user_token.blacklisted:
                raise ValueError("Token is blacklisted")

            # Authenticate the user using the decoded token
            decoded_token = self.decode_token(token)
            user = self.get_or_create_user(decoded_token)

            # Store the token in the backend
            self.store_token_in_backend(user, token)

            return (user, None)

        except jwt.ExpiredSignatureError:
            raise ValueError("Token is expired")
        except jwt.InvalidTokenError:
            raise ValueError("Token is invalid")
        except User.DoesNotExist:
            raise ValueError("User not found")

    def verify_token_with_azure_ad(self, token):
        """
        Verify the token with Azure AD to ensure it's valid.
        """
        introspection_url = os.getenv("AZURE_AD_OPENID_CONFIG_URL")
        headers = {
            "Authorization": f"Bearer {token}",
        }

        try:
            response = requests.get(introspection_url, headers=headers)
            response.raise_for_status()
            # Additional checks can be performed here
        except requests.exceptions.RequestException as e:
            raise ValueError("Failed to validate token with Azure AD: " + str(e))

    def decode_token(self, token):
        """
        Decode the JWT token and return the payload.
        """
        return jwt.decode(token, options={"verify_signature": False})

    def get_or_create_user(self, decoded_token):
        """
        Get or create a user from the decoded token.
        """
        preferred_username = (
            decoded_token.get("preferred_username") or
            decoded_token.get("upn") or 
            decoded_token.get("oid")
        )

        email = decoded_token.get("email") or decoded_token.get("upn")
        name = decoded_token.get("name", "")

        if not preferred_username:
            raise ValueError("No suitable username found in token")

        if not email:
            raise ValueError("No email found in token")

        user, created = User.objects.get_or_create(
            username=preferred_username,
            defaults={"email": email, "first_name": name}
        )

        if not created:
            user.email = email or user.email
            user.first_name = name or user.first_name
            user.save()

        return user

    def store_token_in_backend(self, user, token):
        """
        Store the token information in the backend (e.g., UserToken model).
        """
        UserToken.objects.update_or_create(
            user=user,
            defaults={
                "token": token,
                "created_at": datetime.now()
            }
        )

    def blacklist_token(self, token):
        """
        Blacklist a token upon user logout.
        """
        try:
            user_token = UserToken.objects.get(token=token)
            user_token.blacklisted = True
            user_token.save()
        except UserToken.DoesNotExist:
            raise ValueError("Token not found to blacklist")

    def is_token_blacklisted(self, token):
        """
        Check if a token is blacklisted in the backend.
        """
        try:
            user_token = UserToken.objects.get(token=token)
            return True, user_token
        except UserToken.DoesNotExist:
            return False, None

    def request_access_token(self):
        """
        Request an access token from Azure AD using client credentials.
        """
        url = f"https://login.microsoftonline.com/{os.getenv('AZURE_AD_TENANT_ID')}/oauth2/v2.0/token"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        body = {
            "grant_type": "client_credentials",
            "client_id": os.getenv("AZURE_AD_CLIENT_ID"),
            "client_secret": os.getenv("AZURE_AD_CLIENT_SECRET"),
            "scope": "https://graph.microsoft.com/.default"
        }

        response = requests.post(url, headers=headers, data=body)
        response.raise_for_status()
        return response.json().get("access_token")
