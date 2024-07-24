# Access Control List

Reference: https://docs.konghq.com/hub/kong-inc/acl/

## Use cases

Typically this is used when your Environment configuration uses the flow `kong-api-key-acl` or `kong-acl-only` where the
`allow` group is a special group defined for the Environment so that Access Managers can grant/revoke access to the
Service from the API Services Portal.

## Example

```
services:
- name: MY_REST_API
  tags: [ ns.<gatewayId> ]
  plugins:
  - name: acl
    tags: [ ns.<gatewayId> ]
    config:
      allow:
      - pir-dev
      deny: null
      hide_groups_header: true
```
