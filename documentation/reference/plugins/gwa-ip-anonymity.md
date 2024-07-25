# GWA IP Anonymity

## Use cases

A user's IP address is considered part of PII (Personally Identifiable
Information). This is a custom plugin that was created to mask the last segment
of the IP address before it is sent to the Upstream Service.

## Example

```yaml
services:
- name: MY_REST_API
  tags: [ ns.<gatewayId> ]
  plugins:
  - name: gwa-ip-anonymity
    tags: [ ns.<gatewayId> ]
    enabled: true
    config:
      ipv4_mask: 0
      ipv6_mask: 0
```
