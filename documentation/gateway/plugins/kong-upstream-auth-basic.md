# Kong Upstream Auth Basic

Reference: https://docs.konghq.com/hub/revolution_systems/upstream-auth-basic/

## Example

```
services:
- name: MY_REST_API
  tags: [ _NS_ ]
  plugins:
    - enabled: true
      name: upstream-auth-basic
      tags: [ _NS_ ]
      config:
        username: user
        password: password
```
