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

<!-- steps -->

## Create a Gateway Service with a Custom Domain

If you have already created a Gateway Service in [Create a Gateway Service](/how-to/create-gateway-service.md) 
or [Quick Start](/tutorials/quick-start.md) using the `gwa generate-config` command, you will need to extract 
the Gateway Service information into a separate YAML file and reformat as shown below.

Example configuration:

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

- `certificates[n].id` is a UUID4 you will generate.
- `certificates[n].snis.name` is the hostname on the custom domain
- `certificates[n].snis.id` is a different UUID4 you will generate.

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

## Publish Gateway Service with Custom Domain

When using a custom domain, you will need to maintain two separate YAML files. One will contain the 
certificate details and Gateway Service configuration (seen above), and will be applied using the `gwa pg` 
command. The other will contain any Portal resources (Product, Dataset, etc.) you define, and will be 
applied using the `gwa apply` command.

Publish your Gateway Service with custom domain using the following command:

```shell linenums="0"
gwa pg gw.yaml
```

<!-- whatsnext -->

## Next steps

- [Add Client Credential Protection](/how-to/client-cred-flow.md)
- [Configure a Private Route](/how-to/private-route.md)
- [Configure Gateway Controls](/how-to/COMMON-CONFIG.md)
- [Share your API](/how-to/api-discovery.md)
- [Monitor your Services](/how-to/monitoring.md)
