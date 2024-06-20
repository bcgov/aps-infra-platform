---
title: Protect an Application
---

This guide walks through the steps to protect your Application using Keycloak SSO and the APS Kong Gateway.

![alt text](/artifacts/keycloak-rbac.png "Keycloak RBAC")

## 1. Configure a confidential client

Go to the Common Hosted SSO (CSS) site (https://bcgov.github.io/sso-requests) and request a new confidential client.

After the client has been provisioned, you can go to the Role Management tab to configure the Roles you want to use to protect resources in your Application.

The `Assign Users to Roles` can be used to administer User permissions.

## 2. Configure the APS Kong Gateway

**Pre-requisites:**

- You have your application deployed in the OpenShift Silver cluster
- You have created a namespace in the `API Services Portal`
- You have a Service Account created with the `GatewayConfig.Publish` permission
- Your Network Policy has been configured to allow traffic from the APS project space
- You have completed your minimal service/route configuration and published it to the APS Kong Gateway

To protect your application, there are two plugins that need to be configured: `oidc` and `acl`.

**oidc**

> Update `discovery` if you are using SSO other than `dev` or if using a non-standard realm

> The `groups_claim` must be `client_roles` as that is what the SSO service uses for the roles that the user has assigned to it.

```
    plugins:
      - enabled: true
        name: oidc
        tags: [ ns.$NS ]
        config:
          access_token_as_bearer: "no"
          access_token_header_name: Authorization
          bearer_jwt_auth_allowed_auds:
            - YOUR_CLIENT_ID
          bearer_jwt_auth_enable: "no"
          bearer_jwt_auth_signing_algs:
            - RS256
          bearer_only: "no"
          client_id: YOUR_CLIENT_ID
          client_secret: YOUR_CLIENT_SECRET
          disable_access_token_header: "yes"
          disable_id_token_header: "yes"
          disable_userinfo_header: "yes"
          discovery: https://dev.loginproxy.gov.bc.ca/auth/realms/standard/.well-known/openid-configuration
          filters: null
          groups_claim: client_roles
          header_claims: []
          header_names: []
          id_token_header_name: X-ID-Token
          ignore_auth_filters: ""
          introspection_cache_ignore: "no"
          introspection_endpoint: null
          introspection_endpoint_auth_method: null
          logout_path: /logout
          realm: kong
          recovery_page_path: null
          redirect_after_logout_uri: /
          redirect_uri: null
          response_type: code
          revoke_tokens_on_logout: "yes"
          scope: openid
          session_secret: null
          skip_already_auth_requests: "no"
          ssl_verify: "no"
          timeout: null
          token_endpoint_auth_method: client_secret_post
          unauth_action: auth
          use_jwks: "yes"
          userinfo_header_name: X-USERINFO
          validate_scope: "yes"
```

> If your upstream service needs specific attributes, the `header_claims` and `header_names` config can be used to pass claims as request headers to the upstream service. A subset of the claims available:

```
  "idir_user_guid": "220469E030000000000000000A607C5",
  "identity_provider": "idir",
  "idir_username": "FLAST",
  "email_verified": false,
  "name": "First Last",
  "preferred_username": "220469e030000000000000a607c5@idir",
  "display_name": "XT:Last, First CITZ:IN",
  "given_name": "Last",
  "family_name": "First",
  "email": "last.first@email"
```

An example to get `idir_username` and `email` passed, would be:

```
  header_claims: [ idir_username, email ]
  header_names: [ X-Idir-Username, X-User-Email ]
```

**acl**

The `acl` plugin will enforce that the user's `client_roles` includes the roles defined in the `allow` list.

```
    plugins:
      - enabled: true
        name: acl
        tags: [ ns.$NS ]
        config:
          allow:
            - ROLE_FOR_ACCESS
          deny: null
          hide_groups_header: false
```

> If `hide_groups_headers` is `false` then `X-Authenticated-Groups` will be a request header with a comma-delimited list of roles that the user belongs to.

**request-transformer (optional)**

If your upstream service is stateless, then you can remove the cookie before the request is forwarded to it.

```
      - name: request-transformer
        protocols: [http]
        tags: [ ns.$NS ]
        config:
          remove:
            headers:
              - Cookie
```

## Outcome

- Vanity url: `my-application.apps.gov.bc.ca`
- Protected by SSL `*.apps.gov.bc.ca` certificate
- Separation of concerns for authentication and authorization
