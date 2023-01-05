# Waiting Queue

This uses the cloned plugin: `jwt-keycloak_1010`.

It is to support Waiting Queue solutions, such as https://github.com/bcgov/WaitingQueue

## Example

```yaml
services:
  - name: MY_REST_API
    tags: [_NS_]
    plugins:
      - name: jwt-keycloak_1010
        tags: [_NS_]
        enabled: true
        config:
          allowed_iss:
            - https://auth.service.issuer
          allowed_aud: an-audience-ref
          access_token_header: AUTH-WAITING-QUEUE
          realm: waitingqueue
          disable_access_token_header: true
          #algorithm: RS256
          #run_on_preflight: true
          #iss_key_grace_period: 10
          #maximum_expiration: 0
          #claims_to_verify:
          #- exp
          #well_known_template: %s/.well-known/openid-configuration
          #cookie_names: []
          #uri_param_names: []
          #scope: null
          #roles: null
          #client_roles: null
          #anonymous: null
          #realm_roles: null
          #consumer_match: false
```

## Key Fields

| Field                       | Type     | Default | Description                                                                                                                                         |
| --------------------------- | -------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| allowed_iss                 | string[] | nil     | A list of allowed issuers for this route/service/api. Can be specified as a `string` or as a [Pattern](http://lua-users.org/wiki/PatternsTutorial). |
| allowed_aud                 | string   | nil     | Allowed audience for this route/service/api. Can be specified as a `string` or as a [Pattern](http://lua-users.org/wiki/PatternsTutorial).          |
| access_token_header         | string   | nil     | An alternate header to use instead of "Authorization"                                                                                               |
| realm                       | string   | nil     | In the event of a 401, this value gets populated in the "WWW-Authenticate" response header as `Bearer realm="<realm>"`                              |
| disable_access_token_header | boolean  | false   | If set to 'true', the access token will not be sent to the upstream service                                                                         |

## Waiting Queue + User Credentials

```yaml
plugins:
  - name: jwt-keycloak_1010
    tags: [ns.NS]
    enabled: true
    config:
      allowed_iss:
        - https://waitingqueue.issuer/auth
      allowed_aud: ap-reg-auth-profile-test
      access_token_header: AUTH-WAITING-QUEUE
      realm: waitingqueue
  - name: jwt-keycloak
    tags: [ns.NS]
    enabled: true
    config:
      allowed_iss:
        - https://test.loginproxy.gov.bc.ca/auth/realms/apigw
      realm: apigw
      consumer_match: true
      consumer_match_claim: azp
      consumer_match_claim_custom_id: true
      consumer_match_ignore_not_found: false
```

If the Waiting Queue token is invalid, then the response will be:

```
HTTP/1.1 401 Unauthorized
WWW-Authenticate: Bearer realm="waitingqueue"
```

If the User's token is invalid, then the response will be:

```
HTTP/1.1 401 Unauthorized
WWW-Authenticate: Bearer realm="apigw"
```

The Waiting Queue plugin (`jwt-keycloak_1010`) will be evaluated first.
