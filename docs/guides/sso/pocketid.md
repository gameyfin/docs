---
title: Pocket-ID
description: Connect Gameyfin with Pocket-ID for Single Sign-On (SSO)
---

## Create an OIDC client in Pocket-ID

Create a new OIDC client in Pocket-ID to enable Single Sign-On (SSO) for Gameyfin.

Go to `OIDC Clients > Add OIDC Client` and follow these steps:

1. **Name**: Fill out to your liking.
2. **Client launch URL**: `https://<your-gameyfin-domain>`
3. **Callback URLs**:`https://<your-gameyfin-domain>/login/oauth2/code/oidc` (or leave empty for automatic detection)


## Create group(s)

Gameyfin is able to read the users roles from SSO. To do this, you need to create groups with custom claims in Pocket-ID.

Create two groups in Pocket-ID (`User Groups > Add Group`), one for superadmins and one for admins:

- **Friendly name**: Fill out to your liking.
- **Name**: Use the generated one or change it if you want.

Click `Save` and then add a custom claim to each group (`Custom Claims > Add custom claim`):
- **Key**: `roles`
- **Value**: For the superadmin group use `["GAMEYFIN_SUPERADMIN"]`, and for the admin group use `["GAMEYFIN_ADMIN"]`.

Click `Save` to create the custom claim.

Add your users to their respective groups in Pocket-ID.
Users that are not in either group will automatically be assigned the "User" role.

## Configure Gameyfin

Go to Gameyfin's SSO settings page (`Administration > SSO`), enable SSO and fill out the SSO provider configuration with the values from Pocket-ID.  
Pocket-ID does not display an "Issuer URL" directly, use the domain of your Pocket-ID instance **without a trailing slash (`/`)**

You can use "Auto-populate" to fill most the values automatically, or copy them manually from the Pocket-ID application you created earlier.

*Hint: "Auto-populate" will only work if Gameyfin and Pocket-ID are hosted under the same domain or if you have configured a CORS policy for Pocket-ID that allows calls from your Gameyfin domain. This is not an issue of Gameyfin but rather a security measure implemented by Pocket-ID.*

Restart Gameyfin to apply the changes.

*Hint: If there is a problem with your SSO configuration, and you can't log in, simply append `?direct=1` to the URL to bypass SSO and login with your username and password.*

