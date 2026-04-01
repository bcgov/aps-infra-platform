---
title: Generate a Service Account
---

<!-- overview -->

This guide explains how to generate a service account.

A service account can be used instead of IDIR to login to the `gwa` command line
interface (CLI). This is useful for integrating with CI/CD pipelines.

## Before you begin

Before you begin, ensure you:

- [Create a Gateway](/how-to/create-gateway.md)

## Generate a Service Account

1. Login to the [API Services Portal](https://api.gov.bc.ca/) and navigate to
   the **Gateways** tab. Select the **Gateway** you would like to create a
   service account for.

1. Click **Service Accounts**, then click **Create New Service Account**.

1. Select the **GatewayConfig.Publish** permission (or other permissions as
   needed) for the Service Account and click **Share**. A new credential will be
   created - make a note of the `Client ID` and `Client Secret`.

!!! note
    Make sure to save the generated `Client ID` and `Client Secret` as it will
    not be possible to retrieve them once the dialog is closed.

The following list describes the permissions:

| Scope                    | Permission                                                                                                                                                                               |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Gateway.Manage`       | Permission to update the Access Control List for controlling access to viewing metrics, service configuration and service account management (effectively a superuser for the Gateway) |
| `Gateway.View`         | Read-only access to the Gateway                                                                                                                                                        |
| `GatewayConfig.Publish`  | Permission to publish Gateway configuration to Kong and view the status of the upstreams                                                                                                 |
| `Content.Publish`        | Permission to update the documentation on the portal                                                                                                                                     |
| `CredentialIssuer.Admin` | Permission to create Authorization Profiles for integrating with third-party Identity Providers; the profiles are available to be used when configuring Product Environments             |
| `Access.Manage`          | Permission to approve/reject access requests to your APIs

## v1 Service Accounts

Services accounts created using early versions of the API Services Portal (prior
to 2022) are only supported by the v1 of the Portal API, and v1.2.0 or less of
the `gwa` CLI. These v1 service accounts can be identified by a short client ID
with structure `sa-<gatewayId>-<id>`, whereas new service accounts have
structure `sa-<gatewayId>-ca853245-<id>`.

If you need to recreate a v1 service account for use in a CI/CD pipeline, you
will also need to update your workflow to use a newer version of the `gwa` CLI.
See [CI/CD Integration](/how-to/cicd-integration.md) for example configuration.

## Next steps

- [CI/CD Integration](/how-to/cicd-integration.md)
