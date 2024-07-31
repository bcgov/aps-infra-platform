# Proxy Cache

The `proxy-cache` plugin provides a reverse proxy cache implementation for Kong Gateway.

## Configuration reference

This is a stock plugin from Kong Hub. See the [configuration reference page](https://docs.konghq.com/hub/kong-inc/proxy-cache/)
for a list of parameters and protocol compatibility notes.

## Common usage example

```yaml
plugins:
  - name: proxy-cache
    service: <SERVICE_NAME>
    config:
      response_code:
        - 200
      request_method:
        - GET
        - HEAD
      content_type:
        - text/html
        - text/css
        - application/javascript
      cache_ttl: 30
      # vary_headers:
      #   - header_1
      # vary_query_params:
      #   - param_1
      # strategy: memory
      # memory:
      #   dictionary_name: proxy_content_cache
```

Replace <SERVICE_NAME> with the name of the service that this plugin
configuration will target.

> `cache_ttl` : This value is restricted to be between 15 and 60 seconds

> The `strategy` and `memory.dictionary_name` will be set automatically and can
> not be overridden.

> - `vary_headers` : Relevant request headers considered for the cache key. If
>   undefined, none of the headers are taken into consideration.
> - `vary_query_params` : Relevant query parameters considered for the cache
>   key. If undefined, all params are taken into consideration.

> The `dictionary_name` is capped at 1Mi to be shared across all services.
> Recommended practice is to use the cache for targeted files to produce the
> greatest improvement on overall performance of your application.
