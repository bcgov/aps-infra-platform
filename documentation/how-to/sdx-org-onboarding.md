---
title: "Onboarding an Organization"
---

This page shows how to onboard an organization onto the Secure Data Exchange.

The steps described in this page are performed by the following roles:

| Role               | Function                                                                       |
| ------------------ | ------------------------------------------------------------------------------ |
| SDX Operator       | Establish member organizations and assign legal representatives Org Admin role |
| Organization Admin | Manage System Owner role assignment for the organization                       |
| System Owner       | Manage systems and service catalog entries for the particular organization     |

Use cases:

- Register new organization
- System Owner role assignment
- List organizations
- Assign gateway for organization

Available environments:

| Environment | Links                                                                                                                                                                                                                                               |
| ----------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `DEV`       | [API Console](https://api-gov-bc-ca.dev.api.gov.bc.ca/ds/api/sdx/v1/console), [OpenAPI Specification](https://api-gov-bc-ca.dev.api.gov.bc.ca/ds/api/sdx/v1/openapi.yaml), [Login](https://api-gov-bc-ca.dev.api.gov.bc.ca/login?identity=provider) |
| `TEST`      | Coming soon                                                                                                                                                                                                                                         |
| `PROD`      | Coming soon                                                                                                                                                                                                                                         |

## Register new organization

This is performed by the SDX Operator to onboard a new Organization.

=== "Restish CLI"

    Help information about the organization creation/update operation:

    ```sh
    restish aps put-organization
    ```

    Example:

    ```sh
    echo '
    {
      "name": "my-org",
      "title": "My Org",
      "description": "It is an organization for me",
      "extSource": "custom",
      "extRecordHash": "0000",
      "tags": [
        "member_class:MIN", "member_id:MYORG"
      ],
      "orgUnits": []
    }
    ' | restish aps put-organization ca.bc.gov
    ```

=== "Reference"

    - **API** `PUT /organizations/{org}`

    Parameters: `{org}=ca.bc.gov`

    ```json
    {
      "name": "ministry-of-food",
      "title": "Ministry of Food",
      "description": "It is a ministry concerned with food",
      "extSource": "custom",
      "extRecordHash": "0000",
      "tags": [
        "member_class:MIN",
        "member_id:FOOD"
      ],
      "publicBodyId": null,
      "orgUnits": []
    }
    ```

    `tags` is `array<string>`. An array containing an object is rejected by
    the live request schema.

## System Owner role assignment

This is performed by the Organization Admin to assign system owners access to manage
their systems and services.

The organization-scoped role that grants this access is `system-admin`, which
carries `System.Manage` for the organization. This is distinct from any
system-level roles and from `organization-admin`, which carries
`GroupAccess.Manage`, `Namespace.Assign`, and `Dataset.Manage` instead.

!!! warning
    Some existing organizations were provisioned before this role was
    introduced and still use a `system-owner` group instead. `system-owner` is
    not a currently supported role for newly onboarded organizations; using it
    returns `204 No Content` but does not create any organization-level group
    or permission, so the member is granted no access. Use `system-admin` for
    new organizations, and verify the resulting permission with a fresh token
    after assignment.

=== "Restish CLI"

    Help information about the organization role membership synchronization operation:

    ```sh
    restish aps put-organization-access
    ```

    Example:

    ```sh
    echo '
    {
      "name": "my-org",
      "parent": "/ca.bc.gov",
      "members": [
        {
          "member": {
            "email": "aidan.cope@gov.bc.ca"
          },
          "roles": ["system-admin"]
        }
      ]
    }
    ' | restish aps put-organization-access ca.bc.gov

    ```

=== "Reference"

    - API `PUT /organizations/{org}/access`

    Parameters: `{org}=ministry-of-food`

    ```json
    {
      "name": "ministry-of-food",
      "parent": "/ca.bc.gov",
      "members": [
        {
          "member": {
            "email": "janis@testmail.com"
          },
          "roles": ["system-admin"]
        }
      ]
    }
    ```

## List organizations

Retrieve the list of organizations available in the SDX catalog, optionally
including each organization's RBAC role membership.

=== "Restish CLI"

    ```sh
    restish sdx organization-list
    ```

    Include role membership:

    ```sh
    restish sdx organization-list --include-access
    ```

=== "Reference"

    - **API** `GET /catalog/organizations`

    Query parameters:

    - `includeAccess` (optional, boolean, default `false`) - when `true`,
      each organization entry includes an `access` array of its RBAC role
      members (`organization-admin`, `system-admin`).

    ```json title="Response Body (includeAccess=true)"
    [
      {
        "name": "ministry-of-food",
        "title": "Ministry of Food",
        "description": "It is a ministry concerned with food",
        "member": {
          "memberClass": "MIN",
          "memberId": "FOOD"
        },
        "access": [
          {
            "member": { "email": "janis@testmail.com" },
            "roles": ["system-admin"]
          }
        ]
      }
    ]
    ```

!!! note "`includeAccess` does not require authentication"
    `organization-list` has always been callable without a bearer token, and
    `includeAccess` does not change that: role membership is resolved using
    the platform's own Keycloak service credentials, not the caller's - so
    passing `includeAccess=true` returns every organization's role members
    to anonymous callers, the same way the base listing already returns
    every organization's name/title/member details to anonymous callers.

## Assign gateway for organization

An organization will have public keys that it will use for organization signing of
traffic through SDX. Each organization is assigned a unique gateway where the
public keys are managed.

=== "Restish CLI"

    Help information about the operation to assign a runtime group:

    ```sh
    restish sdx register-organization-gateway
    ```

    Example:

    ```sh
    restish sdx register-organization-gateway \
      my-org
    ```

## Next steps

- [Install a Runtime Group](/how-to/sdx-edge-servers.md)
