---
title: Kong API Key
---

<!-- overview -->

This guide explains how to add key-based authentication to your GatewayService.

You can read more about key-based authentication in the [Protect an API](/concepts/protect-api.md) concept page.

<!-- prerequisites -->

## Before you begin

Before you begin, ensure you:

- [Install gwa CLI](/how-to/gwa-install.md)
- [Create a Namespace](/resources/gwa-commands.md#namespacecreate)
- [Create a Service](/how-to/create-gateway-service.md)

<!-- steps -->

## Key-auth plugin

You can add the following plugin to your Gateway Configuration file to add key-based authentication to your GatewayService:

```yaml
  plugins:
  - name: key-auth
    tags: [ ns.<YOUR_NAMESPACE> ]
    protocols: [ http, https ]
    config:
      key_names: ["X-API-KEY"]
      run_on_preflight: true
      hide_credentials: true
      key_in_body: false
```

It is recommended to [share your API](/how-to/api-discovery.md) for discovery so that consumers of your API can request an API key.

## Next steps

- [Share an API](/how-to/api-discovery.md)
