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

## Next steps

If you would like to dive deeper or start implementing services on SDX, check out the
following resources:

How-to guides

- [Onboarding an organization onto SDX](/how-to/sdx-org-onboarding.md)
- [Provision a new Runtime Group (Edge Server)](/how-to/sdx-edge-servers.md)
- [Managing systems and services](/how-to/sdx-subsystems.md)
- [Connecting a Service](/how-to/sdx-connections.md)
