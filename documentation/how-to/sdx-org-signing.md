---
title: "Setup Organization Signing"
---

Organization signing is used to cryptographically verify that messages were transmitted
with permission between the involved systems.

Before systems can make connections, the organization must register signing keys
with the Runtime Group that their systems are using to connect to SDX.

| Role               | Function                             |
| ------------------ | ------------------------------------ |
| Organization Admin | Manage organization keys for signing |

Use cases:

- Request a new signing key CSR
- Get the CSR signed by an approved Certificate Authority
- Register CA signed certificate

## Prerequisites

- [Install Restish CLI](/reference/restish-cli.md)

## Request a new signing key CSR

=== "Restish CLI"

    Help information about the operation:

    ```sh
    restish sdx create-new-key
    ```

    Example call:

    ```sh
    restish sdx create-new-key \
      ministry-of-citz \
      runtimeGroupName: TARGET-RUNTIME-GROUP-NAME
    ```

## Get the CSR signed by an approved Certificate Authority

SDX Operator provides a Certificate Authority (CA).

Reach out to the APS team with your CSR to get it reviewed, approved and signed.

## Register CA signed certificate

Once you receive back the certificate, save the certificate
(and its intermediate CAs) in a `new.crt` file, and the root
certificate for the CA in `root.crt`.

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
      'pattern:sdx-keys.r1, parameters:{ certificate_pem[0]: @new.crt, ca_certs: @root.crt }'
    ```
