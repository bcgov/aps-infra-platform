---
title: Secure Data Exchange (SDX)
---


<!-- overview -->
Secure Data Exchange (SDX) is a service designed to facilitate secure, reliable transfer of data between government agencies and external partners. As data sharing becomes increasingly critical to service delivery, SDX provides a standardized, policy-compliant mechanism that reduces security risks while simplifying integration. This document covers the fundamental concepts of SDX, how it complements the API Gateway within the platform architecture, and the core mechanisms that enable safe data exchange.

**Clients**: Clients invoke services and can be either an SDX member organization or a subsystem within that organization.

**Services**: Services are API implementations described using an OpenAPI specification. They belong to a subsystem and expose functionality to SDX clients.

The SDX is a forward proxy for the clients and a reverse proxy for the services.  Each proxy interaction provides an opportunity to apply policies, such as:

- privacy zone token exchange
- timestamping
- legal entity signatures (electronic seals)

{A summary paragraph introducing a concept, explaining its importance or
relevance, and providing an overview of the content that will be covered
in the document (scope).}

This article explains what the Secure Data Exchange is, how it is different from the API Gateway, and how it works.


{Then include a paragraph with a definition of the concept you are explaining.
If more definitions are needed, include those definitions here as a bulleted list.}

{Optional: Add visual aids to complement explanations (system diagram,
flowchart, decision tree) - see the
[Style Guide - Diagrams](/contribute/style-guide.md#diagrams)
and [Good Docs](https://gitlab.com/tgdp/templates/-/blob/main/concept/process-concept.md#create-visual-aids-for-a-concept-document).}

(Optional) Image/Figure: {Image title, which concisely explains the image or
figure.}

<!-- body -->

## Background (optional)

{Use this section to provide a reader with a context, prehistory, or background information.}

Typical wordings to use are:

- The reason {X} is designed that way is because historically, ...
- The idea of {X} originated from the growing demand for ...

## Use cases OR Purpose

{Answer "How can I use it?" or "How does it help me?" from the reader's perspective.
Use this section to explain the overall purpose and provide use
cases to show how a reader can benefit from a concept.}

## Comparison of {thing being compared} (optional)

{Use this section to compare options or alternatives within a concept.}

Table: {Table title which concisely explains the comparison.}

| Option   | Pros                                  | Cons                                  |
|----------|---------------------------------------|---------------------------------------|
| {Concept} option 1 | <ul><li>Pro 1 for Option 1</li><li>Pro 2 for Option 1</li></ul> | <ul><li>Con 1 for Option 1</li><li>Con 2 for Option 1</li></ul> |
| {Concept} option 2 | <ul><li>Pro 1 for Option 2</li><li>Pro 2 for Option 2</li></ul> | <ul><li>Con 1 for Option 2</li><li>Con 2 for Option 2</li></ul> |

OR

| Use case   | Recommendation     | Why                       |
|------------|--------------------|---------------------------|
| Use case 1 | {Concept} option 1 | Reason for using option 1 |
| Use case 2 | {Concept} option 2 | Reason for using option 2 |

<!-- whatsnext -->

## Next steps (optional)

If you would like to dive deeper or start implementing {concept}, check out the
following resources:

How-to guides

- [Natural next thing to do](/how-to/gwa-install.md)
- [Something else to consider or explore](/how-to/private-route.md)

Linked concepts

- [Concept 1](/concepts/api-directory.md)

External resources

- [Kong](https://docs.konghq.com/gateway/latest/key-concepts/services/)
