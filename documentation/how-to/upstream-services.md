---
title: Set Up an Upstream Service
---

## Upstream Services on OpenShift

API Program Services (APS) has Kong data planes running on the Silver, Gold, and
Emerald clusters of the BC Government Private Cloud OpenShift platform. API
providers must configure their upstream services to allow traffic from the
Kong data plane running on the same cluster as their services.

!!! warning "Services on Gold or Emerald? Contact APS"
    Before getting started with Gateway configuration, teams with upstream services
    running on Gold or Emerald clusters must [contact the APS team](/how-to/get-support.md).

    Start by creating a Gateway with [`gwa gateway create`](/reference/gwa-commands.md/#gatewaycreate),
    then contact APS with the new Gateway ID to have your Gateway configured for the
    appropriate cluster.

### Silver cluster

By default, new Gateways are created on the Silver cluster. Setting up a Gateway on Silver is completely self-serve.

The following steps are required to configure the Gateway for your API:

#### Service configuration

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

#### IP Addresses

Silver cluster route hosts will always resolve to `142.34.194.118` - silver's ingress IP.

#### Network policies

You will need to create a Network Policy on your side to allow the API Gateway to route traffic to your API.

Follow this template:

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

Where:

- `podSelector` is a selector that matches your upstream service.
- `namespaceSelector` is the APS namespace which hosts the API Gateway on Silver (`264e6f`), not your namespace. Don't change this.

#### DNS

If the consumers of your API are going to all be on the Silver cluster, you can consider setting up [private routing](/how-to/private-route.md) to limit consumer access using an Openshift Service.

### Gold cluster

Before you can create Gateway Services on the Gold cluster, you must
[contact the APS team](/how-to/get-support.md) to request that your Gateway be
configured for the Gold cluster Kong data plane.

Start by creating a Gateway with [`gwa gateway create`](/reference/gwa-commands.md/#gatewaycreate),
then contact APS with the new Gateway ID to have your Gateway configured before
continuing with your configuration.

The Gold cluster has some additional considerations related to DNS and the
expectations around when failover to Calgary (Gold DR) occurs, which are
explained below.

#### Service configuration

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

#### IP Addresses

Gold cluster route hosts will always resolve to `142.34.229.4` or `142.34.64.4`
depending on whether the APS service is in Gold (Kamloops) or for disaster
recovery in Gold DR (Calgary).

#### Network policies

You will need to create a Network Policy on your side to allow the API Gateway
to route traffic to your API.

Follow this template:

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

Where:

- `podSelector` is a selector that matches your upstream service.
- `namespaceSelector` is the APS namespace which hosts the API Gateway on Gold
  and Gold DR (`b8840c`), not your namespace. Don't change this.

#### DNS

By default the wildcard `*.api.gov.bc.ca` domain resolves to the Silver cluster
(`142.34.194.118`). For domains that will be routing to the Gold cluster, a
manual DNS entry must be setup by APS.

You will need to [contact the APS team](/how-to/get-support.md) to have your
Gateway provisioned for DNS. The information required will be the `Route.hosts`
endpoints that will be configured on your Gateway.

If the consumers of your API are going to all be on the Gold cluster, you can
consider setting up [private routing](/how-to/private-route.md) to limit
consumer access using an Openshift Service.

### Emerald cluster

Before you can create Gateway Services on the Emerald cluster, you must
[contact the APS team](/how-to/get-support.md) to request that your Gateway be
configured for the Emerald cluster Kong data plane.

Start by creating a Gateway with [`gwa gateway create`](/reference/gwa-commands.md/#gatewaycreate),
then contact APS with the new Gateway ID to have your Gateway configured before
continuing with your configuration.

The Emerald cluster has some additional considerations related to DataClass
tags, NetworkPolicies, and DNS, which are explained below.

#### Service configuration

Emerald Gateway Services must include a DataClass tag (`aps.route.dataclass.<data-class>`). Acceptable values for `<data-class>` are: `public`, `medium`, and `high`.

This tag should be included in the `tags` field of the Service and will be applied to all Routes created for the Service.

Here is an example Gateway Service with `medium` data class:

```yaml
kind: GatewayService
name: example-service-dev
tags: [ ns.<gatewayId>, aps.route.dataclass.medium ]
host: <ocp-service-name>.<ocp-namespace>.svc
port: <ocp-service-port>
protocol: http
routes:
  ...
```

For more information on the Emerald cluster and security classifications, see the
[Guide for Emerald teams](https://digital.gov.bc.ca/technology/cloud/private/internal-resources/emerald/) (IDIR-restricted) from Platform Services.

#### IP Addresses

Emerald cluster route hosts will be assigned an IP address depending on the data class that was specified in the Gateway Service.

[Contact the APS team](/how-to/get-support.md) to get the IP address for your routes. This IP address will not change for the route unless the data class changes.

#### Network policies for upstream

##### Services on Emerald cluster

For services on Emerald cluster, both `ingress` and `egress` Network Policies are required to connect the Kong gateway with your upstream service.

**Upstream ingress policy**: You will need to create an `ingress` Network Policy in your OpenShift project.

Follow this template:

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

Where:

- `podSelector` is a selector that matches your upstream service.
- `namespaceSelector` is the APS namespace which hosts the API Gateway on Emerald (`cc9a8a`), not your namespace. Don't change this.

**Upstream egress policy**: APS will also create an `egress` Network Policy to send traffic from the API Gateway to the upstream service.

[Contact the APS team](/how-to/get-support.md) to have an `egress` policy created for your Gateway.
You will need to provide the `namespaceSelector` details for the Openshift projects that will be receiving traffic.
APS will also add a rule to prevent traffic from reaching your service through a different Gateway.

##### Services external to Emerald cluster

For services that are not on the Emerald cluster, an APS `egress` Network Policy is required to send traffic from the API Gateway to the upstream service and you will need to setup firewall rules to allow the API Gateway access to your particular VLAN.

When making the firewall request, the IP CIDIR for the API Gateway on Emerald is: `10.91.43.128/26`

[Contact the APS team](/how-to/get-support.md) to have an `egress` policy created for your Gateway.
You will need to provide the network details of your VLAN.
APS will also add a rule to prevent traffic from reaching your service through a different Gateway.

#### Network policies for consumers

Consumers may require network policies to access your API, depending on how the route has been setup.

| Consumer    | Service Route     | Data Class   | Network policies                                                                                                                                                                                                                         |
| ----------- | ----------------- | ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| On cluster  | `*.cluster.local` | Low/Med/High | The Consumer will require an `egress policy` with a `to namespaceSelector` to the Kong API Gateway (see example 1 below). The API Gateway will require an `ingress` with a `from namespaceSelector` of the Consumer Openshift namespace. |
| Off cluster | `*.api.gov.bc.ca` | Low/Med/High | The API Gateway has `ingress` policies to allow traffic to the Kong API Gateway. No additional setup is required.                                                                                                                        |

**Example (1) Egress policy for on-cluster consumer**:

```yaml
kind: NetworkPolicy
apiVersion: networking.k8s.io/v1
metadata:
  name: allow-traffic-to-gateway-service
spec:
  podSelector:
    matchLabels:
      name: my-consumer-app
  egress:
    - to:
        - namespaceSelector:
            matchLabels:
              environment: prod
              name: cc9a8a
  policyTypes:
    - Egress
```

For on-cluster consumers (consumers that reside on Emerald), [Contact the APS team](/how-to/get-support.md) to have an `ingress` policy created for your Gateway.

#### DNS

For domains that will be routing to the Emerald cluster, a manual DNS entry must be setup by APS.

[Contact the APS team](/how-to/get-support.md) to have DNS configured for your Gateway.
You will need to provide the `Route.hosts` endpoints that will be configured on your Gateway.

If the consumers of your API are going to all be on the Emerald cluster, you can consider setting up [private routing](/how-to/private-route.md) to limit consumer access using an Openshift Service.

## Public cloud and on-premise

If your upstream service runs outside the Private Cloud OpenShift clusters (for
example, in a public cloud or an on-premise data centre), you can't use network
policies to control who reaches it. Since your service is reachable over a wider
network, it needs another way to accept only the requests that come through your
Gateway.

Always use HTTPS (`protocol: https`) between the Gateway and your upstream
service so the traffic is encrypted. Then use one or more of these methods to
confirm that requests came from the Gateway:

| Method                                                                         | What your service can confirm                                                                                             | What you set up                                                     |
| ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| [Gateway-signed JWT](#verify-requests-with-a-gateway-signed-jwt) (recommended) | The request came through an APS Gateway in the last minute, and was meant for your Gateway Service (when you check `aud`) | A plugin on your Gateway Service, and token validation in your code |
| [mTLS](#verify-upstream-services-with-mtls)                                    | The connection came from the Gateway, using a client certificate that only your Gateway has                               | A client certificate you create and renew, and a root CA from APS   |
| [IP restrictions](#restrict-by-ip-address)                                     | The request came from APS Gateway infrastructure, which other teams share                                                 | Firewall rules on your network                                      |

You can combine these methods. For example, IP restrictions block most unwanted
traffic before it reaches your service, and a Gateway-signed JWT confirms each
request that gets through.

### Verify requests with a Gateway-signed JWT

The [`kong-upstream-jwt`](/reference/plugins/kong-upstream-jwt.md) plugin lets
your service check that each request came through the APS Gateway.

How it works:

1. When the Gateway forwards a request to your service, the plugin adds a
   short-lived token (JWT) to a request header.
2. The Gateway signs the token with a private key that only APS holds.
3. Your service checks the signature with APS's public keys, which are published
   at a JWKS URL, and checks that the token's `aud` claim is your Gateway
   Service name. If the token is missing or expired, the signature doesn't
   match, or `aud` is any other value, your service rejects the request.

Your service only needs the public JWKS URL. You don't share secrets with APS or
manage certificates, and the plugin also works for services on OpenShift as an
extra check on top of network policies.

To set up the plugin and validate the token in your service, see the
[Kong Upstream JWT plugin reference](/reference/plugins/kong-upstream-jwt.md).

### Verify upstream services with mTLS

With mutual TLS (mTLS), the Gateway and your upstream service each check the
other's certificate:

- **The Gateway checks your service's server certificate** against your root
  CA. The Gateway Service configuration below sets this up, and also makes the
  Gateway present your client certificate when it connects.
- **Your service checks the Gateway's client certificate.** You set this up on
  your upstream service: configure it to require a client certificate, and to
  trust only your client certificate or the CA that issued it.

To support mTLS between the API Gateway and your upstream service, you will need
to provide client certificate and Root CA details along with your Gateway
Service configuration.

If using mTLS, publish your Gateway Service configuration using
`gwa pg <gateway-config.yaml>` rather than `gwa apply`.

Example configuration:

```yaml
services:
  - name: my-upstream-service
    host: my-upstream.site
    tags: [ ns.<gatewayId> ]
    port: 443
    protocol: https
    tls_verify: true
    ca_certificates: [0a780ee0-626c-11eb-ae93-0242ac130012]
    client_certificate: 8fc131ef-9752-43a4-ba70-eb10ba442d4e
    routes: [...]
certificates:
  - cert: "<PEM FORMAT>"
    key: "<PEM FORMAT>"
    tags: [ ns.<gatewayId> ]
    id: 8fc131ef-9752-43a4-ba70-eb10ba442d4e
```

Where:

- `services[n].tls_verify` is set to `true` so the Gateway verifies your upstream service's server certificate.
- `services[n].ca_certificates` contains the UUID of the Root CA for the certificate chain.

  Root CAs must be installed by the APS team -
  please [contact the APS team](/how-to/get-support.md) to request setup of your Root
  CA. A UUID will be provided to you.

- `services[n].client_certificate` contains the UUID of the client certificate, which matches the `certificate.id`.

  You must generate a UUID4 for each certificate you create.

  Use this Python command to get a UUID4:

  ```python linenums="0"
  python3 -c 'import uuid; print(uuid.uuid4())'
  ```

- `certificates[n].cert` and `certificates[n].key` contain the PEM formatted certificate and key, respectively.

  These values are most easily included in the YAML configuration in a single line.

  Use this Python command to get a PEM file on one line:

  ```python linenums="0"
  python3 -c 'import sys; import json; print(json.dumps(open(sys.argv[1]).read()))' my.pem
  ```

### Restrict by IP address

You can set your firewall to accept traffic only from the APS Gateway's outbound
IP addresses (the OpenShift cluster egress IPs). On its own this is the weakest
method: the Gateway runs on shared infrastructure, so other teams' traffic can
come from the same addresses. Use it with a Gateway-signed JWT or mTLS, or on
its own only when the data your service handles allows a lower level of
protection.

OpenShift egress IPs are listed on [Private Cloud network topology page](https://digital.gov.bc.ca/technology/cloud/private/internal-resources/topology/) (IDIR-restricted).
