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

For further information on individual headers, see: <https://owasp.org/www-project-secure-headers/>

## Rate limiting

### Rate limiting strategies

Rate limiting policies in Kong can be configured to use either a distributed
cache (such as Redis) or local node memory. A short explanation of each option
and example configuration is provided below. More information can be found in the
[Kong Rate Limiting plugin
docs](https://developer.konghq.com/plugins/rate-limiting/#strategies).

#### Option 1 - Using a distributed cache (`redis`)

Use when every transation counts. `redis` provides the most accurate rate limiting
because it uses a centralized cache for traffic to all all Kong nodes. The
downside is that there is 100-200 ms added latency.

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

#### Option 2 - Node local caching

Use for basic backend protection. `local` provides the fastest rate limiting
option, with minimal latency (~1 ms). The downside is that it is local to each
Kong node so the number of requests allowed to your upstream is a function of
the number of Kong nodes (which scale based on total gateway traffic).

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

### Two-tiered access

The `key-auth` and `jwt-keycloak` plugins let you enable "anonymous" access
alongside authenticated access, potentially offering two-tiers of service access:

- "free" service tier with restrictions (such as allowing only 100 requests per
minute).
- "elevated" service tier for authenticated consumers (such as higher rate limits).

To enable anonymous access to your API, add the global `anonymous` consumer with
the ID `ce26955a-cf08-4907-9427-12d01c8bd94c` to your auth plugin configuration:

#### `key-auth`

```yaml
- name: key-auth
  tags: [ ns.<gatewayId> ]
  config:
    ...
    anonymous: ce26955a-cf08-4907-9427-12d01c8bd94c
```

#### `jwt-keycloak`

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

Provide elevated access for authenticated consumers via the Consumers page on
the API Services Portal. Elevated access must be configured on a
consumer-by-consumer basis.

In the API Directory, Products with two-tiered access will display this notice
regarding elevated access:

![New API card](/artifacts/api-directory-product-two-tiered.png)

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
