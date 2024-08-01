# Key Auth

The `key-auth` plugin adds API key authentication to a service or route.

## Configuration reference

This is a stock plugin from Kong Hub. See the [configuration reference page](https://docs.konghq.com/hub/kong-inc/key-auth/)
for a list of parameters and protocol compatibility notes.

## Common usage example

The `key-auth` plugin can be used in order to add API key authentication.
Consumers can then add their API key to authenticate their requests.

To enable API key authentication, add this section to your GatewayService
configuration file:

```yaml
plugins:
- name: key-auth
  service: <SERVICE_NAME>
  tags: [ ns.<gatewayId> ]
  config:
    key_names:
    - X-API-KEY
```

Replace <SERVICE_NAME> with the name of the service that this plugin
configuration will target.
