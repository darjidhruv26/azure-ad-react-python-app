# Single Sign-On (SSO)

Single Sign-On (SSO) is an authentication method that lets users log in once to access multiple systems or applications without re-entering credentials. It improves user convenience by reducing password management and enhances security through centralized authentication, stronger password policies, multi-factor authentication (MFA), and better access control. SSO relies on a trusted relationship between an identity provider (IdP) and service providers (SPs). The IdP authenticates the user and issues a token or assertion, which SPs recognize to grant access. Common SSO protocols include SAML, OAuth, and OpenID Connect.

# Azure Active Directory (Azure AD)

Azure Active Directory (Azure AD) is Microsoft’s cloud-based identity and access management service, designed to help organizations manage user identities, control access to applications and resources, and enforce security policies. As a core part of Microsoft’s enterprise mobility and security solutions, Azure AD integrates with Microsoft 365, Azure services, and numerous third-party applications. Organizations of all sizes widely adopt it to modernize identity infrastructure, enhance security, and enable seamless access to both cloud and hybrid environments. Azure AD is particularly vital for enterprises implementing zero-trust security models and driving digital transformation initiatives.

### In web server apps, the sign-in authentication flow takes these high-level steps

![Azure_SPA_res_rq](https://github.com/user-attachments/assets/08767790-9d96-4458-b8fc-128bbcb469e6)

# Steps to Setup Azure Active Directory

## Step 1: Create a New Azure AD Tenant

- In the Azure Portal, search for `Azure Active Directory` or `Microsoft Entra ID` in the top search bar.
- Click on `Microsoft Entra ID` in the search results.
- In the left-hand menu, click `Manage tenants`.
  
![manage_tenants](https://github.com/user-attachments/assets/93ca955a-8caa-4a09-905f-b3cba9929f3d)

- Click `+ Create` to create a new tenant.
- Select a tenant type is `Azure AD B2C` and click Next.
  
![createATenant](https://github.com/user-attachments/assets/19b9114c-2e92-49e2-9c18-451a533480a5)

## Step 2: Configure the Directory Details
- Organization name: Enter a unique name for your directory (e.g., demoApp).
- Initial domain name: Enter a domain (e.g., yourcompany.onmicrosoft.com).
- Country/Region: Select your country (e.g., India).
- Click Review + create.
- After validation, click Create.

![demoApp](https://github.com/user-attachments/assets/882904f6-ac23-41ed-878c-2c76c648130a)

##  Step 3: Add Users
- Navigate to `Microsoft Entra ID`.
- Click Users > + New user to add users.
- Copy User name and Password
![image](https://github.com/user-attachments/assets/3ac80feb-e753-4243-a413-201e8148f878)


# Steps to configure a Web App (SPA (frontend) and Django backend API)

## Step 1: Create a Single Azure AD App Registration

- Navigate to Azure Active Directory > App Registrations > New Registration.

- Name: MyApp-SPA-API (or your preferred name).

- Supported Account Types: Select based on your needs (e.g., "Accounts in this organizational directory only" for single-tenant).

- Redirect URI:

   - Type: Single-page application (SPA).

   - Value: http://localhost:3000 (your SPA's development URL).

Click Register.

![image](https://github.com/user-attachments/assets/10a41fd6-d3bb-4520-a37b-93991f61e483)

## Step 2: Expose the Backend API

- In your app registration, go to Expose an API.

- Application ID URI: Set to `api://<client-id>` or `https://<primary-domain>/<client-id>` (replace <client-id> with your app's client ID).

- Click Save.

- Add a Scope:

  - Scope name: access_as_user.

  - Who can consent?: Admins and users.

  - Admin consent display name: Access MyApp API.

  - Admin consent description: Allows the app to access the backend API on behalf of the user.

    ![image](https://github.com/user-attachments/assets/460d48df-f8a4-4706-b107-a71647f01298)

Click Add Scope.

![image](https://github.com/user-attachments/assets/bed90957-8cf2-408c-a259-a336649e2ab7)

## Step 3: Configure API Permissions

- Go to API Permissions.

- Add a Permission > Microsoft Graph > Delegated Permissions:

Select User.Read (for basic user profile access).

![image](https://github.com/user-attachments/assets/73b42380-5cf3-4ba0-aa49-a47f36e93fe2)

Add a Permission > My APIs > Select your app registration:

Select the access_as_user scope.

![image](https://github.com/user-attachments/assets/949a3b83-34c8-478e-ba76-8165e90e825e)

Click Grant admin consent (if you’re an admin).

![image](https://github.com/user-attachments/assets/de3a8f63-1537-4023-b0ea-193a22843c27)

## Step 4: Configure Authentication for the SPA

- Go to Authentication.

- Under Platform Configurations, add a Single-page application:

 - Redirect URI: http://localhost:3000.

 - Logout URL: http://localhost:3000.

![image](https://github.com/user-attachments/assets/be1aafc3-fafd-405b-ad09-0cf1f7cb57da)

- Ensure the Implicit grant is disabled (use Auth Code Flow with PKCE).

- Front-channel logout URL: Optional (set if needed).

- Click on Save

## Step 5: Create a Client Secret (for the Backend)

- Go to Certificates & Secrets.

- Click New client secret.

- Description: Django Backend Secret.

- Expires: Choose a duration (e.g., 24 months).

- Copy the secret value (you won’t see it again).

![image](https://github.com/user-attachments/assets/734b812f-9a36-404a-af74-5479cd532c2e)

## Step 6: Configure Token Settings

- Go to Token Configuration.

- Optional Claims > Add optional claim:

  - Token type: Access.

  - Claim: aud (ensure the audience matches your API's client_id).

Save.

Or if there is no option of Token Configuration then click on `Manifest`

- Click on Microsoft Graph App Manifest (New)

- Add this to the manifest file 

```
"optionalClaims": {
	"accessToken": [
    	{
        	"name": "aud",
        	"source": null,
        	"essential": false,
        	"additionalProperties": []
    	}
	]
},
```

![image](https://github.com/user-attachments/assets/3b7dc018-b617-4384-a4fb-fd33d0eaafbc)

## Step 7: : Note Critical Azure AD Details

- Save these values for your frontend and backend:

- `Application (Client) ID`: Found on the app registration overview page.

- `Directory (Tenant) ID`: Found on the app registration overview page.

- `Client Secret`: From Step 5.

- `Scope URI`: `api://<client-id>/access_as_user` or `https://<primary-domain>/<client-id>/access_as_user`.

- `Authority URL`: `https://login.microsoftonline.com/<tenant-id>`.

![image](https://github.com/user-attachments/assets/e15b8d7d-eff6-40ca-9a05-d00d7e6feb99)

## Step 8: Configure Post-Login Redirects

- Go to Authentication > Platform Configurations.

- Ensure `http://localhost:3000` is listed under Redirect URIs.

- Add `http://localhost:3000/silent-renew.html` if using silent token renewal.

![image](https://github.com/user-attachments/assets/03802228-6c91-4bd8-a804-f6e868861200)


## Step 9: Test the Configuration

- Use tools like Postman or the Microsoft Graph Explorer to validate:

- Acquire a token for your SPA with the access_as_user scope.

- Verify the token includes the correct aud (audience) claim.

# Setup Application

## Step 1: Clone demo application

- I have created a demo application for implementing SSO

## [GitHub Repository](https://github.com/darjidhruv26/azure-ad-react-python-app)

- Clone this repository `https://github.com/darjidhruv26/azure-ad-react-python-app.git`

## Step 2: Update in .env

- Update .env file in both frontend and backend
  
- Replace with your Azure AD `Tenant ID`, `Client ID`, `Client Secret`, `Scope URI` and `Authority URL`

## Step 3: Run Application

- Frontend run on `http://localhost:3000/`

![image](https://github.com/user-attachments/assets/04b7c7cd-49fa-460e-b684-c0e7fe42e224)

## Step 4: Test Authentication flow

- Start this application in the incognito tab

- Click on `Login with Azure AD`
  
- Login pop-up is open
  
- Enter `User Name`
  
![image](https://github.com/user-attachments/assets/c226ebf9-7faa-4d7a-9468-5538169708c6)

- Enter `Password` (When the User Created in AD)
  
![image](https://github.com/user-attachments/assets/4edf661a-848f-4a92-a196-9029b25a912f)

- Update `password`
  
![image](https://github.com/user-attachments/assets/9e779e17-daa7-4ba4-8c55-87631af4ca1d)

- Enable multi-factor authentication for additional security.
  
![image](https://github.com/user-attachments/assets/d3c95139-130e-4637-b254-cef43f024b69)

- Congratulations, Chris Martin successfully logged in to your site 🎉🎉.
  
![image](https://github.com/user-attachments/assets/12bdc584-a564-4f8c-96b3-844fb4199671)

## Step 5: Access Token, Refresh Token and Scope

![image](https://github.com/user-attachments/assets/d0afc73e-ebe2-4dd1-9843-3cf09bf7b8e5)

![image](https://github.com/user-attachments/assets/f66388d0-9dbd-49d0-adec-828b381e0d88)

- Copy the Access Token and paste it in [jwt.io](https://jwt.io/) for verification

![image](https://github.com/user-attachments/assets/da4351b5-93c1-4066-971f-a16d7f9fd250)

# Reference

- [Microsoft identity platform documentation](https://learn.microsoft.com/en-us/entra/identity-platform/)

- [Application types for the Microsoft identity platform](https://learn.microsoft.com/en-us/entra/identity-platform/v2-app-types#single-page-apps)
  
- [Configure authentication in a sample React single-page application by using Azure Active Directory B2C](https://learn.microsoft.com/en-us/azure/active-directory-b2c/configure-authentication-sample-react-spa-app)
 
