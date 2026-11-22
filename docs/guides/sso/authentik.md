---
title: Authentik
description: Connect Gameyfin with Authentik for Single Sign-On (SSO)
icon: simple/authentik
---

## Create an application in Authentik

Create a new application in Authentik to enable Single Sign-On (SSO) for Gameyfin.

Go to `Applications > Applications > Create with Provider` and follow these steps:

1. **Application**: Fill out to your liking.
2. **Choose a Provider**: `OAuth2/OpenID Provider`
3. **Configure Provider**:
     - Client type: `Confidential`
     - Redirect URIs: `https://<your-gameyfin-domain>/login/oauth2/code/oidc`
4. **Configure Bindings**: Bind policies to the application as needed.
5. **Review and Submit Application**: Your settings should look similar to this:
   ![Authentik Application Configuration](../../assets/guides/sso/authentik/authentik-application.png)


## Create a property mapping

Gameyfin is able to read the users roles from SSO. To do this, you need to create groups and a property mapping in Authentik.

First create two groups in Authentik (`Directory > Groups > Create`), one for superadmins and one for admins.  
Then go to `Customization > Property Mappings > Create` and create a new mapping with the following settings:

- **Scope name**: `profile`
- **Expression**: Fill out the placeholders with the groups you created above:
   ```python
   if ak_is_group_member(request.user, name="<your superadmin group name>"):
     return { "roles": ["GAMEYFIN_SUPERADMIN"] }
   if ak_is_group_member(request.user, name="<your admin group name>"):
     return { "roles": ["GAMEYFIN_ADMIN"] }
   return { "roles": ["GAMEYFIN_USER"] }
   ```

Add your users to their respective groups in Authentik.
For ordinary users, return `["GAMEYFIN_USER"]` in the roles claim. Verify that every intended user receives a role.

## Configure Gameyfin

Go to Gameyfin's SSO settings page (`Administration > Security`), enable SSO and fill out the SSO provider configuration with the values from Authentik.
You can use "Auto-populate" to fill most the values automatically, or copy them manually from the Authentik application you created earlier.

*Hint: "Auto-populate" will only work if Gameyfin and Authentik are hosted under the same domain or if you have configured a CORS policy for Authentik that allows calls from your Gameyfin domain. This is not an issue of Gameyfin but rather a security measure implemented by Authentik.*

Save the settings and test the SSO login. Gameyfin applies SSO configuration changes without an application restart.

*Hint: If there is a problem with your SSO configuration, and you can't log in, simply append `?direct=1` to the URL to bypass SSO and login with your username and password.*

