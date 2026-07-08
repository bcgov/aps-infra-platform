---
title: "Managing Subsystems"
---

## Overview

This page shows how to manage subsystems on the Secure Data Exchange.

The steps described in this page are performed by the following roles:

| Role         | Function                                                                   |
| ------------ | -------------------------------------------------------------------------- |
| System Owner | Manage systems and service catalog entries for the particular organization |

Use cases:

- Register a subsystem
- Assign your subsystem to a runtime group
- Subsystem management
  - Delete a subsystem

## Prerequisites

- [Install Restish CLI](/reference/restish-cli.md)

## Register a subsystem

=== "Restish CLI"

    Help information about the operation:

    ```sh
    restish sdx upsert-subsystem
    ```

    Example call:

    ```sh
    restish sdx upsert-subsystem \
      my-org \
      name: MY-NEW-SUBSYSTEM
    ```

=== "Reference"

    > **API** `PUT /organizations/{org}/subsystems`

    Parameters: `{org}=ministry-of-food`

    ```json
    {
      "name": "MY-NEW-SUBSYSTEM"
    }
    ```

## Assign your subsystem to a runtime group

As a System Owner, you perform this task. Once complete, you can set up routing
policies for connecting to other systems on SDX.

=== "Restish CLI"

    Help information about the operation to list available runtimes:

    ```sh
    restish sdx list-runtime-groups
    ```

    Example:

    ```sh
    restish sdx list-runtime-groups \
      my-org \
      --filter available
    ```

    Help information about the operation to assign a runtime group:

    ```sh
    restish sdx register-subsystem-gateway
    ```

    Example:

    ```sh
    restish sdx register-subsystem-gateway \
      my-org MY-NEW-SUBSYSTEM \
      runtimeGroupName: newrg
    ```

    An assigned Gateway ID will be returned. This Gateway can be used to configure
    routes and controls for services it connects to.

=== "Reference"

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

    An assigned Gateway ID will be returned. This Gateway can be used to configure
    routes and controls for services it connects to.

## Subsystem management

### Delete a subsystem

A subsystem can be deleted when it has no active connection requests and no
gateway configuration.

If deletion succeeds, related OAS services are deleted with the subsystem.

=== "Restish CLI"

    Help information about the operation:

    ```sh
    restish sdx delete-subsystem
    ```

    Example:

    ```sh
    restish sdx delete-subsystem \
      my-org SUBSYSTEM-NAME
    ```

=== "Reference"

    > **API** `DELETE /organizations/{org}/subsystems/{name}`

    Parameters:

    - `{org}=<your-organization>`
    - `{name}=<subsystem-name>`

The delete request will not proceed if any of the following are true:

- the subsystem has active connection requests as a client
- a service under the subsystem has active connection requests
- subsystem gateway configuration exists

After a subsystem is deleted, the same subsystem name can be used again.

## Next steps

- [Managing services](/how-to/sdx-services.md)
