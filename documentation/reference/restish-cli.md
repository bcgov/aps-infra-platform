---
title: Restish CLI
---

Restish is a command-line HTTP client designed for working with REST APIs through simple, readable commands. It combines API discovery, authentication, request execution, and response formatting into a single workflow, making it useful for both quick testing and repeatable API operations.

Key capabilities include:

- **OpenAPI-first interaction**: auto-discovers operations from API descriptions.
- **Short, command-style syntax**: invokes endpoints as CLI subcommands instead of manually crafting raw HTTP requests.
- **Built-in auth support**: handles common schemes (including OAuth flows) through API profiles.
- **Configurable API aliases**: stores named API definitions for faster reuse across environments.
- **Structured output options**: prints responses in formats like JSON and YAML for easy piping and scripting.
- **Plugin/extensibility model**: supports additional functionality via extensions.

In practice, Restish works well as a lightweight alternative to GUI API tools when you want terminal-native, script-friendly API access.

## Installation

=== "Linux"

    If you are on Linux, you can install by downloading a compressed archive:

```sh
curl -LO https://github.com/rest-sh/restish/releases/download/v0.21.2/restish-0.21.2-linux-amd64.tar.gz
tar -xf restish-0.21.2-linux-amd64.tar.gz
sudo mv restish /usr/local/bin/.
```

=== "macOS"

    If you are on macoS, you can install by downloading a compressed archive:

```sh
curl -LO https://github.com/rest-sh/restish/releases/download/v0.21.2/restish-0.21.2-darwin-amd64.tar.gz
tar -xf restish-0.21.2-darwin-amd64.tar.gz
sudo mv restish /usr/local/bin/.
```

## Usage with SDX

### Configure the API

Edit the restish config and add the below "sdx" api shortname details.

```sh
restish api edit
```

```json
{
  "$schema": "https://rest.sh/schemas/apis.json",
  "sdx": {
    "base": "https://api-gov-bc-ca-lab.dev.api.gov.bc.ca/ds/api/sdx/v1",
    "profiles": {
      "default": {
        "auth": {
          "name": "oauth-authorization-code",
          "params": {
            "audience": "sdx-bruno-client",
            "authorize_url": "https://authz-apps-gov-bc-ca-lab.dev.api.gov.bc.ca/auth/realms/aps/protocol/openid-connect/auth",
            "client_id": "sdx-bruno-client",
            "scopes": "openid",
            "token_url": "https://authz-apps-gov-bc-ca-lab.dev.api.gov.bc.ca/auth/realms/aps/protocol/openid-connect/token"
          }
        }
      }
    },
    "tls": {}
  }
}
```

### Interacting with the API

```sh
restish sdx

-- listing subsystems from the SDX catalog
restish sdx subsystem-list

-- listing organizations from the SDX catalog
restish sdx organization-list

-- creation example
restish sdx create-subsystem ministry-of-books name: BOOKY, description: "Some booky system"

-- deletion
restish sdx delete-subsystem ministry-of-books BOOKY --force

-- piping will pass without color, only body, default JSON format
restish  sdx organization-list | cat

-- output YAML
restish  sdx organization-list -o yaml
```
