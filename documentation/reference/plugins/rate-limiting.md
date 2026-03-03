# Rate Limiting

The `rate-limiting` plugin adds rate limits to the amount of HTTP requests that
can be made in a given period of time.

## Configuration reference

This is a stock plugin from Kong Hub. See the [configuration reference page](https://docs.konghq.com/hub/kong-inc/rate-limiting/configuration)
for a list of parameters and protocol compatibility notes.

Here are some of the parameters which can be used in the plugin's `config` section:

- **policy**: default: `local` | `redis`
  
  See [rate limiting strategies](/how-to/COMMON-CONFIG.md#rate-limiting-strategies)
  for more information.
- **limit_by**: `consumer` | `credential` | `ip` | `service` | `header` | `path`
- **fault_tolerant**: Applies when Kong is connecting to Redis - if Redis is
  down, do you want to block traffic, or allow it through without limiting

## Common usage examples

To add rate limiting, add this section to your GatewayService configuration file:

```yaml
plugins:
- name: rate-limiting
  service: <MY_SERVICE>
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

Replace <SERVICE_NAME> with the name of the service that this plugin
configuration will target.

### Two-tiered access

If using an authentication plugin alongside rate limiting, you can enable
anonymous and authenticated access with different rate limits. See [two-tiered
access](/how-to/COMMON-CONFIG.md/#two-tiered-access).

### Backend service protection

Often rate limiting is applied on a per-user basis (using `limit_by = ip`,
`credential`, or `consumer`. To provide a global limit to the number of requests
to a service to ensure a backend service is not overwhelmed, you can use
`limit_by = service`.

To apply a second rate limit to a service (or route), you can use the plugin
`rate-limiting_902`, which will run with higher priority - that is, before - the
regular `rate-limiting` plugin.

Here is example configuration showing per-user and global (service) rate
limiting:

```yaml
plugins:
- name: rate-limiting
  config:
    limit_by: consumer
    policy: redis
    hide_client_headers: false # users need to see these headers
    minute: 600
- name: rate-limiting_902
  config:
    limit_by: service
    policy: local
    hide_client_headers: true # users DO NOT need to see these headers
    minute: 10000
```

### Rate limiting by JWT credential

Teams using a single-page application (SPA) can protect their backend
API service with per-user rate limiting.

A common auth pattern for SPAs is for the SPA to authenticate a user, obtain a
JWT from an authorization server, and then include that JWT in API requests in
the `Authorization: Bearer <token>` header. The `jwt-keycloak` plugin can be
used to validate the token at the gateway, potentially in addition to validation
on the backend.

To rate limit per authenticated user, set `consumer_match = true` in the
`jwt-keycloak` config - the plugin will find the Kong consumer `id` matching the
`consumer_match_claim` (default `azp`). In the `rate-limiting` plugin, use
`limit_by = credential`, like so:

```yaml
plugins:
- name: jwt-keycloak
  config:
    allowed_iss:
    - https://<KEYCLOAK>/auth/realms/<REALM>
    consumer_match: true
- name: rate-limiting
  config:
    limit_by: credential
    policy: redis
    minute: 600
```
