# Proxy Cache

Reference: https://docs.konghq.com/hub/kong-inc/proxy-cache/

## Example

```yaml
services:
  - name: MY_REST_API
    tags: [_NS_]
    plugins:
      - name: proxy-cache
        tags: [_NS_]
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
          # strategy: memory
          # memory:
          #   dictionary_name: proxy_content_cache
          # vary_headers:
          #   - header_1
          # vary_query_params:
          #   - param_1
```

> `cache_ttl` : We only allow this value to be between 15 and 60 seconds

> The `strategy` and `memory.dictionary_name` will be set automatically and can not be overridden.

> - `vary_headers` : Relevant request headers considered for the cache key. If undefined, none of the headers are taken into consideration.
> - `vary_query_params` : Relevant query parameters considered for the cache key. If undefined, all params are taken into consideration.

> The `dictionary_name` is capped at 1Mi to be shared across all services. Recommended practice is to use the cache for targeted files to produce the greatest improvement on overall performance of your application.
