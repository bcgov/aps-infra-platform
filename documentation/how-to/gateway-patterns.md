---
title: Using Gateway Patterns
---

A {{ glossary_tooltip term_id="gateway" }} provides a
mechanism for isolating groups of resources and can be managed by multiple users
on a team.

An administrator has the flexibility of configuring the resources
to fulfill their particular requirements.

There is now an option for an administrator to use predefined configurations,
making setup faster and ensures the config is based around proven security
and gateway standards.

This guide explains how to generate configuration using predefined patterns.

## Before you begin

You should be familiar with using the `gwa` CLI and configuring gateway configuration.

Before you begin, ensure you:

- [Install gwa CLI](/how-to/gwa-install.md)
- [Create a Gateway](/how-to/create-gateway.md)

## Use a predefined pattern

1. Create a `pattern-input.yaml` file containing input for one of the available patterns below.

   Review the provided example `pattern-input.yaml` for required parameters.

2. Generate gateway configuration and apply it.

   Using the `gwa` command line (version `3.0.7` or higher),
   run `gateway-pattern` using your inputs, and pipe the output to the `apply` command:

```sh linenums="0"
gwa gateway-pattern pattern-input.yaml | gwa apply -i -
```

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
