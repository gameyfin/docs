---
icon: material/shield-lock
---

# Security and single sign-on

Open **Administration → Security** for public access, API documentation, and SSO.

## Public access

Access without login is disabled by default.
Enabling it lets visitors browse games and potentially download them without an account.
Review your enabled download providers before allowing public access.

## Interactive API documentation

Interactive API documentation is disabled by default.
Enabling it makes `/swagger-ui.html` and the OpenAPI document publicly accessible.
This exposes the API documentation; API operations still require their own permissions.
See [API keys](api.md) for integration credentials.

## Configure an identity provider

SSO through OpenID Connect / OAuth 2.0 is optional and disabled by default.
Keep a working local administrator login while configuring it.

1. Register Gameyfin as a client in your identity provider.
2. Set the callback URL to `https://<your-gameyfin-host>/login/oauth2/code/oidc`.
3. Enter the client ID, client secret, and issuer URL in Gameyfin.
4. Enable SSO and use **Auto-populate** to fill endpoints from OIDC discovery.
5. Check the authorization, token, userinfo, JWKS, and logout URLs; fill them manually if discovery is unavailable.
6. Save and test the login.

Use the [Authentik guide](../guides/sso/authentik.md) or [Pocket ID guide](../guides/sso/pocketid.md) for provider-specific steps.

## Claims, scopes, and account matching

Choose whether an SSO identity matches an existing account by **username** or **email**.
The username claim defaults to `preferred_username`.
If missing or blank, Gameyfin tries `preferred_username`, `nickname`, `name`, `email`, then `sub`.

The roles claim defaults to `roles`. Supply a list of role strings in the userinfo response.
Gameyfin maps roles prefixed with `GAMEYFIN_`, such as `GAMEYFIN_USER` and `GAMEYFIN_ADMIN`, to its roles.
Grant administrator roles only to trusted accounts.

Default scopes are `openid`, `profile`, `email`, and `roles`.
The requested scopes must include `openid`. If your provider does not support `roles`, adjust the scope list and role claim accordingly.

See the [reference](reference.md#sso-oidc-enabled) for every SSO field and default.
