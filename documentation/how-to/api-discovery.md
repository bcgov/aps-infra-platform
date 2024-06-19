---
title: "Share an API"
---

This page shows how to list an API on the [API Directory](https://api.gov.bc.ca/devportal/api-directory).

The API Directory enables you to package your APIs and make them available for
discovery by developers and other API consumers, across BC Government and beyond.

## Before you begin

- [Install gwa CLI](/how-to/gwa-install.md)
- [Create a Namespace](/reference/gwa-commands.md#namespacecreate)
- [Create a Service](/how-to/create-gateway-service.md)
  - API Providers with externally protected APIs should follow [this guide](/how-to/protected-externally.md) instead
- [Protect an API](/concepts/protect-api.md) (optional)

You should also be familiar with these concepts:

- [API Directory](/concepts/api-directory.md)

## Options

API listings in the Directory can be created and managed via:

- ⭐ **Command Line Interface (CLI)**
- **Web user interface (UI)**: Visit the [API Services Portal](https://api.gov.bc.ca/) and login to the API Provider zone.

!!! warning "Web UI limitations"
    At this time, not all steps required to create an API listing are possible through the web UI. Using the CLI is recommended.

## Environments

All API Directory functionality is accessible in both the `test` and
`production` environments. While you are encouraged to utilize the `test`
environment for experimentation and training purposes, if you already know the
details of the API you're building, you can add it directly to the production
Directory.

| Environment     | API Services Portal Directory Link                               |
| --------------- | ---------------------------------------------------------------- |
| TEST / TRAINING | https://api-gov-bc-ca.test.api.gov.bc.ca/devportal/api-directory |
| PRODUCTION      | https://api.gov.bc.ca/devportal/api-directory                    |

If using the `test` environment, set the host before logging in with `gwa`:

```linenums="0"
gwa config set host api-gov-bc-ca.test.api.gov.bc.ca
```

## Create a Dataset

First, you need a Dataset with metadata about your API. This information
helps consumers find your API in the Directory. If your API is already listed in
the [BC Data Catalogue](https://catalogue.data.gov.bc.ca/), skip ahead to [Link
Your Dataset to a Product](#link-your-dataset-to-a-product).

Start by writing up a DraftDataset in a local YAML file to apply using the `gwa`
CLI.

Here is the schema with example data, omitting some optional fields:

=== "YAML Template"
    ```yaml
    kind: DraftDataset
    name: dataset-name
    title: Useful API
    notes: A handy API with *many* uses.
    tags: [useful, data, openapi]
    organization: ministry-of-citizens-services
    organizationUnit: databc
    license_title: Open Government Licence - British Columbia
    view_audience: Government
    security_class: PUBLIC
    record_publish_date: "2021-05-27"
    ```

=== "YAML Template (w/ field descriptions)"
    ```yaml
    kind: DraftDataset # object type for gwa-cli use
    name: dataset-name # unique dataset name, not displayed
    title: Useful API # API title shown on the Directory
    notes: A handy API with *many* uses. # API description, supports Markdown formatting
    tags: [useful, data, openapi] # keywords, may be used for search in future
    organization: ministry-of-citizens-services # ministry or agency associated with the API (see https://api.gov.bc.ca/ds/api/v2/organizations for options) - this must match the organization associated with the namespace
    organizationUnit: databc # organization business sub-unit (see https://api.gov.bc.ca/ds/api/v2/organizations/<organization> for options)
    license_title: Open Government Licence - British Columbia # see https://bcgov.github.io/data-publication/pages/dps_licences.html for licensing options
    view_audience: Government # who can access the API
    security_class: PUBLIC # OCIO Information Security Classification Standard, see https://www2.gov.bc.ca/assets/gov/government/services-for-government-and-broader-public-sector/information-technology-services/standards-files/618_information_security_classification_standard.pdf
    record_publish_date: "2021-05-27" # date when the API was published
    ```

=== "JSON Template"
    ```json
    {
    "name": "dataset-name",
    "title": "Useful API",
    "notes": "A handy API with *many* uses.",
    "tags": [
        "useful",
        "data",
        "openapi"
    ],
    "organization": "ministry-of-citizens-services",
    "organizationUnit": "databc",
    "license_title": "Open Government Licence - British Columbia",
    "view_audience": "Government",
    "security_class": "PUBLIC",
    "record_publish_date": "2021-05-27"
    }
    ```

Check our [source
code](https://github.com/bcgov/api-services-portal/blob/dev/src/batch/data-rules.js#L116)
for up-to-date data rules for DraftDatasets.

!!! note "Link to your API"
    In the `notes` field, be sure to add a link to your API to allow interested consumers to find out more.
    Specifically, ensure there are links to the API specification and developer guide. 
    Use Markdown for formatting.
    For example:

    ```md
    notes: |
      Useful API is a versatile toolset for developers, offering a comprehensive suite of functions 
      and endpoints to streamline application development.

      Visit the [Useful API page](https://api.useful.com) to view the API spec and read the developer guide.
    ```

Now it's time to publish the Dataset:

=== "CLI"
    1. Login - `gwa login`
    2. Set the namespace - `gwa config set namespace <namespace-name>`
    3. Publish the DraftDataset - `gwa apply -i <draft-dataset.yaml>`

    You should see `✔ [DraftDataset] <dataset-name>: created`

## Link Your Dataset to a Product

It's time to create a *Product*, which describes the type of protection on the
API. Products are used to bundle Gateway Services and manage consumer access.

If you've already worked through the [Quick Start
tutorial](/tutorials/quick-start.md) or set up a GatewayService, you may already
have a Product.

Follow these steps to create a Product (if necessary), and link the Product with
the descriptive metadata in the Dataset:

=== "CLI"
    1. Create a Product configuration using the YAML template below
      (or modify an existing configuration).
      
      Specify your Dataset by `name` in the configuration: `dataset: <dataset-name>`.

      If your API is already listed in the [BC Data Catalogue](https://catalogue.data.gov.bc.ca/),
      use the slug value for `dataset` from the Data Catalogue dataset URL, `https://catalogue.data.gov.bc.ca/dataset/<api-slug-value>`.

      Add other available environments if desired (e.g. `dev`, `test`, `sandbox`).
        
      ```yaml title="Product YAML Template"
      kind: Product
      name: Useful API # Name shown on the API Directory
      dataset: dataset-name # Dataset name or BC Data Catalogue slug value
      environments:
      - name: prod
        active: false
      ```
    
    2. Publish the Product: `gwa apply -i <product.yaml>`
    

=== "Web UI"
    #### Create a Product

    1. Navigate to **Namespaces** -> **Products**.
    2. Click **New Product** in the top right.
   
    #### Link a Dataset

    Once you have a Product, associate the Product with a Dataset:

    1. Open the **Products** page in the API Services Portal.
    2. Click the ellipsis (**...**) next to **Add Env**, select **Edit Product**.
    3. In the **Link to BC Data Catalogue** text field, enter the `title` of your newly created or existing BCDC dataset.
    4. Click **Update**.
      
    !!! warning
        Search is exact. Be mindful of spaces and upper vs lowercase.

## Preview Your API Listing

Preview your new API listing by opening the API Directory and clicking the
**Your Products** tab. Confirm everything is as desired.

![New API card](/artifacts/new-api-directory-card.png)

## Enabling for Discovery

Once the content is complete and you have applied the appropriate controls to
your API, you are ready to make it available on the API Directory.

!!! note "Prerequisite: Add Organization"
    Before sharing your API on the API
    Directory, you must add your Organization and Business Unit to your
    Namespace. If you have yet to complete this you will see a banner on the
    Namespaces page on the API Service Portal asking you to **Add
    Organization**. You will then need to wait for approval from the
    Organization Administrator.

Enable an environment to display the API in the API Directory. You can
individually enable each environment (dev, test, prod).

Enable environments by either updating the Product Environment configuration
YAML to `active: true`, or on the API Services Portal > **Product** page -> **Edit**
the Environment details -> check **Enable Environment**.

## View Your Product in the API Directory

Find your API in the **API Directory**.

It is now ready to receive access requests from the community!

Documentation on how to grant and manage your API consumer access is coming soon.
