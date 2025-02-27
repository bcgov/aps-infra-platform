---
title: "Quick Start"
---

<!-- overview -->

In this tutorial, you'll learn how to get started with the {{ glossary_tooltip term_id="api-services-portal" }}
and create a Gateway to route traffic to an API. This
tutorial is intended for {{ glossary_tooltip term_id="api-provider" text="API
providers" }}.

By the end of this tutorial, you'll be able to:

- Create a new project, called a Gateway, in the API Services Portal
- Use templates to generate Gateway Service configuration
- Publish an API to the {{ glossary_tooltip term_id="api-directory" }} for developers to discover

!!! note "Operating system compatibility"
    The commands provided in this tutorial are compatible with Linux, MacOS, and Windows.

    However, the commands provided in most of our documentation are for a Unix shell (e.g. `bash`, `zsh`).
    If you are running Windows, it is recommended to use [WSL](https://learn.microsoft.com/en-us/windows/wsl/install).

<!-- prerequisites -->
<!-- NONE - this is a beginner tutorial -->

<!-- steps -->

## Download the `gwa` CLI

1. Download the `gwa` cli and add to `PATH`:

  === "Linux / WSL"

      If you are on Linux or WSL, you can install by downloading a compressed archive:

      ```shell
      curl -sL https://github.com/bcgov/gwa-cli/releases/latest/download/gwa_Linux_x86_64.tgz -o gwa.tar.gz
      tar -xf gwa.tar.gz -C /tmp
      sudo cp /tmp/gwa /usr/local/bin/
      ```

  === "Windows"

      If you are on Windows, you can install using Command Prompt (CMD) by 
      navigating to the target installation folder and downloading a compressed archive:

      ```shell
      mkdir gwa
      cd gwa
      curl -sL https://github.com/bcgov/gwa-cli/releases/latest/download/gwa_Windows_x86_64.zip -o gwa.zip
      tar -xf gwa.zip
      powershell -command "[Environment]::SetEnvironmentVariable('Path', [Environment]::GetEnvironmentVariable('Path', 'User') + [IO.Path]::PathSeparator + [System.IO.Directory]::GetCurrentDirectory(), 'User')"
      ```

  === "macOS"

      If you are on macOS, you can install by downloading a compressed archive:

      ```shell
      curl -sL https://github.com/bcgov/gwa-cli/releases/latest/download/gwa_Darwin_x86_64.zip -o gwa.zip
      tar -xf gwa.zip -C /tmp
      sudo cp /tmp/gwa /usr/local/bin/
      ```

## Prepare and apply Gateway configuration

Gateway configuration is provided in a declarative configuration {{ glossary_tooltip term_id="yaml-file" text="YAML file" }} that defines the Gateway Services and additional resources for your API.

Templates are available for generating Gateway configuration for popular integration patterns. In this tutorial you will use a basic template to route traffic to a custom endpoint URL.

1. Log in with your IDIR via the CLI. Follow the prompts provided in the terminal to complete the login process.

  ```sh linenums="0"
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
  
  First, choose a unique name for your API service to be shown as part of your vanity URL: `<MYSERVICE>.dev.api.gov.bc.ca`.

  Then run the following command, substituting your service name for `<MYSERVICE>`:

  ```sh linenums="0"
  gwa generate-config --template quick-start --service <MYSERVICE> --upstream https://httpbin.org
  ```

  !!! note "Upstream service"
      The "upstream service" refers to the backend service that the API Gateway forwards client requests to.

      You can specify an upstream service or leave the example provided (https://httpbin.org).

1. Review the configuration in the `gw-config.yaml` file.

  You'll see the *GatewayService* configuration, including: 
  
  -  the upstream service (`url`)
  -  the route that exposes the GatewayService at the new endpoint (`routes.hosts`)
  -  tags on each object with the format `tags: [ ns.<GatewayId> ]`
  
  Below the GatewayService, you'll find additional resources:

  - *Product* packages GatewayServices for managing consumer access
  - *DraftDataset* provides metadata about the service for the API Directory 
   
  Don't worry if you don't understand all the details, you will learn more about Gateway configuration as you continue to work with the API Services Portal.

1. Apply the configuration file to send it to the API Services Portal:

  ```sh
  gwa apply -i gw-config.yaml
  ```

  The output is similar to this:

  ```sh
  ↑ Publishing Gateway Services
  ✓ Gateway Services published
  creating service basic-example-dev
  creating route basic-example-dev
  Summary:
    Created: 2
    Updated: 0
    Deleted: 0

  ✓ [DraftDataset] basic-example-dataset: created
  ✓ [Product] Basic-Example API: created
  ```

## Access your API

1. Confirm the health of the connection between the API gateway and the upstream service by running:

  ```sh linenums="0"
  gwa status
  ```

  The output is similar to this:

  ```sh
  Status  Name           Reason        Upstream
  UP      basic-example  200 Response  https://httpbin.org:443/
  ```

1. Retrieve the URL of your Gateway Service by adding the `--hosts` flag to the `gwa status` command:
   
  ```sh linenums="0"
  gwa status --hosts
  ```

  The URL will be shown under the `Hosts` column and will be `https://<MYSERVICE>.dev.api.gov.bc.ca/`.

1. Visit the URL in a browser to see your API gateway in action.
   
  You will see the contents of the httpbin.org homepage, but routed through your URL.

1. To see a more typical API response, visit `https://<MYSERVICE>.dev.api.gov.bc.ca/uuid`.
   
   You will see a random UUID4 from the upstream `https://httpbin.org/uuid` in JSON format, similar to:

  ```
  {
      "uuid": "16498622-b62b-4070-9467-785107380a47"
  }
  ```

  That's it! You have confirmed the successful configuration of your Gateway Service.

## View your API in the API Directory

1. Log into the [API Services Portal](https://api.gov.bc.ca).
1. Go to the **Gateways** tab and select your newly created Gateway.
1. In the **Products** panel, click the **Preview in Directory** link.
1. You will see a card with the service name you chose earlier (`<MYSERVICE>`). 
  This card is a preview of how the service would look when shared to the API Directory.
   
  The contents of the card can be customzied by editing the DraftDataset
  resource in the Gateway configuration (`gw-config.yaml`).

  For more information on making your API visible to the public, see
  [Share an API - Enabling for Discovery](/how-to/api-discovery.md#enabling-for-discovery).

<!-- summary -->

## Summary

In this tutorial, you learned how to:
  
- Create a route to your service, using a vanity URL
- List your API in the API Directory (in private preview mode)

<!-- cleanup -->

## Clean up

To clean up the resources resulting from this tutorial, complete the following steps:

1. Delete the Gateway and associated services which were set up during the tutorial with this command:

  !!! danger
      The following action is irreversible. Ensure the correct Gateway is active first with:
      ``` linenums="0"
      gwa gateway current
      ```
      
  ```sh linenums="0"
  gwa gateway destroy --force
  ```

## Next steps

Continue to the next tutorial to set up a protected API:
- [Protect an API with Client Credential Flow](/tutorials/protect-client-cred.md)

Learn more about Gateway Service configuration:

- [Create a Gateway Service](/how-to/create-gateway-service.md)
- [Set Up an Upstream Service](/how-to/upstream-services.md)

Discover other API Services Portal features:

- [Manage Team Access](/how-to/gateway-admin.md)
- [Share an API](/how-to/api-discovery.md)
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
