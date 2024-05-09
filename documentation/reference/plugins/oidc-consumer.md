# OIDC Consumer

**Description:** This plugin is used in conjunction with the `oidc` plugin to map the JWT Token to a Kong Consumer.

## Example

```
services:
- name: MY_REST_API
  tags: [ _NS_ ]
  plugins:
  - name: oidc-consumer
    enabled: true
    tags: [ _NS_ ]
    config:
      username_field: preferred_username
      create_consumer: false
```
