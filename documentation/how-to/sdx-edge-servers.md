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
- Create runtime group gateway
- Deploy runtime group infrastructure
  - Request a one-time-use certificate signing token
  - Deploy the runtime group infrastructure
  - Apply default routes and controls
  - Verification test
  - Add public key to the registry

## Prerequisites

- [Install Restish CLI](/reference/restish-cli.md)
- [Install Helm](https://helm.sh/docs/intro/install/) (if deploying the runtime group infrastructure)

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
      my-org \
      'name: newrg, environment: lab, hostedOrganizations: ["my-org"], sdxEndpoint: "https://142.34.194.118:443"'
    ```

=== "Reference"

    This is performed by a System Owner to create a new runtime group.

    - **API** `PUT /organizations/{org}/runtime-groups`

    Parameters:

    - `{org}=<your-organization>`

    ```json
    {
      "name": "abc123",
      "environment": "dev",
      "sdxEndpoint": "https://142.34.194.118:443",
      "consumerEndpoint": "http://internal.abc123.servers.sdx",
      "hostedOrganizations": ["ministry-X", "ministry-Y"]
    }
    ```

    | Attribute             | Description                                                                           |
    | --------------------- | ------------------------------------------------------------------------------------- |
    | `name`                | Unique identifier (lowercase alphanumeric text between 3 and 8 characters)            |
    | `environment`         | Target environment |
    | `sdxEndpoint`         | Routable IP-based endpoint from the internet (example above is the Gold ingress IP)   |
    | `consumerEndpoint`    | Domain that the Runtime Group uses automatically (port 8000, internal.<EDGE_DOMAIN>)  |
    | `hostedOrganizations` | List of all the organizations that are permitted to use this particular Runtime Group |

## Create runtime group gateway

As a System Owner, you perform this task. Once complete, you can set up the
default routing policies for this runtime group.

!!! warning "Registration is not a safe retry"
    `register-runtime-group-gateway` is create-only. If the runtime group's
    namespace was already partially registered (for example after an earlier
    failed or interrupted attempt), rerunning registration for the same name
    fails rather than repairing the existing namespace, and manually deleting
    the namespace can leave retained Kong catalog services/routes with no
    corresponding live data-plane configuration. There is currently no
    documented preflight or reconcile command for this state — verify with
    the APS team before deleting an existing runtime namespace to retry
    registration.

=== "Restish CLI"

    Help information about the operation to assign a runtime group:

    ```sh
    restish sdx register-runtime-group-gateway
    ```

    Example:

    ```sh
    restish sdx register-runtime-group-gateway \
      my-org newrg
    ```

=== "Reference"

    - **API** `PUT /organizations/{org}/runtime-groups/{name}/gateway`

    Parameters:

    - `{org}=<your-organization>`
    - `{name}=<your-runtime-group-name>`

An assigned Gateway ID will be returned. This Gateway can be used to configure
default routes and controls for this runtime group.

!!! note "Granting namespace access to additional users"
    Registration grants SDX namespace scopes only to the caller who created
    the runtime group's gateway. There is no Restish or other APS/SDX REST
    operation for granting or repairing another user's scopes on an existing
    namespace. Additional users must be granted access through the API
    Services Portal's **Administration Access** page (GraphQL API), which
    itself requires the requesting user to hold `Namespace.Manage` on that
    namespace. Do not attempt to grant access by creating an ordinary
    Keycloak authorization permission directly — the platform expects a
    resource-owner-managed UMA permission ticket, and the two are not
    interchangeable. A namespace with no `Namespace.Manage` holder currently
    has no self-service recovery path; contact the APS team.

## Deploy runtime group infrastructure

### Request a one-time-use certificate signing token

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
      my-org newrg lab
    ```

=== "Reference"

    - **API** `POST /organizations/{org}/runtime-groups/{name}/tokens`

    Parameters:

    - `{org}=<your-organization>`
    - `{name}=<your-runtime-group-name>`

It will return a token which can be extracted and stored in a local file
for the next step.

### Deploy the runtime group infrastructure

We have a helm chart available for deploying a runtime group into a Kubernetes/Openshift environment.

There has been some exploratory work for deploying infrastructure in Azure.

Please reach out to the APS team to discuss your requirements if the helm chart is not sufficient.

```sh
export IP="<ip specified in the sdxEndpoint above>"
export EDGE_ID="<name specified above>"
export ENV=lab
export DOMAIN="${EDGE_ID}.${ENV}.servers.sdx"

helm upgrade --install ${EDGE_ID} \
  --set bootstrap.tls.token=$(cat token) \
  --set bootstrap.tls.cn=${DOMAIN} \
  --set bootstrap.tls.ip=${IP} \
  --set route.host=${DOMAIN} \
  oci://ghcr.io/bcgov/aps-devops/sdx-edge:0.3.0
```

### Provision default routes and controls

You can now call the API to preview and then publish Gateway configuration
containing the default routing rules for the runtime group.

Actions available:

- `preview` : see what configuration the pattern produced
- `apply` : apply the configuration
- `diff` : dry run showing what will be updated if the `apply` is used
- `delete` : deletes the configuration

=== "Restish CLI"

    Help information about the operation to generate and apply Gateway configuration:

    ```sh
    restish sdx provision-config-from-pattern
    ```

    Example:

    ```sh
    restish sdx provision-config-from-pattern \
      my-org sdx-runtime-group.r1 \
      --action apply \
      'parameters:{ runtimeGroupName: newrg, environment: lab }'
    ```

!!! note "Required authorization scope"
    The generated help for `provision-config-from-pattern` lists
    `System.Manage` as the required scope. The effective requirement is
    actually `GatewayPattern.Publish`, resolved against the runtime's
    namespace (for example `<namespace>:GatewayPattern.Publish`), and it is
    granted automatically to the runtime's registering System Owner.
    Authorization happens in two stages: `GatewayPattern.Publish` gates the
    `preview`/`diff`/`apply`/`delete` endpoint itself for the human caller,
    and a separate `GatewayConfig.Publish` scope, held by the internal
    `sdx-provisioner` client rather than the caller's own token, gates the
    downstream GWA namespace publish that `diff` and `apply` trigger.
    `preview` returns generated configuration before that downstream request
    and therefore only needs the outer `GatewayPattern.Publish` scope.

!!! note "Reading `diff` results"
    `diff` is a dry run, but its response reuses mutation-sounding fields —
    a top-level `applied` count and a per-provider `status: applied` — even
    when nothing was changed. Those fields describe successful **processing**
    of the dry run, not the number of gateway changes committed. Do not treat
    a `diff` response as evidence that Kong configuration changed; check the
    nested `details.message` (for example `Dry-run. No changes applied.`) and
    the Created/Updated/Deleted summary for the actual proposed changes, and
    use `apply` to commit them.

### Verification test

Running the following should return `400 No required SSL certificate was sent`.

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

!!! note "Peer TLS trust"
    These checks verify the runtime group's own edge, but do not verify
    trust between peer runtime groups. Before relying on an active
    peer-to-peer connection, confirm that the calling edge's Kong trusts the
    peer edge's issuing CA (Kong returns `HTTP 502` with an upstream TLS
    verification failure otherwise). Also note that the endpoint host
    displayed by the portal may be normalized by GWA to the namespace's
    permitted environment domain rather than shown verbatim.

### Add public key to the registry

The public key will be used for other runtime groups to verify the integrity
of the request.

The helm deployment and bootstrap job will create the sdx-edge secret for the tls certificate
pair. Save the `tls.crt` contents to a `tls.crt` file locally.

=== "Restish CLI"

    Help information about the operation:

    ```sh
    restish sdx provision-config-from-pattern
    ```

    Example call:

    ```sh
    restish sdx provision-config-from-pattern \
      my-org sdx-keys.r1 \
      --action apply \
      'parameters:{ certificatePem[0]: @tls.crt, runtimeGroupName: newrg, environment: lab }'
    ```

=== "Reference"

    Using the same pattern endpoint from above, you can use the `sdx-keys.r1` pattern
    to add the public key using the certificate from the runtime group.

    ```json
    {
      "pattern": "sdx-keys.r1",
      "parameters": {
        "runtimeGroupName": "<runtime-group-name>",
        "environment": "lab|dev|test|prod",
        "certificatePem": ["<public-certificate-pem-format>"]
      }
    }
    ```

    `certificatePem` is an array; only the public certificate is supplied
    here, and the private key must remain mounted in the runtime group's
    edge. `organization` is derived from the `{org}` path parameter and does
    not need to be supplied in the body.

!!! warning "Prerequisite for signed connections"
    Registering the runtime group's public key with `sdx-keys.r1` is a
    mandatory prerequisite before enabling the `sign` upgrade on a consumer
    connection or the `verify` upgrade on a provider connection (see
    [Manage Connections](/how-to/sdx-connections.md)). The `trust-sign`
    plugin embeds the runtime's JWKS URI in the signature but does not create
    or publish the key set itself — until `sdx-keys.r1` has been applied, the
    JWKS URL will return `404 Key set not found` and traffic relying on
    verification will fail.

## Decommission Runtime Group

> To be documented..

Steps to decommission:

- uninstall infrastructure
- remove default routes
- remove keys
- delete runtime group

## Next steps

- [Setup Organization Signing](/how-to/sdx-org-signing.md)
