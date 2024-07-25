# Key Auth

Reference: <https://docs.konghq.com/hub/kong-inc/key-auth/>

## Example

```yaml
services:
- name: MY_REST_API
  tags: [ ns.<gatewayId> ]
  plugins:
  - name: key-auth
    tags: [ ns.<gatewayId> ]
    config:
      key_names:
      - X-API-KEY
```
