---
title: "Add CI/CD Integration"
---

This guide explains how to add CI/CD integration for publishing Gateway
configuration alongside your project code.

API Program Services recommends CI/CD integration to keep your Gateway
configuration trackable and in sync with your project.

While there is no published GitHub Actions workflow, the `gwa` CLI provides a
straightforward way to publish your Gateway configuration in CI/CD pipelines.

## Before you begin

You should be familiar with how to [create a Gateway Service](/how-to/create-gateway-service.md).

Before you begin, ensure you:

- [Install gwa CLI](/how-to/gwa-install.md)
- [Create a Gateway](/how-to/create-gateway.md)
- [Generate a Service Account](/how-to/generate-service-account.md)

## Github Actions examples

In the repository where you maintain your CI/CD pipeline, set up two `Secrets`
with service account credentials for your Gateway:

- GWA_CLIENT_ID
- GWA_CLIENT_SECRET

### Single Gateway configuration file

You may choose to keep all your Gateway configuration in a single file,
potentially including Gateway Services for all environments.

Sample folder structure:

```text
Add a `.gwa` folder that will be used to hold your Gateway configuration.

.gwa
└── gw-config.yaml
```

Sample Github workflow:

```yaml
name: Publish Gateway Configuration

on:
  push:
    branches: [ main ]

jobs:
  publish:
    runs-on: ubuntu-latest
    env:
      GW: <gatewayId> # replace with your gateway ID
    steps:
      - uses: actions/checkout@v6

      - name: Get GWA Command Line
        run: |
          GWA_CLI_VERSION=v3.0.6
          curl -L -O https://github.com/bcgov/gwa-cli/releases/download/${GWA_CLI_VERSION}/gwa_Linux_x86_64.tgz
          tar -xf gwa_Linux_x86_64.tgz

      - name: Apply Gateway Configuration
        run: |
          export PATH=`pwd`:$PATH
          cd .gwa
          
          gwa login \
          --client-id=${{ secrets.GWA_CLIENT_ID }} \
          --client-secret=${{ secrets.GWA_CLIENT_SECRET }}
          gwa config set gateway $GW

          gwa apply -i gw-config.yaml

          # If you are preparing configuration in the Kong-based format,
          # (`services: ...`), run the following command instead:
          # gwa pg gw-config.yaml
```

### Split configuration by environment

Gateway configuration can be split by environment within the same Gateway using
qualifier tags (e.g. `ns.<gatewayId>.dev`, `ns.<gatewayId>.prod`, etc.), which
will be shown here. Alternatively, you can split the configuration by publishing
to separate Gateways for each environment.

The example below shows how to split the configuration by environment using
branch-based deployment, where the `dev` branch is used to publish the
configuration to the `dev` Gateway and the `main` branch is used to publish the
configuration to the `prod` Gateway.

Sample folder structure:

```text
Add a `.gwa` folder with subfolders for each environment.

.gwa
├── dev
│   └── gw-config.yaml # tag Gateway Services with ns.<gatewayId>.dev
└── prod
    └── gw-config.yaml # tag Gateway Services with ns.<gatewayId>.prod
```

Sample Github workflow for branch-based deployment:

```yaml
name: Publish Gateway Configuration

on:
  push:
    branches: [ dev, main ]

jobs:
  publish:
    runs-on: ubuntu-latest
    env:
      GW: <gatewayId> # replace with your gateway ID
    steps:
      - uses: actions/checkout@v6

      - name: Get GWA Command Line
        run: |
          GWA_CLI_VERSION=v3.0.6
          curl -L -O https://github.com/bcgov/gwa-cli/releases/download/${GWA_CLI_VERSION}/gwa_Linux_x86_64.tgz
          tar -xf gwa_Linux_x86_64.tgz

      - name: Apply Dev Gateway Configuration
        if: github.ref == 'refs/heads/dev'
        run: |
          export PATH=`pwd`:$PATH
          cd .gwa/dev
          gwa login \
            --client-id=${{ secrets.GWA_CLIENT_ID }} \
            --client-secret=${{ secrets.GWA_CLIENT_SECRET }}
          gwa config set gateway $GW
          gwa apply -i gw-config.yaml
          # gwa pg gw-config.yaml

      - name: Apply Prod Gateway Configuration
        if: github.ref == 'refs/heads/main'
        run: |
          export PATH=`pwd`:$PATH
          cd .gwa/prod
          gwa login \
            --client-id=${{ secrets.GWA_CLIENT_ID }} \
            --client-secret=${{ secrets.GWA_CLIENT_SECRET }}
          gwa config set gateway $GW
          gwa apply -i gw-config.yaml
          # gwa pg gw-config.yaml
```

<!-- ## Next steps -->