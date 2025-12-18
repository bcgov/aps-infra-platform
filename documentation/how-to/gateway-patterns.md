---
title: Gateway Patterns
---

This guide explains how to generate configuration using predefined patterns.

## Before you begin

You should be familiar with using the `gwa` CLI and configuring gateway configuration.

Before you begin, ensure you:

- [Install gwa CLI](/how-to/gwa-install.md)
- [Create a Gateway](/how-to/create-gateway.md)

## Use a predefined pattern

Prepare a `pattern.yaml` file using one of the available patterns described below.

Using the `gwa` command line (version `3.0.7` or higher),
you can run `generate-pattern` and pipe it to the `apply` command to apply the configuration:

`gwa generate-pattern pattern.yaml | gwa apply -i -`

## Available Patterns

| Pattern             | Plugins | Description           |
| ------------------- | ------- | --------------------- |
| `simple-service.r1` | none    | Minimal configuration |

### `simple-service.r1`

Example `pattern.yaml`:

```yaml
pattern: simple-service.r1
parameters:
  service_name: test-abc
  service_url: "https://httpbun.com"
```
