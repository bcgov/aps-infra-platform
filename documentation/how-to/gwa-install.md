---
title: Install gwa CLI
---

<!-- overview -->

The `gwa` command line interface (CLI) is a tool for creating and publishing
Gateway Services and other resources on the API Management Portal.

`gwa` runs from a single executable file for convenient installation.

## Compatibility

The `gwa` command line interface (CLI) is available for Linux, MacOS, and Windows.

However, the commands provided in most of our documentation are for a Unix shell (e.g. `bash`, `zsh`).
If you are running Windows, it is recommended to use [WSL](https://learn.microsoft.com/en-us/windows/wsl/install).

Visit the [release page](https://github.com/bcgov/gwa-cli/releases) for all versions.

## Linux

If you are on Linux, you can install by downloading a compressed archive:

```shell
curl -sL https://github.com/bcgov/gwa-cli/releases/download/v2.0.15/gwa_Linux_x86_64.tgz -o gwa.tar.gz
tar -xf gwa.tar.gz -C /tmp
sudo cp /tmp/gwa /usr/local/bin/
```

## Windows

If you are on Windows, you can install using Command Prompt (CMD) by navigating to
the target installation folder and downloading a compressed archive:

```shell
curl -sL https://github.com/bcgov/gwa-cli/releases/download/v2.0.15/gwa_Windows_x86_64.zip -o gwa.zip
mkdir gwa
tar -xf gwa.zip -C gwa
powershell -command "[Environment]::SetEnvironmentVariable('Path', [Environment]::GetEnvironmentVariable('Path', 'User') + [IO.Path]::PathSeparator + [System.IO.Directory]::GetCurrentDirectory() + '\gwa', 'User')"
```

## Confirm installation

Check `gwa` installed correctly by opening a new command prompt and running:

```shell linenums="0"
gwa --version
```

## Next steps

If you would like to dive deeper with the `gwa` command line interface (CLI), check out the
following resource:

- [gwa Commands](/how-to/gwa-commands.md)

Once you have `gwa` installed, try setting up an API on 
the {{ glossary_tooltip term_id="api-services-portal" text="API Services Portal" }}:

- [API Provider Quick Start](/tutorials/quick-start.md)