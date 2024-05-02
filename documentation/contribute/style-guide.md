---
title: Documentation Style Guide
---

<!-- overview -->
This page gives writing style guidelines for API Program Services documentation.
These are guidelines, not rules. Use your best judgment, and feel free to
propose changes to this document in a pull request.

This document is modified from the Kubernetes Documentation Style Guide. © 2024
The Kubernetes Authors CC BY 4.0. For topics not covered in this style guide
defer to the [Kubernetes documentation styles guides](https://kubernetes.io/docs/contribute/style/).

<!-- body -->

!!! Note
    API Program Services documentation uses [mkdocs](https://www.mkdocs.org/)
    and the [mkdocs-techdocs-core plugin](https://github.com/backstage/mkdocs-techdocs-core).
    The [Material for mkdocs framework](https://squidfunk.github.io/mkdocs-material/reference/)
    appears to be the best reference for Markdown syntax for the current deployment.

## General formatting standards

### Use upper camel case for API objects

When you refer to an API object, use
[UpperCamelCase](https://en.wikipedia.org/wiki/Camel_case), also known as
Pascal case. Write the API object name as a single word.

| Do | Don't |
| -- | ----- |
| Then, publish the DraftDataset. | Then, publish the draft dataset. |
| Products bundle one or more GatewayServices. | `products` bundle one or more gateway `services`. |

!!! info
    This one is tricky! If `code style` seems like a better option to you, open
    a PR and we can revisit this standard.

### Use bold for user interface elements

Use bold for clickable actions or to highlight items in a UI.

| Do | Don't |
| -- | ----- |
| Click **Service Accounts**, then click **New Service Account**. | Click `Service Accounts`, then click `New Service Account`. |
| Go to the **Authorization** tab. | Go to the Authorization tab. |

### Use italics to define or introduce new terms

This guideline applies to introductory or overview content, most likely to be
found in Tutorial and Explanation pages. Follow this alongside using UpperCamelCase.

| Do | Don't |
| -- | ----- |
| *Products* bundle one or more GatewayServices. | "Products" bundle one or more GatewayServices. |
| Namespaces must be associated with an *Organization*. | Namespaces must be associated with an **Organization**. |

### Use code style (`monospace`) for filenames, directories, and paths

| Do | Don't |
| -- | ----- |
| Open the `gw-config.yaml` file. | Open the "gw-config.yaml" file. |
| Go to the `/docs/tutorials` directory. | Go to the /docs/tutorials directory. |

### Use code style for object field names and values

| Do | Don't |
| -- | ----- |
| Set the value of the `host` field in the configuration file. | Set the value of the "host" field in the configuration file. |
| Change the value of `minute` to `30000`. | Change the value of "minute" to "30000". |

!!! info
    This one is also tricky! It looks like Kong service configurations often
    include string field values in quotes. Using code style makes it more clear
    where these quotes are required.

    If normal text seems like a better option to you for field values,open a PR.

### Use code style for gwa command line tool

| Do | Don't |
| -- | ----- |
| `gwa` handles authenticating to the API server. | Gwa handles authenticating to the API server. |

## Code formatting

### Use code style for inline code and commands

For inline code in a Markdown document, use the backtick (`` ` ``).
In an HTML document, use the `<code>` tag.

| Do | Don't |
| -- | ----- |
| Login with the `gwa login` command. | Login with the "gwa login" command. |

### Use code blocks for multi-line code and commands

Enclose multi-line code samples with triple backticks (\`\`\`).

DevHub supports syntax highlighting for code samples. Specifying a language is
optional and can be included after the first set of backticks, for example, ````yaml`.

Add titles for code blocks using `title=<custom title>` after the backticks, for
example, ````yaml title="Product YAML Template"`.

```yaml title="Product YAML Template"
kind: Product
name: Useful API
...
```

### Don't include the command prompt

| Do | Don't |
| -- | ----- |
| `gwa get datasets` | `$ gwa get datasets` |

### Separate commands from output

For example:

Retrieve a table of Datasets in your Namespace:

```shell linenums="0"
gwa get datasets
```

The output is similar to this:

```console
Name                 Title
useful-api-dataset   Useful API
another-api-dataset  Another API
```

### Turn off line numbers for single-line code blocks

Code blocks can be helpful to offset single line commands and provide easy
access to a **Copy to Clipboard** button. Turn off line numbers to improve
readability, or use inline code formatting. Stay consistent within a document.

```md
Code block without line numbers:

    ```shell linenums="0"
    gwa login --client-id <YOUR_CLIENT_ID> --client-secret <YOUR_CLIENT_SECRET>
    ```
```

Code block without line numbers:

```shell linenums="0"
gwa login --client-id <YOUR_CLIENT_ID> --client-secret <YOUR_CLIENT_SECRET>
```

### Command line syntax

| Notation | Description | Example use |
| -------- | ----------- | ----------- |
| `Text without brackets or braces` | Items you must type as shown. | `gwa namespace list` |
| `<Text inside angle brackets>` | Placeholder for which you must supply a value. | `gwa get <resource>` |
| `[Text inside square brackets]` | Optional items. | `gwa status [flags]` |
| `{Text inside braces}` | Set of required items. You must choose one. | `gwa config get {api_key\|host\|namespace}` |
| Vertical bar (`\|`) | Separator for mutually exclusive items. You must choose one. | `gwa config get {api_key\|host\|namespace}` |
| Ellipsis (`...`) | Items that can be repeated and used multiple times. | `gwa publish-gateway <filename...>` |

### Use angle brackets for placeholders

Use angle brackets as a placeholder for variables you want the user to enter.
Use meaningful variable names for the context.

| Do | Don't |
| -- | ----- |
| `gwa apply --input <gateway-config.yaml>` | `gwa apply --input [file]` |
| `tags: [ ns.<namespace> ]` | `tags: [ _NS_ ]` |
| `gwa get <resource>` | `gwa get <foo>` |
| `curl https://<MYSERVICE>.api.gov.bc.ca/headers` | `curl https://*MYSERVICE*.api.gov.bc.ca/headers` |

## Markdown elements

### Callouts

Use callouts to highlight important information users need to know.
Do not use quote formatting (`> Your text`) to achieve the same outcome.

There are many available [callout types](https://squidfunk.github.io/mkdocs-material/reference/admonitions/#supported-types),
of which these three should be used: note,  warning, and danger.

Add callouts using `!!! <type> ["Custom callout title"]` and indenting any
content to contain in the callout, for example:

```md
!!! warning "Don't forget"
    You **must** do this. You *may* include markdown here.
```

!!! warning "Don't forget"
    You **must** do this. You *may* include markdown here.

**Usage guidelines:**

!!! note
    Notes provide useful information or reminders for the user, but the
    information is not required to follow. Notes may not be relevant or necessary
    to every user.

!!! warning
    Warnings are potentially dangerous actions that a user should heed before
    continuing with a task. They are often non-optional steps.

!!! danger
    Danger notices are dangerous actions that a user should exercise extreme
    caution before performing. They often involve the potential for data loss
    or other destructive actions.

### Details

Use collapsible details blocks to include longer notes which may be useful but
are not required information for all users.

```md
??? optional-class "Summary"
    Write the callout type (default is `info`), then a title/summary in quotes,
    then more content in here.

???+ warning "Summary"
    Expand details blocks by default with `???+`.
```

??? optional-type "Summary"
    Write the callout type (default is `info`), then a title/summary in quotes,
    then more content in here.

???+ warning "Summary"
    Expand details by default with a `+`.

### Tabs

Use tabs for documenting multiple user paths to achieve the same end, for example,
using the CLI or Portal UI.

```md
=== "Tab 1"
    Add Markdown **content**.

    Write multiple paragraphs.

=== "Tab 2"
    More Markdown **content**.

    - list item a
    - list item b
```

=== "Tab 1"
    Add Markdown **content**.

    Write multiple paragraphs.

=== "Tab 2"
    More Markdown **content**.

    - list item a
    - list item b

=== "Tab 3"
    ```
    kind: DraftDataset
    name: my-draft-dataset
    title: Useful API
    ```

### Line breaks

Use a single empty newline to separate block-level content like headings, lists,
images, code blocks, and others.

Manually wrap long lines by adding breaks in the Markdown source.
Since git generates file diffs on a line-by-line basis, manually wrapping long lines
helps reviewers to easily find the changes made in a PR and provide feedback.

Rather than doing this manually, find an extension like
[Rewrap](https://marketplace.visualstudio.com/items?itemName=stkb.rewrap){:data-proofer-ignore} for
Visual Studio Code (shortcut `ALT + Q`).

### Headings and titles {#headings}

People accessing this documentation may use a screen reader or other assistive technology.
[Screen readers](https://en.wikipedia.org/wiki/Screen_reader) are linear output devices,
outputting items on a page one at a time. If there is a lot of content on a page,
you can use headings to give the page an internal structure. A good page structure
helps all readers to easily navigate the page or filter topics of interest.

| Do | Don't |
| -- | ----- |
| Use ordered headings (level 2 and 3) to provide a meaningful high-level outline of your content. | Use headings level 4 through 6, unless it is absolutely necessary. If your content is that detailed, it may need to be broken into separate articles. |
| Use sentence case for headings in the page body. For example, "Use the access approval process." | Use title case for headings in the page body. For example, "Use the Access Approval Process." |
| Use title case for the page title in the front matter. For example, `title: Client Credential Protection`. | Use sentence case for page titles. For example, don't use `title: Client credential protection`. |
| If necessary, provide a shortened page title in the front matter. Specify the title to display on the page as a level one heading (`# Full Title`). | Specify page titles in `mkdocs.yml`. |

### Horizontal rules

| Do | Don't |
| -- | ----- |
| Use three hyphens (`---`) to create a horizontal rule. Use horizontal rules for meaningful breaks within paragraph content. For example, a shift of topic within a section. | Use horizontal rules in addition to headings or for decoration. |

### Links

Write links using `[link text](URL)`. 

Write hyperlinks that give you context for the content they link to - avoid "click here."

| Do | Don't |
| -- | ----- |
| The [Swagger Console](https://openapi.apps.gov.bc.ca/?url=https://gwa-api-gov-bc-ca.test.api.gov.bc.ca/docs/v2/openapi.yaml) can be used to test API endpoints. | The Swagger Console can be used to test API endpoints. Try it out [here](https://openapi.apps.gov.bc.ca/?url=https://gwa-api-gov-bc-ca.test.api.gov.bc.ca/docs/v2/openapi.yaml). |

Use root-relative links to support documents moving around without breaking links.

| Do | Don't |
| -- | ----- |
| `[Tutorial](/tutorials/quick-start.md)` (even if linking from another page in `/tutorials`) | `[Tutorial](quick-start.md)` or `[Tutorial](../quick-start.md)` |

### Lists

- End each item in a list with a period if one or more items in the list are
  complete sentences.
- For the sake of consistency, normally either all items or none should be
  complete sentences.

  !!! note
      Ordered lists that are part of an incomplete introductory sentence can be
      in lowercase and punctuated as if each item was a part of the introductory
      sentence. For example:

      Fruits I enjoy include:
        
      - apples
      - pears
      - persimmons.

- Use the number one (`1.`) for all items in ordered lists.
- Use (`+`), (`*`), or (`-`) for unordered lists.

### Diagrams

Use Mermaid to create diagrams by tagging a code block with the `mermaid` language tag. See the [Kubernetes Diagram Guide](https://kubernetes.io/docs/contribute/style/diagram-guide/) more information on creating diagrams with Mermaid (and don't forget about GenAI).

!!! Note
	Mermaid diagrams won't show when using the [devhub-techdocs-publish](https://github.com/bcgov/devhub-techdocs-publish/blob/main/docs/index.md#how-to-use-the-docker-image-to-preview-content-locally) to preview the documentation locally. 
    They will show up when published to DevHub's preview or production sites.

````
```mermaid
  graph TD;
      A-->B;
      A-->C;
      B-->D;
      C-->D;
```
````

```mermaid
  graph TD;
      A-->B;
      A-->C;
      B-->D;
      C-->D;
```

## Content best practices

This section contains suggested best practices for clear, concise, and consistent
content.

### Use present tense

| Do | Don't |
| -- | ----- |
| This command checks status. | This command will check status. |

Exception: Use future or past tense if it is required to convey the correct
meaning.

### Use active voice

To help identify uses of the passive voice, you can try [Hemingway Editor](https://hemingwayapp.com/).

| Do | Don't |
| -- | ----- |
| You can explore the API using a browser. | The API can be explored using a browser. |
| The YAML file specifies the route. | The route is specified in the YAML file. |

Exception: Use passive voice if active voice leads to an awkward construction.

### Use simple and direct language

Use simple and direct language. Avoid using unnecessary phrases, such as saying "please."

| Do | Don't |
| -- | ----- |
| To create a Product, ... | In order to create a Product, ... |
| See the configuration file. | Please see the configuration file. |
| View the Consumer. | With this next command, we'll view the Consumer. |

### Address the reader as "you"

| Do | Don't |
| -- | ----- |
| You can create a Dataset by ... | We'll create a Dataset by ... |
| In the preceding output, you can see... | In the preceding output, one can see ... |

## Patterns to avoid

### Avoid Latin abbreviations

Prefer English terms over Latin abbreviations.

| Do | Don't |
| -- | ----- |
| For example, ... | e.g., ... |
| That is, ...| i.e., ... |

Exception: Use "etc." for et cetera.

### Avoid ambiguous pronouns

Avoid using "we." Using "we" in a sentence can be confusing, because the reader
might not know whether they're part of the "we" you're describing.

Be mindful when using "it" to ensure the there is no confusion about the noun
being referenced. When in doubt, reuse the noun.

| Do | Don't |
| -- | ----- |
| Version 1.4 includes ... | In version 1.4, we have added ...|
| This page teaches you how to create a Product. | In this page, we are going to learn about Products. |
| The popup will display options... | It will display options... |

### Avoid jargon and idioms

Some readers speak English as a second language. Avoid jargon and idioms to help
them understand better.

| Do | Don't |
| -- | ----- |
| Internally, ... | Under the hood, ... |
| Create a new Service. | Spin up a new Service. |

### Avoid statements about the future

Avoid making promises or giving hints about the future. If you need to talk about
an alpha feature, put the text under a heading that identifies it as alpha
information.

An exception to this rule is documentation about announced deprecations
targeting removal in future versions.

### Avoid statements that will soon be out of date

Avoid words like "currently" and "new." A feature that is new today might not be
considered new in a few months.

| Do | Don't |
| -- | ----- |
| In version 1.4, ... | In the current version, ... |
| The Federation feature provides ... | The new Federation feature provides ... |

### Avoid words that assume a specific level of understanding

Avoid words such as "just", "simply", "easy", "easily", or "simple". These words
do not add value.

| Do | Don't |
| -- | ----- |
| You can remove ... | You can easily remove ... |
| These steps ... | These simple steps ... |
