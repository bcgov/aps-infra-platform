---
title: Production Readiness Checklist
---

This guide gives
{{ glossary_tooltip term_id="api-provider" text="API Providers" }} a quick
reference of actions they need to complete before publishing their Gateway
Services to the {{ glossary_tooltip term_id="api-directory" }} for discovery by
consumers.

## First time activities

- [ ] Learn about and understand the benefits of the
{{ glossary_tooltip term_id="api-services-portal" }}:

  - Review our [plain language](https://www2.gov.bc.ca/gov/content/data/finding-and-sharing/api-management)
    and [technical documentation](https://developer.gov.bc.ca/docs/default/component/aps-infra-platform-docs/).
  
  - Reach out to the APS team by opening a [support ticket](https://dpdd.atlassian.net/servicedesk/customer/portal/1/group/2)
    or in the [API-ProgramServices-operations](https://teams.microsoft.com/l/channel/19%3Ac81bf553c07647cebeb2aeb034ec0d25%40thread.tacv2/API-ProgramServices-operations?groupId=a80418da-c27b-406e-89ab-7695b61924d8&tenantId=6fdb5200-3d0d-4a8a-b036-d3685e359adc)
    Microsoft Teams channel if you can’t find the information you’re looking for.

- [ ] Have access to a production-ready API:

  - This could be a public or private service. If your API service runs the BC
    Government [Private Cloud OpenShift platform](https://digital.gov.bc.ca/technology/cloud/private/),
    you will need to configure the
    network policies to allow access from your API gateway. View our
    [Set Up an Upstream Service](/how-to/upstream-services.md) guide for more
    information.

- [ ] Get Organizational approval to share your API service:

  - Comply with your Organization’s information management and security
    guidelines. For BC Government, this includes but is not limited to
    [Privacy Impact Assessments](https://www2.gov.bc.ca/gov/content/governments/services-for-government/information-management-technology/privacy/privacy-impact-assessments)
    (PIA) and [Security Threat and Risk Assessments](https://www2.gov.bc.ca/gov/content/governments/services-for-government/information-management-technology/information-security/security-threat-and-risk-assessment)
    (STRA).

- [ ] **Recommended**: Document your API in an [OpenAPI specification](https://swagger.io/docs/specification/about/)
(OAS, formerly Swagger).

## Configure a Gateway Service

- [ ] Create a [Gateway Service](/how-to/create-gateway-service.md).

## Protect your API

- [ ] Ensure that your Gateway Services are protected to safeguard your APIs and
the data they handle:

  - Implement [authentication](/how-to/client-cred-flow.md) to control who can
    interact with your services.

  - Manage [consumer access](/how-to/api-access.md) and configure [rate limiting](/how-to/COMMON-CONFIG.md#rate-limiting)
    to prevent abuse of your resources.

## Share your API

- [ ] Package your Gateway Services and make them available for discovery by
developers and consumers in BC Government and beyond:

  - Author a [Dataset](/how-to/api-discovery.md/#create-a-dataset) with metadata
    about your API. If your API is already listed in the BC Data Catalogue, you
    can skip this step.

  - Bundle your Gateway Services into a [Product](/how-to/api-discovery.md/#link-your-dataset-to-a-product).

  - Associate your Gateway with an Organization and Business Unit.

  - Preview your Product on the API Directory and enable it for discovery in the
    API Services Portal.

## Additional steps

These steps are not required to enable your Gateway Services for discovery but
may be useful for Gateway administrators.

- [ ] Integrate DevOps

  - Learn how to keep your Gateway Services updated by
  [adding the `gwa` CLI  to existing CI/CD pipelines](/how-to/cicd-integration.md).

- [ ] Monitor your Gateway Services

  - Understand how to [view request metrics](/how-to/monitoring.md) in
  real-time for your Gateway Services.
