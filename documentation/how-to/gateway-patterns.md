---
title: Using Gateway Patterns
---

This guide explains how to generate configuration using predefined patterns.

## Before you begin

You should be familiar with using the `gwa` CLI and configuring gateway configuration.

Before you begin, ensure you:

- [Install gwa CLI](/how-to/gwa-install.md)
- [Create a Gateway](/how-to/create-gateway.md)

## Use a predefined pattern

Refer to the available patterns below to create a `pattern.yaml` file.

Using the `gwa` command line (version `3.0.7` or higher),
you can run `gateway-pattern` and pipe it to the `apply` command to apply the configuration:

  ```sh linenums="0"
  gwa gateway-pattern pattern-input.yaml | gwa apply -i -`

## Available Patterns

| Pattern             | Plugins | Description           |
| ------------------- | ------- | --------------------- |
| `simple-service.r1` | none    | Minimal configuration |

### `simple-service.r1`

Example `pattern-input.yaml`:

```yaml
pattern: simple-service.r1
parameters:
  service_name: <SERVICE_NAME>
  service_url: "https://httpbun.com"
```
