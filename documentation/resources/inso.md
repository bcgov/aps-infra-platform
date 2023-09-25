## Using an OpenAPI Spec

Generating Kong Gateway configuration from an OpenAPI spec.

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
      operationId: get-heaers
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

Add in some Kong specific metadata:

```yaml
x-kong-name: ajc-deck-services

x-kong-route-defaults:
  hosts:
    - a-service-for-ajc-deck.api.gov.bc.ca
```

Add other plugin information:

```yaml
security:
  - keyAuth: []

x-kong-plugin-acl:
  config:
    hide_groups_header: true
    allow: ["115BC13D"]

components:
  securitySchemes:
    keyAuth:
      type: apiKey
      name: apikey
      in: header
      x-kong-plugin-key-auth:
        config:
          key_names: ["X-API-KEY"]
          run_on_preflight: true
          hide_credentials: true
          key_in_body: false
```

Reference: https://docs.insomnia.rest/inso-cli/cli-command-reference/OAS-spec.yml

**Generate Kong Configuration:**

```shell
inso generate config -f json -o kong/gwconfig.json --tags ns.ajc-deck openapi.yaml
inso generate config -f yaml -o kong/gwconfig.yaml --tags ns.ajc-deck openapi.yaml
```

**Publish:**

```shell
curl -v -F dryRun='false' -F configFile=@kong/gwconfig.json \
  http://localhost:2000/v2/namespaces/ajc-deck/gateway \
  -H "Authorization: Bearer $TOK" -X PUT
```

**Interactive**

```shell

echo '
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>Elements in HTML</title>
    <!-- Embed elements Elements via Web Component -->
    <script src="https://unpkg.com/@stoplight/elements/web-components.min.js"></script>
    <link rel="stylesheet" href="https://unpkg.com/@stoplight/elements/styles.min.css">
  </head>
  <body>

    <elements-api
      apiDescriptionUrl="openapi.yaml"
      router="hash"
      layout="sidebar"
    />

  </body>
</html>
' > elements.html

npx serve
```

> NOTE: An open annoyance is that the "Live URL" that Elements display is based on the `Servers` - and the `openapi-to-kong` uses the `Servers` to derive the Service, which is the Upstream internal host.
