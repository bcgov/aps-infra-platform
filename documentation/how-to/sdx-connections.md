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
- TBC: Open a connection on SDX

## Assign your subsystem to a runtime group

As a System Owner, you perform this task. Once complete, you can set up routing
policies for connecting to other systems on SDX.

To find available runtime groups for your organization, use the following API:

- **API** `GET /organizations/{org}/runtime-groups?filter=available`

Parameters:

- `{org}=<your-organization>`

After choosing a runtime group, make a note of the name.

!!! note
If there are none returned, reach out to the SDX Operator to find out
information for onboarding your organization onto SDX.

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

Documentation for this feature is in progress.
