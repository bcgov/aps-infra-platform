# aps-infra-platform

## Development

```
cd documentation
npx retypeapp watch
```

## Validate Broken Links

```
npx broken-link-checker \
  -r \
  --exclude cluster.local \
  --exclude github \
  --exclude lua-users.org \
  http://localhost:5000/aps-infra-platform/

```
