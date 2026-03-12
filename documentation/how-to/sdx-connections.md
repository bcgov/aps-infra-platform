---
title: "Connecting a Service"
---

This page shows how to make a connection between your system
and another on the Secure Data Exchange.

The steps described in this page are performed by the following roles:

| Role         | Function                                                                   |
| ------------ | -------------------------------------------------------------------------- |
| System Owner | Manage systems and service catalog entries for the particular organization |

Use cases:

- Assign your subsystem to a runtime group
- Open a connection on SDX (Consumer)
- Open a connection on SDX (Provider)

## Assign your subsystem to a runtime group

As a System Owner, you perform this task. Once complete, you can set up routing
policies for connecting to other systems on SDX.

To find available runtime groups for your organization, use the following API:

- **API** `GET /organizations/{org}/runtime-groups?filter=available`

Parameters:

- `{org}=<your-organization>`

After choosing a runtime group, make a note of the name.

> If there are none returned, reach out to the SDX Operator (APS Team) to find out
> information for onboarding your organization onto SDX.

You can now call the API to assign your subsystem to the runtime group.

- **API** `PUT /organizations/{org}/subsystems/{name}/gateway`

Parameters:

- `{org}=<your-organization>`
- `{name}=<subsystem-name>`

```json title="Request Body"
{
  "runtimeGroupName": "<runtime-group-name>"
}
```

## Open a connection on SDX

You can now call the API to preview and then publish the routing rules for opening
a connection between two systems.

- **API** `PUT /organizations/{org}/pattern?action=apply&dryRun=true`

Parameters:

- `{org}=<your-organization>`
- values for `action`: `preview` and `apply`

For `action=apply` you can specify `dryRun=true` if you want to see what changes
will be applied without the changes actually being made.

### Consumer-side

Gateway Pattern: `sdx-p2p-consumer.r1`

| Parameter    | Description                                                                                |
| ------------ | ------------------------------------------------------------------------------------------ |
| `conn_id`    | Unique identifier for the connection (in future will be reference to an approval workflow) |
| `client_id`  | Client identifier for authentication                                                       |
| `service_id` | Service identifier being connected                                                         |
| `upgrades`   | Optional set of controls that can be added to the routing                                  |

Example:

```json
{
  "pattern": "sdx-p2p-consumer.r1",
  "parameters": {
    "conn_id": "001",
    "client_id": "LAB.MIN.CITZ.SDG",
    "service_id": "LAB.MIN.SDPR.CASE-MANAGEMENT.v1",
    "upgrades": {}
  }
}
```

Available upgrades for the `sdx-p2p-consumer.r1` pattern:

```json
{
  "sign": {},
  "verify": {}
}
```

### Provider-side

Gateway Pattern: `sdx-p2p-provider.r1`

| Parameter      | Description                                                                                |
| -------------- | ------------------------------------------------------------------------------------------ |
| `conn_id`      | Unique identifier for the connection (in future will be reference to an approval workflow) |
| `client_id`    | Client identifier for authentication                                                       |
| `service_id`   | Service identifier being connected                                                         |
| `upstream_url` | The upstream service implementation endpoint                                               |
| `upgrades`     | Optional set of controls that can be added to the routing                                  |

Example:

```json
{
  "pattern": "sdx-p2p-provider.r1",
  "parameters": {
    "conn_id": "001",
    "client_id": "LAB.MIN.CITZ.SDG",
    "service_id": "LAB.MIN.SDPR.CASE-MANAGEMENT.v1",
    "upstream_url": "http://<ocp_service>.<ocp_namespace>.svc",
    "upgrades": {}
  }
}
```

Available upgrades for the `sdx-p2p-provider.r1` pattern:

```json
{
  "sign": {},
  "verify": {},
  "token_exchange": {
    "token_endpoint": "",
    "client_id": "",
    "scopes": "",
    "audience": ""
  }
}
```
