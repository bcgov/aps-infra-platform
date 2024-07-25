---
title: Create a Gateway Service
---

<!-- overview -->

In Kong, the API gateway which underlies the API Services Portal, a
{{ glossary_tooltip term_id="gateway-service" }} is an entity representing an
external upstream API or microservice. Service configuration allows Kong to
manage, route, and handle requests to upstream services.

Service configuration is stored in a Gateway Service object in the API Services
Portal. Gateway Services can be crafted from a template or generated from an
OpenAPI specification, both of which are explained below.

Once you have created a Gateway Service, its functionality can be extended with
our [Supported Plugins](/reference/plugins/AVAILABLE-PLUGINS.md). They are
essentially modular components that can be added to Kong to add new features or
alter the behavior of existing features.

<!-- ## Declarative Configuration -->
<!-- this could be a good place to add in a general introduction to declarative 
syntax -->

!!! warning "Upstream service setup"
    If your upstream services run on Platform
    Service's Silver or Gold OpenShift cluster, you will need to
    configure the network polices to allow access from the API Gateway.
    See the [Upstream service setup](/how-to/upstream-services.md) guide for
    more information.

## Before you begin

- [Install gwa CLI](/how-to/gwa-install.md)
- [Create a Gateway](/reference/gwa-commands.md#gatewaycreate)

## Define service configuration

### Using a template

There are currently two Gateway configuration templates supported by the `gwa`
command line interface (CLI).

They are:

- `kong-httpbin`, which creates a basic, unprotected service, and
- `client-credentials-shared-idp`, which creates a service protected with
  [Client Credential Protection](/how-to/client-cred-flow.md), as well as a
  CredentialIssuer, DraftDataset, and Product.

To use one of these templates, follow these steps:

1. Generate Configuration File:

  Run the following command, substituting a unique service subdomain for your
  API which will be part of your vanity URL: `<MYSERVICE>.api.gov.bc.ca`

  === "kong-httpbin"

      ```shell linenums="0"
      gwa generate-config \
        --template kong-httpbin \
        --service <MYSERVICE> \
        --upstream https://httpbin.org
      ```

  === "client-credentials-shared-idp"

      ```shell linenums="0"
      gwa generate-config \
        --template client-credentials-shared-idp \
        --service <MYSERVICE> \
        --upstream https://httpbin.org
      ```

1. Publish to the API Services Portal:

  === "kong-httpbin"

      ```shell linenums="0"
      gwa pg gw-config.yml
      ```
  === "client-credentials-shared-idp"

      ```shell linenums="0"
      gwa apply -i gw-config.yml
      ```

### Using an OpenAPI spec

Kong's `deck` command line tool is used to convert an OpenAPI specification to a
Kong configuration.

Reference: <https://docs.konghq.com/deck/latest/>

Follow the installation instructions here: <https://docs.konghq.com/deck/latest/installation/>

Below is an example of a simple OpenAPI spec that you will use to generate a
Kong configuration file.

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

1. Add the following Kong specific metadata to the end of your OpenAPI spec,
substituting a unique service subdomain for your API which will be part of your
vanity URL: `<MYSERVICE>.api.gov.bc.ca`

  ```yaml
  x-kong-name: <MYSERVICE>

  x-kong-route-defaults:
    hosts:
      - <MYSERVICE>.api.gov.bc.ca
  ```

2. Save to `openapi.yaml`.

3. Generate Kong configuration

    Run the following command, substituting your API Services Portal Gateway in
    the `--select-tag` option:

    ```shell linenums="0"
    deck file openapi2kong -s openapi.yaml -o gw.yaml --select-tag ns.<gatewayId>
    ```

  !!! warning "Kong 2.x Incompatibility"
      Due to an incompatibility between `openapi2kong` and Kong 2 (used by the
      API Services Portal), you will need to remove the '~' at the beginning of
      paths. This can be done by manually editing the gw.yaml file, or by
      running `yq -i eval '(.services[].routes[].paths[]) |= sub("~"; "")' gw.yaml`.
      (You may need to install `yq` [here](https://github.com/mikefarah/yq/#install)).

  !!! note "Gateway tags"
      A Gateway `tag` with the format `ns.<gatewayId>` is mandatory for each
      service, route, and plugin object. If you have separate pipelines for your
      environments (`dev`, `test` and `prod`), you can split your configuration and
      update the `tags` with the qualifier. For example, you can use a tag
      `ns.<gatewayId>.dev` to sync the Kong configuration for `dev` Service and
      Routes only.

4. Publish to the API Services Portal:

  ```shell linenums="0"
  gwa pg gw.yaml
  ```

!!! note "OpenAPI spec maintenance"
    You can opt to either maintain your OpenAPI spec and execute the steps above
    when necessary, or convert your OpenAPI spec once and maintain the generated
    Kong configuration.

## Verify routes

To verify that the Gateway can access the upstream services, run the command
`gwa status`.

In the APS `test` environment, the hosts that you defined in the routes are
altered. To see the actual hosts:

1. Log into the [API Services Portal](https://api-gov-bc-ca.test.api.gov.bc.ca/).

2. Go to the **Gateways** tab and select your **Gateway** from the list.

3. Go to **Gateway Services** and expand the accordion of your particular
   service on the right to get the routing details.

You can also use `curl` to verify your endpoint, and `ab` for load testing:

```bash
curl https://<MYSERVICE>-api-gov-bc-ca.test.api.gov.bc.ca/headers

ab -n 20 -c 2 https://<MYSERVICE>-api-gov-bc-ca.test.api.gov.bc.ca/headers

```

## Next steps

- [Add Client Credential Protection](/how-to/client-cred-flow.md)
- [Configure a Private Route](/how-to/private-route.md)
- [Configure Gateway Controls](/how-to/COMMON-CONFIG.md)
- [Share your API](/how-to/api-discovery.md)
- [Monitor your Services](/how-to/monitoring.md)
