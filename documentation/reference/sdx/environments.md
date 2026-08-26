---
title: "SDX Environments"
---

!!! Playground

    The Playground environment is for service providers to verify the
    installation of SDX and test new functionality before moving it to production.
    There is NO data or service quality in this environment!

!!! Production

    The Production environment supports the Test data and Production
    data SDX instances. Data and service quality is the same for both SDX
    instances.  It also supports a `Staging` environment for runtime group
    operators to stage infrastructure changes.

Links to the different services for each environment:

| Service               | Playground                                                                     | Production                                                  |
| --------------------- | ------------------------------------------------------------------------------ | ----------------------------------------------------------- |
| SDX UI                | [UI](https://sdx-api-gov-bc-ca.test.api.gov.bc.ca)                             | [UI](https://sdx.gov.bc.ca)                                 |
| SDX Member API        | [API](https://api-gov-bc-ca.test.api.gov.bc.ca/ds/api/sdx/v1/console)          | [API](https://api.gov.bc.ca/ds/api/sdx/v1/console)          |
| OpenAPI Specification | [OpenAPI](https://api-gov-bc-ca.test.api.gov.bc.ca/ds/api/sdx/v1/openapi.yaml) | [OpenAPI](https://api.gov.bc.ca/ds/api/sdx/v1/openapi.yaml) |
| API Services Portal   | [APS Portal](https://api-gov-bc-ca.test.api.gov.bc.ca/login?identity=provider) | [APS Portal](https://api.gov.bc.ca/login?identity=provider) |

## Production

Production is split into the following environments:

- `Staging` : reserved for runtime group administrators to stage infrastructure
- `Non-Prod` : functionally equivalent to production, but with connected synthetic data
- `Prod` : live data

Subsystem authentication in SDX is performed using a token that is issued
by Common SSO.

For access to services in `Non-Prod`, the following token issuers are accepted:

- https://dev.loginproxy.gov.bc.ca/auth/realms/standard
- https://test.loginproxy.gov.bc.ca/auth/realms/standard

For access to services in `Prod`, the following token issuers are accepted:

- https://loginproxy.gov.bc.ca/auth/realms/standard

Subsystem authentication using tokens from Common SSO is not supported in `Staging`.

### Services that are also SDX Clients

Services that are running in `Prod` will only be allowed to access services
running in `Prod`.

Services that are running in `Non-Prod` can choose either `dev` or `test` tokens
from CSS.

!!! note "Token Exchange"

    For cases where the service is also calling SDX services, the token will be
    passed through as-is, where SDX will perform token exchange.

    The use case of a service provider that is also an SDX client calling another service,
    is still under construction and not supported at this time.
