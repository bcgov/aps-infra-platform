# Kong Upstream JWT

The `kong-upstream-jwt` plugin adds a signed JWT to each request the Gateway
proxies to your upstream service. Your service validates the token's signature
to confirm that the request came through an APS Gateway, and checks the `aud`
claim to confirm that the request was meant for your Gateway Service.

The token is in the `JWT` header by default (set `header` to change it). APS
signs it with an RS256 key, and it expires one minute after it's issued. Validate
it against the [JWKS](#jwks) for your environment, and check the
[token claims](#token-claims), including that `aud` matches your Gateway Service
name.

For how this compares with mTLS and IP restrictions, see
[Set Up an Upstream Service](/how-to/upstream-services.md#public-cloud-and-on-premise).

## Configuration reference

This is a third-party plugin managed by Optum. See the [configuration reference page](https://docs.konghq.com/hub/optum/kong-upstream-jwt)
for a list of parameters and protocol compatibility notes.

## Common usage example

```yaml
plugins:
  - enabled: true
    name: kong-upstream-jwt
    service: <SERVICE_NAME>
    tags: [ ns.<gatewayId> ]
    config:
      header: GW-JWT
      include_credential_type: false
```

Use a dedicated header such as `GW-JWT` if your service also needs the
consumer's own `Authorization` header.

## Token claims

The token contains these claims:

- `iss`: the issuer, which is your environment's [JWKS](#jwks) URL without
  `/certs`.
- `aud`: the name of your Gateway Service.
- `iat`: when the Gateway issued the token.
- `exp`: when the token expires, 60 seconds after `iat`.
- `jti`: a unique ID for the request.
- `consumerid`: the ID of the consumer that called your API. Only included
  when the route identifies a consumer.
- `consumername`: the consumer's username. Only included when the route
  identifies a consumer that has a username.
- `payloadhash`: a lowercase hex SHA-256 hash of the raw request body. It
  doesn't cover the path, query string, or headers. It's an empty string (`""`)
  when the Gateway doesn't hold the body in memory: for requests with no body
  (such as `GET`), and for larger bodies (for example, over 8 KB on the Gold
  cluster). Because of this, don't rely on `payloadhash` to prove the body
  wasn't changed.

!!! warning "Check the audience as well as the signature"
    All Gateways in an APS environment share the same signing keys. A valid
    signature proves the request came through _an_ APS Gateway, not _your_
    Gateway. Your service must also check that `aud` matches your Gateway
    Service name, and reject every other value.

## JWKS

| Environment   | URL                                                                  |
| ------------- | -------------------------------------------------------------------- |
| Test/Training | <https://aps-jwks-upstream-jwt-api-gov-bc-ca.test.api.gov.bc.ca/certs> |
| Production    | <https://aps-jwks-upstream-jwt.api.gov.bc.ca/certs>                    |

## Clients

### Javascript (Express)

For this example, the `kong-upstream-jwt` plugin should be configured with:

```yaml
config:
  header: Authorization
  include_credential_type: true
```

`npm i express express-oauth2-jwt-bearer`

```javascript
const express = require("express");
const app = express();
const port = 3300;

const { auth } = require("express-oauth2-jwt-bearer");
app.use(auth());

app.get("/", (req, res) => {
  res.send("Hello World!");
});

app.listen(port, () => {
  console.log(`Listening on port ${port}`);
});
```

For `test/training` environment:

```sh
ISSUER_BASE_URL=https://aps-jwks-upstream-jwt-api-gov-bc-ca.test.api.gov.bc.ca \
AUDIENCE=<SERVICE-NAME> \
node server.js
```

### Python (FastAPI)

For this example, the `kong-upstream-jwt` plugin should be configured with:

```yaml
config:
  header: gw-jwt
  include_credential_type: false
```

`pip install fastapi uvicorn pyjwt`

```python
import os
import jwt
from jwt import PyJWKClient
from fastapi import FastAPI, Request, Depends, HTTPException

app = FastAPI()

def gateway_auth(request: Request) -> dict:
    try:
        encoded_token = request.headers['gw-jwt']
        jwks_client = PyJWKClient(os.environ.get('JWKS_URI'))
        signing_key = jwks_client.get_signing_key_from_jwt(encoded_token)
        return jwt.decode(encoded_token, signing_key.key,
          algorithms=["RS256"],
          audience=os.environ.get('AUDIENCE').split(","))
    except Exception as ex:
        raise HTTPException(
          status_code=401,
          detail=str(ex),
          headers={"WWW-Authenticate": "X-Gateway"})

@app.get("/")
def read_root( gateway: dict = Depends(gateway_auth)):
    return {"Hello": "World"}
```

For `test/training` environment:

```sh
JWKS_URI=https://aps-jwks-upstream-jwt-api-gov-bc-ca.test.api.gov.bc.ca/certs \
AUDIENCE=<SERVICE-NAME> \
uvicorn server:app --reload
```

> NOTE: If you are trying to run this on a Mac and you get `unable to get local
> issuer certificate`, you may need to run: `open /Applications/Python\
> 3.11/Install\ Certificates.command` to install the latest CA certificates.
