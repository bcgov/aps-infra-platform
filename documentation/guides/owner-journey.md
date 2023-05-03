# API Provider User Journey

The following steps guide an API Provider through setting up an API on the BC Government API Gateway in a Test/Training instance. If you are ready to deploy to the Production instance, use the links available at the end of this document ([here](#production-links)).

## 1. Register a New Namespace

A `namespace` represents a collection of Kong Gateway Services and Routes that are managed independently.

Create a new namespace:

1. Log in to the [API Services Portal](https://api-gov-bc-ca.test.api.gov.bc.ca) as an `API Provider` using your IDIR.

2. Click the namespace drop-down menu (top right next to your user name - it may show `No Active Namespace`).

3. Click `Create New Namespace`.

4. Enter the Namespace name.

5. Click Create.

> NOTE: The name must be a lowercase alphanumeric string between 5 and 15 characters (RegExp reference: `^[a-z][a-z0-9-]{4,14}$`).

You can manage namespaces by clicking the namespace drop-down menu and selecting the required namespace.

## 2. Generate a Service Account

1. Go to the `Namespaces` tab.

2. Click `Service Accounts`, then Cick `New Service Account`.

3. Select the `GatewayConfig.Publish` permission for the Service Account and click `Share`. A new credential will be created - make a note of the `ID` and `Secret`.

> NOTE: Make sure to save the generated Client ID and Secret.

The following list describes the permissions:

| Scope                    | Permission                                                                                                                                                                               |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Namespace.Manage`       | Permission to update the Access Control List for controlling access to viewing metrics, service configuration and service account management (effectively a superuser for the namespace) |
| `Namespace.View`         | Read-only access to the namespace                                                                                                                                                        |
| `GatewayConfig.Publish`  | Permission to publish gateway configuration to Kong and view the status of the upstreams                                                                                                 |
| `Content.Publish`        | Permission to update the documentation on the portal                                                                                                                                     |
| `CredentialIssuer.Admin` | Permission to create Authorization Profiles for integrating with third-party Identity Providers; yhe profiles are available to be used when configuring Product Environments             |
| `Access.Manage`          | Permission to approve/reject access requests to your APIs                                                                                                                                |

## 3. Prepare Configuration

The gateway configuration can be hand-crafted or you can use a command line interface that APS developed called `gwa` to convert your OpenAPI v3 spec to a Kong configuration.

**Run the following commands to create a basic configuration of a single service and route:**

```bash
export NS="<YOUR NAMESPACE>"
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
    request_buffering: true
    response_buffering: true
" > gwconfig.yaml
```

Review the `gwconfig.yaml` file to see what it is doing. There is a single upstream service defined to be `httpbin.org`, and a single route `$NAME.api.gov.bc.ca` that passes all `GET` requests to the upstream service.

> To view common plugin configuration go to [Common Controls](../gateway-plugins/COMMON-CONFIG.md)

> To learn about other available plugins, navigate to `Gateway > Plugins`.

> **Declarative Config:** DecK is used to sync your configuration with Kong; see https://docs.konghq.com/deck/overview/ for more information.

> **Splitting Your Config:** A namespace `tag` with the format `ns.$NS` is mandatory for each service/route/plugin. But, if you have separate pipelines for your environments (i.e., dev, test and prod), you can split your configuration and update the `tags` with the qualifier. For example, you can use a tag `ns.$NS.dev` to sync the Kong configuration for `dev` Service and Routes only.

### OCP Network Policies

> If your service is running on the Openshift platform, you should specify the Kubernetes Service in the `Service.host`. It must have the format: `<name>.<ocp-namespace>.svc`. Also, make sure your `Service.port` matches your Kubernetes Service Port. Any Security Policies for egress from the Gateway will be setup automatically on the API Gateway side.

The Kong Gateway runs Data Planes in both Silver and Gold clusters.

**Silver Cluster**

You will need to create a Network Policy on your side similar to the following to allow the Gateway's test and prod environments to route traffic to your API:

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

**Gold Cluster**

If your service is running on Gold, you will need to contact the APS team so that we can properly provision the `namespace` on the correct Kong Data Plane and ensure the correct DNS is setup for your routes. The following is the Network Policy on Gold.

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
              name: b8840c
    - from:
        - namespaceSelector:
            matchLabels:
              environment: prod
              name: b8840c
```

### Private Routing

By default, publically available endpoints are created based on Kong Routes where the hosts must end with `*.api.gov.bc.ca` or `*.apps.gov.bc.ca`.

There are use cases where the clients that are consuming the API are on the same Openshift platform that the API is deployed to. In this case, there is a security benefit of not making the API endpoints publically available.

To support this, the route `hosts` can be updated with a host that follows the format: `<api-name>.cluster.local`. When the configuration is published to Kong, an Openshift Service is created with a corresponding Service Serving Certificate (SSC), which is routeable from within the Openshift cluster.

An example Gateway configuration for an upstream API deployed in the Silver cluster would be:

```yaml
services:
  - name: my-service
    host: httpbin.org
    tags: [ns.$NS]
    port: 443
    protocol: https
    retries: 0
    routes:
      - name: my-service-route
        tags: [ns.$NS]
        hosts:
          - my-service.cluster.local
```

A new endpoint is then created in our Silver Test environment as: https://gw-my-service.264e6f-test.svc.cluster.local (if it was configured in our Prod environment, it would be: https://gw-my-service.264e6f-prod.svc.cluster.local)

To verify that the endpoint is callable, you can deploy a simple pod that mounts the `service-ca` to be used for verifying the SSC.

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: tmp-ca
  annotations:
    service.beta.openshift.io/inject-cabundle: "true"
data: {}
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: tmp-deployment
  labels:
    app: sleeper
spec:
  replicas: 1
  selector:
    matchLabels:
      app: sleeper
  template:
    metadata:
      labels:
        app: sleeper
    spec:
      volumes:
        - name: config
          configMap:
            name: tmp-ca

      containers:
        - name: idle
          image: docker.io/curlimages/curl:latest
          command: ["sh"]
          args:
            - -c
            - |
              sleep Infinite
          ports:
            - containerPort: 80
          volumeMounts:
            - name: config
              mountPath: "/config"
              readOnly: true
```

From the Pod's Terminal, you can then run:

```bash
curl -v --cacert /config/service-ca.crt \
  https://gw-my-service.264e6f-prod.svc.cluster.local/uuid
```

You should see a 200 response with a valid UUID.

### Upstream mTLS

> **Require mTLS between the Gateway and your Upstream Service?** To support mTLS on your Upstream Service, you will need to provide client certificate details and if you want to verify the upstream endpoint then the `ca_certificates` and `tls_verify` is required as well. Example:

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

### Using an OpenAPI Spec

Run: `./gwa new` and follow the prompts.

Example:

```bash
./gwa new -o sample.yaml \
  --route-host myapi.api.gov.bc.ca \
  --service-url https://httpbin.org \
  https://bcgov.github.io/gwa-api/openapi/simple.yaml
```

> See below for the `gwa` CLI install instructions.

## 4. Apply Gateway Configuration

The Swagger console for the `gwa-api` can be used to publish the Kong Gateway configuration, or you can use the `gwa Command Line`.

### 4.1. gwa Command Line (recommended)

**Install (for Linux)**

```bash
GWA_CLI_VERSION=v1.3.1; curl -L -O https://github.com/bcgov/gwa-cli/releases/download/${GWA_CLI_VERSION}/gwa_${GWA_CLI_VERSION}_linux_x64.zip
unzip gwa_${GWA_CLI_VERSION}_linux_x64.zip
./gwa --version
```

> **Using MacOS or Windows?** Download here: [https://github.com/bcgov/gwa-cli/releases/tag/v1.3.1](https://github.com/bcgov/gwa-cli/releases/tag/v1.3.1)

> NOTE: As of version 1.2+ there is support for v2 of the APS API. To continue using v1 of the API, ensure that the API Version is set to 1.

**Configure**

Run the following to configure a `.env` file that will hold all the env vars for running `gwa`:

```
./gwa init -T --api-version=2 --namespace=<YOUR NAMESPACE> \
  --client-id=<YOUR SERVICE ACCOUNT ID> \
  --client-secret=<YOUR SERVICE ACCOUNT SECRET>`
```

> NOTE: Use the Client ID and Secret obtained from step 2.

> NOTE: The `-T` indicates the APS Test environment. For production use `-P`.

Run `./gwa status` to confirm that access to the Gateway is working.

**Publish**

```bash
./gwa pg gwconfig.yaml
```

If you want to see the expected changes, but not actually apply them, you can run:

```bash
./gwa pg --dry-run gwconfig.yaml
```

### 4.2. Swagger Console (optional)

Go to [gwa-api Swagger Console](https://openapi.apps.gov.bc.ca?url=https://gwa-api-gov-bc-ca.test.api.gov.bc.ca/docs/v2/openapi.yaml).

Select the `PUT` `/namespaces/{namespace}/gateway` API.

The Service Account uses the OAuth2 Client Credentials Grant Flow. Click the `lock` link (on the right) and enter the Service Account credentials generated in Section 2.

For the `Parameter namespace`, enter the namespace you created in Section 1.

Set `dryRun` to `true`.

Select a `configFile` file.

Send the request.

### 4.3. Postman (optional)

From the Postman App, click `Import` and go to the `Link` tab.

Enter the URL: https://openapi-to-postman.api.gov.bc.ca/?u=https://gwa-api-gov-bc-ca.test.api.gov.bc.ca/docs/v2/openapi.yaml

After creation, go to `Collections` and right-click on the `Gateway Administration (GWA) API` collection and select `edit`.

Go to the `Authorization` tab, enter your `Client ID` and `Client Secret`, and click `Get New Access Token`.

You should get a successful dialog to proceed. Click `Proceed` and `Use Token`.

You can verify that the token works by going to the Collection `Return key information about authenticated identity` and clicking `Send`.

### 4.4. Helm Chart

There is a helm chart available that provisions resources on the API Gateway, API Services Portal and OCP (Network Policy).

The helm chart is located at: https://github.com/bcgov/helm-charts/tree/master/charts/aps-gateway-ns

The chart creates Jobs to provision the resources, and it expects secrets to be setup in the common Hashicorp Vault https://vault.developer.gov.bc.ca instance.

Prepare a `config.yaml` file:

- update the security context for the particular OCP project
- the license plate `af9xxx` can be replaced with your own OCP license plate
- the secret `example-dev` should be the name of the secret that has the following keys defined (information from a APS Portal namespace Service Account):
  - GWA_ACCT_ID
  - GWA_ACCT_SECRET
  - NAMESPACE
  - TOKEN_URL
  - GWA_INIT_FLAG : Set to either `-T` or `-P` representing the API Gateway environment
- update the Pod matching `networkPolicy.matchLabels` for the Network Policy for Ingress traffic from the API Gateway

```yaml
podSecurityContext:
  fsGroup: 1013540000

securityContext:
  runAsUser: 1013540000

serviceAccount:
  create: false
  name: af9xxx-vault

vault:
  authPath: auth/k8s-silver
  namespace: platform-services
  role: xxxxxx-nonprod
  secret: xxxxxx-nonprod/aps-gateway-creds

networkPolicy:
  create: true
  namespaces: [xxxxxx-dev, xxxxxx-test, xxxxxx-prod]
  matchLabels:
    app.kubernetes.io/name: my-api

services: []

directoryConfig:
  products: []
  issuers: []
  datasets: []
```

The yaml created earlier for the API Gateway (`gwconfig.yaml`) can be used as part of the helm configuration.

Run Helm to install the Jobs:

```
helm repo add bcgov https://bcgov.github.io/helm-charts
helm upgrade --install example -f config.yaml -f gwconfig.yaml bcgov/aps-gateway-ns
```

## 5. Verify Routes

To verify that the Gateway can access the upstream services, run the command: `./gwa status`.

In the APS `test` environment, the hosts that you defined in the routes are altered. To see the actual hosts, log into the [API Services Portal](https://api-gov-bc-ca.test.api.gov.bc.ca), go to the `Namespaces` tab, go to `Gateway Services`, and select your particular service to get the routing details.

```bash
curl https://${NAME}-api-gov-bc-ca.test.api.gov.bc.ca/headers

ab -n 20 -c 2 https://${NAME}-api-gov-bc-ca.test.api.gov.bc.ca/headers

```

## 6. View Metrics

You can view the following metrics in real-time for the Services that you configure on the Gateway:

- **Request Rate**: Requests / Second (by Service/Route, by HTTP Status)
- **Latency**: Standard deviations measured for latency inside Kong and on the Upstream Service (by Service/Route)
- **Bandwidth**: Ingress/egress bandwidth (by Service/Route)
- **Total Requests**: In 5 minute windows (by Consumer, by User Agent, by Service, by HTTP Status)

All metrics can be viewed by an arbitrary time window; default is `Last 24 Hours`.

Go to [Grafana](https://grafana-apps-gov-bc-ca.test.api.gov.bc.ca) to view metrics for your configured services.

You can also access summarized metrics from the `API Services Portal` by going to the `Namespaces` tab and clicking the `Gateway Services` link.

> NOTE: A shortcut to Grafana is provided from the `Gateway Services` page by clicking `View metrics in real-time`.

## 7. Grant Access to Other Users

To grant access to other users, you need to grant them the appropriate Scopes. You can do this from the `API Services Portal` by selecting the relevant `Namespace` and going to the Namespaces `Namespace Access` page. From there, you can grant users access to the Namespace.

## 8. Add to your CI/CD Pipeline

Update your CI/CD pipelines to run the `gwa-cli` to keep your services updated on the gateway.

### 8.1. Github Actions Example

In the repository where you maintain your CI/CD Pipeline configuration, use the Service Account details from `Section 2` to set up two `Secrets`:

- GWA_ACCT_ID

- GWA_ACCT_SECRET

Add a `.gwa` folder (can be called anything) that will be used to hold your gateway configuration.

Github Workflow example:

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

### 8.2. Helm Chart

```
helm repo add bcgov https://bcgov.github.io/helm-charts
helm upgrade --install example -f config.yaml -f gwconfig.yaml bcgov/aps-gateway-ns
```

## 9. Share your API for Discovery

Package your APIs and make them available for discovery through the API Services Portal and BC Data Catalogue.

The `API Services Portal` Directory organizes your APIs by Datasets, Products and Environments. You can manage them via an API or through the UI.

To use the Directory API, the following scopes are required:

- For `contents` (documentation), the service account must have the `Content.Publish` scope
- For `datasets`, `products` and `environments`, the service account must have the `Namespace.Manage` scope
- For `credential issuers`, the service account must have the `CredentialIssuer.Admin` scope

How to update scopes:

1. Click `Namespaces` in the navigation bar
2. Click `Namespace Access`, and then `Service accounts with access`
3. Click the ellipses to the right of the appropriate service account and select `Edit Access`

View the Directory API:

- **V1:** [V1 Directory API Console](https://openapi-apps-gov-bc-ca.test.api.gov.bc.ca/?url=https://api-gov-bc-ca.test.api.gov.bc.ca/ds/api/openapi.yaml)
- **V2:** [V2 Directory API Console](https://openapi-apps-gov-bc-ca.test.api.gov.bc.ca/?url=https://api-gov-bc-ca.test.api.gov.bc.ca/ds/api/v2/openapi.yaml)

### 9.1 Setup your Draft Dataset

If you do not have a Dataset already defined in the BC Data Catalogue, you can create a draft in the API Services Portal.

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

### 9.2 Setup your Product

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

### 9.3 Update Gateway Configuration

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

Add the plugin configuration to the service `a-service-for-$NS` in the `sample.yaml` file you created in Section 3.

Re-run the publish command: `./gwa pg`. This will protect the upstream service with an API Key.

### 9.4 Check Access

```
curl https://${NAME}-api-gov-bc-ca.test.api.gov.bc.ca/headers
```

You will get an error: `No API key found in request`.

### 9.5 Get an API Key

Go to the `Namespaces` tab in the `API Services Portal`. Click the `Preview in Directory` link in the `Products` panel.

You will see a card with the title of the Dataset that you created in Section 9.1.

Click the title, then click `Request Access`.

Choose or create an `Application`, select the `Dev` environment, and click `Request Access & Continue`.

Clicking `Generate Secrets` will generate your API Key. Make a note of the Key.

> NOTE: An Environment can be configured for auto-approval. For the sample, `Dev` auto-approval is enabled so the Access Manager does not need to approve the request before getting access.

When you run the command:

```
curl https://${NAME}-api-gov-bc-ca.test.api.gov.bc.ca/headers -H "X-API-KEY: $KEY"
```

It should return header information similar to the following:

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

> NOTE: To manage access to your APIs, you must have the `Access.Manage` permission for the Namespace.

As an Access Manager, you can manage the new Consumer by going to the `Namespaces` tab, and selecting `Consumers`.

Here you should see the newly created Consumer. Click on the `name`.

You can administer Controls such as rate limiting and IP restrictions.

You can administer Authorization by toggling access to the particular Product and Environment.

### 9.7 Enabling for Discovery

Once the content is complete and you have applied the appropriate controls to your API, you are ready to make it available on the API Directory.

**Prerequisite:** Your namespace must be approved for use by a Ministry Organization Administrator. This is a one-time process to link the Ministry to the Namespace and can be requested here: https://dpdd.atlassian.net/servicedesk/customer/portal/1/group/2/create/118

Once approved, you must make an Environment `active` for the corresponding Product Environment to appear in the API Directory. You can do this by either updating the Product Environment configuration above to `active: true`, or going to the API Services Portal UI and editing the Environment details.

### 9.8 View Your Product in the API Directory

Find your API in the [API Services Portal Directory](https://api-gov-bc-ca.test.api.gov.bc.ca/devportal/api-directory).

It is now ready to receive access requests from the community!

## 10 What to try next?

### 10.1 Connect with the BC Government API Community

Post a message on [Rocket.Chat #aps-ops](https://chat.developer.gov.bc.ca/channel/aps-ops).

### 10.2 Read Our Other Guides

Find information about authentication and authorization patterns, reference implementations, plugin usage and much more.

### 10.3 Protect Your API using an External Identity Provider

Use the `client-credentials` flow to protect your API (see [Client Credential Protection](tutorial-idp-client-cred-flow/)).

### 10.4 Use the Access Approval Process

Enable `approval` for an Environment and go through the access request process by requesting access, and playing the role of Access Manager to review the request and approve access.

### 10.5 Publish Your Documentation on the Portal

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
- [gwa-api Swagger Console](https://openapi.apps.gov.bc.ca?url=https://gwa.api.gov.bc.ca/docs/v2/openapi.yaml)
- [gwa-api Postman Collection](https://openapi-to-postman.api.gov.bc.ca/?u=https://gwa.api.gov.bc.ca/docs/v2/openapi.yaml)
- [Gateway Metrics - Grafana](https://grafana.apps.gov.bc.ca)
