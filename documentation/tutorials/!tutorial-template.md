---
title: {Tutorial Title}
---
<!-- template preamble -->

Tutorials are learning-oriented and targeted at beginners or experts to help
them learn a skill through hands-on experience. A tutorial page shows how to
accomplish a goal that is larger than a single task, following a single, carefully
managed path from start to finish. Tutorials should assume users have limited
prior experience and thus include surface-level explanations of core concepts, while
linking to related concept pages for deeper explanations.

Tutorials should use the test environment (when applicable).

To write a new tutorial page, copy this file. All text in {curly brackets} should be replaced or removed.

For more information on tutorial pages, read the [Good Docs Project guide](https://gitlab.com/tgdp/templates/-/blob/main/tutorial/guide-tutorial.md).

<!-- overview -->

In this tutorial, you'll learn how to {insert brief description of the main tutorial task}. This tutorial is intended for {audience}.

By the end of this tutorial, you'll be able to:

- Learning objective 1
- Learning objective 2
- Learning objective 3

<!-- background -->

{This section is optional. Feel free to use some of the text below to help you get started.}

- {product} is a {product type} that you can use to {common use case}...
- Using {feature} enables you to {pain point}...

{Optional: Include links/tooltips to relevant concepts when terms are introduced here or in the `steps` section.}

<!-- prerequisites -->

## Before you begin

{Intro tutorials should have no prerequisites, though more advanced tutorials might have some.}

{Optional: You should be familiar with how to do a [more basic task](/how-to/gwa-install.md) or [concept](/concepts/api-directory.md).}

Before you begin, ensure you:

- [Install gwa CLI](/how-to/gwa-install.md)
- [Create a Namespace](/resources/gwa-commands.md#namespacecreate)

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

{Optional: Use example code blocks as needed}

{**TO DISCUSS**: When to use placeholders in example code - see [how-to template](/how-to/!how-to-template.md)}

```yaml
services:
  - name: my-service
    host: httpbin.org
    tags: [ns.<NAMESPACE>]
    routes:
      - name: my-service-route
        tags: [ns.<NAMESPACE>]
        hosts:
          - <MYSERVICE>.cluster.local
```

<!-- summary -->

## Summary

{Use this section to summarize what the user learned in the tutorial.}

In this tutorial, you learned how to:

- Summary point 1
- Summary point 2
- Summary point 3

<!-- whatsnext -->

## What's next?

- [Natural next thing to do](/how-to/gwa-install.md)
- [Something else to consider or explore](/how-to/private-route.md)
- Read more about the [Relevant concept](/concepts/api-directory.md)
- 5 items max!
