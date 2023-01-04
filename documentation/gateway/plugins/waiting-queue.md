# Waiting Queue

This uses the cloned plugin: `jwt-keycloak_1010`.

## Example

```
services:
- name: MY_REST_API
  tags: [ _NS_ ]
  plugins:
  - name: jwt-keycloak_1010
    tags: [ _NS_ ]
    enabled: true
    config:
      algorithm: RS256
      well_known_template: https://keycloak/auth/realms/REALM/.well-known/openid-configuration
      allowed_iss:
      - https://keycloak/auth/realms/REALM
      allowed_aud: an-audience-ref
      bearer_header: AUTH-WAITING-QUEUE
      run_on_preflight: true
      iss_key_grace_period: 60
      maximum_expiration: 0
      claims_to_verify:
      - exp
      cookie_names: []
      uri_param_names: []
      scope: null
      roles: null
      client_roles: null
      anonymous: null
      realm_roles: null
      consumer_match: false

```
