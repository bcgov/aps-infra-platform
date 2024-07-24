---
title: Plugins
---

This article explains the basics of Plugins, and how they work to extend the functionality of your [Gateway Services](/concepts/services.md).

## Purpose

Plugins extend the functionality of Kong Gateway, allowing you to add new features to your implementation.
Plugins can perform various tasks such as authentication, rate limiting, logging, transformation of requests and
responses, security enforcement, and more. Plugins can be configured to run in a variety of contexts, ranging from
a specific route to all upstreams, and can execute actions inside Kong before or after a request has been proxied
to the upstream API, as well as on any incoming responses.

Some common types of Kong plugins include:

1. Authentication plugins: These plugins enable different authentication mechanisms such as API keys, JWT, OAuth, and basic authentication.

2. Rate limiting plugins: Rate limiting plugins help in controlling the rate at which requests are made to APIs, preventing abuse and ensuring fair usage.

3. Logging plugins: Logging plugins allow users to log request and response data for monitoring, analysis, and debugging purposes.

4. Transformation plugins: Transformation plugins modify the request or response data, enabling tasks like request/response body manipulation, header manipulation, and response caching.

## Next steps

If you would like to dive deeper or start using plugins on your gateway services, check out the following resources:

How-to Guides

- [Common Controls](how-to/COMMON-CONFIG.md)

Reference

- [Supported Plugins](/reference/plugins/AVAILABLE-PLUGINS.md)

External Resources

- [Kong: Plugins](https://docs.konghq.com/gateway/latest/key-concepts/plugins/)

