---
title: Manage Team Access
---

## Grant access to other users

To grant access to other members of your team, you need to grant them the
appropriate Scopes. You can do this from the API Services Portal by navigating
to **Gateways**, clicking the relevant **Gateway**, and selecting
**Administration Access** from the Actions list. From there, you can grant users
access to the Gateway.

!!! note
    Users must sign in to the API Services Portal at least once before you can
    grant them access to a Gateway.

| Environment     | API Services Portal Link                 |
| --------------- | ---------------------------------------- |
| TEST / TRAINING | <https://api-gov-bc-ca.test.api.gov.bc.ca> |
| PRODUCTION      | <https://api.gov.bc.ca>                    |

## Using Service Accounts

Service Accounts are credentials that can be used to access the APS Directory
and Gateway APIs.

### Generate a Service Account

1. Login to the API Services Portal, navigate to **Gateways**, and select the
   relevant **Gateway**.

2. Select **Service Accounts** from the Actions list, then click **Create New
   Service Account**.

3. Select the **GatewayConfig.Publish** checkbox for the Service Account and
   click **Share**. A new credential will be created. Make a note of the `Client
   ID` and `Client Secret`.

> Make sure to save the Client ID and Secret as they will not be
> retrievable once the dialog is closed.

## Available permissions

The following list describes the access permissions:

| Scope                    | Permission                                                                                                                                                                               |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Gateway.Manage`       | Permission to update the Access Control List for controlling access to viewing metrics, service configuration and service account management (effectively a superuser for the Gateway) |
| `Gateway.View`         | Read-only access to the Gateway                                                                                                                                                        |
| `GatewayConfig.Publish`  | Permission to publish Gateway configuration to Kong and view the status of the upstreams                                                                                                 |
| `Content.Publish`        | Permission to update the documentation on the portal                                                                                                                                     |
| `CredentialIssuer.Admin` | Permission to create Authorization Profiles for integrating with third-party Identity Providers; the profiles are available for use when configuring Product Environments                |
| `Access.Manage`          | Permission to approve/reject access requests to your APIs                                                                                                                                |

## About the Admin APIs

! note
    The Admin APIs are used internally by the CLI and API Services Portal
    to manage Gateway settings and operations. They provide endpoints to
    configure Services, Products, and access control.

### Directory API

| Environment     | Directory API Swagger Console Link                                                                 |
| --------------- | -------------------------------------------------------------------------------------------------- |
| TEST / TRAINING | <https://openapi.apps.gov.bc.ca?url=https://api-gov-bc-ca.test.api.gov.bc.ca/ds/api/v2/openapi.yaml> |
| PRODUCTION      | <https://openapi.apps.gov.bc.ca?url=https://api.gov.bc.ca/ds/api/v2/openapi.yaml>                    |

### Kong Gateway API

| Environment     | Kong Gateway API Swagger Console Link                                                                |
| --------------- | ---------------------------------------------------------------------------------------------------- |
| TEST / TRAINING | <https://openapi.apps.gov.bc.ca?url=https://gwa-api-gov-bc-ca.test.api.gov.bc.ca/docs/v2/openapi.yaml> |
| PRODUCTION      | <https://openapi.apps.gov.bc.ca?url=https://gwa.api.gov.bc.ca/docs/v2/openapi.yaml>                    |

#### Swagger Console

Go to the `gwa-api` **Swagger Console** and navigate to the `PUT` `/gateways/{gw}/gateway`
API.

The Service Account uses the OAuth2 Client Credentials Grant Flow. Click the
**Lock** action on the right and enter the Service Account credentials obtained
from [Generate a Service Account](/how-to/gateway-admin.md/#generate-a-service-account).

Close the modal dialog and click **Try it out**.

Under **Parameters**, provide the **Gateway**.

Set **dryRun** to `true`.

Select a `configFile` file.

Click **Execute** to send the request.

#### Postman

From the Postman App, click **Import**. Go to the **Link** tab and enter one of
the below URLs.

| Environment     | Kong Gateway API Postman URL                                                                                  |
| --------------- | ------------------------------------------------------------------------------------------------------------- |
| TEST / TRAINING | <https://openapi-to-postman.api.gov.bc.ca/?u=https://gwa-api-gov-bc-ca.test.api.gov.bc.ca/docs/v2/openapi.yaml{:data-proofer-ignore}> |
| PRODUCTION      | <https://openapi-to-postman.api.gov.bc.ca/?u=https://gwa.api.gov.bc.ca/docs/v2/openapi.yaml{:data-proofer-ignore}>                    |

After creation, go to **Collections** and right-click on the
**Gateway Administration API** collection and select **Edit**.

Go to the **Authorization** tab, enter your `<Client ID>` and `<Client Secret>`,
and click **Get New Access Token**.

You should get a successful dialog to proceed. Click **Proceed** and **Use Token**.

You can verify that the token works by going to the Collection
**Return key information about authenticated identity** and clicking **Send**.
