---
title: Generate a Service Account
---

<!-- overview -->

This guide explains how to generate a service account.

{Optional: Specify when and why your user might want to perform the task.}
A service account can be used instead of IDIR to login to the `gwa` command line interface (CLI).
This is useful for intergrating with CI/CD pipelines.
Ask aidan about other benefits

## Before you begin

Before you begin, ensure you:

- [Create a Namespace](/resources/gwa-commands.md#namespacecreate)

## Generate a Service Account

1. Login to the [Test](https://api-gov-bc-ca.test.api.gov.bc.ca/) or [Production](https://api.gov.bc.ca/) instance of the Portal, whichever you are working in.

2. Go to the `Namespaces` tab.

3. Click `Service Accounts`, then Cick `New Service Account`.

4. Select the `GatewayConfig.Publish` permission for the Service Account and click `Share`. A new credential will be created - make a note of the `ID` and `Secret`.

> NOTE: Make sure to save the generated Client ID and Secret.

The following list describes the permissions:

| Scope                    | Permission                                                                                                                                                                               |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Namespace.Manage`       | Permission to update the Access Control List for controlling access to viewing metrics, service configuration and service account management (effectively a superuser for the namespace) |
| `Namespace.View`         | Read-only access to the namespace                                                                                                                                                        |
| `GatewayConfig.Publish`  | Permission to publish gateway configuration to Kong and view the status of the upstreams                                                                                                 |
| `Content.Publish`        | Permission to update the documentation on the portal                                                                                                                                     |
| `CredentialIssuer.Admin` | Permission to create Authorization Profiles for integrating with third-party Identity Providers; yhe profiles are available to be used when configuring Product Environments             |
| `Access.Manage`          | Permission to approve/reject access requests to your APIs                                

## Next steps

- [CI/CD Integration](/resources/cicd-integration.md)