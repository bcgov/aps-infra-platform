# Kong Upstream Auth Basic

Reference: https://docs.konghq.com/hub/revolution_systems/upstream-auth-basic/

## Example

```
services:
- name: MY_REST_API
  tags: [ ns.<gatewayId> ]
  plugins:
    - enabled: true
      name: upstream-auth-basic
      tags: [ ns.<gatewayId> ]
      config:
        username: user
        password: password
```
