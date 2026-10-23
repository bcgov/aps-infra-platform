---
title: "Approve and test an SDX connection"
---

After a consumer submits an [R0 request](/how-to/sdx-connections-r0-policy.md)
or an [R1 request](/how-to/sdx-connections-r1-policy.md), the provider Access
Manager reviews it and both teams confirm provisioning before the consumer tests.
For the management examples below, [install Restish](/reference/restish-cli.md)
and use the intended environment's API configuration and authorized organization.

## Notifications and request status

Confirm with the provider how the deployed workflow notifies the Access Manager
of a pending request. Do not rely on a notification alone: inspect the connection
request and verify its consumer, service/version, environment and, for R1, scopes.
If an expected notification is absent, coordinate with the provider and APS team
and check request status through the supported management workflow below.

For R1, SDX also sends approved/revoked access events to CSS so it can synchronize
scope grants. These integration events are separate from a human notification;
confirm delivery and provisioning rather than assuming approval completed them.

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

## Confirm R1 scope synchronization

For an R1 request, confirm approved access has synchronized back to CSS. SDX sends
the approved-access snapshot to CSS, which provisions the allowed scopes for the
integration. If a callback fails or expected scopes are absent, ask APS/Common SSO
to inspect delivery and registration before requesting broader permissions.
Never share credentials or tokens in a support ticket.

## Consumer testing

1. Have the operator confirm the connection is active and both sides are
   provisioned. Record the actual consumer invocation endpoint from the deployed
   connection; do not derive it by concatenating catalogue identifiers.
2. Use the API's documented method/path and synthetic Playground data. Obtain
   credentials through the selected policy's supported flow; for R1, follow
   [user-token setup](/how-to/sdx-connections-r1-policy.md#obtain-a-token-and-call-the-service).
3. Call through SDX and compare the response with the expected result agreed
   with the provider. A direct upstream call does not verify the SDX connection.
4. With the provider, verify missing/invalid credentials and unapproved access
   are denied. For R1, also verify approved scopes and target-zone identity where
   exchange applies; HTTP success alone does not prove correct identity.
5. Record sanitized identifiers, timestamps, expected/observed results and support
   request IDs. Keep tokens, credentials and personal data out of shared records.
6. On revocation, confirm access is removed from the connection and, for R1, CSS.
   Verify denied access and clean up disposable connections using the lifecycle
   steps below.

## Playground walkthrough record

Use this record with the consumer, provider and, for R1, APS/Common SSO teams before
accepting the draft. Record the date, deployed version and sanitized identifiers;
mark a check as pending when the deployed workflow cannot support it yet.
Do not record token contents or personal subject identifiers.

| Check | Evidence to record |
| --- | --- |
| Request | Environment, consumer subsystem and provider service/version; for R1, CSS integration ID, OAuth client ID and requested scopes. |
| Approval and provisioning | Provider approval and operator confirmation that both sides are active; for R1, approved scope set and CSS synchronization result. |
| Allowed call | Actual consumer endpoint and documented operation, timestamp, expected response and observed result using synthetic data. |
| Denied call | Provider-agreed missing/invalid-token and unapproved-access cases, expected denial and observed result. |
| Cross-zone identity, when applicable | Operator confirmation of exchange and provider confirmation of the intended target-zone identity and authorization, without copying identity values. |
| Revocation and cleanup | Denied access after revocation and operator confirmation of disposable connection cleanup; for R1, CSS grant removal. |

If scopes, audiences or identity differ from the agreed values, retain the failed
check and its sanitized support/request ID. Resolve it with the responsible team
before treating the walkthrough as passed.

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
