---
title: Protect an API
---

This article explains the basics of adding protection to your Gateway Service,
and how it works in conjunction with supported plugins.

Protecting your API is crucial for several reasons:

1. Security: Unprotected APIs are vulnerable to various security threats such as
   unauthorized access, data breaches, injection attacks, and more. By
   implementing security measures, you can safeguard your API and the data it
   handles.

2. Data Integrity: APIs often deal with sensitive data. Protecting your API
   ensures the integrity of this data, preventing unauthorized modification or
   access.

3. Authentication and Authorization: Protecting your API allows you to enforce
   authentication and authorization mechanisms. This ensures that only
   authorized users or systems can access the API and perform specific actions,
   maintaining control over who can interact with your services.

4. Preventing Abuse: Without protection, your API may be susceptible to abuse,
   such as excessive requests, denial of service attacks, or misuse of
   resources. Implementing security measures can help mitigate these risks.

5. Compliance: Depending on your industry and the type of data your API handles,
   there may be legal or regulatory requirements regarding data protection and
   privacy. Protecting your API helps ensure compliance with these regulations.

6. Maintaining Reputation: Security breaches or misuse of your API can damage
   your organization's reputation and erode trust with your users or clients.
   Protecting your API helps maintain your reputation as a trustworthy and
   reliable provider.

Overall, protecting your API is essential for ensuring the security, integrity,
and proper functioning of your systems and services.

## Kong API key

Key-based authentication, often referred to as key-auth, is a method of
authentication where a unique key or token is required to access an API or
service. Here's how it typically works:

1. API Key Generation: The API Gateway issues a unique API key to each client or
   application that wants to access your API. This key is a long alphanumeric
   string that serves as a credential for authentication.

2. Include Key in Requests: Clients or applications that want to access your API
   include their API key in the request they send to the API Gateway. This key
   is usually included in the request headers.

3. Authentication: When the API Gateway receives a request, it checks the
   included API key to verify the identity of the client or application. If the
   key is valid and authorized to access the your API, the API Gateway processes
   the request; otherwise, it denies access.

4. Key Management: API keys can be managed by you, the provider, allowing you to
   revoke or regenerate keys as needed. This provides a level of control over
   access to your API and enables you to respond to security threats or
   unauthorized access attempts.

Key-based authentication is simple to implement and widely used across various
APIs and services. However, it's important to handle API keys securely to
prevent unauthorized access or misuse.

See the how-to on [Kong API Key](/how-to/kong-api-key.md) to protect your API
with key-based authentication.

## OAuth 2.0 Client Credential Flow

With Oauth 2.0 client credential flow, the client application authenticates
itself with the API Gateway using its client ID and client secret. The API
gateway then forwards this authentication to the authorization server, which
issues an access token. With this token, the client can access protected
resources through the API gateway.

See the how-to on [Client Credential Protection](/how-to/client-cred-flow.md) to
protect your API with OAuth 2.0 Client Credentials Flow.

## Next steps

- [Kong API Key](/how-to/kong-api-key.md)
- [Client Credential Protection](/how-to/client-cred-flow.md)
