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

Available environments:

| Environment | Links                                                                                                                                                                                                                                                           |
| ----------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `LAB`       | [API Console](https://api-gov-bc-ca-lab.dev.api.gov.bc.ca/ds/api/sdx/v1/console), [OpenAPI Specification](https://api-gov-bc-ca-lab.dev.api.gov.bc.ca/ds/api/sdx/v1/openapi.yaml), [Login](https://api-gov-bc-ca-lab.dev.api.gov.bc.ca/login?identity=provider) |
| `DEV`       | [API Console](https://api-gov-bc-ca.dev.api.gov.bc.ca/ds/api/sdx/v1/console), [OpenAPI Specification](https://api-gov-bc-ca.dev.api.gov.bc.ca/ds/api/sdx/v1/openapi.yaml), [Login](https://api-gov-bc-ca.dev.api.gov.bc.ca/login?identity=provider)             |
| `TEST`      | Coming soon                                                                                                                                                                                                                                                     |
| `PROD`      | Coming soon                                                                                                                                                                                                                                                     |

## Register new organization

This is performed by the SDX Operator to onboard a new Organization.

=== "Restish CLI"

=== "Reference"

    - **API** `PUT /organizations/{org}`

    Parameters: `{org}=ca.bc.gov`

    ```json
    {
      "extForeignKey": "ministry-of-food",
      "name": "ministry-of-food",
      "title": "Ministry of Food",
      "description": "It is a ministry concerned with food",
      "extSource": "custom",
      "extRecordHash": "0000",
      "tags": [],
      "orgUnits": []
    }
    ```

## System Owner role assignment

This is performed by the Organization Admin to assign system owners access to manage
their systems and services.

The `System Owner` is able to register new subsystems and services
and browse the service catalog.

> **API** `PUT /organizations/{org}/access`

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
