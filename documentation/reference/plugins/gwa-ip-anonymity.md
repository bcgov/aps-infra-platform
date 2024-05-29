# GWA IP Anonymity

## Use Cases

A user's IP address is considered part of PII (Personally Identifiable Information). This is a custom plugin that was created to mask the last segment of the IP address before it is sent to the Upstream Service.

## Example

```
services:
- name: MY_REST_API
  tags: [ _NS_ ]
  plugins:
  - name: gwa-ip-anonymity
    tags: [ _NS_ ]
    enabled: true
    config:
      ipv4_mask: 0
      ipv6_mask: 0
```
