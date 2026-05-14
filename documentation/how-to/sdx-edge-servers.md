---
title: Install a Runtime Group
---

This page shows how to install a runtime group for your organization on SDX.

Before your systems can start to connect with other systems in SDX, your organization must
either deploy a runtime group in your own infrastructure (`client-hosted`), or you must signup
for using one of the shared runtime groups (`community-hosted`).

The steps described in this page are performed by the following roles:

| Role         | Function                                                               |
| ------------ | ---------------------------------------------------------------------- |
| System Owner | Request a new runtime group, and manage onboarding a new runtime group |

!!! note "Community Hosted"

    If you are going to use one of the `community-hosted` runtime groups, please
    reach out to the APS team, and skip this how-to guide.

Use cases for `client-hosted`:

- Register a new runtime group
- Request a one-time-use certificate signing token
- Deploy the runtime group infrastructure
- Apply default routes and controls
- Verification test
- Add public key to registry

## Prerequisites

- [Install Restish CLI](/reference/restish-cli.md)

## Register a new runtime group

To register a runtime group, you need to know the internet-facing IP address that
will be used to route traffic to this runtime group.

=== "Restish CLI"

    Help information about the operation to list available runtimes:

    ```sh
    restish sdx create-runtime-group
    ```

    Example:

    ```sh
    restish sdx create-runtime-group \
      ministry-of-citz \
      'name: newrg, hostedOrganizations: ["ministry-of-citz"], sdxEndpoint: "https://142.34.194.118:443"'
    ```

=== "Reference"

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

    | Attribute             | Description                                                                           |
    | --------------------- | ------------------------------------------------------------------------------------- |
    | `name`                | Unique identifier (lowercase alphanumeric text between 3 and 8 characters)            |
    | `sdxEndpoint`         | Routable IP-based endpoint from the internet (example above is the Gold ingress IP)   |
    | `consumerEndpoint`    | Domain that the Runtime Group uses automatically (port 8000, internal.<EDGE_DOMAIN>)  |
    | `hostedOrganizations` | List of all the organizations that are permitted to use this particular Runtime Group |

## Request a one-time-use certificate signing token

The runtime group infrastructure uses a token from the CA to bootstrap
the first certificate.

The certificate is used from supporting `mTLS` between runtime groups.

This is performed by a System Owner to request a new cert signing token.

=== "Restish CLI"

    Help information about the operation:

    ```sh
    restish sdx generate-one-time-use-token
    ```

    Example call:

    ```sh
    restish sdx generate-one-time-use-token \
      ministry-of-citz newrg
    ```

=== "Reference"

    - **API** `PUT /organizations/{org}/runtime-groups/{name}/tokens`

    Parameters:

    - `{org}=<your-organization>`
    - `{name}=<your-runtime-group-name>`

It will return a token which can be extracted and stored in a local file
for the next step.

## Deploy the runtime group infrastructure

We have a helm chart available for deploying a runtime group into a Kubernetes/Openshift environment.

There has been some exploratory work for deploying infrastructure in Azure.

Please reach out to the APS team to discuss your requirements if the helm chart is not sufficient.

```sh
export IP="<ip specified in the sdxEndpoint above>"
export EDGE_ID="<name specified above>"
export DOMAIN="${EDGE_ID}.servers.sdx"

helm upgrade --install ${EDGE_ID} \
  --set bootstrap.tls.token=$(cat token) \
  --set bootstrap.tls.cn=${DOMAIN} \
  --set bootstrap.tls.ip=${IP} \
  --set route.host=${DOMAIN} \
  oci://ghcr.io/bcgov/aps-devops/sdx-edge:0.2.0
```

## Create runtime group gateway

As a System Owner, you perform this task. Once complete, you can set up the
default routing policies for this runtime group.

=== "Restish CLI"

    Help information about the operation to assign  a runtime group:

    ```sh
    restish sdx register-runtime-group-gateway
    ```

    Example:

    ```sh
    restish sdx register-runtime-group-gateway \
      ministry-of-citz newrg
    ```

    An assigned Gateway ID will be returned. This Gateway can be used to configure
    default routes and controls for this runtime group.

## Apply default routes and controls

=== "Restish CLI"

    Help information about the operation to list available runtimes:

    ```sh
    restish sdx generate-config-from-pattern
    ```

    Example:

    ```sh
    restish sdx generate-config-from-pattern \
      ministry-of-citz \
      --action apply --dry-run=false \
      'pattern:sdx-runtime-group.r1, parameters:{ runtime_group_name: "newrg" }'
    ```

=== "Reference"

    You can now call the API to preview and then publish the default routing rules for
    the runtime group.

    - **API** `PUT /organizations/{org}/pattern?action=apply&dryRun=true`

    Parameters:

    - `{org}=<your-organization>`
    - values for `action`: `preview` and `apply`

    For `action=apply` you can specify `dryRun=true` if you want to see what changes
    will be applied without the changes actually being made.

    ```json
    {
      "pattern": "sdx-runtime-group.r1",
      "parameters": {
        "runtime_group_name": "<runtime-group-name>"
      }
    }
    ```

## Verification test

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

## Add public key to registry

The public key will be used for other runtime groups to verify the integrity
of the request.

The helm deployment and bootstrap job will create the sdx-edge secret for the tls certificate
pair. Save the `tls.crt` contents to a `tls.crt` file locally.

=== "Restish CLI"

    Help information about the operation:

    ```sh
    restish sdx generate-config-from-pattern
    ```

    Example call:

    ```sh
    restish sdx generate-config-from-pattern \
      ministry-of-citz \
      --action apply --dry-run=false \
      'pattern:sdx-keys.r1, parameters:{ certificate_pem[0]: @tls.crt, runtime_group_name: "newrg" }'
    ```

=== "Reference"

    Using the same pattern endpoint from above, you can use the `sdx-keys.r1` pattern
    to add the public key using the certificate from the runtime group.

    ```json
    {
      "pattern": "sdx-keys.r1",
      "parameters": {
        "runtime_group_name": "<runtime-group-name>",
        "certificate_pem": "<public-certificate-pem-format>"
      }
    }
    ```

## Next steps

- [Setup Organization Signing](/how-to/sdx-org-signing.md)
