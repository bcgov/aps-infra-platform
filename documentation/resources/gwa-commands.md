# GWA CLI Commands

GWA CLI helps manage gateway resources in a declarative fashion.

## apply

**Usage:** `gwa apply [flags]`

Apply your GatewayService, CredentialIssuer, DraftDataset, and Product resources.  Use the `generate-config` command to see examples of these resources.

**Flags**

| Flag | Description |
| ----- | ------ |
| `-i, --input string` | YAML file containing your configuration (default "gw-config.yml") |


**Examples**

```shell
$ gwa apply --input gw-config.yaml
```


## config

**Usage:** `gwa config`

Configuration commands


### config.get

**Usage:** `gwa config get [key]`

This is a convenience getter to print out the currently stored global setting for the following arguments  
  
- api_key  
- host  
- namespace  



### config.set

**Usage:** `gwa config set [key] [value] [flags]`

Exposes some specific config values that can be defined by the user.  
  
Configurable Settings:  
  namespace:       The default namespace used  
  token:           Use only if you have a token you know is authenticated  
  host:            The API host you wish to communicate with  
  scheme:          http or https  
  
    

**Flags**

| Flag | Description |
| ----- | ------ |
| `--host string` | set the host |
| `--namespace string` | set the namespace |
| `--scheme string` | set the scheme |
| `--token string` | set the namespace |


**Examples**

```shell
$ gwa config set namespace ns-sampler
$ gwa config set --namespace ns-sampler
```


## generate-config

**Usage:** `gwa generate-config [flags]`

Generate gateway resources based on pre-defined templates

**Flags**

| Flag | Description |
| ----- | ------ |
| `--org string` | Set the organization (default "ministry-of-citizens-services") |
| `--org-unit string` | Set the organization unit (default "databc") |
| `-o, --out string` | The file to output the generate config to (default "gw-config.yml") |
| `-s, --service string` | A unique service subdomain for your vanity url: https://<service>.api.gov.bc.ca |
| `-t, --template string` | Name of a pre-defined template (kong-httpbin, client-credentials-shared-idp) |
| `-u, --upstream string` | The upstream implementation of the API |


**Examples**

```shell
$ gwa generate-config --template kong-httpbin \
    --service my-service \
	--upstream https://httpbin.org

$ gwa generate-config --template client-credentials-shared-idp \
    --service my-service \
	--upstream https://httpbin.org
```


## get

**Usage:** `gwa get [type] <flags> [flags]`

Get gateway resources.  Retrieve a table of datasets, issuers, organizations, org-units or products.

**Flags**

| Flag | Description |
| ----- | ------ |
| `--json` | Return output as JSON |
| `--org string` | Organization to filter results by |
| `--yaml` | Return output as YAML |


**Examples**

```shell
$ gwa get datasets
$ gwa get datasets --json
$ gwa get datasets --yaml
```


## init

> _Command 'init' is deprecated.  .env files are no longer used, see config command_


## login

**Usage:** `gwa login [flags]`

You can login via device login or by using client credentials.

**Flags**

| Flag | Description |
| ----- | ------ |
| `--client-id string` | Your gateway's client ID |
| `--client-secret string` | Your gateway's client secret |


**Examples**

```shell
$ gwa login
$ gwa login --client-id <YOUR_CLIENT_ID> --client-secret <YOUR_CLIENT_SECRET>
```


## namespace

**Usage:** `gwa namespace`

Namespaces are used to organize your services.


### namespace.create

**Usage:** `gwa namespace create [flags]`

Create a new namespace

**Flags**

| Flag | Description |
| ----- | ------ |
| `-d, --description string` | optionally add a description |
| `-g, --generate` | generates a random, unique namespace |
| `-n, --name string` | optionally define your own namespace |


**Examples**

```shell
$ gwa namespace create --generate
$ gwa namespace create --name my-namespace --description="This is my namespace"
```


### namespace.current

**Usage:** `gwa namespace current`

Display the current namespace


### namespace.destroy

**Usage:** `gwa namespace destroy [flags]`

Destroy the current namespace

**Flags**

| Flag | Description |
| ----- | ------ |
| `--force` | force deletion |



### namespace.list

**Usage:** `gwa namespace list`

List all your managed namespaces


## publish

> _Command 'publish' is deprecated.  Use apply instead._


## publish-gateway

**Usage:** `gwa publish-gateway [inputs...] [flags]`

Once you have a gateway configuration file ready to publish, you can run the following command to reflect your changes in the gateway:  
  
  $ gwa pg sample.yaml  
  
If you want to see the expected changes but not actually apply them, you can run:  
  
  $ gwa pg --dry-run sample.yaml  
  
inputs accepts a wide variety of formats, for example:  
  
  1. Empty, which means find all the possible YAML files in the current directory and publish them  
  2. A space-separated list of specific YAML files in the current directory, or  
  3. A directory relative to the current directory  


**Flags**

| Flag | Description |
| ----- | ------ |
| `--dry-run` | Dry run your API changes before committing to them |
| `--qualifier string` | Sets a tag qualifier, which specifies that the gateway configuration is a partial set of configuration |


**Examples**

```shell
$ gwa publish-gateway
$ gwa publish-gateway path/to/config1.yaml other-path/to/config2.yaml
$ gwa publish-gateway path/to/directory/containing-configs/
$ gwa publish-gateway path/to/config.yaml --dry-run
$ gwa publish-gateway path/to/config.yaml --qualifier dev
```


## status

**Usage:** `gwa status [flags]`

Check the status of your services configured on the Kong gateway

**Flags**

| Flag | Description |
| ----- | ------ |
| `--json` | Output status as a JSON string |


**Examples**

```shell
$ gwa status
$ gwa status --json
```


