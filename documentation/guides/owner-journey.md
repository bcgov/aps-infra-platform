# API Provider User Journey

The following steps walk an API Owner through setting up an API on the BC Gov API Gateway in our Test instance. If you are ready to deploy to our Production instance, use the links found at the bottom of this document ([here](#production-links)).

## 1. Register a new namespace

A `namespace` represents a collection of Kong Gateway Services and Routes that are managed independently.

To create a new namespace, login to the [API Services Portal](https://api-gov-bc-ca.test.api.gov.bc.ca).

After login with your IDIR, click the namespace dropdown in the top right next to your user name (it may show `No Active Namespace`), then click `Create New Namespace`.

The namespace must be an lowercase alphanumeric string between 5 and 15 characters (RegExp reference: `^[a-z][a-z0-9-]{4,14}$`).

You can select and manage namespaces by clicking the namespace dropdown in the top right next to your user name.

## 2. Generate a Service Account

Go to the `Namespaces` tab, click the `Service Accounts` action link, and click the `New Service Account` button. Select the `GatewayConfig.Publish` permissions for the Service Account and click `Share`. A new credential will be created - make a note of the `ID` and `Secret`.

The available Scopes are:

| Scope                    | Permission                                                                                                                                                                               |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Namespace.Manage`       | Permission to update the Access Control List for controlling access to viewing metrics, service configuration and service account management (effectively a superuser for the namespace) |
| `Namespace.View`         | Read-only access to the namespace                                                                                                                                                        |
| `GatewayConfig.Publish`  | Permission to publish gateway configuration to Kong and to view the status of the upstreams                                                                                              |
| `Content.Publish`        | Permission to update the documentation on the portal                                                                                                                                     |
| `CredentialIssuer.Admin` | Permission to create Authorization Profiles so that they are available to be used when configuring Product Environments                                                                  |
| `Access.Manage`          | Permission to approve/reject access requests to your APIs that you make discoverable                                                                                                     |

## 3. Prepare configuration

The gateway configuration can be hand-crafted or you can use a command line interface that we developed called `gwa` to convert your Openapi v3 spec to a Kong configuration.

**Basic configuration of a single service and route:**

```bash
export NS="my_namespace"
export NAME="a-service-for-$NS"
echo "
services:
- name: $NAME
  host: httpbin.org
  tags: [ ns.$NS ]
  port: 443
  protocol: https
  retries: 0
  routes:
  - name: $NAME-route
    tags: [ ns.$NS ]
    hosts:
    - $NAME.api.gov.bc.ca
    paths:
    - /
    methods:
    - GET
    strip_path: false
    https_redirect_status_code: 426
    path_handling: v0
" > sample.yaml
```

Review the `sample.yaml` file to see what it is doing. There is a single upstream service defined to be `httpbin.org`, and a single route `$NAME.api.gov.bc.ca` that passes all `GET` requests to the upstream service.

> To view common plugin config go to [Common Controls](../gateway-plugins/COMMON-CONFIG.md)

> To view some other plugin navigation to `Gateway > Plugins`.

> **Declarative Config** Behind the scenes, DecK is used to sync your configuration with Kong. For reference: https://docs.konghq.com/deck/overview/

> **Splitting Your Config:** A namespace `tag` with the format `ns.$NS` is mandatory for each service/route/plugin. But if you have separate pipelines for your environments (i.e./ dev, test and prod), you can split your configuration and update the `tags` with the qualifier. So for example, you can use a tag `ns.$NS.dev` to sync Kong configuration for `dev` Service and Routes only.

> **Upstream Services on OCP4:** If your service is running on OCP4, you should specify the Kubernetes Service in the `Service.host`. It must have the format: `<name>.<ocp-namespace>.svc`. Also make sure your `Service.port` matches your Kubernetes Service Port. Any Security Policies for egress from the Gateway will be setup automatically on the API Gateway side.
> The Aporeto Network Security Policies are being removed in favor of the Kubernetes Security Policies (KSP). You will need to create a KSP on your side looking something like this to allow the Gateway's test and prod environments to route traffic to your API:

```yaml
kind: NetworkPolicy
apiVersion: networking.k8s.io/v1
metadata:
  name: allow-traffic-from-gateway-to-your-api
spec:
  podSelector:
    matchLabels:
      name: my-upstream-api
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              environment: test
              name: 264e6f
    - from:
        - namespaceSelector:
            matchLabels:
              environment: prod
              name: 264e6f
```

> **Migrating from OCP3 to OCP4?** Please review the [OCP4-Migration](https://github.com/bcgov/gwa-api/blob/dev/docs/OCP4-MIGRATION.md) instructions to help with transitioning to OCP4 and the new APS Gateway.

> **Require mTLS between the Gateway and your Upstream Service?** To support mTLS on your Upstream Service, you will need to provide client certificate details and if you want to verify the upstream endpoint then the `ca_certificates` and `tls_verify` is required as well. An example:

```yaml
services:
  - name: my-upstream-service
    host: my-upstream.site
    tags: [_NS_]
    port: 443
    protocol: https
    tls_verify: true
    ca_certificates: [0a780ee0-626c-11eb-ae93-0242ac130012]
    client_certificate: 8fc131ef-9752-43a4-ba70-eb10ba442d4e
    routes: [...]
certificates:
  - cert: "<PEM FORMAT>"
    key: "<PEM FORMAT>"
    tags: [_NS_]
    id: 8fc131ef-9752-43a4-ba70-eb10ba442d4e
ca_certificates:
  - cert: "<PEM FORMAT>"
    tags: [_NS_]
    id: 0a780ee0-626c-11eb-ae93-0242ac130012
```

> NOTE: You must generate a UUID (`python -c 'import uuid; print(uuid.uuid4())'`) for each certificate and ca_certificate you create (set the `id`) and reference it in your `services` details.

> HELPER: Python command to get a PEM file on one line: `python -c 'import sys; import json; print(json.dumps(open(sys.argv[1]).read()))' my.pem`

#### Using an OpenAPI Spec Document (optional)

Run: `gwa new` and follow the prompts.

Example:

```bash
gwa new -o sample.yaml \
  --route-host myapi.api.gov.bc.ca \
  --service-url https://httpbin.org \
  https://bcgov.github.io/gwa-api/openapi/simple.yaml
```

> See below for the `gwa` CLI install instructions.

## 4. Apply gateway configuration

The Swagger console for the `gwa-api` can be used to publish Kong Gateway configuration, or the `gwa Command Line` can be used.

### 4.1. gwa Command Line (recommended)

**Install (for Linux)**

```bash
GWA_CLI_VERSION=v1.3.1; curl -L -O https://github.com/bcgov/gwa-cli/releases/download/${GWA_CLI_VERSION}/gwa_${GWA_CLI_VERSION}_linux_x64.zip
unzip gwa_${GWA_CLI_VERSION}_linux_x64.zip
./gwa --version
```

> **Using MacOS or Windows?** Download here: [https://github.com/bcgov/gwa-cli/releases/tag/v1.3.1](https://github.com/bcgov/gwa-cli/releases/tag/v1.3.1)

> NOTE: As of version 1.2+ there is support for v2 of our api. To continue using v1 of the api, ensure that the API Version is set to 1 (see below)

**Configure**

Create a `.env` file and update the CLIENT_ID and CLIENT_SECRET with the new credentials that were generated in step #2:

Run the following to configure the `.env` file:

```
gwa init -T --api-version=2 --namespace=$NS \
  --client-id=<YOUR SERVICE ACCOUNT ID> \
  --client-secret=<YOUR SERVICE ACCOUNT SECRET>`
```

> NOTE: The `-T` indicates our Test environment. For production use `-P`.

Run `gwa status` to confirm that access to the Gateway is working.

**Publish**

```bash
gwa pg sample.yaml
```

If you want to see the expected changes but not actually apply them, you can run:

```bash
gwa pg --dry-run sample.yaml
```

### 4.2. Swagger Console (optional)

Go to [gwa-api Swagger Console](https://gwa-api-gov-bc-ca.test.api.gov.bc.ca/docs/).

Select the `PUT` `/namespaces/{namespace}/gateway` API.

The Service Account uses the OAuth2 Client Credentials Grant Flow. Click the `lock` link on the right and enter in the Service Account credentials that were generated in step #2.

For the `Parameter namespace`, enter the namespace that you created in step #1.

Select `dryRun` to `true`.

Select a `configFile` file.

Send the request.

### 4.3. Postman (optional)

From the Postman App, click the `Import` button and go to the `Link` tab.

Enter a URL: https://openapi-to-postman-api-gov-bc-ca.test.api.gov.bc.ca/?u=https://gwa-api-gov-bc-ca.test.api.gov.bc.ca/docs/v2/openapi.yaml

After creation, go to `Collections` and right-click on the `Gateway Administration (GWA) API` collection and select `edit`.

Go to the `Authorization` tab, enter in your `Client ID` and `Client Secret` and click `Get New Access Token`.

You should get a successful dialog to proceed. Click `Proceed` and `Use Token`.

You can then verify that the token works by going to the Collection `Return key information about authenticated identity` and click `Send`.

## 5. Verify routes

To verify that the Gateway can access the upstream services, run the command: `gwa status`.

In our `test` environment, the hosts that you defined in the routes get altered; to see the actual hosts, log into the [API Services Portal](https://api-gov-bc-ca.test.api.gov.bc.ca), go to the `Namespaces` tab, go to `Gateway Services` and select your particular service to get the routing details.

```bash
curl https://${NAME}-api-gov-bc-ca.test.api.gov.bc.ca/headers

ab -n 20 -c 2 https://${NAME}-api-gov-bc-ca.test.api.gov.bc.ca/headers

```

To help with troubleshooting, you can use the GWA API to get a health check for each of the upstream services to verify the Gateway is connecting OK.

## 6. View metrics

The following metrics can be viewed in real-time for the Services that you configure on the Gateway:

- **Request Rate** : Requests / Second (by Service/Route, by HTTP Status)
- **Latency** : Standard deviations measured for latency inside Kong and on the Upstream Service (by Service/Route)
- **Bandwidth** : Ingress/egress bandwidth (by Service/Route)
- **Total Requests** : In 5 minute windows (by Consumer, by User Agent, by Service, by HTTP Status)

All metrics can be viewed by an arbitrary time window - defaults to `Last 24 Hours`.

Go to [Grafana](https://grafana-apps-gov-bc-ca.test.api.gov.bc.ca) to view metrics for your configured services.

You can also access summarized metrics from the `API Services Portal` by going to the `Namespaces` tab and clicking the `Gateway Services` link.

## 7. Grant access to others

To grant access to others, you need to grant them the appropriate Scopes. This can be done from the `API Services Portal`, selecting the relevant `Namespace` and going to the Namespaces `Namespace Access` page. From here, you are able to grant Users access to the Namespace.

## 8. Add to your CI/CD Pipeline

Update your CI/CD pipelines to run the `gwa-cli` to keep your services updated on the gateway.

### 8.1. Github Actions Example

In the repository that you maintain your CI/CD Pipeline configuration, use the Service Account details from `Step 2` to set up two `Secrets`:

- GWA_ACCT_ID

- GWA_ACCT_SECRET

Add a `.gwa` folder (can be called anything) that will be used to hold your gateway configuration.

An example Github Workflow:

```yaml
env:
  NS: "<your namespace>"

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
        with:
          fetch-depth: 0

      - uses: actions/setup-node@v1
        with:
          node-version: 10
          TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Get GWA Command Line
        run: |
          curl -L -O https://github.com/bcgov/gwa-cli/releases/download/v1.3.1/gwa_v1.3.1_linux_x64.zip
          unzip gwa_v1.3.1_linux_x64.zip
          export PATH=`pwd`:$PATH

      - name: Apply Namespace Configuration
        run: |
          export PATH=`pwd`:$PATH
          cd .gwa/$NS

          gwa init -T \
            --namespace=$NS \
            --client-id=${{ secrets.TEST_GWA_ACCT_ID }} \
            --client-secret=${{ secrets.TEST_GWA_ACCT_SECRET }}

          gwa pg
```

## 9. Share your API for Discovery

Package your APIs and make them available for discovery through the API Services Portal and BC Data Catalog.

The `API Services Portal` Directory organizes your APIs by Datasets, Products and Environments. You can manage them via an API or through the UI.

To use the Directory API, the following scopes are required:

- For `contents` (documentation), the service account must have the `Content.Publish` scope
- For `datasets`, `products` and `environments`, the service account must have the `Namespace.Manage` scope
- For `credential issuers`, the service account must have the `CredentialIssuer.Admin` scope

View the Directory API:

- **V1:** [V1 Directory API Console](https://openapi-apps-gov-bc-ca.test.api.gov.bc.ca/?url=https://api-gov-bc-ca.test.api.gov.bc.ca/ds/api/openapi.yaml)
- **V2:** [V2 Directory API Console](https://openapi-apps-gov-bc-ca.test.api.gov.bc.ca/?url=https://api-gov-bc-ca.test.api.gov.bc.ca/ds/api/v2/openapi.yaml)

### 9.1 Setup your Draft Dataset

If you do not have a Dataset already defined in the BC Data Catalog, then you can create a draft in the API Services Portal.

> Find the list of organizations here:
>
> https://api-gov-bc-ca.test.api.gov.bc.ca/ds/api/v2/organizations

> Use the following to get the `organizationUnit`:
>
> https://api-gov-bc-ca.test.api.gov.bc.ca/ds/api/v2/organizations/ORG_KEY

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

### 9.2 Setup your Product

> There are various patterns for protecting an API that the Kong API Gateway supports. In this example, we will be protecting the API with Kong's API Key and ACL plugins (`kong-api-key-acl` flow).

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

### 9.3 Update Gateway Configuration

In the previous section our example defines an environment that is protected using Kong's API Key and ACL plugins. To protect the Service, the corresponding plugins need to exist on the Gateway for that service or route. The ACL `allow` corresponds to the unique `Environment ID` defined in section 9.2.

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

Add the plugin configuration to the service `a-service-for-$NS` in `sample.yaml` file that you created in section 3.

Re-run the publish command: `gwa pg`. This will protect the upstream service with an API Key.

### 9.4 Check Access

```
curl https://${NAME}-api-gov-bc-ca.test.api.gov.bc.ca/headers
```

You should get an error: "No API key found in request".

### 9.5 Get an API Key

Go to the `Namespaces` tab in the `API Services Portal`. Click the `Preview in Directory` link that is in the `Products` panel.

You should see a card with the title of your Dataset that you created earlier in step 9.1.

Click on the title and click the `Request Access` button.

Choose or create an `Application`, select the `Dev` environment and click the "Request Access & Continue" button.

The `Generate Secrets` button will generate your API Key. Make a note of it.

> NOTE: An Environment can be configured be auto-approved. For our sample `Dev`, auto-approval is enabled so the Access Manager does not need to approve the request before getting access.

Now, when you run the command:

```
curl https://${NAME}-api-gov-bc-ca.test.api.gov.bc.ca/headers -H "X-API-KEY: $KEY"
```

It should return header information looking something like:

```
{
  "headers": {
    "Accept": "*/*",
    "User-Agent": "curl/7.64.1",
    "X-Consumer-Custom-Id": "8ED11248-072EBB2791974533",
    "X-Consumer-Id": "db3a0658-c049-430e-b143-ce46685d8e20",
    "X-Consumer-Username": "8ED11248-072EBB2791974533",
    "X-Credential-Identifier": "a91bb07c-41a9-49b6-9481-155e9fd68dba"
  }
}
```

### 9.6 Manage Access

> Note: To manage access to your APIs, you must have the `Access.Manage` role for the Namespace.

As an API Provider, you can manage this new Consumer by going to the `Namespaces` tab, and selecting `Consumers`.

Here you should see the newly created Consumer. Click on the `name`.

Administer Controls, such as rate limiting and ip restrictions.

Administer Authorization, by toggling access to the particular Product and Environment.

### 9.7 Enabling for Discovery

Once you are happy with the content and have applied the appropriate controls to your API, you can do the following to publish to the API Directory.

Your namespace must be approved for use by a Ministry Organization Administrator. This is a one-time process to link the Ministry to the Namespace and can be requested here: https://dpdd.atlassian.net/servicedesk/customer/portal/1/group/2/create/118

Once approved, you just need to make an Environment `active` for the corresponding Product and Dataset to appear on the API Directory. You can do this by either updating the Product Environment configuration above to `active: true`, or going to the API Services Portal UI and editing the Environment details.

### 9.8 View your product in the API Directory

Find your API in the [API Services Portal Directory](https://api-gov-bc-ca.test.api.gov.bc.ca/devportal/api-directory)

It is now ready to receive access requests from the community!

## 10 What to try next?

### 10.1 Connect with the BC Government API community

Message us on [Rocket.Chat #aps-ops](https://chat.developer.gov.bc.ca/channel/aps-ops).

### 10.2 Read our other guides

Find information about authentication and authorization patterns, reference implementations, plugin usage and much more.

### 10.3 Protect your API using an external Identity Provider

Use the `client-credentials` flow to protect your API (see [Client Credential Protection](tutorial-idp-client-cred-flow/))

### 10.4 Use the access approval process

Enable `approval` for an Environment and then go through the access request process by requesting access, and then as an Access Manager, reviewing the request and approving or rejecting it.

### 10.5 Publish your documentation on the Portal

```yaml
kind: Content
title: Getting Started with Example API
description: Getting Started with Example API
externalLink: https://github.com/bcgov/$NS/getting_started.md
content: "all markdown content"
order: 1
tags: [ns.$NS]
isComplete: true
isPublic: true
publishDate: "2021-06-02T08:00:00.000-08:00"
```

## Production Links

- [API Services Portal](https://api.gov.bc.ca)
- [gwa-api Swagger Console](https://gwa.api.gov.bc.ca/docs/)
- [gwa-api Postman Collection](https://openapi-to-postman.api.gov.bc.ca/?u=https://gwa.api.gov.bc.ca/docs/v2/openapi.yaml)
- [Gateway Metrics - Grafana](https://grafana.apps.gov.bc.ca)
