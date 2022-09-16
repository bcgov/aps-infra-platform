---
title: Glossary
order: 390
icon: book
---

# Glossary

| Term | Definition |
| --------------- | --------------- |
| Access Control | Access control is a set of security measures that regulate who can access a system, services, data, or resource. Access control policies use authentication and authorization to verify users and enable access. |
| Access Token | Access tokens enable clients to securely call protected APIs. The APIs use the access tokens to perform authentication and authorization. The information in the access token verifies that a user is entitled to access an API. |
| API          | An Application Programming Interface (API) is a software-to-software interface that provides a secure and standardized way for applications to communicate with each other to deliver requested data without user intervention. |
| API Consumer  | API Consumers (organizations providing services to end-users) use the APIs available through the APS Platform in the delivery of their services. API Consumers integrate the APIs into their applications. |
| API Directory | The API Directory is a centralized repository where API Providers can securely publish their APIs and API Consumers can find and request access to the published APIs. The APIs in the Directory are available to anyone with access to the APS Portal. |
| API Gateway   | The API Gateway is a service that facilitates the management and execution of APIs by routing requests. It extends the capabilities of APIs with the use of controls such as authentication, authorization, rate limiting, and IP limitations allowing systems to be safely and efficiently integrated. |
| API Key       | An API Key is a unique identifier (a random series of letters and numbers) used to authenticate an application accessing a specific API. The application includes the Key in each API request, and the API uses the Key to identify the application and authorize the request. The API Key is used in combination with an API Secret. |
| API Secret    | The API Secret is a software-level credential (password) used to securely authenticate an application or user. The Secret is included in all API requests to identify the Consumer. The API Secret is used in combination with an API Key. The Secret is known only to the Consumer and the API gateway. It is only displayed upon creation and must be recorded by the Consumer. |
| API Program Services (APS) | API Program Services (APS) is the team responsible for delivering services that enable ongoing access to public sector data by providing support for managing APIs. APS ensures the efficient development and operation of APIs through the APS Platform and API Services Portal. |
| API Provider               | An API Provider, usually a developer, creates, publishes, operates, and maintains APIs in the APS Management Platform. |
| APS Platform               | The APS Platform is the APS backend that enables data providers to manage their APIs and deliver services using the Kong API Gateway Community edition and a combination of tools to provide API security, authentication, routing, and publishing. |
| API Services Portal        | The API Services Portal is the access point for API Providers and API Consumers to publish, discover, and manage APIs. The APS Portal enables:<br />- API Providers to build, configure, and share their APIs publicly or privately<br />- API Consumers to setup applications, discover APIs available for integration, and send access requests |
| Authentication             | Authentication is a security process for verifying the identity of a user or device before allowing access to a system, resource, or function. Authentication validates that a user or system is who they claim to be. |
| Authorization              | Authorization is a security process for providing a user or device with access to a requested system, resource, or function based on permissions. Authorization is provided only after a user or device has been authenticated. |
| Environment                | An environment in software development is the collection of stages that an application moves through during development and include development, testing, staging and production.<br />- The development environment is the workspace for developers to design, program, debug, change, etc. an application or system.<br />- Test teams use the testing environment to conduct tests and ensure the quality and functionality of the application or system. Testers can identify bugs, errors, or defects and review fixes.<br />- A staging environment is a replica of a production environment with the purpose of testing code, builds, and updates to ensure quality in a production-like environment before deploying the application or system to the live (production) environment.<br />- Production is the environment where the application or system is in operation and available to end-users. |
| Kong Gateway               | The Kong Gateway Service is a data communication service that acts as middleware facilitating the transmission of requests between a client and an application using an API. |
| Namespace    | A namespace is a collection of Kong Gateway Services and Routes that are managed independently. |
| Organization | An organization is any ministry, crown corporation, or agency within the B.C. Government. |
| Publish      | Publishing APIs is the process by which an API Provider makes their API publicly available in the API Directory for discovery by API Consumers. |
| Role         | A role is a group of predefined access permissions assigned to a user. |
| Route        | A route is a means of exposing a service to users. It is the path used to send requests to its respective service after reaching the Gateway. A single service can have multiple routes. |
| Service      | A service represents an external upstream API or microservice consisting of a URL, which listens for incoming requests. |
| Scope        | Scope is a method used to specify authorization, or a set of permissions that grant access to specified systems and actions. Scopes can be applied to both users and service accounts. For example, the API Gateway *Namespace.View* scope allows read-only access to a namespace; therefore, a user with *Namespace.View* cannot approve API access requests. To approve an API access request, the user requires the *Access.Manage* scope, which gives permission to approve or reject access requests. |

If you have comments or feedback on any of these definitions, please submit a [Data Systems & Services ticket](https://dpdd.atlassian.net/servicedesk/customer/portal/1/group/1/create/18?summary=APS%20Glossary%20Feedback.&customfield_10402=10423).