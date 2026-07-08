---
title: "Managing Services"
---

## Overview

This page shows how to manage services on the Secure Data Exchange.

The steps described in this page are performed by users with the following permissions:

| Permission             | Function        |
| ---------------------- | --------------- |
| GatewayPattern.Publish | Manage services |

The permissions are setup by a System Owner for the organization.

Use cases:

- Register a service
- View API service catalog
- Subsystem management
  - Delete a service

## Prerequisites

- [Install Restish CLI](/reference/restish-cli.md)

## Register a service

=== "Restish CLI"

    Help information about the operation:

    ```sh
    restish sdx create-oas-service
    ```

    Example:

    ```sh
    restish sdx create-oas-service \
      my-org \
      --subsystem MY-NEW-SUBSYSTEM \
      --environment lab \
      --rsh-header "Content-Type: application/yaml" \
      < openapi.yaml
    ```

## View API service catalog

=== "Restish CLI"

    List all subsystems:

    ```sh
    restish sdx subsystems-list
    ```

    List only name and title of APIs:

    ```sh
    restish sdx list-service-catalog | jq '.[] | .name+": "+.title'
    ```

## Service management

### Delete a service

A service can be deleted when there are no active connection requests for it.

=== "Restish CLI"

    Help information about the operation:

    ```sh
    restish sdx delete-organization-oas-service
    ```

    Example:

    ```sh
    restish sdx delete-organization-oas-service \
      my-org SERVICE-NAME
    ```

The delete request will not proceed if the service has active connection requests.

After a service is deleted, the same service name can be used again.

## Next steps

- [Connecting a Service](/how-to/sdx-connections.md)
