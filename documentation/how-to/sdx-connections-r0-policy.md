---
title: "Request access with SDX.R0.00"
---

Use R0 for a basic peer-to-peer connection in the SDX Playground. The consumer
Tech Lead submits the connection request using Restish with `policyVersion:
SDX.R0.00` and requester details. For CSS integration and scope-based access,
use the [R1 consumer journey](/how-to/sdx-connections-r1-policy.md).

## Prerequisites

- [Install Restish CLI](/reference/restish-cli.md).
- Complete [organization onboarding](/how-to/sdx-org-onboarding.md) and
  [subsystem registration](/how-to/sdx-subsystems.md).
- Select the Playground endpoints from [SDX environments](/reference/sdx/environments.md).
- Identify the provider service/version and consumer subsystem. Confirm the
  participating [runtime groups and gateways](/how-to/sdx-edge-runtime-groups.md)
  are ready with the provider/operator.

## Request access (as consumer)

=== "Restish CLI"

    Help information about the operation:

    ```sh
    restish sdx upsert-connection
    ```

    Example call:

    ```sh
    restish sdx upsert-connection \
      my-org \
      clientId: MIN.MYORG.MY-NEW-SUBSYSTEM, \
      serviceId: LAB.MIN.MYORG.EFV-ICBC.v0, \
      policyVersion: SDX.R0.00, \
      "requesterDetails: {}"
    ```

!!! note "requester details"

    Under `SDX.R0.00`, `requesterDetails` must be supplied together with
    `policyVersion` on this initial request — when both are present, the
    controller replaces `requesterDetails.requester` with the authenticated
    caller's name and email. Omitting `requesterDetails` leaves an invalid
    empty default in place that will pass creation but fail activation.
    `requesterDetails` can only be set on creation; it cannot be repaired
    afterwards through `upsert-connection` (that field is reserved for the
    provisioner on update) — if activation fails for a missing requester
    record, deactivate and delete the connection, then recreate it with
    `policyVersion` and `requesterDetails` included together.

After submission, follow the shared [notifications, approval and consumer testing
steps](/how-to/sdx-connection-approval.md). Submission does not establish an active
connection. Use the service's documented authentication for testing; the R1 CSS
user-token and token-exchange instructions belong to the R1 journey.
