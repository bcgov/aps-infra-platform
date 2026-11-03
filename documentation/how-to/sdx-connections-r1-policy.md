---
title: "Request access with SDX.R1.00"
---

Request service access through your Common SSO (CSS) integration. R1 adds scopes
and, where configured, token exchange across privacy zones.

[Choose a connection policy](/how-to/sdx-connections.md).

!!! note "First iteration - review required"

    This consumer journey is a draft for Service Designer and BA review.
    Confirm the available Common SSO workflow and deployed policy with the APS
    team. It does not implement CSS integration or change authorization policy.
    For the Playground peer-to-peer journey, see
    [Request access with R0](/how-to/sdx-connections-r0-policy.md).

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

### Request access

1. Open the intended CSS integration's SDX access workflow with the required
   integration permissions. Discover the target service and environment, select
   the service version and only the scopes needed by the application. Confirm
   the exact CSS UI entry point with Common SSO; this draft does not prescribe
   an unverified screen label.
2. Submit through the supported CSS/SDX partner integration for `SDX.R1.00`.
   The partner workflow validates the request and populates trusted integration
   metadata. A user management token or an R0 `upsert-connection` example is not
   a replacement for this flow; do not write `requesterDetails` directly.
Continue with [notifications, approval and consumer testing](/how-to/sdx-connection-approval.md).
For R1, that includes CSS scope synchronization before testing.

### Obtain a token and call the service

Use the integration's supported CSS authentication flow to obtain a **user access
token** for the intended environment, scopes and audiences. A Partner API
service-account token authenticates CSS to SDX management; it is not the token
that the consuming application sends to the provider service.

```http
GET <approved-consumer-endpoint>/<documented-operation>
Authorization: Bearer <user-access-token>
```

Follow the [common consumer testing steps](/how-to/sdx-connection-approval.md#consumer-testing)
using this token and the approved consumer endpoint.

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
and [troubleshooting](/how-to/sdx-connections-r1-policy.md#troubleshooting-token-exchange-scopes-and-audiences).
For a same-zone route without token exchange, the original token must already
satisfy the target's trust and authorization requirements.

### Verify, change and retire access

- With the provider/operator, verify the approved service/version and scope set,
  successful/denied calls, and target-zone identity where exchange applies.
- Confirm how the deployed integration handles scope/version changes and
  reapproval before changing an approved request; verify the new CSS grant.
- On rejection/revocation, confirm the removed access is reflected in CSS and
  the provisioned connection. Deactivate and clean up disposable connections
  before deletion using the
  [connection lifecycle instructions](/how-to/sdx-connection-approval.md#connection-management).
- Capture sanitized environment, integration/service identifiers, timestamps and
  observed results for support; omit tokens, credentials and personal data.

Service Designer and BA review, plus an end-to-end CSS/Playground walkthrough,
remain required before this guide is accepted. Publishing TechDocs and changing
R1 policy/CSS behavior are outside APS-5045.

<!-- prettier-ignore -->
!!! note "Associating an OAuth integration client with a connection"
    `requesterDetails.client.clientId` (used for
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

