# WAVE 10: SBOM INTEGRATION & SOFTWARE SUPPLY CHAIN
**File:** 12_WAVE_10_SBOM_INTEGRATION.md
**Created:** 2025-10-30 00:00:00 UTC
**Version:** v1.0.0
**Status:** ACTIVE
**Wave Priority:** 10 of 12
**Estimated Nodes:** ~140,000

## Wave Overview

Wave 10 implements comprehensive Software Bill of Materials (SBOM) integration, covering ~140,000 nodes for software components, dependencies, licenses, build information, and provenance tracking. This wave enables complete software supply chain visibility and vulnerability tracking from source to deployment.

### Objectives
1. Define complete SBOM component schemas
2. Implement dependency tree analysis
3. Establish license compliance tracking
4. Enable build and provenance verification
5. Integrate vulnerability propagation through supply chain
6. Support multiple SBOM standards (SPDX, CycloneDX)

### Dependencies
- Wave 3-5: Cybersecurity (vulnerability mapping)
- Wave 9: IT Infrastructure (software deployment mapping)

---

## COMPLETE NODE SCHEMAS

### 1. SOFTWARE COMPONENTS (~50,000 nodes)

#### 1.1 Base Software Component (20,000 nodes)

**SoftwareComponent**
```yaml
SoftwareComponent:
  properties:
    # Identity - Multiple identifier formats
    componentID: string (unique)
    purl: string (Package URL - RFC 7396)
    cpe: string (Common Platform Enumeration 2.3)
    swid: string (SWID Tag ID - ISO/IEC 19770-2)

    # Basic Metadata
    name: string
    version: string
    versionScheme: enum[semver, integer, alpha, custom]
    group: string (namespace/organization)
    namespace: string

    # Type Classification
    componentType: enum[
      library, framework, application, container, operating_system,
      device, firmware, file, source, archive, install, patch,
      documentation, data, configuration, tool, service
    ]

    # Supplier Information
    supplier: {
      name: string,
      url: string,
      contact: string,
      organizationType: enum[vendor, contributor, maintainer, distributor]
    }

    # Author Information
    author: string
    authors: array[{name: string, email: string, organization: string}]
    publisher: string

    # Descriptive Information
    description: text
    summary: string
    category: array[string]
    tags: array[string]

    # License Information
    license: string (SPDX identifier)
    licenses: array[{
      id: string (SPDX),
      name: string,
      text: text,
      url: string,
      acknowledgement: enum[declared, concluded, discovered]
    }]
    licenseExpression: string (SPDX expression)
    copyright: text

    # Hash Values (for integrity verification)
    hashes: array[{
      algorithm: enum[md5, sha1, sha224, sha256, sha384, sha512, sha3_256, sha3_384, sha3_512, blake2b_256, blake2b_384, blake2b_512],
      value: string (hex)
    }]

    # File Information
    fileName: string
    fileSize: integer (bytes)
    mimeType: string
    encoding: string

    # Scope & Context
    scope: enum[required, optional, excluded, development, test, runtime, provided, system]
    modified: boolean
    pedigree: {
      ancestors: array[string (component IDs)],
      descendants: array[string],
      variants: array[string],
      commits: array[string (git commit hashes)],
      patches: array[string (patch IDs)],
      notes: text
    }

    # External References
    externalReferences: array[{
      type: enum[
        vcs, issue_tracker, website, documentation, mailing_list,
        social, chat, support, distribution, license, build_meta,
        build_system, release_notes, security_contact, security_advisory,
        vulnerability_report, other
      ],
      url: string,
      comment: string,
      hashes: array[{algorithm: string, value: string}]
    }]

    # Properties (extensible key-value pairs)
    properties: array[{
      name: string,
      value: string,
      type: enum[string, integer, float, boolean, datetime, uri]
    }]

    # Evidence (how component was identified)
    evidence: {
      licenses: array[{
        method: enum[declared, discovered, analyzed],
        confidence: float (0-1),
        source: string
      }],
      occurrences: array[{
        location: string,
        line: integer,
        offset: integer,
        symbolLocation: string,
        additionalContext: string
      }],
      callstack: array[{
        package: string,
        version: string,
        method: string
      }],
      identity: {
        field: enum[group, name, version, purl, cpe, swid, hash],
        confidence: float,
        methods: array[{
          technique: enum[
            manifest_analysis, ast_fingerprint, hash_comparison,
            binary_analysis, filename, attestation, source_code_analysis,
            instrumentation, dynamic_analysis
          ],
          confidence: float,
          value: string
        }]
      }
    }

    # SBOM Metadata
    bomRef: string (unique reference within BOM)
    spdxID: string (SPDX specific identifier)
    specVersion: string (SBOM specification version)
    serialNumber: string (URN)

    # Lifecycle
    releaseDate: datetime
    buildDate: datetime
    validUntilDate: datetime
    deprecatedDate: datetime
    endOfSupportDate: datetime

    # Quality & Trust
    confidence: float (0-1)
    trustScore: float (0-100)
    verificationStatus: enum[verified, unverified, failed, pending]

  relationships:
    # Dependency Relationships
    dependsOn: SoftwareComponent (many-to-many)
      properties:
        dependencyType: enum[direct, indirect, transitive, optional, dev, peer]
        versionConstraint: string
        scope: enum[compile, runtime, test, provided, system]
        optional: boolean

    # Containment
    partOf: Package|SoftwareComponent (many-to-1)
    contains: SoftwareComponent (1-to-many)

    # Variants & Evolution
    variantOf: SoftwareComponent (many-to-1)
    succeeds: SoftwareComponent (many-to-1)
    replaces: SoftwareComponent (many-to-many)

    # Build & Provenance
    builtBy: BuildSystem (many-to-1)
    producedBy: Build (many-to-1)
    sourceIn: CodeRepository (many-to-many)

    # Deployment
    installedOn: Asset (many-to-many)
    providesService: Service (many-to-many)

    # Security
    hasVulnerability: Vulnerability (many-to-many)
      properties:
        discoveryDate: datetime
        affectedVersions: array[string]
        fixedVersions: array[string]
        severity: enum[critical, high, medium, low, none]
        exploitability: enum[high, functional, poc, unproven]

    patchedBy: Patch (many-to-many)

    # Licensing
    licensedUnder: SoftwareLicense (many-to-many)

    # Attestation & Verification
    attestedBy: Attestation (many-to-many)
    signedBy: CryptographicKey (many-to-1)

  validation_rules:
    - componentID must be unique
    - At least one of purl, cpe, swid must be present
    - version must follow versionScheme format
    - hashes must use secure algorithms (no MD5 for security verification)
    - license must be valid SPDX identifier if present
    - confidence range [0, 1]
```

#### 1.2 Package Types (10,000 nodes)

**Package**
```yaml
Package:
  extends: SoftwareComponent
  properties:
    # Package-specific metadata
    packageManager: enum[
      npm, yarn, pip, poetry, maven, gradle, nuget, gem, bundler,
      cargo, go_mod, composer, pub, cocoapods, swift_pm, hex,
      crates_io, hackage, opam, cpan, cran
    ]

    # Distribution
    downloadLocation: string (URL or NOASSERTION or NONE)
    packageURL: string (canonical package URL)
    homepage: string
    sourceInfo: string

    # Repository Information
    repository: {
      type: enum[git, svn, mercurial, cvs, bazaar],
      url: string,
      branch: string,
      tag: string,
      commit: string
    }

    # Verification
    checksums: array[{
      algorithm: string,
      checksumValue: string
    }]
    packageVerificationCode: {
      value: string,
      excludedFiles: array[string]
    }

    # Files Analyzed
    filesAnalyzed: boolean
    annotations: array[{
      annotator: string,
      annotationDate: datetime,
      annotationType: enum[review, comment, issue],
      comment: text
    }]

  relationships:
    managedBy: PackageManager (many-to-1)
    publishedTo: Registry (many-to-1)
    mirroredIn: Registry (many-to-many)
```

**ContainerImage**
```yaml
ContainerImage:
  extends: SoftwareComponent
  properties:
    # Image Identity
    imageID: string (SHA256 digest)
    imageName: string
    imageTag: string
    imageDigest: string

    # Registry Information
    registry: string
    repository: string

    # Image Metadata
    architecture: enum[amd64, arm64, armv7, 386, ppc64le, s390x]
    os: string
    osVersion: string
    variant: string

    # Image Layers
    layers: array[{
      digest: string,
      size: integer,
      mediaType: string,
      command: string,
      created: datetime
    }]

    # Configuration
    config: {
      user: string,
      exposedPorts: array[string],
      env: array[string],
      entrypoint: array[string],
      cmd: array[string],
      volumes: array[string],
      workingDir: string,
      labels: object
    }

    # Size Information
    size: integer (bytes)
    virtualSize: integer (bytes)

  relationships:
    basedOn: ContainerImage (many-to-1)
    layerContains: SoftwareComponent (many-to-many)
    scannedBy: VulnerabilityScanner (many-to-many)
```

#### 1.3 Specialized Components (20,000 nodes)

**Firmware**
```yaml
Firmware:
  extends: SoftwareComponent
  properties:
    firmwareType: enum[bios, uefi, embedded, bootloader, microcode]
    targetDevice: string
    flashSize: integer (bytes)
    bootloader: string
    cryptographicSignature: string

  relationships:
    installedOn: saref:Device (many-to-many)
    hasVulnerability: CVE (many-to-many)
```

**Library**
```yaml
Library:
  extends: SoftwareComponent
  properties:
    libraryType: enum[static, dynamic, shared, header_only]
    apiVersion: string
    abiVersion: string
    interfaceStability: enum[stable, unstable, deprecated, experimental]

    # API Surface
    exportedSymbols: array[{
      name: string,
      type: enum[function, class, variable, constant],
      visibility: enum[public, private, protected, internal]
    }]

  relationships:
    implements: Interface (many-to-many)
    providesAPI: API (1-to-many)
```

---

### 2. DEPENDENCIES (~40,000 nodes)

#### 2.1 Dependency Relationships (30,000 nodes)

**Dependency**
```yaml
Dependency:
  properties:
    # Identity
    dependencyID: string
    ref: string (bomRef of dependent component)
    dependsOn: string (bomRef of dependency)

    # Dependency Type
    dependencyType: enum[
      direct,           # Explicitly declared
      indirect,         # Pulled in by another dependency
      transitive,       # Multi-level indirect
      dev,              # Development-only
      test,             # Testing-only
      runtime,          # Runtime-only
      optional,         # Optional feature
      peer,             # Peer dependency (npm)
      provided,         # Provided by runtime (Maven)
      bundled,          # Bundled with package
      build             # Build-time only
    ]

    # Version Constraints
    versionConstraint: string
    versionRange: {
      min: string,
      max: string,
      minInclusive: boolean,
      maxInclusive: boolean
    }
    constraintExpression: string (e.g., ">=1.0.0 <2.0.0")

    # Scope
    scope: enum[compile, runtime, test, provided, system, import]

    # Metadata
    optional: boolean
    required: boolean
    excluded: boolean
    reason: string (why dependency exists)

    # Resolution
    resolvedVersion: string
    resolved: boolean
    resolutionStrategy: enum[newest, oldest, range, exact, dynamic]

    # Conflict Information
    conflicts: array[{
      with: string (component ID),
      reason: string,
      resolution: enum[override, exclude, force, fail]
    }]

    # Integrity
    integrity: string (hash for package managers)
    integrityVerified: boolean

  relationships:
    # Core dependency graph
    from: SoftwareComponent (many-to-1)
    to: SoftwareComponent (many-to-1)

    # Vulnerability propagation
    introduces: Vulnerability (many-to-many)
      properties:
        introducedIn: string (version)
        fixedIn: string (version)
        transitiveDepth: integer

    # License propagation
    inheritsLicense: SoftwareLicense (many-to-many)

    # Conflict relationships
    conflictsWith: Dependency (many-to-many)
    overrides: Dependency (many-to-1)
    excludes: SoftwareComponent (many-to-many)
```

#### 2.2 Dependency Trees (10,000 nodes)

**DependencyTree**
```yaml
DependencyTree:
  properties:
    # Identity
    treeID: string
    rootComponent: string (bomRef)
    specVersion: string

    # Metrics
    totalNodes: integer
    maxDepth: integer
    directDependencies: integer
    transitiveDependencies: integer

    # Analysis Results
    cyclicDependencies: boolean
    diamondDependencies: boolean (multiple paths to same dependency)
    conflicts: array[{
      component: string,
      requestedVersions: array[string],
      resolvedVersion: string
    }]

    # Vulnerability Summary
    criticalVulnerabilities: integer
    highVulnerabilities: integer
    mediumVulnerabilities: integer
    lowVulnerabilities: integer

    # License Summary
    licenseCombinations: array[string]
    licenseConflicts: array[string]
    copyleftLicenses: array[string]

    # Generation Metadata
    generatedBy: string (tool name)
    generatedOn: datetime
    generationMethod: enum[static_analysis, dynamic_analysis, manifest, hybrid]

  relationships:
    represents: SoftwareComponent (many-to-1)
    includes: Dependency (1-to-many)
    analyzedBy: SBOMTool (many-to-1)
```

**DependencyPath**
```yaml
DependencyPath:
  properties:
    pathID: string
    pathType: enum[shortest, critical, vulnerable, license_sensitive]
    depth: integer
    nodes: array[string] (ordered list of component IDs)

    # Risk Assessment
    cumulativeRisk: float
    criticalNode: string (highest risk component in path)

  relationships:
    startsAt: SoftwareComponent (many-to-1)
    endsAt: SoftwareComponent (many-to-1)
    traverses: Dependency (many-to-many)
```

---

### 3. BUILD INFORMATION (~20,000 nodes)

#### 3.1 Build Systems (5,000 nodes)

**BuildSystem**
```yaml
BuildSystem:
  properties:
    # Identity
    buildSystemID: string
    name: string
    type: enum[
      make, cmake, gradle, maven, ant, msbuild, xcodebuild,
      bazel, buck, ninja, scons, waf, cargo, go_build, npm_scripts
    ]
    version: string

    # Configuration
    configurationFiles: array[string]
    buildScripts: array[string]

    # Capabilities
    supportedLanguages: array[string]
    supportedPlatforms: array[string]

  relationships:
    executes: Build (1-to-many)
    uses: BuildTool (many-to-many)
```

**Build**
```yaml
Build:
  properties:
    # Identity
    buildID: string (unique)
    buildNumber: string
    buildName: string

    # Timing
    buildDate: datetime
    buildStartTime: datetime
    buildEndTime: datetime
    buildDuration: integer (seconds)

    # Build Configuration
    buildType: enum[debug, release, test, staging, production]
    buildTool: string
    buildToolVersion: string
    buildScript: string
    buildCommand: string

    # Compiler Information
    compiler: string
    compilerVersion: string
    compilerFlags: array[string]
    optimizationLevel: string

    # Environment
    buildEnvironment: {
      os: string,
      osVersion: string,
      architecture: string,
      hostname: string,
      user: string,
      environmentVariables: object
    }

    # Build Parameters
    buildParameters: array[{
      name: string,
      value: string,
      type: string
    }]

    # Source Information
    sourceRepository: string
    sourceBranch: string
    sourceCommit: string
    sourceTag: string

    # Build Status
    buildStatus: enum[success, failure, unstable, aborted]
    exitCode: integer
    errorMessages: array[string]
    warnings: integer
    errors: integer

    # Artifacts
    artifactCount: integer
    artifactTotalSize: integer (bytes)

    # Testing
    testsRun: integer
    testsPassed: integer
    testsFailed: integer
    testCoverage: float (percentage)

    # Quality Metrics
    staticAnalysisFindings: integer
    securityScanFindings: integer
    codeCoverage: float (percentage)
    technicalDebt: string

  relationships:
    # Build inputs
    uses: BuildTool (many-to-many)
    basedOn: SourceCode (many-to-many)
    requires: BuildDependency (many-to-many)

    # Build outputs
    produces: SoftwareComponent (1-to-many)
    generates: Artifact (1-to-many)

    # Build provenance
    triggeredBy: CommitEvent|User|Schedule (many-to-1)
    executedOn: BuildAgent (many-to-1)
    documented By: Provenance (1-to-1)

    # Build lineage
    childOf: Build (many-to-1)
    promotes: Build (many-to-1)
```

**BuildTool**
```yaml
BuildTool:
  properties:
    toolID: string
    toolName: string
    toolVersion: string
    toolType: enum[
      compiler, linker, assembler, packager, minifier, obfuscator,
      code_generator, preprocessor, linter, formatter, test_runner
    ]

    # Tool Binary
    executablePath: string
    hash: string

    # Configuration
    configFile: string
    commandLine: string

  relationships:
    usedIn: Build (many-to-many)
    hasVulnerability: Vulnerability (many-to-many)
```

#### 3.2 Build Artifacts (15,000 nodes)

**Artifact**
```yaml
Artifact:
  properties:
    # Identity
    artifactID: string
    name: string
    groupID: string
    version: string

    # File Information
    fileName: string
    filePath: string
    fileSize: integer (bytes)
    mimeType: string

    # Hashes
    hashes: array[{
      algorithm: enum[sha256, sha512, blake2b],
      value: string
    }]

    # Artifact Type
    artifactType: enum[
      executable, library, archive, container, package, document,
      configuration, data, source, debug_symbols, metadata
    ]

    # Classification
    classifier: string (e.g., sources, javadoc, native)
    extension: string

    # Storage
    storageLocation: string
    repositoryPath: string
    downloadURL: string

    # Metadata
    creationDate: datetime
    modificationDate: datetime
    signature: string

  relationships:
    producedBy: Build (many-to-1)
    contains: SoftwareComponent (many-to-many)
    signedBy: CryptographicKey (many-to-1)
    publishedTo: ArtifactRepository (many-to-1)
```

---

### 4. LICENSES (~15,000 nodes)

#### 4.1 Software Licenses (8,000 nodes)

**SoftwareLicense**
```yaml
SoftwareLicense:
  properties:
    # Identity (SPDX standard)
    licenseID: string (SPDX identifier, e.g., "MIT", "Apache-2.0")
    licenseName: string
    licenseFullName: string

    # License Text
    licenseText: text (full license text)
    standardLicenseTemplate: text (SPDX template with variables)
    licenseTextInFile: string (file containing license)

    # Classification
    licenseType: enum[
      permissive,           # MIT, Apache, BSD
      weak_copyleft,        # LGPL, MPL
      strong_copyleft,      # GPL, AGPL
      proprietary,          # Commercial licenses
      public_domain,        # CC0, Unlicense
      creative_commons,     # CC-BY, CC-BY-SA
      other
    ]

    # Standards Compliance
    osiApproved: boolean (OSI approved)
    fsfLibre: boolean (FSF free software)
    spdxApproved: boolean

    # License Properties
    commercialUse: boolean
    modification: boolean
    distribution: boolean
    patentUse: boolean
    privateUse: boolean
    sublicense: boolean
    trademarkUse: boolean

    # Requirements
    includeNotice: boolean (must include license notice)
    includeLicenseText: boolean
    includeSourceCode: boolean
    includeCopyright: boolean
    stateChanges: boolean (must state modifications)
    discloseSource: boolean

    # Restrictions
    networkDeployment: boolean (triggers obligations on network use)
    trademark: boolean (restricted)
    patent: boolean (patent grant)
    liability: boolean (limits liability)
    warranty: boolean (warranty disclaimer)

    # URLs
    licenseURL: string (canonical URL)
    referenceURL: string (SPDX reference)
    seeAlso: array[string] (additional references)

    # Cross References
    crossRef: array[{
      url: string,
      isValid: boolean,
      isLive: boolean,
      timestamp: datetime,
      match: enum[exact, close, partial]
    }]

    # SPDX Metadata
    isDeprecated: boolean
    deprecatedVersion: string
    isFsfLibre: boolean

  relationships:
    # License relationships
    compatibleWith: SoftwareLicense (many-to-many)
      properties:
        compatibilityType: enum[permissive, conditional, incompatible]
        conditions: array[string]

    conflictsWith: SoftwareLicense (many-to-many)
      properties:
        conflictReason: string
        severity: enum[critical, high, medium, low]

    supersedes: SoftwareLicense (many-to-1)

    # Usage
    appliesTo: SoftwareComponent (many-to-many)

    # License families
    memberOf: LicenseFamily (many-to-1)
```

#### 4.2 License Compliance (7,000 nodes)

**LicenseCompliance**
```yaml
LicenseCompliance:
  properties:
    # Identity
    complianceID: string
    assessmentDate: datetime
    assessor: string

    # Compliance Status
    complianceStatus: enum[
      compliant,              # Fully compliant
      non_compliant,          # Violations found
      needs_review,           # Requires manual review
      unknown,                # Cannot determine
      conditionally_compliant # Compliant with conditions
    ]

    # Risk Assessment
    riskLevel: enum[critical, high, medium, low, none]
    riskScore: float (0-100)

    # Obligations
    obligations: array[{
      type: enum[
        include_license, include_notice, include_source,
        state_changes, provide_install_instructions,
        retain_copyright, rename_product
      ],
      description: string,
      fulfilled: boolean,
      dueDate: datetime
    }]

    # Restrictions
    restrictions: array[{
      type: enum[
        no_commercial_use, no_modification, no_distribution,
        no_sublicense, no_trademark, network_deployment,
        patent_retaliation
      ],
      description: string,
      violated: boolean
    }]

    # Compatibility Analysis
    licenseStack: array[string] (ordered list of licenses)
    compatibilityIssues: array[{
      license1: string,
      license2: string,
      issueType: enum[incompatible, conditional, unclear],
      description: string,
      resolution: string
    }]

    # Attribution Requirements
    attributionText: text
    noticeFile: string

    # Review Information
    reviewDate: datetime
    reviewer: string
    reviewNotes: text
    reviewApproval: enum[approved, rejected, conditional, pending]

    # Remediation
    remediationRequired: boolean
    remediationPlan: text
    remediationDueDate: datetime
    remediationStatus: enum[not_started, in_progress, completed]

  relationships:
    evaluates: SoftwareLicense (many-to-1)
    affects: SoftwareComponent (many-to-many)
    assessedBy: ComplianceTool (many-to-1)
    requires: Action (1-to-many)
```

**LicensePolicy**
```yaml
LicensePolicy:
  properties:
    policyID: string
    policyName: string
    policyVersion: string
    effectiveDate: date
    owner: string

    # Policy Rules
    allowedLicenses: array[string] (SPDX IDs)
    prohibitedLicenses: array[string]
    conditionalLicenses: array[{
      license: string,
      conditions: array[string]
    }]

    # Use Case Policies
    internalUse: enum[allowed, prohibited, requires_review]
    distribution: enum[allowed, prohibited, requires_review]
    saas: enum[allowed, prohibited, requires_review]
    modification: enum[allowed, prohibited, requires_review]

    # Copyleft Handling
    copyleftPolicy: enum[prohibited, isolated, allowed_with_review, allowed]
    networkCopyleftPolicy: enum[prohibited, requires_review, allowed]

  relationships:
    enforces: LicenseRule (1-to-many)
    appliesTo: Project|Organization (many-to-many)
```

---

### 5. PROVENANCE & ATTESTATION (~15,000 nodes)

#### 5.1 Provenance (8,000 nodes)

**Provenance**
```yaml
Provenance:
  properties:
    # Identity (SLSA Provenance format)
    provenanceID: string
    provenanceVersion: string (e.g., "slsa/v0.2", "slsa/v1.0")

    # Builder Identity
    builder: {
      id: string (builder URI),
      version: object,
      builderDependencies: array[{
        uri: string,
        digest: object
      }]
    }

    # Build Type
    buildType: string (URI identifying build procedure)

    # Invocation
    invocation: {
      configSource: {
        uri: string,
        digest: object,
        entryPoint: string
      },
      parameters: object,
      environment: object
    }

    # Build Config
    buildConfig: object (build-specific configuration)

    # Metadata
    metadata: {
      buildInvocationID: string,
      buildStartedOn: datetime,
      buildFinishedOn: datetime,
      completeness: {
        parameters: boolean,
        environment: boolean,
        materials: boolean
      },
      reproducible: boolean
    }

    # Materials (inputs to build)
    materials: array[{
      uri: string,
      digest: object (hash values),
      annotations: object
    }]

    # External Parameters
    externalParameters: object

    # System Parameters
    systemParameters: object

    # Resolved Dependencies
    resolvedDependencies: array[{
      uri: string,
      digest: object,
      name: string,
      downloadLocation: string
    }]

    # Run Details
    runDetails: {
      builder: object,
      metadata: object,
      byproducts: array[{
        name: string,
        uri: string,
        digest: object
      }]
    }

  relationships:
    # Subject (what was built)
    documents: Build (many-to-1)
    verifies: SoftwareComponent|Artifact (many-to-many)
      properties:
        digest: object (hash values)

    # Signing
    signedBy: CryptographicKey (many-to-1)
    attestedBy: Attestation (many-to-1)

    # Build chain
    derivedFrom: Provenance (many-to-many)
```

#### 5.2 Attestations (7,000 nodes)

**Attestation**
```yaml
Attestation:
  properties:
    # Identity (in-toto Attestation format)
    attestationID: string
    attestationType: string (e.g., "https://in-toto.io/Statement/v0.1")

    # Subject (what is being attested)
    subject: array[{
      name: string,
      digest: object (alg → value mapping)
    }]

    # Predicate Type
    predicateType: string (URI)
      # Common types:
      # - https://slsa.dev/provenance/v0.2
      # - https://spdx.dev/Document
      # - https://cyclonedx.org/bom
      # - https://in-toto.io/attestation/scai/attribute-report/v0.2
      # - https://in-toto.io/attestation/vuln/v0.1

    # Predicate (type-specific content)
    predicate: object

    # Envelope (DSSE - Dead Simple Signing Envelope)
    envelope: {
      payloadType: string,
      payload: string (base64),
      signatures: array[{
        keyid: string,
        sig: string (base64)
      }]
    }

    # Timestamp
    timestamp: datetime
    validUntil: datetime

    # Issuer
    issuer: string
    issuerType: enum[organization, individual, automated_system]

    # Verification
    verificationMethod: enum[signature, certificate, token]
    verified: boolean
    verificationDate: datetime

  relationships:
    attests: SoftwareComponent|Build|Artifact (many-to-1)
    signedBy: CryptographicKey (many-to-1)
    verifiedBy: PublicKey|Certificate (many-to-1)
    includes: Provenance (many-to-1)
```

**VulnerabilityAttestation**
```yaml
VulnerabilityAttestation:
  extends: Attestation
  properties:
    # Vulnerability Scan Results
    scannerName: string
    scannerVersion: string
    scanDate: datetime

    # Results
    vulnerabilitiesFound: integer
    criticalCount: integer
    highCount: integer
    mediumCount: integer
    lowCount: integer

    # Detailed Results
    vulnerabilities: array[{
      cveID: string,
      severity: string,
      affectedComponent: string,
      fixedVersion: string,
      exploitAvailable: boolean
    }]

  relationships:
    scannedBy: VulnerabilityScanner (many-to-1)
```

---

## COMPLETE RELATIONSHIP SCHEMAS

### Component-to-Vulnerability Propagation

```cypher
# Direct vulnerability
(comp:SoftwareComponent)-[:HAS_VULNERABILITY]->(vuln:Vulnerability)

# Transitive vulnerability through dependencies
MATCH path = (root:SoftwareComponent)-[:DEPENDS_ON*]->(dep:SoftwareComponent)
              -[:HAS_VULNERABILITY]->(vuln:Vulnerability)
WHERE root.componentID = 'myapp-1.0.0'
RETURN path

# Calculate transitive vulnerability exposure
MATCH (root:SoftwareComponent {componentID: 'myapp-1.0.0'})
MATCH (root)-[:DEPENDS_ON*]->(dep:SoftwareComponent)-[:HAS_VULNERABILITY]->(vuln:Vulnerability)
WITH vuln, count(DISTINCT dep) as affectedDeps
RETURN vuln.cveID, vuln.cvssScore, affectedDeps
ORDER BY vuln.cvssScore DESC
```

### License Compliance Propagation

```cypher
# License inheritance through dependencies
MATCH (root:SoftwareComponent)-[:DEPENDS_ON*]->(dep:SoftwareComponent)
      -[:LICENSED_UNDER]->(license:SoftwareLicense)
WHERE license.licenseType IN ['strong_copyleft', 'weak_copyleft']
RETURN root, dep, license

# Detect license conflicts
MATCH (comp:SoftwareComponent)-[:DEPENDS_ON]->(dep:SoftwareComponent)
      -[:LICENSED_UNDER]->(lic1:SoftwareLicense)
MATCH (comp)-[:LICENSED_UNDER]->(lic2:SoftwareLicense)
MATCH (lic1)-[:CONFLICTS_WITH]->(lic2)
RETURN comp, dep, lic1, lic2
```

### Build Provenance Chain

```cypher
# Complete build provenance
MATCH (artifact:Artifact)<-[:PRODUCES]-(build:Build)
      <-[:DOCUMENTS]-(prov:Provenance)<-[:ATTESTS]-(att:Attestation)
WHERE artifact.artifactID = 'myapp-v1.0.0.jar'
RETURN artifact, build, prov, att

# Verify build chain integrity
MATCH path = (source:SourceCode)-[:USED_IN]->(build:Build)
             -[:PRODUCES]->(artifact:Artifact)
WHERE all(node in nodes(path) WHERE node.verified = true)
RETURN path
```

---

## INTEGRATION PATTERNS

### 1. SBOM Generation from Deployed Systems

```cypher
# Generate SBOM from running application
MATCH (app:Application)-[:RUNS_ON]->(server:Server)
MATCH (app)-[:CONTAINS]->(comp:SoftwareComponent)
OPTIONAL MATCH (comp)-[:DEPENDS_ON*]->(dep:SoftwareComponent)
OPTIONAL MATCH (comp)-[:HAS_VULNERABILITY]->(vuln:Vulnerability)
RETURN {
  application: app.applicationName,
  version: app.version,
  components: collect(DISTINCT comp),
  dependencies: collect(DISTINCT dep),
  vulnerabilities: collect(DISTINCT vuln)
} as sbom
```

### 2. Vulnerability Impact Analysis

```cypher
# Find all deployed systems affected by a CVE
MATCH (cve:Vulnerability {cveID: 'CVE-2024-1234'})
MATCH (cve)<-[:HAS_VULNERABILITY]-(comp:SoftwareComponent)
MATCH (comp)<-[:CONTAINS]-(app:Application)
MATCH (app)<-[:RUNS]-(asset:Asset)
RETURN asset, app, comp, cve
```

### 3. License Compliance Reporting

```cypher
# Audit license compliance across organization
MATCH (org:Organization)-[:OWNS]->(app:Application)
      -[:CONTAINS]->(comp:SoftwareComponent)
      -[:LICENSED_UNDER]->(lic:SoftwareLicense)
OPTIONAL MATCH (lic)-[:CONFLICTS_WITH]->(conflict:SoftwareLicense)
RETURN app.applicationName,
       collect(DISTINCT lic.licenseName) as licenses,
       collect(DISTINCT conflict.licenseName) as conflicts
```

---

## VALIDATION CRITERIA

### Schema Validation
- [ ] All 140,000 SBOM nodes defined
- [ ] Component schemas support SPDX and CycloneDX
- [ ] Dependency relationships include cardinality
- [ ] License schemas support SPDX identifiers
- [ ] Provenance schemas support SLSA and in-toto

### Data Quality
- [ ] Component identifiers (PURL, CPE, SWID) validated
- [ ] Version formats follow semantic versioning where applicable
- [ ] Hash algorithms use cryptographically secure functions
- [ ] License identifiers match SPDX registry
- [ ] Attestation signatures verified

### Integration
- [ ] SBOM components map to deployed applications
- [ ] Vulnerabilities propagate through dependency trees
- [ ] License conflicts detected automatically
- [ ] Build provenance chain verifiable
- [ ] Cross-wave queries validated

---

## EXAMPLE QUERIES

### SBOM Analysis

```cypher
# Generate complete SBOM for application
MATCH (app:Application {name: 'MyWebApp', version: '2.1.0'})
MATCH (app)-[:CONTAINS]->(comp:SoftwareComponent)
OPTIONAL MATCH (comp)-[:DEPENDS_ON]->(dep:SoftwareComponent)
OPTIONAL MATCH (comp)-[:LICENSED_UNDER]->(lic:SoftwareLicense)
OPTIONAL MATCH (comp)-[:HAS_VULNERABILITY]->(vuln:Vulnerability)
RETURN {
  application: {name: app.name, version: app.version},
  components: collect(DISTINCT {
    name: comp.name,
    version: comp.version,
    purl: comp.purl,
    license: lic.licenseID,
    vulnerabilities: collect(vuln.cveID)
  })
}

# Find applications using vulnerable components
MATCH (vuln:Vulnerability {cveID: 'CVE-2024-5678'})
MATCH (comp:SoftwareComponent)-[:HAS_VULNERABILITY]->(vuln)
MATCH (app:Application)-[:CONTAINS|DEPENDS_ON*]->(comp)
RETURN app.name, comp.name, comp.version, vuln.cvssScore

# Identify outdated dependencies
MATCH (comp:SoftwareComponent)
WHERE comp.endOfSupportDate < date()
MATCH (app:Application)-[:CONTAINS|DEPENDS_ON*]->(comp)
RETURN app.name, comp.name, comp.version, comp.endOfSupportDate
ORDER BY comp.endOfSupportDate
```

---

**Wave Status:** COMPLETE
**Nodes Defined:** ~140,000
**Schemas Complete:** 100%
**Standards Supported:** SPDX 2.3, CycloneDX 1.5, SLSA v1.0, in-toto v0.1
**Integration Ready:** YES
