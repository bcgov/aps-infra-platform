---
title: {Guide Title for a Specific Task}
---
<!-- template preamble -->

A how-to page shows how to do a single thing, typically by giving a short
sequence of steps. How-to pages have minimal explanation, but often provide links
to conceptual topics that provide related background and knowledge.

To write a new how-to page, copy this file. All text in {curly brackets} should be replaced or removed.

For more information on how-to pages, read the [Good Docs Project guide](https://gitlab.com/tgdp/templates/-/blob/main/how-to/guide-how-to.md).

<!-- overview -->

This guide explains how to {insert a brief description of the task}.

{Optional: Specify when and why your user might want to perform the task.}

{Optional: Include links/tooltips to relevant concepts when terms are introduced here or in the `steps` section.}

<!-- prerequisites -->

## Before you begin

{Optional: You should be familiar with how to do a [more basic task](/how-to/basic.md) or [concept](/concepts/topic.md).}

Before you begin, ensure you:

- [Install gwa CLI](/how-to/gwa-install.md)
- [Create a Namespace](/resources/gwa-commands.md#namespacecreate)
- [Complete This](/how-to/do-this.md)
- [Do That](/how-to/do-that.md)

<!-- steps -->

## {Sub-task name}

{Optional: Provide a concise description of the purpose of this sub-task. Only include this if the purpose is not clear from the sub-task title.}

{You can use this format to describe steps to complete a sub-task:}

1. {Write the first step here. Use a verb to start.}

  {Optional: Explanatory text}

  {Optional: Code sample or screenshot that helps your users complete this step.}

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

{Optional: Use example code blocks as needed}

{**TO DISCUSS**: When to use placeholders in example code}

```yaml
services:
  - name: my-service
    host: httpbin.org
    tags: [ns.<NAMESPACE>]
    port: 443
    protocol: https
    retries: 0
    routes:
      - name: my-service-route
        tags: [ns.<NAMESPACE>]
        hosts:
          - <MYSERVICE>.cluster.local
```

### {Sub-task details}

{This section is optional. Only include h3 headings if the sub-task is big and complex and demands splitting.
Consider if the sub-task deserves it's own how-to page.}

<!-- whatsnext -->

## What's next?

- [Natural next thing to do](/how-to/next.md)
- [Related reference material](/reference/api.md)
- [Something else to consider or explore](/how-to/more.md)
- Read more about the [Relevant concept](/concepts/relevant.md)
- 5 items max!
