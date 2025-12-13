"""
SBOM Analysis Service
=====================

Service layer for E03: SBOM Dependency & Vulnerability Tracking.
Provides CRUD operations, dependency analysis, and vulnerability correlation
with customer isolation and Qdrant vector storage.

Version: 1.0.0
Created: 2025-12-04
"""

from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional, List, Dict, Any, Tuple, Set
from uuid import uuid4
import logging

from qdrant_client import QdrantClient
from api.database_manager import get_qdrant_client
from qdrant_client.models import (
    Filter,
    FieldCondition,
    MatchAny,
    MatchValue,
    Range,
    PointStruct,
    VectorParams,
    Distance,
)

from ..customer_isolation import CustomerContext, CustomerContextManager

from .sbom_models import (
    SoftwareComponent,
    SBOM,
    SoftwareVulnerability,
    DependencyRelation,
    LicenseComplianceResult,
    DependencyGraphNode,
    SBOMFormat,
    ComponentType,
    LicenseType,
    LicenseRisk,
    DependencyType,
    DependencyScope,
    VulnerabilitySeverity,
    ExploitMaturity,
    RemediationType,
    ComponentStatus,
)

logger = logging.getLogger(__name__)


# =============================================================================
# Search Request/Response Models
# =============================================================================


@dataclass
class ComponentSearchRequest:
    """Request parameters for component search."""
    query: Optional[str] = None
    customer_id: Optional[str] = None
    sbom_id: Optional[str] = None
    component_type: Optional[ComponentType] = None
    license_risk: Optional[LicenseRisk] = None
    has_vulnerabilities: Optional[bool] = None
    min_cvss: Optional[float] = None
    status: Optional[ComponentStatus] = None
    limit: int = 20
    include_system: bool = True


@dataclass
class ComponentSearchResult:
    """Single component search result."""
    component: SoftwareComponent
    score: float = 0.0
    match_reason: Optional[str] = None


@dataclass
class VulnerabilitySearchRequest:
    """Request parameters for vulnerability search."""
    query: Optional[str] = None
    customer_id: Optional[str] = None
    component_id: Optional[str] = None
    min_cvss: Optional[float] = None
    severity: Optional[VulnerabilitySeverity] = None
    exploit_available: Optional[bool] = None
    cisa_kev: Optional[bool] = None
    has_fix: Optional[bool] = None
    limit: int = 50
    include_system: bool = True


@dataclass
class VulnerabilitySearchResult:
    """Single vulnerability search result."""
    vulnerability: SoftwareVulnerability
    score: float = 0.0


@dataclass
class SBOMSearchRequest:
    """Request parameters for SBOM search."""
    query: Optional[str] = None
    customer_id: Optional[str] = None
    format: Optional[SBOMFormat] = None
    has_vulnerabilities: Optional[bool] = None
    target_system_id: Optional[str] = None
    limit: int = 20
    include_system: bool = True


@dataclass
class SBOMSearchResult:
    """Single SBOM search result."""
    sbom: SBOM
    score: float = 0.0


@dataclass
class DependencyPath:
    """Path in dependency graph."""
    path: List[str]  # Component IDs
    path_names: List[str]  # Component names
    depth: int
    has_vulnerabilities: bool = False
    max_cvss_in_path: float = 0.0


@dataclass
class ImpactAnalysis:
    """Impact analysis result for a component."""
    component_id: str
    component_name: str
    direct_dependents: int
    total_dependents: int  # Including transitive
    affected_sboms: List[str]
    vulnerability_exposure: int  # Components affected by this component's vulns


@dataclass
class RiskSummary:
    """Risk summary for an SBOM or component."""
    total_components: int
    vulnerable_components: int
    critical_vulns: int
    high_vulns: int
    medium_vulns: int
    low_vulns: int
    license_risks: Dict[str, int]  # {risk_level: count}
    exploitable_vulns: int
    cisa_kev_vulns: int
    avg_cvss: float


# =============================================================================
# SBOM Analysis Service
# =============================================================================


class SBOMAnalysisService:
    """
    Service for SBOM dependency and vulnerability analysis.

    Provides customer-isolated operations for:
    - SBOM import and management
    - Software component tracking
    - Dependency graph analysis
    - Vulnerability correlation and alerting
    - License compliance checking
    """

    COLLECTION_NAME = "ner11_sbom"
    VECTOR_SIZE = 384  # sentence-transformers/all-MiniLM-L6-v2

    def __init__(
        self,
        qdrant_url: str = "http://openspg-qdrant:6333",
        neo4j_driver: Optional[Any] = None,
        embedding_service: Optional[Any] = None,
    ):
        """
        Initialize SBOM analysis service.

        Args:
            qdrant_url: Qdrant server URL
            neo4j_driver: Neo4j driver instance (optional)
            embedding_service: EmbeddingService instance for semantic search
        """
        self.qdrant_client = get_qdrant_client()
        self.neo4j_driver = neo4j_driver
        self._embedding_service = embedding_service
        self._ensure_collection()

    def _ensure_collection(self) -> None:
        """Ensure Qdrant collection exists."""
        try:
            self.qdrant_client.get_collection(self.COLLECTION_NAME)
            logger.info(f"Collection {self.COLLECTION_NAME} exists")
        except Exception:
            logger.info(f"Creating collection {self.COLLECTION_NAME}")
            self.qdrant_client.create_collection(
                collection_name=self.COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=self.VECTOR_SIZE,
                    distance=Distance.COSINE,
                ),
            )

    def _get_customer_context(self) -> CustomerContext:
        """Get required customer context."""
        return CustomerContextManager.require_context()

    def _build_customer_filter(
        self,
        customer_id: str,
        include_system: bool = True,
        additional_conditions: Optional[List[FieldCondition]] = None,
    ) -> Filter:
        """Build Qdrant filter with customer isolation."""
        customer_ids = [customer_id]
        if include_system:
            customer_ids.append("SYSTEM")

        conditions = [
            FieldCondition(
                key="customer_id",
                match=MatchAny(any=customer_ids),
            )
        ]

        if additional_conditions:
            conditions.extend(additional_conditions)

        return Filter(must=conditions)

    def _generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for text using embedding service."""
        if self._embedding_service is not None:
            return self._embedding_service.encode(text)
        # Return zero vector if no model (for testing)
        return [0.0] * self.VECTOR_SIZE

    def _generate_point_id(self) -> str:
        """Generate unique point ID."""
        return str(uuid4())

    # =========================================================================
    # SBOM Operations
    # =========================================================================

    def create_sbom(self, sbom: SBOM) -> SBOM:
        """Create a new SBOM with customer isolation."""
        context = self._get_customer_context()

        if not context.can_write():
            raise PermissionError("Write access required to create SBOM")

        if sbom.customer_id != context.customer_id:
            raise ValueError("SBOM customer_id must match context customer_id")

        # Generate embedding from SBOM name and metadata
        embed_text = f"{sbom.name} {sbom.target_application or ''} {sbom.description or ''}"
        embedding = self._generate_embedding(embed_text)

        # Store in Qdrant
        point_id = self._generate_point_id()
        self.qdrant_client.upsert(
            collection_name=self.COLLECTION_NAME,
            points=[
                PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload=sbom.to_qdrant_payload(),
                )
            ],
        )

        logger.info(f"Created SBOM {sbom.sbom_id} for customer {sbom.customer_id}")
        return sbom

    def get_sbom(self, sbom_id: str) -> Optional[SBOM]:
        """Get SBOM by ID with customer isolation."""
        context = self._get_customer_context()

        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(key="sbom_id", match=MatchValue(value=sbom_id)),
                    FieldCondition(
                        key="customer_id",
                        match=MatchAny(any=context.get_customer_ids()),
                    ),
                    FieldCondition(key="entity_type", match=MatchValue(value="sbom")),
                ]
            ),
            limit=1,
        )

        if results[0]:
            payload = results[0][0].payload
            return self._payload_to_sbom(payload)
        return None

    def _payload_to_sbom(self, payload: Dict[str, Any]) -> SBOM:
        """Convert Qdrant payload to SBOM object."""
        return SBOM(
            sbom_id=payload["sbom_id"],
            customer_id=payload["customer_id"],
            name=payload["name"],
            format=SBOMFormat(payload.get("format", "cyclonedx")),
            format_version=payload.get("format_version", "1.5"),
            total_components=payload.get("total_components", 0),
            direct_dependencies=payload.get("direct_dependencies", 0),
            transitive_dependencies=payload.get("transitive_dependencies", 0),
            total_vulnerabilities=payload.get("total_vulnerabilities", 0),
            critical_count=payload.get("critical_count", 0),
            high_count=payload.get("high_count", 0),
            target_system_id=payload.get("target_system_id"),
            generator_tool=payload.get("generator_tool"),
            is_valid=payload.get("is_valid", True),
        )

    def list_sboms(
        self,
        customer_id: Optional[str] = None,
        format: Optional[SBOMFormat] = None,
        limit: int = 100,
    ) -> List[SBOM]:
        """List SBOMs with optional filters."""
        context = self._get_customer_context()
        customer_id = customer_id or context.customer_id

        conditions = [
            FieldCondition(key="entity_type", match=MatchValue(value="sbom"))
        ]

        if format:
            conditions.append(
                FieldCondition(key="format", match=MatchValue(value=format.value))
            )

        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=self._build_customer_filter(customer_id, additional_conditions=conditions),
            limit=limit,
        )

        sboms = []
        for point in results[0]:
            sboms.append(self._payload_to_sbom(point.payload))
        return sboms

    def delete_sbom(self, sbom_id: str) -> bool:
        """Delete SBOM and all associated components."""
        context = self._get_customer_context()

        if not context.can_write():
            raise PermissionError("Write access required to delete SBOM")

        # Delete SBOM
        self.qdrant_client.delete(
            collection_name=self.COLLECTION_NAME,
            points_selector=Filter(
                must=[
                    FieldCondition(key="sbom_id", match=MatchValue(value=sbom_id)),
                    FieldCondition(key="customer_id", match=MatchValue(value=context.customer_id)),
                ]
            ),
        )

        logger.info(f"Deleted SBOM {sbom_id} and associated entities")
        return True

    # =========================================================================
    # Component Operations
    # =========================================================================

    def create_component(self, component: SoftwareComponent) -> SoftwareComponent:
        """Create a new software component with customer isolation."""
        context = self._get_customer_context()

        if not context.can_write():
            raise PermissionError("Write access required to create component")

        if component.customer_id != context.customer_id:
            raise ValueError("Component customer_id must match context customer_id")

        # Generate embedding from component name and metadata
        embed_text = f"{component.name} {component.version} {component.group or ''} {component.description or ''}"
        embedding = self._generate_embedding(embed_text)

        # Store in Qdrant
        point_id = self._generate_point_id()
        self.qdrant_client.upsert(
            collection_name=self.COLLECTION_NAME,
            points=[
                PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload=component.to_qdrant_payload(),
                )
            ],
        )

        logger.info(f"Created component {component.component_id}: {component.name}@{component.version}")
        return component

    def get_component(self, component_id: str) -> Optional[SoftwareComponent]:
        """Get component by ID with customer isolation."""
        context = self._get_customer_context()

        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(key="component_id", match=MatchValue(value=component_id)),
                    FieldCondition(
                        key="customer_id",
                        match=MatchAny(any=context.get_customer_ids()),
                    ),
                    FieldCondition(key="entity_type", match=MatchValue(value="software_component")),
                ]
            ),
            limit=1,
        )

        if results[0]:
            payload = results[0][0].payload
            return self._payload_to_component(payload)
        return None

    def _payload_to_component(self, payload: Dict[str, Any]) -> SoftwareComponent:
        """Convert Qdrant payload to SoftwareComponent object."""
        return SoftwareComponent(
            component_id=payload["component_id"],
            customer_id=payload["customer_id"],
            name=payload["name"],
            version=payload["version"],
            purl=payload.get("purl"),
            cpe=payload.get("cpe"),
            component_type=ComponentType(payload.get("component_type", "library")),
            group=payload.get("group"),
            license_type=LicenseType(payload.get("license_type", "unknown")),
            license_risk=LicenseRisk(payload.get("license_risk", "low")),
            vulnerability_count=payload.get("vulnerability_count", 0),
            critical_vuln_count=payload.get("critical_vuln_count", 0),
            high_vuln_count=payload.get("high_vuln_count", 0),
            max_cvss_score=payload.get("max_cvss_score", 0.0),
            epss_score=payload.get("epss_score"),
            status=ComponentStatus(payload.get("status", "active")),
            sbom_id=payload.get("sbom_id"),
        )

    def search_components(self, request: ComponentSearchRequest) -> List[ComponentSearchResult]:
        """Search components with filters and optional semantic search."""
        context = self._get_customer_context()
        customer_id = request.customer_id or context.customer_id

        conditions = [
            FieldCondition(key="entity_type", match=MatchValue(value="software_component"))
        ]

        if request.sbom_id:
            conditions.append(
                FieldCondition(key="sbom_id", match=MatchValue(value=request.sbom_id))
            )

        if request.component_type:
            conditions.append(
                FieldCondition(key="component_type", match=MatchValue(value=request.component_type.value))
            )

        if request.license_risk:
            conditions.append(
                FieldCondition(key="license_risk", match=MatchValue(value=request.license_risk.value))
            )

        if request.has_vulnerabilities is not None:
            if request.has_vulnerabilities:
                conditions.append(
                    FieldCondition(key="vulnerability_count", range=Range(gte=1))
                )
            else:
                conditions.append(
                    FieldCondition(key="vulnerability_count", match=MatchValue(value=0))
                )

        if request.min_cvss is not None:
            conditions.append(
                FieldCondition(key="max_cvss_score", range=Range(gte=request.min_cvss))
            )

        if request.status:
            conditions.append(
                FieldCondition(key="status", match=MatchValue(value=request.status.value))
            )

        search_filter = self._build_customer_filter(
            customer_id,
            include_system=request.include_system,
            additional_conditions=conditions,
        )

        # Semantic search if query provided
        if request.query:
            query_embedding = self._generate_embedding(request.query)
            results = self.qdrant_client.search(
                collection_name=self.COLLECTION_NAME,
                query_vector=query_embedding,
                query_filter=search_filter,
                limit=request.limit,
            )
            return [
                ComponentSearchResult(
                    component=self._payload_to_component(result.payload),
                    score=result.score,
                    match_reason="semantic_search",
                )
                for result in results
            ]
        else:
            # Filter-only search
            results = self.qdrant_client.scroll(
                collection_name=self.COLLECTION_NAME,
                scroll_filter=search_filter,
                limit=request.limit,
            )
            return [
                ComponentSearchResult(
                    component=self._payload_to_component(point.payload),
                    score=1.0,
                    match_reason="filter_match",
                )
                for point in results[0]
            ]

    def get_components_by_sbom(self, sbom_id: str) -> List[SoftwareComponent]:
        """Get all components for an SBOM."""
        context = self._get_customer_context()

        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(key="sbom_id", match=MatchValue(value=sbom_id)),
                    FieldCondition(
                        key="customer_id",
                        match=MatchAny(any=context.get_customer_ids()),
                    ),
                    FieldCondition(key="entity_type", match=MatchValue(value="software_component")),
                ]
            ),
            limit=10000,  # Large limit for complete component list
        )

        return [self._payload_to_component(point.payload) for point in results[0]]

    def get_vulnerable_components(
        self,
        customer_id: Optional[str] = None,
        min_cvss: float = 0.0,
        limit: int = 100,
    ) -> List[SoftwareComponent]:
        """Get components with vulnerabilities above CVSS threshold."""
        context = self._get_customer_context()
        customer_id = customer_id or context.customer_id

        conditions = [
            FieldCondition(key="entity_type", match=MatchValue(value="software_component")),
            FieldCondition(key="vulnerability_count", range=Range(gte=1)),
        ]

        if min_cvss > 0:
            conditions.append(
                FieldCondition(key="max_cvss_score", range=Range(gte=min_cvss))
            )

        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=self._build_customer_filter(customer_id, additional_conditions=conditions),
            limit=limit,
        )

        return [self._payload_to_component(point.payload) for point in results[0]]

    def get_high_risk_components(self, customer_id: Optional[str] = None) -> List[SoftwareComponent]:
        """Get components with critical/high vulnerabilities or license risks."""
        context = self._get_customer_context()
        customer_id = customer_id or context.customer_id

        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=self._build_customer_filter(
                customer_id,
                additional_conditions=[
                    FieldCondition(key="entity_type", match=MatchValue(value="software_component")),
                    FieldCondition(key="is_high_risk", match=MatchValue(value=True)),
                ]
            ),
            limit=500,
        )

        return [self._payload_to_component(point.payload) for point in results[0]]

    # =========================================================================
    # Vulnerability Operations
    # =========================================================================

    def create_vulnerability(self, vulnerability: SoftwareVulnerability) -> SoftwareVulnerability:
        """Create a new vulnerability record."""
        context = self._get_customer_context()

        if not context.can_write():
            raise PermissionError("Write access required to create vulnerability")

        if vulnerability.customer_id != context.customer_id:
            raise ValueError("Vulnerability customer_id must match context customer_id")

        # Generate embedding from CVE description
        embed_text = f"{vulnerability.cve_id} {vulnerability.component_name} {vulnerability.description or ''}"
        embedding = self._generate_embedding(embed_text)

        # Store in Qdrant
        point_id = self._generate_point_id()
        self.qdrant_client.upsert(
            collection_name=self.COLLECTION_NAME,
            points=[
                PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload=vulnerability.to_qdrant_payload(),
                )
            ],
        )

        logger.info(f"Created vulnerability {vulnerability.cve_id} for component {vulnerability.component_id}")
        return vulnerability

    def get_vulnerability(self, vulnerability_id: str) -> Optional[SoftwareVulnerability]:
        """Get vulnerability by ID."""
        context = self._get_customer_context()

        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(key="vulnerability_id", match=MatchValue(value=vulnerability_id)),
                    FieldCondition(
                        key="customer_id",
                        match=MatchAny(any=context.get_customer_ids()),
                    ),
                    FieldCondition(key="entity_type", match=MatchValue(value="software_vulnerability")),
                ]
            ),
            limit=1,
        )

        if results[0]:
            payload = results[0][0].payload
            return self._payload_to_vulnerability(payload)
        return None

    def _payload_to_vulnerability(self, payload: Dict[str, Any]) -> SoftwareVulnerability:
        """Convert Qdrant payload to SoftwareVulnerability object."""
        return SoftwareVulnerability(
            vulnerability_id=payload["vulnerability_id"],
            customer_id=payload["customer_id"],
            cve_id=payload["cve_id"],
            component_id=payload["component_id"],
            component_name=payload.get("component_name", ""),
            component_version=payload.get("component_version", ""),
            severity=VulnerabilitySeverity(payload.get("severity", "medium")),
            cvss_v3_score=payload.get("cvss_v3_score", 0.0),
            epss_score=payload.get("epss_score"),
            exploit_maturity=ExploitMaturity(payload.get("exploit_maturity", "not_defined")),
            exploit_available=payload.get("exploit_available", False),
            in_the_wild=payload.get("in_the_wild", False),
            cisa_kev=payload.get("cisa_kev", False),
            remediation_type=RemediationType(payload.get("remediation_type", "no_fix")),
            apt_groups=payload.get("apt_groups", []),
            cwe_ids=payload.get("cwe_ids", []),
        )

    def search_vulnerabilities(self, request: VulnerabilitySearchRequest) -> List[VulnerabilitySearchResult]:
        """Search vulnerabilities with filters."""
        context = self._get_customer_context()
        customer_id = request.customer_id or context.customer_id

        conditions = [
            FieldCondition(key="entity_type", match=MatchValue(value="software_vulnerability"))
        ]

        if request.component_id:
            conditions.append(
                FieldCondition(key="component_id", match=MatchValue(value=request.component_id))
            )

        if request.min_cvss is not None:
            conditions.append(
                FieldCondition(key="cvss_v3_score", range=Range(gte=request.min_cvss))
            )

        if request.severity:
            conditions.append(
                FieldCondition(key="severity", match=MatchValue(value=request.severity.value))
            )

        if request.exploit_available is not None:
            conditions.append(
                FieldCondition(key="exploit_available", match=MatchValue(value=request.exploit_available))
            )

        if request.cisa_kev is not None:
            conditions.append(
                FieldCondition(key="cisa_kev", match=MatchValue(value=request.cisa_kev))
            )

        if request.has_fix is not None:
            conditions.append(
                FieldCondition(key="has_fix", match=MatchValue(value=request.has_fix))
            )

        search_filter = self._build_customer_filter(
            customer_id,
            include_system=request.include_system,
            additional_conditions=conditions,
        )

        if request.query:
            query_embedding = self._generate_embedding(request.query)
            results = self.qdrant_client.search(
                collection_name=self.COLLECTION_NAME,
                query_vector=query_embedding,
                query_filter=search_filter,
                limit=request.limit,
            )
            return [
                VulnerabilitySearchResult(
                    vulnerability=self._payload_to_vulnerability(result.payload),
                    score=result.score,
                )
                for result in results
            ]
        else:
            results = self.qdrant_client.scroll(
                collection_name=self.COLLECTION_NAME,
                scroll_filter=search_filter,
                limit=request.limit,
            )
            return [
                VulnerabilitySearchResult(
                    vulnerability=self._payload_to_vulnerability(point.payload),
                    score=1.0,
                )
                for point in results[0]
            ]

    def get_vulnerabilities_by_component(self, component_id: str) -> List[SoftwareVulnerability]:
        """Get all vulnerabilities for a component."""
        context = self._get_customer_context()

        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(key="component_id", match=MatchValue(value=component_id)),
                    FieldCondition(
                        key="customer_id",
                        match=MatchAny(any=context.get_customer_ids()),
                    ),
                    FieldCondition(key="entity_type", match=MatchValue(value="software_vulnerability")),
                ]
            ),
            limit=1000,
        )

        return [self._payload_to_vulnerability(point.payload) for point in results[0]]

    def get_critical_vulnerabilities(self, customer_id: Optional[str] = None) -> List[SoftwareVulnerability]:
        """Get all critical vulnerabilities (CISA KEV, in-the-wild, or CVSS >= 9.0)."""
        context = self._get_customer_context()
        customer_id = customer_id or context.customer_id

        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=self._build_customer_filter(
                customer_id,
                additional_conditions=[
                    FieldCondition(key="entity_type", match=MatchValue(value="software_vulnerability")),
                    FieldCondition(key="is_critical", match=MatchValue(value=True)),
                ]
            ),
            limit=500,
        )

        return [self._payload_to_vulnerability(point.payload) for point in results[0]]

    def get_vulnerabilities_by_apt(self, apt_group: str) -> List[SoftwareVulnerability]:
        """Get vulnerabilities associated with an APT group."""
        context = self._get_customer_context()

        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(
                        key="customer_id",
                        match=MatchAny(any=context.get_customer_ids()),
                    ),
                    FieldCondition(key="entity_type", match=MatchValue(value="software_vulnerability")),
                    FieldCondition(key="apt_groups", match=MatchAny(any=[apt_group])),
                ]
            ),
            limit=500,
        )

        return [self._payload_to_vulnerability(point.payload) for point in results[0]]

    # =========================================================================
    # Dependency Relation Operations
    # =========================================================================

    def create_dependency(self, relation: DependencyRelation) -> DependencyRelation:
        """Create a dependency relationship."""
        context = self._get_customer_context()

        if not context.can_write():
            raise PermissionError("Write access required to create dependency")

        if relation.customer_id != context.customer_id:
            raise ValueError("Relation customer_id must match context customer_id")

        # Generate embedding from relationship
        embed_text = f"{relation.source_component_name} depends on {relation.target_component_name}"
        embedding = self._generate_embedding(embed_text)

        # Store in Qdrant
        point_id = self._generate_point_id()
        self.qdrant_client.upsert(
            collection_name=self.COLLECTION_NAME,
            points=[
                PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload=relation.to_qdrant_payload(),
                )
            ],
        )

        logger.info(f"Created dependency {relation.source_component_name} -> {relation.target_component_name}")
        return relation

    def get_dependencies(self, component_id: str) -> List[DependencyRelation]:
        """Get all dependencies of a component (what it depends on)."""
        context = self._get_customer_context()

        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(key="source_component_id", match=MatchValue(value=component_id)),
                    FieldCondition(
                        key="customer_id",
                        match=MatchAny(any=context.get_customer_ids()),
                    ),
                    FieldCondition(key="entity_type", match=MatchValue(value="dependency_relation")),
                ]
            ),
            limit=1000,
        )

        return [self._payload_to_relation(point.payload) for point in results[0]]

    def get_dependents(self, component_id: str) -> List[DependencyRelation]:
        """Get all dependents of a component (what depends on it)."""
        context = self._get_customer_context()

        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(key="target_component_id", match=MatchValue(value=component_id)),
                    FieldCondition(
                        key="customer_id",
                        match=MatchAny(any=context.get_customer_ids()),
                    ),
                    FieldCondition(key="entity_type", match=MatchValue(value="dependency_relation")),
                ]
            ),
            limit=1000,
        )

        return [self._payload_to_relation(point.payload) for point in results[0]]

    def _payload_to_relation(self, payload: Dict[str, Any]) -> DependencyRelation:
        """Convert Qdrant payload to DependencyRelation object."""
        return DependencyRelation(
            relation_id=payload["relation_id"],
            customer_id=payload["customer_id"],
            source_component_id=payload["source_component_id"],
            source_component_name=payload.get("source_component_name", ""),
            source_version=payload.get("source_version", ""),
            target_component_id=payload["target_component_id"],
            target_component_name=payload.get("target_component_name", ""),
            target_version=payload.get("target_version", ""),
            dependency_type=DependencyType(payload.get("dependency_type", "direct")),
            scope=DependencyScope(payload.get("scope", "runtime")),
            depth=payload.get("depth", 1),
            is_optional=payload.get("is_optional", False),
            is_dev_dependency=payload.get("is_dev_dependency", False),
            sbom_id=payload.get("sbom_id"),
            propagates_vulnerabilities=payload.get("propagates_vulnerabilities", True),
        )

    # =========================================================================
    # Analytics & Risk Summary
    # =========================================================================

    def get_sbom_risk_summary(self, sbom_id: str) -> RiskSummary:
        """Get comprehensive risk summary for an SBOM."""
        components = self.get_components_by_sbom(sbom_id)

        total = len(components)
        vulnerable = sum(1 for c in components if c.vulnerability_count > 0)
        critical = sum(c.critical_vuln_count for c in components)
        high = sum(c.high_vuln_count for c in components)
        medium = sum(c.medium_vuln_count for c in components)
        low = sum(c.low_vuln_count for c in components)

        license_risks = {}
        for c in components:
            risk = c.license_risk.value
            license_risks[risk] = license_risks.get(risk, 0) + 1

        # Get vulnerabilities for exploitable/kev counts
        vulns = []
        for c in components:
            vulns.extend(self.get_vulnerabilities_by_component(c.component_id))

        exploitable = sum(1 for v in vulns if v.is_exploitable)
        kev = sum(1 for v in vulns if v.cisa_kev)
        avg_cvss = sum(v.cvss_v3_score for v in vulns) / len(vulns) if vulns else 0.0

        return RiskSummary(
            total_components=total,
            vulnerable_components=vulnerable,
            critical_vulns=critical,
            high_vulns=high,
            medium_vulns=medium,
            low_vulns=low,
            license_risks=license_risks,
            exploitable_vulns=exploitable,
            cisa_kev_vulns=kev,
            avg_cvss=round(avg_cvss, 2),
        )

    def get_license_compliance(
        self,
        sbom_id: str,
        allowed_licenses: Optional[List[str]] = None,
        denied_licenses: Optional[List[str]] = None,
    ) -> LicenseComplianceResult:
        """Analyze license compliance for an SBOM."""
        components = self.get_components_by_sbom(sbom_id)
        context = self._get_customer_context()

        # Default permissive allowlist
        if allowed_licenses is None:
            allowed_licenses = ["mit", "apache-2.0", "bsd-2-clause", "bsd-3-clause", "isc"]

        if denied_licenses is None:
            denied_licenses = ["gpl-2.0", "gpl-3.0", "agpl-3.0"]

        compliant = 0
        non_compliant = 0
        unknown = 0
        copyleft_violations = []
        license_conflicts = []
        unknown_licenses = []

        risk_counts = {"low": 0, "medium": 0, "high": 0, "critical": 0}

        for c in components:
            license_val = c.license_type.value

            if license_val == "unknown":
                unknown += 1
                unknown_licenses.append(c.name)
            elif license_val in denied_licenses:
                non_compliant += 1
                copyleft_violations.append({
                    "component": c.name,
                    "version": c.version,
                    "license": license_val,
                    "risk": "copyleft_required",
                })
            elif license_val in allowed_licenses:
                compliant += 1
            else:
                # Not explicitly allowed or denied
                compliant += 1

            risk_counts[c.license_risk.value] = risk_counts.get(c.license_risk.value, 0) + 1

        is_compliant = non_compliant == 0 and unknown < (len(components) * 0.1)

        return LicenseComplianceResult(
            result_id=f"LIC-{uuid4().hex[:8].upper()}",
            customer_id=context.customer_id,
            sbom_id=sbom_id,
            is_compliant=is_compliant,
            total_components=len(components),
            compliant_count=compliant,
            non_compliant_count=non_compliant,
            unknown_count=unknown,
            low_risk_count=risk_counts["low"],
            medium_risk_count=risk_counts["medium"],
            high_risk_count=risk_counts["high"],
            critical_risk_count=risk_counts["critical"],
            copyleft_violations=copyleft_violations,
            license_conflicts=license_conflicts,
            unknown_licenses=unknown_licenses,
            allowed_licenses=allowed_licenses,
            denied_licenses=denied_licenses,
        )

    def get_dashboard_summary(self, customer_id: Optional[str] = None) -> Dict[str, Any]:
        """Get comprehensive dashboard summary for customer."""
        context = self._get_customer_context()
        customer_id = customer_id or context.customer_id

        sboms = self.list_sboms(customer_id=customer_id)
        high_risk_components = self.get_high_risk_components(customer_id=customer_id)
        critical_vulns = self.get_critical_vulnerabilities(customer_id=customer_id)

        total_components = sum(s.total_components for s in sboms)
        total_vulns = sum(s.total_vulnerabilities for s in sboms)

        return {
            "summary": {
                "total_sboms": len(sboms),
                "total_components": total_components,
                "total_vulnerabilities": total_vulns,
                "high_risk_components": len(high_risk_components),
                "critical_vulnerabilities": len(critical_vulns),
            },
            "sboms_by_format": self._count_by_field(sboms, "format"),
            "vulnerability_breakdown": {
                "critical": sum(s.critical_count for s in sboms),
                "high": sum(s.high_count for s in sboms),
                "medium": sum(s.medium_count for s in sboms),
                "low": sum(s.low_count for s in sboms),
            },
            "critical_alerts": [
                {
                    "cve_id": v.cve_id,
                    "cvss_score": v.cvss_v3_score,
                    "component": v.component_name,
                    "cisa_kev": v.cisa_kev,
                    "in_the_wild": v.in_the_wild,
                }
                for v in critical_vulns[:10]
            ],
        }

    def _count_by_field(self, items: List, field: str) -> Dict[str, int]:
        """Count items by field value."""
        counts = {}
        for item in items:
            val = getattr(item, field)
            if hasattr(val, "value"):
                val = val.value
            counts[val] = counts.get(val, 0) + 1
        return counts

    # =========================================================================
    # Day 3: Dependency Graph Analysis
    # =========================================================================

    def build_dependency_tree(
        self,
        component_id: str,
        max_depth: int = 10,
        include_dev: bool = False,
    ) -> DependencyGraphNode:
        """
        Build a dependency tree starting from a component.

        Args:
            component_id: Root component ID
            max_depth: Maximum tree depth to traverse
            include_dev: Include dev dependencies

        Returns:
            DependencyGraphNode with nested children
        """
        visited: Dict[str, DependencyGraphNode] = {}
        return self._build_tree_recursive(component_id, 0, max_depth, include_dev, visited)

    def _build_tree_recursive(
        self,
        component_id: str,
        current_depth: int,
        max_depth: int,
        include_dev: bool,
        visited: Dict[str, DependencyGraphNode],
    ) -> DependencyGraphNode:
        """Recursively build dependency tree."""
        # Prevent infinite recursion
        if component_id in visited:
            existing = visited[component_id]
            return DependencyGraphNode(
                component_id=existing.component_id,
                component_name=existing.component_name,
                version=existing.version,
                depth=current_depth,
                children=[],  # Don't recurse into already-visited
                is_circular=True,
                vulnerability_count=existing.vulnerability_count,
                max_severity=existing.max_severity,
            )

        # Get component details
        component = self.get_component(component_id)
        if not component:
            return DependencyGraphNode(
                component_id=component_id,
                component_name="unknown",
                version="unknown",
                depth=current_depth,
                children=[],
            )

        # Create node
        node = DependencyGraphNode(
            component_id=component_id,
            component_name=component.name,
            version=component.version,
            depth=current_depth,
            children=[],
            dependencies_count=0,
            dependents_count=0,
            vulnerability_count=component.vulnerability_count,
            max_severity=component.max_cvss_score,
            is_circular=False,
            sbom_id=component.sbom_id,
        )

        visited[component_id] = node

        # Stop at max depth
        if current_depth >= max_depth:
            return node

        # Get dependencies
        deps = self.get_dependencies(component_id)
        if not include_dev:
            deps = [d for d in deps if not d.is_dev_dependency]

        node.dependencies_count = len(deps)

        # Recursively build children
        for dep in deps:
            child = self._build_tree_recursive(
                dep.target_component_id,
                current_depth + 1,
                max_depth,
                include_dev,
                visited,
            )
            node.children.append(child)

        return node

    def get_transitive_closure(
        self,
        component_id: str,
        direction: str = "dependencies",  # or "dependents"
        max_depth: int = 50,
    ) -> List[str]:
        """
        Get all transitive dependencies or dependents of a component.

        Args:
            component_id: Starting component ID
            direction: "dependencies" (what it needs) or "dependents" (what needs it)
            max_depth: Maximum traversal depth

        Returns:
            List of all component IDs in transitive closure
        """
        visited: set = set()
        to_visit: List[Tuple[str, int]] = [(component_id, 0)]

        while to_visit:
            current_id, depth = to_visit.pop(0)

            if current_id in visited or depth > max_depth:
                continue

            visited.add(current_id)

            # Get next level based on direction
            if direction == "dependencies":
                relations = self.get_dependencies(current_id)
                next_ids = [r.target_component_id for r in relations]
            else:  # dependents
                relations = self.get_dependents(current_id)
                next_ids = [r.source_component_id for r in relations]

            for next_id in next_ids:
                if next_id not in visited:
                    to_visit.append((next_id, depth + 1))

        # Remove starting component from result
        visited.discard(component_id)
        return list(visited)

    def get_impact_analysis(self, component_id: str) -> ImpactAnalysis:
        """
        Analyze the impact if a component has a vulnerability.

        Calculates how many other components would be affected.

        Args:
            component_id: Component to analyze

        Returns:
            ImpactAnalysis with metrics
        """
        component = self.get_component(component_id)
        if not component:
            return ImpactAnalysis(
                component_id=component_id,
                component_name="unknown",
                direct_dependents=0,
                total_dependents=0,
                affected_sboms=[],
                vulnerability_exposure=0,
            )

        # Get direct dependents
        direct_deps = self.get_dependents(component_id)
        direct_count = len(direct_deps)

        # Get transitive dependents
        all_dependents = self.get_transitive_closure(component_id, direction="dependents")
        total_count = len(all_dependents)

        # Find affected SBOMs
        affected_sbom_ids = set()
        for dep_id in all_dependents:
            dep = self.get_component(dep_id)
            if dep and dep.sbom_id:
                affected_sbom_ids.add(dep.sbom_id)
        if component.sbom_id:
            affected_sbom_ids.add(component.sbom_id)

        # Calculate vulnerability exposure (components affected by this one's vulns)
        exposure = total_count if component.vulnerability_count > 0 else 0

        return ImpactAnalysis(
            component_id=component_id,
            component_name=component.name,
            direct_dependents=direct_count,
            total_dependents=total_count,
            affected_sboms=list(affected_sbom_ids),
            vulnerability_exposure=exposure,
        )

    def detect_cycles(self, sbom_id: str) -> List[List[str]]:
        """
        Detect circular dependencies in an SBOM.

        Args:
            sbom_id: SBOM to analyze

        Returns:
            List of cycles, each cycle is a list of component IDs
        """
        components = self.get_components_by_sbom(sbom_id)
        component_ids = {c.component_id for c in components}

        cycles: List[List[str]] = []
        visited: set = set()
        rec_stack: set = set()

        def dfs(node_id: str, path: List[str]) -> None:
            if node_id in rec_stack:
                # Found cycle - extract it
                cycle_start = path.index(node_id)
                cycle = path[cycle_start:] + [node_id]
                cycles.append(cycle)
                return

            if node_id in visited:
                return

            visited.add(node_id)
            rec_stack.add(node_id)
            path.append(node_id)

            # Get dependencies within this SBOM
            deps = self.get_dependencies(node_id)
            for dep in deps:
                if dep.target_component_id in component_ids:
                    dfs(dep.target_component_id, path.copy())

            rec_stack.remove(node_id)

        # Run DFS from each unvisited node
        for comp in components:
            if comp.component_id not in visited:
                dfs(comp.component_id, [])

        return cycles

    def find_shortest_path(
        self,
        source_id: str,
        target_id: str,
    ) -> Optional[DependencyPath]:
        """
        Find shortest dependency path between two components.

        Args:
            source_id: Starting component ID
            target_id: Target component ID

        Returns:
            DependencyPath if path exists, None otherwise
        """
        if source_id == target_id:
            component = self.get_component(source_id)
            return DependencyPath(
                path=[source_id],
                path_names=[component.name if component else "unknown"],
                depth=0,
                has_vulnerabilities=component.vulnerability_count > 0 if component else False,
                max_cvss_in_path=component.max_cvss_score if component else 0.0,
            )

        # BFS for shortest path
        visited: set = set()
        queue: List[Tuple[str, List[str]]] = [(source_id, [source_id])]

        while queue:
            current_id, path = queue.pop(0)

            if current_id in visited:
                continue
            visited.add(current_id)

            deps = self.get_dependencies(current_id)
            for dep in deps:
                target = dep.target_component_id
                new_path = path + [target]

                if target == target_id:
                    # Found path - build result
                    path_names = []
                    has_vulns = False
                    max_cvss = 0.0

                    for comp_id in new_path:
                        comp = self.get_component(comp_id)
                        if comp:
                            path_names.append(comp.name)
                            if comp.vulnerability_count > 0:
                                has_vulns = True
                            max_cvss = max(max_cvss, comp.max_cvss_score)
                        else:
                            path_names.append("unknown")

                    return DependencyPath(
                        path=new_path,
                        path_names=path_names,
                        depth=len(new_path) - 1,
                        has_vulnerabilities=has_vulns,
                        max_cvss_in_path=max_cvss,
                    )

                if target not in visited:
                    queue.append((target, new_path))

        return None  # No path found

    def get_dependency_depth_analysis(self, sbom_id: str) -> Dict[str, Any]:
        """
        Analyze dependency depth distribution for an SBOM.

        Returns:
            Analysis with depth statistics and deep dependencies
        """
        components = self.get_components_by_sbom(sbom_id)
        depth_counts: Dict[int, int] = {}
        deepest_chains: List[Dict] = []

        for comp in components:
            tree = self.build_dependency_tree(comp.component_id, max_depth=20)
            max_depth = self._get_max_depth(tree)

            depth_counts[max_depth] = depth_counts.get(max_depth, 0) + 1

            if max_depth >= 5:  # Track deep dependency chains
                deepest_chains.append({
                    "component": comp.name,
                    "version": comp.version,
                    "max_depth": max_depth,
                    "vulnerability_count": comp.vulnerability_count,
                })

        # Sort deepest chains
        deepest_chains.sort(key=lambda x: x["max_depth"], reverse=True)

        return {
            "sbom_id": sbom_id,
            "total_components": len(components),
            "depth_distribution": depth_counts,
            "avg_depth": sum(k * v for k, v in depth_counts.items()) / len(components) if components else 0,
            "max_depth": max(depth_counts.keys()) if depth_counts else 0,
            "deep_dependencies": deepest_chains[:10],  # Top 10 deepest
        }

    def _get_max_depth(self, node: DependencyGraphNode) -> int:
        """Get maximum depth in a dependency tree."""
        if not node.children:
            return 0
        return 1 + max(self._get_max_depth(child) for child in node.children)

    def get_vulnerable_paths(
        self,
        sbom_id: str,
        min_cvss: float = 7.0,
    ) -> List[Dict[str, Any]]:
        """
        Find all paths to vulnerable components in an SBOM.

        Args:
            sbom_id: SBOM to analyze
            min_cvss: Minimum CVSS score to consider

        Returns:
            List of vulnerable paths with details
        """
        vulnerable_components = self.get_vulnerable_components(min_cvss=min_cvss)
        vuln_in_sbom = [c for c in vulnerable_components if c.sbom_id == sbom_id]

        # Get root components (no dependents within SBOM)
        components = self.get_components_by_sbom(sbom_id)
        component_ids = {c.component_id for c in components}

        roots = []
        for comp in components:
            dependents = self.get_dependents(comp.component_id)
            # Check if any dependents are within this SBOM
            internal_dependents = [d for d in dependents if d.source_component_id in component_ids]
            if not internal_dependents:
                roots.append(comp)

        # Find paths from roots to vulnerable components
        vulnerable_paths = []
        for root in roots:
            for vuln_comp in vuln_in_sbom:
                path = self.find_shortest_path(root.component_id, vuln_comp.component_id)
                if path:
                    vulnerable_paths.append({
                        "root_component": root.name,
                        "vulnerable_component": vuln_comp.name,
                        "path": path.path_names,
                        "depth": path.depth,
                        "max_cvss": vuln_comp.max_cvss_score,
                        "vulnerability_count": vuln_comp.vulnerability_count,
                    })

        return vulnerable_paths

    def get_dependency_graph_stats(self, sbom_id: str) -> Dict[str, Any]:
        """
        Get comprehensive dependency graph statistics for an SBOM.

        Returns:
            Graph statistics including connectivity, density, and risk metrics
        """
        components = self.get_components_by_sbom(sbom_id)
        component_ids = {c.component_id for c in components}

        total_edges = 0
        in_degree: Dict[str, int] = {c.component_id: 0 for c in components}
        out_degree: Dict[str, int] = {c.component_id: 0 for c in components}

        for comp in components:
            deps = self.get_dependencies(comp.component_id)
            internal_deps = [d for d in deps if d.target_component_id in component_ids]
            total_edges += len(internal_deps)
            out_degree[comp.component_id] = len(internal_deps)

            for dep in internal_deps:
                in_degree[dep.target_component_id] += 1

        n = len(components)
        max_edges = n * (n - 1) if n > 1 else 1

        # Find root nodes (in_degree == 0) and leaf nodes (out_degree == 0)
        roots = [cid for cid, deg in in_degree.items() if deg == 0]
        leaves = [cid for cid, deg in out_degree.items() if deg == 0]

        # Vulnerability propagation risk
        vuln_components = [c for c in components if c.vulnerability_count > 0]
        vuln_reachable = 0
        for vc in vuln_components:
            dependents = self.get_transitive_closure(vc.component_id, direction="dependents")
            vuln_reachable += len([d for d in dependents if d in component_ids])

        cycles = self.detect_cycles(sbom_id)

        return {
            "sbom_id": sbom_id,
            "total_nodes": n,
            "total_edges": total_edges,
            "graph_density": total_edges / max_edges if max_edges > 0 else 0,
            "root_nodes": len(roots),
            "leaf_nodes": len(leaves),
            "avg_in_degree": sum(in_degree.values()) / n if n > 0 else 0,
            "avg_out_degree": sum(out_degree.values()) / n if n > 0 else 0,
            "max_in_degree": max(in_degree.values()) if in_degree else 0,
            "max_out_degree": max(out_degree.values()) if out_degree else 0,
            "vulnerable_components": len(vuln_components),
            "vulnerability_reachability": vuln_reachable,
            "circular_dependencies": len(cycles),
            "cycles": cycles[:5],  # First 5 cycles
        }

    # =========================================================================
    # Day 4: Vulnerability Correlation
    # =========================================================================

    def match_cve_to_component(
        self,
        cve_id: str,
        component_id: str,
        cvss_score: float,
        description: str = "",
        exploit_available: bool = False,
        cisa_kev: bool = False,
        epss_score: Optional[float] = None,
        apt_groups: Optional[List[str]] = None,
        fixed_version: Optional[str] = None,
    ) -> SoftwareVulnerability:
        """
        Match a CVE to a component and create the vulnerability record.

        Args:
            cve_id: CVE identifier (e.g., "CVE-2023-12345")
            component_id: Component the CVE affects
            cvss_score: CVSS v3 score
            description: CVE description
            exploit_available: Whether exploit code exists
            cisa_kev: Is in CISA Known Exploited Vulnerabilities
            epss_score: EPSS score (0.0-1.0)
            apt_groups: APT groups known to exploit
            fixed_version: Version that fixes the vulnerability

        Returns:
            Created SoftwareVulnerability record
        """
        context = self._get_customer_context()
        component = self.get_component(component_id)

        if not component:
            raise ValueError(f"Component {component_id} not found")

        # Determine severity from CVSS
        severity = self._cvss_to_severity(cvss_score)

        # Determine exploit maturity
        exploit_maturity = ExploitMaturity.NOT_DEFINED
        if cisa_kev:
            exploit_maturity = ExploitMaturity.WEAPONIZED
        elif exploit_available:
            exploit_maturity = ExploitMaturity.FUNCTIONAL

        # Determine remediation type
        remediation_type = RemediationType.NO_FIX
        if fixed_version:
            remediation_type = RemediationType.UPGRADE

        vuln = SoftwareVulnerability(
            vulnerability_id=f"VULN-{uuid4().hex[:8].upper()}",
            customer_id=context.customer_id,
            cve_id=cve_id,
            component_id=component_id,
            component_name=component.name,
            component_version=component.version,
            severity=severity,
            cvss_v3_score=cvss_score,
            description=description,
            epss_score=epss_score,
            exploit_maturity=exploit_maturity,
            exploit_available=exploit_available,
            in_the_wild=cisa_kev,  # CISA KEV implies in-the-wild
            cisa_kev=cisa_kev,
            remediation_type=remediation_type,
            fixed_version=fixed_version,
            apt_groups=apt_groups or [],
            sbom_id=component.sbom_id,
        )

        return self.create_vulnerability(vuln)

    def _cvss_to_severity(self, cvss_score: float) -> VulnerabilitySeverity:
        """Convert CVSS score to severity enum."""
        if cvss_score == 0.0:
            return VulnerabilitySeverity.NONE
        elif cvss_score < 4.0:
            return VulnerabilitySeverity.LOW
        elif cvss_score < 7.0:
            return VulnerabilitySeverity.MEDIUM
        elif cvss_score < 9.0:
            return VulnerabilitySeverity.HIGH
        else:
            return VulnerabilitySeverity.CRITICAL

    def bulk_match_cves(
        self,
        cve_matches: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Bulk match CVEs to components.

        Args:
            cve_matches: List of dicts with cve_id, component_id, cvss_score, etc.

        Returns:
            Summary with created_count, failed_count, errors
        """
        created = []
        errors = []

        for match in cve_matches:
            try:
                vuln = self.match_cve_to_component(
                    cve_id=match["cve_id"],
                    component_id=match["component_id"],
                    cvss_score=match.get("cvss_score", 5.0),
                    description=match.get("description", ""),
                    exploit_available=match.get("exploit_available", False),
                    cisa_kev=match.get("cisa_kev", False),
                    epss_score=match.get("epss_score"),
                    apt_groups=match.get("apt_groups"),
                    fixed_version=match.get("fixed_version"),
                )
                created.append(vuln.vulnerability_id)
            except Exception as e:
                errors.append({
                    "cve_id": match.get("cve_id"),
                    "component_id": match.get("component_id"),
                    "error": str(e),
                })

        return {
            "created_count": len(created),
            "failed_count": len(errors),
            "created_ids": created,
            "errors": errors,
        }

    def get_epss_prioritized_vulns(
        self,
        min_epss: float = 0.1,
        limit: int = 50,
    ) -> List[SoftwareVulnerability]:
        """
        Get vulnerabilities prioritized by EPSS score (exploit probability).

        High EPSS + any CVSS = higher priority than low EPSS + high CVSS.

        Args:
            min_epss: Minimum EPSS score (0.0-1.0)
            limit: Max results

        Returns:
            Vulnerabilities sorted by EPSS descending
        """
        context = self._get_customer_context()

        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=self._build_customer_filter(
                context.customer_id,
                additional_conditions=[
                    FieldCondition(key="entity_type", match=MatchValue(value="software_vulnerability")),
                    FieldCondition(key="epss_score", range=Range(gte=min_epss)),
                ]
            ),
            limit=limit * 2,  # Get more to allow sorting
        )

        vulns = [self._payload_to_vulnerability(p.payload) for p in results[0]]
        # Sort by EPSS descending
        vulns.sort(key=lambda v: v.epss_score or 0.0, reverse=True)
        return vulns[:limit]

    def get_kev_vulnerabilities(self) -> List[SoftwareVulnerability]:
        """
        Get all CISA Known Exploited Vulnerabilities (KEV).

        These are highest priority - actively exploited in the wild.

        Returns:
            All KEV vulnerabilities for the customer
        """
        context = self._get_customer_context()

        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=self._build_customer_filter(
                context.customer_id,
                additional_conditions=[
                    FieldCondition(key="entity_type", match=MatchValue(value="software_vulnerability")),
                    FieldCondition(key="cisa_kev", match=MatchValue(value=True)),
                ]
            ),
            limit=1000,
        )

        return [self._payload_to_vulnerability(p.payload) for p in results[0]]

    def get_exploitable_vulnerabilities(
        self,
        maturity_level: Optional[ExploitMaturity] = None,
    ) -> List[SoftwareVulnerability]:
        """
        Get vulnerabilities with known exploits.

        Args:
            maturity_level: Optional filter by exploit maturity level

        Returns:
            Exploitable vulnerabilities
        """
        context = self._get_customer_context()

        conditions = [
            FieldCondition(key="entity_type", match=MatchValue(value="software_vulnerability")),
            FieldCondition(key="exploit_available", match=MatchValue(value=True)),
        ]

        if maturity_level:
            conditions.append(
                FieldCondition(key="exploit_maturity", match=MatchValue(value=maturity_level.value))
            )

        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=self._build_customer_filter(
                context.customer_id,
                additional_conditions=conditions,
            ),
            limit=500,
        )

        return [self._payload_to_vulnerability(p.payload) for p in results[0]]

    def get_apt_vulnerability_report(self) -> Dict[str, Any]:
        """
        Get vulnerability report grouped by APT groups.

        Returns:
            Report with APT groups and their associated vulnerabilities
        """
        context = self._get_customer_context()

        # Get all vulnerabilities with APT groups
        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=self._build_customer_filter(
                context.customer_id,
                additional_conditions=[
                    FieldCondition(key="entity_type", match=MatchValue(value="software_vulnerability")),
                ]
            ),
            limit=1000,
        )

        vulns = [self._payload_to_vulnerability(p.payload) for p in results[0]]

        # Group by APT groups
        apt_map: Dict[str, List[Dict]] = {}
        for v in vulns:
            for apt in v.apt_groups:
                if apt not in apt_map:
                    apt_map[apt] = []
                apt_map[apt].append({
                    "cve_id": v.cve_id,
                    "cvss_score": v.cvss_v3_score,
                    "component": v.component_name,
                    "cisa_kev": v.cisa_kev,
                    "exploit_available": v.exploit_available,
                })

        # Build report
        apt_summary = []
        for apt, cves in sorted(apt_map.items(), key=lambda x: len(x[1]), reverse=True):
            apt_summary.append({
                "apt_group": apt,
                "vulnerability_count": len(cves),
                "max_cvss": max(c["cvss_score"] for c in cves),
                "kev_count": sum(1 for c in cves if c["cisa_kev"]),
                "cves": cves[:10],  # Top 10 CVEs per group
            })

        return {
            "total_apt_groups": len(apt_map),
            "total_apt_linked_vulns": sum(len(cves) for cves in apt_map.values()),
            "apt_groups": apt_summary,
        }

    def correlate_vulns_with_equipment(
        self,
        sbom_id: str,
        equipment_id: str,
    ) -> Dict[str, Any]:
        """
        Correlate SBOM vulnerabilities with E15 equipment.

        Links software vulnerabilities to physical equipment for
        prioritization based on equipment criticality.

        Args:
            sbom_id: SBOM ID
            equipment_id: E15 Equipment ID

        Returns:
            Correlation report with risk summary
        """
        context = self._get_customer_context()
        components = self.get_components_by_sbom(sbom_id)

        all_vulns = []
        for comp in components:
            vulns = self.get_vulnerabilities_by_component(comp.component_id)
            all_vulns.extend(vulns)

        critical_count = sum(1 for v in all_vulns if v.severity == VulnerabilitySeverity.CRITICAL)
        high_count = sum(1 for v in all_vulns if v.severity == VulnerabilitySeverity.HIGH)
        kev_count = sum(1 for v in all_vulns if v.cisa_kev)
        exploitable_count = sum(1 for v in all_vulns if v.exploit_available)

        return {
            "sbom_id": sbom_id,
            "equipment_id": equipment_id,
            "total_components": len(components),
            "total_vulnerabilities": len(all_vulns),
            "risk_summary": {
                "critical_vulns": critical_count,
                "high_vulns": high_count,
                "kev_vulns": kev_count,
                "exploitable_vulns": exploitable_count,
            },
            "priority_vulns": [
                {
                    "cve_id": v.cve_id,
                    "cvss_score": v.cvss_v3_score,
                    "component": v.component_name,
                    "cisa_kev": v.cisa_kev,
                    "epss_score": v.epss_score,
                }
                for v in sorted(all_vulns, key=lambda x: x.cvss_v3_score, reverse=True)[:10]
            ],
        }

    def get_vulnerability_timeline(
        self,
        sbom_id: Optional[str] = None,
        days_back: int = 90,
    ) -> List[Dict[str, Any]]:
        """
        Get vulnerability discovery timeline.

        Args:
            sbom_id: Optional SBOM filter
            days_back: Number of days to look back

        Returns:
            Timeline of vulnerability discoveries
        """
        context = self._get_customer_context()
        from datetime import timedelta

        cutoff_date = datetime.now() - timedelta(days=days_back)

        conditions = [
            FieldCondition(key="entity_type", match=MatchValue(value="software_vulnerability")),
        ]

        if sbom_id:
            conditions.append(
                FieldCondition(key="sbom_id", match=MatchValue(value=sbom_id))
            )

        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=self._build_customer_filter(
                context.customer_id,
                additional_conditions=conditions,
            ),
            limit=1000,
        )

        vulns = [self._payload_to_vulnerability(p.payload) for p in results[0]]

        # Group by discovery date (or published date)
        timeline: Dict[str, List[Dict]] = {}
        for v in vulns:
            if v.published_date:
                date_str = v.published_date.strftime("%Y-%m-%d") if isinstance(v.published_date, datetime) else str(v.published_date)
            else:
                date_str = "unknown"

            if date_str not in timeline:
                timeline[date_str] = []
            timeline[date_str].append({
                "cve_id": v.cve_id,
                "cvss_score": v.cvss_v3_score,
                "severity": v.severity.value,
                "component": v.component_name,
            })

        # Convert to sorted list
        return [
            {
                "date": date_str,
                "count": len(cves),
                "max_cvss": max(c["cvss_score"] for c in cves) if cves else 0,
                "vulnerabilities": cves,
            }
            for date_str, cves in sorted(timeline.items(), reverse=True)
        ]

    def acknowledge_vulnerability(
        self,
        vulnerability_id: str,
        acknowledged_by: str,
        notes: str = "",
        risk_accepted: bool = False,
    ) -> bool:
        """
        Acknowledge a vulnerability (mark as reviewed).

        Args:
            vulnerability_id: Vulnerability to acknowledge
            acknowledged_by: Who acknowledged it
            notes: Optional notes
            risk_accepted: Whether the risk is formally accepted

        Returns:
            True if successful
        """
        context = self._get_customer_context()

        if not context.can_write():
            raise PermissionError("Write access required")

        # Find the vulnerability point
        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(key="vulnerability_id", match=MatchValue(value=vulnerability_id)),
                    FieldCondition(key="customer_id", match=MatchValue(value=context.customer_id)),
                    FieldCondition(key="entity_type", match=MatchValue(value="software_vulnerability")),
                ]
            ),
            limit=1,
            with_payload=True,
            with_vectors=True,
        )

        if not results[0]:
            raise ValueError(f"Vulnerability {vulnerability_id} not found")

        point = results[0][0]
        payload = dict(point.payload)
        payload["is_acknowledged"] = True
        payload["acknowledged_by"] = acknowledged_by
        payload["acknowledged_date"] = datetime.now().isoformat()
        payload["acknowledgement_notes"] = notes
        payload["risk_accepted"] = risk_accepted

        # Update the point
        self.qdrant_client.upsert(
            collection_name=self.COLLECTION_NAME,
            points=[
                PointStruct(
                    id=point.id,
                    vector=point.vector,
                    payload=payload,
                )
            ],
        )

        logger.info(f"Acknowledged vulnerability {vulnerability_id} by {acknowledged_by}")
        return True

    def get_remediation_report(self, sbom_id: str) -> Dict[str, Any]:
        """
        Generate remediation report for an SBOM.

        Groups vulnerabilities by remediation type and provides
        upgrade recommendations.

        Args:
            sbom_id: SBOM to analyze

        Returns:
            Remediation report with actionable recommendations
        """
        components = self.get_components_by_sbom(sbom_id)

        upgrades_available = []
        no_fix_available = []
        workarounds = []

        for comp in components:
            vulns = self.get_vulnerabilities_by_component(comp.component_id)

            for v in vulns:
                vuln_info = {
                    "cve_id": v.cve_id,
                    "cvss_score": v.cvss_v3_score,
                    "component": v.component_name,
                    "current_version": v.component_version,
                    "fixed_version": v.fixed_version,
                    "cisa_kev": v.cisa_kev,
                }

                if v.remediation_type == RemediationType.UPGRADE and v.fixed_version:
                    upgrades_available.append(vuln_info)
                elif v.remediation_type == RemediationType.WORKAROUND:
                    vuln_info["workaround"] = v.workaround_description
                    workarounds.append(vuln_info)
                else:
                    no_fix_available.append(vuln_info)

        # Sort by CVSS
        upgrades_available.sort(key=lambda x: x["cvss_score"], reverse=True)
        no_fix_available.sort(key=lambda x: x["cvss_score"], reverse=True)

        return {
            "sbom_id": sbom_id,
            "summary": {
                "total_vulnerabilities": len(upgrades_available) + len(no_fix_available) + len(workarounds),
                "upgrades_available": len(upgrades_available),
                "no_fix_available": len(no_fix_available),
                "workarounds_available": len(workarounds),
            },
            "priority_upgrades": upgrades_available[:20],
            "no_fix_vulns": no_fix_available[:20],
            "workarounds": workarounds[:10],
            "recommendations": self._generate_remediation_recommendations(
                upgrades_available, no_fix_available
            ),
        }

    def _generate_remediation_recommendations(
        self,
        upgrades: List[Dict],
        no_fix: List[Dict],
    ) -> List[str]:
        """Generate prioritized remediation recommendations."""
        recommendations = []

        # KEV vulnerabilities first
        kev_upgrades = [u for u in upgrades if u.get("cisa_kev")]
        if kev_upgrades:
            recommendations.append(
                f"CRITICAL: {len(kev_upgrades)} CISA KEV vulnerabilities have fixes available. "
                "These are actively exploited and should be patched immediately."
            )

        # Critical CVSS with upgrades
        critical_upgrades = [u for u in upgrades if u["cvss_score"] >= 9.0 and not u.get("cisa_kev")]
        if critical_upgrades:
            recommendations.append(
                f"HIGH PRIORITY: {len(critical_upgrades)} critical vulnerabilities (CVSS >= 9.0) "
                "have fixes available."
            )

        # No fix available
        no_fix_critical = [n for n in no_fix if n["cvss_score"] >= 9.0]
        if no_fix_critical:
            recommendations.append(
                f"RISK ACCEPTANCE NEEDED: {len(no_fix_critical)} critical vulnerabilities "
                "have no fix available. Consider compensating controls or component replacement."
            )

        return recommendations
