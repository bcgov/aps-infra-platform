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

**Base path:** `/ds/api/v3/gateways/{gatewayId}/consumers`

| Action     | Method | Path                                                                        | Success |
| ---------- | ------ | --------------------------------------------------------------------------- | ------- |
| Issue      | `POST` | `/ds/api/v3/gateways/{gatewayId}/consumers`                                 | `201`   |
| Regenerate | `PUT`  | `/ds/api/v3/gateways/{gatewayId}/consumers/{clientId}?action=regenerate`    | `200`   |

!!! note
    Revoke is not available on this API yet. Use the Portal **Consumers** page
    to revoke access. See [Manage Consumer Access](/how-to/api-access.md).

For interactive API reference, open the
[Directory API OpenAPI console](https://api.gov.bc.ca/ds/api/v3/console).
Look for the `issue-gateway-consumer` and
`regenerate-gateway-consumer` operations.

## Before you begin

Before you begin, ensure you:

- [Create a Gateway](/how-to/create-gateway.md)
- Configure Product Environments with a [supported flow](#supported-flows)
  (and an Authorization Profile for client-credentials flows)
- Publish Gateway Services and plugins for those Environments — see
  [Create a Gateway Service](/how-to/create-gateway-service.md)
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

## Get `environmentAppId`

The issue request requires `environmentAppId`. This value is **API-only** today
— it is not shown as a field in the Portal Products UI.

1. Sign in to the API Services Portal with `Namespace.Manage` access to the
   Gateway.
2. Open the
   [Directory API OpenAPI console](https://api.gov.bc.ca/ds/api/v3/console).
3. Find `GET /gateways/{gatewayId}/products`, click **Try it out**, enter the
   Gateway ID, and click **Execute**.
4. From the response, copy `[].environments[].appId` for the target
   Environment. Pass that value as `environmentAppId`.

Alternatively, call the endpoint directly with a bearer token:

```http
GET /ds/api/v3/gateways/{gatewayId}/products
Authorization: Bearer <token>
```

See [Getting an access token](/how-to/prom-query.md#getting-an-access-token) for
an example of generating a bearer token from Service Account credentials.

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
  `[].environments[].appId`
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

## Reuse an Application across Environments

The issue response does not return `application.appId` as a separate field.
Derive it from the returned `clientId`, which has the following format:

```text
{environmentAppId}-{applicationAppId}
```

Remove the `{environmentAppId}-` prefix from `clientId`, then pass the remaining
Application ID in a request for another Environment:

```json
{
  "environmentAppId": "<another-Environment.appId>",
  "application": {
    "appId": "<applicationAppId>"
  }
}
```

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

The optional `controls` object customizes the access granted to the Consumer.
Available controls vary by Product Environment flow and Authorization Profile.
Omit `controls` when the flow does not require additional configuration.

| Flow / authenticator   | Typical `controls`                                                                 |
| ---------------------- | ---------------------------------------------------------------------------------- |
| `kong-api-key-only`    | Omit or `{}`                                                                       |
| `kong-api-key-acl`     | Usually omit or `{}` (the Environment `appId` is applied as the ACL group). Optional `aclGroups` for additional groups |
| `client-secret`        | Usually omit or `{}`; optional scopes/roles if the issuer profile expects them     |
| `client-jwt`           | `clientGenCertificate: true` **or** supply `clientCertificate`                     |
| `client-jwt-jwks-url`  | `jwksUrl` **or** `clientCertificate`                                               |

Optional fields such as `defaultClientScopes`, `roles`, and `plugins` may also
apply. The `plugins` control can apply Consumer-specific plugins, including
[rate limiting](/reference/plugins/rate-limiting.md), to a Gateway Service or
route in the Product Environment.

## Important behaviors

- **Duplicate issue** for the same Application and Environment fails.
- Optional **labels** appear on and can be used to filter the Portal
  **Consumers** page.
- Ownerless Applications created by the issuer are **excluded from My Access**,
  but can be viewed on the **Consumers** page.
- Regenerate rotates secrets/keys in place; the `clientId` does not change.
- Empty or null response fields are stripped from API responses.

## Next steps

- [Manage Consumer Access](/how-to/api-access.md) (approve requests, edit
  controls, revoke)
- [Generate a Service Account](/how-to/generate-service-account.md)
- [Client Credential Protection](/how-to/client-cred-flow.md)
- [Kong API Key](/how-to/kong-api-key.md)
