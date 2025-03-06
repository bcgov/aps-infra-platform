---
title: Kong 3.0 transition guide
---
 
## What is happening

API Program Services (APS) is preparing to upgrade instances of Kong Gateway
from version 2.8 to version 3.0. This is happening because Kong Enterprise
version 2.8 LTS is reaching vendor end of life on March 25, 2025. The upgrade
will enhance security and reliability, provide additional flexibility with
plugins, and provide significant performance enhancements.

## What action API providers need to take

With the release of Kong Gateway 3.0, route paths that use regular expressions
are no longer automatically detected. For Kong to parse paths that contain a
regular expression, the path must be prefixed with a `~`. All paths that do not
start with `~` will be considered plain text.

### Identify resources to update

The `gwa` CLI has been updated to identify configuration files that are
incompatible with Kong Gateway version 3.0. Run the `gwa apply` or `gwa pg`
commands with your current Gateway configuration file to receive an alert
identifying routes that need to be updated.

See the [Create a Gateway Service](how-to/create-gateway-service) documentation
for a refresher on Gateway configuration.

### Update resources

Depending on the [Gateway configuration format](concepts/gateway-config/#gateway-configuration-formats)
you are using, follow these steps:

#### Kong format

Manually add a `~` prefix to affected `route.paths` values or use the decK convert
[tool](https://docs.konghq.com/deck/reference/3.0-upgrade/#convert-declarative-configuration-files).
Publish the updated configuration file using `gwa apply` or `gwa pg`.

#### Resource-based format

Manually add a `~` prefix to affected `route.paths` values. Publish the updated
configuration file using `gwa apply` or `gwa pg`.

APS will ensure backwards compatibility with Kong Gateway version 2.8 during
this transition period. We encourage API provider teams to test their
configuration updates in `dev` or `test` environments before releasing changes
to production.

### Update timeline

API provider teams should plan to complete necessary configuration updates by
**March 25, 2025**.

## What action API consumers need to take

No action is required for API consumers. There are no impacts to API consumers
using existing services during the transition period.

## Support options

More information can be found in the [Kong documentation](https://docs.konghq.com/deck/reference/3.0-upgrade/)
for version 3.0 upgrades.

If you require further clarification or assistance, please [contact us](how-to/get-support).
