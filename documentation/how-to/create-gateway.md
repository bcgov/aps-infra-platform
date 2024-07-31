---
title: Create a Gateway
---

<!-- overview -->

This guide explains how to create a {{ glossary_tooltip term_id="gateway"}} in
the API Services Portal. Gateways are the top-level entitiy in the API Services
Portal for API providers and serve as a project container. Creating a Gateway is
the first step in adding a new API to the API Services Portal.

<!-- prerequisites -->

## Before you begin

Before you begin, ensure you:

- [Install gwa CLI](/how-to/gwa-install.md)

## Create a Gateway

Using the `gwa` command line interface (CLI), create a Gateway by running this command:

```sh linenums="0"
gwa gateway create
```

You'll be prompted to provide a display name to help you identify the Gateway.

The expected output is similar to this:

```sh linenums="0"
Gateway created. Gateway ID: gw-cf97b, display name: My New Gateway
```

<!-- whatsnext -->

## Next steps

- If you are just getting started, try the [API Provider Quick Start](/tutorials/quick-start.md) tutorial
- Read more about [`gwa gateway create`](/reference/gwa-commands.md/#gatewaycreate) command
- [Manage Team Access](/how-to/gateway-admin.md)
- [Create a Gateway Service](/how-to/create-gateway-service.md)