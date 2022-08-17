# CORS

```
  - name: cors
    tags: [slashui-dev]
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
