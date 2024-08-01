# Cross-origin Resource Sharing (CORS)

The `cors` plugin can be used in order to add cross-origin resource sharing
(CORS) to a service or route.

## Configuration reference

This is a stock plugin from Kong Hub. See the [configuration reference page](https://docs.konghq.com/hub/kong-inc/cors/configuration)
for a list of parameters and protocol compatibility notes.

## Common usage example

To add CORS to a service or route, add this section to your GatewayService
configuration file:

```yaml
plugins:
- name: cors
  service: <SERVICE_NAME>
  tags: [ ns.<gatewayId> ]
  config:
    origins: ["*"]
    methods: [GET, POST, PUT, PATCH, OPTIONS]
    headers:
      [
        Connection,
        Upgrade,
        Cache-Control,
        Access-Control-Allow-Headers,
        Keep-Alive,
      ]
    credentials: true
    max_age: 3600
```

Replace <SERVICE_NAME> with the name of the service that this plugin
configuration will target.

## Additional references

<https://github.com/Kong/kong/issues/4859>
