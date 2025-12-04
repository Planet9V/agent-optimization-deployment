"""
Compliance Mapping Models
=========================

Data models for E07: Compliance & Framework Mapping API.
Includes ComplianceControl, ComplianceMapping, ComplianceAssessment, ComplianceEvidence, and ComplianceGap entities.

Version: 1.0.0
Created: 2025-12-04
"""

from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from typing import Optional, List, Dict, Any


# =============================================================================
# Enums for Compliance Mapping
# =============================================================================


class ComplianceFramework(Enum):
    """Supported compliance frameworks."""
    NERC_CIP = "nerc_cip"           # NERC Critical Infrastructure Protection
    NIST_CSF = "nist_csf"           # NIST Cybersecurity Framework
    ISO_27001 = "iso_27001"         # ISO/IEC 27001
    SOC2 = "soc2"                   # SOC 2 Type II
    PCI_DSS = "pci_dss"             # Payment Card Industry DSS
    HIPAA = "hipaa"                 # Health Insurance Portability and Accountability Act
    GDPR = "gdpr"                   # General Data Protection Regulation
    CIS_CONTROLS = "cis_controls"   # CIS Critical Security Controls


class ComplianceStatus(Enum):
    """Compliance status for controls."""
    COMPLIANT = "compliant"           # Fully compliant
    NON_COMPLIANT = "non_compliant"   # Not compliant
    PARTIAL = "partial"               # Partially compliant
    NOT_ASSESSED = "not_assessed"     # Not yet assessed
    NOT_APPLICABLE = "not_applicable" # Not applicable to organization


class ControlCategory(Enum):
    """Control category types."""
    ADMINISTRATIVE = "administrative"  # Administrative/procedural controls
    TECHNICAL = "technical"           # Technical/logical controls
    PHYSICAL = "physical"             # Physical security controls


class AssessmentType(Enum):
    """Types of compliance assessments."""
    SELF_ASSESSMENT = "self_assessment"       # Internal self-assessment
    INTERNAL_AUDIT = "internal_audit"         # Internal audit
    EXTERNAL_AUDIT = "external_audit"         # External auditor assessment
    CONTINUOUS_MONITORING = "continuous_monitoring"  # Automated continuous monitoring


class EvidenceType(Enum):
    """Types of compliance evidence."""
    DOCUMENT = "document"             # Policy, procedure document
    SCREENSHOT = "screenshot"         # Screenshot of configuration
    LOG = "log"                       # Log file or extract
    CONFIGURATION = "configuration"   # System configuration file
    ATTESTATION = "attestation"       # Signed attestation or declaration


# =============================================================================
# Core Data Models
# =============================================================================


@dataclass
class ComplianceControl:
    """
    Compliance Control entity.

    Represents a specific control requirement from a compliance framework
    with implementation and assessment details.
    """
    control_id: str
    customer_id: str  # For multi-tenant isolation
    framework: ComplianceFramework
    control_number: str  # e.g., "CIP-007-6 R1"

    # Control details
    title: str
    description: str
    category: ControlCategory = ControlCategory.TECHNICAL

    # Requirements
    requirements: List[str] = field(default_factory=list)  # Specific requirements
    implementation_guidance: Optional[str] = None
    evidence_requirements: List[str] = field(default_factory=list)  # Required evidence types

    # Cross-framework mapping
    mapped_controls: Dict[str, List[str]] = field(default_factory=dict)  # {framework: [control_ids]}

    # Assessment
    status: ComplianceStatus = ComplianceStatus.NOT_ASSESSED
    assessment_date: Optional[date] = None
    assessor: Optional[str] = None
    findings: List[str] = field(default_factory=list)  # Assessment findings
    remediation_actions: List[str] = field(default_factory=list)  # Required remediation

    # Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate control data on creation."""
        if not self.control_id or not self.control_id.strip():
            raise ValueError("control_id is required")
        if not self.customer_id or not self.customer_id.strip():
            raise ValueError("customer_id is required")
        if not self.control_number or not self.control_number.strip():
            raise ValueError("control_number is required")
        if not self.title or not self.title.strip():
            raise ValueError("title is required")
        if not self.description or not self.description.strip():
            raise ValueError("description is required")

        # Normalize values
        self.control_id = self.control_id.strip()
        self.customer_id = self.customer_id.strip()
        self.control_number = self.control_number.strip()
        self.title = self.title.strip()

    @property
    def is_compliant(self) -> bool:
        """Check if control is compliant."""
        return self.status == ComplianceStatus.COMPLIANT

    @property
    def has_gaps(self) -> bool:
        """Check if control has compliance gaps."""
        return self.status in {ComplianceStatus.NON_COMPLIANT, ComplianceStatus.PARTIAL}

    @property
    def compliance_score(self) -> float:
        """Calculate compliance score (0.0-10.0)."""
        if self.status == ComplianceStatus.COMPLIANT:
            return 10.0
        elif self.status == ComplianceStatus.PARTIAL:
            return 5.0
        elif self.status == ComplianceStatus.NON_COMPLIANT:
            return 0.0
        elif self.status == ComplianceStatus.NOT_APPLICABLE:
            return 10.0  # N/A counts as "compliant"
        else:
            return 0.0  # Not assessed

    @property
    def mapped_framework_count(self) -> int:
        """Count number of frameworks this control maps to."""
        return len(self.mapped_controls)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response."""
        return {
            "control_id": self.control_id,
            "customer_id": self.customer_id,
            "framework": self.framework.value,
            "control_number": self.control_number,
            "title": self.title,
            "description": self.description,
            "category": self.category.value,
            "requirements": self.requirements,
            "implementation_guidance": self.implementation_guidance,
            "evidence_requirements": self.evidence_requirements,
            "mapped_controls": self.mapped_controls,
            "status": self.status.value,
            "assessment_date": self.assessment_date.isoformat() if self.assessment_date else None,
            "assessor": self.assessor,
            "findings": self.findings,
            "remediation_actions": self.remediation_actions,
            "is_compliant": self.is_compliant,
            "has_gaps": self.has_gaps,
            "compliance_score": self.compliance_score,
            "mapped_framework_count": self.mapped_framework_count,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def to_qdrant_payload(self) -> Dict[str, Any]:
        """Convert to Qdrant point payload."""
        return {
            "control_id": self.control_id,
            "customer_id": self.customer_id,
            "entity_type": "compliance_control",
            "framework": self.framework.value,
            "control_number": self.control_number,
            "title": self.title,
            "category": self.category.value,
            "status": self.status.value,
            "is_compliant": self.is_compliant,
            "has_gaps": self.has_gaps,
            "compliance_score": self.compliance_score,
            "requirement_count": len(self.requirements),
            "finding_count": len(self.findings),
            "remediation_count": len(self.remediation_actions),
            "mapped_framework_count": self.mapped_framework_count,
        }

    def validate(self) -> bool:
        """Validate control data integrity."""
        try:
            self.__post_init__()
            return True
        except ValueError:
            return False

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "ComplianceControl":
        """Factory method to create ComplianceControl from dictionary."""
        # Convert enum strings to enum values
        if isinstance(data.get("framework"), str):
            data["framework"] = ComplianceFramework(data["framework"])
        if isinstance(data.get("category"), str):
            data["category"] = ControlCategory(data["category"])
        if isinstance(data.get("status"), str):
            data["status"] = ComplianceStatus(data["status"])

        # Convert date strings to date objects
        if isinstance(data.get("assessment_date"), str):
            data["assessment_date"] = date.fromisoformat(data["assessment_date"])
        if isinstance(data.get("created_at"), str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        if isinstance(data.get("updated_at"), str):
            data["updated_at"] = datetime.fromisoformat(data["updated_at"])

        return ComplianceControl(**data)


@dataclass
class ComplianceMapping:
    """
    Compliance Mapping entity.

    Maps controls between different compliance frameworks to show
    equivalence and coverage relationships.
    """
    mapping_id: str
    customer_id: str  # For multi-tenant isolation

    # Source control
    source_framework: ComplianceFramework
    source_control: str  # Control number in source framework

    # Target control
    target_framework: ComplianceFramework
    target_control: str  # Control number in target framework

    # Mapping details
    mapping_strength: float = 1.0  # 0.0-1.0: how closely controls align
    rationale: Optional[str] = None  # Explanation of mapping

    # Verification
    verified_by: Optional[str] = None
    verified_date: Optional[date] = None

    # Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate mapping data on creation."""
        if not self.mapping_id or not self.mapping_id.strip():
            raise ValueError("mapping_id is required")
        if not self.customer_id or not self.customer_id.strip():
            raise ValueError("customer_id is required")
        if not self.source_control or not self.source_control.strip():
            raise ValueError("source_control is required")
        if not self.target_control or not self.target_control.strip():
            raise ValueError("target_control is required")
        if not 0.0 <= self.mapping_strength <= 1.0:
            raise ValueError("mapping_strength must be between 0.0 and 1.0")

        # Normalize values
        self.mapping_id = self.mapping_id.strip()
        self.customer_id = self.customer_id.strip()
        self.source_control = self.source_control.strip()
        self.target_control = self.target_control.strip()

    @property
    def is_verified(self) -> bool:
        """Check if mapping has been verified."""
        return self.verified_by is not None and self.verified_date is not None

    @property
    def is_strong_mapping(self) -> bool:
        """Check if mapping is strong (>= 0.8 alignment)."""
        return self.mapping_strength >= 0.8

    @property
    def mapping_quality_score(self) -> float:
        """Calculate mapping quality score (0.0-10.0)."""
        score = self.mapping_strength * 7.0  # Base score from strength

        # Bonus for verification
        if self.is_verified:
            score += 2.0

        # Bonus for detailed rationale
        if self.rationale and len(self.rationale) > 50:
            score += 1.0

        return min(score, 10.0)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response."""
        return {
            "mapping_id": self.mapping_id,
            "customer_id": self.customer_id,
            "source_framework": self.source_framework.value,
            "source_control": self.source_control,
            "target_framework": self.target_framework.value,
            "target_control": self.target_control,
            "mapping_strength": self.mapping_strength,
            "rationale": self.rationale,
            "verified_by": self.verified_by,
            "verified_date": self.verified_date.isoformat() if self.verified_date else None,
            "is_verified": self.is_verified,
            "is_strong_mapping": self.is_strong_mapping,
            "mapping_quality_score": self.mapping_quality_score,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def to_qdrant_payload(self) -> Dict[str, Any]:
        """Convert to Qdrant point payload."""
        return {
            "mapping_id": self.mapping_id,
            "customer_id": self.customer_id,
            "entity_type": "compliance_mapping",
            "source_framework": self.source_framework.value,
            "source_control": self.source_control,
            "target_framework": self.target_framework.value,
            "target_control": self.target_control,
            "mapping_strength": self.mapping_strength,
            "is_verified": self.is_verified,
            "is_strong_mapping": self.is_strong_mapping,
            "mapping_quality_score": self.mapping_quality_score,
        }

    def validate(self) -> bool:
        """Validate mapping data integrity."""
        try:
            self.__post_init__()
            return True
        except ValueError:
            return False

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "ComplianceMapping":
        """Factory method to create ComplianceMapping from dictionary."""
        # Convert enum strings to enum values
        if isinstance(data.get("source_framework"), str):
            data["source_framework"] = ComplianceFramework(data["source_framework"])
        if isinstance(data.get("target_framework"), str):
            data["target_framework"] = ComplianceFramework(data["target_framework"])

        # Convert date strings to date objects
        if isinstance(data.get("verified_date"), str):
            data["verified_date"] = date.fromisoformat(data["verified_date"])
        if isinstance(data.get("created_at"), str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        if isinstance(data.get("updated_at"), str):
            data["updated_at"] = datetime.fromisoformat(data["updated_at"])

        return ComplianceMapping(**data)


@dataclass
class ComplianceAssessment:
    """
    Compliance Assessment entity.

    Represents a formal assessment of compliance with a specific framework,
    including scope, findings, and overall results.
    """
    assessment_id: str
    customer_id: str  # For multi-tenant isolation
    framework: ComplianceFramework
    assessment_type: AssessmentType

    # Scope
    scope: str  # Description of assessment scope
    start_date: date
    end_date: Optional[date] = None

    # Status
    status: str = "in_progress"  # in_progress, completed, failed

    # Results
    findings_summary: Optional[str] = None
    control_results: Dict[str, str] = field(default_factory=dict)  # {control_id: status}
    overall_score: float = 0.0  # 0.0-100.0 percentage

    # Participants
    assessor: Optional[str] = None
    reviewer: Optional[str] = None

    # Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate assessment data on creation."""
        if not self.assessment_id or not self.assessment_id.strip():
            raise ValueError("assessment_id is required")
        if not self.customer_id or not self.customer_id.strip():
            raise ValueError("customer_id is required")
        if not self.scope or not self.scope.strip():
            raise ValueError("scope is required")
        if not 0.0 <= self.overall_score <= 100.0:
            raise ValueError("overall_score must be between 0.0 and 100.0")

        # Normalize values
        self.assessment_id = self.assessment_id.strip()
        self.customer_id = self.customer_id.strip()
        self.scope = self.scope.strip()

    @property
    def is_completed(self) -> bool:
        """Check if assessment is completed."""
        return self.status == "completed"

    @property
    def duration_days(self) -> Optional[int]:
        """Calculate assessment duration in days."""
        if not self.end_date:
            return (date.today() - self.start_date).days
        return (self.end_date - self.start_date).days

    @property
    def pass_rate(self) -> float:
        """Calculate control pass rate (0.0-100.0)."""
        if not self.control_results:
            return 0.0
        passed = sum(1 for status in self.control_results.values()
                    if status in {"compliant", "not_applicable"})
        return (passed / len(self.control_results)) * 100.0

    @property
    def risk_level(self) -> str:
        """Determine risk level based on overall score."""
        if self.overall_score >= 90.0:
            return "low"
        elif self.overall_score >= 70.0:
            return "medium"
        elif self.overall_score >= 50.0:
            return "high"
        else:
            return "critical"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response."""
        return {
            "assessment_id": self.assessment_id,
            "customer_id": self.customer_id,
            "framework": self.framework.value,
            "assessment_type": self.assessment_type.value,
            "scope": self.scope,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "status": self.status,
            "findings_summary": self.findings_summary,
            "control_results": self.control_results,
            "overall_score": self.overall_score,
            "assessor": self.assessor,
            "reviewer": self.reviewer,
            "is_completed": self.is_completed,
            "duration_days": self.duration_days,
            "pass_rate": self.pass_rate,
            "risk_level": self.risk_level,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def to_qdrant_payload(self) -> Dict[str, Any]:
        """Convert to Qdrant point payload."""
        return {
            "assessment_id": self.assessment_id,
            "customer_id": self.customer_id,
            "entity_type": "compliance_assessment",
            "framework": self.framework.value,
            "assessment_type": self.assessment_type.value,
            "status": self.status,
            "overall_score": self.overall_score,
            "is_completed": self.is_completed,
            "duration_days": self.duration_days,
            "pass_rate": self.pass_rate,
            "risk_level": self.risk_level,
            "control_count": len(self.control_results),
        }

    def validate(self) -> bool:
        """Validate assessment data integrity."""
        try:
            self.__post_init__()
            return True
        except ValueError:
            return False

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "ComplianceAssessment":
        """Factory method to create ComplianceAssessment from dictionary."""
        # Convert enum strings to enum values
        if isinstance(data.get("framework"), str):
            data["framework"] = ComplianceFramework(data["framework"])
        if isinstance(data.get("assessment_type"), str):
            data["assessment_type"] = AssessmentType(data["assessment_type"])

        # Convert date strings to date objects
        if isinstance(data.get("start_date"), str):
            data["start_date"] = date.fromisoformat(data["start_date"])
        if isinstance(data.get("end_date"), str):
            data["end_date"] = date.fromisoformat(data["end_date"])
        if isinstance(data.get("created_at"), str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        if isinstance(data.get("updated_at"), str):
            data["updated_at"] = datetime.fromisoformat(data["updated_at"])

        return ComplianceAssessment(**data)


@dataclass
class ComplianceEvidence:
    """
    Compliance Evidence entity.

    Represents evidence collected to demonstrate compliance with
    specific control requirements.
    """
    evidence_id: str
    customer_id: str  # For multi-tenant isolation
    control_id: str  # Link to ComplianceControl

    # Evidence details
    evidence_type: EvidenceType
    title: str
    description: Optional[str] = None
    file_path: Optional[str] = None  # Storage path for evidence file

    # Timeline
    collected_date: date = field(default_factory=date.today)
    expiry_date: Optional[date] = None  # When evidence becomes stale

    # Verification
    verified: bool = False
    verified_by: Optional[str] = None

    # Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate evidence data on creation."""
        if not self.evidence_id or not self.evidence_id.strip():
            raise ValueError("evidence_id is required")
        if not self.customer_id or not self.customer_id.strip():
            raise ValueError("customer_id is required")
        if not self.control_id or not self.control_id.strip():
            raise ValueError("control_id is required")
        if not self.title or not self.title.strip():
            raise ValueError("title is required")

        # Normalize values
        self.evidence_id = self.evidence_id.strip()
        self.customer_id = self.customer_id.strip()
        self.control_id = self.control_id.strip()
        self.title = self.title.strip()

    @property
    def is_expired(self) -> bool:
        """Check if evidence has expired."""
        if not self.expiry_date:
            return False
        return date.today() > self.expiry_date

    @property
    def days_until_expiry(self) -> Optional[int]:
        """Calculate days until evidence expires."""
        if not self.expiry_date:
            return None
        delta = self.expiry_date - date.today()
        return delta.days

    @property
    def evidence_quality_score(self) -> float:
        """Calculate evidence quality score (0.0-10.0)."""
        score = 5.0  # Base score

        # Verification bonus
        if self.verified:
            score += 3.0

        # Freshness factor
        if not self.is_expired:
            score += 2.0
            if self.days_until_expiry and self.days_until_expiry > 180:
                score += 0.5  # Extra bonus for long-lived evidence

        # Evidence type factor
        if self.evidence_type in {EvidenceType.LOG, EvidenceType.CONFIGURATION}:
            score += 0.5  # Technical evidence slightly preferred

        return min(score, 10.0)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response."""
        return {
            "evidence_id": self.evidence_id,
            "customer_id": self.customer_id,
            "control_id": self.control_id,
            "evidence_type": self.evidence_type.value,
            "title": self.title,
            "description": self.description,
            "file_path": self.file_path,
            "collected_date": self.collected_date.isoformat(),
            "expiry_date": self.expiry_date.isoformat() if self.expiry_date else None,
            "verified": self.verified,
            "verified_by": self.verified_by,
            "is_expired": self.is_expired,
            "days_until_expiry": self.days_until_expiry,
            "evidence_quality_score": self.evidence_quality_score,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def to_qdrant_payload(self) -> Dict[str, Any]:
        """Convert to Qdrant point payload."""
        return {
            "evidence_id": self.evidence_id,
            "customer_id": self.customer_id,
            "entity_type": "compliance_evidence",
            "control_id": self.control_id,
            "evidence_type": self.evidence_type.value,
            "title": self.title,
            "verified": self.verified,
            "is_expired": self.is_expired,
            "days_until_expiry": self.days_until_expiry,
            "evidence_quality_score": self.evidence_quality_score,
        }

    def validate(self) -> bool:
        """Validate evidence data integrity."""
        try:
            self.__post_init__()
            return True
        except ValueError:
            return False

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "ComplianceEvidence":
        """Factory method to create ComplianceEvidence from dictionary."""
        # Convert enum strings to enum values
        if isinstance(data.get("evidence_type"), str):
            data["evidence_type"] = EvidenceType(data["evidence_type"])

        # Convert date strings to date objects
        if isinstance(data.get("collected_date"), str):
            data["collected_date"] = date.fromisoformat(data["collected_date"])
        if isinstance(data.get("expiry_date"), str):
            data["expiry_date"] = date.fromisoformat(data["expiry_date"])
        if isinstance(data.get("created_at"), str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        if isinstance(data.get("updated_at"), str):
            data["updated_at"] = datetime.fromisoformat(data["updated_at"])

        return ComplianceEvidence(**data)


@dataclass
class ComplianceGap:
    """
    Compliance Gap entity.

    Represents an identified gap in compliance with control requirements,
    including severity assessment and remediation planning.
    """
    gap_id: str
    customer_id: str  # For multi-tenant isolation
    framework: ComplianceFramework
    control_id: str  # Link to ComplianceControl

    # Gap details
    gap_description: str
    severity: str = "medium"  # low, medium, high, critical
    impact: Optional[str] = None  # Business impact description
    root_cause: Optional[str] = None

    # Remediation
    remediation_plan: Optional[str] = None
    target_date: Optional[date] = None
    status: str = "open"  # open, in_progress, resolved, accepted_risk
    owner: Optional[str] = None  # Person responsible for remediation

    # Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate gap data on creation."""
        if not self.gap_id or not self.gap_id.strip():
            raise ValueError("gap_id is required")
        if not self.customer_id or not self.customer_id.strip():
            raise ValueError("customer_id is required")
        if not self.control_id or not self.control_id.strip():
            raise ValueError("control_id is required")
        if not self.gap_description or not self.gap_description.strip():
            raise ValueError("gap_description is required")
        if self.severity not in {"low", "medium", "high", "critical"}:
            raise ValueError("severity must be one of: low, medium, high, critical")

        # Normalize values
        self.gap_id = self.gap_id.strip()
        self.customer_id = self.customer_id.strip()
        self.control_id = self.control_id.strip()
        self.gap_description = self.gap_description.strip()

    @property
    def is_resolved(self) -> bool:
        """Check if gap has been resolved."""
        return self.status == "resolved"

    @property
    def is_overdue(self) -> bool:
        """Check if gap remediation is overdue."""
        if not self.target_date or self.is_resolved:
            return False
        return date.today() > self.target_date

    @property
    def days_until_target(self) -> Optional[int]:
        """Calculate days until target remediation date."""
        if not self.target_date:
            return None
        delta = self.target_date - date.today()
        return delta.days

    @property
    def severity_score(self) -> float:
        """Calculate severity score (0.0-10.0)."""
        severity_map = {
            "low": 2.5,
            "medium": 5.0,
            "high": 7.5,
            "critical": 10.0
        }
        base_score = severity_map.get(self.severity, 5.0)

        # Increase score if overdue
        if self.is_overdue:
            base_score = min(base_score + 2.0, 10.0)

        return base_score

    @property
    def risk_priority(self) -> int:
        """Calculate risk priority (1-5, 5 being highest)."""
        # Base priority from severity
        priority_map = {"low": 1, "medium": 2, "high": 4, "critical": 5}
        priority = priority_map.get(self.severity, 2)

        # Increase if overdue
        if self.is_overdue and priority < 5:
            priority += 1

        return priority

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response."""
        return {
            "gap_id": self.gap_id,
            "customer_id": self.customer_id,
            "framework": self.framework.value,
            "control_id": self.control_id,
            "gap_description": self.gap_description,
            "severity": self.severity,
            "impact": self.impact,
            "root_cause": self.root_cause,
            "remediation_plan": self.remediation_plan,
            "target_date": self.target_date.isoformat() if self.target_date else None,
            "status": self.status,
            "owner": self.owner,
            "is_resolved": self.is_resolved,
            "is_overdue": self.is_overdue,
            "days_until_target": self.days_until_target,
            "severity_score": self.severity_score,
            "risk_priority": self.risk_priority,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def to_qdrant_payload(self) -> Dict[str, Any]:
        """Convert to Qdrant point payload."""
        return {
            "gap_id": self.gap_id,
            "customer_id": self.customer_id,
            "entity_type": "compliance_gap",
            "framework": self.framework.value,
            "control_id": self.control_id,
            "severity": self.severity,
            "status": self.status,
            "is_resolved": self.is_resolved,
            "is_overdue": self.is_overdue,
            "days_until_target": self.days_until_target,
            "severity_score": self.severity_score,
            "risk_priority": self.risk_priority,
        }

    def validate(self) -> bool:
        """Validate gap data integrity."""
        try:
            self.__post_init__()
            return True
        except ValueError:
            return False

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "ComplianceGap":
        """Factory method to create ComplianceGap from dictionary."""
        # Convert enum strings to enum values
        if isinstance(data.get("framework"), str):
            data["framework"] = ComplianceFramework(data["framework"])

        # Convert date strings to date objects
        if isinstance(data.get("target_date"), str):
            data["target_date"] = date.fromisoformat(data["target_date"])
        if isinstance(data.get("created_at"), str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        if isinstance(data.get("updated_at"), str):
            data["updated_at"] = datetime.fromisoformat(data["updated_at"])

        return ComplianceGap(**data)
