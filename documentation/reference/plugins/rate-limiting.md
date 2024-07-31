# Rate Limiting

The `rate-limiting` plugin adds rate limits to the amount of HTTP requests that
can be made in a given period of time.

## Configuration reference

This is a stock plugin from Kong Hub. See the [configuration reference page](https://docs.konghq.com/hub/kong-inc/rate-limiting/configuration)
for a list of parameters and protocol compatibility notes.

Here are some of the parameters which can be used in the plugin's `config` section:

- **policy**: `local` | `redis`
- **limit_by**: `consumer` | `credential` | `ip` | `service` | `header` | `path`
- **fault_tolerant**: Applies when Kong is connecting to Redis - if Redis is
  down, do you want to block traffic, or allow it through without limiting

## Common usage example

To add rate limiting, add this section to your GatewayService configuration file:

```yaml
plugins:
- name: rate-limiting
  service: <MY_SERVICE>
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

Replace <SERVICE_NAME> with the name of the service that this plugin
configuration will target.

## Alternatives

If you want to apply 2 global rate limits, you can use the plugin:
`rate-limiting_902`.

For example, one control with `limit_by = service` that provides an umbrella max
requests per minute and another control with `limit_by = credential` that
ensures each authenticated user plays nice.
