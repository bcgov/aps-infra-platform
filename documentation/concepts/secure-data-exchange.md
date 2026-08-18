---
title: Secure Data Exchange (SDX)
---

<!-- overview -->

Secure Data Exchange (SDX) is a service designed to facilitate secure, reliable transfer of data between government agencies and external partners. As data sharing becomes increasingly critical to service delivery, SDX provides a standardized, policy-compliant mechanism that reduces security risks while simplifying integration. This document covers the fundamental concepts of SDX, how it complements the API Gateway within the platform architecture, and the core mechanisms that enable safe data exchange.

![SDX Architecture](/artifacts/SDX.svg)

The Edge Server is a forward proxy for the service consumer (IS client) and a reverse proxy for the service provider (IS service). Each proxy interaction provides an opportunity to apply policies, such as:

- privacy zone identity token exchange
- timestamping
- legal entity signatures (electronic seals)
- logging
- access control policy enforcement

**Clients**: Clients invoke services and can be either an SDX member organization or a subsystem within that organization.

**Services**: Services are API implementations described using an OpenAPI specification. They belong to a subsystem and expose functionality to SDX clients.

Edge Servers sit in an organization's DMZ, where they are able to communicate with other Edge Servers in a secure and auditable way.

## Environments

> **Playground:** Playground environment is for service providers to verify the
> installation of SDX and test new functionality before moving it to production.
> There is NO data or service quality in this environment!
>
> **Production:** Production environment supports the Test data and Production
> data SDX instances. Data and service quality is the same for both SDX instances.

Links to the different services for each environment:

| Service               | Playground                                                                     | Production                                                  |
| --------------------- | ------------------------------------------------------------------------------ | ----------------------------------------------------------- |
| SDX UI                | [UI](https://sdx-api-gov-bc-ca.test.api.gov.bc.ca)                             | [UI](https://sdx.gov.bc.ca)                                 |
| SDX Member API        | [API](https://api-gov-bc-ca.test.api.gov.bc.ca/ds/api/sdx/v1/console)          | [API](https://api.gov.bc.ca/ds/api/sdx/v1/console)          |
| OpenAPI Specification | [OpenAPI](https://api-gov-bc-ca.test.api.gov.bc.ca/ds/api/sdx/v1/openapi.yaml) | [OpenAPI](https://api.gov.bc.ca/ds/api/sdx/v1/openapi.yaml) |
| API Services Portal   | [APS Portal](https://api-gov-bc-ca.test.api.gov.bc.ca/login?identity=provider) | [APS Portal](https://api.gov.bc.ca/login?identity=provider) |

## Roles

| Role               | Function                                                                       |
| ------------------ | ------------------------------------------------------------------------------ |
| SDX Operator       | Establish member organizations and assign legal representatives Org Admin role |
| Organization Admin | Manage System Admin role assignment for the organization                       |
| System Admin       | Manage subsystem onboarding for the particular organization                    |
| Subsystem Owner    | Manage service catalog entries and key sets for a particular subsystem         |
| Tech Lead          | Manage service catalog entries and key sets for a particular subsystem         |
| Access Manager     | Review/approve connection requests to services for a particular subsystem      |

## The public consumer host (PZGW)

`pzgw` is the shared, community-hosted runtime group that acts as the public
consumer entry point for member organizations that do not run their own
Internet-routable edge. It is not a general-purpose provider runtime: a
consumer application reaches SDX through PZGW's `consumerEndpoint`, PZGW then
forwards the request edge-to-edge to the **provider's own runtime group**
(over mTLS, using that runtime's `sdxEndpoint`), and the provider edge
forwards it to the private provider `upstreamUrl`.

Because PZGW is the only runtime with a widely recognizable public
(`*.api.gov.bc.ca`) hostname, it is easy to mistake it for the provider
runtime in a connection. It is not: the provider must still register and
host its own runtime group (`client-hosted` or another `community-hosted`
runtime group), and that runtime — not PZGW — must appear in the
provider's organization `hostedOrganizations`.

## Next steps

If you would like to dive deeper or start implementing services on SDX, check out the
following resources:

How-to guides

- [Onboarding an organization onto SDX](/how-to/sdx-org-onboarding.md)
- [Install an edge runtime group](/how-to/sdx-edge-runtime-groups.md)
- [Managing subsystems](/how-to/sdx-subsystems.md)
- [Managing services](/how-to/sdx-services.md)
- [Connecting a service](/how-to/sdx-connections.md)
- [Event Mgmt (preview)](/how-to/sdx-ape-event-mgmt.md)
- [Policy Mgmt (preview)](/how-to/sdx-ape-policy-mgmt.md)
