---
title: "Connecting a Service"
---

This page shows how to make a connection between your system
and another on the Secure Data Exchange.

SDX supports different authorization models, which are identified by a `policyVersion`
when a connection request is submitted. The following policies are supported:

| Policy      | Description                                                                                                                           |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| `SDX.R0.00` | Simple peer-to-peer connection policy. Requires a `requesterDetails` object (see below). Available only in the SDX Playground.        |
| `SDX.R1.00` | Adds Common SSO, token-exchange and scopes support; requires additional requester and gateway resources and is not a drop-in default. |

This guide focuses on the `SDX.R0.00` policy where it establishes a basic peer-to-peer connection.
It is only available in the SDX Playground environment.

Policy `SDX.R1.00` is part of a collaboration with Common SSO (CSS) where CSS integrations will
be able to request API and scope access through their tool and have the connection request
managed in SDX for approvals. SDX will send events to CSS when connections have
been approved/revoked so that the appropriate scopes can be provisioned in Keycloak. For clients
that call services across privacy zones, SDX will perform an exchange of the token so that
the subject identifier properly identifies the user in the target privacy zone.

The steps described in this page are performed by the following roles:

| Role           | Function                                                             |
| -------------- | -------------------------------------------------------------------- |
| Tech Lead      | For service clients, request/revoke connections to another service   |
| Access Manager | For service providers, review and approve client connection requests |

Use cases:

- Consumer setup with SDX.R1.00 and Common SSO
- Request access (as consumer)
- Review connection access requests
- Approve access (as provider)
- Open a connection
  - Consumer side
  - Provider side
- Connection management
  - Delete a connection request

## Prerequisites

- [Install Restish CLI](/reference/restish-cli.md)

## Consumer setup with SDX.R1.00 and Common SSO

!!! note "First iteration - review required"

    This consumer journey is a draft for Service Designer and BA review.
    Confirm the available Common SSO workflow and deployed policy with the APS
    team. It does not implement CSS integration or change authorization policy.
    Keep the R0 Restish examples below for their existing use case; they are not
    a complete R1 consumer onboarding procedure.

### Roles, prerequisites and resources

| Participant | Responsibility |
| --- | --- |
| Consumer System Admin / Subsystem Owner | Establish organization/subsystem ownership and request the intended service access. |
| Consumer CSS integration owner | Maintain the correct integration, OAuth client and privacy-zone registration; configure the application to obtain appropriate user access tokens. |
| Provider Access Manager | Review and approve/reject the requested service, version, environment and scopes, and revoke access when required. |
| Runtime group operator and APS/Common SSO administrators | Confirm gateway readiness, identity trust, token-exchange permissions and environment-specific integration setup. |

Before requesting access:

- Complete [organization onboarding](/how-to/sdx-org-onboarding.md) and
  [subsystem registration](/how-to/sdx-subsystems.md). Associate the intended CSS
  OAuth client with the consumer subsystem through the supported setup process.
  An integration/request identifier and its OAuth client ID are distinct values.
- Select the [SDX environment](/reference/sdx/environments.md): `apstst` is the
  Playground; production/nonproduction data labels and identity issuers differ.
  Use the appropriate catalogue, Member API and gateway endpoints from that page.
- Identify the provider service/version, required operations and minimum scopes
  from the service catalogue/OpenAPI description. Agree the consumer privacy
  zone and required target resource audiences with the provider and APS team.
- Confirm both participating [runtime groups and gateways](/how-to/sdx-edge-runtime-groups.md)
  are ready. R1 uses
  `sdx-p2p-consumer-access.r1` and `sdx-p2p-consumer.r1` on the consumer side,
  and `sdx-p2p-provider.r1` on the provider side; see
  [Connection Resources](/how-to/sdx-connection-resources.md#sdxr100-policy).

### Request access and confirm approval

1. Open the intended CSS integration's SDX access workflow with the required
   integration permissions. Discover the target service and environment, select
   the service version and only the scopes needed by the application. Confirm
   the exact CSS UI entry point with Common SSO; this draft does not prescribe
   an unverified screen label.
2. Submit through the supported CSS/SDX partner integration for `SDX.R1.00`.
   The partner workflow validates the request and populates trusted integration
   metadata. A user management token or an R0 `upsert-connection` example is not
   a replacement for this flow; do not write `requesterDetails` directly.
3. The provider Access Manager reviews the request through the deployed
   catalogue/access interface or supported management workflow. Wait for the
   intended service, environment, version and scopes to be approved; submission
   success is not approval, activation or callback delivery.
4. Confirm approved access has been synchronized back to CSS. SDX sends the
   approved-access snapshot to CSS, which provisions the allowed scopes for the
   integration. If the callback fails or expected scopes are absent, ask the
   APS/Common SSO team to inspect delivery and registration before requesting
   broader permissions. Never share credentials or tokens in a support ticket.
5. Have the operator confirm the connection is active and both sides are
   provisioned. Record the actual consumer invocation endpoint from the deployed
   connection; do not derive it by concatenating catalogue identifiers.

### Obtain a token and call the service

Use the integration's supported CSS authentication flow to obtain a **user access
token** for the intended environment, scopes and audiences. A Partner API
service-account token authenticates CSS to SDX management; it is not the token
that the consuming application sends to the provider service.

```http
GET <approved-consumer-endpoint>/<documented-operation>
Authorization: Bearer <user-access-token>
```

Use the API's actual method/path and synthetic test data for Playground. Keep
private credentials out of command history and shared transcripts. Confirm the
expected response through SDX, and verify missing/invalid-token and unapproved
access cases with the provider. A direct call to the upstream API does not prove
that the provisioned SDX connection is working.

### How token exchange crosses privacy zones

When configured for a cross-zone request, the consumer Edge Runtime first
validates the original CSS token, then asks the authorization server to exchange
it for the target privacy-zone identity. The resulting token is forwarded through
SDX to the provider. Exchange is an identity translation step, not a grant of
additional service access or broader scopes.

The verified token supplies the scope and audience context. The original token must satisfy the consumer endpoint's configured issuer and
audience checks before exchange. The SDX exchange client must also be an allowed
audience in the original token and be permitted to
request the required scopes/audiences. Confirm privacy-zone scope configuration
and activation dependencies with APS/Common SSO; the documented APS-4931 scope
transfer does not itself compose the target privacy-zone scope. Do not assume
exchange is enabled for every connection or that matching HTTP success alone
proves correct target-zone identity.

See the authoritative [scope and audience behavior](/how-to/sdx-connection-resources.md#token-exchange-scopes)
and [troubleshooting](/how-to/sdx-connections.md#troubleshooting-token-exchange-scopes-and-audiences).
For a same-zone route without token exchange, the original token must already
satisfy the target's trust and authorization requirements.

### Playground walkthrough record

Use this record with the consumer, provider and APS/Common SSO teams before
accepting the draft. Record the date, deployed version and sanitized identifiers;
mark a check as pending when the deployed workflow cannot support it yet.
Do not record token contents or personal subject identifiers.

| Check | Evidence to record |
| --- | --- |
| Request | Environment, CSS integration ID, OAuth client ID, consumer subsystem, provider service/version and requested scopes. |
| Approval and provisioning | Approved scope set, provider approval, CSS synchronization result and operator confirmation that both sides are active. |
| Allowed call | Actual consumer endpoint and documented operation, timestamp, expected response and observed result using synthetic data. |
| Denied call | Provider-agreed missing/invalid-token and unapproved-access cases, expected denial and observed result. |
| Cross-zone identity, when applicable | Operator confirmation of exchange and provider confirmation of the intended target-zone identity and authorization, without copying identity values. |
| Revocation and cleanup | CSS grant removal, denied access after revocation, and operator confirmation of disposable connection cleanup. |

If scopes, audiences or identity differ from the agreed values, retain the failed
check and its sanitized support/request ID. Resolve it with the responsible team
before treating the walkthrough as passed.

### Verify, change and retire access

- With the provider/operator, verify the approved service/version and scope set,
  successful/denied calls, and target-zone identity where exchange applies.
- Confirm how the deployed integration handles scope/version changes and
  reapproval before changing an approved request; verify the new CSS grant.
- On rejection/revocation, confirm the removed access is reflected in CSS and
  the provisioned connection. Deactivate and clean up disposable connections
  before deletion using the lifecycle instructions below.
- Capture sanitized environment, integration/service identifiers, timestamps and
  observed results for support; omit tokens, credentials and personal data.

Service Designer and BA review, plus an end-to-end CSS/Playground walkthrough,
remain required before this guide is accepted. Publishing TechDocs and changing
R1 policy/CSS behavior are outside APS-5045.

## Request access (as consumer)

=== "Restish CLI"

    Help information about the operation:

    ```sh
    restish sdx upsert-connection
    ```

    Example call:

    ```sh
    restish sdx upsert-connection \
      my-org \
      clientId: MIN.MYORG.MY-NEW-SUBSYSTEM, \
      serviceId: LAB.MIN.MYORG.EFV-ICBC.v0, \
      policyVersion: SDX.R0.00, \
      "requesterDetails: {}"
    ```

!!! note "requester details"

    Under `SDX.R0.00`, `requesterDetails` must be supplied together with
    `policyVersion` on this initial request — when both are present, the
    controller replaces `requesterDetails.requester` with the authenticated
    caller's name and email. Omitting `requesterDetails` leaves an invalid
    empty default in place that will pass creation but fail activation.
    `requesterDetails` can only be set on creation; it cannot be repaired
    afterwards through `upsert-connection` (that field is reserved for the
    provisioner on update) — if activation fails for a missing requester
    record, deactivate and delete the connection, then recreate it with
    `policyVersion` and `requesterDetails` included together.

## Review connection access requests

=== "Restish CLI"

    Help information about the operation:

    ```sh
    restish sdx list-connections
    ```

    Example call:

    ```sh
    restish sdx list-connections \
      my-org
    ```

## Approve access (as provider)

=== "Restish CLI"

    Help information about the operation:

    ```sh
    restish sdx update-connection-approval
    ```

    Example call:

    ```sh
    restish sdx update-connection-approval \
      my-org \
      clientId: MIN.MYORG.MY-NEW-SUBSYSTEM, \
      serviceId: LAB.MIN.MYORG.EFV-ICBC.v0, \
      isApproved: true, isActive: true
    ```

## Open a connection

Once the connection request has been approved, both sides are able to publish the
routing rules for opening a channel between the two systems.

### Consumer side

=== "Restish CLI"

    Help information about the operation:

    ```sh
    restish sdx upsert-connection
    ```

    Prepare a pattern input file (`client-input.json`) for the Consumer:

    ```json
    {
      "gatewayPatterns": {
        "sdx-p2p-consumer.r1": {
          "upgrades": {
            "sign": {},
            "verify": {}
          }
        }
      }
    }
    ```

    Example call:

    ```sh
    restish sdx upsert-connection \
      my-org \
      clientId: MIN.MYORG.MY-NEW-SUBSYSTEM, \
      serviceId: LAB.MIN.MYORG.EFV-ICBC.v0, \
      clientResources: @client-input.json

    ```

For details on configuring the `sdx-p2p-consumer.r1` pattern,
go to [Connection Resources](/how-to/sdx-connection-resources.md).

### Provider side

=== "Restish CLI"

    Help information about the operation:

    ```sh
    restish sdx upsert-connection
    ```

    Prepare a pattern input file (`service-input.json`) for the Provider:

    ```json
    {
      "gatewayPatterns": {
        "sdx-p2p-provider.r1": {
          "upgrades": {
            "mtlsAuth": {},
            "sign": {},
            "verify": {}
          }
        }
      }
    }
    ```

    Example call:

    ```sh
    restish sdx upsert-connection \
      my-org \
      clientId: MIN.MYORG.MY-NEW-SUBSYSTEM, \
      serviceId: LAB.MIN.MYORG.EFV-ICBC.v0, \
      serviceResources: @service-input.json
    ```

For details on configuring the `sdx-p2p-provider.r1` pattern,
go to [Connection Resources](/how-to/sdx-connection-resources.md).

<!-- prettier-ignore -->
!!! note "Associating an OAuth integration client with a connection"
    `requesterDetails.client.clientId` (used above for
    `sdx-p2p-consumer-access.r1`/ACL and, when configured, `consumerMatch`)
    is provisioner-managed. It cannot be written directly through the SDX
    management API — attempting a direct `upsert-connection` update of
    `requesterDetails` returns `HTTP 400`. Registering an
    `integrationClientId` on the consumer subsystem (see
    [Register an SDX Subsystem](/how-to/sdx-subsystems.md)) is only the
    first half of the relationship: the field is populated by calling the
    supported `POST /v1/integrations/{clientId}/access-requests` operation
    on the SDX Partner Authorization Services API, which validates the
    requested scopes against the registered OAD and writes the requester
    metadata with trusted provisioner credentials. That API uses a separate
    base URL and bearer-token audience from the main SDX API — consult the
    APS team for the current Restish/API configuration for it. Before
    enabling strict `consumerMatch`, verify that the connection contains the
    integration client and that the Kong consumer created by
    `sdx-p2p-consumer-access.r1` exists, since enabling `consumerMatch`
    ahead of a matching consumer blocks legitimate traffic.

## Troubleshooting token-exchange scopes and audiences

### Original token does not authorize the SDX exchange client

When token exchange is enabled, the verified original token's `aud` claim must
contain the consumer `tokenExchange.clientId`. If the value is missing, the
claim is malformed, or it is not a string or array of strings, SDX returns HTTP
400 without calling the authorization server:

```json
{
  "message": "The supplied token is not authorized for SDX token exchange. Refer to the SDX documentation and use request ID <request-id> when requesting support.",
  "error": {
    "code": "SDX_TOKEN_EXCHANGE_NOT_AUTHORIZED"
  }
}
```

The `<request-id>` in the message matches the `X-Kong-Request-Id` response
header and the diagnostic SDX Kong log entry. The public response does not
contain the original audiences, configured client ID, token, or authorization
server details.

The requesting client is responsible for requesting any audience required by
the provider API or another downstream resource. SDX propagates those verified
original audiences and removes exact duplicates. Retaining the SDX exchange
client allows the provider to use the exchanged token for a subsequent SDX
call. An original token containing only the SDX exchange client is valid when
no target resource requires another audience.

The optional plugin setting `tokenExchange.audience` adds one configured
audience to the exchange request. When present, SDX merges it with the verified
original audiences and removes duplicates. This supports both connections that
use a configured audience and connections whose target audiences are already
present in the original token. Current provisioning policies may continue to
require or supply the configured value.

### Original token has no usable scope claim (E4)

Verified-subject scope derivation fails before the token endpoint is called
when the verified token is unavailable, its `scope` claim is missing or is not
a string, or the claim is empty or contains only whitespace. Each condition
returns HTTP 500:

```json
{
  "message": "Token exchange failed",
  "error": { "code": "E4" }
}
```

This E4 response does not include a request ID. Kong logs `Unable to derive
token exchange scopes:` followed by `verified subject token is unavailable`,
`verified subject token has no string scope claim`, or `verified subject token
has an empty scope claim`.

### SDX exchange client cannot request a scope or audience

The SDX token-exchange client must be permitted to request every scope and
audience sent in the exchange. If the authorization server rejects the exchange
because a requested scope or audience is unavailable, SDX returns HTTP 500 with
a generic response:

```json
{
  "message": "The SDX token-exchange client is not configured to complete this request. Refer to the SDX Kong token-exchange plugin logs using request ID <request-id> for details.",
  "error": {
    "code": "SDX_TOKEN_EXCHANGE_CONFIGURATION_ERROR"
  }
}
```

The `<request-id>` in the message matches the `X-Kong-Request-Id` response
header. Provide that value to the SDX support team. SDX operators can use it to
find the diagnostic entry in the Kong token-exchange plugin logs. That entry
records the authorization server status and error code, requested scopes, and
audiences.

The client response does not include the requested scopes, audience,
authorization server response or error description, client assertion, or
tokens.

An explicit granted scope set that differs from the requested set is a warning,
not an exchange failure. SDX continues with the successful exchanged token, and
the provider's normal token validation and authorization rules apply.

## Connection management

### Deleting a connection

Deleting a connection request is two steps. First step is to make it inactive:

```sh
restish sdx upsert-connection \
  my-org \
  clientId: MIN.MYORG.MY-NEW-SUBSYSTEM, \
  serviceId: LAB.MIN.MYORG.EFV-ICBC.v0, \
  isActive: false
```

Then the connection can be deleted using its unique identifier.

=== "Restish CLI"

    Help information about the operation:

    ```sh
    restish sdx delete-connection
    ```

    Example call:

    ```sh
    restish sdx delete-connection \
      ministry-of-citz 2010
    ```

=== "Reference"

    - **API** `DELETE /organizations/{org}/connections/{id}`

    Parameters:

    - `{org}=<your-organization>`
    - `{id}=<connection-request-id>`

    The `{org}` value can be the consumer organization or the provider
    organization for the connection request.

    Successful response:

    ```json
    {
      "result": "deleted",
      "id": "1"
    }
    ```

    If gateway configuration still exists on either side, the request is
    rejected. Remove the remaining gateway configuration and try again.
