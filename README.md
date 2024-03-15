# aps-infra-platform

## Development

Linux:
```
docker pull ghcr.io/bcgov/devhub-techdocs-publish
docker run -it -p 3000:3000 -v $(pwd):/github/workspace ghcr.io/bcgov/devhub-techdocs-publish preview
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

## Update GWA CLI

**Prerequisite: `golang`**

```
mkdir _tmp
cd _tmp
git clone https://github.com/bcgov/gwa-cli
cd gwa-cli
just docs
cp docs/gwa-commands.md ../../documentation/resources/gwa-commands.md
```
