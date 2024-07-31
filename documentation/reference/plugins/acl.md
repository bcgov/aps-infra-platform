# Access Control List

The `acl` plugin can be used in order to restrict access to a service or route
by adding consumers to allowed or denied lists using arbitrary Access Control
List (ACL) groups.

## Configuration reference

This is a stock plugin from Kong Hub. See the [configuration reference page](https://docs.konghq.com/hub/kong-inc/acl/configuration/)
for a list of parameters and protocol compatibility notes.

## Common usage example

Typically this is used when your Environment configuration uses the flow
`kong-api-key-acl` or `kong-acl-only` where the `allow` group is a special group
defined for the Environment so that Access Managers can grant/revoke access to
the Service from the API Services Portal.

To restrict access using ACL groups, add this section to your GatewayService
configuration file:

```yaml

plugins:
- name: acl
  service: <SERVICE_NAME>
  tags: [ ns.<gatewayId> ]
  config:
    allow:
    - pir-dev
    deny: null
    hide_groups_header: true
```

Replace <SERVICE_NAME> with the name of the service that this plugin
configuration will target.
