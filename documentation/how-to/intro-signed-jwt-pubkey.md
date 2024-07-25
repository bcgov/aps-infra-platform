---
title: "Signed JWT w/ Certificate"
---


The following example uses NodeJS code to show how to prepare for signed JWT
authentication to an API on the BC Government API Gateway.

## 1. Generate a Certificate Key pair

```javascript
npm install --save node-jose ms

echo "
const fs = require('fs');
const jose = require('node-jose');

const keyStore = jose.JWK.createKeyStore()
keyStore.generate('RSA', 2048, {alg: 'RS256', use: 'sig' })
.then(result => {
  const [key] = keyStore.all({ use: 'sig' })
  fs.writeFileSync(
    'client.key',
    key.toPEM(true)
  )
  fs.writeFileSync(
    'client.crt',
    key.toPEM(false)
  )
  console.log('Saved to: client.key and client.crt')
})
" | node
```

## 2. Request access to an API

Go to the API Services Portal and request access to an API that is configured
with the Signed JWT protection. After selecting the environment, you will be
prompted to provide a "Public Key", which will be the contents of the
`client.crt` created in step 1. After requesting access, you will be provided
with some secrets.

Make a note of the `Client ID`, `Issuer` and `Token Endpoint`.

```shell
export CID=""
export ISS=""
export TURL=""
```

## 3. Request a Client JWT token

Requesting a Client JWT token is a two-step process:

a) Build a Client Assertion Token that is signed with the private key you
generated earlier.

b) Request a token from the Token Endpoint using the Client Assertion.

The following sample performs both steps:

```javascript
npm install --save njwt node-fetch@v2

echo "
const njwt = require('njwt');

const fs = require('fs')

const privateKey = fs.readFileSync('client.key')
const clientId = process.env.CID; // Or load from configuration
const now = Math.floor( new Date().getTime() / 1000 ); // seconds since epoch
const plus5Minutes = new Date( ( now + (5*60) ) * 1000); // Date object
const alg = 'RS256'; // one of RSA or ECDSA algorithms: RS256, RS384, RS512,
// ES256, ES384, ES512

const claims = {
  aud: process.env.ISS
};

const jwt = njwt.create(claims, privateKey, alg)
  .setIssuedAt(now)
  .setExpiration(plus5Minutes)
  .setIssuer(clientId)
  .setSubject(clientId)
  .compact();

const fetch = require('node-fetch');
const { URLSearchParams } = require('url');

const params = new URLSearchParams();
params.append('grant_type', 'client_credentials');
params.append('client_id', process.env.CID);
params.append('scopes', 'openid');
params.append('client_assertion_type', 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer');
params.append('client_assertion', jwt);

fetch(process.env.TURL, { method: 'POST', body: params })
    .then(res => res.json())
    .then(json => console.log(json));

" | node
```

## 4. Call the API

Call the API using the newly generated Token returned from the Identity Provider.

```shell
curl -v https://a-protected-api.test.api.gov.bc.ca/headers \
  -H "Authorization: Bearer $TOK"

```
