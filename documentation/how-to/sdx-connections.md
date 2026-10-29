---
title: "Connecting a Service"
---

## Overview

The consumer journey for requesting access to services published on SDX, begins
with Common SSO (CSS).

The integration owner submits the request through CSS, the provider Access
Manager reviews it in the SDX UI, and the consumer verifies scope
synchronization and gateway provisioning before calling the service. Where
configured, SDX exchanges the user token across privacy zones so the subject
identifies the user in the target zone.

## Prerequisites

- Complete [organization onboarding](/how-to/sdx-org-onboarding.md) and
  [subsystem registration](/how-to/sdx-subsystems.md), linking your consumer
  subsystem to the intended CSS integration client.
- Have permission to manage that CSS integration and identify the provider
  service/version and requested scopes from its catalogue/OpenAPI description.
- Use matching CSS, catalogue and runtime [environments](/reference/sdx/environments.md).
- Provider decisions require the **Access Manager** role on the provider
  subsystem. Sign-in alone does not grant that role.

## Request access through Common SSO (consumer)

1. Open the **Common SSO** link for your
   [environment](/reference/sdx/environments.md) and sign in.
1. Open the integration that will call the API. Use the
   integration and environment linked to your SDX consumer subsystem.
1. In that integration's SDX access-request flow, select the provider service and
   the scopes your application needs. Review the service, target environment
   and requested scopes before submitting.
1. Submit the request and retain its submission identifier and the consumer and
   service identifiers for follow-up with the provider's Access Manager.
1. Wait for the provider's decision. A submitted request does not itself grant
   access. After approval, confirm the integration has received the approved
   scopes and the SDX connection is provisioned before testing a service call.

## Review a request in the SDX UI (provider)

1. Open the **SDX UI** link for your
   [environment](/reference/sdx/environments.md) and sign in.
1. Open **Member Console**, then **Connection Requests** (`/connections`). Select
   the provider organization and the intended environment. Requests are grouped
   by subsystem; locate the consumer-to-service pair for your service.
1. For a pending request, select **Approve / Reject**. Check the policy is
   `SDX.R1.00`, the environment, consumer and service identifiers, requester,
   submission ID, integration/client ID and requested scopes. Compare them with
   the consumer's request and your service's access requirements.
1. If information is missing or unexpected, confirm it with the requester before
   deciding. **Cancel** closes the review without making a decision.

## Approve or reject in the SDX UI (provider)

In the review dialog, select **Approve** to approve the request or **Reject** to
remove the pending request. Check the result message after returning to the
list. If an error is displayed, the action has not been confirmed; review the
error and refresh the list before retrying.

After approval, expand **Connection details** to review the provisioner status
and any diagnostic message. An **Approved** connection is not necessarily
**Active**: activation and the required R1 gateway resources must also be ready.
Coordinate outstanding provisioning with the subsystem's technical lead; see
[SDX.R1.00 connection resources](/how-to/sdx-connection-resources.md#sdxr100-policy). The consumer should check CSS scope synchronization and test with an
appropriate new token before relying on access. Approval does not replace
technical gateway setup.

To review existing access later, return to **Connection Requests**, select the
same provider organization/environment, locate the connection and expand
**Connection details**. Check its client/service pair, scopes, approval/active
state and provisioner status before changing access.

## Confirm provisioning and call the service (consumer)

1. Confirm the provider approved the intended service and scopes, CSS synchronized
   those grants, and the SDX connection is active and provisioned on both
   edges. Ask the technical lead or APS team to resolve provisioning errors
   before testing.
1. Obtain a fresh user access token through your integration's supported CSS
   authentication flow for the intended environment and approved scopes. A
   token used to manage SDX is separate from the token your application sends
   to the API.
1. Confirm the token meets the consumer endpoint's issuer/audience requirements.
   When token exchange is enabled, its original `aud` must include the
   configured SDX exchange client ID and any target resource audiences. The
   exchange transfers scopes from the verified token; it does not grant
   additional access. Confirm target privacy-zone scope setup with APS/Common
   SSO before activation; see
   [token-exchange scopes and audiences](/how-to/sdx-connection-resources.md#token-exchange-scopes).
1. Call your consumer runtime's `consumerEndpoint` (or the configured override),
   using the registered service `name` as `serviceId` and your subsystem ID as
   `X-Client-Id`:

   ```sh
   curl 'https://<consumer-runtime-host>/sdx/0/<serviceId>/<operation-path>' \
     -H 'X-Client-Id: <consumer-subsystem-id>' \
     -H "Authorization: Bearer ${ACCESS_TOKEN}"
   ```

   Use the service's documented method and operation path. The token's
   authorized client must be allowed for the selected consumer subsystem. See
   the [Connection Resources](/how-to/sdx-connection-resources.md).

1. Verify an actual service operation with the provider, including approved scopes
   and target-zone identity when exchange applies. `/hello` tests the provider
   edge only. Check that missing/invalid credentials and unapproved access are
   denied.

## Revoke access in the SDX UI (Access Manager)

Revocation removes an existing approved connection. To reject an unapproved
request, use **Approve / Reject** instead.

1. In **Member Console → Connection Requests**, select the provider organization
   and environment, and find the approved consumer-to-service connection.
   Confirm the consumer, service and scopes before proceeding.
1. If the connection is active, select **Customize...**, clear **Active**, then
   select **Save**. Coordinate this step with the subsystem's technical lead if
   your account is not permitted to change activation. Wait for the provisioner
   to remove the gateway configuration on both sides; review **Connection
   details** for progress or errors.
1. Select **Revoke access** and review the confirmation dialog. Confirm only when
   you intend to remove that connection; this action deletes the connection,
   rather than merely pausing it.
1. Check the result message and refresh the list to confirm the connection is
   gone. If deletion reports remaining gateway configuration, wait for cleanup
   or ask the technical lead/APS team to resolve the provisioner error, then
   retry. An error message is not confirmation that access was revoked.
1. Coordinate with the consumer to confirm CSS has processed the revocation and
   removed the corresponding integration access/scopes. Verify the service is
   no longer accessible through the revoked connection; do not infer immediate
   invalidation of already issued tokens from the UI message alone.

The UI performs the connection deletion on your behalf, replacing the Restish
commands in
[deleting a connection](/how-to/sdx-connections.md#deleting-a-connection).
Reinstating access after deletion requires a new request and approval. If a
connection or action is missing, confirm the provider organization, environment
and subsystem role with your administrator.

<!-- prettier-ignore -->
??? note "Associating an OAuth integration client with a connection"
    `requesterDetails.client.clientId` (used above for
    `sdx-p2p-consumer-access.r1`/ACL and, when configured, `consumerMatch`) is
    provisioner-managed. It cannot be written directly through the SDX
    management API — attempting a direct `upsert-connection` update of
    `requesterDetails` returns `HTTP 400`. Registering an `integrationClientId`
    on the consumer subsystem (see
    [Register an SDX Subsystem](/how-to/sdx-subsystems.md)) is only the first
    half of the relationship: the field is populated by calling the supported
    `POST /v1/integrations/{clientId}/access-requests` operation on the SDX
    Partner Authorization Services API, which validates the requested scopes
    against the registered OAD and writes the requester metadata with trusted
    provisioner credentials. That API uses a separate base URL and bearer-token
    audience from the main SDX API — consult the APS team for the current
    Restish/API configuration for it. Before enabling strict `consumerMatch`,
    verify that the connection contains the integration client and that the Kong
    consumer created by `sdx-p2p-consumer-access.r1` exists, since enabling
    `consumerMatch` ahead of a matching consumer blocks legitimate traffic.

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

The requesting client is responsible for requesting any audience required by the
provider API or another downstream resource. SDX propagates those verified
original audiences and removes exact duplicates. Retaining the SDX exchange
client allows the provider to use the exchanged token for a subsequent SDX call.
An original token containing only the SDX exchange client is valid when no
target resource requires another audience.

The optional plugin setting `tokenExchange.audience` adds one configured
audience to the exchange request. When present, SDX merges it with the verified
original audiences and removes duplicates. This supports both connections that
use a configured audience and connections whose target audiences are already
present in the original token. Current provisioning policies may require or
supply the configured value.

### Original token has no usable scope claim (E4)

Verified-subject scope derivation fails before the token endpoint is called when
the verified token is unavailable, its `scope` claim is missing or is not a
string, or the claim is empty or contains only whitespace. Each condition
returns HTTP 500:

```json
{
  "message": "Token exchange failed",
  "error": { "code": "E4" }
}
```

This E4 response does not include a request ID. Kong logs
`Unable to derive token exchange scopes:` followed by
`verified subject token is unavailable`,
`verified subject token has no string scope claim`, or
`verified subject token has an empty scope claim`.

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
authorization server response or error description, client assertion, or tokens.

An explicit granted scope set that differs from the requested set is a warning,
not an exchange failure. SDX continues with the successful exchanged token, and
the provider's normal token validation and authorization rules apply.

## CLI alternative for connection cleanup

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
