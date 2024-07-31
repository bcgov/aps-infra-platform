# GWA IP Anonymity

The `gwa-ip-anonymity` plugin lets you mask the last segment of a user's IP
address before it is sent to the upstream service. A user's IP
address is considered part of PII (Personally Identifiable Information).

## Configuration reference

This is a custom plugin managed by the API Program Services team.

## Common usage example

To mask the last segment of a user's IP address before it is sent to the
Upstream Service, add this section to your GatewayService configuration file:

```yaml
plugins:
- name: gwa-ip-anonymity
  service: <SERVICE_NAME>
  enabled: true
  config:
    ipv4_mask: 0
    ipv6_mask: 0
```

Replace <SERVICE_NAME> with the name of the service that this plugin
configuration will target.
