# Rate Limiting

Reference: <https://docs.konghq.com/hub/kong-inc/rate-limiting/>

- **policy**: `local` | `redis`
- **limit_by**: `consumer` | `credential` | `ip` | `service` | `header` | `path`
- **fault_tolerant**: Applies when Kong is connecting to Redis - if Redis is
  down, do you want to block traffic, or allow it through without limiting

## Example

```yaml
services:
- name: MY_REST_API
  tags: [ ns.<gatewayId> ]
  plugins:
  - name: rate-limiting
    tags: [ ns.<gatewayId> ]
    config:
      fault_tolerant: true
      hide_client_headers: false
      limit_by: ip
      minute: 30000
      second: null
      hour: null
      day: null
      month: null
      year: null
```

## Alternatives

If you want to apply 2 global rate limits, you can use the plugin:
`rate-limiting_902`.

For example, one control with `limit_by = service` that provides an umbrella max
requests per minute and another control with `limit_by = credential` that
ensures each authenticated user plays nice.
