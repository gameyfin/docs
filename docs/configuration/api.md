---
icon: material/key
---

# API keys

Use API credentials for scripts and integrations instead of sharing your account password.
Manage service credentials in **Administration → API keys**. Personal tokens are available from your profile.

Copy a new token when it is shown and store it securely. Treat it like a password.
Use an expiry and only the permissions your integration needs. Revoke unused or exposed credentials.
Personal tokens follow their owner's permissions; service credentials use their selected scopes.

Send the token in the HTTP `X-API-Key: <token>` header for the REST API under `/v1`.
The interactive API documentation at `/swagger-ui.html` is available after an administrator enables it under **Security**.
It documents endpoints and request formats for the installed Gameyfin version.

You can also browse the [public API reference](../api/reference.md) on this documentation site or [download its OpenAPI schema](../api/openapi.json).
