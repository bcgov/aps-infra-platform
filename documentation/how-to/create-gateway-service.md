---
title: Create a Service
---

<!-- overview -->

In Kong, the API gateway which underlies the API Management Platform, a service
is an entity representing an external upstream API or microservice. For example,
a data transformation microservice, a billing API, and so on.

The main attribute of a service is its URL. You can specify the URL with a
single string, or by specifying its protocol, host, port, and path individually.

Read more about services on the [Kong Gateway page](https://docs.konghq.com/gateway/latest/key-concepts/services/).

Service configuration is stored in a GatewayService object in the API Services
Portal. GatewayServices can be crafted from a template or generated from an
OpenAPI specification. This guide only contains information on the OpenAPI
route.

## Before you begin

- [Install gwa CLI](/how-to/gwa-install.md)
- [Create a Namespace](/how-to/gwa-commands.md#namespacecreate)

<!-- ## Declarative Configuration -->

!!! warning "Upstream service setup"
    If your upstream services run on Platform
    Service's Silver or Gold OpenShift cluster, then you will need to
    configuration the network polices to allow access from the API Gateway.
     [Upstream service setup](/how-to/upstream-services.md)

## Using an OpenAPI Spec

Kong's `deck` command line tool is used to convert an OpenAPI specification to a Kong configuration (which underlies )

Reference: https://docs.konghq.com/deck/latest/

Follow the installation instructions here: https://docs.konghq.com/deck/latest/installation/

Below is an example of a simple OpenAPI spec that we will use to generate a Kong configuration file.

```yaml
openapi: 3.0.1
info:
  version: "1.0-oas3"
  title: httpbin
  description: An unofficial OpenAPI definition for [httpbin.org](https://httpbin.org).
  license:
    name: blah license
    url: https://somelicense.com

servers:
  - url: https://httpbin.org

tags:
  - name: HTTP methods
    description: Operations for testing different HTTP methods

externalDocs:
  url: http://httpbin.org/legacy

security: []

paths:
  /headers:
    get:
      operationId: get-headers
      summary: Returns the request headers.
      responses:
        "4XX":
          description: Ooops something went wrong
        "200":
          description: OK
          content:
            application/json:
              schema:
                type: object
                properties:
                  headers:
                    type: object
                    additionalProperties:
                      type: string
                required:
                  - headers
```

Add the following Kong specific metadata to the end of your OpenAPI spec,
substituting a unique service subdomain for your API which will be part of your vanity URL: <MYSERVICE>.api.gov.bc.ca.

```yaml
x-kong-name: <MY-SERVICE>

x-kong-route-defaults:
  hosts:
    - <MY-SERVICE>.api.gov.bc.ca
```

Save to `openapi.yaml`.

**Generate Kong Configuration:**

Run the following command, substituting your API Services Portal Namespace in the `--select-tag` option:

```shell linenums="0"
deck file openapi2kong -s openapi.yaml -o gw.yaml --select-tag ns.<GW-NAMESPACE>
```

!!! note "Namespace tags"
    A namespace `tag` with the format `ns.<NAMESPACE>` is mandatory for each
    service, route, and plugin object.
    
    If you have separate pipelines for your environments (dev, test and prod),
    you can split your configuration and update the `tags` with the qualifier. 
    
    For example, you can use a tag `ns.<NAMESPACE>.dev` to sync the Kong configuration
    for `dev` Service and Routes only.

**Publish to the API Services Portal:**

```shell linenums="0"
gwa publish-gateway gw.yaml
```

## Next steps

- [Add Client Credential Protection](/how-to/client-cred-flow.md)
- [Configure a Private Route](/how-to/private-route.md)
- [Configure Gateway Controls](/how-to/COMMON-CONFIG.md)
- [Share your API](/how-to/api-discovery.md)
- [Monitor your Services](/how-to/monitoring.md)
