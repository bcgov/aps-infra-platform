---
title: Gateway Configuration
---

This article explains the basics of gateway configurations. Gateway
configurations define how the API gateway routes incoming requests, applies
security measures, handles transformations, and performs other tasks related to
API management. As such, they are the most fundamental part of setting up your
API in the API Services Portal.

## Background

Kong is an open-source API gateway and microservices management layer which
powers the API Services Portal. A Kong gateway configuration is a
{{ glossary_tooltip term_id="yaml-file" text="YAML file" }} used to define the
configuration settings for Kong, such as routes, services, and plugins, using
declarative syntax.

## Use case

In a Gateway configuration file, you can specify details like:

1. [Services](/concepts/services.md): These represent the backend services that
Kong will proxy requests to.

2. Routes: Routes define rules for matching incoming requests to services.

3. [Plugins](/concepts/plugins.md): Plugins are used to add functionalities like
authentication, rate limiting, logging, etc., to your API endpoints.

Here's an example of what a simple Gateway Configuration might look like:

```yaml
kind: GatewayService
name: example-service-dev
tags: [ ns.<gatewayId> ]
host: httpbin.org
port: 443
protocol: https
retries: 0
routes:
  - name: example-service-route
    tags: [ ns.<gatewayId> ]
    hosts:
      - example-service.dev.api.gov.bc.ca
    methods:
      - GET
    strip_path: false
    https_redirect_status_code: 426
    path_handling: v0
    request_buffering: true
    response_buffering: true
plugins:
  - name: request-transformer
    tags: [ ns.<gatewayId> ]
    enabled: true
    config:
      add:
        headers:
        - x-new-header:value
        - x-another-header:something
```

This configuration defines a service `example-service-dev` with a corresponding
route `example-service-route` and applies a `request-transformer` plugin to it
to add custom headers.

## Gateway configuration formats

There are two Gateway configuration formats that can be used:

- **Legacy format:** Introduced with v1 of the `gwa` CLI. This format supports
  only basic GatewayService configuration.

  ```yaml
  services:
    - name: example-service-1
      host: httpbin.org
      ...
    - name: example-service-2
      host: httpbin.org
      ...
  ```

- **Resource-based format:** An updated format introduced with v2 of `gwa`. This
  format supports additional resource types for the API Services Portal.
  Individual resources are separated by `---`.

  ```yaml
  kind: GatewayService
  name: example-service-1
  host: httpbin.org
  ...

  ---
  kind: GatewayService
  name: example-service-2
  host: httpbin.org
  ...

  ---
  kind: Product
  name: example-product
  ...
  ```

Unless you need to load SSL certificates to support [custom
domains](/how-to/custom-domain) or
[mTLS](/how-to/upstream-services.md#verify-upstream-services-with-mtls), the
resource-based format is recommended for its flexibility and support for
additional resource types.

### Key differences between formats
| Attribute                                                                       | Legacy                   | Resource-based |
|------------------------------------------------------------------------------|--------------------------|----------------|
| Supports GatewayService configuration                                        | ✅                        | ✅              |
| Supports SSL certificates                                                    | ✅                        | ❌              |
| Supports additional resource types (Product, DraftDataset, CredentialIssuer) | ❌                        | ✅              |
| Publish command                                                              | `publish-gateway` (`pg`) | `apply`        |
| Minimum `gwa` CLI version                                                    | v1.0.0                      | v2.0.4             |

## Configuration update behaviour

The configuration update behaviour depends on the type of resource and applies
to both legacy and resource-based formats.

### Gateway Service Configuration

For Gateway Services, the configuration is **declarative**:
- The provided configuration represents the exact state of the Gateway Services
  that will be set up.
- In the resource-based format, if no `kind: GatewayService` resources are
  included, the Gateway Service configuration will remain unchanged.

!!! note "Clearing Gateway Service configuration"
    To clear all Gateway Service configuration, create a YAML file with the following content:
    ```yaml
    services: []
    ```
 
### Other resource types

For other resource types, such as Product, DraftDataset, or CredentialIssuer:

- If no resource with the same `name` exists, a new resource will be created. 
- If a resource with the same `name` exists, it will be updated with the provided configuration.

This provides flexibility for managing non-GatewayService resources without
requiring a complete declaration of their current state.

Deleting other resource types is not supported via the `gwa` CLI. 
Use the API Services Portal to delete Products, ProductEnvironments, and CredentialIssuers.

## Next steps

If you would like to dive deeper or start implementing a Gateway Configuration,
check out the following resources:

How-to guides

- [Create a Gateway Service](/how-to/create-gateway-service.md)

Linked concepts

- [Services](/concepts/services.md)
- [Plugins](/concepts/plugins.md)

External resources

- [Kong: Declarative configuration format](https://docs.konghq.com/gateway/latest/production/deployment-topologies/db-less-and-declarative-config/#declarative-configuration-format)
