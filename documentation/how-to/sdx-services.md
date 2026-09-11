---
title: "Managing Services"
---

## Overview

This page shows how to manage services on the Secure Data Exchange.

The steps described in this page are performed by users with the following roles:

| Role            | Function                                                     |
| --------------- | ------------------------------------------------------------ |
| System Admin    | Organization-level role for managing subsystems and services |
| Subsystem Owner | Subsystem-level role for managing services for a subsystem   |

Use cases:

- Register a service
- View API service catalog
- Subsystem management
  - Delete a service

## Prerequisites

- [Install Restish CLI](/reference/restish-cli.md)

## Register a service

To register a service, you need to identify the `environment` you are deploying the service
to, the `upstream URL` for routing to where your service is running,
and the OpenAPI specification itself.

For details about valid `environment` values, visit [Environment labels](/reference/sdx/environments.md#environment-labels).

=== "Restish CLI"

    Help information about the operation:

    ```sh
    restish sdx upsert-oas-service
    ```

    Example:

    ```sh
    restish sdx upsert-oas-service \
      my-org \
      --subsystem MY-NEW-SUBSYSTEM \
      --environment lab \
      --upstream-url "https://your-upstream-endpoint" \
      --rsh-header "Content-Type: application/yaml" \
      < openapi.yaml
    ```

!!! note "OAS security scopes are not automatically enforced"

    Distinct OpenAPI `security` scopes declared per-operation (read, create,
    update, delete, etc.) are **not** automatically converted into
    route-level runtime authorization. Registering an OAS that declares
    scopes does not by itself restrict which operations a caller with a
    valid token can reach. Runtime access control must be configured
    explicitly through connection `upgrades` — see the `token`,
    `consumerMatch`, and `tokenExchange` options in
    [Connection Resources](/how-to/sdx-connection-resources.md) and the
    [JWT Keycloak plugin](/reference/plugins/jwt-keycloak.md) — and, as
    deployed today, the JWT guard verifies the token's signature, issuer,
    expiry, and `sub`, but does not itself verify `scope`, audience, or
    authorized party. Treat declared OAS scopes as descriptive metadata
    until per-operation enforcement is explicitly configured.

### Troubleshooting service registration

An `upsert-oas-service` request can return `HTTP 503`,
`validation_service_unavailable`, `OAS validation service unavailable` for
two different reasons that look identical to the caller:

- the validation service is genuinely unreachable or timed out, or
- the validation service is reachable and responded, but its internal rules
  engine failed to process the document (for example, a Spectral rule
  throwing on a legitimate `null` value in the document).

Both cases currently surface as the same `503`. If you hit this error:

- retry once to rule out a transient network/timeout issue;
- if it persists, check whether the validator's `/versions` endpoint is
  reachable and returning `200` — if it is, the failure is more likely in
  the rules engine than in service availability;
- if the failure appears tied to a specific document construct (for
  example, a nullable field with an explicit `null` example value), report
  it to the APS team with the offending OAS fragment rather than continuing
  to retry.

## View API service catalog

=== "Restish CLI"

    List all subsystems:

    ```sh
    restish sdx subsystems-list
    ```

    List only name and title of APIs:

    ```sh
    restish sdx list-service-catalog | jq '.[] | .name+": "+.title'
    ```

### Retrieve a service's OpenAPI Description (OAD)

The registered OAD for a service can be retrieved two ways:

- publicly, with no credentials required:

  ```text
  GET /ds/api/sdx/v1/catalog/services/{serviceId}/oas-spec
  ```

- organization-scoped, requiring `System.Manage`, via the
  `get-organization-service-spec` Restish operation.

Neither operation returns the fully SDX-transformed publication artifact
described by the SDX API Standard. The stored document is
validation-enriched only — registration adds `x-csbc-api-standard` and
`x-csbc-api-standard-ruleset` under `info`, recording the validation
service's version and ruleset — but the `servers` section, OAuth endpoints,
and provider `info.contact` are otherwise returned as uploaded, and no SDX
`externalDocs` is added. Do not assume the retrieved document's `servers` or
OAuth URLs are environment-correct without further transformation.

`x-csbc-api-standard` here records the validation service version, not a
provider-declared API standard release name; treat its meaning as
implementation-specific until this is reconciled with the SDX API Standard.

An interactive Swagger UI is not currently provided through SDX for a
registered service; only the OAD retrieval operations above are available.

## Service management

### Delete a service

A service can be deleted when there are no active connection requests for it.

=== "Restish CLI"

    Help information about the operation:

    ```sh
    restish sdx delete-organization-oas-service
    ```

    Example:

    ```sh
    restish sdx delete-organization-oas-service \
      my-org SERVICE-NAME
    ```

The delete request will not proceed if the service has active connection requests.

After a service is deleted, the same service name can be used again.

## Next steps

- [Connecting a Service](/how-to/sdx-connections.md)
