---
title: "Share an Externally Protected API"
---


This page shows how to share externally protected APIs on the {{ glossary_tooltip
term_id="api-directory" }}, without setting up any {{ glossary_tooltip term_id="gateway-service"
text="Gateway Services" }} in the {{ glossary_tooltip term_id="api-services-portal"}}.

## Before you begin

You need to have the `gwa` command line interface (CLI) installed. Download it from
[GitHub](https://github.com/bcgov/gwa-cli/releases) and add to `PATH` for the session.

On Linux, run this command to get set up:

```sh linenums="0"
curl -L https://github.com/bcgov/gwa-cli/releases/download/v2.0.15/gwa_Linux_x86_64.tgz | tar -zxf -
export PATH=$PATH:$PWD
```

## Login

Log into the API Services Portal with your IDIR account:

``` linenums="0"
gwa config set host api.gov.bc.ca
gwa login
```

Alternatively run `gwa config set host api-gov-bc-ca.test.api.gov.bc.ca` to work
on the Test/Training instance of the API Services Portal.

## Create a Gateway

First, create a new {{ glossary_tooltip term_id="gateway" }}. Gateways provide a
mechanism for isolating groups of resources and can be managed by multiple users
on a team.

``` linenums="0"
gwa gateway create -g
```

`-g` generates a random, unique namespace which is displayed in response.
Confirm this is the active Gateway with:

``` linenums="0"
gwa gateway current
```

## Add a Dataset

Now, add a *Dataset* with metadata about the API to display in the API
Directory. This information helps consumers find your API in the Directory.
Typically, each Dataset would describe one API.

If your API is already listed in the [BC Data Catalogue](https://catalogue.data.gov.bc.ca/),
skip ahead to [Add a Product](#create-a-product).

Start by writing up a DraftDataset in a local YAML file. Here is the schema,
omitting some optional fields:

```yaml title="Dataset template"
    kind: DraftDataset
    name: dataset-name
    title: Useful API
    notes: A handy API with many uses.
    tags: [useful, data, openapi]
    organization: ministry-of-citizens-services
    organizationUnit: databc
    license_title: Open Government Licence - British Columbia
    view_audience: Government
    security_class: PUBLIC
    record_publish_date: "2021-05-27"
```

 | Field     | Description                              |
 | --------------- | ---------------------------------------------------------------- |
 | `kind` |     |
 | `name`      | Unique dataset name, not displayed                  |
 | `title`      | API title shown in the API Directory                 |
 |`notes`      | API description, supports Markdown formatting                |
 |`tags`      | Keywords, may be used for search in the future                 |
 | `organization`      | Ministry or agency associated with the API ([options](<https://api.gov.bc.ca/ds/api/v2/organizations>)) that must match the organization associated with the Gateway                |
 | `organizationUnit`      | Organization business sub-unit ([options](https://api.gov.bc.ca/ds/api/v2/organizations/<organization>)) |
 |`license_title`      | [Licensing options](https://bcgov.github.io/data-publication/pages/dps_licences.html)                |
 | `view_audience`      | Who can access the API                |
 | `security_class`      | [OCIO Information Security Classification Standard](https://www2.gov.bc.ca/assets/gov/government/services-for-government-and-broader-public-sector/information-technology-services/standards-files/618_information_security_classification_standard.pdf)                 |
 | `record_publish_date`      | Date when the API was published                  |

!!! note "Link to your API"
    In the `notes` field, be sure to add a link to your API to allow interested
    consumers to find out more. Specifically, ensure there are links to the API
    specification, developer guide, and how to request access. Use Markdown for
    formatting. For example:

    ```md
    notes: |
      Useful API is a versatile toolset for developers, offering a comprehensive
      suite of functions and endpoints to streamline application development.

      Visit the [Useful API page](https://api.useful.com) to view the API spec,
      read the developer guide, and request access.
    ```

After preparing a DraftDataset, publish it with:

``` linenums="0"
gwa apply -i <draft-dataset.yaml>
```

You should see `✔ [DraftDataset] <dataset-name>: created`.

## Create a Product

It's time to create a *Product*, which describes the type of protection on the
API. Products are typically used to bundle Gateway Services and manage consumer
access, but since your API is externally protected, very little is required
here.

Create a Product configuration using the YAML template below. If your API is
already listed in the [BC Data Catalogue](https://catalogue.data.gov.bc.ca/),
use the slug value for `dataset` from the Data Catalogue dataset URL:
`https://catalogue.data.gov.bc.ca/dataset/<api-slug-value>`.

Add other available environments if desired (e.g. `dev`, `test`, `sandbox`).

```yaml title="Product template"
kind: Product
name: Useful API # Name shown on the API Directory
dataset: dataset-name # Dataset name or BC Data Catalogue slug value
environments:
- name: prod
  active: false
  flow: protected-externally
```

Then publish the product:

``` linenums="0"
gwa apply -i <product.yaml>
```

## Preview your API listing

Preview your new API listing by signing in to the [API Services Portal](https://api.gov.bc.ca/)
, opening the **API Directory**, and clicking the **Your Products** tab. Confirm
everything is as desired.

## Add your Organization

On top of the API Directory, you will see a banner notification stating "Your
APIs are in preview mode." To make your APIs publicly visible in the Directory,
select **Add Organization** and follow the instructions in the dialogue.

An Organization Administrator will receive your request and should approve it or
follow up for more information within 2 business days. At this time, there is no
approval notification.

## Enable Product environments

After receiving organization approval, the final step is to enable the Product
environment(s).

Enable environments by either updating the Product environment configuration
YAML to `active: true`, or navigate to the API Services Portal > **Gateway** >
**Products** > **Edit** in the table > **Configure environment** > select
**Enable Environment**.

!!! note
    The **Enable Environment** checkbox will be disabled if an Organization has
    not been added to the Gateway.

Your API is now listed on the [API Directory](https://api.gov.bc.ca/devportal/api-directory).
