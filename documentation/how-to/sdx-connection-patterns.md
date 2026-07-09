---
title: "Connection Gateway Patterns"
---

Gateway patterns for peer-to-peer will have different rules over time around how
they should be configured. This page describes all the parameters that are available.

## Connection Request

- following parameters MUST by set: `clientId`, `serviceId`

| Parameter          | Type    | Rule     |
| ------------------ | ------- | -------- |
| `clientId`         | string  | required |
| `serviceId`        | string  | required |
| `isApproved`       | boolean | required |
| `isActive`         | boolean | required |
| `requesterDetails` | object  | optional |
| `clientResources`  | object  | optional |
| `.gatewayPatterns` | object  | optional |
| `serviceResources` | object  | optional |
| `.gatewayPatterns` | object  | optional |

`isApproved` is set by the service system owner.

### clientResources.gatewayPatterns

| Parameter                      | Type    | Rule                      |
| ------------------------------ | ------- | ------------------------- |
| **sdx-p2p-consumer-access.r1** | object  | required                  |
|                                |         |                           |
| **sdx-p2p-consumer.r1**        | object  | required                  |
| `.tlsVerify`                   | boolean | optional, default `true`  |
| `.stripPath`                   | boolean | optional, default `false` |
| `.upgrades`                    | object  | optional                  |

**upgrades:**

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

**upgrades:**

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
