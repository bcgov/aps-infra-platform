---
title: Client Onboarding - Silver, Gold and Emerald Clusters
---

This page provides step-by-step instructions to onboard the upstream services across Silver, Gold, and Emerald clusters. It covers service configuration, network policies, DNS requirements, and special considerations like mTLS setup.

## Cluster Options

| Consumer    | Description   | Onboarding Steps   | Traffic routing policies                                                                                                                                                                                                                          |
| ----------- | ----------------- | ------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Silver  | Default cluster with self-serve capabilities | 1. Configure Gateway Service<br>
2. Set up Network Policy<br>
3. Deploy | Traffic flows through the Silver Kong data plane via routes on the Silver OpenShift cluster. |
| Gold | Requires APS involvement for DNS setup. Supports failover to the Gold DR cluster in Calgary. | 1. Contact APS for DNS setup<br>
2. Configure Gateway Service<br>
3. Network Policy Setup<br>
4. Deploy
 | Routes traffic through Kong data planes on the Gold OpenShift cluster.                                                                                                                        |
 | Emerald | High-security cluster, requires APS for DNS & egress policies | 1. Contact APS for DNS & Egress Policies<br>
 2. Configure Gateway Service (DataClass tag required)<br>
 3. Setup Ingress/Egress Policies<br>
 4. Deploy
 | Routes traffic to pods on the Emerald cluster, which may be inaccessible due to network restrictions.                                                                                                                        |

## Onboarding to Silver Cluster (Default)
The Silver cluster is the default cluster for new clients, and new Gateways are automatically created within this cluster. Traffic to Gateway Services on a Gateway located in the Silver cluster is routed through the Silver Kong data plane via routes on the Silver Openshift cluster.

The onboarding process for the Silver cluster is fully self-service and does not require any manual intervention from APS.

### Flowchart: Silver Onboarding
![Silver Onboarding](/artifacts/ToSilver.png "Silver Onboarding")

### Steps:
1. Client Registration - Client signs up and initiates API Gateway onboarding via the Developer Portal.
2. Gateway Creation - By default, a Gateway is created on the Silver cluster automatically using the `gwa` CLI tool.
3. Routing Setup - All service traffic is routed through Silver Kong Data Plane and corresponding OpenShift routes are set up.
4. No Manual APS Steps Required
   * No DNS update needed
   * No Keycloak attribute configuration
   * No additional NetworkPolicy changes

For detailed instructions on configuring the gateway in the Silver cluster, please visit the [Set up an Upstream Service](https://developer.gov.bc.ca/docs/default/component/aps-infra-platform-docs/how-to/upstream-services/#silver-cluster) page.

## Onboarding to Alternate Clusters (Gold & Emerald)
Gateways can also be created or migrated to Gold or Emerald clusters. This requires coordinated manual steps involving both the API Provider and APS Team.

### Flowchart: Gold/Emerald Onboarding
![Gold/Emerald Onboarding](/artifacts/ToGoldEmerald.png "Gold/Emerald Onboarding")

### Detailed Steps:
#### Step 1: Remove Silver Config (if migrating)
For clients transitioning from Silver to Gold/Emerald, it’s critical that the services are removed from Silver before being setup on Gold/Emerald.

| Performer   | Action   | 
| ----------- | ----------------- | 
| API Provider | Run `gwa pg` with yaml: `services: []` to remove Silver config. |

_Reason_: Routes are managed up by the `kube-api:` the Silver `kube-api` has to remove all the related routes, and then the Gold/Emerald `kube-api` will provision the new ones on the respective cluster.

#### Step 2: Create Gateway for Gold/Emerald
The first step for new clients or the second step for transitioning clients is to create a Gateway using `gwa` that will be assigned to the alternate Kong data plane.

| Performer | Action   | 
| ----------- | ----------------- | 
| API Provider  | Create new Gateway using `gwa` CLI for Gold/Emerald. Existing Gateways **cannot be reused** due to namespace-specific routing. |

For detailed instructions on configuring the gateway in the Gold cluster, please visit the [Set up an Upstream Service](https://developer.gov.bc.ca/docs/default/component/aps-infra-platform-docs/how-to/upstream-services/#gold-cluster) page.

For detailed instructions on configuring the gateway in the Emerald cluster, please visit the [Set up an Upstream Service](https://developer.gov.bc.ca/docs/default/component/aps-infra-platform-docs/how-to/upstream-services/#emerald-cluster) page.

#### Step 3: Configure the Gateway in Keycloak
| Performer    |  Action  | 
| ----------- | ----------------- | 
| APS Team  | Add attributes in Keycloak under APS Realm → Groups → ns → Gateway Group → Attributes Tab. |

**Keycloak Attributes:**
| Cluster    | Attribute Key   | Attribute Value   | 
| ----------- | ----------------- | ----------------- | 
| Gold  | perm-data-plane | `konghd-kong-proxy` |
| Emerald  | perm-data-plane | `dp-emerald-kong-proxy` |
| Emerald  | perm-upstreams | e.g.,`ff22b9-test,ff22b9-prod` |

The API provider must set the `Service.host` parameter to point to the correct OpenShift services using the format: `<SERVICE>.<PROJECT>.svc` or `<SERVICE>.<PROJECT>.svc.cluster.local`. Any other `Service.host` values outside of this format will be **rejected**.

#### Step 4: Update Gateway Configuration
| Performer    |  Action  | 
| ----------- | ----------------- | 
| API Provider  | Update `Service.host` in Gateway config to point to Gold/Emerald service URLs. |

Refer to the TechDocs for detailed [Gold](https://developer.gov.bc.ca/docs/default/component/aps-infra-platform-docs/how-to/upstream-services/#gold-cluster) and [Emerald](https://dev.developer.gov.bc.ca/docs/default/component/aps-infra-platform-docs/how-to/upstream-services/#emerald-cluster) configurations.


#### Step 5: Update DNS in Remedy
The client must supply the Route `hosts` intended for use in the Gold cluster, allowing us to update DNS to direct traffic to the Gold or Emerald clusters for those domains. Any future changes to these Route `hosts` must also be communicated to the APS team; otherwise, traffic will default to the Silver OpenShift cluster.

| Performer    |  Action  | 
| ----------- | ----------------- | 
|  APS Team | 1. Login to [Remedy](https://remedyapps.gov.bc.ca/)<br> 
2. Open `NNRv2`<br>
3. Navigate to the `DNS` tab. In the `Search DNS` field, enter `%.api.gov.bc.ca` and click the first icon to the right of the text box.<br>
4. Go to `Quick Update and Add`, then add an entry for each host according to the service type. |

**Service Type Configuration:**
| Service Type    | Record Type   | TTL | Data / CNAME Target   | 
| ----------- | ----------------- | -----------| ----------------- | 
| Gold (with DR)  | CNAME | 300 | `ggw.api.gov.bc.ca.glb.gov.bc.ca` |
| Gold (no DR)  | CNAME | 300 | `kdc.api.gov.bc.ca` |
| Emerald  | A | 600 | `*IP from Emerald OpenShift Route` |

**IP from Emerald OpenShift Route*: On Emerald cluster, lookup the corresponding OpenShift Route's `status.ingress[0].conditions[0].message` for the IP Address.

#### Step 6: Update Network Policy
| Performer   | Action  | 
| ----------- | ----------------- | 
| API Provider (APS assists for Emerald) | Add NetworkPolicy to allow Kong traffic to Gold/Emerald services. For Emerald, APS configures additional egress policies. |

Refer to the TechDocs for detailed [Gold](https://developer.gov.bc.ca/docs/default/component/aps-infra-platform-docs/how-to/upstream-services/#gold-cluster) and [Emerald](https://dev.developer.gov.bc.ca/docs/default/component/aps-infra-platform-docs/how-to/upstream-services/#emerald-cluster) configurations.

**Example for Emerald Cluster: upstream project `ff22b9` **
```yaml
kind: NetworkPolicy
apiVersion: networking.k8s.io/v1
metadata:
  name: allow-kong-traffic-to-upstream-ff22b9
  namespace: cc9a8a-prod
spec:
  podSelector:
    matchLabels:
      app.kubernetes.io/instance: apsgw
    matchExpressions:
      - key: app.kubernetes.io/name
        operator: In
        values:
          - emerald-kong
          - kubeapi
  egress:
    - to:
        - namespaceSelector:
            matchLabels:
                environment: test
                name: ff22b9
    - to:
        - namespaceSelector:
            matchLabels:
                environment: prod
                name: ff22b9
  policyTypes:
    - Egress
```

#### Step 7: Test End-to-End Connectivity
| Performer    |  Action  | 
| ----------- | ----------------- | 
| API Provider   | Wait 15-20 minutes for DNS propagation. Test connectivity using the new Route. Hardcode IP if necessary. |
