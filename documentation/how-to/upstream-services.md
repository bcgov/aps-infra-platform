---
title: Set Up an Upstream Service
---

## Upstream Services on OCP

We have Kong Data Planes running on Platform Service's Silver and Gold Private
OpenShift clusters. If your upstream services run on one of these clusters, then
you will need to configuration the network polices to allow access from the API
Gateway.

Additionally, you can set up [private routing](/how-to/private-route.md) to
limit consumer access to that cluster.

### Network Policies

> If your service is running on the OpenShift platform, you should specify the Kubernetes Service in the `Service.host`. It must have the format: `<name>.<ocp-namespace>.svc`. Also, make sure your `Service.port` matches your Kubernetes Service Port. Any Security Policies for egress from the Gateway will be setup automatically on the API Gateway side.

The Kong Gateway runs Data Planes in both Silver and Gold clusters.

**Silver Cluster**

You will need to create a Network Policy on your side similar to the following to allow the Gateway's test and prod environments to route traffic to your API:

```yaml
kind: NetworkPolicy
apiVersion: networking.k8s.io/v1
metadata:
  name: allow-traffic-from-gateway-to-your-api
spec:
  podSelector:
    matchLabels:
      name: my-upstream-api
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              environment: test
              name: 264e6f
    - from:
        - namespaceSelector:
            matchLabels:
              environment: prod
              name: 264e6f
```

**Gold Cluster**

If your service is running on Gold, you will need to contact the APS team so that we can properly provision the `namespace` on the correct Kong Data Plane and ensure the correct DNS is setup for your routes. The following is the Network Policy on Gold.

```yaml
kind: NetworkPolicy
apiVersion: networking.k8s.io/v1
metadata:
  name: allow-traffic-from-gateway-to-your-api
spec:
  podSelector:
    matchLabels:
      name: my-upstream-api
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              environment: test
              name: b8840c
    - from:
        - namespaceSelector:
            matchLabels:
              environment: prod
              name: b8840c
```

## Upstream Services with mTLS

> **Require mTLS between the Gateway and your Upstream Service?** To support mTLS on your Upstream Service, you will need to provide client certificate details and if you want to verify the upstream endpoint then the `ca_certificates` and `tls_verify` is required as well. Example:

```yaml
services:
  - name: my-upstream-service
    host: my-upstream.site
    tags: [_NS_]
    port: 443
    protocol: https
    tls_verify: true
    ca_certificates: [0a780ee0-626c-11eb-ae93-0242ac130012]
    client_certificate: 8fc131ef-9752-43a4-ba70-eb10ba442d4e
    routes: [...]
certificates:
  - cert: "<PEM FORMAT>"
    key: "<PEM FORMAT>"
    tags: [_NS_]
    id: 8fc131ef-9752-43a4-ba70-eb10ba442d4e
```

> NOTE: `ca_certificates` (Root CAs) must be installed by the `APS` team - please reach out to us on Rocket.Chat `#aps-ops` to request setup of your Root CA.  A `ca_certificates` `UUID` will be provided to you, to add to your `services` details.

> NOTE: You must generate a UUID (`python -c 'import uuid; print(uuid.uuid4())'`) for each certificate you create (set the `id`) and reference it in your `services` details.

> HELPER: Python command to get a PEM file on one line: `python -c 'import sys; import json; print(json.dumps(open(sys.argv[1]).read()))' my.pem`
