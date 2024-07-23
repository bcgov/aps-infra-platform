---
title: Generate a Service Account
---

<!-- overview -->

This guide explains how to generate a service account.

{Optional: Specify when and why your user might want to perform the task.}
A service account can be used instead of IDIR to login to the `gwa` command line interface (CLI).
This is useful for integrating with CI/CD pipelines.
Ask Aidan Cope about other benefits.

## Before you begin

Before you begin, ensure you:

- [Create a Gateway](/reference/gwa-commands.md#gatewaycreate)

## Generate a Service Account

1. Login to the [Test](https://api-gov-bc-ca.test.api.gov.bc.ca/) or [Production](https://api.gov.bc.ca/) instance of the Portal, whichever you are working in.

2. Go to the **Gateways** tab. Select the **Gateway** you would like to create a service account for.

3. Click **Service Accounts**, then click **Create New Service Account**.

4. Select the **GatewayConfig.Publish** permission for the Service Account and click **Share**. A new credential will be created - make a note of the `Client ID` and `Client Secret`.

!!! note
    Make sure to save the generated `Client ID` and `Client Secret` as it will not be possible to retrieve them once the dialog is closed.

The following list describes the permissions:

| Scope                    | Permission                                                                                                                                                                               |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Gateway.Manage`       | Permission to update the Access Control List for controlling access to viewing metrics, service configuration and service account management (effectively a superuser for the Gateway) |
| `Gateway.View`         | Read-only access to the Gateway                                                                                                                                                        |
| `GatewayConfig.Publish`  | Permission to publish Gateway configuration to Kong and view the status of the upstreams                                                                                                 |
| `Content.Publish`        | Permission to update the documentation on the portal                                                                                                                                     |
| `CredentialIssuer.Admin` | Permission to create Authorization Profiles for integrating with third-party Identity Providers; yhe profiles are available to be used when configuring Product Environments             |
| `Access.Manage`          | Permission to approve/reject access requests to your APIs                                

## Next steps

- [CI/CD Integration](/how-to/cicd-integration.md)