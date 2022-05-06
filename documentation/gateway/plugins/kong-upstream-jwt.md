# Kong Upstream JWT

Reference: https://docs.konghq.com/hub/optum/kong-upstream-jwt

## Example

```
services:
- name: MY_REST_API
  tags: [ _NS_ ]
  plugins:
    - enabled: true
      name: kong-upstream-jwt
      tags: [ _NS_ ]
      config:
        header: GW-JWT
        include_credential_type: false
        issuer: null
        key_id: null
        private_key_location: /etc/secrets/kongh-cluster-ca/kong-upstream-jwt.key
        public_key_location: /etc/secrets/kongh-cluster-ca/kong-upstream-jwt.pem
```
