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

| Role                   | Function                                                                                  |
| ---------------------- | ----------------------------------------------------------------------------------------- |
| System Admin           | Request a runtime group, publish its routes, and publish and retire its public keys      |
| Runtime group operator | Deploy the edge, prepare a replacement certificate, and restart the edge                 |

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

    ```

=== "Reference"

    - **API** `POST /organizations/{org}/runtime-groups/{name}/environments/{environment}/tokens`

    Parameters:

    - `{org}=<your-organization>`
    - `{name}=<your-runtime-group-name>`
    - `{environment}=<target-environment>`

The response includes a one-time token. Send that token to the runtime group
operator with the runtime group name and the IP address from `sdxEndpoint`.
The operator uses it to deploy the edge. Do not reuse a token that has
already been spent.

### Deploy the runtime group infrastructure

The runtime group operator deploys the edge after you send the certificate
signing token. If that deployment is not possible in your infrastructure,
contact the APS team.

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
Replace the host with the runtime group domain and the IP with the address
from `sdxEndpoint`.

```sh
curl -v -k --resolve <runtime-group-host>:443:<ip> \
  https://<runtime-group-host>
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

Ask the runtime group operator for the edge public certificate and save it
as `tls.crt`. Publish only that public certificate. Do not publish the
private key.

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

The runtime group operator must not restart the edge with the new private
key until the rotate `apply` has succeeded. If the edge starts signing with
a key that is not yet in JWKS, verification denies the requests.

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

The runtime group operator prepares the new edge certificate and restarts
the edge. You publish and retire the public keys.

Follow these steps for an overlap rotation:

1. Request a new one-time certificate signing token, the same way as in
   [Request a one-time-use certificate signing token](#request-a-one-time-use-certificate-signing-token).
   Send the token to the runtime group operator. Ask the operator to prepare
   the new certificate without restarting the edge, and to send you the new
   public certificate. Save that certificate as `tls-next.crt`.

1. Publish the new public certificate while retaining the existing keys:

   ```sh
   restish sdx provision-config-from-pattern \
     my-org sdx-keys.r1 \
     --action apply \
     'parameters:{
       operation: rotate,
       certificatePem[0]: @tls-next.crt,
       runtimeGroupName: newrg,
       environment: lab
     }'
   ```

   `operation=rotate` returns `422` if the same public key is already in the
   key set. Use `operation=add` when you need to publish a key that is
   already in the set.

1. Record the new `kid` from `changes.added` and every outgoing `kid` from
   `changes.retained`. Find the JWKS URL in the `details.endpoint` field of
   the response's `info` result. Confirm that the JWKS contains both the new
   and outgoing `kid` values.

1. Wait at least 300 seconds after publishing the new key.
   `trust-verify-signature` reloads a cached key set after a missing `kid`
   only when that cache is older than `iss_key_grace_period`. In the SDX
   patterns that period is 300 seconds. Waiting before the edge restarts
   keeps a verifier that cached only the old key from rejecting the new
   `kid`.

1. Ask the runtime group operator to switch the edge to the new certificate
   and restart it. The operator should do this only after the rotate `apply`
   has succeeded and the wait above has elapsed.

1. Ask the runtime group operator to confirm that the edge certificate is
   the public certificate you published. Make a representative SDX connection
   request and confirm that the peer accepts it. The `kid` in a signed
   `X-Edge-Token` is the new `kid` from `changes.added`.

1. Wait another 300 seconds so requests signed with the outgoing key can
   finish. Remove each outgoing `kid`, keeping the new `kid`:

   ```sh
   restish sdx provision-config-from-pattern \
     my-org sdx-keys.r1 \
     --action apply \
     'parameters:{
       operation: delete,
       targetKid: "urn:ca:bc:sdx:edge:newrg:lab:8875a149",
       runtimeGroupName: newrg,
       environment: lab
     }'
   ```

1. Confirm that JWKS contains the new `kid` and no retired `kid`. Delete the
   local copy of the public certificate.

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

    If rotate `apply` succeeds and the edge has not restarted, traffic still
    signs with the old private key and old `kid`. Both public keys are in
    JWKS, so verification continues.

    If the edge restarts before the new public key is published, signing is
    denied because the new private key has no matching `kid`. Publish the
    new certificate with `operation=rotate`, or with `operation=add` if that
    certificate is already in the set. Wait for the gateway configuration to
    propagate, then test signing again.

    To abandon a new certificate before the edge switches to it, ask the
    runtime group operator to discard it. If you already published that
    public key, remove its `kid` with `operation=delete`.

    After the edge has switched, ask the runtime group operator to restore
    the previous certificate and restart. Remove the new `kid` only after
    verifiers no longer receive traffic signed with it.

### Decommission runtime group

> To be documented..

Steps to decommission:

- runtime group operator uninstalls the edge
- remove default routes
- remove keys (`sdx-keys.r1` with query `action=delete` and no `operation`
  removes the entire key qualifier)
- delete runtime group

## Next steps

- [Setup Organization Signing](/how-to/sdx-org-signing.md)
