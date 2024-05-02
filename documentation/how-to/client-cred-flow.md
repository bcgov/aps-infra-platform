---
title: Client Credential Protection
---

This page shows how to protect and call an API using the OAuth2 Client Credential flow.

Here is overview of the process (numbers reference steps in the table of contents):

![Client Credential flow](/artifacts/oauth2.png "Client Credential flow")

## Before you begin

- [Install gwa CLI](/how-to/gwa-install.md)
- [Create a Namespace](/resources/gwa-commands.md#namespacecreate)
- [Create a GatewayService](/how-to/create-gateway-service.md)
- [Share an API in the API Directory](/how-to/api-discovery.md)
- [Create a service account](/how-to/generate-service-account.md) (optional)

## 1. Configure a service on the gateway

Firstly, complete the steps listed above in **Before you begin**. This includes
setting up an unprotected GatewayService pointing to your service.

## 2. Grant access to the identity provider

This step varies depending on your identity provider (IdP).
If you're unsure which path to follow, use the shared IdP pattern.

??? "Shared IdP"

    The shared IdP pattern leverages Pathfinder SSO (running Keycloak on
    the Gold cluster) as an identity provider for managing Client Credentials.
    The API Services Portal administers a custom realm on Pathfinder SSO called `apigw`,
    so you never need to directly interact with the identity provider.

    Token Issuers:

    - https://dev.loginproxy.gov.bc.ca/auth/realms/apigw
    - https://test.loginproxy.gov.bc.ca/auth/realms/apigw
    - https://loginproxy.gov.bc.ca/auth/realms/apigw

    To use the shared IdP, perform the following steps:

    #### a) Setup the Authorization Profile

    A credential with `CredentialIssuer.Admin` is required to update Authorization Profiles (`CredentialIssuer`).

    Authorization Profiles can be setup either via the Portal or by using a Service Account with the Portal Directory API.

    Update the below `CredentialIssuer` with the `name` and `description` that makes sense to you, and include the desired Roles setup for authorization.

    ```yaml
    kind: CredentialIssuer
    name: Resource Server Example
    namespace: <GW-NAMESPACE>
    description: <Authorization Profile description>
    flow: client-credentials
    mode: auto
    authPlugin: jwt-keycloak
    clientAuthenticator: client-secret
    clientRoles: []
    inheritFrom: Gold Shared IdP
    ```

    #### b) Link the Authorization Profile to the Product

    Before making the API available on the Directory, the API should be configured with a plugin for protecting access. To do this, an API Provider can edit the Product details to select `Oauth2 Client Credential Flow` and the newly created Authorization Profile.

    #### c) Update your Gateway Configuration with the Plugin

    Update your Gateway Configuration to include the `jwt-keycloak` plugin.

    !!! note
        When you configure the Product Environment, a `Plugin Template` will be displayed - this can be a starting point for protecting your API on the Gateway.

    Finally, from the Portal, `enable` the Environment to make it available on the API Directory.

    #### d) Optional Configuration

    ##### Roles

    If you have Roles that you want to have controlled by the Portal, add them to the Client's `Roles`.

    Update the `CredentialIssuer` record above with the `clientRoles` you want to manage.

??? "Custom IdP"

    Before the Portal can be configured, a new set of credentials must be created on the IdP. For this tutorial, we will include the steps when Keycloak is the IdP.

    #### a) Create a new Client on the IdP

    Create a new client with Access Type `confidential`. All flows except `Service Accounts` should be turned off.

    Make a note of the `Client ID` and `Client Secret` , they will be used when the Portal `Authorization Profile` is created.

    The `Full Scope Allowed` can be turned off and the `realm-management` client roles for `manage-clients` and `manage-users` should be added.

    Add the `manage-clients` and `manage-users` client roles to the `Service Account Roles`.

    #### b) Setup the Authorization Profile

    A credential with `CredentialIssuer.Admin` is required to update Authorization Profiles (`CredentialIssuer`).

    Authorization Profiles can be setup either via the Portal or by using a Service Account with the Portal Directory API.

    Update the below `CredentialIssuer` to include the environment details and the Scopes and Roles setup for authorization.

    ```yaml
    kind: CredentialIssuer
    name: Resource Server Example
    namespace: <GW-NAMESPACE>
    description: <Authorization Profile description>
    flow: client-credentials
    mode: auto
    authPlugin: jwt-keycloak
    clientAuthenticator: client-secret
    clientRoles: []
    clientMappers:
      - name: audience
        defaultValue: ""
    availableScopes: [Function1/read, Function2/*, Function3/write, Function3/read]
    owner: <your-username>
    environmentDetails:
      - environment: prod
        issuerUrl: <https://auth-issuer>
        clientId: <testapp-client>
        clientRegistration: managed
        clientSecret: ""
    ```

    #### c) Link the Authorization Profile to the Product

    Before making the API available on the Directory, the API should be configured with a plugin for protecting access. To do this, an API Provider can edit the Product details to select `Oauth2 Client Credential Flow` and the newly created Authorization Profile.

    #### d) Update your GatewayService with the Plugin

    Update your GatewayService configuration to include the `jwt-keycloak` plugin.

    !!! note
        When you configure the Product Environment, a `Plugin Template` will be displayed - this can be a starting point for protecting your API on the Gateway.

    Finally, from the Portal, `enable` the Environment to make it available on the API Directory.

    #### e) Optional configuration

    ##### Scopes

    If you have Client Scopes that you want to have controlled by the Portal, add them to the Realm's `Client Scopes` and `Default Client Scopes` on the IdP.

    Update the `CredentialIssuer` record above to match the `availableScopes` with the ones added on the IdP.

    ##### Roles

    If you have Roles that you want to have controlled by the Portal, add them to the Client's `Roles`.

    Update the `CredentialIssuer` record above to match the `clientRoles` with the ones added on the IdP.

    ##### Client mappers

    The `audience` is an optional mapper that can be added to a Client.

    The IdP needs to have a policy that allows Audience to be added as a Protocol Mapper to the client.

    In Keycloak, this is updated under the Realm's `Client Registration` -> `Client Registration Policies`.

    Edit the Authenticated Access Policies -> Allowed Protocol Mapper Types to include the `oidc-audience-mapper`.

    ##### UMA2 Authorization Resources

    If you want to use the Authorization services, then set `Authorization Enabled` to `ON` for the Client on the IdP. You will also want to set the `Decision Strategy` to `Affirmative`.

    Update the following `CredentialIssuer` attributes:

    ```
      resourceType: ""
      resourceAccessScope: ""
      resourceScopes: []
    ```

    - `resourceType`: The Resource Type of the resources that will be managed (required)
    - `resourceScopes`: A list of the Authorization Scopes managed for the particular Resources (required)
    - `resourceAccessScope`: Used in the case where the Resource Server owns all the resources, a user must have the `resourceAccessScope` assigned in order to be allowed to manage the access. If it is not set, then the user has to be the resource owner in order to manage access.

    > `resourceAccessScope` - The API Services Portal has not completed the implementation for the scenario where the User is the Resource Owner (`resourceAccessScope` is left blank). It uses the `Token Exchange` capability but it's an optional service available on Keycloak and has numerous caveats around it. Please contact the APS team if interested to know more.

## 3. Request Access (API Consumer)

At this point the API is protected with a Client Credential grant. The next
steps show how to validate the flow.

The API consumer would request access to the API via the API Services Portal and
generate the credentials to be used below.

The Portal will use the credentials setup in the Authorization Profile, to
create a disabled Client on the IdP (with any applicable Client Mappers) and
return the credentials to the Requesting user.

## 4. Approve Access (API Provider)

An Access Manager reviews the access request, sets any additional controls,
grants the relevant permissions (such as scopes and roles), and approves. The
Portal will enable the Client and apply the permissions on the IdP.

The Portal sends a notification to the Requester letting them know that API
Access has been approved (or rejected).

## 5. Retrieve the Access Token (Client)

Using the Credentials generated in step 3, the Requester calls the Token
endpoint to get a new JWT token.

```sh
export CID="<Client ID>"
export CSC="<Client Secret>"
export URL="<Token Endpoint>"

RESPONSE=$(curl -X POST "$URL" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=$CID" \
  -d "client_secret=$CSC" \
  -d "grant_type=client_credentials" \
  -d "scopes=openid")

echo "$RESPONSE" | jq
export TOKEN=$(echo "$RESPONSE" | jq -r '.access_token')
```

## 6. Call the API (Client)

Call the API with the Bearer token:

```sh linenums="0"
curl -v -H "Authorization: Bearer $TOKEN" https://<MYSERVICE>.api.gov.bc.ca/
```

The API Gateway's `jwt-keycloak` plugin will use the IdP's public keys to
validate the token and depending on the plugin configuration, validate the
scopes or roles.

## 7. Gateway Proxying to Upstream

A technical, but important step in the integration is the Gateway proxying the
request to the Upstream Service API and deciding on the different options for
securing that interaction.

Options:

- `Network Policy` : If the Services are co-located on the same Cluster as the
  Gateway's Data Plane, then native network policies can be used to protect the
  channel between the Gateway and the Upstream Service. This approach is used
  for Services running on the OpenShift Silver cluster.

- `Kong Upstream JWT`: This plugin adds a signed JWT to the request headers so
  that the Upstream Service can verify that the request came specifically from
  the Gateway.

- `Client Certificates` : Client certificates (mTLS) provides a way for the
  Upstream Service to provide a secure channel from the Gateway and to verify
  that the request came specifically from the Gateway.

- `Firewall IP Restrictions` : This provides a low-level of protection by
  limiting the IPs to the ones of the Gateway Data Planes. Because the Data
  Planes are typically on shared infrastructure, this would still allow traffic
  from other tenants. This might be acceptable based on the type of data
  delivered by or to the Upstream Service.

## Variations

### Signed JWT

The Authorization Profile `clientAuthenticator` was set to `client-secret` in
this tutorial, but there is an alternate setup that can be used:

- `client-jwt-jwks-url` (Signed JWT with JWKS URL or Certificate)

In this scenario, when a Client is requesting access, they will be required to
enter details about the client assertion certificates. The details can either be
a public JWKS URL that holds the public key information for a key pair, or
providing just the public key information. The information will be used in step
5 when retrieving the Bearer Token. For further details, you can see the
specific examples [Signed JWT w/ Hosted JWKS](/how-to/intro-signed-jwt.md) or
[Signed JWT w/ Certificate](/how-to/intro-signed-jwt-pubkey.md).
