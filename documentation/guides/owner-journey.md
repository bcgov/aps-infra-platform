<<<<<<< HEAD
=======
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

> To view common plugin configuration go to [Common Controls](../gateway/COMMON-CONFIG.md)

> To learn about other available plugins, navigate to `Gateway > Plugins` on the sidebar of this page.

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
>>>>>>> f52b256db0e7414d8e33ef1404adb31f455779d4
---
externalLink: https://github.com/bcgov/gwa-api/blob/dev/USER-JOURNEY.md
title: "API Provider Quick Start"
description: "Setup a new namespace for onboarding services on the BC Gov API Gateway."
order: 3
tags: ["ns.platform"]
isComplete: true
isPublic: true
publishDate: "2021-06-10T20:00:00.000-08:00"
---

# API Provider Quick Start

> NOTE: As of Sep 19, 2023, we have upgraded our command line interface to version 2. This user journey goes through the steps with the new CLI. If you are looking for Version 1 of the user journey, please go [here](owner-journey-v1.md).

The following steps guide an API Provider through setting up an API on the BC Government API Gateway in a Test/Training instance. At the end of the guide, you will have a public API endpoint that is protected using the OAuth2 Client Credential Grant.

## 1. Download the `gwa` CLI

The `gwa` CLI is available for Linux, MacOS, and Windows at https://github.com/bcgov/gwa-cli/releases/tag/v2.0.11. For this tutorial, if you have access to a Platform Services Openshift cluster, you can use the Openshift Terminal and run:

```sh
curl -L https://github.com/bcgov/gwa-cli/releases/download/v2.0.11/gwa_Linux_x86_64.tgz | tar -zxf -
export PATH=$PATH:$PWD

```

## 2. Login

Log into the API Services Portal with your IDIR account.

```
gwa config set host api-gov-bc-ca.test.api.gov.bc.ca
gwa login
```

## 3. Apply Configuration

Templates are available for generating gateway configuration for popular integration patterns. Below has one that uses the [Client Credentials Oauth2 Grant](./tutorial-idp-client-cred-flow.md) and uses a [Shared Identity Provider](./tutorial-idp-client-cred-flow.md#shared-idp).

First, create a new namespace.

```
gwa namespace create
```

Second, choose a vanity url: `<MYSERVICE>.api.gov.bc.ca`.

Then run the following command, substituting `<MYSERVICE>` with your unique name for your API.

If you know your upstream service, you can specify that as well, or you can use the example one `https://httpbin.org` provided.

```
gwa generate-config \
  --template client-credentials-shared-idp \
  --service <MYSERVICE> \
  --upstream https://httpbin.org
```

Apply changes:

```
gwa apply -i gw-config.yml
```

You can confirm the health of the connection between the API Gateway and the upstream service by running:

```
gwa status
```

## 4. Review Setup

To review what configuration has been setup, log into the [API Services Portal](https://api-gov-bc-ca.test.api.gov.bc.ca), go to the `Namespaces` tab, and select the newly created namespace.

From here, you can go to `Activity` to review what configuration has been setup.

What you have setup:

- Vanity url: `<MYSERVICE>.dev.api.gov.bc.ca`
- Protected by an SSL `*.api.gov.bc.ca` certificate
- Protected with the Client Credential grant using OCIO SSO Gold cluster
- Separation of concerns for authentication and authorization

## 5. Access your API

Go to the `Namespaces` tab in the `API Services Portal` and click the `Preview in Directory` link in the `Products` panel.

You will see a card with the title of the Dataset that you created earlier.

Click the title, then click `Request Access`.

Choose or create an `Application`, select the `Dev` environment, and click `Request Access & Continue`.

Clicking `Generate Secrets` will generate a Client ID and Secret pair with a Token URL. Make a note of this information as it will be used to request a JWT Token.

To get a JWT Token, run the following command:

```
export CID="<Client ID>"
export CSC="<Client Secret>"
export URL="<Token Endpoint>"
```

```
curl -s $URL \
  -X POST -H "Content-Type: application/x-www-form-urlencoded" \
  -d client_id=$CID -d client_secret=$CSC \
  -d grant_type=client_credentials \
  -d scopes=openid
```

Extract the `access_token` and put it into an environment variables `TOK`.

```
curl https://<MYSERVICE>-api-gov-bc-ca.test.api.gov.bc.ca/headers -H "Authorization: Bearer $TOK"
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

## 6. What to try next?

### Connect with the BC Government API Community

Post a message on [Rocket.Chat #aps-ops](https://chat.developer.gov.bc.ca/channel/aps-ops).

### Read Our Other Guides and Resources

Find information about authentication and authorization patterns, reference implementations, plugin usage and much more.

- [Monitor your Services](../resources/monitoring.md) : View metrics for performance, traffic and trends.
- [Gateway Administration](../resources/gateway-admin.md) : Add team members and create service accounts.
- [Explore Different Plugins](../resources/gateway-configuration.md)
- [Upstream Service Setup](../resources/upstream-services.md)
- [API Discovery](../resources/api-discovery.md) : Setup metadata about your APIs for discovery.
- [API Access](../resources/api-access.md) : Approve and administer controls for consumer access to your APIs.
- [CI/CD Integration](../resources/cicd-integration.md)

<<<<<<< HEAD
<<<<<<< HEAD
=======
Use the `client-credentials` flow to protect your API (see [Client Credential Protection](../guides/tutorial-idp-client-cred-flow.md)).
>>>>>>> f52b256db0e7414d8e33ef1404adb31f455779d4

### Ready for Production?

=======
Use the `client-credentials` flow to protect your API (see [Client Credential Protection](../guides/tutorial-idp-client-cred-flow.md)).

> > > > > > > f52b256db0e7414d8e33ef1404adb31f455779d4

Our production instance supports all your environments, so once you know what you are building and are ready to deploy your "dev" environment, you can setup the API gateway in our production instance.

To get started, go to the API Services Portal at https://api.gov.bc.ca.
