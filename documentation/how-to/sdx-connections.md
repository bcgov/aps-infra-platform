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

- Assign your subsystem to an Edge Server
- TBC: Open a connection on SDX

## Assign your subsystem to an Edge Server

This is performed by the System Owner so that you can configure
routing policies for connecting to other systems.

To find available Edge Servers for your organization, use the following API:

- **API** `GET /organizations/{org}/runtime-groups?filter=available`

Parameters:

- `{org}=<YOUR-ORGANIZATION>`

Make a note of the Runtime Group name.

You can now call the API to assign your subsystem to the Edge Server.

- **API** `PUT /organizations/{org}/subsystems/{name}/gateway`

Parameters:

- `{org}=<YOUR-ORGANIZATION>`
- `{name}=<YOUR SUBSYSTEM>`

```json
{
  "runtimeGroupName": "<RUNTIME_GROUP_NAME>"
}
```

## Open a connection on SDX

Coming soon..
