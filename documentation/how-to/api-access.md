---
title: Manage Consumer Access
---

This guide explains how API Providers can use the API Services Portal to manage
access to their APIs.

## Before you begin

Before you begin, ensure you:

- [Create a Gateway](/how-to/create-gateway.md)
- [Create a Gateway Service](/how-to/create-gateway-service.md)
- Configure a protected Gateway Service with [API Key](/how-to/kong-api-key.md)
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
- Consumer requests (requestor, application, status)
- Consumer access, metrics, and controls
