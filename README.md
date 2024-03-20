# aps-infra-platform

## Preview docs locally

Linux:
```
docker pull ghcr.io/bcgov/devhub-techdocs-publish
docker run -it -p 3000:3000 -v $(pwd):/github/workspace ghcr.io/bcgov/devhub-techdocs-publish preview
```

## Validate Broken Links

First run the local preview. Then:

```
npm install -g @umbrelladocs/linkspector
linkspector check
```

See https://github.com/UmbrellaDocs/linkspector

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
