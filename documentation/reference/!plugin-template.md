---
title: {Plugin Name}
---
<!-- template preamble -->

## Template preamble (remove!)

Reference articles concisely present information as a structured set of entries,
with little to no procedural or instructional content. They are like the
nutritional information on a food package.

Alongside other one-off reference page types, we will have a collection of Kong
plugin reference pages.

To write a new plugin reference page, copy this file. All text in {curly
brackets} should be replaced or removed.

---

<!-- overview -->

{A sentence or two introducing the plugin and its core functionality.
Draw from the [Kong Hub](https://docs.konghq.com/hub/) plugin pages' Overview section.}

The {plugin name} plugin lets you {what the plugin is used for}.

<!-- config-reference -->

## Configuration reference

{No need to duplicate the docs from Kong for stock plugins!}

This is a stock plugin from Kong Hub. See the [configuration reference
page](https://docs.konghq.com/hub/kong-inc/{plugin-name}/{kong-version}/configuration/)
for a list of parameters and protocol compatibility notes.

{For custom plugins, we should list the parameters}

This is a custom plugin managed by the API Program Services team.

Here is a list of all the parameters which can be used in this plugin's `config` section:

- **parameter**
  
  {datatype} | {required} | {default: `default_value`} | {additional constraints, e.g. between, len_min} | {Must be one of: `option1`, `option2`}
  
  Description: {A sentence or two describing the field. If applicable, describe value options.}

<!-- examples -->

## Common usage example

The {plugin name} plugin can be used in order to {specific desired outcome}.

To {short description of desired outcome}, add this section to your
GatewayService YAML configuration file:

```yaml
plugins:
- name: rate-limiting
  service: <SERVICE_NAME>
  config:
    second: 5
    hour: 10000
    policy: local
```

Replace <SERVICE_NAME> with the name of the service that this plugin
configuration will target.

### {Optional: Another use case}

The {plugin name} plugin can be used in order to {specific desired outcome}.

{...}

## {Special consideration}

{Optional: Some plugins have special considerations which we may want to
highlight and give guidance around different use cases.}

{For example, for the Rate Limiting plugin, the [Strategies](https://docs.konghq.com/hub/kong-inc/rate-limiting/#strategies) should be mentioned.}