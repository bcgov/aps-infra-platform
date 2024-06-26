---
title: "API Provider Quick Start"
---

The following steps guide an {{ glossary_tooltip term_id="api-provider" }} through setting up an API on the {{ glossary_tooltip term_id="api-services-portal" text="API Services Portal" }} in a Test/Training instance. 
At the end of the guide, you will have a public API endpoint that is protected using the OAuth2 Client Credential Grant.

## 1. Download the `gwa` CLI

The `gwa` command line interface (CLI) is available for Linux, MacOS, and Windows at https://github.com/bcgov/gwa-cli/releases. 

The commands provided in this tutorial are for a Unix shell (e.g. `bash`, `zsh`). If you are running Windows, it is recommended to use WSL2. 

Alternatively, if you have access to a Platform Services OpenShift cluster, you can use the OpenShift commmand line [terminal](https://console.apps.silver.devops.gov.bc.ca/terminal) from any operating system.

Start by downloading the `gwa` cli and adding to `PATH` for the session:

```sh
curl -L https://github.com/bcgov/gwa-cli/releases/download/v2.0.15/gwa_Linux_x86_64.tgz | tar -zxf -
export PATH=$PATH:$PWD
```

## 2. Login

Log into the API Services Portal with your IDIR account.

```
gwa config set host api-gov-bc-ca.test.api.gov.bc.ca
gwa login
```

## 3. Apply Configuration

Templates are available for generating gateway configuration for popular integration patterns. In this tutorial you will use a template to protect an API with an [Oauth 2.0 Client Credentials flow](/how-to/client-cred-flow.md) using a [Shared Identity Provider](/how-to/client-cred-flow.md#2-grant-access-to-the-identity-provider).

First, create a new Namespace. 

```
gwa namespace create -g
```

`-g` generates a random, unique Namespace name which is displayed in response and set as the current Namespace.

Second, choose a unique name for your API to be shown as part of your vanity URL: `<MYSERVICE>.api.gov.bc.ca`.

You can also specify an upstream service or leave the example provided (`https://httpbin.org`).

Then run the following command, substituting your service name for `<MYSERVICE>`:

```
gwa generate-config \
  --template client-credentials-shared-idp \
  --service <MYSERVICE> \
  --upstream https://httpbin.org
```

Apply the configuration file:

```
gwa apply -i gw-config.yml
```

You can confirm the health of the connection between the API Gateway and the upstream service by running:

```
gwa status
```

## 4. Review Setup

To review what configuration has been setup, log into the [API Services Portal](https://api-gov-bc-ca.test.api.gov.bc.ca), go to the **Namespaces** tab, and select the newly created Namespace.

From here, go to **Activity** and select **More details** next to "published gateway configuration" to review what the configuration.

What you have setup:

- Route to your service, via the vanity URL: `<MYSERVICE>-dev-api-gov-bc-ca.test.api.gov.bc.ca/`
  - Retrieve the URL directly with this command: `gwa status --json | jq -r '.[].env_host'`
  - If this service were created on the production instance of the API Services Portal, the vanity URL would be `<MYSERVICE>.dev.api.gov.bc.ca`
- Protected by an SSL `*.api.gov.bc.ca` certificate
- Protected with the Client Credential grant using Pathfinder SSO
- Separation of concerns for authentication and authorization

## 5. Access your API

If you try to access your service now without any authentication, you will receive an `Unauthorized` 401 response. Try:

```sh
curl https://<MYSERVICE>-dev-api-gov-bc-ca.test.api.gov.bc.ca/uuid
```

This command returns an error `{  "message": "Unauthorized" }`, rather than a UUID4 from the upstream `https://httpbin.org/uuid`.

Gaining access involves requesting access (as a consumer of your API would), obtaining a client secret and ID, and requesting a JWT token.

Start by going to the **Namespaces** tab in the API Services Portal and click the **Preview in Directory** link in the **Products** panel.

You will see a card with the service name you chose earlier (`<MYSERVICE>`). This card is a preview of how the service would look when shared to the {{ glossary_tooltip term_id="api-directory" }}.

Click the title, then click **Request Access**.

Choose or create an **Application**, select the **Dev** environment, and click **Request Access & Continue**.

Click **Generate Secrets** to generate a Client ID and Secret pair with a Token URL. Copy these values into the following command to set as environment variables.

```sh
export CID="<Client ID>"
export CSC="<Client Secret>"
export URL="<Token Endpoint>"
```

Then run the following command to request a JWT token and export it to an environment variable (`TOKEN`):

```sh
RESPONSE=$(curl -X POST "$URL" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=$CID" \
  -d "client_secret=$CSC" \
  -d "grant_type=client_credentials" \
  -d "scopes=openid")

echo "$RESPONSE" | jq
export TOKEN=$(echo "$RESPONSE" | jq -r '.access_token')
```

Finally, try the `curl` command again with the token in the header:

```sh
curl https://<MYSERVICE>-dev-api-gov-bc-ca.test.api.gov.bc.ca/uuid -H "Authorization: Bearer $TOKEN"
```

It should return a random UUID4 similar to the following:

`{  "uuid": "fb49e86c-7e91-45e7-aca1-d0bf1515252d" }`


## 6. What to try next?

### Connect with the BC Government API Community

Post a message on [Rocket.Chat #aps-ops](https://chat.developer.gov.bc.ca/channel/aps-ops).

### Read Our Other Guides and Resources

Find information about authentication and authorization patterns, reference implementations, plugin usage and much more.

- [Monitor your Services](/how-to/monitoring.md) : View metrics for performance, traffic and trends.
- [Gateway Administration](/how-to/gateway-admin.md) : Add team members and create service accounts.
- [Customize Gateway Controls](/how-to/create-gateway-service.md)
- [Upstream Service Setup](/how-to/upstream-services.md)
- [Share your API](/how-to/api-discovery.md) : Setup metadata about your APIs for discovery.
- [API Access](/how-to/api-access.md) : Approve and administer controls for consumer access to your APIs.
- [CI/CD Integration](/how-to/cicd-integration.md)
- [Add Client Credential Protection](/how-to/client-cred-flow.md)

### Ready for Production?

Our production instance supports all your environments, so once you know what
you are building and are ready to deploy your "dev" environment, you can setup
the API gateway in our production instance.

To get started, go to the API Services Portal at https://api.gov.bc.ca.
