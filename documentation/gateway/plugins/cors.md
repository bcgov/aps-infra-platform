# Cross-origin Resource Sharing (CORS)

Reference: https://docs.konghq.com/hub/kong-inc/cors/

Example

```
services:
- name: MY_REST_API
  tags: [ _NS_ ]
  plugins:
  - name: cors
    tags: [ _NS_ ]
    config:
      origins: ["*"]
      methods: [GET, POST, PUT, PATCH, OPTIONS]
      headers:
        [
          Connection,
          Upgrade,
          Cache-Control,
          Access-Control-Allow-Headers,
          Keep-Alive,
        ]
      credentials: true
      max_age: 3600
```

Additional references:
* https://github.com/Kong/kong/issues/4859
