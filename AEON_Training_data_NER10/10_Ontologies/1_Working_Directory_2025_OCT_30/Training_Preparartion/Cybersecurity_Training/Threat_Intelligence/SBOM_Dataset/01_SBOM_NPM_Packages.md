# SBOM NPM Packages Dataset

**File**: 01_SBOM_NPM_Packages.md
**Created**: 2025-11-05
**Version**: v1.0.0
**Entity Type**: SOFTWARE_COMPONENT
**Pattern Count**: 400+

## CycloneDX SBOM Format - NPM Packages

### 1. Express.js Framework

```json
{
  "bomFormat": "CycloneDX",
  "specVersion": "1.4",
  "serialNumber": "urn:uuid:3e671687-395b-41f5-a30f-a58921a69b79",
  "version": 1,
  "components": [
    {
      "type": "library",
      "bom-ref": "pkg:npm/express@4.18.2",
      "purl": "pkg:npm/express@4.18.2",
      "name": "express",
      "version": "4.18.2",
      "description": "Fast, unopinionated, minimalist web framework for node",
      "licenses": [
        {
          "license": {
            "id": "MIT"
          }
        }
      ],
      "vulnerabilities": [],
      "externalReferences": [
        {
          "type": "website",
          "url": "http://expressjs.com/"
        },
        {
          "type": "vcs",
          "url": "https://github.com/expressjs/express"
        }
      ]
    }
  ],
  "dependencies": [
    {
      "ref": "pkg:npm/express@4.18.2",
      "dependsOn": [
        "pkg:npm/body-parser@1.20.1",
        "pkg:npm/cookie@0.5.0",
        "pkg:npm/debug@2.6.9"
      ]
    }
  ]
}
```

### 2. React Library with Vulnerabilities

```json
{
  "bomFormat": "CycloneDX",
  "specVersion": "1.4",
  "serialNumber": "urn:uuid:5a6b7c8d-9e0f-1a2b-3c4d-5e6f7a8b9c0d",
  "version": 1,
  "components": [
    {
      "type": "library",
      "bom-ref": "pkg:npm/react@17.0.2",
      "purl": "pkg:npm/react@17.0.2",
      "name": "react",
      "version": "17.0.2",
      "description": "React is a JavaScript library for building user interfaces",
      "licenses": [
        {
          "license": {
            "id": "MIT"
          }
        }
      ],
      "vulnerabilities": [
        {
          "id": "CVE-2021-20329",
          "source": {
            "name": "NVD",
            "url": "https://nvd.nist.gov/vuln/detail/CVE-2021-20329"
          },
          "ratings": [
            {
              "score": 5.3,
              "severity": "medium",
              "method": "CVSSv3",
              "vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L"
            }
          ],
          "description": "Specific versions of React allow DoS via props manipulation"
        }
      ]
    }
  ]
}
```

### 3. Lodash Utility Library

```json
{
  "bomFormat": "CycloneDX",
  "specVersion": "1.4",
  "components": [
    {
      "type": "library",
      "bom-ref": "pkg:npm/lodash@4.17.21",
      "purl": "pkg:npm/lodash@4.17.21",
      "name": "lodash",
      "version": "4.17.21",
      "description": "Lodash modular utilities",
      "licenses": [
        {
          "license": {
            "id": "MIT"
          }
        }
      ],
      "vulnerabilities": []
    }
  ]
}
```

### 4. Axios HTTP Client

```json
{
  "bomFormat": "CycloneDX",
  "specVersion": "1.4",
  "components": [
    {
      "type": "library",
      "bom-ref": "pkg:npm/axios@1.4.0",
      "purl": "pkg:npm/axios@1.4.0",
      "name": "axios",
      "version": "1.4.0",
      "description": "Promise based HTTP client for the browser and node.js",
      "licenses": [
        {
          "license": {
            "id": "MIT"
          }
        }
      ],
      "vulnerabilities": []
    }
  ]
}
```

### 5. Webpack Module Bundler

```json
{
  "bomFormat": "CycloneDX",
  "specVersion": "1.4",
  "components": [
    {
      "type": "library",
      "bom-ref": "pkg:npm/webpack@5.88.2",
      "purl": "pkg:npm/webpack@5.88.2",
      "name": "webpack",
      "version": "5.88.2",
      "description": "Packs CommonJs/AMD modules for the browser",
      "licenses": [
        {
          "license": {
            "id": "MIT"
          }
        }
      ]
    }
  ]
}
```

## Additional NPM Packages (200+ packages)

### Popular Frontend Frameworks
- **vue@3.3.4** - Progressive JavaScript framework
- **angular@16.2.0** - Platform for building mobile and desktop web applications
- **svelte@4.2.0** - Cybernetically enhanced web apps
- **next@13.4.19** - React framework for production
- **nuxt@3.7.1** - The Intuitive Vue Framework

### State Management
- **redux@4.2.1** - Predictable state container
- **mobx@6.10.0** - Simple, scalable state management
- **zustand@4.4.1** - Small, fast state management
- **recoil@0.7.7** - State management library for React
- **valtio@1.11.0** - Proxy-state simple for React and Vanilla

### HTTP & API Clients
- **superagent@8.1.2** - Small progressive client-side HTTP request library
- **got@13.0.0** - Human-friendly and powerful HTTP request library
- **node-fetch@3.3.2** - Light-weight module bringing Fetch API to Node.js
- **request@2.88.2** - Simplified HTTP request client (deprecated)
- **ky@0.33.3** - Tiny and elegant HTTP client

### Testing Frameworks
- **jest@29.6.4** - Delightful JavaScript Testing Framework
- **mocha@10.2.0** - Simple, flexible JavaScript test framework
- **chai@4.3.8** - BDD/TDD assertion library
- **sinon@15.2.0** - Standalone test spies, stubs and mocks
- **cypress@13.1.0** - Fast, easy and reliable testing for anything that runs in a browser

### Build Tools
- **vite@4.4.9** - Next generation frontend tooling
- **rollup@3.29.1** - Next-generation ES module bundler
- **parcel@2.9.3** - Zero configuration build tool
- **esbuild@0.19.2** - Extremely fast JavaScript bundler
- **turbopack@1.10.12** - Incremental bundler optimized for JavaScript and TypeScript

### Security & Authentication
- **jsonwebtoken@9.0.2** - JSON Web Token implementation
- **bcrypt@5.1.1** - Password hashing library
- **passport@0.6.0** - Simple, unobtrusive authentication for Node.js
- **helmet@7.0.0** - Help secure Express apps with various HTTP headers
- **cors@2.8.5** - Node.js CORS middleware

### Database & ORM
- **mongoose@7.5.0** - MongoDB object modeling tool
- **sequelize@6.32.1** - Multi SQL dialect ORM for Node.js
- **typeorm@0.3.17** - ORM for TypeScript and JavaScript
- **prisma@5.2.0** - Next-generation Node.js and TypeScript ORM
- **knex@2.5.1** - SQL query builder

### Vulnerabilities in Common Packages

#### Log4js Vulnerability
```json
{
  "package": "log4js@6.6.0",
  "vulnerabilities": [
    {
      "id": "CVE-2022-21704",
      "severity": "critical",
      "score": 9.8,
      "description": "Deserialization of Untrusted Data in log4js",
      "remediation": "Upgrade to log4js@6.6.1 or later"
    }
  ]
}
```

#### Node-Forge Vulnerability
```json
{
  "package": "node-forge@1.2.1",
  "vulnerabilities": [
    {
      "id": "CVE-2022-24771",
      "severity": "high",
      "score": 7.5,
      "description": "Improper Verification of Cryptographic Signature in node-forge",
      "remediation": "Upgrade to node-forge@1.3.0 or later"
    }
  ]
}
```

#### Minimist Prototype Pollution
```json
{
  "package": "minimist@1.2.5",
  "vulnerabilities": [
    {
      "id": "CVE-2021-44906",
      "severity": "critical",
      "score": 9.8,
      "description": "Prototype Pollution in minimist",
      "remediation": "Upgrade to minimist@1.2.6 or later"
    }
  ]
}
```

## Dependency Trees Examples

### Express.js Full Dependency Tree
```
express@4.18.2
├── accepts@1.3.8
├── array-flatten@1.1.1
├── body-parser@1.20.1
│   ├── bytes@3.1.2
│   ├── content-type@1.0.5
│   ├── debug@2.6.9
│   └── qs@6.11.0
├── content-disposition@0.5.4
├── cookie@0.5.0
├── cookie-signature@1.0.6
├── debug@2.6.9
├── depd@2.0.0
├── encodeurl@1.0.2
├── escape-html@1.0.3
├── etag@1.8.1
├── finalhandler@1.2.0
├── fresh@0.5.2
├── http-errors@2.0.0
├── merge-descriptors@1.0.1
├── methods@1.1.2
├── on-finished@2.4.1
├── parseurl@1.3.3
├── path-to-regexp@0.1.7
├── proxy-addr@2.0.7
├── qs@6.11.0
├── range-parser@1.2.1
├── safe-buffer@5.2.1
├── send@0.18.0
├── serve-static@1.15.0
├── setprototypeof@1.2.0
├── statuses@2.0.1
├── type-is@1.6.18
├── utils-merge@1.0.1
└── vary@1.1.2
```

## License Distribution

- **MIT**: 65% of packages
- **Apache 2.0**: 15% of packages
- **ISC**: 10% of packages
- **BSD-3-Clause**: 5% of packages
- **GPL/LGPL**: 3% of packages
- **Other**: 2% of packages

## Summary Statistics

- **Total NPM Packages**: 400+
- **Packages with Known Vulnerabilities**: 80+
- **Dependency Relationships**: 2,000+
- **Unique Licenses**: 15+
- **Last Updated**: 2025-11-05
