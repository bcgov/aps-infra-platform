---
title: "Share an Externally Protected API"
---

# Share an Externally Protected API

Teams may want to take advantage of the API Directory to share their APIs, without managing their service with the API Management Platform's API Gateway. This guide shows how to 

## Before you begin

The commands provided in this tutorial are for a Unix shell (e.g. `bash`, `zsh`). If you are running Windows, it is recommended to use WSL2.

## Download the `gwa` CLI 

Start by downloading the `gwa` cli and adding to `PATH` for the session:

```sh
curl -L https://github.com/bcgov/gwa-cli/releases/download/v2.0.15/gwa_Linux_x86_64.tgz | tar -zxf -
export PATH=$PATH:$PWD
```

## Login

Log into the API Services Portal with your IDIR account.

```
gwa config set host api.gov.bc.ca
gwa login
```

Alternatively run `gwa config set host api-gov-bc-ca.test.api.gov.bc.ca` to work on the Test/Training instance of the API Management Platform. 

## Create a Namespace

First, create a new *Namespace*. Namespaces provide a mechanism for isolating groups of resources and can be managed by multiple users on a team.

```
gwa namespace create -g
```

`-g` generates a random, unique namespace which is displayed in response. Confirm this is the active namespace with:

```
gwa namespace current
```

## Add a Dataset

Now, add a *Dataset* with metadata about the API to display in the API Directory. This information helps consumers find your API in the Directory. Typically, each Dataset would describe one API.

If your API is already listed in the [BC Data Catalogue](https://catalogue.data.gov.bc.ca/), skip ahead to [Add a Product](#add-a-product).

Start by writing up a DraftDataset in a local YAML file (if using the CLI) or JSON file (if using the API). Here is the schema, omitting some optional fields:

=== "YAML Template (w/ field descriptions)"
    ```yaml
    kind: DraftDataset
    name: my-draft-dataset # unique dataset name, not displayed
    title: Useful API # API title shown on the API Directory
    notes: A handy API with many uses. # API description, supports Markdown formatting
    tags: [useful, data, openapi] # keywords, may be used for search in future
    organization: ministry-of-citizens-services # ministry or agency associated with the API (see https://api.gov.bc.ca/ds/api/v2/organizations for options) - this must match the organization associated with the namespace
    organizationUnit: databc # organization business sub-unit (see https://api.gov.bc.ca/ds/api/v2/organizations/<organization> for options)
    license_title: Open Government Licence - British Columbia # see https://bcgov.github.io/data-publication/pages/dps_licences.html for licensing options
    view_audience: Government # who can access the API
    security_class: PUBLIC # OCIO Information Security Classification Standard, see https://www2.gov.bc.ca/assets/gov/government/services-for-government-and-broader-public-sector/information-technology-services/standards-files/618_information_security_classification_standard.pdf
    record_publish_date: "2021-05-27" # date when the API was published
    ```

=== "YAML Template"
    ```yaml
    kind: DraftDataset
    name: my-draft-dataset
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

After preparing a DraftDataset, publish it with:

```
`gwa apply -i <draft-dataset.yaml>`
```

You should see `✔ [DraftDataset] <dataset-name>: created`.

## Add a Product

It's time to add a *Product*, which describes the type of protection on the API. Products are typically used to bundle Gateway Services and manage consumer access, but since your API is externally protected, very little is required here.

Create a Product configuration using the YAML template below. If your API is already listed in the [BC Data Catalogue](https://catalogue.data.gov.bc.ca/), use the slug value for `dataset` from the Data Catalogue dataset URL, `https://catalogue.data.gov.bc.ca/dataset/<api-slug-value>`.

Add other available environments if desired (e.g. `dev`, `test`, `sandbox`).

```yaml title="Product YAML Template"
kind: Product
name: Useful API # Name shown on the API Directory
dataset: my-draft-dataset # Dataset name or BC Data Catalogue slug value
environments:
- name: prod
  active: false
  flow: protected-externally
  appId: '<UNIQUE_APP_ID>' # Retrieve from https://api.gov.bc.ca/ds/api/v2/identifiers/environment.
```

Then publish the product:

```
gwa apply -i <product.yaml>
```

## Preview your Product

Preview your new API listing by signing in to the [API Services Portal](https://api.gov.bc.ca/), opening the **API Directory** and clicking the **Your Products** tab. Confirm everything is as desired.

## Add your Organization

On top of the API Directory, you will see a banner notification stating "Your APIs are in preview mode." To make your APIs publicly visible in the Directory, select **Add Organization** and follow the instructions in the dialogue.

An Organization Administrator will receive your request and should approve it or follow up for more information within 2 business days. At this time, there is no approval notification.

## Enable Product environments

After receiving organization approval, the final step is to enable the Product environment(s).

Enable environments by either updating the Product environment configuration YAML to `active: true`, or on the API Services Portal -> **Product** page -> **Edit** the environment details -> check **Enable Environment**.

Your API is now listed on the [API Directory](https://api.gov.bc.ca/devportal/api-directory).