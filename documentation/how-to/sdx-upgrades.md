---
title: "Connection Gateway Patterns"
---

Gateway patterns for peer-to-peer will have different rules over time around how
they should be configured. This page describes the rules for each policy release.

## **SDX.R0.00**

This policy makes all controls/upgrades optional - it only opens up the connection
between the two subsystems. This will be used in development only. Test and
production will require certain controls to be configured in a particular way.

### Connection Request

- following parameters MUST by set: `clientId`, `serviceId`

| Parameter    | Type    | Rule     |
| ------------ | ------- | -------- |
| `clientId`   | string  | required |
| `serviceId`  | string  | required |
| `isApproved` | boolean | required |

`isApproved` is set by the service system owner.

### Pattern sdx-p2p-consumer.r1

- following parameters MUST be set: `conn_id`, `client_id`, `service_id`
- following parameters MAY be set: `tls_verify`, `upgrades`

| Parameter    | Type    | Rule                     |
| ------------ | ------- | ------------------------ |
| `conn_id`    | string  | required                 |
| `client_id`  | string  | required                 |
| `service_id` | string  | required                 |
| `tls_verify` | boolean | optional, default `true` |
| `upgrades`   | object  | optional                 |

**upgrades:**

| Parameter                          | Type     | Rule                |
| ---------------------------------- | -------- | ------------------- |
| **sign**                           | object   | optional            |
|                                    |          |                     |
| **verify**                         | object   | optional            |
|                                    |          |                     |
| **counter_sign**                   | object   | optional            |
|                                    |          |                     |
| **dpop**                           | object   | optional            |
|                                    |          |                     |
| **token**                          | object   | optional            |
| `.allowed_aud`                     | string   | required            |
| `.allowed_iss`                     | string[] | required            |
| `.scope`                           | string   | optional            |
| `.consumer_match`                  | boolean  | optional            |
| `.consumer_match_claim`            | string   | optional            |
| `.consumer_match_claim_custom_id`  | boolean  | optional            |
| `.consumer_match_ignore_not_found` | boolean  | optional            |
|                                    |          |                     |
| **token_exchange**                 | object   | optional            |
| `.client_id`                       | string   | required            |
| `.token_endpoint`                  | string   | required, any value |
| `.scopes`                          | string[] | optional            |
| `.audience`                        | string   | optional            |

### Pattern sdx-p2p-provider.r1

- following parameters MUST be set: `conn_id`, `client_id`, `service_id`
- following parameter MAY be set: `upgrades`

| Parameter    | Type   | Rule     |
| ------------ | ------ | -------- |
| `conn_id`    | string | required |
| `client_id`  | string | required |
| `service_id` | string | required |
| `upgrades`   | object | optional |

**upgrades:**

| Parameter                          | Type     | Rule     |
| ---------------------------------- | -------- | -------- |
| **mtls_auth**                      | object   | optional |
|                                    |          |          |
| **mtls_acl**                       | object   | optional |
|                                    |          |          |
| **sign**                           | object   | optional |
|                                    |          |          |
| **verify**                         | object   | optional |
|                                    |          |          |
| **counter_sign**                   | object   | optional |
|                                    |          |          |
| **token**                          | object   | optional |
| `.allowed_aud`                     | string   | required |
| `.allowed_iss`                     | string[] | required |
| `.scope`                           | string   | optional |
| `.consumer_match`                  | boolean  | optional |
| `.consumer_match_claim`            | string   | optional |
| `.consumer_match_claim_custom_id`  | boolean  | optional |
| `.consumer_match_ignore_not_found` | boolean  | optional |
