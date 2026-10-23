---
title: "Connecting a Service"
---

Connect your consumer system to a provider service on the Secure Data Exchange
using the consumer journey for the service's authorization policy. The
`policyVersion` identifies the policy when a request is submitted.

## Choose your consumer journey

| Policy | Consumer requesting experience |
| --- | --- |
| [SDX.R0.00 — Request access](/how-to/sdx-connections-r0-policy.md) | A consumer Tech Lead submits a peer-to-peer request through Restish with requester details. Available only in the SDX Playground. |
| [SDX.R1.00 — Request access through Common SSO](/how-to/sdx-connections-r1-policy.md) | A CSS integration owner requests service/version and scope access through the supported CSS/SDX integration. Includes user-token setup and cross-privacy-zone exchange where configured. |

## After requesting access

Follow [connection notifications, approval and consumer testing](/how-to/sdx-connection-approval.md)
for the shared provider review, activation, testing and cleanup steps. An approved
request still requires provisioned gateways; R1 also requires confirmation that
CSS scope grants have synchronized.

For gateway configuration details, see [Connection Resources](/how-to/sdx-connection-resources.md).

## Troubleshooting token-exchange scopes and audiences

R1 troubleshooting has moved to [the R1 policy guide](/how-to/sdx-connections-r1-policy.md#troubleshooting-token-exchange-scopes-and-audiences).
