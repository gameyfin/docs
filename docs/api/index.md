---
title: Public API
icon: material/api
---

# Public API

Gameyfin's REST API lets scripts and third-party applications work with games, libraries, collections, requests,
downloads, and instance information.
Endpoints use the `/v1` prefix on **your Gameyfin instance**.

Browse the [API reference](reference.md) for operations, parameters, request bodies, responses, and schemas.
You can also [download the OpenAPI document](openapi.json) for API clients and code generators.

## Authentication

Create a personal access token in your profile, or a scoped service API key under **Administration → API keys**.
Send the credential in the `X-API-Key` header. The REST API does not use your browser login session.

For example, list games from a local installation:

```sh
curl --header "X-API-Key: YOUR_TOKEN" \
  "http://localhost:8080/v1/games"
```

Replace the URL with your own instance and `YOUR_TOKEN` with your credential.
Use HTTPS when accessing a server over the internet, and keep credentials out of source control.
Personal tokens follow the account's permissions. Service keys need the scopes required by each operation, such as
`games:read`.
See [API keys](../configuration/api.md) for credential management.

## Reference version

Your installation may run a different Gameyfin version.
For its exact API, enable interactive API documentation under **Administration → Security**, then open
`/swagger-ui.html` on your instance.
Its grouped schema is available at `/v3/api-docs/v1` as JSON or `/v3/api-docs.yaml/v1` as YAML.

The web interface's internal Hilla endpoints are not part of this public API.
