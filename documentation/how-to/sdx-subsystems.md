---
title: "Managing systems and services"
---

## Overview

This page shows how to manage subsystems and services on the Secure Data Exchange.

The steps described in this page are performed by the following roles:

| Role         | Function                                                                   |
| ------------ | -------------------------------------------------------------------------- |
| System Owner | Manage systems and service catalog entries for the particular organization |

Use cases:

- Register a subsystem
- Register a service
- View API service catalog

## Prerequisites

- [Install Restish CLI](/reference/restish-cli.md)

## Register a subsystem

=== "Restish CLI"

    Help information about the operation:

    ```sh
    restish dev create-subsystem
    ```

    Example call:

    ```sh
    restish dev create-subsystem \
      ministry-of-citz \
      name: MY-NEW-SUBSYSTEM
    ```

=== "Reference"

    > **API** `PUT /organizations/{org}/subsystems`

    Parameters: `{org}=ministry-of-food`

    ```json
    {
      "name": "MY-NEW-SUBSYSTEM"
    }
    ```

## Register a service

=== "Restish CLI"

    Help information about the operation:

    ```sh
    restish dev create-oas-service
    ```

    Example:

    ```sh
    -- does not work currently with restish :(
    restish dev create-oas-service \
      ministry-of-citz \
      subsystem: MY-NEW-SUBSYSTEM, \
      configFile: @openapi.yaml
    ```

=== "Reference"

    > **API** `PUT /organizations/{org}/oas-service`

    Parameters: `{org}=ministry-of-food`

    Specify the subsystem and choose a file for the OpenAPI Spec
    (YAML format) of your API.

## View API service catalog

=== "Restish CLI"

    List all subsystems:

    ```sh
    restish dev subsystems-list
    ```

    List only name and title of APIs:

    ```sh
    restish dev list-service-catalog | jq '.[] | .name+"   "+.title'
    ```

=== "Reference"

    > **API** `GET /catalog/services`

Example response:

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
