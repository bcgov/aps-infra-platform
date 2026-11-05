---
title: Kong API Key + ACL
---

<!-- overview -->

This guide explains how to protect your Gateway Service with a Kong API key and
an Access Control List (ACL), so that only consumers you approve for your Product
Environment can call it. This is the `kong-api-key-acl` flow, and it is the
typical choice when you protect an API with API keys.

You can read more about the API key flows and how they differ on the
[Protect an API](/concepts/protect-api.md#kong-api-key-flows) Concept page.

!!! warning "API key without ACL is only for public APIs"
    The `key-auth` plugin on its own (the `kong-api-key-only` flow) checks that
    a request has a valid API key, but not that the key was issued for your
    API. Any valid API key issued by any Gateway on the platform is accepted.
    Only use API key without ACL for public APIs.

    If your API is public and you want to give a higher rate limit to consumers
    who request one, see [Two-tiered access](/how-to/COMMON-CONFIG.md#two-tiered-access).

<!-- prerequisites -->

## Before you begin

Before you begin, ensure you:

- [Install gwa CLI](/how-to/gwa-install.md)
- [Create a Gateway](/how-to/create-gateway.md)
- [Create a Gateway Service](/how-to/create-gateway-service.md)
- [Create a Product](/how-to/api-discovery.md#link-your-dataset-to-a-product)
  with an Environment for your Gateway Service

<!-- steps -->

## How it works

The `kong-api-key-acl` flow uses two plugins on your Gateway Service:

- `key-auth` checks that the request has a valid API key and identifies the
  consumer.
- `acl` checks that the consumer belongs to the ACL group allowed for your
  Product Environment.

Each Product Environment has a unique `appId` that the API Services Portal
generates for it. When you approve an access request for the Environment, the
Portal adds the consumer to an ACL group named after the Environment's `appId`.

Your `acl` plugin must allow that `appId`. Requests with a valid API key from a
consumer that is not in the group are rejected.

## Set the Environment flow

Set the Authorization for your Product Environment to the `kong-api-key-acl`
flow:

=== "Web UI"
    1. Sign in to the [API Services Portal](https://api.gov.bc.ca/), navigate to
    **Gateways**, select your **Gateway**, then click the **Products** card.
    2. Click **Edit** next to the Environment, then click **Configure
    environment**.
    3. Set **Authorization** to **Kong API Key with ACL Flow**.
    4. Save your changes.

=== "CLI"
    1. Set `flow: kong-api-key-acl` on the Environment in your Product
    configuration:

      ```yaml title="Product template"
      kind: Product
      name: Useful API # Name shown on the API Directory
      dataset: dataset-name # Dataset name or BC Data Catalogue slug value
      environments:
      - name: prod
        active: false
        flow: kong-api-key-acl
        services: [ <SERVICE_NAME> ]
      ```

    2. Publish the Product: `gwa apply -i <product.yaml>`

## Get the Environment `appId`

Get the `appId` of the Product Environment that your Gateway Service belongs to.
Each Environment (for example `dev`, `test` and `prod`) has its own `appId`.

=== "Plugin Template"
    1. On the API Services Portal, open the Environment's **Configure
    environment** page, as in [Set the Environment flow](#set-the-environment-flow).
    2. With **Authorization** set to **Kong API Key with ACL Flow**, click
    **View Plugin Template**.

    The template shows the `key-auth` and `acl` plugin configuration for the
    Environment, with your Gateway ID and the Environment's `appId` filled in.
    You can copy it into your Gateway configuration.

=== "Directory API"
    1. Call the Directory API with a token that has `Namespace.Manage` access to
    the Gateway:

      ```http
      GET /ds/api/v3/gateways/{gatewayId}/products
      Authorization: Bearer <token>
      ```

    2. From the response, copy `[].environments[].appId` for the target
    Environment.

    You can also run this request from the
    [Directory API OpenAPI console](https://api.gov.bc.ca/ds/api/v3/console).
    See [Get `environmentAppId`](/how-to/self-issue-credentials.md#get-environmentappid)
    for the step-by-step console instructions and how to get a token.

## Add the plugins

Add the `key-auth` and `acl` plugins to your Gateway Service in your Gateway
configuration file. Replace `<environment appId>` with the `appId` from the
previous step:

```yaml
  plugins:
  - name: key-auth
    tags: [ ns.<gatewayId> ]
    protocols: [ http, https ]
    config:
      key_names: ["X-API-KEY"]
      run_on_preflight: true
      hide_credentials: true
      key_in_body: false
  - name: acl
    tags: [ ns.<gatewayId> ]
    config:
      hide_groups_header: true
      allow: [ "<environment appId>" ]
```

Then publish your Gateway configuration:

``` linenums="0"
gwa apply -i <gw-config.yaml>
```

!!! note
    The `acl` plugin rejects every request until a consumer is added to the
    `appId` group. After you add the plugin, consumers can only call the
    service once their access request is approved.

## Share your API

[Share your API](/how-to/api-discovery.md) for discovery so that consumers can
request access. When an access request is approved, the Portal adds the
consumer to the Environment's ACL group and their API key starts working.

## Next steps

- [Share an API](/how-to/api-discovery.md)
- [Manage Consumer Access](/how-to/api-access.md)
- [Access Control List plugin reference](/reference/plugins/acl.md)
