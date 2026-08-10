---
title: Issue Consumer Credentials via API
---

<!-- overview -->

This guide explains how API Providers can **issue and regenerate consumer
credentials** for Product Environments using the Credential Issuer API — without
an Access Request or approval queue.

Use this when you want to provision credentials programmatically (for example,
from your own onboarding system or CI/CD pipeline) for services in a Gateway you
manage.

| Environment     | Directory API Base URL                         |
| --------------- | ---------------------------------------------- |
| TEST / TRAINING | `https://api-gov-bc-ca.test.api.gov.bc.ca`     |
| PRODUCTION      | `https://api.gov.bc.ca`                        |

**Base path:** `/ds/api/v3/gateways/{gatewayId}/consumers`

| Action     | Method | Path                                                                        | Success |
| ---------- | ------ | --------------------------------------------------------------------------- | ------- |
| Issue      | `POST` | `/ds/api/v3/gateways/{gatewayId}/consumers`                                 | `201`   |
| Regenerate | `PUT`  | `/ds/api/v3/gateways/{gatewayId}/consumers/{clientId}?action=regenerate`    | `200`   |

!!! note
    Revoke is not available on this API yet. Use the Portal **Consumers** page
    to revoke access. See [Manage Consumer Access](/how-to/api-access.md).

For interactive API reference, open the Directory API OpenAPI console:

| Environment     | OpenAPI Console                                                                                              |
| --------------- | ------------------------------------------------------------------------------------------------------------ |
| TEST / TRAINING | <https://api-gov-bc-ca.test.api.gov.bc.ca/ds/api/v3/console>                                                 |
| PRODUCTION      | <https://api.gov.bc.ca/ds/api/v3/console>                                                                    |

Look for the `issue-gateway-consumer` and `regenerate-gateway-consumer`
operations.

## Before you begin

Before you begin, ensure you:

- [Create a Gateway](/how-to/create-gateway.md)
- Configure Product Environments with a [supported flow](#supported-flows)
  (and an Authorization Profile for client-credentials flows)
- Publish Kong services and plugins for those Environments (same as a normal
  API publish) — see [Create a Gateway Service](/how-to/create-gateway-service.md)
- [Generate a Service Account](/how-to/generate-service-account.md) (or use a
  user token) with the `CredentialIssuer.Generate` scope on that Gateway

Product Environments do **not** need to be active in the API Directory for
issuing credentials.

## Supported flows

| Flow                 | Authenticator / variant                                      |
| -------------------- | ------------------------------------------------------------ |
| `kong-api-key-only`  | API key                                                      |
| `kong-api-key-acl`   | API key with ACL                                             |
| `client-credentials` | `client-secret`                                              |
| `client-credentials` | `client-jwt` (generated certificate / key pair)              |
| `client-credentials` | `client-jwt-jwks-url` (caller supplies JWKS URL or certificate) |

## Permission

Requests require a JWT (service account or user token) with the UMA scope
`CredentialIssuer.Generate`. In the Portal, that scope maps to the
`credential-issuer` role:

> Can issue and regenerate consumer credentials for services in this gateway
> via the Credential Issuer API.

A token without this scope receives `403`.

## Get `environmentAppId`

The issue request requires `environmentAppId`. This value is **API-only** today
— it is not shown as a field in the Portal Products UI.

1. Obtain a token with access to the Gateway.
2. Call:

   ```http
   GET /ds/api/v3/gateways/{gatewayId}/products
   Authorization: Bearer <token>
   ```

3. From the response, copy `products[].environments[].appId` for the target
   Environment. That value is what you pass as `environmentAppId`.

## Issue credentials

```http
POST /ds/api/v3/gateways/{gatewayId}/consumers
Authorization: Bearer <issuer-token>
Content-Type: application/json
```

```json
{
  "environmentAppId": "<Environment.appId>",
  "application": {
    "name": "required-when-creating",
    "description": "optional",
    "appId": "optional-reuse-existing-app"
  },
  "labels": {
    "issued-by": "my-system"
  },
  "controls": {}
}
```

The `application` object is required. When creating a new Application, include
`application.name`. When reusing an existing Application, pass
`application.appId` instead (`name` and `description` are ignored).

Replace:

- `<Environment.appId>`: value from
  `GET /ds/api/v3/gateways/{gatewayId}/products` →
  `products[].environments[].appId`
- `<issuer-token>`: access token for a service account (or user) with
  `CredentialIssuer.Generate`

### Example

```http
POST /ds/api/v3/gateways/{gatewayId}/consumers
Authorization: Bearer <issuer-token>
Content-Type: application/json

{
  "environmentAppId": "<Environment.appId>",
  "application": {
    "name": "tenant-a",
    "description": "Credentials for tenant A"
  },
  "labels": {
    "issued-by": "docs-smoke"
  }
}
```

A successful issue returns `201` and creates an Application (often
**ownerless**), a Consumer, and ServiceAccess. Access is enabled immediately.

Confirm the Consumer in the Portal **Consumers** page (labels and details), then
call the protected upstream with the returned `apiKey` or OAuth client
credentials as appropriate for the flow.

## Regenerate credentials

Rotate secrets or keys **in place** (same `clientId`):

```http
PUT /ds/api/v3/gateways/{gatewayId}/consumers/{clientId}?action=regenerate
Authorization: Bearer <issuer-token>
```

!!! warning
    Regenerate for the `client-jwt-jwks-url` authenticator is **not supported**.
    Issue credentials for that variant only.

## `controls` by flow

| Flow / authenticator   | Typical `controls`                                                                 |
| ---------------------- | ---------------------------------------------------------------------------------- |
| `kong-api-key-only`    | Omit or `{}`                                                                       |
| `kong-api-key-acl`     | Usually omit or `{}` (the Environment `appId` is applied as the ACL group). Optional `aclGroups` for additional groups |
| `client-secret`        | Usually omit or `{}`; optional scopes/roles if the issuer profile expects them     |
| `client-jwt`           | `clientGenCertificate: true` **or** supply `clientCertificate`                     |
| `client-jwt-jwks-url`  | `jwksUrl` **or** `clientCertificate`                                               |

Optional fields such as `defaultClientScopes`, `defaultOptionalScopes`,
`roles`, and `plugins` may also apply depending on the Product Environment and
Authorization Profile.

## Important behaviors

- **Reuse Applications across Environments** by passing `application.appId` from
  a prior issue response. The Consumer `clientId` is typically
  `{environmentAppId}-{applicationAppId}`.
- **Duplicate issue** for the same Application and Environment fails.
- Optional **labels** appear on and can be used to filter the Portal
  **Consumers** page.
- Ownerless Applications created by the issuer are **excluded from My Access**.
- Regenerate rotates secrets/keys in place; the `clientId` does not change.
- Empty or null response fields are stripped from API responses.

## Next steps

- [Manage Consumer Access](/how-to/api-access.md) (approve requests, edit
  controls, revoke)
- [Generate a Service Account](/how-to/generate-service-account.md)
- [Client Credential Protection](/how-to/client-cred-flow.md)
- [Kong API Key](/how-to/kong-api-key.md)
