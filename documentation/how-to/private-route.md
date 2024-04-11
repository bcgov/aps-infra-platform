---
title: Configure a Private Route
---

<!-- overview -->

By default, publicly available endpoints are created based on Kong Routes where
the hosts must end with `*.api.gov.bc.ca` or `*.apps.gov.bc.ca`.

There are use cases where the clients that are consuming the API are on the same
OpenShift platform that the API is deployed to. In this case, there is a security
benefit of not making the API endpoints publicly available by using a private route.

This page shows how to configure a private route for a service.

## Before you begin

- [Install gwa CLI](/how-to/gwa-install.md)
- [Create a Namespace](/resources/gwa-commands.md#namespacecreate)
- [Create a GatewayService](/how-to/create-gateway-service.md)

## Submit a request with APS

Reach out to the APS team on Rocket.Chat in the
[#aps-ops](https://chat.developer.gov.bc.ca/channel/aps-ops) channel or [open a
support
ticket](https://dpdd.atlassian.net/servicedesk/customer/portal/1/group/2) to get
permission to create a local cluster route.

## Configure the route

The route `hosts` can be updated with a host that follows the
format: `<api-name>.cluster.local`. When the configuration is published to Kong,
an OpenShift Service is created with a corresponding Service Serving Certificate
(SSC), which is routeable from within the OpenShift cluster.

An example GatewayService configuration for an upstream API deployed in the Silver cluster would be:

```yaml
services:
  - name: <MY-SERVICE>
    host: httpbin.org
    tags: [ns.$NS]
    port: 443
    protocol: https
    retries: 0
    routes:
      - name: <MY-SERVICE-ROUTE>
        tags: [ns.$NS]
        hosts:
          - <MY-SERVICE>.cluster.local
```

A new service endpoint with SSL termination (using Service Serving Certificates)
is then created in the APS project space for the given OpenShift cluster, with
the following format:

| Cluster     | Endpoint                                               |
| ----------- | ------------------------------------------------------ |
| Silver TEST | `https://gw-<MY-SERVICE>.264e6f-test.svc.cluster.local` |
| Silver PROD | `https://gw-<MY-SERVICE>.264e6f-prod.svc.cluster.local` |
| Gold TEST   | `https://gw-<MY-SERVICE>.b8840c-test.svc.cluster.local` |
| Gold PROD   | `https://gw-<MY-SERVICE>.b8840c-prod.svc.cluster.local` |

The route can be viewed by running `gwa status --json` and looking at the value of `env_host`.

## Validation

To verify that the endpoint is callable, you can deploy a simple pod that mounts
the `service-ca` to be used for verifying the SSC.

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: tmp-ca
  annotations:
    service.beta.openshift.io/inject-cabundle: "true"
data: {}
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: tmp-deployment
  labels:
    app: sleeper
spec:
  replicas: 1
  selector:
    matchLabels:
      app: sleeper
  template:
    metadata:
      labels:
        app: sleeper
    spec:
      volumes:
        - name: config
          configMap:
            name: tmp-ca

      containers:
        - name: idle
          image: docker.io/curlimages/curl:latest
          command: ["sh"]
          args:
            - -c
            - |
              sleep Infinite
          ports:
            - containerPort: 80
          volumeMounts:
            - name: config
              mountPath: "/config"
              readOnly: true
```

From the Pod's Terminal, you can then a `curl` command against your service:

```bash
curl -v --cacert /config/service-ca.crt \
  https://gw-<MY-SERVICE>.<APS-CLUSTER>.svc.cluster.local/uuid
```

You should see a 200 response including a UUID, if using the `httpbin.org`
upstream host as shown in the example GatewayService.
