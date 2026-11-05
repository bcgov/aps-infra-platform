---
title: Protect an API
---

This article explains the basics of adding protection to your Gateway Service,
and how it works in conjunction with supported plugins.

## Compare protection methods

The API Services Portal supports these ways to protect a Gateway Service. Each
Product Environment uses one of them, set as the Environment's flow.

| Method | What the Gateway confirms | What you set up | Choose it when |
| ------ | ------------------------- | --------------- | -------------- |
| [Kong API key + ACL](#kong-api-key-flows) (`kong-api-key-acl`) | The request has a valid API key from a consumer you approved for the Product Environment | Two plugins on your Gateway Service. Consumers send a long-lived key in a header | You want the simplest setup that limits access to approved consumers. A key works until it is revoked, so a leaked key stays usable until you or the consumer act |
| [OAuth 2.0 Client Credentials](#oauth-20-client-credential-flow) (`client-credentials`) | The request has a valid, short-lived access token from an identity provider and, depending on the plugin configuration, the scopes or roles you granted | An Authorization Profile and a plugin. Consumers get a token from the identity provider before they call your API | You need scopes or roles, short-lived tokens, or a standard OAuth 2.0 flow your consumers already use. There is more to set up for you and your consumers |
| [Kong API key only](#kong-api-key-flows) (`kong-api-key-only`) | The request has a valid API key issued by any Gateway on the platform | One plugin on your Gateway Service | Your API is public. You get per-consumer identity and rate limits, but no control over who can call your API |

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
   key is not valid, the API Gateway denies access.

4. Key Management: API keys can be managed by you, the provider, allowing you to
   revoke or regenerate keys as needed. This provides a level of control over
   access to your API and enables you to respond to security threats or
   unauthorized access attempts.

Key-based authentication is simple to implement and widely used across various
APIs and services. However, it's important to handle API keys securely to
prevent unauthorized access or misuse.

### Kong API key flows

The API Services Portal supports two API key flows. Set the flow as the
**Authorization** on your Product Environment.

| Flow | Plugins | What the Gateway checks | Use for |
| ---- | ------- | ----------------------- | ------- |
| `kong-api-key-acl` (Kong API Key with ACL) | `key-auth` and `acl` | The API key is valid, **and** the consumer has been approved for your Product Environment | Most APIs protected with API keys |
| `kong-api-key-only` | `key-auth` | The API key is valid (for all Gateways on the platform) | Public APIs only |

With `kong-api-key-acl`, the Portal adds each approved consumer to an ACL group
named after the Product Environment's `appId`. Your `acl` plugin allows only
that group, so only consumers approved for your Environment can call your API.

With `kong-api-key-only`, approving an access request does not change what the
Gateway accepts. All Gateways on the platform share one Kong instance, and
consumers and their API keys are not scoped to a Gateway. A service protected by
the `key-auth` plugin alone accepts any valid API key issued by any Gateway on the
platform, not only keys issued for your API. The key still identifies the
consumer for rate limiting and lets you revoke access, and it keeps out
anonymous callers. It does not control which consumers can call your API.

!!! warning "Only use Kong API Key Only for public APIs"
    Use `kong-api-key-only` only when anyone could be allowed to call your API.
    For any API that should be limited to consumers you approve, use
    `kong-api-key-acl`.

    If your API is public and you want to give a higher rate limit to consumers
    who request one, see [Two-tiered access](/how-to/COMMON-CONFIG.md#two-tiered-access).

See the how-to on [Kong API Key + ACL](/how-to/kong-api-key.md) to protect your
API with an API key and ACL.

## OAuth 2.0 Client Credential Flow

With Oauth 2.0 client credential flow, the client application authenticates
itself with the API Gateway using its client ID and client secret. The API
gateway then forwards this authentication to the authorization server, which
issues an access token. With this token, the client can access protected
resources through the API gateway.

See the how-to on [Client Credential Protection](/how-to/client-cred-flow.md) to
protect your API with OAuth 2.0 Client Credentials Flow.

## Next steps

- [Kong API Key + ACL](/how-to/kong-api-key.md)
- [Client Credential Protection](/how-to/client-cred-flow.md)
