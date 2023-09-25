---
order: 2200
---

# API Discovery

## Share your API for Discovery

Package your APIs and make them available for discovery through the API Services Portal and BC Data Catalogue.

The `API Services Portal` Directory organizes your APIs by Datasets, Products and Environments. You can manage them via the CLI, the API or through the UI.

Go to [Gateway Administration](../resources/gateway-admin.md#directory-api) for links to the Directory API.

## Setup your Draft Dataset

If you do not have a Dataset already defined in the BC Data Catalogue, you can create a draft in the API Services Portal:

1. Click `Help` in the top right, then `API Docs`
2. Click the green `Authorize` button, then enter your Client ID and Secret
3. Click the `PUT /namespaces/{ns}/datasets` accordion item
4. Click `Try it out`, enter your namespace, personalize any fields in the Request body, remove the lines pertaining to organization, and click `Execute`
5. Scroll down and ensure a 200 Response was received

```yaml
kind: DraftDataset
name: my-draft-dataset
organization: ministry-of-citizens-services
organizationUnit: databc
notes: Some information about this API
tags: [health, standards, openapi]
sector: Service
license_title: Access Only
view_audience: Government
security_class: LOW-PUBLIC
record_publish_date: "2021-05-27"
```

> List of available organizations:
>
> https://api-gov-bc-ca.test.api.gov.bc.ca/ds/api/v2/organizations

> Use the following to get the `organizationUnit`:
>
> https://api-gov-bc-ca.test.api.gov.bc.ca/ds/api/v2/console/#/Organizations/organization-units

## Setup your Product

How to add a Product:

1. Navigate to Namespaces -> Products
2. Click `New Product` in the top right

How to associate Product with a Dataset:

1. Click the ellipses next to Add Env
2. Find your newly created dataset and click Update

> There are various patterns for protecting an API that the Kong API Gateway supports. In the following example, the API is protected with Kong's API Key and ACL plugins (`kong-api-key-acl` flow).

```yaml
kind: Product
appId: 2B04C28E08AW
name: My API
dataset: my-draft-dataset
environments:
  - id: 1F7CA929
    name: dev
    active: false
    approval: false
    legal: terms-of-use-for-api-gateway-1
    flow: kong-api-key-acl
    additionalDetailsToRequest: Please provide a bit more of this
    services: []
  - id: 2F7CA929
    name: test
    active: false
    approval: true
    legal: terms-of-use-for-api-gateway-1
    flow: kong-api-key-acl
    additionalDetailsToRequest: Asking for test environment? Please provide some more info
    services: [a-service-for-$NS]
  - id: 3F7CA929
    name: prod
    active: false
    approval: true
    legal: terms-of-use-for-api-gateway-1
    flow: client-credentials
    credentialIssuer: Resource Server $NS
    additionalDetailsToRequest: Production? Great, please provide X, Y and Z
    services: []
```

## Update Gateway Configuration

In the previous section the example defined an environment that is protected using Kong's API Key and ACL plugins. To protect the Service, the corresponding plugins need to exist on the Gateway for that service or route. The ACL `allow` corresponds to the unique `Environment ID` defined in Section 9.2.

```
  plugins:
  - name: key-auth
    tags: [ ns.$NS ]
    protocols: [ http, https ]
    config:
      key_names: ["X-API-KEY"]
      run_on_preflight: true
      hide_credentials: true
      key_in_body: false
  - name: acl
    tags: [ ns.$NS ]
    config:
      hide_groups_header: true
      allow: [ <SEE ENVIRONMENT DETAIL> ]
```

How to Update Gateway Configuration:

1. In Namespaces -> Products, click edit next to product environment
2. For Authorization, choose Kong API Key with ACL Flow. Assign Terms of Use if desired.
3. Check Require Approval
4. Click View Plugin Template, and add the plugin configuration to the service `a-service-for-$NS` in the `gwconfig.yaml` file you created in Section 3.
5. Re-run the publish command: `./gwa pg gwconfig.yaml`. This will protect the upstream service with an API Key.
6. Back in the portal, click Continue
7. Drag and drop the available service to Active Services
8. Click Save

## Enabling for Discovery

Once the content is complete and you have applied the appropriate controls to your API, you are ready to make it available on the API Directory.

**Prerequisite:** Your namespace must be approved for use by a Ministry Organization Administrator. This is a one-time process to link the Ministry to the Namespace and can be requested here: https://dpdd.atlassian.net/servicedesk/customer/portal/1/group/2/create/118

Once approved, you must make an Environment `active` for the corresponding Product Environment to appear in the API Directory. You can do this by either updating the Product Environment configuration above to `active: true`, or going to the API Services Portal UI and editing the Environment details.

## View Your Product in the API Directory

Find your API in the `API Services Portal Directory`.

| Environment     | API Services Portal Directory Link                               |
| --------------- | ---------------------------------------------------------------- |
| TEST / TRAINING | https://api-gov-bc-ca.test.api.gov.bc.ca/devportal/api-directory |
| PRODUCTION      | https://api.gov.bc.ca/devportal/api-directory                    |

It is now ready to receive access requests from the community!
