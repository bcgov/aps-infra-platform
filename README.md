# aps-infra-platform

## Preview docs locally

Linux:
```
docker pull ghcr.io/bcgov/devhub-techdocs-publish
docker run -it -p 3000:3000 -v $(pwd):/github/workspace ghcr.io/bcgov/devhub-techdocs-publish preview
```

## Validate broken links

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

## Insert glossary term references

Use this tag when introducing key concepts. Most often this will be in an introductory / overview section.

`{{ glossary_tooltip term_id="api-services-portal" text="API Services Portal" }}`

`term_id`: The term to reference, defined in `scripts/glossary_reference.yaml`.

`text` (optional): The displayed text. If not provided, the `name` (in Title Case) is used.

The result is the display text specially styled with a tooltip including the definition and a link to a relevant reference URL (if defined in `glossary_reference.yaml`).
