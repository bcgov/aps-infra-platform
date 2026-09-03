---
title: "Event Management"
---

This page shows how to publish an AsyncAPI service that can be used to publish messages
and for consumers to setup webhooks to receive messages.

!!! warning "Preview"

    This feature is in `preview` only, which means it is experimental.
    It is available in our `LAB` environment as is.

The steps described in this page are performed by the following roles:

| Role            | Function                                                   |
| --------------- | ---------------------------------------------------------- |
| Subsystem Owner | Subsystem-level role for managing services for a subsystem |

Use cases:

- Register an async service
- Configure a publisher endpoint
- Connecting a service
- Configure a webhook
- Publishing a message

## Prerequisites

- [Install Restish CLI](/reference/restish-cli.md)

## Register an async service

=== "Restish CLI"

    Help information about the operation:

    ```sh
    restish sdx upsert-oas-service
    ```

    Example:

    ```sh
    restish sdx upsert-oas-service \
      ministry-of-citz \
      --subsystem MY-NEW-SUBSYSTEM \
      --rsh-header "Content-Type: application/json" \
      < asyncapi.yaml
    ```

## Configure a publisher endpoint

This sets up a protected URL that can be used by the Resource Server to publish
messages on the topics described in the AsyncAPI.

=== "Restish CLI"

    Help information about the operation:

    ```sh
    restish sdx provision-config-from-pattern
    ```

    Example call:

    ```sh
    restish sdx provision-config-from-pattern \
      ministry-of-citz events-publisher.r1 \
      --action apply \
      parameters:{serviceId:"LAB.USR.ACOPE.HELLO-WORLD-APPLICATION.v0"}
    ```

    The output from this call will be a `publisher_url` that the Resource
    Server will be able to securely call to send messages.

## Connecting a service

With the async service published, clients can request access to the AsyncAPI service.

All the same security controls that are in place for OpenAPIs, are also available for AsyncAPIs.

The how to guide for making connections is at [Connecting a Service](/how-to/sdx-connections.md).

## Configure a webhook

Once a connection has been approved, the client is able to configure the webhook
details so that it can start to receive messages from the publisher.

=== "Restish CLI"

    Help information about the operation:

    ```sh
    restish sdx provision-config-from-pattern
    ```

    Example call:

    ```sh
    echo '
      {
        "pattern": "events-webhook.r1",
        "parameters": {
          "connId": "42",
          "clientId": "LAB.MIN.CITZ.SDG-FE",
          "serviceId": "LAB.USR.ACOPE.HELLO-WORLD-APPLICATION.v0",
          "webhookUrl": "https://bright-island-08.webhook.cool"
        }
      }' | \
    restish sdx provision-config-from-pattern \
      ministry-of-citz \
      --action apply
    ```

## Publishing a message

The RS published an AsyncAPI spec to state all the events it will publish.

The RS will use its local runtime group publisher endpoint to send a message.

The client authentication will use the same approach described in the
[SDX Data Access Protocol](/reference/sdx/data-access-protocol.md) document.

```sh
curl -v -H "Host:internal.share0.servers.sdx" \
  http://localhost:8000/sdx/1/815a243837865c1ed61e94c0/messages \
  -H "Content-Type: application/json" \
  -d '{"value":{"note":"return it!"}}'
```

The return, if successful, is a `202 Accepted`, payload:

```json
{
  "topicName": "Event-LAB.USR.ACOPE.HELLO-WORLD-APPLICATION.v0",
  "partition": 0,
  "errorCode": 0,
  "baseOffset": "0",
  "logAppendTime": "-1",
  "logStartOffset": "0"
}
```
