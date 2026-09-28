---
title: "Connection Resources"
---

Connection resources for peer-to-peer will have different rules over time around how
they should be configured. This page describes all the parameters that are available.

!!! note "These patterns are not invoked directly"

    `sdx-p2p-consumer.r1`, `sdx-p2p-consumer-access.r1`, `sdx-p2p-provider.r1`,
    and their `upgrades` are **connection resources**, not gateway patterns
    invoked through the public `/patterns` endpoint or
    `provision-config-from-pattern`. You configure them by setting
    `clientResources.gatewayPatterns` (consumer side) and
    `serviceResources.gatewayPatterns` (provider side) on a connection via
    `upsert-connection`, as shown in
    [Connecting a Service](/how-to/sdx-connections.md). The provisioner
    evaluates them automatically whenever the connection's `isActive` state
    changes — there is no separate preview/publish/delete step for these
    patterns, and deleting a peer-to-peer configuration is done by setting
    `isActive: false` on the connection rather than by deleting the pattern
    directly.

## All Parameters

- The following parameters MUST be set: `clientId`, `serviceId`

| Parameter          | Type    | Rule                    |
| ------------------ | ------- | ----------------------- |
| `clientId`         | string  | required                |
| `serviceId`        | string  | required                |
| `isApproved`       | boolean | optional; default=false |
| `isActive`         | boolean | optional; default=false |
| `requesterDetails` | object  | optional                |
| `clientResources`  | object  | optional                |
| `.gatewayPatterns` | object  | optional                |
| `serviceResources` | object  | optional                |
| `.gatewayPatterns` | object  | optional                |

`isApproved` is set by a user with the "Access Manager" subsystem role.

### requesterDetails

| Parameter               | Type          | Rule     |
| ----------------------- | ------------- | -------- |
| `.client`               | object        | optional |
| `.client.integrationId` | string        | optional |
| `.client.clientId`      | string        | optional |
| `.client.privacyZone`   | string        | optional |
| `.requester`            | object        | required |
| `.requester.name`       | string        | required |
| `.requester.email`      | string        | optional |
| `.scopes`               | set of string | optional |
| `.service`              | object        | optional |
| `.service.clientId`     | string        | optional |
| `.submissionId`         | string        | optional |

### clientResources.gatewayPatterns

| Parameter                      | Type    | Rule                              |
| ------------------------------ | ------- | --------------------------------- |
| **sdx-p2p-consumer-access.r1** | object  | required                          |
| `.integrationClientId`         | string  | optional, example `325`           |
|                                |         |                                   |
| **sdx-p2p-consumer.r1**        | object  | required                          |
| `.tlsVerify`                   | boolean | optional, default `true`          |
| `.stripPath`                   | boolean | optional, default `false`         |
| `.clientRuntimeOverride`       | string  | optional, example `MIN.CITZ.pzgw` |
| `.upgrades`                    | object  | optional                          |

#### sdx-p2p-consumer upgrades

| Parameter                      | Type     | Rule                |
| ------------------------------ | -------- | ------------------- |
| **sign**                       | object   | optional            |
|                                |          |                     |
| **verify**                     | object   | optional            |
|                                |          |                     |
| **counterSign**                | object   | optional            |
|                                |          |                     |
| **dpop**                       | object   | optional            |
|                                |          |                     |
| **token**                      | object   | optional            |
| `.allowedAud`                  | string   | optional            |
| `.allowedIss`                  | string[] | required            |
| `.scope`                       | string   | optional            |
| `.consumerMatch`               | boolean  | optional            |
| `.consumerMatchClaim`          | string   | optional            |
| `.consumerMatchClaimCustomId`  | boolean  | optional            |
| `.consumerMatchIgnoreNotFound` | boolean  | optional            |
|                                |          |                     |
| **acl**                        | object   | optional            |
|                                |          |                     |
| **tokenExchange**              | object   | optional            |
| `.clientId`                    | string   | required            |
| `.tokenEndpoint`               | string   | required, any value |
| `.scopes`                      | string[] | optional fallback   |
| `.audience`                    | string   | required for verified SDX token exchange |

### serviceResources.gatewayPatterns

| Parameter               | Type   | Rule     |
| ----------------------- | ------ | -------- |
| **sdx-p2p-provider.r1** | object | required |
| `.upstreamUrl`          | string | optional |
| `.upgrades`             | object | optional |

#### sdx-p2p-provider upgrades

| Parameter                      | Type     | Rule     |
| ------------------------------ | -------- | -------- |
| **mtlsAuth**                   | object   | optional |
|                                |          |          |
| **mtlsAcl**                    | object   | optional |
|                                |          |          |
| **sign**                       | object   | optional |
|                                |          |          |
| **verify**                     | object   | optional |
|                                |          |          |
| **counterSign**                | object   | optional |
|                                |          |          |
| **token**                      | object   | optional |
| `.allowedAud`                  | string   | optional |
| `.allowedIss`                  | string[] | required |
| `.scope`                       | string   | optional |
| `.consumerMatch`               | boolean  | optional |
| `.consumerMatchClaim`          | string   | optional |
| `.consumerMatchClaimCustomId`  | boolean  | optional |
| `.consumerMatchIgnoreNotFound` | boolean  | optional |
|                                |          |          |
| **acl**                        | object   | optional |

## SDX.R1.00 Policy

The `SDX.R1.00` policy adds Common SSO tokens for client authentication,
token-exchange for crossing privacy zones, and resource scopes.

### Service Client

Both `sdx-p2p-consumer-access.r1` and `sdx-p2p-consumer.r1` patterns are
required.

The following upgrades to `sdx-p2p-consumer.r1` are required:

| Upgrade         | Purpose                                                                                       |
| --------------- | --------------------------------------------------------------------------------------------- |
| `token`         | Verify access token issued by an approved IAM provider (authorized party: client integration) |
| `acl`           | Verify client represents the SDX client subsystem                                             |
| `tokenExchange` | Connected Services Link - Initiate token exchange for cross-privacy zone requests             |
| `sign`          | Standard Edge Runtime token added as an `X-Edge-Token` header                                 |
| `verify`        | Verification of Edge Runtime token on response from Provider                                  |
| `counterSign`   | Client organization transaction signature on request                                          |

#### Token exchange scopes

When the `token` and `tokenExchange` upgrades are used together, SDX obtains
the requested scopes from the `scope` claim in the token already verified by
the `token` upgrade. Duplicate values are removed, and the resulting list is
sent to the authorization server in the token-exchange request. This prevents
the exchange from defaulting to every scope available to the SDX exchange
client.

The `tokenExchange.scopes` setting is retained as a compatibility fallback for
a route without verified-token context. It does not override the verified
subject token's scopes. Normal `SDX.R1.00` connections should use the `token`
upgrade before `tokenExchange` and should not rely on the fallback to change a
caller's requested scopes.

The successful token response may omit `scope` when the granted scopes match
the request, as defined by
[RFC 8693 section 2.2.1](https://www.rfc-editor.org/rfc/rfc8693.html#section-2.2.1).
If the response declares a different scope set, SDX logs the requested and
granted sets as a warning and continues with the exchanged token. SDX does not
decode or introspect the exchanged token to perform this comparison.

#### Token exchange audiences

The consumer `tokenExchange` upgrade uses three audience inputs for different
purposes:

| Audience | Where it is supplied | Requirement and purpose |
| -------- | -------------------- | ----------------------- |
| Consumer endpoint audience | Original token `aud`; checked through `token.allowedAud` | The original token must satisfy the consumer endpoint's normal token validation. |
| SDX exchange client | `tokenExchange.clientId` and original token `aud` | Required in the original token when token exchange is enabled. It authorizes this SDX client to exchange the token. |
| Provider resource audience | `tokenExchange.audience` | Required consumer-side configuration. SDX always requests it for the exchanged token, so the requesting client does not need to know or request this audience. |
| Optional downstream audiences | Original token `aud` | Optional. SDX preserves them when a downstream client needs to perform another permitted exchange. |

SDX reads `aud` only from the token already verified by the `token` upgrade. It
accepts a string or an array, requires an exact match for
`tokenExchange.clientId`, and removes that client from the outgoing audience
set. SDX then combines the configured `tokenExchange.audience` with all
remaining original audiences and removes exact duplicates. The configured
audience is sent first, and every value is encoded as a separate RFC 8693
`audience` parameter.

For example:

```text
Configured consumer audience:
  provider-resource

Original token aud:
  [sdx-exchange-client, provider-resource, downstream-client]

Token-exchange request:
  audience=provider-resource
  audience=downstream-client
```

The provider resource audience in the original token is redundant in this
example and is sent only once. The optional downstream audience can allow that
client to use the exchanged token in a later permitted exchange. When the
original token contains no optional audience, SDX requests only the configured
consumer audience.

Without the `tokenExchange` upgrade, SDX does not replace the bearer token. The
requesting client must then obtain an original token that already contains the
audience expected by the target resource.

Keycloak must be able to resolve every requested audience through the SDX
exchange client's roles, client scopes, and audience mappers. Explicit
`audience` parameters constrain the intended recipients; they do not make an
otherwise unavailable audience resolvable.

### Service Provider

`sdx-p2p-provider.r1` pattern is required.

The following upgrades to this pattern are required:

| Upgrade       | Purpose                                                                        |
| ------------- | ------------------------------------------------------------------------------ |
| `token`       | Verify access token issued by an approved IAM provider (authorized party: SDX) |
| `sign`        | Standard Edge Runtime token added as an `X-Edge-Token` response header         |
| `verify`      | Verification of Edge Runtime token on request from Client                      |
| `counterSign` | Service organization transaction signature on response                         |
