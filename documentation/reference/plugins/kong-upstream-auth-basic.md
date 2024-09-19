# Kong Upstream Auth Basic

## Configuration reference

Reference: <https://docs.konghq.com/hub/revolution_systems/upstream-auth-basic/>

## Common usage example

```yaml
plugins:
  - enabled: true
    name: upstream-auth-basic
    service: <SERVICE_NAME>
    tags: [ ns.<gatewayId> ]
    config:
      username: user
      password: password
```

Replace <SERVICE_NAME> with the name of the service that this plugin
configuration will target.
