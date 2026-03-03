---
title: Manage Consumer Access
---

## Use the Access Approval Process

Enable `approval` for an Environment and act as Access Manager, reviewing
requests and approving access to your APIs.

## Manage Access and Controls

!!! note
    To manage access to your APIs, you must have the `Access.Manage`
    permission for the Gateway.

As an Access Manager, you can manage new Consumers by going to the **Gateways**
tab, selecting a **Gateway**, and clicking the **Consumers** card.

Here you should see the newly created Consumer. Click on the `name` in the
**Name/ID** column to view **Consumer Details** and **Products** they have
access to.

You can administer **Controls** such as rate limiting and IP restrictions.

You can administer **Authorization** by toggling access to the particular
Product and Environment.

## Export Gateway Report

On the **Gateways** tab on the API Services Portal, click **Export Gateway
Report**  to generate an Excel report for your Gateways, including data on:

- Gateways (permitted hosts, data plane, organization)
- Gateway access (user and service account permissions)
- Gateway metrics (total requests in the last 30 days)
- Gateway controls (plugin configuration)
- Consumer requests (requestor, application, status)
- Consumer access, metrics, and controls
