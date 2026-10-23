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
| Access Manager  | Subsystem-level role for reviewing and approving consumer access |

Use cases:

- Prepare the service implementation for SDX.R1.00
- Register a service
- Verify the service in the SDX Playground
- View API service catalog
- Subsystem management
  - Delete a service

## Prerequisites

- [Install Restish CLI](/reference/restish-cli.md)

## Preparing the service implementation for SDX.R1.00

!!! note "First iteration - review required"

    This provider walkthrough is a documentation draft for review with the
    Service Designer and BA. Confirm the deployed Playground behavior with the
    APS team before using it as production readiness evidence. It does not
    introduce a new testing service or change the authorization policy.

Registration publishes the service description; it does not approve a consumer,
open a connection or prove that the upstream API enforces authorization.
Use this checklist before **Register a service** below.

1. **Identify ownership.** Select the provider organization, subsystem and
   responsible Subsystem Owner. Identify an Access Manager who can review
   consumer requests. Complete [organization onboarding](/how-to/sdx-org-onboarding.md),
   [subsystem setup](/how-to/sdx-subsystems.md) and the required
   [runtime group setup](/how-to/sdx-edge-runtime-groups.md) with the operator.
2. **Select the environment.** Use `apstst` for the SDX Playground; do not copy
   the older generic `lab` example below as the R1 environment selection.
   Resolve the UI, management API and public gateway hosts from
   [SDX Environments](/reference/sdx/environments.md). Keep development, test and
   production upstreams, data and identity registrations separate.
3. **Prepare the API.** Run the implementation at an operator-reachable upstream
   URL with the agreed transport trust. Prepare a valid OpenAPI description
   containing the service/version identity, operations and requested resource
   scopes. Agree the service privacy zone and its identity-provider registration
   with the APS/Common SSO administrators; do not invent a privacy-zone value or
   reuse a consumer client ID as the service identity.
4. **Agree the protection contract.** The R1 provider connection uses the
   `sdx-p2p-provider.r1` pattern. Review the [R1 connection resources](/how-to/sdx-connection-resources.md#sdxr100-policy)
   with the operator, including token validation, Edge request verification,
   response signing and organization transaction signatures. The required provider
   upgrades are `token`, `sign`, `verify` and `counterSign`; the minimal
   connection example is not a complete R1 protection configuration. Confirm the exact
   deployed policy resources and upstream responsibility for scope/operation
   enforcement; OpenAPI security declarations alone do not enforce access.
5. **Prepare a verification case.** Choose one safe operation, synthetic data,
   a participating consumer/CSS integration and an Access Manager. Record the
   expected successful response and an expected denied request without including
   secrets, bearer tokens or personal data in the evidence.

### Environment-specific inputs to confirm

| Input | Where to obtain or verify it |
| --- | --- |
| SDX label and catalogue/Member API hosts | [Environment labels and links](/reference/sdx/environments.md); Playground is `apstst`. |
| Provider organization, subsystem, runtime group and gateway | Your SDX registration and runtime group operator. |
| Upstream URL and TLS trust | The provider deployment and operator; use the target environment's reachable upstream. |
| Service ID/version, advertised scopes and privacy zone | The registered OpenAPI description, service configuration and agreed identity contract. |
| Accepted token issuer, audience and exchanged identity | The deployed R1 policy and APS/Common SSO administrators; these are not interchangeable with a Partner API service-account token. |
| Public runtime-group signing keys | [Public key sets](/reference/sdx/environments.md#public-key-sets) for the selected SDX environment. |

Keep credentials and private keys in the established secret mechanism. For the
current Playground issuer list, use [SDX Playground](/reference/sdx/environments.md#sdx-playground);
production issuer settings are different. A listed issuer is not evidence that
an integration has been approved or activated.

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

### Register in the Playground

The [Restish configuration](/reference/restish-cli.md#configure-the-api) names
its Playground management API alias `sdxstg` and its production alias `sdx`.
Confirm the configured base URL before running a command: the `--environment`
value selects the service environment; it does not change the management API
host. If you use different alias names, substitute your verified Playground
alias throughout registration, catalogue lookup, connection management and deletion.

With the documented `sdxstg` alias pointing to the Playground Member API:

```sh
restish sdxstg upsert-oas-service \
  my-org \
  --subsystem MY-NEW-SUBSYSTEM \
  --environment apstst \
  --upstream-url "https://your-playground-upstream-endpoint" \
  --rsh-header "Content-Type: application/yaml" \
  < openapi.yaml
```

Replace the organization, subsystem, upstream and OpenAPI file with your
prepared inputs. The generic `sdx` / `lab` example above is retained for the
existing workflow; use the verified Playground alias and `apstst` for this R1 walkthrough.

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

## Verify the service in the SDX Playground

This is the current manual verification approach, not a scalable test harness
or an automated readiness certification. Use synthetic data only: Playground
has no data or service quality guarantees.

1. Complete the preparation checklist and register the service for `apstst`
   using the verified Playground management API alias above.
   Use **View API service catalog** below to confirm its identity and retrieve
   the stored OpenAPI description; check version, operations and scopes against
   the implementation. Registration success alone is not an end-to-end test.
2. Agree a consumer and CSS integration with the APS/Common SSO team. Follow
   [Connecting a Service](/how-to/sdx-connections.md) using `SDX.R1.00`; its R0
   Restish example is not an R1 requester payload. The supported partner flow
   must populate trusted integration metadata. Do not edit that metadata directly.
3. Have the provider Access Manager review the requested service, environment,
   version and scopes, then approve the intended access. Confirm activation and
   provisioning on both consumer and provider sides before attempting a call.
4. From the participating consumer, call the agreed safe operation through the
   provisioned SDX endpoint using its approved CSS user access token. Confirm
   the expected response, upstream invocation and transaction/Edge-signature
   evidence where configured. Never substitute the internal upstream URL as
   proof that the SDX route works.
5. Repeat with a missing/invalid token and an unapproved request. Confirm the
   expected denial at the relevant boundary. Verify operation/scope restrictions
   against the agreed enforcement contract; do not assume OAS scopes alone
   restrict runtime access. For cross-zone cases, confirm the provider receives
   the intended target-zone identity with the APS/Common SSO team.
6. Record environment, service/version, connection identity, timestamp,
   sanitized result and any correlation identifier returned. Include the
   reviewer and unresolved failures. Consult the [token-exchange troubleshooting
   guide](/how-to/sdx-connections.md#troubleshooting-token-exchange-scopes-and-audiences)
   for scope/audience errors. Do not record tokens, private keys or personal data.
7. Revoke/deactivate test access and remove provisioned resources through the
   supported connection lifecycle before deleting disposable registrations.
   Confirm no active requests remain, then use **Delete a service** below.

### Review before accepting the provider guide

- Service Designer and BA confirm terminology, roles and placement in the journey.
- Provider, consumer and operator walk through registration, catalogue lookup,
  approval, successful/denied calls and cleanup in the current Playground.
- APS/Common SSO confirm environment-specific identity values and any policy
  activation dependencies. Record gaps rather than presenting them as completed.

Publishing TechDocs and designing the future service readiness test harness
(APS-5048) are outside this first iteration.

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
