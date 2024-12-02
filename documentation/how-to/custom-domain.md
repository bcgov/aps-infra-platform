---
title: Configure a Custom Domain
---

<!-- overview -->

This guide explains how to configure a custom domain for your Gateway Service(s).

<!-- prerequisites -->

## Before you begin

Before you begin, ensure you:

- [Install gwa CLI](/how-to/gwa-install.md)
- [Create a Gateway](/how-to/create-gateway.md)
- Register your custom domain and obtain SSL certificates

<!-- steps -->

## Submit a request with APS

Routing to a custom domain requires special permissions for your Gateway. Reach
out to the APS team on Rocket.Chat in the
[#aps-ops](https://chat.developer.gov.bc.ca/channel/aps-ops) channel or [open a
support
ticket](https://dpdd.atlassian.net/servicedesk/customer/portal/1/group/2). You will need to provide the fully qualified domain name (FQDN) and the `gatewayId` for your Gateway.

The APS team will also create a DNS record for your custom domain pointing to
the OpenShift cluster where your Gateway is deployed. See [Set Up an Upstream
Service](/how-to/upstream-services) for more information on the available
clusters.

## Create a Gateway Service

Creating a Gateway Service with a custom domain is much the same as creating a
Gateway Service without a custom domain. The key difference is the inclusion of
SSL certficiates in the `certificates` section.

For more general information on creating Gateway Services, see [Create a Gateway Service](/how-to/create-gateway-service.md).

Add the `certificates` section to your Gateway Service configuration as shown in this example:

```yaml
certificates:
  - cert: "<PEM FORMAT>"
    key: "<PEM FORMAT>"
    tags: [ns.<gatewayId>]
    id: <GENERATED UUID4>
    snis:
      - name: <HOSTNAME>
        id: <GENERATED UUID4>
        tags: [ns.<gatewayId>]
services:
  - name: example-service-name
    host: httpbin.org
    tags: [ns.<gatewayId>]
    port: 443
    protocol: https
    routes:
      - name: example-route-name
        tags: [ns.<gatewayId>]
        hosts:
          - <HOSTNAME>
```

Where:

- `certificates[n].cert` and `certificates[n].key` contain the PEM formatted certificate and key, respectively.

  These values are most easily included in the YAML configuration in a single line. 
  
  Use this Python command to get a PEM file on one line:
    
    ```python linenums="0"
    python3 -c 'import sys; import json; print(json.dumps(open(sys.argv[1]).read()))' my.pem
    ```

- `certificates[n].id` is a UUID4 you will generate.
- `certificates[n].snis.name` is the hostname on the custom domain
- `certificates[n].snis.id` is a different UUID4 you will generate.

  Use this Python command to get a UUID4:
    
  ```python linenums="0"
  python3 -c 'import uuid; print(uuid.uuid4())'
  ```

!!! warning "Gateway configuration formats"
    There are [two formats for Gateway configuration](/concepts/gateway-config.md#gateway-configuration-formats).
    To include SSL certificates in your Gateway Service configuration, you must use the **legacy format**, as shown above.   

    To publish other resource types (Product, Dataset, etc.), you can maintain a separate 
    YAML file using the resource-based format and publish it using the `gwa apply` command. 

## Publish Gateway Service

Publish your Gateway Service with custom domain using the following command:

```shell linenums="0"
gwa pg gw-config.yaml
```

## Configure DNS for your custom domain

You will need to add a DNS record for your custom domain pointing to the OpenShift cluster where your Gateway is deployed.

### Silver cluster

By default, new Gateways are created on the Silver cluster. Create an A record
for your custom domain pointing to `142.34.194.118`, Silver's ingress IP
address.

### Gold cluster

Gold cluster route hosts will resolve to `142.34.229.4` or `142.34.64.4`
depending on whether the APS service is in Gold (Kamloops) or for disaster
recovery in Gold DR (Calgary).

To ensure routing to the appropriate cluster, create a CNAME record for your
custom domain pointing to `ggw.api.gov.bc.ca.glb.gov.bc.ca`, APS's Global Load
Balancer.

### Emerald cluster

Emerald cluster route hosts will be assigned an IP address depending on the data
class that was specified in the Gateway Service.

[Contact the APS team](README.md#need-a-hand) to get the IP address for your
routes. This IP address will not change for the route unless the data class
changes.

Once you have the IP address, create an A record for your custom domain pointing
to the IP address.

## Access your API (Validation)

After publishing your Gateway Service and configuring DNS, you can access your
API by visiting the URL of your Gateway Service.

You can expect to see upstream API responses in the browser, or if you used the
placeholder `httpbin.org` in the Gateway Service configuration, you will see the
contents of the httpbin.org homepage.

<!-- whatsnext -->

## Next steps

- [Add Client Credential Protection](/how-to/client-cred-flow.md)
- [Configure a Private Route](/how-to/private-route.md)
- [Configure Gateway Controls](/how-to/COMMON-CONFIG.md)
- [Share your API](/how-to/api-discovery.md)
- [Monitor your Services](/how-to/monitoring.md)
