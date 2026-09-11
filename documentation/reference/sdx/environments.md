---
title: "SDX Environments"
---

!!! note "Playground"

    The Playground environment is for service providers to verify the
    installation of SDX and test new functionality before moving it to production.
    This environment provides no data or service quality guarantees.

!!! note "Production"

    The Production environment supports the Test data and Production
    data SDX instances. Data and service quality is the same for both SDX
    instances. The Production environment also supports a `Staging` environment
    for runtime group operators to stage infrastructure changes.

## Useful links

Links to the different services for each environment:

| Service               | Playground                                                                     | Production                                                  |
| --------------------- | ------------------------------------------------------------------------------ | ----------------------------------------------------------- |
| SDX UI                | [UI](https://sdx-api-gov-bc-ca.test.api.gov.bc.ca)                             | [UI](https://sdx.gov.bc.ca)                                 |
| SDX Member API        | [API](https://api-gov-bc-ca.test.api.gov.bc.ca/ds/api/sdx/v1/console)          | [API](https://api.gov.bc.ca/ds/api/sdx/v1/console)          |
| OpenAPI Specification | [OpenAPI](https://api-gov-bc-ca.test.api.gov.bc.ca/ds/api/sdx/v1/openapi.yaml) | [OpenAPI](https://api.gov.bc.ca/ds/api/sdx/v1/openapi.yaml) |
| API Services Portal   | [APS Portal](https://api-gov-bc-ca.test.api.gov.bc.ca/login?identity=provider) | [APS Portal](https://api.gov.bc.ca/login?identity=provider) |

## Environment labels

| APS Environment | SDX Environment | Purpose                  |
| --------------- | --------------- | ------------------------ |
| APS Dev         | `apsdev`        | APS internal development |
| APS Test        | `apstst`        | SDX Playground           |
| APS Prod        | `stg`           | SDX Staging              |
| APS Prod        | `bct`           | SDX Non-Prod             |
| APS Prod        | `bc`            | SDX Prod                 |

## Playground

### SDX Playground

Subsystem authentication in SDX is performed using a token that is issued
by Common SSO.

For access to services in this `Playground` environment, the following token
issuers are accepted:

- `https://dev.sandbox.loginproxy.gov.bc.ca/auth/realms/standard`
- `https://test.sandbox.loginproxy.gov.bc.ca/auth/realms/standard`
- `https://sandbox.loginproxy.gov.bc.ca/auth/realms/standard`

## Production

### SDX Staging

Subsystem authentication using tokens from Common SSO is not supported in `Staging`.

Clients can use the internal consumer endpoints of the relevant runtime groups
to call services in this environment.

### SDX Non-Prod

For access to services in `Non-Prod`, the following token issuers are accepted:

- `https://dev.loginproxy.gov.bc.ca/auth/realms/standard`
- `https://test.loginproxy.gov.bc.ca/auth/realms/standard`

!!! note "BC Services Card `sub`"

    For BC Services Card login, both of these environments reference the
    BCSC Test environment, so they return the same `sub` when it
    comes to privacy zones.

Services that are running in `Non-Prod` can choose either `dev` or `test` tokens
from CSS.

!!! note "Token exchange"

    For cases where the service is also calling SDX services, the token is
    passed through as-is, and SDX performs the token exchange.

### SDX Prod

For access to services in `Prod`, the following token issuers are accepted:

- `https://loginproxy.gov.bc.ca/auth/realms/standard`
