---
title: "SDX Data Access Protocol"
---

The exchange of data between two organization _Information Systems_ (IS) is
performed over mTLS between two _Edge Runtime Groups_ (RG).

Certificates for all RGs are signed by an approved Certificate Authority.

An additional layer of authentication is implemented using tokens signed by each
RG and exchanged using standard HTTP headers.

The Client RG prepares an `X-Edge-Token` JWT and passes it to the Service RG.
The Service RG validates the token before passing the request to the upstream
service, then returns a signed `X-Edge-Token` JWT. The Client RG validates the
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

## Message transport

### Client Edge to Service Edge (request)

The Client RG prepares an `X-Edge-Token` JWT signed with its
private key and adds it to the request headers. The Service RG validates
the JWT using the specified `jwks_uri` and checks it is in a defined allow list.

The Client RG creates the content digest if the client does not supply one.
If the client supplies a digest, the Client RG validates it.

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

The Service RG prepares an `X-Edge-Token` JWT signed by its
private key and adds it to the response headers. The Client RG validates
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

## IS Service to Edge (response)

| Header Name      | Description                                                                |
| ---------------- | -------------------------------------------------------------------------- |
| `Content-Digest` | Optional - response content digest (RFC 9530)<br>`sha-256=:<hash-base64>:` |
