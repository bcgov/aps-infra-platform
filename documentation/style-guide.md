<!-- copied whole hog from https://github.com/kubernetes/website/blob/main/content/en/docs/contribute/style/style-guide.md -->
<!-- needs to be pared down -->

<!-- overview -->
This page gives writing style guidelines for the API Program Services documentation.
These are guidelines, not rules. Use your best judgment, and feel free to
propose changes to this document in a pull request.

<!-- body -->

!!! Note
    API Program Services documentation uses [mkdocs](https://www.mkdocs.org/) and the [mkdocs-techdocs-core plugin](https://github.com/backstage/mkdocs-techdocs-core). The [Material for mkdocs framework](https://squidfunk.github.io/mkdocs-material/reference/) appears to be the best reference for Markdown syntax for the current deployment.

## Documentation formatting standards

### Use upper camel case for API objects

When you refer to an API object, use
[UpperCamelCase](https://en.wikipedia.org/wiki/Camel_case), also known as
Pascal case. 

| Do | Don't |
| -- | -----|
| Then, publish the DraftDataset. | Then, publish the draft dataset. |
| Products bundle one or more GatewayServices. | `products` bundle one or more gateway `services`. |

!!! question
    This one is tricky! If `code style` seems like a better option to you, we could revisit this standard.

### Use bold for user interface elements
Use bold for clickable actions or to highlight items in a UI.

| Do | Don't |
| -- | -----|
| Click **Service Accounts**, then click **New Service Account**. | Click `Service Accounts`, then click `New Service Account`. |
| Go to the **Authorization** tab. | Go to the Authorization tab. |

### Use italics to define or introduce new terms

This guideline applies to introductory or overview content, most likely to be found in Tutorial and Explanation pages. Follow this alongside using UpperCamelCase.

| Do | Don't |
| -- | -----|
| *Products* bundle one or more GatewayServices. | "Products" bundle one or more GatewayServices. |
| Namespaces must be associated with an *Organization*. | Namespaces must be associated with an **Organization**. |

### Use code style (`monospace`) for filenames, directories, and paths

| Do | Don't |
| -- | -----|
| Open the `gw-config.yaml` file. | Open the `gw-config.yaml` file. |
| Go to the `/docs/tutorials` directory. | Go to the /docs/tutorials directory. |

## Code formatting

### Use code style for inline code and commands

For inline code in an HTML document, use the `<code>` tag. In a Markdown
document, use the backtick (`` ` ``).

| Do | Don't |
| -- | -----|
| Login with the `gwa login` command. | Login with the "gwa login" command. |



### Code sni
| Enclose code samples with triple backticks. (\`\`\`)| Enclose code samples with any other syntax. |

| Use meaningful variable names that have a context. | Use variable names such as 'foo','bar', and 'baz' that are not meaningful and lack context. |

| 

{{< table caption = "Do and Don't - Use code style for inline code, commands, and API objects" >}}
Do | Don't
:--| :-----
The `kubectl run` command creates a `Pod`. | The "kubectl run" command creates a pod.
The kubelet on each node acquires a `Lease`… | The kubelet on each node acquires a lease…
A `PersistentVolume` represents durable storage… | A Persistent Volume represents durable storage…
For declarative management, use `kubectl apply`. | For declarative management, use "kubectl apply".
Enclose code samples with triple backticks. (\`\`\`)| Enclose code samples with any other syntax.
Use single backticks to enclose inline code. For example, `var example = true`. | Use two asterisks (`**`) or an underscore (`_`) to enclose inline code. For example, **var example = true**.
Use triple backticks before and after a multi-line block of code for fenced code blocks. | Use multi-line blocks of code to create diagrams, flowcharts, or other illustrations.
Use meaningful variable names that have a context. | Use variable names such as 'foo','bar', and 'baz' that are not meaningful and lack context.
Remove trailing spaces in the code. | Add trailing spaces in the code, where these are important, because the screen reader will read out the spaces as well.
{{< /table >}}

!!! note
    DevHub supports syntax highlighting for code samples, though specifying a language is optional. 

### Use angle brackets for placeholders

Use angle brackets as a placeholder for variables you want the user to enter (except in URLs, where you should use curly braces for placeholders). Use meaningful variable names for the context.

| Do | Don't |
| -- | -----|
| `gwa apply --input <gateway-config.yaml>` | `gwa apply --input [file]` 
| tags: [ <namespace> ] | tags: [ _NS_ ] |

### Use square brackets for optional arguments
Place optional arguments in square brackets (and thus show mandatory arguments without brackets). Parameters for optional 


### Use code style for object field names and namespaces

{{< table caption = "Do and Don't - Use code style for object field names" >}}
Do | Don't
:--| :-----
Set the value of the `replicas` field in the configuration file. | Set the value of the "replicas" field in the configuration file.
The value of the `exec` field is an ExecAction object. | The value of the "exec" field is an ExecAction object.
Run the process as a DaemonSet in the `kube-system` namespace. | Run the process as a DaemonSet in the kube-system namespace.
{{< /table >}}

### Use code style for Kubernetes command tool and component names

{{< table caption = "Do and Don't - Use code style for Kubernetes command tool and component names" >}}
Do | Don't
:--| :-----
The `kubelet` preserves node stability. | The kubelet preserves node stability.
The `kubectl` handles locating and authenticating to the API server. | The kubectl handles locating and authenticating to the apiserver.
Run the process with the certificate, `kube-apiserver --client-ca-file=FILENAME`. | Run the process with the certificate, kube-apiserver --client-ca-file=FILENAME. |
{{< /table >}}

### Starting a sentence with a component tool or component name

{{< table caption = "Do and Don't - Starting a sentence with a component tool or component name" >}}
Do | Don't
:--| :-----
The `kubeadm` tool bootstraps and provisions machines in a cluster. | `kubeadm` tool bootstraps and provisions machines in a cluster.
The kube-scheduler is the default scheduler for Kubernetes. | kube-scheduler is the default scheduler for Kubernetes.
{{< /table >}}

### Use a general descriptor over a component name

{{< table caption = "Do and Don't - Use a general descriptor over a component name" >}}
Do | Don't
:--| :-----
The Kubernetes API server offers an OpenAPI spec. | The apiserver offers an OpenAPI spec.
Aggregated APIs are subordinate API servers. | Aggregated APIs are subordinate APIServers.
{{< /table >}}

### Use normal style for string and integer field values

For field values of type string or integer, use normal style without quotation marks.

{{< table caption = "Do and Don't - Use normal style for string and integer field values" >}}
Do | Don't
:--| :-----
Set the value of `imagePullPolicy` to Always. | Set the value of `imagePullPolicy` to "Always".
Set the value of `image` to nginx:1.16. | Set the value of `image` to `nginx:1.16`.
Set the value of the `replicas` field to 2. | Set the value of the `replicas` field to `2`.
{{< /table >}}

## Referring to Kubernetes API resources

This section talks about how we reference API resources in the documentation.

### Clarification about "resource"

Kubernetes uses the word "resource" to refer to API resources, such as `pod`,
`deployment`, and so on. We also use "resource" to talk about CPU and memory
requests and limits. Always refer to API resources as "API resources" to avoid
confusion with CPU and memory resources.

### When to use Kubernetes API terminologies

The different Kubernetes API terminologies are:

- Resource type: the name used in the API URL (such as `pods`, `namespaces`)
- Resource: a single instance of a resource type (such as `pod`, `secret`)
- Object: a resource that serves as a "record of intent". An object is a desired
  state for a specific part of your cluster, which the Kubernetes control plane tries to maintain.

Always use "resource" or "object" when referring to an API resource in docs.
For example, use "a `Secret` object" over just "a `Secret`".

### API resource names

Always format API resource names using [UpperCamelCase](https://en.wikipedia.org/wiki/Camel_case),
also known as PascalCase, and code formatting.

For inline code in an HTML document, use the `<code>` tag. In a Markdown document, use the backtick (`` ` ``).

Don't split an API object name into separate words. For example, use `PodTemplateList`, not Pod Template List.

For more information about PascalCase and code formatting, please review the related guidance on
[Use upper camel case for API objects](/docs/contribute/style/style-guide/#use-upper-camel-case-for-api-objects)
and [Use code style for inline code, commands, and API objects](/docs/contribute/style/style-guide/#code-style-inline-code).

For more information about Kubernetes API terminologies, please review the related
guidance on [Kubernetes API terminology](/docs/reference/using-api/api-concepts/#standard-api-terminology).

## Code snippet formatting

### Don't include the command prompt

{{< table caption = "Do and Don't - Don't include the command prompt" >}}
Do | Don't
:--| :-----
kubectl get pods | $ kubectl get pods
{{< /table >}}

### Separate commands from output

Verify that the pod is running on your chosen node:

```shell
kubectl get pods --output=wide
```

The output is similar to this:

```console
NAME     READY     STATUS    RESTARTS   AGE    IP           NODE
nginx    1/1       Running   0          13s    10.200.0.4   worker0
```

### Versioning Kubernetes examples

Code examples and configuration examples that include version information should
be consistent with the accompanying text.

If the information is version specific, the Kubernetes version needs to be defined
in the `prerequisites` section of the [Task template](/docs/contribute/style/page-content-types/#task)
or the [Tutorial template](/docs/contribute/style/page-content-types/#tutorial).
Once the page is saved, the `prerequisites` section is shown as **Before you begin**.

To specify the Kubernetes version for a task or tutorial page, include
`min-kubernetes-server-version` in the front matter of the page.

If the example YAML is in a standalone file, find and review the topics that include it as a reference.
Verify that any topics using the standalone YAML have the appropriate version information defined.
If a stand-alone YAML file is not referenced from any topics, consider deleting it instead of updating it.

For example, if you are writing a tutorial that is relevant to Kubernetes version 1.8,
the front-matter of your markdown file should look something like:

```yaml
---
title: <your tutorial title here>
min-kubernetes-server-version: v1.8
---
```

In code and configuration examples, do not include comments about alternative versions.
Be careful to not include incorrect statements in your examples as comments, such as:

```yaml
apiVersion: v1 # earlier versions use...
kind: Pod
...
```

## Kubernetes.io word list

A list of Kubernetes-specific terms and words to be used consistently across the site.

{{< table caption = "Kubernetes.io word list" >}}
Term | Usage
:--- | :----
Kubernetes | Kubernetes should always be capitalized.
Docker | Docker should always be capitalized.
SIG Docs | SIG Docs rather than SIG-DOCS or other variations.
On-premises | On-premises or On-prem rather than On-premise or other variations.
{{< /table >}}

## Shortcodes

Hugo [Shortcodes](https://gohugo.io/content-management/shortcodes) help create
different rhetorical appeal levels. Our documentation supports three different
shortcodes in this category: **Note** `{{</* note */>}}`,
**Caution** `{{</* caution */>}}`, and **Warning** `{{</* warning */>}}`.

1. Surround the text with an opening and closing shortcode.

2. Use the following syntax to apply a style:

   ```none
   {{</* note */>}}
   No need to include a prefix; the shortcode automatically provides one. (Note:, Caution:, etc.)
   {{</* /note */>}}
   ```

   The output is:

   {{< note >}}
   The prefix you choose is the same text for the tag.
   {{< /note >}}

### Note

Use `{{</* note */>}}` to highlight a tip or a piece of information that may be helpful to know.

For example:

```
{{</* note */>}}
You can _still_ use Markdown inside these callouts.
{{</* /note */>}}
```

The output is:

{{< note >}}
You can _still_ use Markdown inside these callouts.
{{< /note >}}

You can use a `{{</* note */>}}` in a list:

```
1. Use the note shortcode in a list

1. A second item with an embedded note

   {{</* note */>}}
   Warning, Caution, and Note shortcodes, embedded in lists, need to be indented four spaces. See [Common Shortcode Issues](#common-shortcode-issues).
   {{</* /note */>}}

1. A third item in a list

1. A fourth item in a list
```

The output is:

1. Use the note shortcode in a list

1. A second item with an embedded note

    {{< note >}}
    Warning, Caution, and Note shortcodes, embedded in lists, need to be indented four spaces. See [Common Shortcode Issues](#common-shortcode-issues).
    {{< /note >}}

1. A third item in a list

1. A fourth item in a list

### Caution

Use `{{</* caution */>}}` to call attention to an important piece of information to avoid pitfalls.

For example:

```
{{</* caution */>}}
The callout style only applies to the line directly above the tag.
{{</* /caution */>}}
```

The output is:

{{< caution >}}
The callout style only applies to the line directly above the tag.
{{< /caution >}}

### Warning

Use `{{</* warning */>}}` to indicate danger or a piece of information that is crucial to follow.

For example:

```
{{</* warning */>}}
Beware.
{{</* /warning */>}}
```

The output is:

{{< warning >}}
Beware.
{{< /warning >}}

## Markdown elements

### Tabs

=== "Tab 1"
    Markdown **content**.

    Multiple paragraphs.

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

```
=== "Tab 1"
    Markdown **content**.

    Multiple paragraphs.

=== "Tab 2"
    More Markdown **content**.

    - list item a
    - list item b
```

### Blocks

!!! warning
    Beware!

```
!!! warning
    Beware!
```

!!! info "Info with custom name"
    Take note, you can modify title for a block by specifying it in quotes after the class.

```
!!! info "Info with custom name"
    Take note, you can modify title for a block by specifying it in quotes after the class.
```

!!! note
    Seriously, take a note.

```
!!! note
    Seriously, take a note.
```

### Details (pop-out)
??? optional-class "Summary"
    Write the class, then a title/summary in quotes, then more content in here.

???+ warning "Summary"
    Expand details by default with a `+`.

```
??? optional-class "Summary"
    Write the class, then a title/summary in quotes, then more content in here.

???+ warning "Summary"
    Expand details by default with a `+`.
```

### Line breaks

Use a single newline to separate block-level content like headings, lists, images,
code blocks, and others. The exception is second-level headings, where it should
be two newlines. Second-level headings follow the first-level (or the title) without
any preceding paragraphs or texts. A two line spacing helps visualize the overall
structure of content in a code editor better.

Manually wrap paragraphs in the Markdown source when appropriate. Since the git
tool and the GitHub website generate file diffs on a line-by-line basis,
manually wrapping long lines helps the reviewers to easily find out the changes
made in a PR and provide feedback. It also helps the downstream localization
teams where people track the upstream changes on a per-line basis.  Line
wrapping can happen at the end of a sentence or a punctuation character, for
example. One exception to this is that a Markdown link or a shortcode is
expected to be in a single line.

### Headings and titles {#headings}

People accessing this documentation may use a screen reader or other assistive technology (AT).
[Screen readers](https://en.wikipedia.org/wiki/Screen_reader) are linear output devices,
they output items on a page one at a time. If there is a lot of content on a page, you can
use headings to give the page an internal structure. A good page structure helps all readers
to easily navigate the page or filter topics of interest.

| Do | Don't |
| -- | ----- |
| Use ordered headings (level 2 and 3) to provide a meaningful high-level outline of your content. | Use headings level 4 through 6, unless it is absolutely necessary. If your content is that detailed, it may need to be broken into separate articles. |
| Use sentence case for headings in the page body. For example, "Use the access approval process." | Use title case for headings in the page body. For example, "Use the Access Approval Process." |
| Use title case for the page title in the front matter. For example, `title: Client Credential Protection`. | Use sentence case for page titles in the front matter. For example, don't use `title: Client credential protection`.

### Paragraphs

| Do | Don't |
| -- | ----- |
| Try to keep paragraphs under 6 sentences. | Indent the first paragraph with space characters. For example, ⋅⋅⋅Three spaces before a paragraph will indent it. |
| Use three hyphens (`---`) to create a horizontal rule. Use horizontal rules for breaks in paragraph content. For example, a change of scene in a story, or a shift of topic within a section. | Use horizontal rules for decoration. |

All API Directory functionality is accessible in both the `test` and `production` environments. While you are encouraged to utilize the `test` environment for experimentation and training purposes, if you already know the details of the API you're building, you can add it directly to the production Directory.
All API Directory functionality is accessible in both the `test` and `production` environments. While you are encouraged to utilize the `test` environment for experimentation and training purposes, if you already know the details of the API you're building, you can add it directly to the production Directory.
All API Directory functionality is accessible in both the `test` and `production` environments. While you are encouraged to utilize the `test` environment for experimentation and training purposes, if you already know the details of the API you're building, you can add it directly to the production Directory.

---

All API Directory functionality is accessible in both the `test` and `production` environments. While you are encouraged to utilize the `test` environment for experimentation and training purposes, if you already know the details of the API you're building, you can add it directly to the production Directory.


### Links

{{< table caption = "Do and Don't - Links" >}}
Do | Don't
:--| :-----
Write hyperlinks that give you context for the content they link to. For example: Certain ports are open on your machines. See <a href="#check-required-ports">Check required ports</a> for more details. | Use ambiguous terms such as "click here". For example: Certain ports are open on your machines. See <a href="#check-required-ports">here</a> for more details.
Write Markdown-style links: `[link text](URL)`. For example: `[Hugo shortcodes](/docs/contribute/style/hugo-shortcodes/#table-captions)` and the output is [Hugo shortcodes](/docs/contribute/style/hugo-shortcodes/#table-captions). | Write HTML-style links: `<a href="/media/examples/link-element-example.css" target="_blank">Visit our tutorial!</a>`, or create links that open in new tabs or windows. For example: `[example website](https://example.com){target="_blank"}`
{{< /table >}}

### Lists

Group items in a list that are related to each other and need to appear in a specific
order or to indicate a correlation between multiple items. When a screen reader comes
across a list—whether it is an ordered or unordered list—it will be announced to the
user that there is a group of list items. The user can then use the arrow keys to move
up and down between the various items in the list. Website navigation links can also be
marked up as list items; after all they are nothing but a group of related links.

- End each item in a list with a period if one or more items in the list are complete
  sentences. For the sake of consistency, normally either all items or none should be complete sentences.

  {{< note >}}
  Ordered lists that are part of an incomplete introductory sentence can be in lowercase
  and punctuated as if each item was a part of the introductory sentence.
  {{< /note >}}

- Use the number one (`1.`) for ordered lists.

- Use (`+`), (`*`), or (`-`) for unordered lists.

- Leave a blank line after each list.

- Indent nested lists with four spaces (for example, ⋅⋅⋅⋅).

- List items may consist of multiple paragraphs. Each subsequent paragraph in a list
  item must be indented by either four spaces or one tab.

## Content best practices

This section contains suggested best practices for clear, concise, and consistent content.

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

Avoid using "we." Using "we" in a sentence can be confusing, because the reader might not know
whether they're part of the "we" you're describing.

Be mindful when using "it" to ensure the there is no confusion about the noun being referenced. When in doubt, reuse the noun.

| Do | Don't |
| -- | ----- |
| Version 1.4 includes ... | In version 1.4, we have added ...|
| This page teaches you how to create a Product. | In this page, we are going to learn about Products. |
| The popup will display options... | It will display options... |

### Avoid jargon and idioms

Some readers speak English as a second language. Avoid jargon and idioms to help them understand better.

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

Avoid words like "currently" and "new." A feature that is new today might not be considered new in a few months.

| Do | Don't |
| -- | ----- |
| In version 1.4, ... | In the current version, ... |
| The Federation feature provides ... | The new Federation feature provides ... |

### Avoid words that assume a specific level of understanding

Avoid words such as "just", "simply", "easy", "easily", or "simple". These words do not add value.

| Do | Don't |
| -- | ----- |
| You can remove ... | You can easily remove ... |
| These steps ... | These simple steps ... |

## {{% heading "whatsnext" %}}

* Learn about [writing a new topic](/docs/contribute/style/write-new-topic/).
* Learn about [using page templates](/docs/contribute/style/page-content-types/).
* Learn about [custom hugo shortcodes](/docs/contribute/style/hugo-shortcodes/).
* Learn about [creating a pull request](/docs/contribute/new-content/open-a-pr/).

This document is modified from the Kubernetes Documentation Style Guide. © 2024 The Kubernetes Authors CC BY 4.0.