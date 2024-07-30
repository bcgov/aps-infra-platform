---
title: "Protect an API with Client Credential Flow"
---

<!-- overview -->

In this tutorial, you'll learn how to protect an API endpoint using the {{ glossary_tooltip term_id="api-services-portal" }}.
This tutorial is intended for {{ glossary_tooltip term_id="api-provider" text="API providers" }}.

By the end of this tutorial, you'll be able to:

- Create a new project, called a Gateway, in the API Services Portal
- Use templates to generate Gateway Service configuration
- Protect an API with an OAuth2 Client Credential Flow
- Publish an API to the {{ glossary_tooltip term_id="api-directory" }} for developers to discover

!!! note "Operating system"
    The commands provided in this tutorial are for a Unix shell (e.g. `bash`, `zsh`). If you are running Windows, it is recommended to use WSL2. 

    Alternatively, if you have access to a Platform Services OpenShift cluster, you can use the OpenShift commmand line [terminal](https://console.apps.silver.devops.gov.bc.ca/terminal) from any operating system.

<!-- background -->

<!-- Would like to include some background info on the Client Credential flow here.  -->

<!-- prerequisites -->

## Before you begin

There are no prerequisites for this tutorial. For a more basic introduction to the API Services Portal and setting up your first Gateway, complete:

- [Quick Start tutorial](/tutorials/quick-start.md)

<!-- steps -->

## Download the `gwa` CLI

1. Download the `gwa` cli and add to `PATH` for the session:

  ```sh
  curl -L https://github.com/bcgov/gwa-cli/releases/download/v3.0.0/gwa_Linux_x86_64.tgz | tar -zxf -
  export PATH=$PATH:$PWD
  ```

## Prepare and apply Gateway configuration

Gateway configuration is provided in a declarative configuration {{ glossary_tooltip term_id="yaml-file" text="YAML file" }} that defines the Gateway Services and additional resources for your API.

Templates are available for generating Gateway configuration for popular integration patterns. In this tutorial you will use a template to protect an API with an [Oauth 2.0 Client Credentials flow](/how-to/client-cred-flow.md) using a [Shared Identity Provider](/how-to/client-cred-flow.md#2-grant-access-to-the-identity-provider).

1. Log into the API Services Portal with your IDIR account. 
 
  !!! note "API Services Portal environment"
      For this tutorial, you will use the test/training environment (https://api-gov-bc-ca.test.api.gov.bc.ca), rather than the production environment (https://api.gov.bc.ca).

  ```
  gwa config set host api-gov-bc-ca.test.api.gov.bc.ca
  gwa login
  ```

1. Create a new {{ glossary_tooltip term_id="gateway"}}:

  ```sh linenums="0"
  gwa gateway create
  ```

  You'll be prompted to provide a display name to help you identify the Gateway.

  The output is similar to this:

  ```sh linenums="0"
  Gateway created. Gateway ID: gw-cf97b, display name: My New Gateway
  ```

1. Run `gwa generate-config` to generate configuration for your Gateway from a template.
  
  First, choose a unique name for your API service to be shown as part of your vanity URL: `<MYSERVICE>.api.gov.bc.ca`.

  Then run the following command, substituting your service name for `<MYSERVICE>`:

  ```
  gwa generate-config \
    --template client-credentials-shared-idp \
    --service <MYSERVICE> \
    --upstream https://httpbin.org \
    --out gw-config-client-cred.yaml
  ```

  !!! note "Upstream service"
      The "upstream service" refers to the backend service that the API Gateway forwards client requests to.

      You can specify an upstream service or leave the example provided (https://httpbin.org).

1. Review the configuration in the `gw-config-client-cred.yaml` file.

  You'll see the GatewayService configuration, including the upstream service (`host`), the route that exposes the GatewayService, and the plugins that add authentication and authorization. 

  Below the GatewayService, you'll find additional resources :

  - CredentialIssuer supports the Client Credentials flow
  - Product packages GatewayServices for managing consumer access
  - DraftDataset provides metadata about the service for the API Directory
   
  Don't worry if you don't understand all the details, you will learn more about Gateway configuration and other resources as you continue to work with the API Services Portal.

1. Apply the configuration file to send it to the API Services Portal:

  ```sh
  gwa apply -i gw-config-client-cred.yaml
  ```

  The output is similar to this:

  ```sh
  ↑ Publishing Gateway Services
  ✓ Gateway Services published
  creating service example-protected-service-dev
  creating route example-protected-service-dev
  creating plugin request-transformer for service e53a89db-03f4-430a-acae-5978ce9551aa
  creating plugin jwt-keycloak for service e53a89db-03f4-430a-acae-5978ce9551aa
  Summary:
    Created: 4
    Updated: 0
    Deleted: 0

  ✓ [CredentialIssuer] gw-de82c default: created
  ✓ [DraftDataset] example-protected-service-dataset: created
  ✓ [Product] example-protected-service API: created
  ```

## Access your API

At this point, you have successfully configured your Gateway. Before accessing your API, let's review what you have set up:

- Route to your service, via a vanity URL
- Protected by an SSL `*.api.gov.bc.ca` certificate
- Protected with the Client Credential flow using Pathfinder SSO
- Separation of concerns for authentication and authorization
- API Directory listing (in private preview mode)

1. Confirm the health of the connection between the API gateway and the upstream service by running:

  ```sh linenums="0"
  gwa status
  ```

  The output is similar to this:

  ```sh
  Status  Name                   Reason        Upstream
  UP      example-protected-service-dev  200 Response  https://httpbin.org:443/
  ```

1. Retrieve the URL of your Gateway Service by adding the `--hosts` flag to the `gwa status` command:
   
  ```sh linenums="0"
  gwa status --hosts
  ```

  The URL will be shown under the `Hosts` column and will be `https://<MYSERVICE>-dev-api-gov-bc-ca.test.api.gov.bc.ca/`.
  
  !!! note "Vanity URL"
      If this service were created on the production instance of the API Services Portal, the vanity URL would be `<MYSERVICE>-dev.api.gov.bc.ca`.

1. Try to access your Service without any authentication using this `curl` command:

  ```sh linenums="0"
  curl https://<MYSERVICE>-dev-api-gov-bc-ca.test.api.gov.bc.ca/uuid
  ```

  You will receive an `Unauthorized` 401 response, rather than the expected UUID4 from the upstream `https://httpbin.org/uuid`.

  Gaining access involves obtaining a client secret and ID (as a consumer of your API would), and requesting a JWT token.

1. Log into the [API Services Portal](https://api-gov-bc-ca.test.api.gov.bc.ca)
   (test instance), go to the **Gateways** tab, and select your newly created
   Gateway.
   
   In the **Products** panel, click the **Preview in Directory** link.

1. You will see a card with the service name you chose earlier (`<MYSERVICE>`). This card is a preview of how the service would look when shared to the API Directory.

  Click the title, then click **Request Access** to generate credentials.

  !!! note "Approval requirements"
      Though the menu is titled "Access Request", your service currently does not require approval to generate working credentials.

      This can be changed by setting `approval: true` in the Product configuration.

1. Click **Create Application** and provide a client application name.

1. Select the **Dev** API environment, and click **Request Access & Continue**.

1. Click **Generate Secrets** to generate a Client ID and Secret pair with a Token URL. Copy these values into the following command to set as environment variables, then run the command:

  ```sh
  export CID="<Client ID>"
  export CSC="<Client Secret>"
  export URL="<Token Endpoint>"
  ```

1. Run this command to request a JWT token and export it to an environment variable (`TOKEN`):

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

1. Finally, try the `curl` command again with the token in the header:

  ```sh
  curl https://<MYSERVICE>-dev-api-gov-bc-ca.test.api.gov.bc.ca/uuid \
  -H "Authorization: Bearer $TOKEN"
  ```

  It should return a random UUID4 similar to the following:

  `{  "uuid": "fb49e86c-7e91-45e7-aca1-d0bf1515252d" }`

  That's it! You have confirmed the successful configuration of your Gateway Service.

<!-- cleanup -->

## Clean up

To clean up the resources resulting from this tutorial, complete the following steps:

1. On the **Gateways** > **Consumers** page, delete the Consumer which was granted access to the service from the ellipsis (**...**) options.  

2. Delete the Gateway and associated services which were set up during the tutorial with this command:

  !!! danger
      The following action is irreversible. Ensure the correct Gateway is active first with:
      ``` linenums="0"
      gwa gateway current
      ```
      
  ```sh linenums="0"
  gwa gateway destroy --force
  ```

## Next steps

Learn more about Gateway Service configuration:

- [Create a Gateway Service](/how-to/create-gateway-service.md)
- [Client Credential Protection](/how-to/client-cred-flow.md)
- [Upstream Service Setup](/how-to/upstream-services.md)

Discover other API Services Portal features:

- [Manage Team Access](/how-to/gateway-admin.md)
- [Share an API](/how-to/api-discovery.md)
- [Manage Consumer Access](/how-to/api-access.md)
- [Monitor your Services](/how-to/monitoring.md)
- [CI/CD Integration](/how-to/cicd-integration.md)

## Get help

Create an account on
[Rocket.Chat](https://docs.developer.gov.bc.ca/join-bc-rocket-chat/) and join
the [#aps-ops](https://chat.developer.gov.bc.ca/channel/aps-ops) channel to
connect with the API Program Services team and user community. Alternatively, [open a support
ticket](https://dpdd.atlassian.net/servicedesk/customer/portal/1/group/2) and
we’ll get back to you via email in 3-5 business days.  

Either way, the API Program Services team is here to answer your questions.
