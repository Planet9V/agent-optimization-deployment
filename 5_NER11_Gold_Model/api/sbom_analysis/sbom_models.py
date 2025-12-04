"""
SBOM Analysis Models
====================

Data models for E03: SBOM Dependency & Vulnerability Tracking.
Includes SoftwareComponent, SBOM, SoftwareVulnerability, and DependencyRelation entities.

Version: 1.0.0
Created: 2025-12-04
"""

from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from typing import Optional, List, Dict, Any


# =============================================================================
# Enums for SBOM Analysis
# =============================================================================


class SBOMFormat(Enum):
    """Supported SBOM formats."""
    CYCLONEDX = "cyclonedx"       # CycloneDX JSON/XML format
    SPDX = "spdx"                 # SPDX JSON/XML/RDF format
    SWID = "swid"                 # Software Identification Tags
    SYFT = "syft"                 # Anchore Syft format
    CUSTOM = "custom"             # Custom/proprietary format


class ComponentType(Enum):
    """Types of software components in SBOM."""
    APPLICATION = "application"   # Standalone application
    LIBRARY = "library"           # Software library/package
    FRAMEWORK = "framework"       # Development framework
    FIRMWARE = "firmware"         # Device firmware
    OPERATING_SYSTEM = "operating_system"
    DEVICE = "device"             # Hardware device with software
    CONTAINER = "container"       # Container image
    FILE = "file"                 # Individual file component
    SNIPPET = "snippet"           # Code snippet
    DATA = "data"                 # Data component


class LicenseType(Enum):
    """Common software license types."""
    MIT = "mit"
    APACHE_2 = "apache-2.0"
    GPL_2 = "gpl-2.0"
    GPL_3 = "gpl-3.0"
    LGPL = "lgpl"
    BSD_2 = "bsd-2-clause"
    BSD_3 = "bsd-3-clause"
    MPL_2 = "mpl-2.0"
    ISC = "isc"
    AGPL_3 = "agpl-3.0"
    PROPRIETARY = "proprietary"
    COMMERCIAL = "commercial"
    UNKNOWN = "unknown"
    OTHER = "other"


class LicenseRisk(Enum):
    """License risk levels for compliance."""
    LOW = "low"           # Permissive (MIT, BSD, Apache)
    MEDIUM = "medium"     # Weak copyleft (LGPL, MPL)
    HIGH = "high"         # Strong copyleft (GPL, AGPL)
    CRITICAL = "critical" # Unknown or proprietary incompatible


class DependencyType(Enum):
    """Types of dependency relationships."""
    DIRECT = "direct"           # Directly declared dependency
    TRANSITIVE = "transitive"   # Indirect dependency
    OPTIONAL = "optional"       # Optional/suggested dependency
    DEV = "dev"                 # Development/test dependency
    PEER = "peer"               # Peer dependency (npm)
    BUILD = "build"             # Build-time dependency
    RUNTIME = "runtime"         # Runtime-only dependency


class DependencyScope(Enum):
    """Scope of dependency in build/runtime."""
    COMPILE = "compile"
    RUNTIME = "runtime"
    TEST = "test"
    PROVIDED = "provided"
    SYSTEM = "system"
    IMPORT = "import"


class VulnerabilitySeverity(Enum):
    """CVSS-based vulnerability severity levels."""
    NONE = "none"         # CVSS 0.0
    LOW = "low"           # CVSS 0.1-3.9
    MEDIUM = "medium"     # CVSS 4.0-6.9
    HIGH = "high"         # CVSS 7.0-8.9
    CRITICAL = "critical" # CVSS 9.0-10.0


class ExploitMaturity(Enum):
    """Exploit maturity levels (EPSS-related)."""
    NOT_DEFINED = "not_defined"
    UNPROVEN = "unproven"
    PROOF_OF_CONCEPT = "proof_of_concept"
    FUNCTIONAL = "functional"
    HIGH = "high"
    WEAPONIZED = "weaponized"


class RemediationType(Enum):
    """Types of vulnerability remediation."""
    PATCH = "patch"                 # Security patch available
    UPGRADE = "upgrade"             # Version upgrade needed
    WORKAROUND = "workaround"       # Temporary workaround available
    MITIGATION = "mitigation"       # Mitigating controls available
    VENDOR_FIX = "vendor_fix"       # Vendor-provided fix
    NO_FIX = "no_fix"               # No fix available
    WILL_NOT_FIX = "will_not_fix"   # Vendor declined to fix


class ComponentStatus(Enum):
    """Status of component in the system."""
    ACTIVE = "active"             # Currently in use
    DEPRECATED = "deprecated"     # Marked for removal
    VULNERABLE = "vulnerable"     # Has known vulnerabilities
    EOL = "eol"                   # End of life
    REPLACED = "replaced"         # Replaced by another component
    PENDING_REVIEW = "pending_review"


# =============================================================================
# Core Data Models
# =============================================================================


@dataclass
class SoftwareComponent:
    """
    Software Component entity for SBOM tracking.

    Represents a single software component (library, package, container)
    with Package URL (purl), CPE, license, and vulnerability information.
    """
    component_id: str
    customer_id: str  # For multi-tenant isolation
    name: str
    version: str

    # Package identification
    purl: Optional[str] = None  # Package URL (e.g., pkg:npm/lodash@4.17.21)
    cpe: Optional[str] = None   # CPE identifier (e.g., cpe:2.3:a:lodash:lodash:4.17.21:*)

    # Component classification
    component_type: ComponentType = ComponentType.LIBRARY
    group: Optional[str] = None      # Maven groupId, npm scope, etc.
    namespace: Optional[str] = None  # Package namespace

    # Version and release
    release_date: Optional[date] = None
    latest_version: Optional[str] = None
    is_latest: bool = False

    # License information
    license_type: LicenseType = LicenseType.UNKNOWN
    license_expression: Optional[str] = None  # SPDX expression (e.g., "MIT OR Apache-2.0")
    license_risk: LicenseRisk = LicenseRisk.LOW

    # Vulnerability summary (denormalized for performance)
    vulnerability_count: int = 0
    critical_vuln_count: int = 0
    high_vuln_count: int = 0
    medium_vuln_count: int = 0
    low_vuln_count: int = 0
    max_cvss_score: float = 0.0
    epss_score: Optional[float] = None  # EPSS probability (0.0-1.0)

    # Status and metadata
    status: ComponentStatus = ComponentStatus.ACTIVE
    description: Optional[str] = None
    supplier: Optional[str] = None      # Package supplier/maintainer
    author: Optional[str] = None
    homepage: Optional[str] = None
    repository_url: Optional[str] = None

    # Source SBOM reference
    sbom_id: Optional[str] = None

    # Hash values for integrity
    sha256: Optional[str] = None
    sha1: Optional[str] = None
    md5: Optional[str] = None

    # Timestamps
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    last_scanned: Optional[datetime] = None

    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate component data on creation."""
        if not self.component_id or not self.component_id.strip():
            raise ValueError("component_id is required")
        if not self.customer_id or not self.customer_id.strip():
            raise ValueError("customer_id is required")
        if not self.name or not self.name.strip():
            raise ValueError("name is required")
        if not self.version or not self.version.strip():
            raise ValueError("version is required")

        # Normalize values
        self.component_id = self.component_id.strip()
        self.customer_id = self.customer_id.strip()
        self.name = self.name.strip()
        self.version = self.version.strip()

        # Calculate license risk from type if not set
        if self.license_risk == LicenseRisk.LOW:
            self.license_risk = self._calculate_license_risk()

    def _calculate_license_risk(self) -> LicenseRisk:
        """Calculate license risk based on license type."""
        permissive = {LicenseType.MIT, LicenseType.BSD_2, LicenseType.BSD_3,
                      LicenseType.APACHE_2, LicenseType.ISC}
        weak_copyleft = {LicenseType.LGPL, LicenseType.MPL_2}
        strong_copyleft = {LicenseType.GPL_2, LicenseType.GPL_3, LicenseType.AGPL_3}

        if self.license_type in permissive:
            return LicenseRisk.LOW
        elif self.license_type in weak_copyleft:
            return LicenseRisk.MEDIUM
        elif self.license_type in strong_copyleft:
            return LicenseRisk.HIGH
        elif self.license_type in {LicenseType.UNKNOWN, LicenseType.PROPRIETARY}:
            return LicenseRisk.CRITICAL
        return LicenseRisk.LOW

    def generate_purl(self) -> str:
        """Generate Package URL if not set."""
        if self.purl:
            return self.purl

        # Infer package type from component type
        pkg_type = "generic"
        if "npm" in str(self.metadata.get("ecosystem", "")).lower():
            pkg_type = "npm"
        elif "pypi" in str(self.metadata.get("ecosystem", "")).lower():
            pkg_type = "pypi"
        elif "maven" in str(self.metadata.get("ecosystem", "")).lower():
            pkg_type = "maven"
        elif "nuget" in str(self.metadata.get("ecosystem", "")).lower():
            pkg_type = "nuget"

        if self.group:
            return f"pkg:{pkg_type}/{self.group}/{self.name}@{self.version}"
        return f"pkg:{pkg_type}/{self.name}@{self.version}"

    @property
    def has_vulnerabilities(self) -> bool:
        """Check if component has any known vulnerabilities."""
        return self.vulnerability_count > 0

    @property
    def is_high_risk(self) -> bool:
        """Check if component is high risk (critical/high vulns or license issues)."""
        return (self.critical_vuln_count > 0 or
                self.high_vuln_count > 0 or
                self.license_risk in {LicenseRisk.HIGH, LicenseRisk.CRITICAL})

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response."""
        return {
            "component_id": self.component_id,
            "customer_id": self.customer_id,
            "name": self.name,
            "version": self.version,
            "purl": self.purl or self.generate_purl(),
            "cpe": self.cpe,
            "component_type": self.component_type.value,
            "group": self.group,
            "namespace": self.namespace,
            "release_date": self.release_date.isoformat() if self.release_date else None,
            "latest_version": self.latest_version,
            "is_latest": self.is_latest,
            "license_type": self.license_type.value,
            "license_expression": self.license_expression,
            "license_risk": self.license_risk.value,
            "vulnerability_count": self.vulnerability_count,
            "critical_vuln_count": self.critical_vuln_count,
            "high_vuln_count": self.high_vuln_count,
            "medium_vuln_count": self.medium_vuln_count,
            "low_vuln_count": self.low_vuln_count,
            "max_cvss_score": self.max_cvss_score,
            "epss_score": self.epss_score,
            "status": self.status.value,
            "description": self.description,
            "supplier": self.supplier,
            "author": self.author,
            "homepage": self.homepage,
            "repository_url": self.repository_url,
            "sbom_id": self.sbom_id,
            "sha256": self.sha256,
            "has_vulnerabilities": self.has_vulnerabilities,
            "is_high_risk": self.is_high_risk,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "last_scanned": self.last_scanned.isoformat() if self.last_scanned else None,
        }

    def to_qdrant_payload(self) -> Dict[str, Any]:
        """Convert to Qdrant point payload."""
        return {
            "component_id": self.component_id,
            "customer_id": self.customer_id,
            "name": self.name,
            "version": self.version,
            "entity_type": "software_component",
            "purl": self.purl or self.generate_purl(),
            "cpe": self.cpe,
            "component_type": self.component_type.value,
            "group": self.group,
            "license_type": self.license_type.value,
            "license_risk": self.license_risk.value,
            "vulnerability_count": self.vulnerability_count,
            "critical_vuln_count": self.critical_vuln_count,
            "high_vuln_count": self.high_vuln_count,
            "max_cvss_score": self.max_cvss_score,
            "epss_score": self.epss_score,
            "status": self.status.value,
            "sbom_id": self.sbom_id,
            "is_high_risk": self.is_high_risk,
        }


@dataclass
class SBOM:
    """
    Software Bill of Materials entity.

    Represents a complete SBOM document with format, component counts,
    and metadata about the analyzed software system.
    """
    sbom_id: str
    customer_id: str  # For multi-tenant isolation
    name: str

    # SBOM format and version
    format: SBOMFormat = SBOMFormat.CYCLONEDX
    format_version: str = "1.5"  # CycloneDX 1.5, SPDX 2.3, etc.
    spec_version: Optional[str] = None  # Specification version

    # Component counts
    total_components: int = 0
    direct_dependencies: int = 0
    transitive_dependencies: int = 0

    # Vulnerability summary (denormalized)
    total_vulnerabilities: int = 0
    critical_count: int = 0
    high_count: int = 0
    medium_count: int = 0
    low_count: int = 0

    # License summary
    license_types: List[str] = field(default_factory=list)  # Unique licenses
    license_risk_summary: Dict[str, int] = field(default_factory=dict)  # {risk: count}

    # Source information
    source_type: Optional[str] = None  # 'git', 'container', 'filesystem', 'upload'
    source_url: Optional[str] = None
    source_hash: Optional[str] = None

    # Target system
    target_system_id: Optional[str] = None  # Link to Asset in NER11
    target_application: Optional[str] = None
    target_version: Optional[str] = None

    # Generation info
    generator_tool: Optional[str] = None  # 'syft', 'trivy', 'cyclonedx-cli', etc.
    generator_version: Optional[str] = None
    generated_at: Optional[datetime] = None

    # Metadata
    description: Optional[str] = None
    serial_number: Optional[str] = None  # CycloneDX serial number
    namespace: Optional[str] = None       # SPDX namespace

    # Status
    is_valid: bool = True
    validation_errors: List[str] = field(default_factory=list)

    # Timestamps
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    last_analyzed: Optional[datetime] = None

    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate SBOM data on creation."""
        if not self.sbom_id or not self.sbom_id.strip():
            raise ValueError("sbom_id is required")
        if not self.customer_id or not self.customer_id.strip():
            raise ValueError("customer_id is required")
        if not self.name or not self.name.strip():
            raise ValueError("name is required")

        # Normalize values
        self.sbom_id = self.sbom_id.strip()
        self.customer_id = self.customer_id.strip()
        self.name = self.name.strip()

    @property
    def has_vulnerabilities(self) -> bool:
        """Check if SBOM has any known vulnerabilities."""
        return self.total_vulnerabilities > 0

    @property
    def vulnerability_density(self) -> float:
        """Calculate vulnerabilities per component ratio."""
        if self.total_components == 0:
            return 0.0
        return self.total_vulnerabilities / self.total_components

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response."""
        return {
            "sbom_id": self.sbom_id,
            "customer_id": self.customer_id,
            "name": self.name,
            "format": self.format.value,
            "format_version": self.format_version,
            "spec_version": self.spec_version,
            "total_components": self.total_components,
            "direct_dependencies": self.direct_dependencies,
            "transitive_dependencies": self.transitive_dependencies,
            "total_vulnerabilities": self.total_vulnerabilities,
            "critical_count": self.critical_count,
            "high_count": self.high_count,
            "medium_count": self.medium_count,
            "low_count": self.low_count,
            "vulnerability_density": self.vulnerability_density,
            "license_types": self.license_types,
            "license_risk_summary": self.license_risk_summary,
            "source_type": self.source_type,
            "source_url": self.source_url,
            "target_system_id": self.target_system_id,
            "target_application": self.target_application,
            "target_version": self.target_version,
            "generator_tool": self.generator_tool,
            "generator_version": self.generator_version,
            "generated_at": self.generated_at.isoformat() if self.generated_at else None,
            "description": self.description,
            "serial_number": self.serial_number,
            "namespace": self.namespace,
            "is_valid": self.is_valid,
            "validation_errors": self.validation_errors,
            "has_vulnerabilities": self.has_vulnerabilities,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "last_analyzed": self.last_analyzed.isoformat() if self.last_analyzed else None,
        }

    def to_qdrant_payload(self) -> Dict[str, Any]:
        """Convert to Qdrant point payload."""
        return {
            "sbom_id": self.sbom_id,
            "customer_id": self.customer_id,
            "name": self.name,
            "entity_type": "sbom",
            "format": self.format.value,
            "format_version": self.format_version,
            "total_components": self.total_components,
            "direct_dependencies": self.direct_dependencies,
            "transitive_dependencies": self.transitive_dependencies,
            "total_vulnerabilities": self.total_vulnerabilities,
            "critical_count": self.critical_count,
            "high_count": self.high_count,
            "vulnerability_density": self.vulnerability_density,
            "target_system_id": self.target_system_id,
            "generator_tool": self.generator_tool,
            "is_valid": self.is_valid,
        }


@dataclass
class SoftwareVulnerability:
    """
    Software Vulnerability entity for CVE tracking.

    Links CVEs to software components with CVSS, EPSS, and remediation info.
    """
    vulnerability_id: str
    customer_id: str  # For multi-tenant isolation
    cve_id: str       # CVE-YYYY-NNNNN format

    # Component linkage
    component_id: str
    component_name: str
    component_version: str
    affected_versions: List[str] = field(default_factory=list)  # Version ranges

    # Severity scoring
    severity: VulnerabilitySeverity = VulnerabilitySeverity.MEDIUM
    cvss_v3_score: float = 0.0
    cvss_v3_vector: Optional[str] = None  # CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H
    cvss_v2_score: Optional[float] = None

    # EPSS (Exploit Prediction Scoring System)
    epss_score: Optional[float] = None     # Probability 0.0-1.0
    epss_percentile: Optional[float] = None

    # Exploit information
    exploit_maturity: ExploitMaturity = ExploitMaturity.NOT_DEFINED
    exploit_available: bool = False
    exploit_url: Optional[str] = None
    in_the_wild: bool = False               # Actively exploited in the wild
    cisa_kev: bool = False                  # CISA Known Exploited Vulnerabilities

    # Vulnerability details
    description: Optional[str] = None
    cwe_ids: List[str] = field(default_factory=list)  # CWE-79, CWE-89, etc.
    attack_vector: Optional[str] = None    # NETWORK, ADJACENT, LOCAL, PHYSICAL
    attack_complexity: Optional[str] = None  # LOW, HIGH

    # Remediation
    remediation_type: RemediationType = RemediationType.NO_FIX
    fixed_version: Optional[str] = None
    patch_url: Optional[str] = None
    workaround: Optional[str] = None

    # APT/Threat Actor linkage
    apt_groups: List[str] = field(default_factory=list)  # Known APT groups using this
    malware_families: List[str] = field(default_factory=list)

    # Timeline
    published_date: Optional[date] = None
    modified_date: Optional[date] = None
    discovered_date: Optional[date] = None

    # References
    references: List[str] = field(default_factory=list)
    nvd_url: Optional[str] = None
    vendor_advisory: Optional[str] = None

    # Status tracking
    is_acknowledged: bool = False
    acknowledged_by: Optional[str] = None
    acknowledged_at: Optional[datetime] = None
    is_false_positive: bool = False

    # Timestamps
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate vulnerability data on creation."""
        if not self.vulnerability_id or not self.vulnerability_id.strip():
            raise ValueError("vulnerability_id is required")
        if not self.customer_id or not self.customer_id.strip():
            raise ValueError("customer_id is required")
        if not self.cve_id or not self.cve_id.strip():
            raise ValueError("cve_id is required")
        if not self.component_id or not self.component_id.strip():
            raise ValueError("component_id is required")

        # Normalize values
        self.vulnerability_id = self.vulnerability_id.strip()
        self.customer_id = self.customer_id.strip()
        self.cve_id = self.cve_id.strip().upper()
        self.component_id = self.component_id.strip()

        # Calculate severity from CVSS if not set correctly
        if self.cvss_v3_score > 0:
            self.severity = self._calculate_severity()

        # Generate NVD URL if not set
        if not self.nvd_url and self.cve_id.startswith("CVE-"):
            self.nvd_url = f"https://nvd.nist.gov/vuln/detail/{self.cve_id}"

    def _calculate_severity(self) -> VulnerabilitySeverity:
        """Calculate severity from CVSS v3 score."""
        if self.cvss_v3_score == 0.0:
            return VulnerabilitySeverity.NONE
        elif self.cvss_v3_score < 4.0:
            return VulnerabilitySeverity.LOW
        elif self.cvss_v3_score < 7.0:
            return VulnerabilitySeverity.MEDIUM
        elif self.cvss_v3_score < 9.0:
            return VulnerabilitySeverity.HIGH
        else:
            return VulnerabilitySeverity.CRITICAL

    @property
    def is_critical(self) -> bool:
        """Check if vulnerability is critical priority."""
        return (self.severity == VulnerabilitySeverity.CRITICAL or
                self.cisa_kev or
                self.in_the_wild)

    @property
    def is_exploitable(self) -> bool:
        """Check if vulnerability has known exploits."""
        return (self.exploit_available or
                self.in_the_wild or
                self.exploit_maturity in {ExploitMaturity.FUNCTIONAL,
                                           ExploitMaturity.HIGH,
                                           ExploitMaturity.WEAPONIZED})

    @property
    def has_fix(self) -> bool:
        """Check if remediation is available."""
        return self.remediation_type in {RemediationType.PATCH,
                                          RemediationType.UPGRADE,
                                          RemediationType.VENDOR_FIX}

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response."""
        return {
            "vulnerability_id": self.vulnerability_id,
            "customer_id": self.customer_id,
            "cve_id": self.cve_id,
            "component_id": self.component_id,
            "component_name": self.component_name,
            "component_version": self.component_version,
            "affected_versions": self.affected_versions,
            "severity": self.severity.value,
            "cvss_v3_score": self.cvss_v3_score,
            "cvss_v3_vector": self.cvss_v3_vector,
            "cvss_v2_score": self.cvss_v2_score,
            "epss_score": self.epss_score,
            "epss_percentile": self.epss_percentile,
            "exploit_maturity": self.exploit_maturity.value,
            "exploit_available": self.exploit_available,
            "exploit_url": self.exploit_url,
            "in_the_wild": self.in_the_wild,
            "cisa_kev": self.cisa_kev,
            "description": self.description,
            "cwe_ids": self.cwe_ids,
            "attack_vector": self.attack_vector,
            "attack_complexity": self.attack_complexity,
            "remediation_type": self.remediation_type.value,
            "fixed_version": self.fixed_version,
            "patch_url": self.patch_url,
            "workaround": self.workaround,
            "apt_groups": self.apt_groups,
            "malware_families": self.malware_families,
            "published_date": self.published_date.isoformat() if self.published_date else None,
            "modified_date": self.modified_date.isoformat() if self.modified_date else None,
            "references": self.references,
            "nvd_url": self.nvd_url,
            "vendor_advisory": self.vendor_advisory,
            "is_acknowledged": self.is_acknowledged,
            "is_false_positive": self.is_false_positive,
            "is_critical": self.is_critical,
            "is_exploitable": self.is_exploitable,
            "has_fix": self.has_fix,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def to_qdrant_payload(self) -> Dict[str, Any]:
        """Convert to Qdrant point payload."""
        return {
            "vulnerability_id": self.vulnerability_id,
            "customer_id": self.customer_id,
            "cve_id": self.cve_id,
            "entity_type": "software_vulnerability",
            "component_id": self.component_id,
            "component_name": self.component_name,
            "severity": self.severity.value,
            "cvss_v3_score": self.cvss_v3_score,
            "epss_score": self.epss_score,
            "exploit_maturity": self.exploit_maturity.value,
            "exploit_available": self.exploit_available,
            "in_the_wild": self.in_the_wild,
            "cisa_kev": self.cisa_kev,
            "remediation_type": self.remediation_type.value,
            "has_fix": self.has_fix,
            "is_critical": self.is_critical,
            "is_exploitable": self.is_exploitable,
            "apt_groups": self.apt_groups,
            "cwe_ids": self.cwe_ids,
        }


@dataclass
class DependencyRelation:
    """
    Dependency Relationship between software components.

    Represents the dependency graph structure with direct/transitive relationships.
    """
    relation_id: str
    customer_id: str  # For multi-tenant isolation

    # Source and target components
    source_component_id: str
    source_component_name: str
    source_version: str

    target_component_id: str
    target_component_name: str
    target_version: str

    # Relationship type
    dependency_type: DependencyType = DependencyType.DIRECT
    scope: DependencyScope = DependencyScope.RUNTIME

    # Depth in dependency tree
    depth: int = 1  # 1 = direct, 2+ = transitive

    # Version constraints
    version_constraint: Optional[str] = None  # ^1.0.0, >=2.0, etc.
    is_version_locked: bool = False

    # Optional/required
    is_optional: bool = False
    is_dev_dependency: bool = False

    # SBOM context
    sbom_id: Optional[str] = None

    # Risk propagation
    propagates_vulnerabilities: bool = True  # Does this dep affect parent?

    # Timestamps
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate relationship data on creation."""
        if not self.relation_id or not self.relation_id.strip():
            raise ValueError("relation_id is required")
        if not self.customer_id or not self.customer_id.strip():
            raise ValueError("customer_id is required")
        if not self.source_component_id or not self.source_component_id.strip():
            raise ValueError("source_component_id is required")
        if not self.target_component_id or not self.target_component_id.strip():
            raise ValueError("target_component_id is required")

        # Normalize values
        self.relation_id = self.relation_id.strip()
        self.customer_id = self.customer_id.strip()
        self.source_component_id = self.source_component_id.strip()
        self.target_component_id = self.target_component_id.strip()

        # Set transitive if depth > 1
        if self.depth > 1:
            self.dependency_type = DependencyType.TRANSITIVE

        # Dev dependencies don't propagate vulnerabilities by default
        if self.is_dev_dependency and self.scope == DependencyScope.TEST:
            self.propagates_vulnerabilities = False

    @property
    def is_direct(self) -> bool:
        """Check if this is a direct dependency."""
        return self.dependency_type == DependencyType.DIRECT and self.depth == 1

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response."""
        return {
            "relation_id": self.relation_id,
            "customer_id": self.customer_id,
            "source_component_id": self.source_component_id,
            "source_component_name": self.source_component_name,
            "source_version": self.source_version,
            "target_component_id": self.target_component_id,
            "target_component_name": self.target_component_name,
            "target_version": self.target_version,
            "dependency_type": self.dependency_type.value,
            "scope": self.scope.value,
            "depth": self.depth,
            "version_constraint": self.version_constraint,
            "is_version_locked": self.is_version_locked,
            "is_optional": self.is_optional,
            "is_dev_dependency": self.is_dev_dependency,
            "sbom_id": self.sbom_id,
            "propagates_vulnerabilities": self.propagates_vulnerabilities,
            "is_direct": self.is_direct,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def to_qdrant_payload(self) -> Dict[str, Any]:
        """Convert to Qdrant point payload."""
        return {
            "relation_id": self.relation_id,
            "customer_id": self.customer_id,
            "entity_type": "dependency_relation",
            "source_component_id": self.source_component_id,
            "source_component_name": self.source_component_name,
            "target_component_id": self.target_component_id,
            "target_component_name": self.target_component_name,
            "dependency_type": self.dependency_type.value,
            "scope": self.scope.value,
            "depth": self.depth,
            "is_optional": self.is_optional,
            "is_dev_dependency": self.is_dev_dependency,
            "sbom_id": self.sbom_id,
            "propagates_vulnerabilities": self.propagates_vulnerabilities,
        }


@dataclass
class LicenseComplianceResult:
    """
    License Compliance Analysis Result.

    Represents the result of analyzing an SBOM for license compliance issues.
    """
    result_id: str
    customer_id: str
    sbom_id: str

    # Compliance summary
    is_compliant: bool = True
    total_components: int = 0
    compliant_count: int = 0
    non_compliant_count: int = 0
    unknown_count: int = 0

    # Risk breakdown
    low_risk_count: int = 0
    medium_risk_count: int = 0
    high_risk_count: int = 0
    critical_risk_count: int = 0

    # Specific issues
    copyleft_violations: List[Dict[str, Any]] = field(default_factory=list)
    license_conflicts: List[Dict[str, Any]] = field(default_factory=list)
    unknown_licenses: List[str] = field(default_factory=list)

    # Policy reference
    policy_name: Optional[str] = None
    allowed_licenses: List[str] = field(default_factory=list)
    denied_licenses: List[str] = field(default_factory=list)

    # Timestamps
    analyzed_at: datetime = field(default_factory=datetime.utcnow)

    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response."""
        return {
            "result_id": self.result_id,
            "customer_id": self.customer_id,
            "sbom_id": self.sbom_id,
            "is_compliant": self.is_compliant,
            "total_components": self.total_components,
            "compliant_count": self.compliant_count,
            "non_compliant_count": self.non_compliant_count,
            "unknown_count": self.unknown_count,
            "low_risk_count": self.low_risk_count,
            "medium_risk_count": self.medium_risk_count,
            "high_risk_count": self.high_risk_count,
            "critical_risk_count": self.critical_risk_count,
            "copyleft_violations": self.copyleft_violations,
            "license_conflicts": self.license_conflicts,
            "unknown_licenses": self.unknown_licenses,
            "policy_name": self.policy_name,
            "allowed_licenses": self.allowed_licenses,
            "denied_licenses": self.denied_licenses,
            "analyzed_at": self.analyzed_at.isoformat(),
        }


@dataclass
class DependencyGraphNode:
    """
    Node in dependency graph for visualization and analysis.

    Used for building dependency trees and calculating impact paths.
    """
    component_id: str
    component_name: str
    version: str

    # Node properties
    depth: int = 0
    is_root: bool = False
    is_leaf: bool = False

    # Metrics
    dependents_count: int = 0    # Components depending on this
    dependencies_count: int = 0  # Components this depends on

    # Risk
    vulnerability_count: int = 0
    max_severity: Optional[str] = None
    license_risk: Optional[str] = None

    # Children in tree (for traversal)
    children: List["DependencyGraphNode"] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API/visualization response."""
        return {
            "component_id": self.component_id,
            "component_name": self.component_name,
            "version": self.version,
            "depth": self.depth,
            "is_root": self.is_root,
            "is_leaf": self.is_leaf,
            "dependents_count": self.dependents_count,
            "dependencies_count": self.dependencies_count,
            "vulnerability_count": self.vulnerability_count,
            "max_severity": self.max_severity,
            "license_risk": self.license_risk,
            "children": [child.to_dict() for child in self.children],
        }
