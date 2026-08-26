---
title: "SDX Data Access Protocol"
---

The exchange of data between two organization Information Systems (IS) is
performed over mTLS between two Edge Runtime Groups (RG).

Certificates for all RGs are signed by an approved Certificate Authority.

An additional layer of authentication is implemented using tokens signed by each
RG and exchanged using standard HTTP headers.

The Client RG prepares an `X-Edge-Token` JWT and passes it to the Service RG,
where it will validate the token before passing to the upstream service.
An `X-Edge-Token` JWT is returned, signed by the Service RG. The Client RG
validates the token before passing the response to the calling client.

## IS Client to Edge (Request)

| Header Name      | Type                                                                      |
| ---------------- | ------------------------------------------------------------------------- |
| `Correlation-Id` | Optional                                                                  |
| `Content-Digest` | Optional - request content digest (RFC-9530)<br>`sha-512=:<hash-base64>:` |
| `Authorization`  | Client identity JWT                                                       |
| `DPoP`           | Optional demonstration of proof of possession (DPoP) JWT                  |

The `Authorization` header MUST contain a token that is issued from an approved
Identity and Authorization Provider. The `azp` claim will map to an SDX Subsystem,
and be used to control the client connection to the requested target service.

## Message Transport

### Client Edge to Service Edge (Request)

The Client RG will prepare an `X-Edge-Token` JWT that will be signed by its
private key and added to the request headers. The Service RG will validate
the JWT using the specified `jwks_uri`.

The Client RG will create the content digest if it is not supplied by the
client. If it is provided, then it will validate it.

| Header Name      | Type                                                           |
| ---------------- | -------------------------------------------------------------- |
| `X-Edge-Token`   | JWT                                                            |
| `Content-Digest` | Request content digest (RFC-9530)<br>`sha-512=:<hash-base64>:` |
| `Authorization`  | Optional identity JWT                                          |
| `Correlation-Id` | If passed, will forward, otherwise will generate a new UUID    |

**X-Edge-Token JWT:**

| Claim        | Description                                           | Example                   |
| ------------ | ----------------------------------------------------- | ------------------------- |
| `jti`        | Unique identifier for a given token                   | UUID                      |
| `iat`        | Issued at timestamp when token was created (RFC-7519) |                           |
| `request_id` | Request ID                                            | UUID                      |
| `client_id`  | Client ID (Consumer)                                  | MIN.CITZ.SDG              |
| `service_id` | Service ID (Provider)                                 | LAB.PUB.LTSA.TITLE-LOOKUP |
| `digest`     | Request content digest (RFC-9530)                     | `sha-512=:<hash-base64>:` |
| `jwks_uri`   | Client Edge's JWK Set                                 |                           |

### Service Edge to Client Edge (Response)

The Service RG will prepare an `X-Edge-Token` JWT that will be signed by its
private key and added to the response headers. The Client RG will validate
the JWT using the specified `jwks_uri`.

| Header Name      | Type                                                            |
| ---------------- | --------------------------------------------------------------- |
| `X-Edge-Token`   | JWT                                                             |
| `Content-Digest` | Response content digest (RFC-9530)<br>`sha-512=:<hash-base64>:` |

**X-Edge-Token JWT:**

The Edge Runtime will use the `request_id`, `client_id`, `service_id`, `digest`
from the X-Edge-Token to populate this token.

| Claim        | Description                                           | Example                   |
| ------------ | ----------------------------------------------------- | ------------------------- |
| `jti`        | Unique identifier for a given token                   | UUID                      |
| `iat`        | Issued at timestamp when token was created (RFC-7519) |                           |
| `request_id` | Request ID                                            | UUID                      |
| `client_id`  | Client ID (Consumer)                                  | MIN.CITZ.SDG              |
| `service_id` | Service ID (Provider)                                 | LAB.PUB.LTSA.TITLE-LOOKUP |
| `digest`     | Request content digest (RFC-9530)                     | `sha-512=:<hash-base64>:` |
| `jwks_uri`   | Service Edge's JWK Set                                |                           |

## IS Service to Edge (Response)

| Header Name      | Type                                                                       |
| ---------------- | -------------------------------------------------------------------------- |
| `Content-Digest` | Optional - response content digest (RFC-9530)<br>`sha-512=:<hash-base64>:` |
