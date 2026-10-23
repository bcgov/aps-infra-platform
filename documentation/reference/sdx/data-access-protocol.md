---
title: "SDX Data Access Protocol"
---

The exchange of data between two organization _Information Systems_ (IS) is
performed over mTLS between two _Edge Runtime Groups_ ("Edge Runtime").

Certificates for all RGs are signed by an approved Certificate Authority.

An additional layer of authentication is implemented using tokens signed by each
RG and exchanged using standard HTTP headers.

The Client Edge Runtime prepares an `X-Edge-Token` JWT and passes it to the Service Edge Runtime.
The Service Edge Runtime validates the token before passing the request to the upstream
service, then returns a signed `X-Edge-Token` JWT. The Client Edge Runtime validates the
token before passing the response to the calling client.

## IS Client to Edge (request)

| Header Name      | Description                                                               |
| ---------------- | ------------------------------------------------------------------------- |
| `X-Client-Id`    | Client subsystem identifier used to select the provisioned connection            |
| `Authorization`  | Client identity JWT                                                       |
| `Correlation-Id` | Optional                                                                  |
| `Content-Digest` | Optional - request content digest (RFC 9530)<br>`sha-256=:<hash-base64>:` |

`X-Client-Id` selects the provisioned connection. The
[P2P routing contract](/reference/sdx/p2p-routing-contract.md) records the
route keys, the headers SDX replaces, and which values a provider may trust.

The `Authorization` header MUST contain a token that is issued from an approved
Identity and Authorization Provider. The `azp` claim is the integration client.
On `SDX.R1.00`, the consumer edge allows the request when that client is
allowed for the subsystem selected by `X-Client-Id`.

### Privacy zone token exchange audiences

When privacy zone token exchange is enabled, the original token must include
the configured SDX exchange client in `aud`. Keycloak uses that audience to
authorize SDX to exchange a token issued to another client. The requesting
client is also responsible for requesting any audience required by the
provider API or another downstream resource, using the mechanism supported by
its authorization server. SDX preserves those audiences during exchange.

SDX constructs the exchange audience set as follows:

1. Read `aud` from the JWT already verified by `jwt-keycloak`.
2. Accept either a string or an array and compare values exactly.
3. Require and retain the SDX exchange client ID.
4. Preserve the other original audiences.
5. Merge `tokenExchange.audience` when an optional configured value is present.
6. Remove exact duplicates and send each resulting value as a repeated RFC 8693
   `audience` parameter.

The SDX exchange client is always requested. Other audiences are included when
the original client requested them because the provider API requires a
resource audience or another downstream client needs the exchanged token as
the subject of a permitted token exchange. Retaining the SDX exchange client
allows the provider to use the exchanged token for a subsequent SDX call.

`tokenExchange.audience` is an optional plugin input. When configured, SDX
merges it with the verified original audiences and removes duplicates. This
supports both connections that use a configured audience and connections whose
target audiences are already present in the original token. Existing SDX
provisioning policies may continue to require or populate the configured
value.

| Token exchange | Original token requirements | Exchanged token audiences |
| -------------- | --------------------------- | -------------------------- |
| Enabled, no target resource audience | Includes the SDX exchange client | SDX exchange client only |
| Enabled, target resource audience required | Includes the SDX exchange client and target audience | SDX exchange client and target audience |
| Enabled, configured audience | Includes the SDX exchange client; configuration supplies one additional audience | SDX exchange client and configured audience |
| Disabled | Already includes the audience expected by the target resource | Original token is forwarded unchanged |

If the original token does not authorize the SDX exchange client, SDX stops
before calling Keycloak and returns a correlated HTTP 400 response. SDX does
not expose the audience values in that response.

### Privacy zone token exchange scopes

When privacy zone token exchange is configured together with the `token`
upgrade for token verification, the Client Edge Runtime reads the
space-delimited `scope` claim from the verified incoming token, removes
duplicate values, and sends those scopes in the token-exchange request. The
`tokenExchange` upgrade alone does not imply that incoming-token verification
or verified-subject scope transfer occurs. The configured SDX exchange client
must be permitted to request every required scope.

APS-4931 transfers only the scopes already present in the verified subject
token. APS-5006, which supplies the target privacy-zone scope, is a prerequisite
for R1 activation.

For a successful exchange, SDX handles the token endpoint's `scope` response
according to
[RFC 8693 section 2.2.1](https://www.rfc-editor.org/rfc/rfc8693.html#section-2.2.1):

- an omitted `scope` value means the granted scopes match the requested scopes;
- an explicit matching set is accepted regardless of order; and
- an explicit different set is logged as a warning, and the exchange continues.

This comparison uses the token response metadata. SDX does not decode,
validate, or introspect the new access token as part of the exchange. The
Service Edge Runtime and provider API remain responsible for validating and
authorizing the exchanged token before serving the request.

## Message transport

### Client Edge to Service Edge (request)

The Client Edge Runtime prepares an `X-Edge-Token` JWT signed with its
private key and adds it to the request headers. The Service Edge Runtime validates
the JWT using the specified `jwks_uri` and checks it is in a defined allow list.

The Client Edge Runtime creates the content digest if the client does not supply one.
If the client supplies a digest, the Client Edge Runtime validates it.

| Header Name                       | Description                                                               |
| --------------------------------- | ------------------------------------------------------------------------- |
| `X-Edge-Token`                    | JWT                                                                       |
| `X-SDX-Client-Subsystem-Id`       | Client subsystem identifier set by SDX                                    |
| `X-SDX-Original-AZP`              | Original verified JWT `azp`; present when SDX performs a token exchange   |
| `X-Client-Id`                     | Client subsystem identifier used for provisioned connection routing      |
| `X-Service-Id`                    | Service identifier                                                        |
| `Content-Digest`                  | Request content digest (RFC 9530)<br>`sha-256=:<hash-base64>:`            |
| `Authorization`                   | Client identity JWT                                                       |
| `Correlation-Id`                  | If passed, forwards it; otherwise, generates a new UUID                   |

**X-Edge-Token JWT:**

| Claim        | Description                                           | Example                      |
| ------------ | ----------------------------------------------------- | ---------------------------- |
| `jti`        | Unique identifier for a given token                   | UUID                         |
| `iat`        | Issued at timestamp when token was created (RFC 7519) |                              |
| `request_id` | Request ID                                            | UUID                         |
| `client_id`  | Client subsystem identifier                           | MIN.CITZ.SDG                 |
| `service_id` | Service identifier                                    | LAB.PUB.LTSA.TITLE-LOOKUP.v1 |
| `digest`     | Request content digest (RFC 9530)                     | `sha-256=:<hash-base64>:`    |
| `jwks_uri`   | Client Edge's JWK Set                                 |                              |

### Service Edge to Client Edge (response)

The Service Edge Runtime prepares an `X-Edge-Token` JWT signed by its
private key and adds it to the response headers. The Client Edge Runtime validates
the JWT using the specified `jwks_uri` and checks it is in a defined allow list.

| Header Name      | Description                                                     |
| ---------------- | --------------------------------------------------------------- |
| `X-Edge-Token`   | JWT                                                             |
| `Content-Digest` | Response content digest (RFC 9530)<br>`sha-256=:<hash-base64>:` |

**X-Edge-Token JWT:**

The Edge Runtime uses the `request_id`, `client_id`, `service_id`, and `digest`
from the `X-Edge-Token` to populate this token.

| Claim        | Description                                           | Example                      |
| ------------ | ----------------------------------------------------- | ---------------------------- |
| `jti`        | Unique identifier for a given token                   | UUID                         |
| `iat`        | Issued at timestamp when token was created (RFC 7519) |                              |
| `request_id` | Request ID                                            | UUID                         |
| `client_id`  | Client subsystem identifier                           | MIN.CITZ.SDG                 |
| `service_id` | Service identifier                                    | LAB.PUB.LTSA.TITLE-LOOKUP.v1 |
| `digest`     | Request content digest (RFC 9530)                     | `sha-256=:<hash-base64>:`    |
| `jwks_uri`   | Service Edge's JWK Set                                |                              |

## Edge to IS Service (request)

| Header Name                       | Description                                                               |
| --------------------------------- | ------------------------------------------------------------------------- |
| `X-Edge-Token`                    | JWT                                                                       |
| `X-SDX-Client-Subsystem-Id`       | Client subsystem identifier set by SDX                                    |
| `X-SDX-Original-AZP`              | Original verified JWT `azp`; present when SDX performs a token exchange   |
| `X-Client-Id`                     | Compatibility copy of the subsystem id for existing provider integrations |
| `X-Service-Id`                    | Service identifier                                                        |
| `Content-Digest`                  | Request content digest (RFC 9530)<br>`sha-256=:<hash-base64>:`            |
| `Authorization`                   | Client identity JWT                                                       |
| `Correlation-Id`                  | Passed from the client or generated by the Client Edge Runtime            |

### Provider identity header rules

SDX always sets `X-SDX-Client-Subsystem-Id` from the client subsystem on the
provisioned connection. The `X-SDX` prefix identifies SDX as the source, and
`Client-Subsystem-Id` states the value's catalog meaning. SDX removes a value
supplied by the calling client before adding the authoritative value.

`X-SDX-Original-AZP` records the `azp` claim from the verified token received
before an SDX token exchange. The name identifies both the source claim and the
fact that it predates the exchange. SDX replaces any caller-supplied value and
omits this header on requests where it cannot obtain a usable `azp` from the
verified subject token. The header contains one client identifier; it is not an
exchange history.

For backward compatibility with existing provider integrations, SDX continues
to send `X-Client-Id` with the same subsystem identifier as
`X-SDX-Client-Subsystem-Id`. Provider APIs should use
`X-SDX-Client-Subsystem-Id` for new integrations. Route selection and the
trust rule for each header are in the
[P2P routing contract](/reference/sdx/p2p-routing-contract.md).

## IS Service to Edge (response)

| Header Name      | Description                                                                |
| ---------------- | -------------------------------------------------------------------------- |
| `Content-Digest` | Optional - response content digest (RFC 9530)<br>`sha-256=:<hash-base64>:` |
