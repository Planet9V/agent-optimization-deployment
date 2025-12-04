"""
Automated Scanning Models
=========================

Data models for E08: Automated Scanning & Testing API.
Includes ScanProfile, ScanSchedule, ScanJob, ScanFinding, and ScanTarget entities.

Version: 1.0.0
Created: 2025-12-04
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any


# =============================================================================
# Enums for Automated Scanning
# =============================================================================


class ScanType(Enum):
    """Types of security scans."""
    VULNERABILITY = "vulnerability"           # Vulnerability scanning
    CONFIGURATION = "configuration"           # Configuration audit
    COMPLIANCE = "compliance"                 # Compliance checking
    PENETRATION = "penetration"               # Penetration testing
    NETWORK = "network"                       # Network scanning
    WEB_APP = "web_app"                       # Web application testing
    CONTAINER = "container"                   # Container security scanning
    CLOUD = "cloud"                           # Cloud infrastructure scanning


class ScanStatus(Enum):
    """Status of scan jobs."""
    SCHEDULED = "scheduled"       # Waiting to run
    RUNNING = "running"           # Currently executing
    COMPLETED = "completed"       # Finished successfully
    FAILED = "failed"             # Failed with errors
    CANCELLED = "cancelled"       # Manually cancelled
    PAUSED = "paused"             # Temporarily paused


class ScannerType(Enum):
    """Types of scanning tools/engines."""
    NESSUS = "nessus"             # Tenable Nessus
    QUALYS = "qualys"             # Qualys scanner
    RAPID7 = "rapid7"             # Rapid7 InsightVM
    OPENVAS = "openvas"           # OpenVAS open source
    NUCLEI = "nuclei"             # ProjectDiscovery Nuclei
    TRIVY = "trivy"               # Aqua Trivy
    PROWLER = "prowler"           # Prowler cloud scanner
    CUSTOM = "custom"             # Custom scanning tool


class ScanFrequency(Enum):
    """Frequency of scheduled scans."""
    ONCE = "once"                 # One-time scan
    HOURLY = "hourly"             # Every hour
    DAILY = "daily"               # Once per day
    WEEKLY = "weekly"             # Once per week
    MONTHLY = "monthly"           # Once per month
    QUARTERLY = "quarterly"       # Once per quarter


class ScanPriority(Enum):
    """Priority level for scan execution."""
    LOW = "low"                   # Low priority
    MEDIUM = "medium"             # Medium priority
    HIGH = "high"                 # High priority
    CRITICAL = "critical"         # Critical priority


class FindingSeverity(Enum):
    """Severity levels for scan findings."""
    INFO = "info"                 # Informational only
    LOW = "low"                   # Low severity
    MEDIUM = "medium"             # Medium severity
    HIGH = "high"                 # High severity
    CRITICAL = "critical"         # Critical severity


class FindingStatus(Enum):
    """Status of scan findings."""
    NEW = "new"                   # Newly discovered
    CONFIRMED = "confirmed"       # Confirmed as valid
    FALSE_POSITIVE = "false_positive"  # Marked as false positive
    REMEDIATED = "remediated"     # Fixed/remediated
    ACCEPTED = "accepted"         # Accepted as risk


# =============================================================================
# Core Data Models
# =============================================================================


@dataclass
class ScanProfile:
    """
    Scan Profile entity for scan configuration.

    Represents a reusable scanning configuration with scanner settings,
    targets, and execution parameters.
    """
    profile_id: str
    customer_id: str  # For multi-tenant isolation
    name: str

    # Profile configuration
    description: Optional[str] = None
    scan_type: ScanType = ScanType.VULNERABILITY
    scanner_type: ScannerType = ScannerType.OPENVAS

    # Scan configuration
    configuration: Dict[str, Any] = field(default_factory=dict)  # Scanner-specific config
    target_specification: List[str] = field(default_factory=list)  # IP ranges, URLs, etc.

    # Credentials and access
    credentials_required: bool = False
    excluded_checks: List[str] = field(default_factory=list)  # Checks to skip

    # Execution parameters
    timeout_minutes: int = 60
    max_concurrent: int = 5  # Max concurrent scans using this profile

    # Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate scan profile data on creation."""
        if not self.profile_id or not self.profile_id.strip():
            raise ValueError("profile_id is required")
        if not self.customer_id or not self.customer_id.strip():
            raise ValueError("customer_id is required")
        if not self.name or not self.name.strip():
            raise ValueError("name is required")
        if self.timeout_minutes <= 0:
            raise ValueError("timeout_minutes must be positive")
        if self.max_concurrent <= 0:
            raise ValueError("max_concurrent must be positive")

        # Normalize values
        self.profile_id = self.profile_id.strip()
        self.customer_id = self.customer_id.strip()
        self.name = self.name.strip()

    @property
    def has_credentials(self) -> bool:
        """Check if profile requires credentials."""
        return self.credentials_required

    @property
    def target_count(self) -> int:
        """Get number of targets in profile."""
        return len(self.target_specification)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response."""
        return {
            "profile_id": self.profile_id,
            "customer_id": self.customer_id,
            "name": self.name,
            "description": self.description,
            "scan_type": self.scan_type.value,
            "scanner_type": self.scanner_type.value,
            "configuration": self.configuration,
            "target_specification": self.target_specification,
            "credentials_required": self.credentials_required,
            "excluded_checks": self.excluded_checks,
            "timeout_minutes": self.timeout_minutes,
            "max_concurrent": self.max_concurrent,
            "has_credentials": self.has_credentials,
            "target_count": self.target_count,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def to_qdrant_payload(self) -> Dict[str, Any]:
        """Convert to Qdrant point payload."""
        return {
            "profile_id": self.profile_id,
            "customer_id": self.customer_id,
            "name": self.name,
            "entity_type": "scan_profile",
            "scan_type": self.scan_type.value,
            "scanner_type": self.scanner_type.value,
            "credentials_required": self.credentials_required,
            "timeout_minutes": self.timeout_minutes,
            "max_concurrent": self.max_concurrent,
            "target_count": self.target_count,
            "excluded_checks_count": len(self.excluded_checks),
        }

    def validate(self) -> bool:
        """Validate profile configuration."""
        if not self.target_specification:
            return False
        if self.timeout_minutes <= 0 or self.timeout_minutes > 1440:  # Max 24 hours
            return False
        if self.max_concurrent <= 0 or self.max_concurrent > 50:
            return False
        return True

    @classmethod
    def create_default(cls, profile_id: str, customer_id: str, name: str, scan_type: ScanType) -> 'ScanProfile':
        """Factory method to create a default scan profile."""
        return cls(
            profile_id=profile_id,
            customer_id=customer_id,
            name=name,
            scan_type=scan_type,
            scanner_type=ScannerType.OPENVAS,
            timeout_minutes=60,
            max_concurrent=5,
            credentials_required=False,
        )


@dataclass
class ScanSchedule:
    """
    Scan Schedule entity for automated scanning.

    Represents a scheduled scan with recurrence rules and
    execution parameters.
    """
    schedule_id: str
    customer_id: str  # For multi-tenant isolation
    profile_id: str   # Link to ScanProfile
    name: str

    # Schedule configuration
    frequency: ScanFrequency = ScanFrequency.WEEKLY
    next_run: Optional[datetime] = None
    last_run: Optional[datetime] = None
    enabled: bool = True

    # Notifications
    notification_recipients: List[str] = field(default_factory=list)  # Email addresses

    # Execution constraints
    maintenance_window_only: bool = False
    max_duration_minutes: int = 120

    # Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate scan schedule data on creation."""
        if not self.schedule_id or not self.schedule_id.strip():
            raise ValueError("schedule_id is required")
        if not self.customer_id or not self.customer_id.strip():
            raise ValueError("customer_id is required")
        if not self.profile_id or not self.profile_id.strip():
            raise ValueError("profile_id is required")
        if not self.name or not self.name.strip():
            raise ValueError("name is required")
        if self.max_duration_minutes <= 0:
            raise ValueError("max_duration_minutes must be positive")

        # Normalize values
        self.schedule_id = self.schedule_id.strip()
        self.customer_id = self.customer_id.strip()
        self.profile_id = self.profile_id.strip()
        self.name = self.name.strip()

    @property
    def is_due(self) -> bool:
        """Check if schedule is due to run."""
        if not self.enabled or not self.next_run:
            return False
        return datetime.utcnow() >= self.next_run

    @property
    def has_notifications(self) -> bool:
        """Check if schedule has notification recipients."""
        return len(self.notification_recipients) > 0

    @property
    def run_count(self) -> int:
        """Calculate estimated number of runs (approximation)."""
        if not self.last_run or not self.created_at:
            return 0
        days_active = (self.last_run - self.created_at).days
        if self.frequency == ScanFrequency.DAILY:
            return days_active
        elif self.frequency == ScanFrequency.WEEKLY:
            return days_active // 7
        elif self.frequency == ScanFrequency.MONTHLY:
            return days_active // 30
        return 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response."""
        return {
            "schedule_id": self.schedule_id,
            "customer_id": self.customer_id,
            "profile_id": self.profile_id,
            "name": self.name,
            "frequency": self.frequency.value,
            "next_run": self.next_run.isoformat() if self.next_run else None,
            "last_run": self.last_run.isoformat() if self.last_run else None,
            "enabled": self.enabled,
            "notification_recipients": self.notification_recipients,
            "maintenance_window_only": self.maintenance_window_only,
            "max_duration_minutes": self.max_duration_minutes,
            "is_due": self.is_due,
            "has_notifications": self.has_notifications,
            "run_count": self.run_count,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def to_qdrant_payload(self) -> Dict[str, Any]:
        """Convert to Qdrant point payload."""
        return {
            "schedule_id": self.schedule_id,
            "customer_id": self.customer_id,
            "profile_id": self.profile_id,
            "name": self.name,
            "entity_type": "scan_schedule",
            "frequency": self.frequency.value,
            "enabled": self.enabled,
            "maintenance_window_only": self.maintenance_window_only,
            "max_duration_minutes": self.max_duration_minutes,
            "has_notifications": self.has_notifications,
            "notification_count": len(self.notification_recipients),
            "is_due": self.is_due,
        }

    def validate(self) -> bool:
        """Validate schedule configuration."""
        if not self.enabled and self.frequency == ScanFrequency.ONCE:
            return True  # One-time disabled is OK
        if self.enabled and not self.next_run:
            return False
        if self.max_duration_minutes <= 0 or self.max_duration_minutes > 1440:
            return False
        return True

    @classmethod
    def create_default(cls, schedule_id: str, customer_id: str, profile_id: str,
                       name: str, frequency: ScanFrequency) -> 'ScanSchedule':
        """Factory method to create a default scan schedule."""
        return cls(
            schedule_id=schedule_id,
            customer_id=customer_id,
            profile_id=profile_id,
            name=name,
            frequency=frequency,
            enabled=True,
            max_duration_minutes=120,
        )


@dataclass
class ScanJob:
    """
    Scan Job entity for scan execution tracking.

    Represents a single scan execution instance with status,
    progress, and results metadata.
    """
    job_id: str
    customer_id: str  # For multi-tenant isolation
    profile_id: str   # Link to ScanProfile
    schedule_id: Optional[str] = None  # Link to ScanSchedule if scheduled

    # Job status
    status: ScanStatus = ScanStatus.SCHEDULED
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    # Results summary
    targets_scanned: int = 0
    findings_count: int = 0
    findings_by_severity: Dict[str, int] = field(default_factory=dict)  # {'critical': 5, 'high': 12}

    # Progress tracking
    progress_percentage: float = 0.0  # 0.0-100.0

    # Error handling
    error_message: Optional[str] = None
    scan_log: List[str] = field(default_factory=list)  # Log entries

    # Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate scan job data on creation."""
        if not self.job_id or not self.job_id.strip():
            raise ValueError("job_id is required")
        if not self.customer_id or not self.customer_id.strip():
            raise ValueError("customer_id is required")
        if not self.profile_id or not self.profile_id.strip():
            raise ValueError("profile_id is required")
        if not 0.0 <= self.progress_percentage <= 100.0:
            raise ValueError("progress_percentage must be between 0.0 and 100.0")

        # Normalize values
        self.job_id = self.job_id.strip()
        self.customer_id = self.customer_id.strip()
        self.profile_id = self.profile_id.strip()

    @property
    def is_running(self) -> bool:
        """Check if job is currently running."""
        return self.status == ScanStatus.RUNNING

    @property
    def is_complete(self) -> bool:
        """Check if job has completed (successfully or failed)."""
        return self.status in {ScanStatus.COMPLETED, ScanStatus.FAILED, ScanStatus.CANCELLED}

    @property
    def duration_minutes(self) -> Optional[int]:
        """Calculate job duration in minutes."""
        if not self.started_at:
            return None
        end = self.completed_at if self.completed_at else datetime.utcnow()
        return int((end - self.started_at).total_seconds() / 60)

    @property
    def critical_findings(self) -> int:
        """Get count of critical findings."""
        return self.findings_by_severity.get(FindingSeverity.CRITICAL.value, 0)

    @property
    def high_findings(self) -> int:
        """Get count of high severity findings."""
        return self.findings_by_severity.get(FindingSeverity.HIGH.value, 0)

    @property
    def risk_score(self) -> float:
        """Calculate risk score based on findings (0.0-10.0)."""
        score = 0.0

        # Critical findings (0-5 points)
        critical = self.critical_findings
        score += min(critical * 1.0, 5.0)

        # High findings (0-3 points)
        high = self.high_findings
        score += min(high * 0.3, 3.0)

        # Medium findings (0-2 points)
        medium = self.findings_by_severity.get(FindingSeverity.MEDIUM.value, 0)
        score += min(medium * 0.1, 2.0)

        return min(score, 10.0)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response."""
        return {
            "job_id": self.job_id,
            "customer_id": self.customer_id,
            "profile_id": self.profile_id,
            "schedule_id": self.schedule_id,
            "status": self.status.value,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "targets_scanned": self.targets_scanned,
            "findings_count": self.findings_count,
            "findings_by_severity": self.findings_by_severity,
            "progress_percentage": self.progress_percentage,
            "error_message": self.error_message,
            "scan_log": self.scan_log,
            "is_running": self.is_running,
            "is_complete": self.is_complete,
            "duration_minutes": self.duration_minutes,
            "critical_findings": self.critical_findings,
            "high_findings": self.high_findings,
            "risk_score": self.risk_score,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def to_qdrant_payload(self) -> Dict[str, Any]:
        """Convert to Qdrant point payload."""
        return {
            "job_id": self.job_id,
            "customer_id": self.customer_id,
            "profile_id": self.profile_id,
            "schedule_id": self.schedule_id,
            "entity_type": "scan_job",
            "status": self.status.value,
            "targets_scanned": self.targets_scanned,
            "findings_count": self.findings_count,
            "progress_percentage": self.progress_percentage,
            "is_running": self.is_running,
            "is_complete": self.is_complete,
            "critical_findings": self.critical_findings,
            "high_findings": self.high_findings,
            "risk_score": self.risk_score,
            "duration_minutes": self.duration_minutes or 0,
        }

    def validate(self) -> bool:
        """Validate job state."""
        if self.status == ScanStatus.RUNNING and not self.started_at:
            return False
        if self.status in {ScanStatus.COMPLETED, ScanStatus.FAILED} and not self.completed_at:
            return False
        if not 0.0 <= self.progress_percentage <= 100.0:
            return False
        return True

    @classmethod
    def create_new(cls, job_id: str, customer_id: str, profile_id: str,
                   schedule_id: Optional[str] = None) -> 'ScanJob':
        """Factory method to create a new scan job."""
        return cls(
            job_id=job_id,
            customer_id=customer_id,
            profile_id=profile_id,
            schedule_id=schedule_id,
            status=ScanStatus.SCHEDULED,
            progress_percentage=0.0,
        )


@dataclass
class ScanFinding:
    """
    Scan Finding entity for discovered vulnerabilities/issues.

    Represents a single security finding from a scan with
    severity, remediation, and lifecycle tracking.
    """
    finding_id: str
    customer_id: str  # For multi-tenant isolation
    job_id: str       # Link to ScanJob

    # Finding details
    title: str
    description: str
    severity: FindingSeverity = FindingSeverity.MEDIUM

    # Vulnerability details
    cvss_score: Optional[float] = None  # 0.0-10.0 CVSS score
    cve_id: Optional[str] = None        # CVE identifier if applicable

    # Asset information
    affected_asset: str = ""            # Hostname, IP, URL, etc.
    affected_component: Optional[str] = None  # Software/service affected

    # Evidence and remediation
    evidence: List[str] = field(default_factory=list)  # Evidence snippets
    remediation: Optional[str] = None   # Remediation guidance

    # Timeline
    first_detected: datetime = field(default_factory=datetime.utcnow)
    last_detected: datetime = field(default_factory=datetime.utcnow)

    # Status tracking
    status: FindingStatus = FindingStatus.NEW
    false_positive: bool = False

    # Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate scan finding data on creation."""
        if not self.finding_id or not self.finding_id.strip():
            raise ValueError("finding_id is required")
        if not self.customer_id or not self.customer_id.strip():
            raise ValueError("customer_id is required")
        if not self.job_id or not self.job_id.strip():
            raise ValueError("job_id is required")
        if not self.title or not self.title.strip():
            raise ValueError("title is required")
        if not self.description or not self.description.strip():
            raise ValueError("description is required")
        if self.cvss_score is not None and not 0.0 <= self.cvss_score <= 10.0:
            raise ValueError("cvss_score must be between 0.0 and 10.0")

        # Normalize values
        self.finding_id = self.finding_id.strip()
        self.customer_id = self.customer_id.strip()
        self.job_id = self.job_id.strip()
        self.title = self.title.strip()
        self.description = self.description.strip()

    @property
    def is_critical(self) -> bool:
        """Check if finding is critical severity."""
        return self.severity == FindingSeverity.CRITICAL

    @property
    def is_high_severity(self) -> bool:
        """Check if finding is high or critical severity."""
        return self.severity in {FindingSeverity.CRITICAL, FindingSeverity.HIGH}

    @property
    def has_cve(self) -> bool:
        """Check if finding has associated CVE."""
        return self.cve_id is not None and len(self.cve_id) > 0

    @property
    def age_days(self) -> int:
        """Calculate age of finding in days since first detected."""
        return (datetime.utcnow() - self.first_detected).days

    @property
    def is_resolved(self) -> bool:
        """Check if finding is resolved."""
        return self.status in {FindingStatus.REMEDIATED, FindingStatus.FALSE_POSITIVE}

    @property
    def priority_score(self) -> float:
        """Calculate priority score for remediation (0.0-10.0)."""
        score = 0.0

        # Severity factor (0-5 points)
        severity_map = {
            FindingSeverity.CRITICAL: 5.0,
            FindingSeverity.HIGH: 4.0,
            FindingSeverity.MEDIUM: 2.5,
            FindingSeverity.LOW: 1.0,
            FindingSeverity.INFO: 0.0,
        }
        score += severity_map.get(self.severity, 0.0)

        # CVSS score factor (0-3 points)
        if self.cvss_score is not None:
            score += (self.cvss_score / 10.0) * 3.0

        # Age factor (0-2 points) - older unresolved findings get higher priority
        if self.age_days > 90:
            score += 2.0
        elif self.age_days > 30:
            score += 1.0

        return min(score, 10.0)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response."""
        return {
            "finding_id": self.finding_id,
            "customer_id": self.customer_id,
            "job_id": self.job_id,
            "title": self.title,
            "description": self.description,
            "severity": self.severity.value,
            "cvss_score": self.cvss_score,
            "cve_id": self.cve_id,
            "affected_asset": self.affected_asset,
            "affected_component": self.affected_component,
            "evidence": self.evidence,
            "remediation": self.remediation,
            "first_detected": self.first_detected.isoformat(),
            "last_detected": self.last_detected.isoformat(),
            "status": self.status.value,
            "false_positive": self.false_positive,
            "is_critical": self.is_critical,
            "is_high_severity": self.is_high_severity,
            "has_cve": self.has_cve,
            "age_days": self.age_days,
            "is_resolved": self.is_resolved,
            "priority_score": self.priority_score,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def to_qdrant_payload(self) -> Dict[str, Any]:
        """Convert to Qdrant point payload."""
        return {
            "finding_id": self.finding_id,
            "customer_id": self.customer_id,
            "job_id": self.job_id,
            "entity_type": "scan_finding",
            "title": self.title,
            "severity": self.severity.value,
            "cvss_score": self.cvss_score,
            "cve_id": self.cve_id,
            "affected_asset": self.affected_asset,
            "affected_component": self.affected_component,
            "status": self.status.value,
            "false_positive": self.false_positive,
            "is_critical": self.is_critical,
            "is_high_severity": self.is_high_severity,
            "has_cve": self.has_cve,
            "age_days": self.age_days,
            "is_resolved": self.is_resolved,
            "priority_score": self.priority_score,
            "evidence_count": len(self.evidence),
        }

    def validate(self) -> bool:
        """Validate finding data."""
        if not self.title or not self.description:
            return False
        if self.cvss_score is not None and not 0.0 <= self.cvss_score <= 10.0:
            return False
        if self.false_positive and self.status != FindingStatus.FALSE_POSITIVE:
            return False
        return True

    @classmethod
    def create_new(cls, finding_id: str, customer_id: str, job_id: str,
                   title: str, description: str, severity: FindingSeverity,
                   affected_asset: str) -> 'ScanFinding':
        """Factory method to create a new scan finding."""
        return cls(
            finding_id=finding_id,
            customer_id=customer_id,
            job_id=job_id,
            title=title,
            description=description,
            severity=severity,
            affected_asset=affected_asset,
            status=FindingStatus.NEW,
            false_positive=False,
        )


@dataclass
class ScanTarget:
    """
    Scan Target entity for target asset management.

    Represents a scannable target (host, network, application)
    with scanning configuration and history.
    """
    target_id: str
    customer_id: str  # For multi-tenant isolation
    name: str

    # Target specification
    target_type: str  # 'host', 'network', 'web_app', 'container', 'cloud'
    address: str      # IP, CIDR, URL, etc.
    port_range: Optional[str] = None  # '80,443,8080-8090'

    # Credentials
    credentials_id: Optional[str] = None  # Reference to credential store

    # Scanning history
    last_scanned: Optional[datetime] = None
    scan_frequency: ScanFrequency = ScanFrequency.WEEKLY
    enabled: bool = True

    # Metadata
    tags: List[str] = field(default_factory=list)  # ['production', 'dmz', 'critical']
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate scan target data on creation."""
        if not self.target_id or not self.target_id.strip():
            raise ValueError("target_id is required")
        if not self.customer_id or not self.customer_id.strip():
            raise ValueError("customer_id is required")
        if not self.name or not self.name.strip():
            raise ValueError("name is required")
        if not self.target_type or not self.target_type.strip():
            raise ValueError("target_type is required")
        if not self.address or not self.address.strip():
            raise ValueError("address is required")

        # Normalize values
        self.target_id = self.target_id.strip()
        self.customer_id = self.customer_id.strip()
        self.name = self.name.strip()
        self.target_type = self.target_type.strip().lower()
        self.address = self.address.strip()

    @property
    def has_credentials(self) -> bool:
        """Check if target has credentials configured."""
        return self.credentials_id is not None and len(self.credentials_id) > 0

    @property
    def days_since_scan(self) -> Optional[int]:
        """Calculate days since last scan."""
        if not self.last_scanned:
            return None
        return (datetime.utcnow() - self.last_scanned).days

    @property
    def is_overdue(self) -> bool:
        """Check if target is overdue for scanning based on frequency."""
        if not self.enabled or not self.last_scanned:
            return False

        days_since = self.days_since_scan
        if days_since is None:
            return True

        frequency_days = {
            ScanFrequency.HOURLY: 1,
            ScanFrequency.DAILY: 1,
            ScanFrequency.WEEKLY: 7,
            ScanFrequency.MONTHLY: 30,
            ScanFrequency.QUARTERLY: 90,
        }

        threshold = frequency_days.get(self.scan_frequency, 7)
        return days_since > threshold

    @property
    def is_critical(self) -> bool:
        """Check if target is tagged as critical."""
        return 'critical' in [tag.lower() for tag in self.tags]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API response."""
        return {
            "target_id": self.target_id,
            "customer_id": self.customer_id,
            "name": self.name,
            "target_type": self.target_type,
            "address": self.address,
            "port_range": self.port_range,
            "credentials_id": self.credentials_id,
            "last_scanned": self.last_scanned.isoformat() if self.last_scanned else None,
            "scan_frequency": self.scan_frequency.value,
            "enabled": self.enabled,
            "tags": self.tags,
            "has_credentials": self.has_credentials,
            "days_since_scan": self.days_since_scan,
            "is_overdue": self.is_overdue,
            "is_critical": self.is_critical,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def to_qdrant_payload(self) -> Dict[str, Any]:
        """Convert to Qdrant point payload."""
        return {
            "target_id": self.target_id,
            "customer_id": self.customer_id,
            "name": self.name,
            "entity_type": "scan_target",
            "target_type": self.target_type,
            "address": self.address,
            "scan_frequency": self.scan_frequency.value,
            "enabled": self.enabled,
            "tags": self.tags,
            "has_credentials": self.has_credentials,
            "days_since_scan": self.days_since_scan or -1,
            "is_overdue": self.is_overdue,
            "is_critical": self.is_critical,
        }

    def validate(self) -> bool:
        """Validate target configuration."""
        if not self.target_type or not self.address:
            return False
        valid_types = {'host', 'network', 'web_app', 'container', 'cloud'}
        if self.target_type not in valid_types:
            return False
        return True

    @classmethod
    def create_new(cls, target_id: str, customer_id: str, name: str,
                   target_type: str, address: str) -> 'ScanTarget':
        """Factory method to create a new scan target."""
        return cls(
            target_id=target_id,
            customer_id=customer_id,
            name=name,
            target_type=target_type,
            address=address,
            scan_frequency=ScanFrequency.WEEKLY,
            enabled=True,
        )
