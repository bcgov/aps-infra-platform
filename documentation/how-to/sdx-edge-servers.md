---
title: Provision a new Edge Server
---

This page shows how to provision a new Edge Server (Runtime Group) on the SDX Ecosystem.

The steps described in this page are performed by the following roles:

| Role         | Function                                                           |
| ------------ | ------------------------------------------------------------------ |
| System Owner | Request a new edge server, and manage onboarding a new edge server |

Use cases:

- Register a new Runtime Group
- Deploy Runtime Group infrastructure
- Initialize default route policies
- Add public key to registry

## Register a new Runtime Group

!!! note
    Documentation for this use case is in progress.

## Deploy Runtime Group infrastructure

!!! note
    Documentation for this use case is in progress.

## Initialize default route policies

You can now call the API to preview and then publish the default routing rules for
the runtime group.

- **API** `PUT /organizations/{org}/pattern?action=apply&dryRun=true`

Parameters:

- `{org}=<your-organization>`
- values for `action`: `preview` and `apply`

For `action=apply` you can specify `dryRun=true` if you want to see what changes
will be applied without the changes actually being made.

### `sdx-runtime-group.r1`

```json
{
  "pattern": "sdx-runtime-group.r1",
  "parameters": {
    "runtime_group_name": "<runtime-group-name>"
  }
}
```

## Add public key to registry

Using the same pattern endpoint from above, you can use the `sdx-keys.r1` pattern
to add the public key using the certificate from the runtime group.

### `sdx-keys.r1`

```json
{
  "pattern": "sdx-keys.r1",
  "parameters": {
    "runtime_group_name": "<runtime-group-name>",
    "certificate_pem": "<public-certificate-pem-format>"
  }
}
```
