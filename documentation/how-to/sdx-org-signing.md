---
title: "Setup Organization Signing"
---

Organization signing is used to cryptographically verify that messages were transmitted
with permission between the involved systems using an authorized Runtime Group.

!!! note "Setup is Optional"

    There are various upgrades related to the connection that can be enabled.
    Performing the counter-sign using the organization keys is one of these upgrades.
    See [Connection Resources](/how-to/sdx-connection-resources.md) for more information.

    If policy requires this to be enabled, then follow the steps to setup organization
    signing. The organization must register signing keys
    with the Runtime Group that their systems are using to connect to SDX.

| Role               | Function                             |
| ------------------ | ------------------------------------ |
| Organization Admin | Manage organization keys for signing |

Use cases:

- Request a new signing key CSR
- Get the CSR signed by an approved Certificate Authority
- Add CA signed certificate to registry

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
      my-org \
      environment: lab, runtimeGroupName: newrg
    ```

The inputs for the CSR will be derived from your organization details and the
runtime group you are registering it on.

You will get back a document in YAML format similar to this:

```yaml
signing_algorithm: ECDSA_SHA_512
csr: |
  -----BEGIN CERTIFICATE REQUEST-----
  MIIBWTCB/wIBADBgMQswCQYDVQQGEwJDQTFCMEAGA1UECgw5TWluaXN0cnkgb2Yg
  Q2l0aXplbnMgU2VydmljZXMvc2VyaWFsTnVtYmVyPUxBQi9NSU4vU0hBUkUwMQ0w
  CwYDVQQDDARDSVRaMFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEyqHYa+yG6YGE
  y1fR1gUEaRzhbe3REt1OBC6F9JDstvROUuYBaKYZJbXZ6wQ8q+bwDRzlcGv1Bc/k
  a73T0xd7XqA9MDsGCSqGSIb3DQEJDjEuMCwwKgYDVR0RBCMwIYIfbGFiLW1pbi1j
  aXR6LnNoYXJlMC5zZXJ2ZXJzLnNkeDAKBggqhkjOPQQDAgNJADBGAiEA2VFX1pKP
  OFYl+JNux0Xz+E1CLeCnK9Acy3pJH4e/cmACIQDiOq/xxg598GYBQOc+gQtiCsPL
  ubWazfkHoChChFcX1g==
  -----END CERTIFICATE REQUEST-----
jwk: '{"y":"TlLmAWimGSW12esEPKvm8A0c5XBr9QXP5Gu909MXe14","kid":"RYDlAYlWr184FTwRk21jQzvZSO3UOwoqRKN5lHLe9zE","crv":"P-256","x":"yqHYa-yG6YGEy1fR1gUEaRzhbe3REt1OBC6F9JDstvQ","kty":"EC"}'
pub_key: |
  -----BEGIN PUBLIC KEY-----
  MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEyqHYa+yG6YGEy1fR1gUEaRzhbe3R
  Et1OBC6F9JDstvROUuYBaKYZJbXZ6wQ8q+bwDRzlcGv1Bc/ka73T0xd7Xg==
  -----END PUBLIC KEY-----
inputs:
  org_name: Ministry of Citizens Services
  requester_name: unknown
  serial_number: LAB/MIN/SHARE0
  requester_email: unknown
  san: lab-min-citz.share0.servers.sdx
  country: CA
  common_name: CITZ
```

## Get the CSR signed by an approved Certificate Authority

SDX Operator provides a Certificate Authority (CA).

Reach out to the APS team with your CSR to get it reviewed, approved and signed.

## Add CA signed certificate to registry

Once you receive back the certificate, save the certificate
(and its intermediate CAs) in a `new.crt` file, and the root
certificate for the CA in `root.crt`.

Use one of the root certificates from below depending on your environment.

For details about environments, visit [SDX Environments](/reference/sdx/environments.md).

### Playground

```text
-----BEGIN CERTIFICATE-----
MIIBqjCCAVCgAwIBAgIRAOx+wUXYgyRY9VGzArB7V+swCgYIKoZIzj0EAwIwMzEx
MC8GA1UEAxMoQ1NCQyBTZWN1cmUgRGF0YSBFeGNoYW5nZSBBUFNUU1QgUm9vdCBD
QTAeFw0yNjA3MTYxNTE4MzBaFw0zNjA3MTMxNTE4MzBaMDMxMTAvBgNVBAMTKENT
QkMgU2VjdXJlIERhdGEgRXhjaGFuZ2UgQVBTVFNUIFJvb3QgQ0EwWTATBgcqhkjO
PQIBBggqhkjOPQMBBwNCAAQceMa6kWDVEqVnG9wZwD7zn3y67LGIcE8lBiQTzxRR
h5LdqhryGnKIOsUMMujvFUTsuUsaG9KywMh/NuTMkaLMo0UwQzAOBgNVHQ8BAf8E
BAMCAQYwEgYDVR0TAQH/BAgwBgEB/wIBAjAdBgNVHQ4EFgQUnbOhKEgO1Xkv1zeZ
zCXusaEzQHEwCgYIKoZIzj0EAwIDSAAwRQIhAPue7wdiw/MocolfSBGZgEp4VO3Q
5Ws2v0C/BBrWI+UTAiAqNqJxusfbu3t0VXjTNg4Z/+uH+bGIQgIMpasQamFQSQ==
-----END CERTIFICATE-----
```

### Staging

```text
-----BEGIN CERTIFICATE-----
MIIBozCCAUqgAwIBAgIRAOqrFxwuBQzATeE2ybv4ci8wCgYIKoZIzj0EAwIwMDEu
MCwGA1UEAxMlQ1NCQyBTZWN1cmUgRGF0YSBFeGNoYW5nZSBERVYgUm9vdCBDQTAe
Fw0yNjAzMjEyMDE2MDFaFw0zNjAzMTgyMDE2MDFaMDAxLjAsBgNVBAMTJUNTQkMg
U2VjdXJlIERhdGEgRXhjaGFuZ2UgREVWIFJvb3QgQ0EwWTATBgcqhkjOPQIBBggq
hkjOPQMBBwNCAASkZrREActpsjEdst6vKcQmxEeO6OuVnoBQ7luxWymcSosJJCHD
WEV/2e9EyGPLHpw5RstPgx+Ha5D6+BcKGzjio0UwQzAOBgNVHQ8BAf8EBAMCAQYw
EgYDVR0TAQH/BAgwBgEB/wIBAjAdBgNVHQ4EFgQUYb2Jz7MuAOKY8bu9NM6tjvS6
xkYwCgYIKoZIzj0EAwIDRwAwRAIgTFXSb8bq5Z8P8oICO3BVHkHxCm0GRcqL10TL
GtlsuWYCIBPfZrhbZX4oFhEk0sq7HXlBJuh6Zaa6dcsO3RIUt1Gm
-----END CERTIFICATE-----
```

### Non-Prod

```text
-----BEGIN CERTIFICATE-----
MIIBpTCCAUugAwIBAgIQBYjl1y/VB9YWcN4ix0J9/jAKBggqhkjOPQQDAjAxMS8w
LQYDVQQDEyZDU0JDIFNlY3VyZSBEYXRhIEV4Y2hhbmdlIFRFU1QgUm9vdCBDQTAe
Fw0yNjA3MTcyMTM5MTBaFw0zNjA3MTQyMTM5MTBaMDExLzAtBgNVBAMTJkNTQkMg
U2VjdXJlIERhdGEgRXhjaGFuZ2UgVEVTVCBSb290IENBMFkwEwYHKoZIzj0CAQYI
KoZIzj0DAQcDQgAEDGVAeDHUrLvBGxuZP7PS/Z8c1RZBb4z8+S7qRySm8VQO6Qt9
X9VTps3N8rXSk1LO15ELWT0WbWBAfOxi0om5MaNFMEMwDgYDVR0PAQH/BAQDAgEG
MBIGA1UdEwEB/wQIMAYBAf8CAQIwHQYDVR0OBBYEFAyGhiqDdh67pQepVugBJ35P
zupYMAoGCCqGSM49BAMCA0gAMEUCIQC0Z98oClh1Ngi63m9Jwvib4GUcfP7b894o
MGzh5gHWSAIgHZw/p+dnqJiq/ukUIUWrWxTuNmuvgIYG+/HscgaV+yM=
-----END CERTIFICATE-----
```

### Prod

```text
-----BEGIN CERTIFICATE-----
MIIBpjCCAUygAwIBAgIRAMJMz93KjTyWx4EVe4SLeAEwCgYIKoZIzj0EAwIwMTEv
MC0GA1UEAxMmQ1NCQyBTZWN1cmUgRGF0YSBFeGNoYW5nZSBQUk9EIFJvb3QgQ0Ew
HhcNMjYwNzIxMjIzMzAzWhcNMzYwNzE4MjIzMzAzWjAxMS8wLQYDVQQDEyZDU0JD
IFNlY3VyZSBEYXRhIEV4Y2hhbmdlIFBST0QgUm9vdCBDQTBZMBMGByqGSM49AgEG
CCqGSM49AwEHA0IABNj3iloPdVoyfNAFAodzvf7Fcz4Pm8l2fYxeP9hZdA8wpk2J
nOmK9hlgburDu3ehXREbEnZmDClxqhcwC/bfSxSjRTBDMA4GA1UdDwEB/wQEAwIB
BjASBgNVHRMBAf8ECDAGAQH/AgECMB0GA1UdDgQWBBTNtqkvHMI2ZafMGoKv+NQy
jIx4XDAKBggqhkjOPQQDAgNIADBFAiAFg+IddYG6zgqalUXVxT+PDfBgI/Jns2Mc
jS6ocTR5cwIhAKl/0ak7GhWLPSbpKxR7woOz+Qe7CzPsjgidM8+SFH5d
-----END CERTIFICATE-----
```

You will then be able to use this information to update the
public key details with the new certificate in the JWKS registry.

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
      'parameters:{ environment: lab, certificatePem[0]: @new.crt, caCerts: @root.crt }'
    ```
