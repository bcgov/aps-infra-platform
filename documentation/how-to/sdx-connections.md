---
title: "Connecting a Service"
---

This page shows how to make a connection between your system
and another on the Secure Data Exchange.

SDX supports different authorization models, which are identified by a `policyVersion`
when a connection request is submitted. The following policies are supported:

| Policy      | Description                                                                                                                           |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| `SDX.R0.00` | Simple peer-to-peer connection policy. Requires a `requesterDetails` object (see below). Available only in the SDX Playground.        |
| `SDX.R1.00` | Adds Common SSO, token-exchange and scopes support; requires additional requester and gateway resources and is not a drop-in default. |

This guide focuses on the `SDX.R0.00` policy where it establishes a basic peer-to-peer connection.
It is only available in the SDX Playground environment.

Policy `SDX.R1.00` is part of a collaboration with Common SSO (CSS) where CSS integrations will
be able to request API and scope access through their tool and have the connection request
managed in SDX for approvals. SDX will send events to CSS when connections have
been approved/revoked so that the appropriate scopes can be provisioned in Keycloak. For clients
that call services across privacy zones, SDX will perform an exchange of the token so that
the subject identifier properly identifies the user in the target privacy zone.

The steps described in this page are performed by the following roles:

| Role           | Function                                                             |
| -------------- | -------------------------------------------------------------------- |
| Tech Lead      | For service clients, request/revoke connections to another service   |
| Access Manager | For service providers, review and approve client connection requests |

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
      isApproved: true, isActive: true
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

For details on configuring the `sdx-p2p-consumer.r1` pattern,
go to [Connection Resources](/how-to/sdx-connection-resources.md).

### Provider side

=== "Restish CLI"

    Help information about the operation:

    ```sh
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

For details on configuring the `sdx-p2p-provider.r1` pattern,
go to [Connection Resources](/how-to/sdx-connection-resources.md).

<!-- prettier-ignore -->
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

## Troubleshooting token-exchange scopes

Verified-subject scope derivation fails before the token endpoint is called
when the verified token is unavailable, its `scope` claim is missing or is not
a string, or the claim is empty or contains only whitespace. Each condition
returns HTTP 500:

```json
{
  "message": "Token exchange failed",
  "error": { "code": "E4" }
}
```

This E4 response does not include a request ID. Kong logs `Unable to derive
token exchange scopes:` followed by `verified subject token is unavailable`,
`verified subject token has no string scope claim`, or `verified subject token
has an empty scope claim`.

This is distinct from an authorization-server `invalid_scope` response. In
that case, the token endpoint was called and SDX returns
`SDX_TOKEN_EXCHANGE_CONFIGURATION_ERROR` as described below.

The SDX token-exchange client must be permitted to request every scope in the
verified incoming token. If the authorization server rejects the exchange with
`invalid_scope`, SDX returns HTTP 500 with a generic response:

```json
{
  "message": "The SDX token-exchange client is not configured to complete this request. Refer to the SDX Kong token-exchange plugin logs using request ID <request-id> for details.",
  "error": {
    "code": "SDX_TOKEN_EXCHANGE_CONFIGURATION_ERROR"
  }
}
```

The `<request-id>` in the message matches the `X-Kong-Request-Id` response
header. Provide that value to the SDX support team. SDX operators can use it to
find the diagnostic entry in the Kong token-exchange plugin logs. That entry
records the authorization server status and error code, requested scopes, and
audience.

The client response does not include the requested scopes, audience,
authorization server response or error description, client assertion, or
tokens.

An explicit granted scope set that differs from the requested set is a warning,
not an exchange failure. SDX continues with the successful exchanged token, and
the provider's normal token validation and authorization rules apply.

## Connection management

### Deleting a connection

Deleting a connection request is two steps. First step is to make it inactive:

```sh
restish sdx upsert-connection \
  my-org \
  clientId: MIN.MYORG.MY-NEW-SUBSYSTEM, \
  serviceId: LAB.MIN.MYORG.EFV-ICBC.v0, \
  isActive: false
```

Then the connection can be deleted using its unique identifier.

=== "Restish CLI"

    Help information about the operation:

    ```sh
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

    If gateway configuration still exists on either side, the request is
    rejected. Remove the remaining gateway configuration and try again.
