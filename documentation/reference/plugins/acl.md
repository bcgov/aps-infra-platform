# Access Control List

The `acl` plugin can be used in order to restrict access to a service or route
by adding consumers to allowed or denied lists using arbitrary Access Control
List (ACL) groups.

## Configuration reference

This is a stock plugin from Kong Hub. See the [configuration reference page](https://docs.konghq.com/hub/kong-inc/acl/configuration/)
for a list of parameters and protocol compatibility notes.

## Common usage example

Typically this is used with the `kong-api-key-acl` flow, where the `allow`
group is the Product Environment's `appId`. Access Managers can then grant or
revoke access to the Service from the API Services Portal. See
[Kong API Key + ACL](/how-to/kong-api-key.md) for how to get the `appId` and
configure the `key-auth` and `acl` plugins together.

To restrict access using ACL groups, add this section to your GatewayService
configuration file:

```yaml

plugins:
- name: acl
  service: <SERVICE_NAME>
  tags: [ ns.<gatewayId> ]
  config:
    allow:
    - <environment appId>
    deny: null
    hide_groups_header: true
```

Replace `<SERVICE_NAME>` with the name of the service that this plugin
configuration will target, and `<environment appId>` with the `appId` of the
Product Environment.
