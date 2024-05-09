---
title: API Directory
---

The [API Directory](https://api.gov.bc.ca/devportal/api-directory) enables you to
package your APIs and make them available for discovery by developers and other
API consumers, across BC Government and beyond.

By listing your API in the API Directory, you also gain access to tools for
managing your API consumers through access requests and approvals.

## API listings

The API Directory shows available APIs through API listings. Each listing features
one API and is visible as a card on the API Directory's main page.

![BC Route Planner API card](/artifacts/api-directory-card.png)

Cards show basic metadata about the API: the API name (`title`), associated ministry
(`organization`), description (`notes`), and available environments. This metadata
is defined in a Dataset.

Despite the name "dataset", don't think that all API's need to serve *data*. Many
API's provide services, for example, the [BC Route Planner API](https://api.gov.bc.ca/devportal/api-directory/740?preview=false)
returns vehicle routes between start and end points.

!!! note
    Think of Datasets as API metadata records.

Clicking on the API name opens the full API listing details.

![BC Route Planner API listing details](/artifacts/api-directory-listing.png)

Here, additional metadata details defined in the Dataset are visible, as well as
the associated Products which consumers can request access to.

!!! note "Products"
    *Products* bundle one or more Gateway Services which are protected in the
    same way. They are used to manage consumer access.
