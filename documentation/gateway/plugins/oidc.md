# OIDC

## Example

```
services:
- name: MY_REST_API
  tags: [ _NS_ ]
  plugins:
    - enabled: true
      name: oidc
      tags: [  _NS_ ]
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
