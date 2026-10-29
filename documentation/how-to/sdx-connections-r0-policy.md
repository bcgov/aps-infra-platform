---
title: "Connecting a Service - SDX.R0 Policy"
---

Use the `SDX.R0.00` authorization policy to connect your consumer subsystem to a
provider service in the SDX Playground. The consumer Tech Lead requests access
through Restish, the provider Access Manager approves it, and both teams
configure their connection resources before the consumer calls the service.

R0 defaults use edge signing and verification. They do not install the R1 token,
ACL or token-exchange upgrades. For Common SSO integration and scope-based
access, follow [Connecting a Service](/how-to/sdx-connections.md). The `.r1`
suffix in gateway resource pattern names is a pattern revision; it does not
change the connection's `SDX.R0.00` authorization policy.

## Prerequisites

- [Install Restish CLI](/reference/restish-cli.md) and use the Playground
  configuration from [SDX environments](/reference/sdx/environments.md).
- Complete [organization onboarding](/how-to/sdx-org-onboarding.md) and
  [subsystem registration](/how-to/sdx-subsystems.md).
- Identify the provider's registered service `name` (the connection `serviceId`)
  and your consumer subsystem ID (`clientId`).
- Confirm the participating [runtime groups](/how-to/sdx-edge-runtime-groups.md)
  are ready and agree the service's authentication requirements with the
  provider.

## Request access (as consumer)

Help information about the operation:

```sh linenums="0"
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

!!! note "Requester details"

    Under `SDX.R0.00`, `requesterDetails` must be supplied together with
    `policyVersion` on this initial request — when both are present, the
    controller replaces `requesterDetails.requester` with the authenticated
    caller's name and email. Omitting `requesterDetails` leaves an invalid empty
    default in place that passes creation but fails activation.
    `requesterDetails` can only be set on creation; it cannot be repaired
    afterwards through `upsert-connection` (that field is reserved for the
    provisioner on update) — if activation fails for a missing requester record,
    deactivate and delete the connection, then recreate it with `policyVersion`
    and `requesterDetails` included together.

## Review connection access requests

Help information about the operation:

```sh linenums="0"
restish sdx list-connections
```

Example call:

```sh
restish sdx list-connections \
  my-org
```

## Approve access (as provider)

Help information about the operation:

```sh linenums="0"
restish sdx update-connection-approval
```

Example call:

```sh
restish sdx update-connection-approval \
  my-org \
  clientId: MIN.MYORG.MY-NEW-SUBSYSTEM, \
  serviceId: LAB.MIN.MYORG.EFV-ICBC.v0, \
  isApproved: true, isActive: true
```

## Open a connection

After the provider approves the connection request, configure the routing
resources on both sides to open a channel between the two systems.

### Consumer side

Help information about the operation:

```sh linenums="0"
restish sdx upsert-connection
```

Prepare a pattern input file (`client-input.json`) for the Consumer:

```json
{
  "gatewayPatterns": {
    "sdx-p2p-consumer.r1": {
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
  clientResources: @client-input.json

```

For details on configuring the `sdx-p2p-consumer.r1` pattern, go to
[Connection Resources](/how-to/sdx-connection-resources.md).

### Provider side

Help information about the operation:

```sh linenums="0"
restish sdx upsert-connection
```

Prepare a pattern input file (`service-input.json`) for the Provider:

```json
{
  "gatewayPatterns": {
    "sdx-p2p-provider.r1": {
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
  serviceResources: @service-input.json
```

For details on configuring the `sdx-p2p-provider.r1` pattern, go to
[Connection Resources](/how-to/sdx-connection-resources.md).

## Call the service (consumer)

Confirm the connection is approved, active and successfully provisioned on both
sides. Obtain the consumer runtime's `consumerEndpoint` from your runtime
operator (or the override runtime when `clientRuntimeOverride` is configured).

Call the consumer runtime with the registered service name in the path and your
consumer subsystem ID in `X-Client-Id`:

```sh
curl 'https://<consumer-runtime-host>/sdx/0/<serviceId>/<operation-path>' \
  -H 'X-Client-Id: <consumer-subsystem-id>'
```

Use the method, operation path and any additional authentication required by the
service. The `/hello` operation tests the provider edge; use an actual service
operation to test the provider API. Confirm an expected response with the
provider.

Leave `stripPath` at its default `false` so the provider edge receives the route
prefix. You do not need to supply `X-Service-Id`; SDX sets it from the selected
connection. See the
[P2P routing contract](/reference/sdx/p2p-routing-contract.md) for route
selection and header handling.

## Connection management

### Deleting a connection

To delete a connection request, first make the connection inactive:

```sh
restish sdx upsert-connection \
  my-org \
  clientId: MIN.MYORG.MY-NEW-SUBSYSTEM, \
  serviceId: LAB.MIN.MYORG.EFV-ICBC.v0, \
  isActive: false
```

Then delete the connection using its unique identifier.

=== "Restish CLI"

    Help information about the operation:

    ```sh linenums="0"
    restish sdx delete-connection
    ```

    Example call:

    ```sh
    restish sdx delete-connection \
      ministry-of-citz 2010
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

    If gateway configuration still exists on either side, SDX rejects the
    request. Remove the remaining gateway configuration and try again.
