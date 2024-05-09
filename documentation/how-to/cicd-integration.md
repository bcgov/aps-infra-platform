---
title: "Add to a CI/CD Pipeline"
---

Update your CI/CD pipelines to run the `gwa-cli` to keep your services updated on the gateway.

**Github Actions Example**

In the repository where you maintain your CI/CD Pipeline configuration, use the Service Account details from `Section 2` to set up two `Secrets`:

- GWA_ACCT_ID

- GWA_ACCT_SECRET

Add a `.gwa` folder (can be called anything) that will be used to hold your gateway configuration.

Github Workflow example:

```yaml
env:
  NS: "<your namespace>"

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
        with:
          fetch-depth: 0

      - uses: actions/setup-node@v1
        with:
          node-version: 10
          TOKEN: ${ {secrets.GITHUB_TOKEN} }

      - name: Get GWA Command Line
        run: |

          curl -L https://github.com/bcgov/gwa-cli/releases/download/v2.0.4/gwa_Linux_x86_64.tgz | tar -zxf -
          export PATH=$PATH:$PWD

      - name: Apply Namespace Configuration
        run: |
          export PATH=`pwd`:$PATH
          cd .gwa

          # include only if working in the test/training environment
          gwa config set host api-gov-bc-ca.test.api.gov.bc.ca

          gwa config set namespace $NS
          gwa login \
            --client-id=${ { secrets.GWA_ACCT_ID } } \
            --client-secret=${ { secrets.GWA_ACCT_SECRET } }

          gwa pg gw-config.yaml

          # If you are preparing the configuration in a format
          # compatible with the 'apply' command, then run the
          # following command instead:
          # gwa apply -i gw-config.yaml
```
