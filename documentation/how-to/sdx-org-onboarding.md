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

    Help information about the operation to list available runtimes:

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
        { "member_class": "MIN", "member_id": "FOOD" }
      ],
      "publicBodyId": null,
      "orgUnits": []
    }
    ```

## System Owner role assignment

This is performed by the Organization Admin to assign system owners access to manage
their systems and services.

The `System Owner` is able to register new subsystems and services
and browse the service catalog.

=== "Restish CLI"

    Help information about the operation to list available runtimes:

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
          "roles": ["system-owner"]
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
          "roles": ["system-owner"]
        }
      ]
    }
    ```

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
