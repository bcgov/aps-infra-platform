# OIDC Consumer

**Description:** This plugin is used in conjunction with the `oidc` plugin to map the JWT Token to a Kong Consumer.

## Example

```
services:
- name: MY_REST_API
  tags: [ ns.<gatewayId> ]
  plugins:
  - name: oidc-consumer
    enabled: true
    tags: [ ns.<gatewayId> ]
    config:
      username_field: preferred_username
      create_consumer: false
```
