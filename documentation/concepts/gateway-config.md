---
title: Gateway Configuration
---

This article explains the basics of a Gateway Configuration. It is an essential part of setting up your API in the API Management Platform.

## Background

Kong is an open-source API gateway and microservices management layer which powers the API Management Platform. 
A Kong gateway configuration is a {{ glossary_tooltip term_id="yaml-file" text="YAML file" }} used to define the configuration settings for Kong, such as routes, services, and plugins, using declarative syntax.

## Use case

In a Gateway Configuration file, you can specify details like:

1. [Services](/concepts/services.md): These represent the backend services that Kong will proxy requests to.

2. Routes: Routes define rules for matching incoming requests to services.

3. [Plugins](/concepts/plugins.md): Plugins are used to add functionalities like authentication, rate limiting, logging, etc., to your API endpoints.


Here's an example of what a simple Gateway Configuration might look like:

```yaml
kind: GatewayService
name: example-service-dev
tags: [ns.example-namespace]
host: httpbin.org
port: 443
protocol: https
retries: 0
routes:
  - name: example-service-route
    tags: [ns.example-namespace]
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
    tags: [ns.example-namespace]
    enabled: true
    config:
      http_method: null
```

This configuration defines a service `example-service-dev` with a corresponding route `example-service-route` and applies a request-transformer plugin to it.

## Next steps

If you would like to dive deeper or start implementing a Gateway Configuration, check out the
following resources:

How-to guides

- [Create a Service](/how-to/create-gateway-service.md)

Linked concepts

- [Services](/concepts/services.md)
- [Plugins](/concepts/plugins.md)

