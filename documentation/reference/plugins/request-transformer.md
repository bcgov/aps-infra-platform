# Request Transformer

The `request-transformer` plugin allows simple transformation of requests before
they reach the upstream server.

## Configuration reference

This is a stock plugin from Kong Hub. See the [configuration reference page](https://docs.konghq.com/hub/kong-inc/request-transformer/configuration)
for a list of parameters and protocol compatibility notes.

## Common usage example

```yaml
plugins:
- config:
    add:
      body: {}
      headers: {}
      querystring: {}
    append:
      body: {}
      headers: {}
      querystring: {}
    remove:
      body: {}
      headers:
      - Cookie
      querystring: {}
    rename:
      body: {}
      headers: {}
      querystring: {}
    replace:
      body: {}
      headers: {}
      querystring: {}
  enabled: true
  name: request-transformer
  protocols:
  - https
  - http
  service: <SERVICE_NAME>
```

Replace <SERVICE_NAME> with the name of the service that this plugin
configuration will target.
