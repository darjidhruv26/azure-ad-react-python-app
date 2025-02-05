# Single Sign-On (SSO)

Single Sign-On (SSO) is an authentication mechanism that allows users to log in once and gain access to multiple applications or systems without needing to re-enter credentials. SSO simplifies the user experience by reducing the number of passwords users need to remember and manage. It also enhances security by centralizing authentication and enabling stronger password policies, multi-factor authentication (MFA), and streamlined access control.

SSO establishes a trusted relationship between an identity provider (IdP) and service providers (SPs). When a user logs in, the IdP authenticates the user and issues a token or assertion recognized by the SPs, granting access to authorized resources. Popular SSO protocols include SAML (Security Assertion Markup Language), OAuth, and OpenID Connect.

# Azure Active Directory (Azure AD)

Azure Active Directory (Azure AD) is Microsoft’s cloud-based identity and access management service. It serves as a comprehensive identity provider, enabling organizations to manage user identities, control access to applications and resources, and enforce security policies. Azure AD is a core component of Microsoft’s enterprise mobility and security offerings, integrating seamlessly with Microsoft 365, Azure services, and thousands of third-party applications.

Azure AD is widely used by organizations of all sizes to modernize their identity infrastructure, improve security, and enable seamless access to cloud and hybrid environments. It is a critical component for enterprises adopting zero-trust security models and digital transformation initiatives.

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

![Ad_user](https://github.com/user-attachments/assets/dc4b5c35-58b3-4d9b-b7bc-d276f594df29)

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

- Application ID URI: Set to api://<client-id> or https://<primary-domain>/<client-id> (replace <client-id> with your app's client ID).

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



