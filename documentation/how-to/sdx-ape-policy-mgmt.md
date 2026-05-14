---
title: "Policy Management"
---

This page shows how to create OPA and CEDAR policies and use them for enforcement on SDX.

!!! warning "Preview"

    This feature is in `preview` only, which means it is experimental.
    It is available in our `LAB` environment as is.

The steps described in this page are performed by the following roles:

| Role         | Function                                                                   |
| ------------ | -------------------------------------------------------------------------- |
| System Owner | Manage systems and service catalog entries for the particular organization |

Use cases:

- Register a policy
- Upgrade connection with a PEP
- Register a data source

## Register a policy

> NOTE: The package name in the policy should match the `subsystem_id` (with `.` and `-` changed to `_`)
> For example: `package LAB_USR_ACOPE_APS_KAFKA.authz`

```sh
{
  "pattern": "opal-policy.r1",
  "parameters": {
    "subsystem_id": "LAB.USR.ACOPE.APS-KAFKA",
    "name": "authz",
    "policy": {{POLICY}}
  }
}
```

### Inputs

When designing your policies, assume the `pep` plugin will provide
the following data about the particular request:

```json
{
  "method": "GET",
  "path": "/v1/widgets/1234",
  "named_params": {
    "id": "1234"
  },
  "token": {
    "sub": "111",
    "aud": "abc",
    "scopes": "scope1 scope2"
  }
}
```

## Upgrade connection with a PEP

When configuring the `sdx-p2p-*.r1` gateway patterns for consumer and provider,
use the `pep` upgrade to run the particular policy that you created in the previous
step.

```json
{
    "upgrades": {
      "sign": {},
      "_co-sign": {},
      "pep": {
        "policy_name": "authz"
      }
    }
```

## Register a data source

The data source (policy information point) is a powerful way of pulling in authorization
data to be used in the decision making. The `upstream_url` should be accessible from the
runtime group that the subsystem is registered on.

```sh
{
  "pattern": "opal-data-source.r1",
  "parameters": {
    "subsystem_id": "LAB.USR.ACOPE.APS-KAFKA",
    "name": "user-gateways",
    "upstream_url": "https://httpbun.com/any"
  }
}
```

For referencing the data source in your policy, use the `subsystem_id` package convention:

```sh
import data.tenant["LAB.USR.ACOPE.APS-KAFKA"] as dat`

items := {row |
    row := dat["user-gateways"]
}
```
