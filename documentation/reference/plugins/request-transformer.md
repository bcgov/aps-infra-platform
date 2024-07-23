# Request Transformer

Reference: https://docs.konghq.com/hub/kong-inc/request-transformer/

## Example:

```
services:
- name: MY_REST_API
  tags: [ ns.<gatewayId> ]
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
    tags: [ ns.<gatewayId> ]
```
