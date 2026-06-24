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

- Request access (as consumer)
- Review connection access requests
- Approve access (as provider)
- Open a connection
  - Consumer side
  - Provider side
- Delete a connection request

## Prerequisites

- [Install Restish CLI](/reference/restish-cli.md)

## Request access (as consumer)

=== "Restish CLI"

    Help information about the operation:

    ```sh
    restish sdx upsert-connection
    ```

    Example call:

    ```sh
    restish sdx upsert-connection \
      my-org \
      clientId: MIN.MYORG.MY-NEW-SUBSYSTEM, \
      serviceId: LAB.MIN.MYORG.EFV-ICBC.v0, \
      policyVersion: SDX.R0.00
    ```

## Review connection access requests

=== "Restish CLI"

    Help information about the operation:

    ```sh
    restish sdx list-connections
    ```

    Example call:

    ```sh
    restish sdx list-connections \
      my-org
    ```

## Approve access (as provider)

=== "Restish CLI"

    Help information about the operation:

    ```sh
    restish sdx upsert-connection
    ```

    Example call:

    ```sh
    restish sdx upsert-connection \
      my-org \
      clientId: MIN.MYORG.MY-NEW-SUBSYSTEM, \
      serviceId: LAB.MIN.MYORG.EFV-ICBC.v0, \
      isApproved: true
    ```

## Open a connection

Once the connection request has been approved, both sides are able to publish the
routing rules for opening a channel between the two systems.

### Consumer side

=== "Restish CLI"

    Help information about the operation:

    ```sh
    restish sdx upsert-connection
    ```

    Prepare a pattern input file (`pattern-input.json`) for the Consumer:

    ```json
    {
      "gatewayPatterns": {
        "sdx-p2p-consumer.r1": {
          "upgrades": {
            "sign": {}
          }
        }
      }
    }
    ```

    Example call:

    ```sh
    restish sdx upsert-connection \
      my-org \
      clientId: MIN.MYORG.MY-NEW-SUBSYSTEM, \
      serviceId: LAB.MIN.MYORG.EFV-ICBC.v0, \
      clientResources: @pattern-input.json

    ```

For details on configuring the `sdx-p2p-consumer.r1` pattern,
go to [Connection Gateway Patterns](/how-to/sdx-upgrades.md).

### Provider side

=== "Restish CLI"

    Help information about the operation:

    ```sh
    restish sdx generate-config-from-pattern
    ```

    Prepare a pattern input file (`pattern-input.json`) for the Provider:

    ```json
    {
      "gatewayPatterns": {
        "sdx-p2p-provider.r1": {
          "upstreamUrl": "https://my-upstream-endpoint.domain",
          "upgrades": {
          }
        }
      }
    }
    ```

    Example call:

    ```sh
    restish sdx upsert-connection \
      my-org \
      clientId: MIN.MYORG.MY-NEW-SUBSYSTEM, \
      serviceId: LAB.MIN.MYORG.EFV-ICBC.v0, \
      "requesterDetails: { requester: "Joe", client: { clientId: abc }, service: { clientId: def } }", \
      serviceResources: @pattern-input.json
    ```

For details on configuring the `sdx-p2p-provider.r1` pattern,
go to [Connection Gateway Patterns](/how-to/sdx-upgrades.md).

## Delete a connection request

Deleting a connection request is the final cleanup step after the consumer and
provider gateway configurations have been removed.

Remove each side's gateway configuration by generating the same pattern
configuration that was used to open the connection, but use `action=remove`.

| Side     | Gateway pattern       |
| -------- | --------------------- |
| Consumer | `sdx-p2p-consumer.r1` |
| Provider | `sdx-p2p-provider.r1` |

=== "Restish CLI"

    Prepare the same pattern input file used to open the connection side being
    removed, then run:

    ```sh
    restish sdx generate-config-from-pattern \
      ministry-of-citz \
      --action remove \
      --dry-run < pattern-input.json
    ```

=== "Reference"

    - **API** `PUT /organizations/{org}/pattern?action=remove&dryRun=true`

    Parameters:

    - `{org}=<your-organization>`
    - values for `action`: `preview`, `apply`, and `remove`

    Use `dryRun=true` to see what changes will be removed without actually
    removing them.

### Delete the connection request

After both sides have removed their gateway configuration, a System Owner for
either organization associated with the connection request can delete it.

=== "Restish CLI"

    Help information about the operation:

    ```sh
    restish sdx delete-connection
    ```

    Example call:

    ```sh
    restish sdx delete-connection \
      ministry-of-citz \
      1
    ```

=== "Reference"

    - **API** `DELETE /organizations/{org}/connections/{id}`

    Parameters:

    - `{org}=<your-organization>`
    - `{id}=<connection-request-id>`

    The `{org}` value can be the consumer organization or the provider
    organization for the connection request.

    Successful response:

    ```json
    {
      "result": "deleted",
      "id": "1"
    }
    ```

    If gateway configuration still exists on either side, the request is
    rejected. Remove the remaining gateway configuration and try again.
