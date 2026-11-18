---
title: Manage Consumer Access
---

This guide explains how API Providers can use the API Services Portal to manage
access to their APIs.

To issue or regenerate credentials programmatically without an Access Request,
see [Issue Consumer Credentials via API](/how-to/self-issue-credentials.md).

## Before you begin

Before you begin, ensure you:

- [Create a Gateway](/how-to/create-gateway.md)
- [Create a Gateway Service](/how-to/create-gateway-service.md)
- Configure a protected Gateway Service with [Kong API Key + ACL](/how-to/kong-api-key.md)
or [Client Credential](/tutorials/protect-client-cred.md)
- [Share an API](/how-to/api-discovery.md)

## Use the access approval process

1. Enable `approval` for a Product Environment (either via Portal UI or gateway
   configuration)

2. Consumers can request access via the API Directory after logging in with one
of the developer identity providers.

3. Access Managers will be notified when access requests are created. To review
and approve requests, go to the **Gateways** tab, select a **Gateway**, and
click the **Consumers** card. Pending access requests will be shown at the top
of the page.

!!! note
    To manage access to your APIs, you must have the `Access.Manage`
    permission for the Gateway.

## Manage access and controls

As an Access Manager, you can manage Consumers by going to the **Gateways**
tab, selecting a **Gateway**, and clicking the **Consumers** card.

Click on the consumer's name in the **Name/ID** column to view **Consumer
Details** and **Products** they have access to. To modify consumer access, click
the **Edit** button next to the Product Environment.

You can administer **Controls** such as rate limiting and IP restrictions.

You can administer **Authorization** by toggling access to the particular
Product and Environment.

## Export gateway report

On the **Gateways** tab on the API Services Portal, click **Export Gateway
Report**  to generate an Excel report for your Gateways, including data on:

- Gateways (permitted hosts, data plane, organization)
- Gateway access (user and service account permissions)
- Gateway metrics (total requests in the last 30 days)
- Gateway controls (plugin configuration)
- Consumer requests (requestor and requestor email, application, status)
- Consumer access (application owner and owner email), metrics, and controls

## Get consumer contact details via API

Use the gateway report endpoints to get your consumers' contact details as
JSON, for example to notify them about API changes, deprecations, or
when a job they submitted has finished.

| Report            | Method | Path                                                       |
| ----------------- | ------ | ---------------------------------------------------------- |
| Consumer access   | `GET`  | `/ds/api/v3/gateways/{gatewayId}/report/consumer-access`   |
| Consumer requests | `GET`  | `/ds/api/v3/gateways/{gatewayId}/report/consumer-requests` |

- **Consumer access** returns one row per consumer and Product Environment, with
  the application name and the application owner's name (`app_owner_name`) and
  email (`app_owner_email`). These are the same rows as the **Consumer Access
  (Products)** sheet in the gateway report.
- **Consumer requests** returns the access requests made for the Gateway's
  Products, with the requestor's name (`requestor`) and email
  (`requestor_email`) and the request result. These are the same rows as the
  **Consumer Requests** sheet in the gateway report.

To call these endpoints, use a user token or a
[Service Account](/how-to/generate-service-account.md) with the
`Namespace.View` or `Access.Manage` scope on the Gateway:

```http
GET /ds/api/v3/gateways/{gatewayId}/report/consumer-access
Authorization: Bearer <token>
```

For interactive API reference, open the
[Directory API OpenAPI console](https://api.gov.bc.ca/ds/api/v3/console) and look
under **Gateways** for the `gateway-report-consumer-access` and
`gateway-report-consumer-requests` operations.
