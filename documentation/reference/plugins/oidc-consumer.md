# OIDC Consumer

The `oidc-consumer` plugin is used in conjunction with the `oidc` plugin to
map the JWT Token to a Kong Consumer.

## Common usage example

```yaml
plugins:
- name: oidc-consumer
  enabled: true
  service: <SERVICE_NAME>
  config:
    username_field: preferred_username
    create_consumer: false
```

Replace <SERVICE_NAME> with the name of the service that this plugin
configuration will target.
