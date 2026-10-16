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

For the Common SSO consumer and Brochure UI Access Manager journey, follow
[Request and manage access with SDX.R1.00](#request-and-manage-access-with-sdxr100).
The Restish request and gateway-resource examples below use `SDX.R0.00` in the
SDX Playground. Keep the policy and environment consistent throughout a journey.

Policy `SDX.R1.00` connects Common SSO (CSS) integration access requests to SDX
approval. Approval and revocation events allow CSS to update the integration's
Keycloak scopes. For connections configured to cross privacy zones, SDX exchanges
the token so the subject identifies the user in the target privacy zone. Approval,
gateway provisioning and CSS scope synchronization are separate steps; check their
results before treating a connection as ready.

The steps described in this page are performed by the following roles:

| Role           | Function                                                             |
| -------------- | -------------------------------------------------------------------- |
| Tech Lead      | For service clients, request/revoke connections to another service   |
| Access Manager | For service providers, review, approve, reject and revoke client access |

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

- Use the matching [SDX environment](/reference/sdx/environments.md) for the
  consumer integration, provider service and catalogue.
- For the R1 journey, have access to the consumer's Common SSO integration, a
  registered consumer subsystem linked to its integration client, and a published
  provider service with the requested scopes. See
  [Register an SDX Subsystem](/how-to/sdx-subsystems.md) and
  [Register a Service](/how-to/sdx-services.md).
- To make provider decisions, sign in with the account assigned the **Access
  Manager** role on the provider subsystem. Sign-in alone does not grant that role;
  ask the organization's administrator if access is missing.
- [Install Restish CLI](/reference/restish-cli.md) only if using the CLI alternatives.

## Request and manage access with SDX.R1.00

### Request access through Common SSO (consumer)

1. Sign in to Common SSO and open the integration that will call the API. Use the
   integration and environment linked to your SDX consumer subsystem.
2. In that integration's SDX access-request flow, select the provider service and
   the scopes your application needs. Review the service, target environment and
   requested scopes before submitting.
3. Submit the request and retain its submission identifier and the consumer and
   service identifiers for follow-up with the provider's Access Manager.
4. Wait for the provider's decision. A submitted request does not itself grant
   access. After approval, confirm the integration has received the approved
   scopes and the SDX connection is provisioned before testing a service call.

The Common SSO flow supplies trusted integration and requester details for R1.
Do not create a second request using the Playground R0 example below, or try to
edit `requesterDetails` with Restish. If the integration does not offer the SDX
request flow or the service/scopes are missing, contact the CSS/APS teams to
confirm onboarding and environment availability.

### Review a request in the Brochure UI (provider)

1. Open the **SDX UI** link for your
   [environment](/reference/sdx/environments.md) and sign in.
2. Open **Member Console**, then **Connection Requests** (`/connections`). Select
   the provider organization and the intended environment. Requests are grouped
   by subsystem; locate the consumer-to-service pair for your service.
3. For a pending request, select **Approve / Reject**. Check the policy is
   `SDX.R1.00`, the environment, consumer and service identifiers, requester,
   submission ID, integration/client ID and requested scopes. Compare them with
   the consumer's request and your service's access requirements.
4. If information is missing or unexpected, confirm it with the requester before
   deciding. **Cancel** closes the review without making a decision.

### Approve or reject in the Brochure UI (provider)

In the review dialog, select **Approve** to approve the request or **Reject** to
remove the pending request. Check the result message after returning to the list.
If an error is displayed, the action has not been confirmed; review the error and
refresh the list before retrying.

After approval, expand **Connection details** to review the provisioner status
and any diagnostic message. An **Approved** connection is not necessarily
**Active**: activation and the required R1 gateway resources must also be ready.
Coordinate outstanding provisioning with the subsystem's technical lead; see
[SDX.R1.00 connection resources](/how-to/sdx-connection-resources.md#sdxr100-policy).
The consumer should check CSS scope synchronization and test with an appropriate
new token before relying on access. Approval is an alternative to the Restish
approval call below; it does not replace technical gateway setup.

To review existing access later, return to **Connection Requests**, select the
same provider organization/environment, locate the connection and expand
**Connection details**. Check its client/service pair, scopes, approval/active
state and provisioner status before changing access.

### Revoke access in the Brochure UI (Access Manager)

Revocation removes an existing approved connection. To reject an unapproved
request, use **Approve / Reject** instead.

1. In **Member Console → Connection Requests**, select the provider organization
   and environment, and find the approved consumer-to-service connection.
   Confirm the consumer, service and scopes before proceeding.
2. If the connection is active, select **Customize...**, clear **Active**, then
   select **Save**. Coordinate this step with the subsystem's technical lead if
   your account is not permitted to change activation. Wait for the provisioner
   to remove the gateway configuration on both sides; review **Connection
   details** for progress or errors.
3. Select **Revoke access** and review the confirmation dialog. Confirm only when
   you intend to remove that connection; this action deletes the connection,
   rather than merely pausing it.
4. Check the result message and refresh the list to confirm the connection is
   gone. If deletion reports remaining gateway configuration, wait for cleanup
   or ask the technical lead/APS team to resolve the provisioner error, then
   retry. An error message is not confirmation that access was revoked.
5. Coordinate with the consumer to confirm CSS has processed the revocation and
   removed the corresponding integration access/scopes. Verify the service is
   no longer accessible through the revoked connection; do not infer immediate
   invalidation of already issued tokens from the UI message alone.

The UI performs the connection deletion on your behalf, replacing the Restish
commands in [Deleting a connection](#deleting-a-connection). Reinstating access
after deletion requires a new request and approval. If a connection or action is
missing, confirm the provider organization, environment and subsystem role with
your administrator.

## Request access (as consumer)

The following request example is for `SDX.R0.00` in the Playground. For an R1
consumer integration, submit the request through Common SSO as described above.

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

## Troubleshooting token-exchange scopes and audiences

### Original token does not authorize the SDX exchange client

When token exchange is enabled, the verified original token's `aud` claim must
contain the consumer `tokenExchange.clientId`. If the value is missing, the
claim is malformed, or it is not a string or array of strings, SDX returns HTTP
400 without calling the authorization server:

```json
{
  "message": "The supplied token is not authorized for SDX token exchange. Refer to the SDX documentation and use request ID <request-id> when requesting support.",
  "error": {
    "code": "SDX_TOKEN_EXCHANGE_NOT_AUTHORIZED"
  }
}
```

The `<request-id>` in the message matches the `X-Kong-Request-Id` response
header and the diagnostic SDX Kong log entry. The public response does not
contain the original audiences, configured client ID, token, or authorization
server details.

The requesting client is responsible for requesting any audience required by
the provider API or another downstream resource. SDX propagates those verified
original audiences and removes exact duplicates. Retaining the SDX exchange
client allows the provider to use the exchanged token for a subsequent SDX
call. An original token containing only the SDX exchange client is valid when
no target resource requires another audience.

The optional plugin setting `tokenExchange.audience` adds one configured
audience to the exchange request. When present, SDX merges it with the verified
original audiences and removes duplicates. This supports both connections that
use a configured audience and connections whose target audiences are already
present in the original token. Current provisioning policies may continue to
require or supply the configured value.

### Original token has no usable scope claim (E4)

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

### SDX exchange client cannot request a scope or audience

The SDX token-exchange client must be permitted to request every scope and
audience sent in the exchange. If the authorization server rejects the exchange
because a requested scope or audience is unavailable, SDX returns HTTP 500 with
a generic response:

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
audiences.

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
