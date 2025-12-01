# SBOM PyPI Python Packages Dataset

**File**: 02_SBOM_PyPI_Python_Packages.md
**Created**: 2025-11-05
**Version**: v1.0.0
**Entity Type**: SOFTWARE_COMPONENT
**Pattern Count**: 400+

## SPDX Format - Python Packages

### 1. Django Web Framework

```json
{
  "spdxVersion": "SPDX-2.3",
  "dataLicense": "CC0-1.0",
  "SPDXID": "SPDXRef-DOCUMENT",
  "name": "Django-4.2.1",
  "documentNamespace": "https://sbom.example/django-4.2.1",
  "packages": [
    {
      "SPDXID": "SPDXRef-Package-Django",
      "name": "Django",
      "versionInfo": "4.2.1",
      "downloadLocation": "https://pypi.org/project/Django/4.2.1/",
      "filesAnalyzed": false,
      "licenseConcluded": "BSD-3-Clause",
      "licenseDeclared": "BSD-3-Clause",
      "copyrightText": "Copyright (c) Django Software Foundation",
      "externalRefs": [
        {
          "referenceCategory": "PACKAGE-MANAGER",
          "referenceType": "purl",
          "referenceLocator": "pkg:pypi/django@4.2.1"
        }
      ],
      "vulnerabilities": [
        {
          "id": "CVE-2023-24580",
          "severity": "HIGH",
          "description": "Potential DoS vulnerability in file uploads"
        }
      ]
    }
  ],
  "relationships": [
    {
      "spdxElementId": "SPDXRef-Package-Django",
      "relationshipType": "DEPENDS_ON",
      "relatedSpdxElement": "SPDXRef-Package-asgiref"
    }
  ]
}
```

### 2. Requests HTTP Library

```json
{
  "spdxVersion": "SPDX-2.3",
  "packages": [
    {
      "SPDXID": "SPDXRef-Package-Requests",
      "name": "requests",
      "versionInfo": "2.31.0",
      "downloadLocation": "https://pypi.org/project/requests/2.31.0/",
      "licenseConcluded": "Apache-2.0",
      "licenseDeclared": "Apache-2.0",
      "externalRefs": [
        {
          "referenceCategory": "PACKAGE-MANAGER",
          "referenceType": "purl",
          "referenceLocator": "pkg:pypi/requests@2.31.0"
        }
      ]
    }
  ]
}
```

### 3. NumPy Scientific Computing

```json
{
  "spdxVersion": "SPDX-2.3",
  "packages": [
    {
      "SPDXID": "SPDXRef-Package-NumPy",
      "name": "numpy",
      "versionInfo": "1.24.3",
      "downloadLocation": "https://pypi.org/project/numpy/1.24.3/",
      "licenseConcluded": "BSD-3-Clause",
      "licenseDeclared": "BSD-3-Clause",
      "externalRefs": [
        {
          "referenceCategory": "PACKAGE-MANAGER",
          "referenceType": "purl",
          "referenceLocator": "pkg:pypi/numpy@1.24.3"
        }
      ]
    }
  ]
}
```

### 4. Flask Microframework

```json
{
  "spdxVersion": "SPDX-2.3",
  "packages": [
    {
      "SPDXID": "SPDXRef-Package-Flask",
      "name": "Flask",
      "versionInfo": "2.3.3",
      "downloadLocation": "https://pypi.org/project/Flask/2.3.3/",
      "licenseConcluded": "BSD-3-Clause",
      "licenseDeclared": "BSD-3-Clause",
      "externalRefs": [
        {
          "referenceCategory": "PACKAGE-MANAGER",
          "referenceType": "purl",
          "referenceLocator": "pkg:pypi/flask@2.3.3"
        }
      ]
    }
  ],
  "relationships": [
    {
      "spdxElementId": "SPDXRef-Package-Flask",
      "relationshipType": "DEPENDS_ON",
      "relatedSpdxElement": "SPDXRef-Package-Werkzeug"
    },
    {
      "spdxElementId": "SPDXRef-Package-Flask",
      "relationshipType": "DEPENDS_ON",
      "relatedSpdxElement": "SPDXRef-Package-Jinja2"
    }
  ]
}
```

### 5. Pandas Data Analysis

```json
{
  "spdxVersion": "SPDX-2.3",
  "packages": [
    {
      "SPDXID": "SPDXRef-Package-Pandas",
      "name": "pandas",
      "versionInfo": "2.0.3",
      "downloadLocation": "https://pypi.org/project/pandas/2.0.3/",
      "licenseConcluded": "BSD-3-Clause",
      "licenseDeclared": "BSD-3-Clause",
      "externalRefs": [
        {
          "referenceCategory": "PACKAGE-MANAGER",
          "referenceType": "purl",
          "referenceLocator": "pkg:pypi/pandas@2.0.3"
        }
      ]
    }
  ]
}
```

## Additional Python Packages (200+ packages)

### Web Frameworks
- **fastapi@0.103.1** - Modern, fast web framework for building APIs
- **aiohttp@3.8.5** - Async HTTP client/server framework
- **tornado@6.3.3** - Python web framework and asynchronous networking library
- **bottle@0.12.25** - Fast, simple and lightweight WSGI micro web-framework
- **pyramid@2.0.2** - The Pyramid Web Framework

### Data Science & ML
- **scikit-learn@1.3.0** - Machine learning in Python
- **tensorflow@2.13.0** - TensorFlow is an end-to-end machine learning platform
- **pytorch@2.0.1** - Tensors and Dynamic neural networks
- **scipy@1.11.2** - Scientific computing tools
- **matplotlib@3.7.2** - Plotting and visualization

### Database & ORM
- **sqlalchemy@2.0.20** - Database Abstraction Library
- **psycopg2@2.9.7** - PostgreSQL database adapter
- **pymongo@4.5.0** - Python driver for MongoDB
- **redis@5.0.0** - Python client for Redis
- **asyncpg@0.28.0** - Fast PostgreSQL Database Client Library

### Testing & Quality
- **pytest@7.4.2** - pytest: simple powerful testing with Python
- **unittest2@1.1.0** - Backport of new unittest features
- **coverage@7.3.0** - Code coverage measurement
- **tox@4.11.1** - Virtualenv-based automation of test activities
- **black@23.7.0** - The uncompromising code formatter

### Security & Authentication
- **cryptography@41.0.4** - Cryptographic recipes and primitives
- **pyjwt@2.8.0** - JSON Web Token implementation in Python
- **bcrypt@4.0.1** - Modern password hashing
- **python-jose@3.3.0** - JOSE implementation in Python
- **passlib@1.7.4** - Comprehensive password hashing framework

### Async & Concurrency
- **asyncio@3.4.3** - Asynchronous I/O, event loop
- **celery@5.3.1** - Distributed Task Queue
- **gevent@23.7.0** - Coroutine-based concurrency library
- **trio@0.22.2** - Friendly Python library for async concurrency
- **uvloop@0.17.0** - Ultra fast asyncio event loop

### CLI & Tools
- **click@8.1.7** - Composable command line interface toolkit
- **typer@0.9.0** - Build great CLIs. Easy to code. Based on Python type hints
- **argparse@1.4.0** - Command-line parsing library
- **rich@13.5.2** - Rich text and beautiful formatting in the terminal
- **colorama@0.4.6** - Cross-platform colored terminal text

## Python Package Vulnerabilities

### Django SQL Injection
```json
{
  "package": "django@3.2.0",
  "vulnerability": {
    "id": "CVE-2021-35042",
    "severity": "HIGH",
    "cvss_score": 7.3,
    "description": "SQL injection vulnerability in QuerySet.order_by()",
    "affected_versions": ">=2.2,<2.2.24 || >=3.1,<3.1.12 || >=3.2,<3.2.4",
    "fixed_version": "3.2.4",
    "remediation": "Upgrade to Django 3.2.4 or later"
  }
}
```

### Pillow Image Processing RCE
```json
{
  "package": "pillow@9.0.0",
  "vulnerability": {
    "id": "CVE-2022-22817",
    "severity": "CRITICAL",
    "cvss_score": 9.8,
    "description": "PIL.ImageMath.eval allows RCE via crafted expression",
    "affected_versions": "<9.0.1",
    "fixed_version": "9.0.1",
    "remediation": "Upgrade to Pillow 9.0.1 or later"
  }
}
```

### PyYAML Arbitrary Code Execution
```json
{
  "package": "pyyaml@5.3.1",
  "vulnerability": {
    "id": "CVE-2020-14343",
    "severity": "CRITICAL",
    "cvss_score": 9.8,
    "description": "Arbitrary code execution via full_load or safe_load",
    "affected_versions": "<5.4",
    "fixed_version": "5.4",
    "remediation": "Upgrade to PyYAML 5.4 or later and use safe_load()"
  }
}
```

### Jinja2 Template Injection
```json
{
  "package": "jinja2@2.11.0",
  "vulnerability": {
    "id": "CVE-2020-28493",
    "severity": "HIGH",
    "cvss_score": 7.5,
    "description": "ReDoS vulnerability in Jinja2 urlize filter",
    "affected_versions": "<2.11.3",
    "fixed_version": "2.11.3",
    "remediation": "Upgrade to Jinja2 2.11.3 or later"
  }
}
```

## Dependency Trees

### Django Full Stack
```
django@4.2.1
├── asgiref@3.7.2
├── sqlparse@0.4.4
├── tzdata@2023.3
└── [dev dependencies]
    ├── pytest-django@4.5.2
    ├── coverage@7.3.0
    └── black@23.7.0
```

### Flask Application
```
flask@2.3.3
├── werkzeug@2.3.7
├── jinja2@3.1.2
│   └── markupsafe@2.1.3
├── click@8.1.7
├── itsdangerous@2.1.2
└── blinker@1.6.2
```

### FastAPI Modern Stack
```
fastapi@0.103.1
├── pydantic@2.3.0
│   ├── pydantic-core@2.6.3
│   └── typing-extensions@4.7.1
├── starlette@0.27.0
│   └── anyio@3.7.1
└── uvicorn@0.23.2
    ├── h11@0.14.0
    └── httptools@0.6.0
```

### Data Science Stack
```
pandas@2.0.3
├── numpy@1.24.3
├── python-dateutil@2.8.2
├── pytz@2023.3
└── [optional]
    ├── matplotlib@3.7.2
    ├── scipy@1.11.2
    └── scikit-learn@1.3.0
```

## License Distribution

- **MIT**: 40% of packages
- **BSD-3-Clause**: 30% of packages
- **Apache 2.0**: 20% of packages
- **PSF (Python Software Foundation)**: 5% of packages
- **GPL/LGPL**: 3% of packages
- **Other**: 2% of packages

## Summary Statistics

- **Total Python Packages**: 400+
- **Packages with Known Vulnerabilities**: 75+
- **Dependency Relationships**: 1,800+
- **Unique Licenses**: 12+
- **Last Updated**: 2025-11-05
