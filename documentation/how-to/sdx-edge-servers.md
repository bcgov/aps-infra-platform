---
title: Provision a new Edge Server
---

This page shows how to provision a new Edge Server (Runtime Group) on the SDX Ecosystem.

The steps described in this page are performed by the following roles:

| Role         | Function                                                           |
| ------------ | ------------------------------------------------------------------ |
| System Owner | Request a new edge server, and manage onboarding a new edge server |

Use cases:

- Register a new Runtime Group
- Deploy Runtime Group infrastructure
- Initialize default route policies
- Add public key to registry

## Register a new Runtime Group

This is performed by a System Owner to create a new runtime group.

- **API** `PUT /organizations/{org}/runtime-groups`

Parameters:

- `{org}=<your-organization>`

```json
{
  "name": "abc123",
  "sdxEndpoint": "https://142.34.194.118:443",
  "consumerEndpoint": "http://internal.abc123.servers.sdx",
  "hostedOrganizations": ["ministry-X", "ministry-Y"]
}
```

| Attribute             | Description                                                                            |
| --------------------- | -------------------------------------------------------------------------------------- |
| `name`                | Unique identifier (lowercase alphanumeric text between 3 and 8 characters)             |
| `sdxEndpoint`         | Routable IP-based endpoint from the internet (example above is the Gold ingress IP)    |
| `consumerEndpoint`    | Domain that the Runtime Group uses automatically (port 8000, internal.<EDGE_DOMAIN>)   |
| `hostedOrganizations` | List of all the organizations that are permitted to use this particular Runetime Group |

## Deploy Runtime Group infrastructure

The runtime group is deployed using a helm chart.

A one-time use token is required for issuing the certificate that the runtime
group uses.

Reach out to the SDX Operator (APS team) to get a token.

```sh

export IP="<ip specified in the sdxEndpoint above>"
export EDGE_ID="<name specified above>"
export DOMAIN="${EDGE_ID}.servers.sdx"

helm upgrade --install ${EDGE_ID} \
  --set tls.client.bootstrap.token=$(cat token) \
  --set tls.client.cn=${DOMAIN} \
  --set tls.server.ip=${IP} \
  --set route.host=${DOMAIN} \
  oci://ghcr.io/bcgov/aps-devops/sdx-edge:0.1.0
```

## Initialize default route policies

You can now call the API to preview and then publish the default routing rules for
the runtime group.

- **API** `PUT /organizations/{org}/pattern?action=apply&dryRun=true`

Parameters:

- `{org}=<your-organization>`
- values for `action`: `preview` and `apply`

For `action=apply` you can specify `dryRun=true` if you want to see what changes
will be applied without the changes actually being made.

### `sdx-runtime-group.r1`

```json
{
  "pattern": "sdx-runtime-group.r1",
  "parameters": {
    "runtime_group_name": "<runtime-group-name>"
  }
}
```

## Verification

Running the following should return 400 No required SSL certificate was sent.

```sh
curl -v -k --resolve ${DOMAIN}:443:${IP} \
  https://${DOMAIN}
```

You can verify the consumer internal endpoint by opening a terminal on the
runtime group Kong pod and running:

```sh
curl -v --resolve internal.${DOMAIN}:8000:127.0.0.1 \
  http://internal.${DOMAIN}:8000/hello
```

## Add public key to the registry

The public key will be used for other runtime groups to verify the integrity
of the request.

Using the same pattern endpoint from above, you can use the `sdx-keys.r1` pattern
to add the public key using the certificate from the runtime group.

### `sdx-keys.r1`

```json
{
  "pattern": "sdx-keys.r1",
  "parameters": {
    "runtime_group_name": "<runtime-group-name>",
    "certificate_pem": "<public-certificate-pem-format>"
  }
}
```
