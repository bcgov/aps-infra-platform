# Rate Limiting

Reference: https://docs.konghq.com/hub/kong-inc/rate-limiting/

- **policy**: `local` | `redis`
- **limit_by**: `consumer` | `credential` | `ip` | `service` | `header` | `path`

## Example

```
services:
- name: MY_REST_API
  tags: [ _NS_ ]
  plugins:
  - name: rate-limiting
    tags: [ _NS_ ]
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

If you want to apply 2 global rate limits, you can use the plugin: `rate-limiting_902`.

For example, one control with `limit_by = service` that provides an umbrella max requests per minute and another control with `limit_by = credential` that ensures each authenticated user plays nice.
