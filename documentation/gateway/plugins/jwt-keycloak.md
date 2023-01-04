# JWT Keycloak

## Example

```yaml
services:
  - name: MY_REST_API
    tags: [_NS_]
    plugins:
      - name: jwt-keycloak
        tags: [_NS_]
        enabled: true
        config:
          allowed_iss:
            - https://keycloak/auth/realms/REALM
          allowed_aud: an-audience-ref
          #access_token_header: Authorization
          #realm: kong
          #disable_access_token_header: false
          #run_on_preflight: true
          #iss_key_grace_period: 10
          #maximum_expiration: 0
          #claims_to_verify:
          #- exp
          #algorithm: RS256
          #well_known_template: %s/.well-known/openid-configuration
          #cookie_names: []
          #scope: null
          #realm_roles: null
          uri_param_names: []
          client_roles: null
          anonymous: null
          consumer_match: true
          #consumer_match_claim: azp
          #consumer_match_ignore_not_found: false
          #consumer_match_claim_custom_id: false
```

## Key Fields

| Field                       | Type     | Default | Description                                                                                                                                         |
| --------------------------- | -------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| allowed_iss                 | string[] | nil     | A list of allowed issuers for this route/service/api. Can be specified as a `string` or as a [Pattern](http://lua-users.org/wiki/PatternsTutorial). |
| allowed_aud                 | string   | nil     | Allowed audience for this route/service/api. Can be specified as a `string` or as a [Pattern](http://lua-users.org/wiki/PatternsTutorial).          |
| access_token_header         | string   | nil     | An alternate header to use instead of "Authorization"                                                                                               |
| realm                       | string   | nil     | In the event of a 401, this value gets populated in the "WWW-Authenticate" response header as `Bearer realm="<realm>"`                              |
| disable_access_token_header | boolean  | false   | If set to 'true', the access token will not be sent to the upstream service                                                                         |
