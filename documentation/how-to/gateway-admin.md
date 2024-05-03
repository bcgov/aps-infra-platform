---
title: Manage Team Access
---

## Grant Access to Other Users

To grant access to other members of your team, you need to grant them the appropriate Scopes. You can do this from the `API Services Portal` by selecting the relevant `Namespace` and going to the Namespaces `Namespace Access` page. From there, you can grant users access to the Namespace.

!!! note
    Users must sign in to the API Services Portal at least once before you can grant them access to a Namespace.

| Environment     | API Services Portal Link                 |
| --------------- | ---------------------------------------- |
| TEST / TRAINING | https://api-gov-bc-ca.test.api.gov.bc.ca |
| PRODUCTION      | https://api.gov.bc.ca                    |

## Using Service Accounts

Service Accounts are credentials that can be used to access the APS Directory and Gateway APIs.

### Generate a Service Account

1. Login to the API Services Portal, select your namespace, and go to the `Namespaces` tab.

2. Click `Service Accounts`, then Cick `New Service Account`.

3. Select the `GatewayConfig.Publish` permission for the Service Account and click `Share`. A new credential will be created - make a note of the `ID` and `Secret`.

> NOTE: Make sure to save the generated Client ID and Secret.

## Available Permissions

The following list describes the permissions:

| Scope                    | Permission                                                                                                                                                                               |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Namespace.Manage`       | Permission to update the Access Control List for controlling access to viewing metrics, service configuration and service account management (effectively a superuser for the namespace) |
| `Namespace.View`         | Read-only access to the namespace                                                                                                                                                        |
| `GatewayConfig.Publish`  | Permission to publish gateway configuration to Kong and view the status of the upstreams                                                                                                 |
| `Content.Publish`        | Permission to update the documentation on the portal                                                                                                                                     |
| `CredentialIssuer.Admin` | Permission to create Authorization Profiles for integrating with third-party Identity Providers; the profiles are available for use when configuring Product Environments                |
| `Access.Manage`          | Permission to approve/reject access requests to your APIs                                                                                                                                |

## About the Admin APIs

### Directory API

| Environment     | Directory API Swagger Console Link                                                                 |
| --------------- | -------------------------------------------------------------------------------------------------- |
| TEST / TRAINING | https://openapi.apps.gov.bc.ca?url=https://api-gov-bc-ca.test.api.gov.bc.ca/ds/api/v2/openapi.yaml |
| PRODUCTION      | https://openapi.apps.gov.bc.ca?url=https://api.gov.bc.ca/ds/api/v2/openapi.yaml                    |

### Kong Gateway API

| Environment     | Kong Gateway API Swagger Console Link                                                                |
| --------------- | ---------------------------------------------------------------------------------------------------- |
| TEST / TRAINING | https://openapi.apps.gov.bc.ca?url=https://gwa-api-gov-bc-ca.test.api.gov.bc.ca/docs/v2/openapi.yaml |
| PRODUCTION      | https://openapi.apps.gov.bc.ca?url=https://gwa.api.gov.bc.ca/docs/v2/openapi.yaml                    |

#### Swagger Console

Go to `gwa-api Swagger Console` and select the `PUT` `/namespaces/{namespace}/gateway` API.

The Service Account uses the OAuth2 Client Credentials Grant Flow. Click the `lock` link (on the right) and enter the Service Account credentials generated in Section 2.

For the `Parameter namespace`, enter the namespace you created in Section 1.

Set `dryRun` to `true`.

Select a `configFile` file.

Send the request.

#### Postman

From the Postman App, click `Import` and go to the `Link` tab, enter one of the below URLs.

| Environment     | Kong Gateway API Postman URL                                                                                  |
| --------------- | ------------------------------------------------------------------------------------------------------------- |
| TEST / TRAINING | https://openapi-to-postman.api.gov.bc.ca/?u=https://gwa-api-gov-bc-ca.test.api.gov.bc.ca/docs/v2/openapi.yaml{:data-proofer-ignore} |
| PRODUCTION      | https://openapi-to-postman.api.gov.bc.ca/?u=https://gwa.api.gov.bc.ca/docs/v2/openapi.yaml{:data-proofer-ignore}                    |

After creation, go to `Collections` and right-click on the `Gateway Administration (GWA) API` collection and select `edit`.

Go to the `Authorization` tab, enter your `Client ID` and `Client Secret`, and click `Get New Access Token`.

You should get a successful dialog to proceed. Click `Proceed` and `Use Token`.

You can verify that the token works by going to the Collection `Return key information about authenticated identity` and clicking `Send`.
