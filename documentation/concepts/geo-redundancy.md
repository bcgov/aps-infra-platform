---
title: Geographic Redundancy and Failover
---

<!-- overview -->

This article explains the basics of geographic redundancy and how it works in
the {{ glossary_tooltip term_id="api-services-portal" }}.

Geographic redundancy is a high-availability architecture that maintains
duplicate infrastructure in geographically separate data centres. In the event
that one data centre becomes unavailable, traffic can be redirected to another
data centre with minimal service disruption.

API Program Services (APS) maintains core infrastructure on the Gold (Kamloops
data centre) and Gold DR (Calgary data centre) OpenShift clusters to provide
geo-redundancy. In the event of an incident impacting service availability on
the Gold cluster, traffic will be directed to the Gold DR cluster. Background
information on the BC Government Private Cloud clusters is available on the
[Hosting Tiers](https://digital.gov.bc.ca/cloud/services/private/products-tools/hosting-tiers/)
article.

Geo-redundancy through an active-passive high availability configuration
provides uninterrupted traffic flow through the {{ glossary_tooltip term_id="api-gateway" }} for configured 
{{ glossary_tooltip term_id="gateway" text="Gateways" }}. It also ensures continued API gateway administration 
for all {{ glossary_tooltip term_id="api-provider" text="API providers" }}, with a brief (15-20 minute) 
maintenance window in the event of failover; a banner will be displayed on 
[https://api.gov.bc.ca](https://api.gov.bc.ca) and `gwa` CLI commands will fail.

!!! note "Gateway configuration"
    Gateway geo-redundancy is only enabled upon request and requires a
    suitable high availability upstream configuration. By default, new Gateways are
    created on the Silver cluster, without geo-redundancy. API providers with
    services on the Gold cluster should contact APS to have their Gateway
    configured. Visit our docs for more information on Gateway and 
    [upstream service configuration](/how-to/upstream-services.md).

## What happens when failover occurs?

Traffic distribution is managed using OCIO's F5 Global Server Load Balancer
(GSLB) to control DNS resolution. The GSLB checks an APS-managed health endpoint
to determine where to resolve client calls to `*api.gov.bc.ca` (or other custom
domain) hosts configured for geo-redundancy. The GSLB resolution endpoint is
`ggw.api.gov.bc.ca.glb.gov.bc.ca`.

Under normal circumstances, calls resolve to Gold. If the health endpoint is
unreachable or shows an unhealthy status, the GSLB will resolve to the IP for
Gold DR; that is, failover will occur. Client traffic will flow to the API
gateway on Gold DR and on to upstream services on Gold DR.

!!! note "Gold without failover"
    API providers who are using Gold without geographic failover to Gold DR
    will see traffic continue to be directed to the Gold gateway and upstream
    services on Gold.

## When does failover occur?

Failover will occur anytime the health endpoint is unavailable, however briefly.
The health endpoint is expected to be unavailable and trigger failover when
there is a data centre or cluster-level disruption. 

On occasion, node drains (e.g. as part of cluster maintenance) and node failures
can result in failover. APS aims to minimize these events but maintains a high
level of sensitivity on the health endpoint to minimize downtime in the event of
an incident.

In case of failover, a notification will be sent to [#aps-ops](https://chat.developer.gov.bc.ca/channel/aps-ops) on Rocket.Chat.

## When will services be restored to Gold after failover?

APS aims to recover services to Gold by the next business day following
failover. As with failover, there will be no gateway downtime but a short
maintenance window for gateway administration.

Notifications will be sent to #aps-ops on Rocket.Chat announcing when recovery
will occur and after recovery is complete.

## What do API provider teams need to do?

API providers should have their services running in both data centres at all
times and capable of handling traffic.

In the event of failover, API providers do not need to take any action. Teams
should monitor their services to ensure traffic is reaching their upstreams on
Gold DR and their API is functioning as expected.

Similarly, no action is required following recovery to Gold.

## What do API consumers need to do?

API consumers (client application teams) do not need to take any action. There
will not be any consumer impact when failover occurs.

## Next steps

- [Get Support](/how-to/get-support.md)
- [Set Up an Upstream Service](/how-to/upstream-services.md)
