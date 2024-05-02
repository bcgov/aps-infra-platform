---
title: {Guide Title for a Specific Task}
---
<!-- template preamble -->

## Template preamble (remove!)

A how-to page shows how to do a single thing, typically by giving a short
sequence of steps. How-to pages have minimal explanation, but often provide links
to conceptual topics that provide related background and knowledge.

How-tos should provide the available environments (`test`/`prod`) and endpoints, when applicable.

To write a new how-to page, copy this file. All text in {curly brackets} should be replaced or removed.

For more information on how-to pages, read the [Good Docs Project guide](https://gitlab.com/tgdp/templates/-/blob/main/how-to/guide-how-to.md).

---

<!-- overview -->

This guide explains how to {insert a brief description of the task}.

{Optional: Specify when and why your user might want to perform the task.}

{Optional: Include links/tooltips to relevant concepts when terms are introduced here or in the `steps` section.}

<!-- prerequisites -->

## Before you begin

{Optional: You should be familiar with how to do a [more basic task](/how-to/gwa-install.md) or [concept](/concepts/api-directory.md).}

Before you begin, ensure you:

- [Install gwa CLI](/how-to/gwa-install.md)
- [Create a Namespace](/resources/gwa-commands.md#namespacecreate)
- [Complete This](/how-to/create-gateway-service.md)
- [Do That](/how-to/generate-service-account.md)

<!-- steps -->

## {Sub-task name}

{Optional: Provide a concise description of the purpose of this sub-task. Only include this if the purpose is not clear from the sub-task title.}

{You can use this format to describe steps to complete a sub-task:}

1. {Write the first step here. Use a verb to start.}

  {Optional: Explanatory text}

  {Optional: Code sample or screenshot that helps your users complete this step.}
  {Re screenshots: Only use an image when it would be significantly harder to explain with text alone. Otherwise, don't.}

  {Optional: The result of completing this step.}

1. {Write the second step here. Use a verb to start.}

  {Substep 1 text}

  {Substep 2 text}

## {Second sub-task name}

{Repeat as above}

{Note on multiple paths: Making users choose between multiple ways of doing this
 is confusing. When it comes to CLI vs UI, the CLI is generally the recommended
 path, so *only* include CLI instructions.}

{Optional: Use tabs for documenting multiple user paths to achieve the same end, for example, using the CLI or Portal UI.}

=== "CLI"
    1. Create a Product configuration using the YAML template.
    2. Publish the Product - `gwa apply -i <product.yaml>`
=== "Web UI"
    1. Navigate to **Namespaces** -> **Products**.
    2. Click **New Product** in the top right.

!!! warning "Don't forget"
    Use callouts to communicate **important** information.

{Optional: Use example code blocks as needed.}

{**TO DISCUSS**: When/how to use `<PLACEHOLDERS>` in example code, in particular in YAML configs}

1. Which elements to use placeholders for? Strike a balance:
  - Use placeholders for elements that users absolutely need to customize for their specific use case or the example will not work.
    - Let's develop some standards on which elements this would include
    - `<NAMESPACE>`
    - `<CLIENT_ID>` and `<CLIENT_SECRET>`
    - ?
  - Use example values (without placeholders) for non-essential configuration
    - How to distinguish these values from the required (non-user chosen) values for a given config?
    - Explain these are example values in comments/accompanying text if there may be any doubt
    - Again, what elements would this include?
    - e.g. in a Service, `host: httpbin.org`

2. How to annotate code blocks?
   - Option A: Use comments inside the code block
   - Option B: Use accompanying descriptive text following the code block (preferred)

3. Conventions for service and route names
   - 

```yaml
services:
  - name: my-service
    host: httpbin.org
    # Replace <NAMESPACE> with the namespace specific to your environment.
    tags: [ns.<NAMESPACE>]
    routes:
      - name: my-service-route
        # Tags should include a namespace identifier, replace <NAMESPACE>.
        tags: [ns.<NAMESPACE>]
        # Replace <MYSERVICE> with your service's desired internal name.
        hosts: 
          - <MYSERVICE>.cluster.local
```

{Replace the following / Where,}:

- `<NAMESPACE>`: Replace with your API Service's Portal Namespace where the service resides, e.g. `gw-e8a5a`.
- `<MYSERVICE>`: Replace this with the name of the service as you would like it to be known within the local network, for example, `api-service`.

### {Sub-task details}

{This section is optional. Only include h3 headings if the sub-task is big and complex and demands splitting.
Consider if the sub-task deserves it's own how-to page.}

<!-- whatsnext -->

## Next steps

- [Natural next thing to do](/how-to/gwa-install.md)
- [Related reference material](/reference/glossary.md)
- [Something else to consider or explore](/how-to/private-route.md)
- Read more about the [Relevant concept](/concepts/api-directory.md)
- 5 items max!
