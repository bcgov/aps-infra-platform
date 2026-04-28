---
title: "Connecting a Service"
---

This page shows how to make a connection between your system
and another on the Secure Data Exchange.

The steps described in this page are performed by the following roles:

| Role         | Function                                                                   |
| ------------ | -------------------------------------------------------------------------- |
| System Owner | Manage systems and service catalog entries for the particular organization |

Use cases:

- Request access (as consumer)
- Approve access (as provider)
- Open a connection
  - Consumer side
  - Provider side

## Prerequisites

- [Install Restish CLI](/reference/restish-cli.md)

## Request access (as consumer)

=== "Restish CLI"

    Help information about the operation:

    ```sh
    restish sdx upsert-connection
    ```

    Example call:

    ```sh
    restish sdx upsert-connection \
      ministry-of-citz \
      clientId: LAB.MIN.CITZ.MY-SUBSYSTEM, \
      serviceId: LAB.MIN.CITZ.SERVICE-A.v1
    ```

## Approve access (as provider)

=== "Restish CLI"

    Help information about the operation:

    ```sh
    restish sdx upsert-connection
    ```

    Example call:

    ```sh
    restish sdx upsert-connection \
      ministry-of-citz \
      clientId: LAB.MIN.CITZ.MY-SUBSYSTEM, \
      serviceId: LAB.MIN.CITZ.SERVICE-A.v1, \
      isApproved: true
    ```

## Open a connection

Once the connection request has been approved, both sides are able to publish the
routing rules for opening a channel between the two systems.

### Consumer-side

=== "Restish CLI"

    Help information about the operation:

    ```sh
    restish sdx generate-config-from-pattern
    ```

    Prepare a pattern input file (`pattern-input.json`) for the Consumer:

    ```json
    {
      "pattern": "sdx-p2p-consumer.r1",
      "parameters": {
        "conn_id": "1",
        "client_id": "LAB.MIN.CITZ.MY-SUBSYSTEM",
        "service_id": "LAB.MIN.CITZ.SERVICE-A.v1",
        "upgrades": {
          "sign": {}
        }
      }
    }
    ```

    Example call:

    ```sh
    restish sdx generate-config-from-pattern \
      ministry-of-citz \
      --action apply \
      --dry-run < pattern-input.json
    ```

=== "Reference"

    - **API** `PUT /organizations/{org}/pattern?action=apply&dryRun=true`

    Parameters:

    - `{org}=<your-organization>`
    - values for `action`: `preview` and `apply`

    For `action=apply` you can specify `dryRun=true` if you want to see what changes
    will be applied without the changes actually being made.

    Gateway Pattern: `sdx-p2p-consumer.r1`

    | Parameter    | Description                                                                                |
    | ------------ | ------------------------------------------------------------------------------------------ |
    | `conn_id`    | Unique identifier for the connection|
    | `client_id`  | Client identifier for authentication                                                       |
    | `service_id` | Service identifier being connected                                                         |
    | `upgrades`   | Optional set of controls that can be added to the routing                                  |

    Example:

    ```json
    {
      "pattern": "sdx-p2p-consumer.r1",
      "parameters": {
        "conn_id": "001",
        "client_id": "LAB.MIN.CITZ.SDG",
        "service_id": "LAB.MIN.SDPR.CASE-MANAGEMENT.v1",
        "upgrades": {}
      }
    }
    ```

Available upgrades for the `sdx-p2p-consumer.r1` pattern:

```json
{
  "sign": {},
  "verify": {}
}
```

### Provider-side

=== "Restish CLI"

    Help information about the operation:

    ```sh
    restish sdx generate-config-from-pattern
    ```

    Prepare a pattern input file (`pattern-input.json`) for the Provider:

    ```json
    {
      "pattern": "sdx-p2p-provider.r1",
      "parameters": {
        "conn_id": "1",
        "client_id": "LAB.MIN.CITZ.MY-SUBSYSTEM",
        "service_id": "LAB.MIN.CITZ.SERVICE-A.v1",
        "upstream_url": "https://my-upstream-endpoint.domain",
        "upgrades": {
          "sign": {}
        }
      }
    }
    ```

    Example call:

    ```sh
    restish sdx generate-config-from-pattern \
      ministry-of-citz \
      --action apply \
      --dry-run < pattern-input.json
    ```

=== "Reference"

    - **API** `PUT /organizations/{org}/pattern?action=apply&dryRun=true`

    Parameters:

    - `{org}=<your-organization>`
    - values for `action`: `preview` and `apply`

    For `action=apply` you can specify `dryRun=true` if you want to see what changes
    will be applied without the changes actually being made.

    Gateway Pattern: `sdx-p2p-provider.r1`

    | Parameter      | Description                                               |
    | -------------- | ------------------------------------------------------------------------------------------ |
    | `conn_id`      | Unique identifier for the connection |
    | `client_id`    | Client identifier for authentication                                                       |
    | `service_id`   | Service identifier being connected                                                         |
    | `upstream_url` | The upstream service implementation endpoint                                               |
    | `upgrades`     | Optional set of controls that can be added to the routing                                  |

    Example:

    ```json
    {
      "pattern": "sdx-p2p-provider.r1",
      "parameters": {
        "conn_id": "001",
        "client_id": "LAB.MIN.CITZ.SDG",
        "service_id": "LAB.MIN.SDPR.CASE-MANAGEMENT.v1",
        "upstream_url": "http://<ocp_service>.<ocp_namespace>.svc",
        "upgrades": {}
      }
    }
    ```

Available upgrades for the `sdx-p2p-provider.r1` pattern:

```json
{
  "sign": {},
  "verify": {},
  "token_exchange": {
    "token_endpoint": "",
    "client_id": "",
    "scopes": "",
    "audience": ""
  }
}
```
