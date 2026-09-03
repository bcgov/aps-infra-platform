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
| `isApproved`       | boolean | required; default=false |
| `isActive`         | boolean | required; default=false |
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
| `.scopes`                      | string[] | optional            |
| `.audience`                    | string   | optional            |

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

### Service Provider

`sdx-p2p-provider.r1` pattern is required.

The following upgrades to this pattern are required:

| Upgrade       | Purpose                                                                        |
| ------------- | ------------------------------------------------------------------------------ |
| `token`       | Verify access token issued by an approved IAM provider (authorized party: SDX) |
| `sign`        | Standard Edge Runtime token added as an `X-Edge-Token` response header         |
| `verify`      | Verification of Edge Runtime token on request from Client                      |
| `counterSign` | Service organization transaction signature on response                         |
