---
title: "API Provider Quick Start"
---

<!-- overview -->

In this tutorial, you'll learn how to get started with the {{ glossary_tooltip term_id="api-services-portal" }}
and create a Gateway to route traffic to an API. This
tutorial is intended for {{ glossary_tooltip term_id="api-provider" text="API
providers" }}.

By the end of this tutorial, you'll be able to:

- Create a new project, called a Gateway, in the API Services Portal
- Use templates to generate Gateway Service configuration

!!! note "Operating system"
    The commands provided in this tutorial are for a Unix shell (e.g. `bash`, `zsh`). If you are running Windows, it is recommended to use WSL2. 

    Alternatively, if you have access to a Platform Services OpenShift cluster, you can use the OpenShift commmand line [terminal](https://console.apps.silver.devops.gov.bc.ca/terminal) from any operating system.

<!-- prerequisites -->
<!-- NONE - this is a beginner tutorial -->

<!-- steps -->

## Download the `gwa` CLI

1. Download the `gwa` cli and add to `PATH` for the session:

  ```sh
  curl -L https://github.com/bcgov/gwa-cli/releases/download/v3.0.0/gwa_Linux_x86_64.tgz | tar -zxf -
  export PATH=$PATH:$PWD
  ```

## Prepare and apply Gateway configuration

Gateway configuration is provided in a declarative configuration {{ glossary_tooltip term_id="yaml-file" text="YAML file" }} that defines the Gateway Services and additional resources for your API.

Templates are available for generating Gateway configuration for popular integration patterns. In this tutorial you will use a basic template to route traffic to a custom endpoint URL.

1. Log into the API Services Portal with your IDIR account. 

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
  
  First, choose a unique name for your API service to be shown as part of your vanity URL: `<MYSERVICE>.api.gov.bc.ca`.

  Then run the following command, substituting your service name for `<MYSERVICE>`:

  ```
  gwa generate-config \
    --template basic-service \
    --service <MYSERVICE> \
    --upstream https://httpbin.org
  ```

  !!! note "Upstream service"
      The "upstream service" refers to the backend service that the API Gateway forwards client requests to.

      You can specify an upstream service or leave the example provided (https://httpbin.org).

1. Review the configuration in the `gw-config.yml` file.

  You'll see the `GatewayService` configuration, including:
  
  -  the upstream service (`url`)
  -  the route that exposes the GatewayService at the new endpoint (`routes.hosts`)
  -  tags on each object with the format `tags: [ ns.<GatewayId> ]`
   
  Don't worry if you don't understand all the details, you will learn more about Gateway configuration as you continue to work with the API Services Portal.

1. Apply the configuration file to send it to the API Services Portal:

  ```sh
  gwa apply -i gw-config.yml
  ```

  The output is similar to this:

  ```sh
  ↑ Publishing Gateway Services
  ✓ Gateway Services published
  creating service one-great-service
  creating route one-great-service
  Summary:
    Created: 2
    Updated: 0
    Deleted: 0

  1/1 Published, 0 Skipped
  ```

## Access your API

1. Confirm the health of the connection between the API gateway and the upstream service by running:

  ```sh linenums="0"
  gwa status
  ```

  The output is similar to this:

  ```sh
  Status  Name               Reason        Upstream
  UP      one-great-service  200 Response  https://httpbin.org:443/
  ```

1. Retrieve the URL of your Gateway Service by adding the `--hosts` flag to the `gwa status` command:
   
  ```sh linenums="0"
  gwa status --hosts
  ```

  The URL will be shown under the `Hosts` column and will be `https://<MYSERVICE>.api.gov.bc.ca/`.

1. Visit the URL in a browser to see your API gateway in action.
   
  You will see the contents of the httpbin.org homepage, but routed through your URL.

1. To see a more typical API response, visit `https://<MYSERVICE>.api.gov.bc.ca/uuid`.
   
   You will see a random UUID4 from the upstream `https://httpbin.org/uuid` in JSON format, similar to:

  ```
  {
      "uuid": "16498622-b62b-4070-9467-785107380a47"
  }
  ```

  That's it! You have confirmed the successful configuration of your Gateway Service. 
  
  You have set up:

   - Route to your service, via a vanity URL
   - Protected by an SSL `*.api.gov.bc.ca` certificate

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
- [Upstream Service Setup](/how-to/upstream-services.md)

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
