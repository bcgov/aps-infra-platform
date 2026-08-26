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

## Connection Request

- following parameters MUST by set: `clientId`, `serviceId`

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
