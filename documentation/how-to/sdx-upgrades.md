---
title: "P2P Gateway Pattern Upgrades"
---

Gateway patterns for peer-to-peer will have different rules over time around how
they should be configured. This page describes the rules for each policy release.

As new feature like token exchange, dpop, and policy enforcement engine get added,
there will be a new policy version describing what is required for a connection
between systems.

## Releases

### SDX.R0.00

#### sdx-p2p-consumer.r1

- following parameters MUST be set: `conn_id`, `client_id`, `service_id`
- following parameters MAY be set: `tls_verify`, `upgrades`, `rg_override`
- `rg_override` can be `subsystem` (the RG that the client subsystem
  is associated with) or `pzgw` (Privacy Zone Gateway)

| Parameter     | Type               | Rule                          |
| ------------- | ------------------ | ----------------------------- |
| `conn_id`     | string             | required                      |
| `client_id`   | string             | required                      |
| `service_id`  | string             | required                      |
| `rg_override` | `subsystem / pzgw` | optional, default `subsystem` |
| `upgrades`    | object             | optional                      |

**upgrades:**

| Parameter         | Type     | Rule                |
| ----------------- | -------- | ------------------- |
| `dpop`            | object   | optional            |
|                   |          |                     |
| `sign`            | object   | optional            |
|                   |          |                     |
| `verify`          | object   | optional            |
|                   |          |                     |
| `counter_sign`    | object   | optional            |
|                   |          |                     |
| `token_exchange`  | object   | optional            |
| `.client_id`      | string   | required            |
| `.token_endpoint` | string   | required, any value |
| `.scopes`         | string[] | optional            |
| `.audience`       | string   | optional            |

#### sdx-p2p-provider.r1

- following parameters MUST be set: `conn_id`, `client_id`, `service_id`
- following parameters MAY be set: `tls_verify`, `upgrades`, `rg_override`
- `rg_override` can be `subsystem` (the RG that the client subsystem
  is associated with) or `pzgw` (Privacy Zone Gateway)

| Parameter     | Type               | Rule                          |
| ------------- | ------------------ | ----------------------------- |
| `conn_id`     | string             | required                      |
| `client_id`   | string             | required                      |
| `service_id`  | string             | required                      |
| `rg_override` | `subsystem / pzgw` | optional, default `subsystem` |
| `upgrades`    | object             | optional                      |

**upgrades:**

| Parameter      | Type   | Rule     |
| -------------- | ------ | -------- |
| `mtls_auth`    | object | optional |
|                |        |          |
| `mtls_acl`     | object | optional |
|                |        |          |
| `verify`       | object | optional |
|                |        |          |
| `counter_sign` | object | optional |
