# Kong Upstream JWT

Reference: https://docs.konghq.com/hub/optum/kong-upstream-jwt

## Example

```
services:
- name: MY_REST_API
  tags: [ ns.<gatewayId> ]
  plugins:
    - enabled: true
      name: kong-upstream-jwt
      tags: [ ns.<gatewayId> ]
      config:
        header: GW-JWT
        include_credential_type: false
```

## JWKS

| Environment   | URL                                                                  |
| ------------- | -------------------------------------------------------------------- |
| Test/Training | https://aps-jwks-upstream-jwt-api-gov-bc-ca.test.api.gov.bc.ca/certs |
| Production    | https://aps-jwks-upstream-jwt.api.gov.bc.ca/certs                    |

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

> NOTE: If you are trying to run this on a Mac and you get `unable to get local issuer certificate`, you may need to run: `open /Applications/Python\ 3.11/Install\ Certificates.command` to install the latest CA certificates.
