---
title: Generate a Service Account
---

1. Go to the `Namespaces` tab.

2. Click `Service Accounts`, then Cick `New Service Account`.

3. Select the `GatewayConfig.Publish` permission for the Service Account and click `Share`. A new credential will be created - make a note of the `ID` and `Secret`.

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