[sbom]]
[[cybersecurity]]
[[jim]]
[]


[[Syft]]
- CLI tool designed for generating SBOMs from container images and filesystems
- Integrates well with Grype for vulnerability scanning
- Open-source tool with Apache-2.0 license
- Specifically built for container and filesystem analysis[
- https://github.com/anchore/syft


[[CyclonedX SBOM Utilty]]
- Functions as an API platform for validating and analyzing BOMs
- Supports multiple BOM formats including CycloneDX and SPDX
- Offers powerful query capabilities for component analysis
- Includes reporting features with various output formats (txt, csv, md, json)[    
- (https://github.com/CycloneDX/sbom-utility)


[[Grype]]


[[Fossa]]

- Requires API key configuration and authentication setup
- Multiple installation methods available through scripts
- Requires additional environment variable configuration
- More complex initial configuration for enterprise features[

	https://github.com/fossas/fossa-cli/blob/master/README.md

[[Trivy]]


### [Fossa]]
https://github.com/fossas/fossa-cli/blob/master/README.md

`fossa-cli` is a zero-configuration polyglot dependency analysis tool. You can point fossa CLI at any codebase or build, and it will automatically detect dependencies being used by your project.

`fossa-cli` currently supports automatic dependency analysis for [many different build tools and languages](https://github.com/fossas/fossa-cli/blob/master/docs/references/strategies/README.md#supported-languages). It also has limited support for vendored dependency detection, container scanning, and system dependency detection. These features are still a work in progress. Our goal is to make the FOSSA CLI a universal tool for dependency analysis.

`fossa-cli` integrates with [FOSSA](https://fossa.com/) for dependency analysis, license scanning, vulnerability scanning, attribution report generation, and more.

## Installation

[](https://github.com/fossas/fossa-cli/blob/master/README.md#installation)
### Using the install script

[](https://github.com/fossas/fossa-cli/blob/master/README.md#using-the-install-script)

FOSSA CLI provides an install script that downloads the latest release from GitHub Releases for your computer's architecture. You can see the source code and flags at [`install-latest.sh`](https://github.com/fossas/fossa-cli/blob/master/install-latest.sh) for Mac and Linux or [`install-latest.ps1`](https://github.com/fossas/fossa-cli/blob/master/install-latest.ps1) for Windows.

**NOTE:** You may need to add the downloaded executable to your `$PATH`. The installer script will output the installed path of the executable. You can also use `-b` to pick the installation directory when using `install-latest.sh` (see [the `install-latest.sh` source code](https://github.com/fossas/fossa-cli/blob/master/install-latest.sh) for details).

#### macOS or 64-bit Linux

[](https://github.com/fossas/fossa-cli/blob/master/README.md#macos-or-64-bit-linux)

```shell
curl -H 'Cache-Control: no-cache' https://raw.githubusercontent.com/fossas/fossa-cli/master/install-latest.sh | bash
```

> The `FOSSA CLI` version in the brew cask is updated to the latest version every 3 hours.

#### Windows with Powershell

[](https://github.com/fossas/fossa-cli/blob/master/README.md#windows-with-powershell)

```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force; iex  ((New-Object System.Net.WebClient).DownloadString('https://raw.githubusercontent.com/fossas/fossa-cli/master/install-latest.ps1'))
```

Alternatively, install using [Scoop](https://scoop.sh/):

```
scoop install fossa
```

Please refer to detailed walkthrough [Installing FOSSA CLI](https://github.com/fossas/fossa-cli/blob/master/docs/walkthroughs/installing-fossa-cli.md), for installing [FOSSA CLI 1.x](https://github.com/fossas/fossa-cli/blob/master/docs/walkthroughs/installing-fossa-cli.md#installing-cli-1x-using-installation-script) and using [GitHub Releases](https://github.com/fossas/fossa-cli/releases) to install [FOSSA CLI manually](https://github.com/fossas/fossa-cli/blob/master/docs/walkthroughs/installing-fossa-cli.md#installing-manually-with-github-releases).

## Getting Started

[](https://github.com/fossas/fossa-cli/blob/master/README.md#getting-started)

### Integrating your project with FOSSA

[](https://github.com/fossas/fossa-cli/blob/master/README.md#integrating-your-project-with-fossa)

#### TL;DR, Linux, Mac, *nix-like

[](https://github.com/fossas/fossa-cli/blob/master/README.md#tldr-linux-mac-nix-like)

```shell
# Download FOSSA.
curl -H 'Cache-Control: no-cache' https://raw.githubusercontent.com/fossas/fossa-cli/master/install-latest.sh | bash

# Set your API key. Get this from the FOSSA web application.
export FOSSA_API_KEY=XXXX

# Run an analysis in your project's directory.
cd $MY_PROJECT_DIR
fossa analyze
```

#### TL;DR, Windows

[](https://github.com/fossas/fossa-cli/blob/master/README.md#tldr-windows)

```powershell
# Download FOSSA.
Set-ExecutionPolicy Bypass -Scope Process -Force; iex  ((New-Object System.Net.WebClient).DownloadString('https://raw.githubusercontent.com/fossas/fossa-cli/master/install-latest.ps1'))

# Set your API key. Get this from the FOSSA web application.
$env:FOSSA_API_KEY=XXXX

# Run an analysis in your project's directory.
cd $MY_PROJECT_DIR
fossa analyze
```

#### Installing FOSSA CLI

[](https://github.com/fossas/fossa-cli/blob/master/README.md#installing-fossa-cli)

Follow [the installation instructions](https://github.com/fossas/fossa-cli/blob/master/README.md#installation) above to install the FOSSA CLI. Once installed, you should have a new binary named `fossa` available on your `$PATH`.

#### Generating an API key

[](https://github.com/fossas/fossa-cli/blob/master/README.md#generating-an-api-key)

To get started with integrating your project into FOSSA, you'll need to [generate an API key](https://docs.fossa.com/docs/api-reference). You'll get this API key from the FOSSA web application ([app.fossa.com](https://app.fossa.com/)).

Once you have your API key:

```shell
export FOSSA_API_KEY=XXXX # Use your API key here.
```

#### Running an analysis

[](https://github.com/fossas/fossa-cli/blob/master/README.md#running-an-analysis)

Now we can run an analysis. To run an analysis, all you need to do is navigate to your project's directory and run `fossa analyze`.

**NOTE:** While `fossa` will try its best to report available results for any kind of project, you'll get the best results by running in a directory with a working project build. A working build lets us integrate directly with your build tool to identify dependencies, instead of trying to infer dependencies from your source code.

```shell
$ cd $MY_PROJECT_DIR # Use your actual project location here.

$ fossa analyze
[ INFO] Using project name: `https://github.com/fossas/fossa-cli`
[ INFO] Using revision: `09ca72e398bb32747b27c0f43731678fa42c3c26`
[ INFO] Using branch: `No branch (detached HEAD)`
[ INFO] ============================================================

      View FOSSA Report:
      https://app.fossa.com/projects/custom+1%2fgithub.com%2ffossas%2ffossa-cli/refs/branch/master/09ca72e398bb32747b27c0f43731678fa42c3c26

  ============================================================
```

#### Viewing your results

[](https://github.com/fossas/fossa-cli/blob/master/README.md#viewing-your-results)

Once an analysis has been uploaded, you can view your results in the FOSSA web application. You can see your analysis by using the link provided as output by `fossa analyze`, or by navigating to your project and revision in the FOSSA web application.

#### What next?

[](https://github.com/fossas/fossa-cli/blob/master/README.md#what-next)

Now that your analysis is complete, there are a couple things you might want to do after an initial integration:

- **Double-check your results.** Some analysis methods may produce partial or unexpected results depending on what information was available when you ran the analysis. If something seems wrong, [our debugging guide](https://github.com/fossas/fossa-cli/blob/master/docs/references/debugging/README.md) can help you diagnose and debug your integration.
    
- **Scan for issues and generate a compliance report.** Once your analysis is ready, we'll automatically queue an issue scan and report the results in the web application. Once an issue scan is complete, you can also [generate a report](https://docs.fossa.com/docs/running-a-scan) from the web application.
    
- **Set up FOSSA in your CI.** You can also use your issue scan results as inputs to CI scripts. For GitHub repositories, you can use FOSSA's [native GitHub integration](https://docs.fossa.com/docs/automatic-updates#pull-request--commit-statuses-github-only) to report a status check on your PRs. For other CI integrations, you can also [use `fossa test`](https://github.com/fossas/fossa-cli/blob/master/docs/references/subcommands/test.md) to get programmatic issue status in CI.
    

## User Manual

[](https://github.com/fossas/fossa-cli/blob/master/README.md#user-manual)

For most users, the FOSSA CLI will work out-of-the-box without any configuration. Just get an API key, run `fossa analyze`, and view your results in the FOSSA web application.

Users who need advanced customization or features should see the [User Manual](https://github.com/fossas/fossa-cli/blob/master/docs/README.md). Some common topics of interest include:

- [Debugging your integration](https://github.com/fossas/fossa-cli/blob/master/docs/references/debugging/README.md)
- [Specifying vendored dependencies](https://github.com/fossas/fossa-cli/blob/master/docs/features/vendored-dependencies.md)
- [Adding manual dependencies](https://github.com/fossas/fossa-cli/blob/master/docs/features/manual-dependencies.md)
- [Supported languages](https://github.com/fossas/fossa-cli/blob/master/docs/references/strategies/README.md)
