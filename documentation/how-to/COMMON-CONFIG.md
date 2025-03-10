---
title: Common Controls
---

The following are sample Gateway controls for common scenarios.

To learn about other available plugins, navigate to `References > Plugins` on the
sidebar of this page.

## Returning an HTTP redirect

```yaml
plugins:
- name: pre-function
  tags: [ ns.<gatewayId> ]
  config:
    access:
    - "kong.response.exit(307, 'site moved - redirecting...', {['Location'] = 'https://my-new-url.site'})"
```

## Request termination

```yaml
plugins:
- name: request-termination
  tags: [ ns.<gatewayId> ]
  config:
    status_code: 400
    message: API not implemented yet!
```

## Adding headers for best security practices

```yaml
plugins:
- name: response-transformer
  tags: [ ns.<gatewayId> ]
  config:
    add:
      headers:
      - "X-Frame-Options: DENY"
      - "X-XSS-Protection: 1; mode=block"
      - "X-Content-Type-Options: nosniff"
      - "Strict-Transport-Security: max-age=31536000"
      - "Content-Security-Policy: script-src 'self'"
```

> For further information on individual headers, see: <https://owasp.org/www-project-secure-headers/>

## Rate limiting

### Option 1 - Using a distributed cache

This provides the most accurate because it uses a centralized cache that all
Kong nodes use. The downside is that there is a 100-200ms latency.

```yaml
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

### Option 2 - Node local caching

This provides the fastest rate limiting option, with minimal latency (~1ms). The
downside is that it is local to each node so calculating the actual load on your
upstream is a function of the number of nodes.

```yaml
plugins:
- name: rate-limiting
  tags: [ ns.<gatewayId> ]
  config:
    policy: local
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

## Two-tiered access setup

The `key-auth` and `jwt-keycloak` plugins support the concept of allowing
"anonymous" access, which allows you to define a "free" service which might have
limits around it (like only allowing 100 requests/minute), in addition to an
"elevated" access where the Consumer would get an improved level of service,
such as higher rate limits.

There is a global "anonymous" consumer that is identified as
`ce26955a-cf08-4907-9427-12d01c8bd94c` in both our Test and Production
environments.

To enable anonymous access to your API, update your plugin configuration with:

### `key-auth`

```yaml
- name: key-auth
  tags: [ ns.<gatewayId> ]
  config:
    ...
    anonymous: ce26955a-cf08-4907-9427-12d01c8bd94c
```

### `jwt-keycloak`

```yaml
- name: jwt-keycloak
  tags: [ ns.<gatewayId> ]
  config:
    ...
    consumer_match: true
    consumer_match_ignore_not_found: false
    consumer_match_claim_custom_id: false
    anonymous: ce26955a-cf08-4907-9427-12d01c8bd94c
```

If you do not want to advertise anonymous access on the API Directory, you can
hide it by adding the `aps.two-tiered-hidden` tag to your plugin configuration.

## Event metrics

The `pre-function` plugin allows you to collect arbitrary metrics that you can then
track in [Grafana](/how-to/monitoring.md) on the **X Events** dashboard.

First define your event conditions and desired `x-event` headers in Lua. Here is
an example which looks at a query parameter:

```lua
if kong.request.get_query_arg("layers") = "WILDFIRE" then
    kong.service.request.set_header("x-event", "wildfire")
else
    kong.service.request.set_header("x-event", "other")
end
```

Then convert the Lua to a string to use in the plugin configuration:

```sh
echo '
if kong.request.get_query_arg("layers") = "WILDFIRE" then
    kong.service.request.set_header("x-event", "wildfire")
else
    kong.service.request.set_header("x-event", "other")
end
' | \
python3 -c "import json,sys; script=sys.stdin.read(); print(json.dumps(script.strip()))"
```

Finally, add the string to the plugin:

```yaml
plugins:
- name: pre-function
  tags: [ ns.<gatewayId> ]
  config:
    access:
    - "<OUTPUT FROM ABOVE>"
```

## Disabling global error handling

APS has a global `post-function` plugin that transforms the response message if
the following HTTP status codes are returned by the upstream service:

```http
s408 = "Request timeout",
s411 = "Length required",
s412 = "Precondition failed",
s413 = "Payload too large",
s414 = "URI too long",
s417 = "Expectation failed",
s494 = "Request header or cookie too large",
s500 = "An unexpected error occurred",
s502 = "An invalid response was received from the upstream server",
s503 = "The upstream server is currently unavailable",
s504 = "The upstream server is timing out",
```

If this transformation is not desired, you can override it by including the
following plugin on your Service:

```yaml
plugins:
- name: post-function
  tags: [ ns.<gatewayId> ]
  config:
    rewrite:
    - "--"
```
