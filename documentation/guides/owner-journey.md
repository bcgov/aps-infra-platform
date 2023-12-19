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

Use the `client-credentials` flow to protect your API (see [Client Credential Protection](tutorial-idp-client-cred-flow.md)).

### Ready for Production?

Our production instance supports all your environments, so once you know what you are building and are ready to deploy your "dev" environment, you can setup the API gateway in our production instance.

To get started, go to the API Services Portal at https://api.gov.bc.ca.
