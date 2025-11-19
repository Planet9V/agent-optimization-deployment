# The VulnCheck CLI

> Take VulnCheck anywhere with the VulnCheck CLI

Access VulnCheck intelligence through CLI across MacOS, Linux and Windows platforms. Browse VulnCheck indices, manage backups and access VulnCheck IP Intelligence offline using a terminal.

### How Can I Access VulnCheck CLI?

VulnCheck's CLI is an open source project available on GitHub: [https://github.com/vulncheck-oss/cli](https://github.com/vulncheck-oss/cli)

### Installing the VulnCheck CLI

You can easily install VulnCheck CLI using an install script. Choose the script and method that matches your operating system:

<code-group>

```bash [OSX]
curl -sSL https://raw.githubusercontent.com/vulncheck-oss/cli/main/install.sh | bash
```

```powershell [Windows]
iex ((New-Object System.Net.WebClient).DownloadString('https://raw.githubusercontent.com/vulncheck-oss/cli/main/install.ps1'))
```

</code-group>

More detailed installation instructions are available on [GitHub](https://github.com/vulncheck-oss/cli?tab=readme-ov-file#installation)

### Configuring VulnCheck Access

1. From the terminal authenticate your VulnCheck account by running:

```bash
vulncheck auth login
```

1. Select to Login with a browser or Paste an authentication token to complete authentication
![VulnCheck Authentication](/images/tools/cli/cli-auth.png)

### How do I use VulnCheck CLI?

[VulnCheck Available Commands](https://github.com/vulncheck-oss/cli?tab=readme-ov-file#available-commands)

[Browse/list indices](https://github.com/vulncheck-oss/cli?tab=readme-ov-file#browselist-indices)

[Browse/list an index](https://github.com/vulncheck-oss/cli?tab=readme-ov-file#browselist-an-index)

[Download a backup](https://github.com/vulncheck-oss/cli?tab=readme-ov-file#download-a-backup)

[Request vulnerabilities related to a CPE](https://github.com/vulncheck-oss/cli?tab=readme-ov-file#request-vulnerabilities-related-to-a-cpe)

[Request vulnerabilities related to a PURL](https://github.com/vulncheck-oss/cli?tab=readme-ov-file#request-vulnerabilities-related-to-a-purl)

[Scan a repository for vulnerabilities](https://github.com/vulncheck-oss/cli?tab=readme-ov-file#scan-a-repository-for-vulnerabilities)

### How Can I Contribute to VulnCheck CLI?

Community contributions in the form of [issues](https://github.com/vulncheck-oss/cli/issues/new?template=1_BUG-FORM.yaml) and [features](https://github.com/vulncheck-oss/cli/issues/new?template=2_FEATURE-REQUEST-FORM.yaml) are welcome and can be submitted on [GitHub](https://github.com/vulncheck-oss/cli/blob/main/.github/CONTRIBUTING.md). When submitting issues, please ensure they include sufficient information to reproduce the problem. For new features, provide a reasonable use case, appropriate unit tests, and ensure compliance with required checks in our automated CI/CD pipeline without generating any complaints.
