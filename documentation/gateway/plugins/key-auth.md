# Key Auth

Reference: https://docs.konghq.com/hub/kong-inc/key-auth/

## Example

```
services:
- name: MY_REST_API
  tags: [ _NS_ ]
  plugins:
  - name: key-auth
    tags: [ _NS_ ]
    config:
      key_names:
      - X-API-KEY
```
