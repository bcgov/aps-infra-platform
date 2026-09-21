---
title: "Install an Edge Runtime Group"
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
- [Install Helm](https://helm.sh/docs/intro/install/) if you are deploying the
  runtime group infrastructure.
- Install `kubectl` or the OpenShift CLI (`oc`) and obtain access to the
  runtime group's namespace.
- Install `jq` to extract certificate tokens from Restish responses.

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
    corresponding live data-plane configuration. There is no documented
    preflight or reconcile command for this state. Verify with the APS team
    before deleting an existing runtime namespace to retry registration.

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
    Keycloak authorization permission directly. The platform expects a
    resource-owner-managed UMA permission ticket, and the two are not
    interchangeable. A namespace with no `Namespace.Manage` holder has no
    self-service recovery path. Contact the APS team.

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
  --set-string bootstrap.tls.token="$(cat token)" \
  --set-string bootstrap.tls.cn="${DOMAIN}" \
  --set-string bootstrap.tls.ip="${IP}" \
  --set-string route.host="${DOMAIN}" \
  oci://ghcr.io/bcgov/aps-devops/sdx-edge:0.3.7

# If you want to upgrade to a newer helm chart version, you can run
helm upgrade --install ${EDGE_ID} \
  --reset-then-reuse-values \
  --set-string bootstrap.tls.token="" \
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
    `System.Manage` as the required scope. The endpoint checks
    `GatewayPattern.Publish` on the runtime namespace (for example
    `<namespace>:GatewayPattern.Publish`). Registration grants that scope to
    the System Admin who registered the runtime.

    `GatewayPattern.Publish` allows the caller to run `preview`, `diff`,
    `apply`, and `delete`. `diff` and `apply` also publish to GWA. That step
    uses `GatewayConfig.Publish` on the internal `sdx-provisioner` client.
    `preview` returns the generated configuration before that publish, so it
    only needs `GatewayPattern.Publish`.

!!! note "Reading `diff` results"

    `diff` is a dry run. The response still includes an `applied` count and a
    per-provider `status: applied` when nothing changed. Those fields mean
    the dry run was processed. They are not the number of gateway changes
    committed. Check `details.message` (for example
    `Dry-run. No changes applied.`) and the Created/Updated/Deleted summary
    for the proposed changes. Use `apply` to commit them.

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
    verification failure otherwise). The endpoint host displayed by the
    portal may be normalized by GWA to the namespace's permitted environment
    domain.

### Add public key to the registry

The public key will be used for other runtime groups to verify the integrity
of the request.

The Helm deployment and bootstrap Job create the `sdx-edge` Secret containing
the TLS certificate pair. Save the `tls.crt` contents to a `tls.crt` file
locally. Do not extract or publish `tls.key`.

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
      'parameters:{
        certificatePem[0]: @tls.crt,
        runtimeGroupName: newrg,
        environment: lab
      }'
    ```

=== "Reference"

    - **API** `PUT /organizations/{org}/patterns/sdx-keys.r1` with query
      `action={preview|diff|apply|delete}`

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

    `certificatePem` is an array. The `add`, `rotate`, and `replace`
    operations accept a single public certificate in that array. The private
    key must remain mounted in the runtime group's edge.

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
    plugin embeds the runtime's JWKS URI in the signature. It does not create
    or publish the key set. Until `sdx-keys.r1` has been applied, the JWKS
    URL returns `404 Key set not found` and traffic that requires verification
    fails.

## Runtime group management

### Rotate runtime group keys

Rotate when the runtime group's edge certificate must change without
dropping verification of in-flight signed traffic. `rotate` publishes the
new public key and retains existing keys so both `kid`s appear in JWKS
until you retire the old one.

Do not restart Kong with the new private key until the rotate `apply` has
succeeded. If the edge starts signing with a key that is not yet in JWKS,
verification denies the requests.

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
A caller may supply a full `urn:ca:bc:sdx:edge:...` `kid` to address an
existing key.

!!! warning "Query parameter `action=delete` vs `operation=delete`"

    Do not combine query parameter `action=delete` with body parameter
    `operation=delete`. Query parameter `action=delete` removes the **entire**
    key qualifier, including the key set and all keys. For targeted deletion,
    use `action=apply` with `operation=delete`.

Use sdx-edge chart version `0.3.7` or later. Set the following variables and
select the Kubernetes or OpenShift namespace that contains the Helm release:

```sh
export ORG="my-org"
export EDGE_ID="newrg"
export ENV="lab"
export SDX_EDGE_CHART_VERSION="0.3.7"
export EDGE_RESOURCE="sdx-edge-${EDGE_ID}"
```

Follow these steps for an overlap rotation:

1. Request a one-time-use certificate signing token and save it to a
   restricted local file:

   ```sh
   umask 077
   restish sdx generate-one-time-use-token \
     "${ORG}" "${EDGE_ID}" "${ENV}" |
     jq -r .token > rotation-token
   ```

1. Stage a new private key and signed certificate without restarting Kong.
   The bootstrap Job writes `${EDGE_RESOURCE}-client-next`. It does not
   change the live client or server Secrets:

   ```sh
   helm upgrade "${EDGE_ID}" \
     "oci://ghcr.io/bcgov/aps-devops/sdx-edge:${SDX_EDGE_CHART_VERSION}" \
     --reuse-values \
     --wait --wait-for-jobs \
     --set-string bootstrap.tls.token="$(cat rotation-token)" \
     --set bootstrap.stageSecret=true \
     --set rotation.promote=false
   ```

1. Confirm the staged Secret exists, then extract only its public
   certificate:

   ```sh
   kubectl get secret "${EDGE_RESOURCE}-client-next"
   kubectl get secret "${EDGE_RESOURCE}-client-next" \
     -o jsonpath='{.data.tls\.crt}' |
     base64 -d > tls-next.crt
   ```

1. Publish the staged public certificate while retaining the existing keys:

   ```sh
   restish sdx provision-config-from-pattern \
     "${ORG}" sdx-keys.r1 \
     --action apply \
     "parameters:{
       operation: rotate,
       certificatePem[0]: @tls-next.crt,
       runtimeGroupName: ${EDGE_ID},
       environment: ${ENV}
     }"
   ```

   `operation=rotate` returns `422` if the same public key is already in the
   key set. Use `operation=add` to make a retry with already-published key
   material idempotent.

1. Record the new `kid` from `changes.added` and every outgoing `kid` from
   `changes.retained`. Find the JWKS URL in the `details.endpoint` field of
   the response's `info` result. Confirm that the JWKS contains both the new
   and outgoing `kid` values:

   ```sh
   curl --fail --silent --show-error "<JWKS_URL>" |
     jq -r '.keys[].kid'
   ```

1. Wait at least one verifier grace period after publishing the new key.
   `trust-verify-signature` refreshes an old cached key set after a missing
   `kid` only when the cache is older than `iss_key_grace_period`, which is
   300 seconds in the SDX patterns. Waiting before promotion prevents a
   verifier with a fresh, old-only cache from rejecting the new `kid`.

1. Back up the live `${EDGE_RESOURCE}-client` and
   `${EDGE_RESOURCE}-server` Secrets using your organization's secure secret
   backup procedure. Promotion overwrites both Secrets, and the chart does
   not create a copy of the previous private key.

1. Promote the staged Secret and restart Kong. Clear the consumed bootstrap
   token with an empty string, set `bootstrap.stageSecret=false`, and set a
   new `rotation.nonce` so the promote Job runs once:

   ```sh
   helm upgrade "${EDGE_ID}" \
     "oci://ghcr.io/bcgov/aps-devops/sdx-edge:${SDX_EDGE_CHART_VERSION}" \
     --reuse-values \
     --wait \
     --set-string bootstrap.tls.token="" \
     --set bootstrap.stageSecret=false \
     --set rotation.promote=true \
     --set-string rotation.nonce="$(date +%s)"
   ```

   !!! warning "Clear the bootstrap token with an empty string"

       Do not use `--set bootstrap.tls.token=null`. Helm can restore the
       previous token when coalescing reused values, leaving an immutable
       completed Job in the release or recreating it with a spent token.

1. Wait for the Kong rollout, then set `rotation.promote` back to `false`.
   If `rotation.promote=true` remains in the release values, a later
   `--reuse-values` upgrade can promote the staged Secret again:

   ```sh
   kubectl rollout status deployment "${EDGE_RESOURCE}"

   helm upgrade "${EDGE_ID}" \
     "oci://ghcr.io/bcgov/aps-devops/sdx-edge:${SDX_EDGE_CHART_VERSION}" \
     --reuse-values \
     --wait \
     --set rotation.promote=false
   ```

1. Make a representative SDX connection request. Confirm that its signed
   `X-Edge-Token` uses the new `kid` and that the peer verifies it
   successfully.

1. Wait through the verifier grace period after the rollout so requests
   signed with the outgoing key can finish. Remove each outgoing `kid`,
   keeping the new `kid`:

   ```sh
   restish sdx provision-config-from-pattern \
     "${ORG}" sdx-keys.r1 \
     --action apply \
     "parameters:{
       operation: delete,
       targetKid: \"<OUTGOING_KID>\",
       runtimeGroupName: ${EDGE_ID},
       environment: ${ENV}
     }"
   ```

1. Confirm that JWKS contains the new `kid` and no retired `kid`, then remove
   the local token and public-certificate files:

   ```sh
   rm -f rotation-token tls-next.crt
   ```

The equivalent API request to publish the replacement certificate is:

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

To remove an outgoing key, send `action=apply` with:

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
    JWKS, so verification continues.

    If restart happens before the new public key is published, signing is
    denied because the mounted private key has no matching `kid`. Publish
    the staged certificate with `operation=rotate` or idempotent
    `operation=add`, wait for Gateway configuration to propagate, and test
    signing again.

    To abandon a staged key before promote, delete
    `${EDGE_RESOURCE}-client-next`. If its public key was published, remove
    that `kid` with `operation=delete`. Leave the live Secrets unchanged.

    After promote, restore both live Secrets from the secure backup, restart
    Kong, and confirm that signing uses the previous `kid`. Remove the new
    `kid` only after verifiers no longer receive traffic signed with it.

### Decommission runtime group

> To be documented..

Steps to decommission:

- uninstall infrastructure
- remove default routes
- remove keys (`sdx-keys.r1` with query `action=delete` and no `operation`
  removes the entire key qualifier)
- delete runtime group

## Next steps

- [Setup Organization Signing](/how-to/sdx-org-signing.md)
