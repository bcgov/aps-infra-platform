---
title: "Connecting a Service"
---

This page shows how to make a connection between your system
and another on the Secure Data Exchange.

The steps described in this page are performed by the following roles:

| Role         | Function                                                                   |
| ------------ | -------------------------------------------------------------------------- |
| System Owner | Manage systems and service catalog entries for the particular organization |

The steps described in this page are performed by users with the following permissions:

| Permission        | Function                                       |
| ----------------- | ---------------------------------------------- |
| Connection.Manage | Review and approve/reject connection requests. |

Use cases:

- Request access (as consumer)
- Review connection access requests
- Approve access (as provider)
- Open a connection
  - Consumer side
  - Provider side
- Connection management
  - Delete a connection request

## Prerequisites

- [Install Restish CLI](/reference/restish-cli.md)

## Request access (as consumer)

`policyVersion` selects the connection policy that governs how the
connection is provisioned:

| Policy        | Description                                                                                    |
| ------------- | ------------------------------------------------------------------------------------------------ |
| `SDX.R0.00`   | Simple point-to-point connection policy. Requires a `requesterDetails` object (see below).       |
| `SDX.R1.00`   | Adds integration/token-exchange support; requires additional requester and gateway resources and is not a drop-in default. |

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
      policyVersion: SDX.R0.00, \
      "requesterDetails: {}"
    ```

!!! note "requester details"
    Under `SDX.R0.00`, `requesterDetails` must be supplied together with
    `policyVersion` on this initial request — when both are present, the
    controller replaces `requesterDetails.requester` with the authenticated
    caller's name and email. Omitting `requesterDetails` leaves an invalid
    empty default in place that will pass creation but fail activation.
    `requesterDetails` can only be set on creation; it cannot be repaired
    afterwards through `upsert-connection` (that field is reserved for the
    provisioner on update) — if activation fails for a missing requester
    record, deactivate and delete the connection, then recreate it with
    `policyVersion` and `requesterDetails` included together.

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
    restish sdx update-connection-approval
    ```

    Example call:

    ```sh
    restish sdx update-connection-approval \
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
          "clientRuntimeOverride": "MIN.CITZ.pzgw",
          "upgrades": {
            "sign": {},
            "verify": {}
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
go to [Connection Gateway Patterns](/how-to/sdx-connection-patterns.md).

### Provider side

=== "Restish CLI"

    Help information about the operation:

    ```sh
    restish sdx upsert-connection
    ```

    Prepare a pattern input file (`pattern-input.json`) for the Provider:

    ```json
    {
      "gatewayPatterns": {
        "sdx-p2p-provider.r1": {
          "upstreamUrl": "https://my-upstream-endpoint.domain",
          "upgrades": {
            "mtlsAuth": {},
            "sign": {},
            "verify": {}
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
      serviceResources: @pattern-input.json
    ```

For details on configuring the `sdx-p2p-provider.r1` pattern,
go to [Connection Gateway Patterns](/how-to/sdx-connection-patterns.md).

!!! note "Associating an OAuth integration client with a connection"
    `requesterDetails.client.clientId` (used above for
    `sdx-p2p-consumer-access.r1`/ACL and, when configured, `consumerMatch`)
    is provisioner-managed. It cannot be written directly through the SDX
    management API — attempting a direct `upsert-connection` update of
    `requesterDetails` returns `HTTP 400`. Registering an
    `integrationClientId` on the consumer subsystem (see
    [Register an SDX Subsystem](/how-to/sdx-subsystems.md)) is only the
    first half of the relationship: the field is populated by calling the
    supported `POST /v1/integrations/{clientId}/access-requests` operation
    on the SDX Partner Authorization Services API, which validates the
    requested scopes against the registered OAD and writes the requester
    metadata with trusted provisioner credentials. That API uses a separate
    base URL and bearer-token audience from the main SDX API — consult the
    APS team for the current Restish/API configuration for it. Before
    enabling strict `consumerMatch`, verify that the connection contains the
    integration client and that the Kong consumer created by
    `sdx-p2p-consumer-access.r1` exists, since enabling `consumerMatch`
    ahead of a matching consumer blocks legitimate traffic.

## Connection management

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
    restish sdx provision-config-from-pattern \
      ministry-of-citz \
      --action remove \
      --dry-run < pattern-input.json
    ```

### Delete a connection request

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
