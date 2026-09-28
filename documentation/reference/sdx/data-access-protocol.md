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
| `X-Client-Id`    | Client subsystem identifier                                               |
| `Authorization`  | Client identity JWT                                                       |
| `Correlation-Id` | Optional                                                                  |
| `Content-Digest` | Optional - request content digest (RFC 9530)<br>`sha-256=:<hash-base64>:` |

The `Authorization` header MUST contain a token that is issued from an approved
Identity and Authorization Provider. The `azp` claim maps to an SDX Subsystem
and controls the client connection to the requested target service.

### Privacy zone token exchange audiences

When privacy zone token exchange is enabled, the original token must include
the configured SDX exchange client in `aud`. Keycloak uses that audience to
authorize SDX to exchange a token issued to another client. The requesting
client does not need to know the target provider resource audience; that value
is configured on the consumer `tokenExchange` upgrade.

SDX constructs the exchange audience set as follows:

1. Read `aud` from the JWT already verified by `jwt-keycloak`.
2. Accept either a string or an array and compare values exactly.
3. Require and remove the SDX exchange client ID.
4. Start the result with the configured consumer audience.
5. Append the remaining original audiences in their original order.
6. Remove exact duplicates and send each value as a repeated RFC 8693
   `audience` parameter.

The configured consumer audience is required and is always requested. Other
audiences in the original token are optional. They can be used when a
downstream client needs the exchanged token as the subject of another
permitted token exchange.

| Token exchange | Original token requirements | Exchanged token audiences |
| -------------- | --------------------------- | -------------------------- |
| Enabled, no optional downstream audience | Includes the SDX exchange client | Configured consumer audience |
| Enabled, optional downstream audiences | Includes the SDX exchange client and optional audiences | Configured consumer audience plus the optional audiences |
| Disabled | Already includes the audience expected by the target resource | Original token is forwarded unchanged |

If the original token does not authorize the SDX exchange client, SDX stops
before calling Keycloak and returns a correlated HTTP 400 response. SDX does
not expose the audience values in that response.

### Privacy zone token exchange scopes

When privacy zone token exchange is configured, the Client Edge Runtime first
verifies the incoming token. It reads the space-delimited `scope` claim from
that verified token, removes duplicate values, and sends those scopes in the
token-exchange request. The configured SDX exchange client must be permitted to
request every required scope.

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

| Header Name      | Description                                                    |
| ---------------- | -------------------------------------------------------------- |
| `X-Edge-Token`   | JWT                                                            |
| `X-Client-Id`    | Client subsystem identifier                                    |
| `X-Service-Id`   | Service identifier                                             |
| `Content-Digest` | Request content digest (RFC 9530)<br>`sha-256=:<hash-base64>:` |
| `Authorization`  | Client identity JWT                                            |
| `Correlation-Id` | If passed, forwards it; otherwise, generates a new UUID        |

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

| Header Name      | Description                                                    |
| ---------------- | -------------------------------------------------------------- |
| `X-Edge-Token`   | JWT                                                            |
| `X-Client-Id`    | Client subsystem identifier                                    |
| `X-Service-Id`   | Service identifier                                             |
| `Content-Digest` | Request content digest (RFC 9530)<br>`sha-256=:<hash-base64>:` |
| `Authorization`  | Client identity JWT                                            |
| `Correlation-Id` | Passed from the client or generated by the Client Edge Runtime |

## IS Service to Edge (response)

| Header Name      | Description                                                                |
| ---------------- | -------------------------------------------------------------------------- |
| `Content-Digest` | Optional - response content digest (RFC 9530)<br>`sha-256=:<hash-base64>:` |
