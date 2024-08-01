# OIDC

The OpenID Connect `oidc` plugin allows for integration with a third party
identity provider in a standardized way.

!!! note
  The `oidc` plugin is only used with endpoints ending with
  `.apps.gov.bc.ca`, please reach out to the APS team on Rocket.Chat `#aps-ops`
  to get this permission added to your namespace.

## Configuration reference

This is a stock plugin from Kong Hub. See the [configuration reference page](https://docs.konghq.com/hub/kong-inc/openid-connect/configuration/)
for a list of parameters and protocol compatibility notes.

## Common usage example

To enable OpenID Connect provider support, add this section to your
GatewayService configuration file:

```yaml
plugins:
  - enabled: true
    name: oidc
    service: <SERVICE_NAME>
    tags: [ ns.<gatewayId> ]
    config:
      access_token_as_bearer: "no"
      access_token_header_name: X-Access-Token
      bearer_jwt_auth_allowed_auds:
        - aud1
      bearer_jwt_auth_enable: "no"
      bearer_jwt_auth_signing_algs:
        - RS256
      bearer_only: "no"
      client_id: <CLIENT_ID>
      client_secret: <CLIENT_SECRET>
      disable_access_token_header: "no"
      disable_id_token_header: "no"
      disable_userinfo_header: "no"
      discovery: https://keycloak/auth/realms/REALM/.well-known/openid-configuration
      filters: null
      groups_claim: groups
      header_claims: []
      header_names: []
      id_token_header_name: X-ID-Token
      ignore_auth_filters: ""
      introspection_cache_ignore: "no"
      introspection_endpoint: https://keycloak/auth/realms/REALM/protocol/openid-connect/token/introspect
      introspection_endpoint_auth_method: null
      logout_path: /logout
      realm: kong
      recovery_page_path: null
      redirect_after_logout_uri: /headers
      redirect_uri: null
      response_type: code
      revoke_tokens_on_logout: "no"
      scope: openid
      session_secret: null
      skip_already_auth_requests: "no"
      ssl_verify: "no"
      timeout: null
      token_endpoint_auth_method: client_secret_post
      unauth_action: auth
      use_jwks: "yes"
      userinfo_header_name: X-USERINFO
      validate_scope: "no"
```

Replace <SERVICE_NAME> with the name of the service that this plugin
configuration will target.
