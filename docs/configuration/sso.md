# SSO

## SSO configuration

### Enable SSO via OIDC/OAuth2
Default: `false`  
This option enables Single Sign-On (SSO) via OIDC/OAuth2. If enabled, users can log in using your configured OIDC/OAuth2 provider.

## SSO user handling

### Automatically create users after registration
Default: `true`  
This option automatically creates users in Gameyfin after they register via SSO. If disabled, SSO users will not be persisted in Gameyfin.

### Match existing users by
Default: `username`  
This option allows you to specify how existing users should be matched with SSO users. You can choose between `username` and `email`.

## SSO provider configuration
This section allows you to configure your OIDC/OAuth2 provider for SSO. You will need to provide the following information:

- **Client ID**: The client ID of your OIDC/OAuth2 application.
- **Client Secret**: The client secret of your OIDC/OAuth2 application.
- **Issuer URL**: The issuer URL of your OIDC/OAuth2 provider.

The rest can be autopopulated by clicking the "Auto-populate" button. However, you can also configure the options automatically.