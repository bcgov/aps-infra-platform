# aps-infra-platform

## Preview docs locally

### Docker

```shell
docker pull ghcr.io/bcgov/devhub-techdocs-publish
docker run -it -p 3000:3000 --user $(id -u):$(id -g) -v $(pwd):/github/workspace ghcr.io/bcgov/devhub-techdocs-publish preview
```

> ⚠️ **Note:** The `--user $(id -u):$(id -g)` flag ensures the container runs with your user ID to avoid permission errors when mounting volumes.

Starts a "preview" web server on <http://localhost:3000> for you to review your
content. When the documents configured in the `mkdocs.yml` file are edited, the
changes will be live-updated on the local site.

For more help, check [INDEX.MD](https://github.com/bcgov/devhub-techdocs-publish/blob/main/docs/index.md)
in DevHub.

### Python / Mkdocs

If you prefer to run MkDocs directly, instead of inside docker, you can use the following commands:

```shell
python3 -m venv .venv
source .venv/bin/activate
pip install mkdocs mkdocs-techdocs-core mkdocs-ezlinks-plugin mkdocs-git-revision-date-localized-plugin
mkdocs serve -a 0.0.0.0:3000
```

This starts up much faster than docker (by omitting `htmltest`), but may
not replicate styles or markdown rendering as accurately.

## Validate broken links

First run the local preview. Then:

```shell
npm install -g @umbrelladocs/linkspector
linkspector check
```

See <https://github.com/UmbrellaDocs/linkspector>

Alternatively, you can view the results of `htmltest` which runs as part of the
DevHub TechDocs build process. Search the build logs for `htmltest` to find the
results.

## Update GWA CLI

> 💡 **Prerequisite:** `golang`

```shell
mkdir _tmp
cd _tmp
git clone https://github.com/bcgov/gwa-cli
cd gwa-cli
just docs
cp docs/gwa-commands.md ../../documentation/reference/gwa-commands.md
```

## Insert glossary term references

Use this tag when introducing key concepts. Most often this will be in an
introductory / overview section.

`{{ glossary_tooltip term_id="api-services-portal" text="API Services Portal" }}`

`term_id`: The term to reference, defined in `scripts/glossary_reference.yaml`.
Must be passed first as first attribute.

`text` (optional): The displayed text. If not provided, the `name` (in Title
Case) is used.

The result is the display text specially styled with a tooltip including the
definition and a link to a relevant reference URL (if defined in
`glossary_reference.yaml`).

## Deploy to DevHub

A GitHub Actions workflow is used to deploy the docs to DevHub. The workflow is
triggered by a push to the `main` or `test` branches - pushing to `main` will
deploy to the `prod` environment
(<https://developer.gov.bc.ca/docs/default/component/aps-infra-platform-docs/>),
and pushing to `test` will deploy to the `test` environment
(<https://dev.developer.gov.bc.ca/docs/default/component/aps-infra-platform-docs/>).

You can also manually trigger the workflow from the [Actions tab](https://github.com/bcgov/aps-infra-platform/actions/workflows/publish-techdocs.yaml)
to deploy a working branch to the `test` environment. Use the `Run workflow`
dropdown to select the branch you want to deploy.

See the [workflow file](.github/workflows/publish-techdocs.yaml) for details.
