---
order: 2600
---

# Create a GatewayService
 
> **Declarative Config:** DecK is used to sync your configuration with Kong; see https://docs.konghq.com/deck/overview/ for more information.

> **Splitting Your Config:** A namespace `tag` with the format `ns.$NS` is mandatory for each service/route/plugin. But, if you have separate pipelines for your environments (i.e., dev, test and prod), you can split your configuration and update the `tags` with the qualifier. For example, you can use a tag `ns.$NS.dev` to sync the Kong configuration for `dev` Service and Routes only.

## Plugins

> To view common plugin configuration go to [Common Controls](../gateway/COMMON-CONFIG.md)

> To learn about other available plugins, navigate to `Gateway > Plugins` on the sidebar of this page.

## Private Routing

By default, publically available endpoints are created based on Kong Routes where the hosts must end with `*.api.gov.bc.ca` or `*.apps.gov.bc.ca`.

There are use cases where the clients that are consuming the API are on the same Openshift platform that the API is deployed to. In this case, there is a security benefit of not making the API endpoints publicly available.

To support this, the route `hosts` can be updated with a host that follows the format: `<api-name>.cluster.local`. When the configuration is published to Kong, an Openshift Service is created with a corresponding Service Serving Certificate (SSC), which is routeable from within the Openshift cluster.

An example Gateway configuration for an upstream API deployed in the Silver cluster would be:

```yaml
services:
  - name: my-service
    host: httpbin.org
    tags: [ns.$NS]
    port: 443
    protocol: https
    retries: 0
    routes:
      - name: my-service-route
        tags: [ns.$NS]
        hosts:
          - <MYSERVICE>.cluster.local
```

A new service endpoint with SSL termination (using Service Serving Certificates) is then created in the APS project space for the given Openshift cluster, with the following format:

| Cluster     | Endpoint                                               |
| ----------- | ------------------------------------------------------ |
| Silver TEST | `https://gw-<MYSERVICE>.264e6f-test.svc.cluster.local` |
| Silver PROD | `https://gw-<MYSERVICE>.264e6f-prod.svc.cluster.local` |
| Gold TEST   | `https://gw-<MYSERVICE>.b8840c-test.svc.cluster.local` |
| Gold PROD   | `https://gw-<MYSERVICE>.b8840c-prod.svc.cluster.local` |

To verify that the endpoint is callable, you can deploy a simple pod that mounts the `service-ca` to be used for verifying the SSC.

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

From the Pod's Terminal, you can then run:

```bash
curl -v --cacert /config/service-ca.crt \
  https://gw-my-service.264e6f-prod.svc.cluster.local/uuid
```

You should see a 200 response with a valid UUID.

## Using an OpenAPI Spec

With version 2 of the GWA CLI, the OpenAPI to Kong configuration generator has been removed from the CLI and is now recommended to use Kong's `deck` command line.

Reference: https://docs.konghq.com/deck/latest/

Follow the installation instructions here: https://docs.konghq.com/deck/latest/installation/

Below is an example of a simple OpenAPI spec that we will use to generate a Kong configuration file.

```yaml
openapi: 3.0.1
info:
  version: "1.0-oas3"
  title: httpbin
  description: An unofficial OpenAPI definition for [httpbin.org](https://httpbin.org).
  license:
    name: blah license
    url: https://somelicense.com

servers:
  - url: https://httpbin.org

tags:
  - name: HTTP methods
    description: Operations for testing different HTTP methods

externalDocs:
  url: http://httpbin.org/legacy

security: []

paths:
  /headers:
    get:
      operationId: get-heaers
      summary: Returns the request headers.
      responses:
        "4XX":
          description: Ooops something went wrong
        "200":
          description: OK
          content:
            application/json:
              schema:
                type: object
                properties:
                  headers:
                    type: object
                    additionalProperties:
                      type: string
                required:
                  - headers
```

Add the following Kong specific metadata to the end of your OpenAPI spec,
substituting a unique service subdomain for your API which will be part of your vanity URL: <MYSERVICE>.api.gov.bc.ca.

```yaml
x-kong-name: <MY-SERVICE>

x-kong-route-defaults:
  hosts:
    - <MY-SERVICE>.api.gov.bc.ca
```

Save to `openapi.yaml`.

**Generate Kong Configuration:**

Run the following command, substituting your API Services Portal Namespace in the `--select-tag` option:

```shell linenums="0"
deck file openapi2kong -s openapi.yaml -o gw.yaml --select-tag ns.<GW-NAMESPACE>
```

**Publish to the API Services Portal:**

```shell linenums="0"
gwa publish-gateway gw.yaml
```
