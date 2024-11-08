---
title: Set Up an Upstream Service
---

## Upstream Services on OpenShift

API Program Services (APS) has Kong data planes running on the Silver, Gold, and
Emerald clusters of the BC Government Private Cloud OpenShift platform. 

If your upstream services run on one of these clusters, then you will need to configure
the network policies to allow access from the API Gateway.

By default, new Gateways are created on the Silver cluster. Traffic to Gateway
Services in a Silver Gateway is routed through the Kong data plane and routes on
the Silver Openshift cluster. Alternatively, a Gateway can be created on (or
migrated to) the Gold or Emerald clusters to support upstream services on these
clusters - see [Gold and Emerald Gateways](#gold-and-emerald-gateways) below 
for additional details.

Regardless of the cluster chosen, you will need to configure the Gateway to
point to your service and a network policy will need to be created to allow
traffic to the service from the Gateway.

Additionally, you can set up [private routing](/how-to/private-route.md) to
limit consumer access to that cluster.

### Service configuration

Specify the OpenShift/Kubernetes service in your [Gateway Service configuration](concepts/gateway-config.md)
using the following format:

```yaml
kind: GatewayService
name: example-service-dev
tags: [ ns.<gatewayId> ]
host: <ocp-service-name>.<ocp-namespace>.svc
port: <ocp-service-port>
protocol: http
routes:
  ...
```

!!! note "DataClass tags for Emerald Gateways"
    Emerald Gateway Services must include a DataClass tag (`aps.route.dataclass.<data-class>`).
    This tag should be included in the `tags` field of the Service and will be applied to all Routes created for the Service.
    Acceptable values for `<data-class>` are: `low`, `medium`, and `high`.
    
    For more information on the Emerald cluster and security classifications, see the
    [Guide for Emerald teams](https://digital.gov.bc.ca/cloud/services/private/internal-resources/emerald/) 
    (IDIR-restricted) from Platform Services.

### Network policies

You will need to create a Network Policy on your side to allow the API Gateway to route traffic to your API.

Follow the template below based on the cluster you are using: 

!!! note "Namespace selector"
    Ensure you do not change the `namepsaceSelector` names - this is the APS namespace which hosts the API Gateway, not your namespace.

=== "Silver"

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

=== "Gold"

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

    !!! warning "Contact APS"
        If your service is running on the Gold cluster, you will need to [contact the APS team](README.md#need-a-hand)
        to have your Gateway provisioned on the correct Kong data plane 
        and to configure DNS for your routes. 

=== "Emerald"

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
                  name: cc9a8a
        - from:
            - namespaceSelector:
                matchLabels:
                  environment: prod
                  name: cc9a8a
    ```
    
    !!! warning "Contact APS"
        If your service is running on the Emerald cluster, you will need to [contact the APS team](README.md#need-a-hand)
        to have your Gateway provisioned on the correct Kong data plane 
        and to configure DNS for your routes. 

Any Security Policies for egress from the Gateway
will be setup automatically on the API Gateway side.

### Gold and Emerald Gateways

A Gateway can be created on (or migrated to) the Gold or Emerald clusters to
support upstream services on these clusters.

**Gold Gateways** route traffic through a data plane on the Gold cluster and support Disaster Recovery (DR) failover
to the Gold DR cluster in Calgary.

**Emerald Gateways** route traffic through a data plane on the Emerald cluster with `DataClass: Medium`. 
Emerald Gateways can route traffic to pods on the Emerald cluster which are 
otherwise inaccessible due to network restrictions.

If your service is running on the Gold or Emerald cluster, you will need to [contact the APS team](README.md#need-a-hand)
to have your Gateway provisioned on the correct Kong data plane and to configure DNS for your routes.

The process to create a Gateway on the Gold or Emerald clusters looks like this:

1. **API provider creates an empty Gateway**
  1. To migrate an existing Gateway, first clear the configuration by running `gwa pg` with a yaml file with: `services: []`
1. **API provider contacts APS team** to request a Gateway on the desired cluster
1. APS updates the Gateway to use the Kong data plane on the desired cluster
1. **API provider updates the Gateway configuration** (`GatewayService.host`) to point to Gold or Emerald service and advises the APS team when configuration is applied
  1. Carefully consider the Route hosts (`*.api.gov.bc.ca`) because a manual DNS update is required for any changes
  1. Emerald Gateway Services must include a DataClass tag (`aps.route.dataclass.<data-class>`)
1. APS updates DNS for the new Routes
1. **API provider updates [NetworkPolicies](#network-policies)** to allow traffic to the service from the approriate APS namespace
1. **API provider tests connectivity**

## Upstream Services with mTLS

Do you require mTLS between the API Gateway and your upstream service? 

To support mTLS on your Upstream Service, you will need to provide client
certificate details. If you want to verify the upstream endpoint the
`ca_certificates` and `tls_verify` is required as well. 

Example:

```yaml
services:
  - name: my-upstream-service
    host: my-upstream.site
    tags: [ns.<gatewayId>]
    port: 443
    protocol: https
    tls_verify: true
    ca_certificates: [0a780ee0-626c-11eb-ae93-0242ac130012]
    client_certificate: 8fc131ef-9752-43a4-ba70-eb10ba442d4e
    routes: [...]
certificates:
  - cert: "<PEM FORMAT>"
    key: "<PEM FORMAT>"
    tags: [ns.<gatewayId>]
    id: 8fc131ef-9752-43a4-ba70-eb10ba442d4e
```

!!! warning "Root CA installation"
    `ca_certificates` (Root CAs) must be installed by the APS team -
    please [contact the APS team](README.md#need-a-hand) to request setup of your Root
    CA.  A `ca_certificates` `UUID` will be provided to you, to add to your
    `services` details.

!!! warning "Certificate UUIDs"
    You must generate a UUID for each certificate you create. Here is a Python command to get a UUID:
    
    ```python linenums="0"
    python -c 'import uuid; print(uuid.uuid4())'
    ```
    
    Set the `id` and reference it in your `services` details (`services.client_certificate` and `certificate.id`).

!!! note "PEM file parsing"
    Here's a handyPython command to get a PEM file on one line:
    
    ```python linenums="0"
    python -c 'import sys; import json; print(json.dumps(open(sys.argv[1]).read()))'my.pem
    ```
