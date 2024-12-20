# JWT Keycloak

## Configuration reference

This is a custom plugin managed by the API Program Services team.

Here is a list of the parameters which can be used in this plugin's `config` section:

| Field                       | Type     | Default | Description                                                                                                                                         |
| --------------------------- | -------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| allowed_iss                 | string[] | nil     | A list of allowed issuers for this route/service/api. Can be specified as a `string` or as a Lua pattern. |
| allowed_aud                 | string   | nil     | Allowed audience for this route/service/api. This must match the `Client ID` shown on the **Client Management** tab for the Authorization Profile. Can be specified as a `string` or as a Lua pattern. | 
| access_token_header         | string   | nil     | An alternate header to use instead of "Authorization"                                                                                               |
| realm                       | string   | nil     | In the event of a 401, this value gets populated in the "WWW-Authenticate" response header as `Bearer realm="<realm>"`                              |
| disable_access_token_header | boolean  | false   | If set to 'true', the access token will not be sent to the upstream service                                                                         |
| client_roles | string[] | nil | List of Client/Roles in the format `<CLIENT_ID>:<ROLE_NAME>` where there has to be at least one match. |

## Common usage example

To validate access tokens issued by Keycloak, add this section to your
GatewayService configuration file:

```yaml
plugins:
  - name: jwt-keycloak
    service: <SERVICE_NAME>
    tags: [ ns.<gatewayId> ]
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

Replace <SERVICE_NAME> with the name of the service that this plugin
configuration will target.

### Multiple Issuers

When you have an API that is consumed by your own frontend and potentially by
some internal processes, and you would also like to give limited access to the
API to external parties, such as other Ministry services, then you can use the
API Gateway to protect the API. Roles are used to define different levels of access to the API.

An example configuration that uses RBAC and verification of User Tokens using
the SSO Standard Realm and Service Account Tokens using APS's Shared IdP:

```yaml
services:
  - name: MY_REST_API
    tags: [ ns.<gatewayId> ]
    routes:
      - name: MY_REST_API_READS
        hosts: [myrestapi.api.gov.bc.ca]
        methods: [GET, OPTIONS]
        paths: [/]
        plugins:
          - name: jwt-keycloak
            tags: [ ns.<gatewayId> ]
            enabled: true
            config:
              allowed_iss:
                - https://loginproxy.gov.bc.ca/auth/realms/standard
                - https://loginproxy.gov.bc.ca/auth/realms/apigw
              allowed_aud: an-audience-ref
              client_roles: [an-audience-ref:Read]
              consumer_match: true

      - name: MY_REST_API_ADMINS
        hosts: [myrestapi.api.gov.bc.ca]
        methods: [GET, OPTIONS, PUT, DELETE, POST, PATCH]
        paths: [/]
        plugins:
          - name: jwt-keycloak
            tags: [ ns.<gatewayId> ]
            enabled: true
            config:
              allowed_iss:
                - https://loginproxy.gov.bc.ca/auth/realms/standard
                - https://loginproxy.gov.bc.ca/auth/realms/apigw
              allowed_aud: an-audience-ref
              client_roles: [an-audience-ref:Admin]
              consumer_match: true
```
