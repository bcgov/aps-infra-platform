---
title: Install an Edge Runtime Group
---

This page shows how to install a runtime group for your organization on SDX.

Before your systems can start to connect with other systems in SDX, your organization must
either deploy a runtime group in your own infrastructure (`client-hosted`), or you must signup
for using one of the shared runtime groups (`community-hosted`).

To learn more about the communication protocol between a client Edge Runtime
Group and a service Edge Runtime Group, visit the
[SDX Data Access Protocol](/reference/sdx/data-access-protocol.md) document.

The steps described in this page are performed by the following roles:

| Role         | Function                                                               |
| ------------ | ---------------------------------------------------------------------- |
| System Admin | Request a new runtime group, and manage onboarding a new runtime group |

!!! note "Community Hosted"

    If you are going to use one of the `community-hosted` runtime groups, please
    reach out to the APS team, and skip this how-to guide.

Use cases for `client-hosted`:

- Establish a new runtime group
- Register a runtime group gateway
- Deploy runtime group infrastructure
  - Request a one-time-use certificate signing token
  - Deploy the runtime group infrastructure
  - Apply default routes and controls
  - Verification test
  - Add public key to the registry
- Rotate runtime group keys

## Prerequisites

- [Install Restish CLI](/reference/restish-cli.md)
- [Install Helm](https://helm.sh/docs/intro/install/) (if deploying the runtime group infrastructure)

## Establish a new runtime group

To establish a runtime group, you need to know the internet-facing IP address that
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

    This is performed by a System Admin to create a new runtime group.

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

## Register a runtime group gateway

As a System Admin, you perform this task. Once complete, you can set up the
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

The certificate is used for supporting `mTLS` between runtime groups.

This is performed by a System Admin to request a new cert signing token.

=== "Restish CLI"

    Help information about the operation:

    ```sh
    restish sdx generate-one-time-use-token
    ```

    Example call:

    ```sh
    restish sdx generate-one-time-use-token \
      my-org newrg lab

    # Generate and save to "token"
    restish sdx generate-one-time-use-token \
      myo newrg lab | jq -r .token > token

    ```

=== "Reference"

    - **API** `POST /organizations/{org}/runtime-groups/{name}/environments/{environment}/tokens`

    Parameters:

    - `{org}=<your-organization>`
    - `{name}=<your-runtime-group-name>`
    - `{environment}=<target-environment>`

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
  oci://ghcr.io/bcgov/aps-devops/sdx-edge:0.3.7

# If you want to upgrade to a newer helm chart version, you can run
helm upgrade --install ${EDGE_ID} \
  --reset-then-reuse-values \
  --set bootstrap.tls.token="" \
  oci://ghcr.io/bcgov/aps-devops/sdx-edge:0.3.7
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
    granted automatically to the runtime's registering System Admin.
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

Provisioning keys is done using the same `provision-config-from-pattern`
operation/endpoint as the default Gateway routes and controls, but using the
`sdx-keys.r1` pattern. The `sdx-keys.r1` pattern is also used later to rotate keys.

The new public key is appended to the key set, and the key id (`kid`) is `{urn}:{8-hex}`
(the first eight hex digits of a UUID). Example:
`urn:ca:bc:sdx:edge:newrg:lab:8875a149`.

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

    - **API** `PUT /organizations/{org}/patterns/sdx-keys.r1?action={preview|diff|apply|delete}`

    ```json
    {
      "pattern": "sdx-keys.r1",
      "parameters": {
        "runtimeGroupName": "<runtime-group-name>",
        "environment": "lab|dev|test|prod",
        "certificatePem": ["<public-certificate-pem-format>"],
        "operation": "add"
      }
    }
    ```

    `certificatePem` is an array; `add`, `rotate`, and `replace` operations accept a
    single public certificate in that array. The private key must remain
    mounted in the runtime group's edge.

A successful `apply` or `diff` returns structured `changes` information:

```json
{
  "operation": "add",
  "added": [
    {
      "kid": "urn:ca:bc:sdx:edge:newrg:lab:8875a149",
      "name": "sdx.keys.newrg.lab.edge:8875a149"
    }
  ],
  "removed": [],
  "retained": []
}
```

The same payload's `info` result includes `details.endpoint`, the JWKS URL for
this key set.

Call `details.endpoint` from that `info` result and confirm the new `kid`
is in the key set.

The listed `kid`s should include the value from `changes.added`.

!!! warning "Prerequisite for signed connections"

    Registering the runtime group's public key with `sdx-keys.r1` is a
    mandatory prerequisite before enabling the `sign` upgrade on a consumer
    connection or the `verify` upgrade on a provider connection (see
    [Connecting a Service](/how-to/sdx-connections.md)). The `trust-sign`
    plugin embeds the runtime's JWKS URI in the signature but does not create
    or publish the key set itself — until `sdx-keys.r1` has been applied, the
    JWKS URL will return `404 Key set not found` and traffic relying on
    verification will fail.

## Runtime Group management

### Rotate runtime group keys

Rotate when the runtime group's edge certificate must change without
dropping verification of in-flight signed traffic. `rotate` publishes the
new public key and retains existing keys so both `kid`s appear in JWKS
until you retire the old one.

Do not restart Kong with the new private key until the rotate `apply` has
succeeded. If the edge starts signing with a key that is not yet in JWKS,
verification fails closed and requests are denied.

Query `action` is unchanged (`preview`, `diff`, `apply`, `delete`). Body
parameter `operation` selects a targeted update:

| `parameters.operation` | Effect                                                                                                                        |
| ---------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `add`                  | Append a public key. Retries with the same public key are idempotent. Default when `operation` is omitted on a runtime group. |
| `rotate`               | Append a **new** public key and retain existing keys for overlap.                                                             |
| `replace`              | Atomically swap `targetKid` for the incoming public key.                                                                      |
| `delete`               | Remove only `targetKid`. Refuses if it is the last remaining key.                                                             |

`targetKid` is required for `replace` and `delete`. `certificatePem` (one
entry) or `publicKeyPem` is required for `add`, `rotate`, and `replace`.
A caller may supply a full `urn:ca:bc:sdx:edge:…` `kid` to address an
existing key.

!!! warning "Query parameter `action=delete` vs `operation=delete`"

    Do not combine query parameter `action=delete` with body parameter `operation=delete`.
    Query parameter `action=delete` removes the **entire** key qualifier (key set and all keys). Targeted deletion is `action=apply` with `operation=delete`.

Overlap rotation:

1. Request a new one-time-use certificate signing token, as in
   [Request a one-time-use certificate signing token](#request-a-one-time-use-certificate-signing-token).
1. Stage a new runtime-group key and CSR **without restarting** Kong, then
   sign the CSR with that token. On the sdx-edge chart,
   `bootstrap.stageSecret=true` writes `{release}-client-next` and skips
   the rollout restart.
1. Publish the new public key with `operation=rotate` (below) while
   retaining the old one. `rotate` of a public key that is already in the
   set returns `422` — use `add` if you only need to republish existing
   material.
1. Confirm JWKS contains **both** kids: call the `endpoint` from the
   apply response's `info` result (same check as after the initial add).
   `changes.added` is the new `kid`; `changes.retained` are the previous
   ones.
1. Promote the staged secret to the live client/server secrets and rolling
   restart Kong (`rotation.promote=true` on the sdx-edge chart). Signed
   `X-Edge-Token` values should now carry the new `kid`.
1. Wait through the verifier grace period (`iss_key_grace_period`, default
   300 seconds).
1. Remove the old `kid` with `operation=delete` (below).

=== "Restish CLI"

    Publish a replacement key and retain the current set:

    ```sh
    restish sdx provision-config-from-pattern \
      my-org sdx-keys.r1 \
      --action apply \
      'parameters:{ operation: rotate, certificatePem[0]: @tls.crt, runtimeGroupName: newrg, environment: lab }'
    ```

    After the grace period, remove the outgoing `kid` (use the value from
    `changes.retained`):

    ```sh
    restish sdx provision-config-from-pattern \
      my-org sdx-keys.r1 \
      --action apply \
      'parameters:{ operation: delete, targetKid: "urn:ca:bc:sdx:edge:newrg:lab:8875a149", runtimeGroupName: newrg, environment: lab }'
    ```

=== "Reference"

    Publish a replacement key:

    ```json
    {
      "pattern": "sdx-keys.r1",
      "parameters": {
        "runtimeGroupName": "newrg",
        "environment": "lab",
        "operation": "rotate",
        "certificatePem": ["<new-public-certificate-pem-format>"]
      }
    }
    ```

    Remove the outgoing `kid`:

    ```json
    {
      "pattern": "sdx-keys.r1",
      "parameters": {
        "runtimeGroupName": "newrg",
        "environment": "lab",
        "operation": "delete",
        "targetKid": "urn:ca:bc:sdx:edge:newrg:lab:8875a149"
      }
    }
    ```

!!! note "Recovery"

    If rotate `apply` succeeds but restart has not happened, traffic still
    signs with the old private key and old `kid`. Both public keys are in
    JWKS, so verification continues. If restart happens before the new
    public key is published, republish with `operation=rotate` or `add`,
    then retry the restart. To abandon a staged key before promote, delete
    `{release}-client-next` and leave the live secret unchanged. After
    promote, restore the previous TLS secret, restart, then
    `operation=delete` (or `replace`) the new `kid` once verifiers no
    longer see it.

### Decommission Runtime Group

> To be documented..

Steps to decommission:

- uninstall infrastructure
- remove default routes
- remove keys (`sdx-keys.r1` with query `action=delete` and no `operation`
  removes the entire key qualifier)
- delete runtime group

## Next steps

- [Setup Organization Signing](/how-to/sdx-org-signing.md)
