---
title: "Onboarding onto the Secure Data Exchange"
---

This page shows how to onboard onto the Secure Data Exchange.

The steps described in this page are performed by the following roles:

| Role               | Function                                                                    |
| ------------------ | --------------------------------------------------------------------------- |
| SDX Operator       | Establish member organization and grant legal representative org admin role |
| Organization Admin | Manage System Owner role assignment for the organization                    |
| System Owner       | Manages systems and service catalog entries for the particular organization |

Use cases:

- Register new organization
- System Owner role assignment
- Register a subsystem
- Register a service
- View service catalog

Available environments:

| Environment | Swagger Console                                                                                                                                                                                                                                      |
| ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `FEATURE`   | [API Console](https://api-services-portal-feature-sdx-service.apps.silver.devops.gov.bc.ca/ds/api/sdx/v1/console/), [OpenAPI Specification](https://api-services-portal-feature-sdx-service.apps.silver.devops.gov.bc.ca/ds/api/sdx/v1/openapi.yaml) |
| `DEV`       | Coming soon                                                                                                                                                                                                                                          |
| `TEST`      | Coming soon                                                                                                                                                                                                                                          |
| `PROD`      | Coming soon                                                                                                                                                                                                                                          |

## Register new organization

This is performed by the SDX Operator to onboard a new Organization.

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

This is performed by the SDX Operator to assign system owners access to manage
their systems and services.

The `System Owner` is able to register new subsystems and services
and browse the service catalog.

> **API** `PUT /organizations/{org}/access`

Parameters: `{org}=ca.bc.gov`

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

## Register a subsystem

> **API** `PUT /organizations/{org}/subsystems`

Parameters: `{org}=ministry-of-food`

```json
{
  "name": "MY-NEW-SUBSYSTEM"
}
```

## Register a service

> **API** `PUT /organizations/{org}/oas-service`

Parameters: `{org}=ministry-of-food`

Specify the subsystem and choose a file for the OpenAPI Spec
(YAML format) of your API.

## View service catalog

> **API** `GET /catalog/services`

```json
[
  {
    "name": "ministry-of-citizens-services.OAS-SPECTRAL-VALIDATION.v0",
    "title": "OAS Spectral Validation API",
    "version": "0.1.0",
    "summary": null,
    "description": "A governance API for discovering and using BCGov Spectral rulesets to validate OpenAPI Specification documents.\nRepository: https://github.com/bcgov/csit-api-governance-spectral-style-guide",
    "subsystem": {
      "name": "DEF",
      "organization": {
        "name": "ministry-of-citizens-services"
      },
      "gateway": {
        "id": "sdx-gw-7053d"
      }
    },
    "operations": [
      {
        "operationId": "listVersions",
        "method": "GET",
        "path": "/versions",
        "summary": "List available ruleset versions",
        "scopes": []
      },
      {
        "operationId": "listRulesetsInVersion",
        "method": "GET",
        "path": "/versions/{version}/rulesets",
        "summary": "List Spectral rulesets in a version",
        "scopes": []
      },
      {
        "operationId": "createValidation",
        "method": "POST",
        "path": "/versions/{version}/rulesets/{ruleset}/validations",
        "summary": "Validate an OpenAPI document",
        "scopes": []
      }
    ]
  }
]
```
