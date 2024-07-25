---
title: Monitor your Services
---

## View metrics

You can view the following metrics in real-time for the Services that you
configure on the Gateway:

- **Request Rate**: Requests / Second (by Service/Route, by HTTP Status)
- **Latency**: Standard deviations measured for latency inside Kong and on the
  Upstream Service (by Service/Route)
- **Bandwidth**: Ingress/egress bandwidth (by Service/Route)
- **Total Requests**: In 5 minute windows (by Consumer, by User Agent, by
  Service, by HTTP Status)

All metrics can be viewed by an arbitrary time window; default is **Last 24 Hours**.

Go to `Grafana` to view metrics for your configured services.

| Environment     | Grafana Link                                      |
| --------------- | ------------------------------------------------- |
| TEST / TRAINING | <https://grafana-apps-gov-bc-ca.test.api.gov.bc.ca> |
| PRODUCTION      | <https://grafana.apps.gov.bc.ca>                    |

You can also access summarized metrics from the API Services Portal by going to
the **Gateways** tab, selecting the desired **Gateway**, clicking
**Gateway Services**, and expanding the accordion of the Service in **7 Day Metrics**.

!!! note
    A shortcut to Grafana is provided from the **Gateway Services** page by
    clicking **View metrics in real-time**.
