"""
Vendor Equipment Service
========================

Service layer for E15: Vendor Equipment Lifecycle Management.
Provides CRUD operations and lifecycle queries with customer isolation.
Includes semantic search with sentence-transformer embeddings.

Version: 1.1.0
Created: 2025-12-04
Updated: 2025-12-04 - Added EmbeddingService integration
"""

from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional, List, Dict, Any, Tuple
from uuid import uuid4
import logging

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Filter,
    FieldCondition,
    MatchAny,
    MatchValue,
    Range,
    PointStruct,
    VectorParams,
    Distance,
    CollectionInfo,
)

from ..customer_isolation import CustomerContext, CustomerContextManager

from .vendor_models import (
    Vendor,
    EquipmentModel,
    SupportContract,
    VendorRiskLevel,
    SupportStatus,
    LifecycleStatus,
)
from .embedding_service import EmbeddingService, get_embedding_service

logger = logging.getLogger(__name__)


@dataclass
class SemanticSearchResult:
    """Result from semantic similarity search."""
    entity_id: str
    entity_type: str
    name: str
    score: float
    payload: Dict[str, Any]


@dataclass
class SimilarityMatch:
    """Equipment or vendor similarity match."""
    source_id: str
    match_id: str
    match_name: str
    similarity_score: float
    match_type: str  # "vendor" or "equipment"


@dataclass
class CVERecord:
    """CVE vulnerability record."""
    cve_id: str
    cvss_score: float
    severity: str  # critical, high, medium, low
    description: str
    affected_vendor_id: str
    affected_equipment_ids: List[str]
    published_date: Optional[date] = None
    customer_id: str = "SYSTEM"  # CVEs are typically system-wide
    flagged_at: Optional[datetime] = None

    def __post_init__(self):
        if self.flagged_at is None:
            self.flagged_at = datetime.utcnow()
        # Calculate severity from CVSS
        if not self.severity:
            if self.cvss_score >= 9.0:
                self.severity = "critical"
            elif self.cvss_score >= 7.0:
                self.severity = "high"
            elif self.cvss_score >= 4.0:
                self.severity = "medium"
            else:
                self.severity = "low"

    def to_qdrant_payload(self) -> Dict[str, Any]:
        """Convert to Qdrant payload."""
        return {
            "cve_id": self.cve_id,
            "cvss_score": self.cvss_score,
            "severity": self.severity,
            "description": self.description,
            "affected_vendor_id": self.affected_vendor_id,
            "affected_equipment_ids": self.affected_equipment_ids,
            "published_date": self.published_date.isoformat() if self.published_date else None,
            "customer_id": self.customer_id,
            "flagged_at": self.flagged_at.isoformat() if self.flagged_at else None,
            "entity_type": "cve",
        }


@dataclass
class VulnerabilityAlert:
    """Alert for supply chain vulnerability."""
    cve_id: str
    vendor_id: str
    vendor_name: str
    cvss_score: float
    severity: str
    affected_equipment_count: int
    critical_equipment_affected: int
    recommendation: str


@dataclass
class VendorSearchRequest:
    """Request parameters for vendor search."""
    query: Optional[str] = None
    customer_id: Optional[str] = None
    risk_level: Optional[VendorRiskLevel] = None
    min_risk_score: Optional[float] = None
    support_status: Optional[SupportStatus] = None
    industry_focus: Optional[List[str]] = None
    supply_chain_tier: Optional[int] = None
    limit: int = 10
    include_system: bool = True


@dataclass
class EquipmentSearchRequest:
    """Request parameters for equipment search."""
    query: Optional[str] = None
    customer_id: Optional[str] = None
    vendor_id: Optional[str] = None
    lifecycle_status: Optional[LifecycleStatus] = None
    approaching_eol_days: Optional[int] = None  # Find equipment within N days of EOL
    category: Optional[str] = None
    criticality: Optional[str] = None
    limit: int = 10
    include_system: bool = True


@dataclass
class VendorSearchResult:
    """Single vendor search result."""
    vendor: Vendor
    score: float = 0.0
    match_reason: Optional[str] = None


@dataclass
class EquipmentSearchResult:
    """Single equipment search result."""
    equipment: EquipmentModel
    score: float = 0.0
    days_to_eol: Optional[int] = None
    days_to_eos: Optional[int] = None
    vendor_name: Optional[str] = None


@dataclass
class VendorRiskSummary:
    """Aggregated vendor risk assessment."""
    vendor_id: str
    vendor_name: str
    total_equipment: int
    total_cves: int
    avg_cvss: float
    critical_cves: int
    equipment_at_eol: int
    equipment_approaching_eol: int
    risk_score: float
    risk_level: VendorRiskLevel


class VendorEquipmentService:
    """
    Service for vendor equipment lifecycle management.

    Provides customer-isolated operations for:
    - Vendor management and risk assessment
    - Equipment model tracking
    - Support contract management
    - EOL/EOS monitoring
    - Supply chain vulnerability tracking
    """

    COLLECTION_NAME = "ner11_vendor_equipment"
    VECTOR_SIZE = 384  # sentence-transformers/all-MiniLM-L6-v2

    def __init__(
        self,
        qdrant_url: str = "http://localhost:6333",
        neo4j_driver: Optional[Any] = None,
        embedding_model: Optional[Any] = None,
        embedding_service: Optional[EmbeddingService] = None,
    ):
        """
        Initialize vendor equipment service.

        Args:
            qdrant_url: Qdrant server URL
            neo4j_driver: Neo4j driver instance (optional)
            embedding_model: Legacy embedding model (deprecated, use embedding_service)
            embedding_service: EmbeddingService instance for semantic search
        """
        self.qdrant_client = QdrantClient(url=qdrant_url)
        self.neo4j_driver = neo4j_driver
        self.embedding_model = embedding_model
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

    @property
    def embedding_service(self) -> EmbeddingService:
        """Get or create embedding service."""
        if self._embedding_service is None:
            self._embedding_service = get_embedding_service()
        return self._embedding_service

    def _generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for text using embedding service."""
        # Use new embedding service if available
        if self._embedding_service is not None:
            return self._embedding_service.encode(text)

        # Legacy support for embedding_model
        if self.embedding_model is not None:
            return self.embedding_model.encode(text).tolist()

        # Return zero vector if no model (for testing)
        return [0.0] * self.VECTOR_SIZE

    # ===== Vendor Operations =====

    def create_vendor(self, vendor: Vendor) -> Vendor:
        """Create a new vendor with customer isolation."""
        context = self._get_customer_context()

        if not context.can_write():
            raise PermissionError("Write access required to create vendor")

        # Ensure customer_id matches context
        if vendor.customer_id != context.customer_id:
            raise ValueError("Vendor customer_id must match context customer_id")

        # Generate embedding from vendor name and metadata
        embed_text = f"{vendor.name} {' '.join(vendor.industry_focus)}"
        embedding = self._generate_embedding(embed_text)

        # Store in Qdrant
        point_id = str(uuid4())
        self.qdrant_client.upsert(
            collection_name=self.COLLECTION_NAME,
            points=[
                PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload=vendor.to_qdrant_payload(),
                )
            ],
        )

        # Store in Neo4j if driver available
        if self.neo4j_driver:
            self._create_vendor_neo4j(vendor)

        logger.info(f"Created vendor {vendor.vendor_id} for customer {vendor.customer_id}")
        return vendor

    def _create_vendor_neo4j(self, vendor: Vendor) -> None:
        """Create vendor node in Neo4j."""
        with self.neo4j_driver.session() as session:
            session.run(
                """
                CREATE (v:Vendor $props)
                """,
                props=vendor.to_neo4j_properties(),
            )

    def get_vendor(self, vendor_id: str) -> Optional[Vendor]:
        """Get vendor by ID with customer isolation."""
        context = self._get_customer_context()

        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(key="vendor_id", match=MatchValue(value=vendor_id)),
                    FieldCondition(
                        key="customer_id",
                        match=MatchAny(any=context.get_customer_ids()),
                    ),
                    FieldCondition(key="entity_type", match=MatchValue(value="vendor")),
                ]
            ),
            limit=1,
        )

        if results[0]:
            payload = results[0][0].payload
            return self._payload_to_vendor(payload)
        return None

    def _payload_to_vendor(self, payload: Dict[str, Any]) -> Vendor:
        """Convert Qdrant payload to Vendor object."""
        return Vendor(
            vendor_id=payload["vendor_id"],
            name=payload["name"],
            customer_id=payload["customer_id"],
            risk_score=payload.get("risk_score", 0.0),
            support_status=SupportStatus(payload.get("support_status", "active")),
            country=payload.get("country"),
            industry_focus=payload.get("industry_focus", []),
            supply_chain_tier=payload.get("supply_chain_tier", 1),
            total_cves=payload.get("total_cves", 0),
            avg_cvss_score=payload.get("avg_cvss_score", 0.0),
        )

    def search_vendors(self, request: VendorSearchRequest) -> List[VendorSearchResult]:
        """Search vendors with filters and customer isolation."""
        context = self._get_customer_context()
        customer_id = request.customer_id or context.customer_id

        # Build additional conditions
        conditions = [
            FieldCondition(key="entity_type", match=MatchValue(value="vendor"))
        ]

        if request.risk_level:
            conditions.append(
                FieldCondition(key="risk_level", match=MatchValue(value=request.risk_level.value))
            )

        if request.min_risk_score is not None:
            conditions.append(
                FieldCondition(key="risk_score", range=Range(gte=request.min_risk_score))
            )

        if request.support_status:
            conditions.append(
                FieldCondition(key="support_status", match=MatchValue(value=request.support_status.value))
            )

        if request.supply_chain_tier:
            conditions.append(
                FieldCondition(key="supply_chain_tier", match=MatchValue(value=request.supply_chain_tier))
            )

        query_filter = self._build_customer_filter(
            customer_id=customer_id,
            include_system=request.include_system,
            additional_conditions=conditions,
        )

        # Perform search
        if request.query:
            embedding = self._generate_embedding(request.query)
            results = self.qdrant_client.search(
                collection_name=self.COLLECTION_NAME,
                query_vector=embedding,
                query_filter=query_filter,
                limit=request.limit,
            )
        else:
            # Scroll without semantic search
            results, _ = self.qdrant_client.scroll(
                collection_name=self.COLLECTION_NAME,
                scroll_filter=query_filter,
                limit=request.limit,
            )

        vendor_results = []
        for result in results:
            if hasattr(result, 'score'):
                score = result.score
                payload = result.payload
            else:
                score = 1.0
                payload = result.payload

            vendor = self._payload_to_vendor(payload)
            vendor_results.append(VendorSearchResult(vendor=vendor, score=score))

        return vendor_results

    def get_high_risk_vendors(self, min_risk_score: float = 7.0) -> List[VendorSearchResult]:
        """Get vendors with high risk scores."""
        request = VendorSearchRequest(
            min_risk_score=min_risk_score,
            limit=100,
        )
        return self.search_vendors(request)

    def get_vendor_risk_summary(self, vendor_id: str) -> Optional[VendorRiskSummary]:
        """Get comprehensive risk summary for a vendor."""
        vendor = self.get_vendor(vendor_id)
        if not vendor:
            return None

        context = self._get_customer_context()

        # Get equipment for this vendor
        equipment_request = EquipmentSearchRequest(
            vendor_id=vendor_id,
            limit=1000,
        )
        equipment_results = self.search_equipment(equipment_request)

        total_equipment = len(equipment_results)
        equipment_at_eol = sum(
            1 for eq in equipment_results
            if eq.equipment.lifecycle_status in [LifecycleStatus.EOL, LifecycleStatus.EOS]
        )
        equipment_approaching_eol = sum(
            1 for eq in equipment_results
            if eq.equipment.lifecycle_status == LifecycleStatus.APPROACHING_EOL
        )

        return VendorRiskSummary(
            vendor_id=vendor.vendor_id,
            vendor_name=vendor.name,
            total_equipment=total_equipment,
            total_cves=vendor.total_cves,
            avg_cvss=vendor.avg_cvss_score,
            critical_cves=vendor.critical_cve_count,
            equipment_at_eol=equipment_at_eol,
            equipment_approaching_eol=equipment_approaching_eol,
            risk_score=vendor.risk_score,
            risk_level=vendor.risk_level,
        )

    # ===== Equipment Operations =====

    def create_equipment(self, equipment: EquipmentModel) -> EquipmentModel:
        """Create equipment model with customer isolation."""
        context = self._get_customer_context()

        if not context.can_write():
            raise PermissionError("Write access required to create equipment")

        if equipment.customer_id != context.customer_id:
            raise ValueError("Equipment customer_id must match context customer_id")

        # Generate embedding
        embed_text = f"{equipment.model_name} {equipment.product_line or ''} {equipment.category or ''}"
        embedding = self._generate_embedding(embed_text)

        # Store in Qdrant
        point_id = str(uuid4())
        self.qdrant_client.upsert(
            collection_name=self.COLLECTION_NAME,
            points=[
                PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload=equipment.to_qdrant_payload(),
                )
            ],
        )

        # Store in Neo4j if driver available
        if self.neo4j_driver:
            self._create_equipment_neo4j(equipment)

        logger.info(f"Created equipment {equipment.model_id} for customer {equipment.customer_id}")
        return equipment

    def _create_equipment_neo4j(self, equipment: EquipmentModel) -> None:
        """Create equipment model node and relationship in Neo4j."""
        with self.neo4j_driver.session() as session:
            session.run(
                """
                CREATE (em:EquipmentModel $props)
                WITH em
                MATCH (v:Vendor {vendor_id: $vendor_id, customer_id: $customer_id})
                CREATE (v)-[:MANUFACTURES]->(em)
                """,
                props=equipment.to_neo4j_properties(),
                vendor_id=equipment.vendor_id,
                customer_id=equipment.customer_id,
            )

    def get_equipment(self, model_id: str) -> Optional[EquipmentModel]:
        """Get equipment model by ID with customer isolation."""
        context = self._get_customer_context()

        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(key="model_id", match=MatchValue(value=model_id)),
                    FieldCondition(
                        key="customer_id",
                        match=MatchAny(any=context.get_customer_ids()),
                    ),
                    FieldCondition(key="entity_type", match=MatchValue(value="equipment_model")),
                ]
            ),
            limit=1,
        )

        if results[0]:
            payload = results[0][0].payload
            return self._payload_to_equipment(payload)
        return None

    def _payload_to_equipment(self, payload: Dict[str, Any]) -> EquipmentModel:
        """Convert Qdrant payload to EquipmentModel."""
        eol_date = None
        eos_date = None
        if payload.get("eol_date"):
            eol_date = date.fromisoformat(payload["eol_date"])
        if payload.get("eos_date"):
            eos_date = date.fromisoformat(payload["eos_date"])

        return EquipmentModel(
            model_id=payload["model_id"],
            vendor_id=payload["vendor_id"],
            model_name=payload["model_name"],
            customer_id=payload["customer_id"],
            product_line=payload.get("product_line"),
            eol_date=eol_date,
            eos_date=eos_date,
            lifecycle_status=LifecycleStatus(payload.get("lifecycle_status", "current")),
            criticality=payload.get("criticality", "medium"),
            category=payload.get("category"),
            deployed_count=payload.get("deployed_count", 0),
            vulnerability_count=payload.get("vulnerability_count", 0),
        )

    def search_equipment(self, request: EquipmentSearchRequest) -> List[EquipmentSearchResult]:
        """Search equipment with filters and customer isolation."""
        context = self._get_customer_context()
        customer_id = request.customer_id or context.customer_id

        conditions = [
            FieldCondition(key="entity_type", match=MatchValue(value="equipment_model"))
        ]

        if request.vendor_id:
            conditions.append(
                FieldCondition(key="vendor_id", match=MatchValue(value=request.vendor_id))
            )

        if request.lifecycle_status:
            conditions.append(
                FieldCondition(key="lifecycle_status", match=MatchValue(value=request.lifecycle_status.value))
            )

        if request.category:
            conditions.append(
                FieldCondition(key="category", match=MatchValue(value=request.category))
            )

        query_filter = self._build_customer_filter(
            customer_id=customer_id,
            include_system=request.include_system,
            additional_conditions=conditions,
        )

        # Perform search
        if request.query:
            embedding = self._generate_embedding(request.query)
            results = self.qdrant_client.search(
                collection_name=self.COLLECTION_NAME,
                query_vector=embedding,
                query_filter=query_filter,
                limit=request.limit,
            )
        else:
            results, _ = self.qdrant_client.scroll(
                collection_name=self.COLLECTION_NAME,
                scroll_filter=query_filter,
                limit=request.limit,
            )

        equipment_results = []
        for result in results:
            if hasattr(result, 'score'):
                score = result.score
                payload = result.payload
            else:
                score = 1.0
                payload = result.payload

            equipment = self._payload_to_equipment(payload)
            equipment_results.append(
                EquipmentSearchResult(
                    equipment=equipment,
                    score=score,
                    days_to_eol=equipment.days_to_eol(),
                    days_to_eos=equipment.days_to_eos(),
                )
            )

        # Filter by approaching EOL if specified
        if request.approaching_eol_days:
            equipment_results = [
                r for r in equipment_results
                if r.days_to_eol is not None and 0 < r.days_to_eol <= request.approaching_eol_days
            ]

        return equipment_results

    def get_equipment_approaching_eol(self, days: int = 180) -> List[EquipmentSearchResult]:
        """Get equipment approaching EOL within specified days."""
        request = EquipmentSearchRequest(
            approaching_eol_days=days,
            limit=100,
        )
        return self.search_equipment(request)

    def get_eol_equipment(self) -> List[EquipmentSearchResult]:
        """Get all equipment that has passed EOL."""
        request = EquipmentSearchRequest(
            lifecycle_status=LifecycleStatus.EOL,
            limit=100,
        )
        return self.search_equipment(request)

    # ===== Supply Chain Vulnerability Tracking =====

    def flag_vendor_vulnerability(
        self,
        vendor_id: str,
        cve_id: str,
        cvss_score: float,
        description: str,
        published_date: Optional[date] = None,
    ) -> VulnerabilityAlert:
        """
        Flag all equipment from a vendor as affected by a vulnerability.
        Stores CVE record in Qdrant for tracking and analysis.

        Args:
            vendor_id: The vendor affected by the CVE
            cve_id: CVE identifier (e.g., CVE-2024-12345)
            cvss_score: CVSS score (0.0-10.0)
            description: Description of the vulnerability
            published_date: Date CVE was published

        Returns:
            VulnerabilityAlert with affected equipment details
        """
        context = self._get_customer_context()

        if not context.can_write():
            raise PermissionError("Write access required to flag vulnerabilities")

        # Get vendor information
        vendor = self.get_vendor(vendor_id)
        vendor_name = vendor.name if vendor else "Unknown Vendor"

        # Get all equipment for this vendor
        request = EquipmentSearchRequest(vendor_id=vendor_id, limit=1000)
        equipment_list = self.search_equipment(request)

        affected_equipment_ids = [eq.equipment.model_id for eq in equipment_list]
        affected_count = len(equipment_list)

        # Count critical equipment
        critical_count = sum(
            1 for eq in equipment_list
            if eq.equipment.criticality in ["critical", "high"]
        )

        # Calculate severity
        if cvss_score >= 9.0:
            severity = "critical"
        elif cvss_score >= 7.0:
            severity = "high"
        elif cvss_score >= 4.0:
            severity = "medium"
        else:
            severity = "low"

        # Create CVE record
        cve_record = CVERecord(
            cve_id=cve_id,
            cvss_score=cvss_score,
            severity=severity,
            description=description,
            affected_vendor_id=vendor_id,
            affected_equipment_ids=affected_equipment_ids,
            published_date=published_date,
            customer_id="SYSTEM",
        )

        # Store CVE in Qdrant for semantic search and tracking
        cve_embedding = self.embedding_service.encode(
            f"{cve_id} {description} {vendor_name} vulnerability"
        )

        point_id = str(uuid4())
        self.qdrant_client.upsert(
            collection_name=self.COLLECTION_NAME,
            points=[
                PointStruct(
                    id=point_id,
                    vector=cve_embedding,
                    payload=cve_record.to_qdrant_payload(),
                )
            ],
        )

        # Update vendor risk score if CVE is severe
        if vendor and cvss_score >= 7.0:
            self._update_vendor_cve_stats(vendor_id, cvss_score)

        # Generate recommendation
        if cvss_score >= 9.0:
            recommendation = f"CRITICAL: Immediate patching required. {affected_count} equipment affected including {critical_count} critical systems."
        elif cvss_score >= 7.0:
            recommendation = f"HIGH: Prioritize patching within 24-48 hours. {affected_count} equipment affected."
        elif cvss_score >= 4.0:
            recommendation = f"MEDIUM: Schedule patching in next maintenance window. {affected_count} equipment affected."
        else:
            recommendation = f"LOW: Monitor and patch during routine maintenance. {affected_count} equipment affected."

        logger.warning(
            f"Supply chain vulnerability {cve_id} (CVSS: {cvss_score}) affects "
            f"{affected_count} equipment models from vendor {vendor_id}"
        )

        return VulnerabilityAlert(
            cve_id=cve_id,
            vendor_id=vendor_id,
            vendor_name=vendor_name,
            cvss_score=cvss_score,
            severity=severity,
            affected_equipment_count=affected_count,
            critical_equipment_affected=critical_count,
            recommendation=recommendation,
        )

    def _update_vendor_cve_stats(self, vendor_id: str, new_cvss: float) -> None:
        """Update vendor's CVE statistics after new vulnerability."""
        # This would update the vendor record in Qdrant and Neo4j
        # For now, just log the update
        logger.info(f"Updating CVE stats for vendor {vendor_id} with new CVSS {new_cvss}")

    def get_vendor_cves(
        self,
        vendor_id: str,
        min_cvss: Optional[float] = None,
        severity: Optional[str] = None,
        limit: int = 50,
    ) -> List[CVERecord]:
        """
        Get all CVEs affecting a specific vendor.

        Args:
            vendor_id: Vendor ID to get CVEs for
            min_cvss: Minimum CVSS score filter
            severity: Filter by severity (critical, high, medium, low)
            limit: Maximum CVEs to return

        Returns:
            List of CVE records affecting the vendor
        """
        context = self._get_customer_context()

        conditions = [
            FieldCondition(key="entity_type", match=MatchValue(value="cve")),
            FieldCondition(key="affected_vendor_id", match=MatchValue(value=vendor_id)),
        ]

        if severity:
            conditions.append(
                FieldCondition(key="severity", match=MatchValue(value=severity))
            )

        if min_cvss is not None:
            conditions.append(
                FieldCondition(key="cvss_score", range=Range(gte=min_cvss))
            )

        query_filter = Filter(
            must=[
                FieldCondition(
                    key="customer_id",
                    match=MatchAny(any=[context.customer_id, "SYSTEM"]),
                )
            ] + conditions
        )

        results, _ = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=query_filter,
            limit=limit,
        )

        cves = []
        for result in results:
            payload = result.payload
            cves.append(self._payload_to_cve(payload))

        # Sort by CVSS score descending
        cves.sort(key=lambda c: c.cvss_score, reverse=True)
        return cves

    def _payload_to_cve(self, payload: Dict[str, Any]) -> CVERecord:
        """Convert Qdrant payload to CVERecord."""
        published_date = None
        if payload.get("published_date"):
            published_date = date.fromisoformat(payload["published_date"])

        flagged_at = None
        if payload.get("flagged_at"):
            flagged_at = datetime.fromisoformat(payload["flagged_at"])

        return CVERecord(
            cve_id=payload["cve_id"],
            cvss_score=payload["cvss_score"],
            severity=payload["severity"],
            description=payload["description"],
            affected_vendor_id=payload["affected_vendor_id"],
            affected_equipment_ids=payload.get("affected_equipment_ids", []),
            published_date=published_date,
            customer_id=payload.get("customer_id", "SYSTEM"),
            flagged_at=flagged_at,
        )

    def search_cves(
        self,
        query: str,
        min_cvss: Optional[float] = None,
        limit: int = 20,
    ) -> List[CVERecord]:
        """
        Semantic search across CVE records.

        Args:
            query: Natural language search (e.g., "SQL injection", "remote code execution")
            min_cvss: Minimum CVSS score
            limit: Maximum results

        Returns:
            List of matching CVE records
        """
        context = self._get_customer_context()

        embedding = self.embedding_service.encode(query)

        conditions = [
            FieldCondition(key="entity_type", match=MatchValue(value="cve")),
        ]

        if min_cvss is not None:
            conditions.append(
                FieldCondition(key="cvss_score", range=Range(gte=min_cvss))
            )

        query_filter = Filter(
            must=[
                FieldCondition(
                    key="customer_id",
                    match=MatchAny(any=[context.customer_id, "SYSTEM"]),
                )
            ] + conditions
        )

        results = self.qdrant_client.search(
            collection_name=self.COLLECTION_NAME,
            query_vector=embedding,
            query_filter=query_filter,
            limit=limit,
        )

        return [self._payload_to_cve(r.payload) for r in results]

    def get_critical_vulnerabilities(self, limit: int = 20) -> List[VulnerabilityAlert]:
        """
        Get critical and high severity vulnerabilities with impact analysis.

        Returns:
            List of vulnerability alerts for critical/high CVEs
        """
        context = self._get_customer_context()

        query_filter = Filter(
            must=[
                FieldCondition(
                    key="customer_id",
                    match=MatchAny(any=[context.customer_id, "SYSTEM"]),
                ),
                FieldCondition(key="entity_type", match=MatchValue(value="cve")),
                FieldCondition(
                    key="severity",
                    match=MatchAny(any=["critical", "high"]),
                ),
            ]
        )

        results, _ = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=query_filter,
            limit=limit,
        )

        alerts = []
        for result in results:
            payload = result.payload
            cve = self._payload_to_cve(payload)

            # Get vendor info
            vendor = self.get_vendor(cve.affected_vendor_id)
            vendor_name = vendor.name if vendor else "Unknown"

            # Count critical equipment
            critical_count = 0
            for eq_id in cve.affected_equipment_ids[:10]:  # Limit to first 10
                eq = self.get_equipment(eq_id)
                if eq and eq.criticality in ["critical", "high"]:
                    critical_count += 1

            if cve.cvss_score >= 9.0:
                recommendation = "CRITICAL: Immediate patching required."
            else:
                recommendation = "HIGH: Prioritize patching within 24-48 hours."

            alerts.append(
                VulnerabilityAlert(
                    cve_id=cve.cve_id,
                    vendor_id=cve.affected_vendor_id,
                    vendor_name=vendor_name,
                    cvss_score=cve.cvss_score,
                    severity=cve.severity,
                    affected_equipment_count=len(cve.affected_equipment_ids),
                    critical_equipment_affected=critical_count,
                    recommendation=recommendation,
                )
            )

        # Sort by CVSS descending
        alerts.sort(key=lambda a: a.cvss_score, reverse=True)
        return alerts

    def get_maintenance_schedule(
        self,
        limit: int = 50,
    ) -> List[Tuple[EquipmentSearchResult, str]]:
        """
        Generate maintenance schedule prioritized by:
        1. EOL proximity
        2. Vulnerability count
        3. Criticality
        """
        context = self._get_customer_context()

        # Get all equipment
        request = EquipmentSearchRequest(limit=1000)
        equipment_list = self.search_equipment(request)

        # Score and sort by priority
        def priority_score(eq_result: EquipmentSearchResult) -> float:
            equipment = eq_result.equipment
            score = 0.0

            # EOL proximity (higher priority if closer)
            if eq_result.days_to_eol is not None:
                if eq_result.days_to_eol <= 0:
                    score += 100  # Past EOL
                elif eq_result.days_to_eol <= 30:
                    score += 80
                elif eq_result.days_to_eol <= 90:
                    score += 60
                elif eq_result.days_to_eol <= 180:
                    score += 40

            # Vulnerability count
            score += min(equipment.vulnerability_count * 5, 30)

            # Criticality
            criticality_scores = {
                "critical": 25,
                "high": 15,
                "medium": 5,
                "low": 0,
            }
            score += criticality_scores.get(equipment.criticality.value if hasattr(equipment.criticality, 'value') else equipment.criticality, 0)

            return score

        # Sort by priority and take top N
        equipment_list.sort(key=priority_score, reverse=True)
        equipment_list = equipment_list[:limit]

        # Generate recommendations
        results = []
        for eq_result in equipment_list:
            equipment = eq_result.equipment

            if equipment.lifecycle_status == LifecycleStatus.EOL:
                recommendation = "URGENT: Equipment is past EOL. Plan immediate replacement."
            elif equipment.lifecycle_status == LifecycleStatus.EOS:
                recommendation = "CRITICAL: Equipment is past End of Support. No security patches available."
            elif equipment.lifecycle_status == LifecycleStatus.APPROACHING_EOL:
                recommendation = f"Equipment approaching EOL in {eq_result.days_to_eol} days. Begin migration planning."
            elif equipment.vulnerability_count > 5:
                recommendation = f"High vulnerability count ({equipment.vulnerability_count}). Prioritize patching."
            else:
                recommendation = f"Scheduled maintenance per {equipment.maintenance_schedule.value} schedule."

            results.append((eq_result, recommendation))

        return results

    # ===== Semantic Search Operations =====

    def semantic_search(
        self,
        query: str,
        entity_type: Optional[str] = None,
        limit: int = 10,
        min_score: float = 0.5,
    ) -> List[SemanticSearchResult]:
        """
        Perform semantic search across vendors and equipment.

        Uses sentence-transformer embeddings for natural language queries
        like "network security appliances" or "critical firewall vendors".

        Args:
            query: Natural language search query
            entity_type: Filter by "vendor" or "equipment_model" (optional)
            limit: Maximum results to return
            min_score: Minimum similarity score threshold

        Returns:
            List of semantically similar results
        """
        context = self._get_customer_context()

        # Generate query embedding
        embedding = self.embedding_service.encode(query)

        # Build filter conditions
        conditions = []
        if entity_type:
            conditions.append(
                FieldCondition(key="entity_type", match=MatchValue(value=entity_type))
            )

        query_filter = self._build_customer_filter(
            customer_id=context.customer_id,
            include_system=True,
            additional_conditions=conditions if conditions else None,
        )

        # Perform semantic search
        results = self.qdrant_client.search(
            collection_name=self.COLLECTION_NAME,
            query_vector=embedding,
            query_filter=query_filter,
            limit=limit,
            score_threshold=min_score,
        )

        semantic_results = []
        for result in results:
            payload = result.payload
            entity_id = payload.get("vendor_id") or payload.get("model_id", "unknown")
            name = payload.get("name") or payload.get("model_name", "unknown")

            semantic_results.append(
                SemanticSearchResult(
                    entity_id=entity_id,
                    entity_type=payload.get("entity_type", "unknown"),
                    name=name,
                    score=result.score,
                    payload=payload,
                )
            )

        return semantic_results

    def find_similar_vendors(
        self,
        vendor_id: str,
        limit: int = 5,
        min_score: float = 0.6,
    ) -> List[SimilarityMatch]:
        """
        Find vendors similar to the given vendor.

        Useful for identifying alternative vendors or discovering
        vendors with similar product offerings.

        Args:
            vendor_id: ID of the source vendor
            limit: Maximum similar vendors to return
            min_score: Minimum similarity threshold

        Returns:
            List of similar vendor matches
        """
        vendor = self.get_vendor(vendor_id)
        if not vendor:
            return []

        context = self._get_customer_context()

        # Generate embedding from vendor data
        embed_text = f"{vendor.name} {' '.join(vendor.industry_focus)}"
        embedding = self.embedding_service.encode(embed_text)

        # Search for similar vendors (excluding the source vendor)
        query_filter = self._build_customer_filter(
            customer_id=context.customer_id,
            include_system=True,
            additional_conditions=[
                FieldCondition(key="entity_type", match=MatchValue(value="vendor")),
            ],
        )

        results = self.qdrant_client.search(
            collection_name=self.COLLECTION_NAME,
            query_vector=embedding,
            query_filter=query_filter,
            limit=limit + 1,  # Get extra to exclude source
            score_threshold=min_score,
        )

        matches = []
        for result in results:
            payload = result.payload
            match_id = payload.get("vendor_id")

            # Skip the source vendor
            if match_id == vendor_id:
                continue

            matches.append(
                SimilarityMatch(
                    source_id=vendor_id,
                    match_id=match_id,
                    match_name=payload.get("name", "Unknown"),
                    similarity_score=result.score,
                    match_type="vendor",
                )
            )

            if len(matches) >= limit:
                break

        return matches

    def find_similar_equipment(
        self,
        model_id: str,
        limit: int = 5,
        min_score: float = 0.6,
    ) -> List[SimilarityMatch]:
        """
        Find equipment similar to the given equipment model.

        Useful for identifying replacement options or compatible alternatives.

        Args:
            model_id: ID of the source equipment model
            limit: Maximum similar equipment to return
            min_score: Minimum similarity threshold

        Returns:
            List of similar equipment matches
        """
        equipment = self.get_equipment(model_id)
        if not equipment:
            return []

        context = self._get_customer_context()

        # Generate embedding from equipment data
        embed_text = f"{equipment.model_name} {equipment.product_line or ''} {equipment.category or ''}"
        embedding = self.embedding_service.encode(embed_text)

        # Search for similar equipment (excluding the source)
        query_filter = self._build_customer_filter(
            customer_id=context.customer_id,
            include_system=True,
            additional_conditions=[
                FieldCondition(key="entity_type", match=MatchValue(value="equipment_model")),
            ],
        )

        results = self.qdrant_client.search(
            collection_name=self.COLLECTION_NAME,
            query_vector=embedding,
            query_filter=query_filter,
            limit=limit + 1,  # Get extra to exclude source
            score_threshold=min_score,
        )

        matches = []
        for result in results:
            payload = result.payload
            match_id = payload.get("model_id")

            # Skip the source equipment
            if match_id == model_id:
                continue

            matches.append(
                SimilarityMatch(
                    source_id=model_id,
                    match_id=match_id,
                    match_name=payload.get("model_name", "Unknown"),
                    similarity_score=result.score,
                    match_type="equipment",
                )
            )

            if len(matches) >= limit:
                break

        return matches

    def find_replacement_candidates(
        self,
        model_id: str,
        exclude_eol: bool = True,
        limit: int = 5,
    ) -> List[SimilarityMatch]:
        """
        Find replacement candidates for equipment approaching EOL.

        Filters out EOL equipment to only show viable replacements.

        Args:
            model_id: ID of the equipment needing replacement
            exclude_eol: If True, exclude equipment at EOL/EOS
            limit: Maximum candidates to return

        Returns:
            List of replacement candidates sorted by similarity
        """
        equipment = self.get_equipment(model_id)
        if not equipment:
            return []

        context = self._get_customer_context()

        # Generate embedding
        embed_text = f"{equipment.model_name} {equipment.product_line or ''} {equipment.category or ''}"
        embedding = self.embedding_service.encode(embed_text)

        # Build filter to exclude EOL equipment
        conditions = [
            FieldCondition(key="entity_type", match=MatchValue(value="equipment_model")),
        ]

        if exclude_eol:
            # Only include current or approaching EOL equipment
            conditions.append(
                FieldCondition(
                    key="lifecycle_status",
                    match=MatchAny(any=["current", "approaching_eol"]),
                )
            )

        query_filter = self._build_customer_filter(
            customer_id=context.customer_id,
            include_system=True,
            additional_conditions=conditions,
        )

        results = self.qdrant_client.search(
            collection_name=self.COLLECTION_NAME,
            query_vector=embedding,
            query_filter=query_filter,
            limit=limit + 1,
            score_threshold=0.5,
        )

        matches = []
        for result in results:
            payload = result.payload
            match_id = payload.get("model_id")

            # Skip the source equipment
            if match_id == model_id:
                continue

            matches.append(
                SimilarityMatch(
                    source_id=model_id,
                    match_id=match_id,
                    match_name=payload.get("model_name", "Unknown"),
                    similarity_score=result.score,
                    match_type="replacement",
                )
            )

            if len(matches) >= limit:
                break

        return matches

    # =========================================================================
    # EOL/EOS Alerting System (Day 5)
    # =========================================================================

    def get_eol_alerts(
        self,
        severity_filter: Optional[str] = None,
        days_ahead: int = 180,
        include_past_due: bool = True,
    ) -> List["EOLAlert"]:
        """
        Get EOL/EOS alerts for equipment approaching or past lifecycle milestones.

        Args:
            severity_filter: Filter by severity ('info', 'warning', 'high', 'critical')
            days_ahead: Look ahead window in days (default 180)
            include_past_due: Include equipment already past EOL/EOS

        Returns:
            List of EOLAlert objects sorted by severity and days remaining
        """
        from .vendor_models import EOLAlert, AlertType, AlertSeverity

        context = self._get_customer_context()
        alerts: List["EOLAlert"] = []

        # Query for equipment with EOL/EOS dates
        conditions = [
            FieldCondition(key="entity_type", match=MatchValue(value="equipment_model")),
        ]

        # Include equipment with lifecycle status indicating EOL concerns
        if include_past_due:
            conditions.append(
                FieldCondition(
                    key="lifecycle_status",
                    match=MatchAny(any=["approaching_eol", "eol", "eos"]),
                )
            )
        else:
            conditions.append(
                FieldCondition(
                    key="lifecycle_status",
                    match=MatchValue(value="approaching_eol"),
                )
            )

        query_filter = self._build_customer_filter(
            customer_id=context.customer_id,
            include_system=False,
            additional_conditions=conditions,
        )

        # Use scroll to get all matching equipment
        results, _ = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=query_filter,
            limit=1000,
            with_payload=True,
        )

        today = date.today()

        for point in results:
            payload = point.payload
            eol_date_str = payload.get("eol_date")
            eos_date_str = payload.get("eos_date")
            model_id = payload.get("model_id")
            model_name = payload.get("model_name", "Unknown")
            vendor_id = payload.get("vendor_id")
            deployed_count = payload.get("deployed_count", 0)

            # Check EOL date
            if eol_date_str:
                eol_date = date.fromisoformat(eol_date_str)
                days_to_eol = (eol_date - today).days

                if days_to_eol <= days_ahead or (include_past_due and days_to_eol < 0):
                    # Determine alert type
                    if days_to_eol < 0:
                        alert_type = AlertType.EOL_PAST
                    else:
                        alert_type = AlertType.EOL_APPROACHING

                    # Calculate severity
                    if days_to_eol < 0:
                        severity = AlertSeverity.CRITICAL
                    elif days_to_eol <= 7:
                        severity = AlertSeverity.CRITICAL
                    elif days_to_eol <= 30:
                        severity = AlertSeverity.HIGH
                    elif days_to_eol <= 90:
                        severity = AlertSeverity.WARNING
                    else:
                        severity = AlertSeverity.INFO

                    # Apply severity filter
                    if severity_filter and severity.value != severity_filter:
                        continue

                    # Generate message
                    if days_to_eol < 0:
                        message = f"{model_name} is {abs(days_to_eol)} days past End of Life"
                    else:
                        message = f"{model_name} reaches End of Life in {days_to_eol} days"

                    import uuid
                    alert = EOLAlert(
                        alert_id=f"ALERT-{uuid.uuid4().hex[:8].upper()}",
                        alert_type=alert_type,
                        severity=severity,
                        customer_id=context.customer_id,
                        entity_type="equipment_model",
                        entity_id=model_id,
                        entity_name=model_name,
                        message=message,
                        days_remaining=days_to_eol,
                        target_date=eol_date,
                        vendor_id=vendor_id,
                        affected_asset_count=deployed_count,
                        recommended_action="Plan migration to supported equipment" if days_to_eol <= 90 else None,
                    )
                    alerts.append(alert)

            # Check EOS date
            if eos_date_str:
                eos_date = date.fromisoformat(eos_date_str)
                days_to_eos = (eos_date - today).days

                if days_to_eos <= days_ahead or (include_past_due and days_to_eos < 0):
                    # Only add EOS alert if it's different from EOL
                    if eos_date_str != eol_date_str:
                        if days_to_eos < 0:
                            alert_type = AlertType.EOS_PAST
                        else:
                            alert_type = AlertType.EOS_APPROACHING

                        if days_to_eos < 0:
                            severity = AlertSeverity.CRITICAL
                        elif days_to_eos <= 7:
                            severity = AlertSeverity.CRITICAL
                        elif days_to_eos <= 30:
                            severity = AlertSeverity.HIGH
                        elif days_to_eos <= 90:
                            severity = AlertSeverity.WARNING
                        else:
                            severity = AlertSeverity.INFO

                        if severity_filter and severity.value != severity_filter:
                            continue

                        if days_to_eos < 0:
                            message = f"{model_name} is {abs(days_to_eos)} days past End of Support"
                        else:
                            message = f"{model_name} reaches End of Support in {days_to_eos} days"

                        import uuid
                        alert = EOLAlert(
                            alert_id=f"ALERT-{uuid.uuid4().hex[:8].upper()}",
                            alert_type=alert_type,
                            severity=severity,
                            customer_id=context.customer_id,
                            entity_type="equipment_model",
                            entity_id=model_id,
                            entity_name=model_name,
                            message=message,
                            days_remaining=days_to_eos,
                            target_date=eos_date,
                            vendor_id=vendor_id,
                            affected_asset_count=deployed_count,
                            recommended_action="Urgent: End of Support reached - no security patches available" if days_to_eos <= 30 else None,
                        )
                        alerts.append(alert)

        # Sort by severity (critical first) then by days remaining
        severity_order = {"critical": 0, "high": 1, "warning": 2, "info": 3}
        alerts.sort(key=lambda a: (severity_order.get(a.severity.value, 4), a.days_remaining))

        return alerts

    def get_contract_expiration_alerts(
        self,
        days_ahead: int = 90,
        include_expired: bool = True,
    ) -> List["EOLAlert"]:
        """
        Get alerts for support contracts approaching expiration or expired.

        Args:
            days_ahead: Look ahead window in days (default 90)
            include_expired: Include already expired contracts

        Returns:
            List of EOLAlert objects for contract expirations
        """
        from .vendor_models import EOLAlert, AlertType, AlertSeverity

        context = self._get_customer_context()
        alerts: List["EOLAlert"] = []

        # Query for support contracts
        conditions = [
            FieldCondition(key="entity_type", match=MatchValue(value="support_contract")),
        ]

        query_filter = self._build_customer_filter(
            customer_id=context.customer_id,
            include_system=False,
            additional_conditions=conditions,
        )

        results, _ = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=query_filter,
            limit=1000,
            with_payload=True,
        )

        today = date.today()

        for point in results:
            payload = point.payload
            end_date_str = payload.get("end_date")
            contract_id = payload.get("contract_id")
            vendor_id = payload.get("vendor_id")
            service_level = payload.get("service_level", "standard")

            if end_date_str:
                end_date = date.fromisoformat(end_date_str)
                days_remaining = (end_date - today).days

                if days_remaining <= days_ahead or (include_expired and days_remaining < 0):
                    # Determine alert type and severity
                    if days_remaining < 0:
                        alert_type = AlertType.CONTRACT_EXPIRED
                        severity = AlertSeverity.CRITICAL
                        message = f"Support contract {contract_id} expired {abs(days_remaining)} days ago"
                    else:
                        alert_type = AlertType.CONTRACT_EXPIRING
                        if days_remaining <= 7:
                            severity = AlertSeverity.CRITICAL
                        elif days_remaining <= 30:
                            severity = AlertSeverity.HIGH
                        elif days_remaining <= 90:
                            severity = AlertSeverity.WARNING
                        else:
                            severity = AlertSeverity.INFO
                        message = f"Support contract {contract_id} expires in {days_remaining} days"

                    import uuid
                    alert = EOLAlert(
                        alert_id=f"ALERT-{uuid.uuid4().hex[:8].upper()}",
                        alert_type=alert_type,
                        severity=severity,
                        customer_id=context.customer_id,
                        entity_type="support_contract",
                        entity_id=contract_id,
                        entity_name=f"Contract {contract_id} ({service_level})",
                        message=message,
                        days_remaining=days_remaining,
                        target_date=end_date,
                        vendor_id=vendor_id,
                        recommended_action="Initiate contract renewal process" if days_remaining <= 90 else None,
                    )
                    alerts.append(alert)

        # Sort by severity then days remaining
        severity_order = {"critical": 0, "high": 1, "warning": 2, "info": 3}
        alerts.sort(key=lambda a: (severity_order.get(a.severity.value, 4), a.days_remaining))

        return alerts

    def get_all_lifecycle_alerts(
        self,
        severity_filter: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get all lifecycle alerts (EOL/EOS and contracts) grouped by type.

        Args:
            severity_filter: Optional filter by severity level

        Returns:
            Dictionary with 'eol_alerts' and 'contract_alerts' keys
        """
        eol_alerts = self.get_eol_alerts(severity_filter=severity_filter)
        contract_alerts = self.get_contract_expiration_alerts()

        # Apply severity filter to contract alerts if specified
        if severity_filter:
            contract_alerts = [a for a in contract_alerts if a.severity.value == severity_filter]

        return {
            "eol_alerts": eol_alerts,
            "contract_alerts": contract_alerts,
            "total_critical": sum(1 for a in eol_alerts + contract_alerts if a.severity.value == "critical"),
            "total_high": sum(1 for a in eol_alerts + contract_alerts if a.severity.value == "high"),
            "total_alerts": len(eol_alerts) + len(contract_alerts),
        }

    def get_vendor_risk_summary(
        self,
        vendor_id: str,
    ) -> Optional["VendorRiskSummary"]:
        """
        Get comprehensive risk summary for a vendor including lifecycle and vulnerability data.

        Args:
            vendor_id: The vendor ID to analyze

        Returns:
            VendorRiskSummary with risk metrics, or None if vendor not found
        """
        vendor = self.get_vendor(vendor_id)
        if not vendor:
            return None

        # Get equipment for this vendor
        equipment_list = self.search_equipment(EquipmentSearchRequest(vendor_id=vendor_id))

        # Count by lifecycle status
        lifecycle_counts: Dict[str, int] = {
            "current": 0,
            "approaching_eol": 0,
            "eol": 0,
            "eos": 0,
        }

        total_deployed = 0
        total_vulnerabilities = 0

        for eq in equipment_list:
            status = eq.get("lifecycle_status", "current")
            lifecycle_counts[status] = lifecycle_counts.get(status, 0) + 1
            total_deployed += eq.get("deployed_count", 0)
            total_vulnerabilities += eq.get("vulnerability_count", 0)

        # Get CVE count
        cves = self.get_vendor_cves(vendor_id)

        return VendorRiskSummary(
            vendor_id=vendor_id,
            vendor_name=vendor.name,
            risk_score=vendor.risk_score,
            risk_level=vendor.risk_level.value,
            total_equipment=len(equipment_list),
            equipment_at_eol=lifecycle_counts.get("eol", 0) + lifecycle_counts.get("eos", 0),
            equipment_approaching_eol=lifecycle_counts.get("approaching_eol", 0),
            total_deployed_assets=total_deployed,
            total_vulnerabilities=total_vulnerabilities,
            critical_cve_count=len([c for c in cves if c.severity == "critical"]),
            high_cve_count=len([c for c in cves if c.severity == "high"]),
            total_cve_count=len(cves),
        )

    # =========================================================================
    # Batch Operations (Day 6)
    # =========================================================================

    def batch_import_vendors(
        self,
        vendors_data: List[Dict[str, Any]],
        skip_duplicates: bool = True,
    ) -> Dict[str, Any]:
        """
        Batch import multiple vendors at once.

        Args:
            vendors_data: List of vendor dictionaries with required fields
            skip_duplicates: If True, skip vendors with existing IDs

        Returns:
            Dict with 'imported', 'skipped', 'errors' counts and details
        """
        context = self._get_customer_context()
        imported = []
        skipped = []
        errors = []

        for vendor_dict in vendors_data:
            try:
                vendor_id = vendor_dict.get("vendor_id")
                if not vendor_id:
                    errors.append({"data": vendor_dict, "error": "Missing vendor_id"})
                    continue

                # Check for existing vendor
                if skip_duplicates:
                    existing = self.get_vendor(vendor_id)
                    if existing:
                        skipped.append(vendor_id)
                        continue

                # Create Vendor object
                vendor = Vendor(
                    vendor_id=vendor_id,
                    name=vendor_dict.get("name", "Unknown"),
                    customer_id=context.customer_id,
                    risk_score=vendor_dict.get("risk_score", 5.0),
                    support_status=SupportStatus(vendor_dict.get("support_status", "active")),
                    country=vendor_dict.get("country"),
                    industry_focus=vendor_dict.get("industry_focus", []),
                    supply_chain_tier=vendor_dict.get("supply_chain_tier", 2),
                    total_cves=vendor_dict.get("total_cves", 0),
                    avg_cvss_score=vendor_dict.get("avg_cvss_score", 0.0),
                    website=vendor_dict.get("website"),
                    contact_email=vendor_dict.get("contact_email"),
                )

                # Store vendor
                self.store_vendor(vendor)
                imported.append(vendor_id)

            except Exception as e:
                errors.append({"data": vendor_dict, "error": str(e)})

        return {
            "imported_count": len(imported),
            "skipped_count": len(skipped),
            "error_count": len(errors),
            "imported_ids": imported,
            "skipped_ids": skipped,
            "errors": errors,
        }

    def batch_import_equipment(
        self,
        equipment_data: List[Dict[str, Any]],
        skip_duplicates: bool = True,
    ) -> Dict[str, Any]:
        """
        Batch import multiple equipment models at once.

        Args:
            equipment_data: List of equipment dictionaries with required fields
            skip_duplicates: If True, skip equipment with existing IDs

        Returns:
            Dict with 'imported', 'skipped', 'errors' counts and details
        """
        context = self._get_customer_context()
        imported = []
        skipped = []
        errors = []

        for eq_dict in equipment_data:
            try:
                model_id = eq_dict.get("model_id")
                if not model_id:
                    errors.append({"data": eq_dict, "error": "Missing model_id"})
                    continue

                # Check for existing equipment
                if skip_duplicates:
                    existing = self.get_equipment(model_id)
                    if existing:
                        skipped.append(model_id)
                        continue

                # Parse dates
                eol_date = None
                eos_date = None
                if eq_dict.get("eol_date"):
                    eol_date = date.fromisoformat(eq_dict["eol_date"])
                if eq_dict.get("eos_date"):
                    eos_date = date.fromisoformat(eq_dict["eos_date"])

                # Create EquipmentModel object
                equipment = EquipmentModel(
                    model_id=model_id,
                    vendor_id=eq_dict.get("vendor_id", "UNKNOWN"),
                    model_name=eq_dict.get("model_name", "Unknown"),
                    customer_id=context.customer_id,
                    product_line=eq_dict.get("product_line"),
                    category=eq_dict.get("category"),
                    criticality=eq_dict.get("criticality", "medium"),
                    eol_date=eol_date,
                    eos_date=eos_date,
                    lifecycle_status=LifecycleStatus(eq_dict.get("lifecycle_status", "current")),
                    firmware_version=eq_dict.get("firmware_version"),
                    vulnerability_count=eq_dict.get("vulnerability_count", 0),
                    deployed_count=eq_dict.get("deployed_count", 0),
                )

                # Store equipment
                self.store_equipment(equipment)
                imported.append(model_id)

            except Exception as e:
                errors.append({"data": eq_dict, "error": str(e)})

        return {
            "imported_count": len(imported),
            "skipped_count": len(skipped),
            "error_count": len(errors),
            "imported_ids": imported,
            "skipped_ids": skipped,
            "errors": errors,
        }

    def export_vendors(
        self,
        format: str = "dict",
        include_equipment: bool = False,
        include_cves: bool = False,
    ) -> List[Dict[str, Any]]:
        """
        Export all vendors for the current customer.

        Args:
            format: Output format ('dict' or 'csv_rows')
            include_equipment: Include associated equipment list
            include_cves: Include associated CVE list

        Returns:
            List of vendor dictionaries or CSV row data
        """
        context = self._get_customer_context()

        query_filter = self._build_customer_filter(
            customer_id=context.customer_id,
            include_system=True,
            additional_conditions=[
                FieldCondition(key="entity_type", match=MatchValue(value="vendor")),
            ],
        )

        results, _ = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=query_filter,
            limit=10000,
            with_payload=True,
        )

        exports = []
        for point in results:
            payload = point.payload
            vendor_data = {
                "vendor_id": payload.get("vendor_id"),
                "name": payload.get("name"),
                "customer_id": payload.get("customer_id"),
                "risk_score": payload.get("risk_score"),
                "risk_level": payload.get("risk_level"),
                "support_status": payload.get("support_status"),
                "country": payload.get("country"),
                "industry_focus": payload.get("industry_focus", []),
                "supply_chain_tier": payload.get("supply_chain_tier"),
                "total_cves": payload.get("total_cves", 0),
                "avg_cvss_score": payload.get("avg_cvss_score", 0.0),
            }

            if include_equipment:
                eq_list = self.search_equipment(
                    EquipmentSearchRequest(vendor_id=payload.get("vendor_id"))
                )
                vendor_data["equipment"] = [
                    {"model_id": e.equipment.model_id, "model_name": e.equipment.model_name}
                    for e in eq_list
                ]

            if include_cves:
                cves = self.get_vendor_cves(payload.get("vendor_id"))
                vendor_data["cves"] = [
                    {"cve_id": c.cve_id, "cvss_score": c.cvss_score, "severity": c.severity}
                    for c in cves
                ]

            exports.append(vendor_data)

        if format == "csv_rows":
            # Flatten for CSV export
            csv_rows = []
            for v in exports:
                row = {k: v for k, v in v.items() if not isinstance(v, list)}
                row["industry_focus"] = "|".join(v.get("industry_focus", []))
                csv_rows.append(row)
            return csv_rows

        return exports

    def export_equipment(
        self,
        vendor_id: Optional[str] = None,
        lifecycle_status: Optional[str] = None,
        format: str = "dict",
    ) -> List[Dict[str, Any]]:
        """
        Export equipment models for the current customer.

        Args:
            vendor_id: Filter by vendor (optional)
            lifecycle_status: Filter by lifecycle status (optional)
            format: Output format ('dict' or 'csv_rows')

        Returns:
            List of equipment dictionaries or CSV row data
        """
        context = self._get_customer_context()

        conditions = [
            FieldCondition(key="entity_type", match=MatchValue(value="equipment_model")),
        ]

        if vendor_id:
            conditions.append(
                FieldCondition(key="vendor_id", match=MatchValue(value=vendor_id))
            )

        if lifecycle_status:
            conditions.append(
                FieldCondition(key="lifecycle_status", match=MatchValue(value=lifecycle_status))
            )

        query_filter = self._build_customer_filter(
            customer_id=context.customer_id,
            include_system=True,
            additional_conditions=conditions,
        )

        results, _ = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=query_filter,
            limit=10000,
            with_payload=True,
        )

        exports = []
        for point in results:
            payload = point.payload
            eq_data = {
                "model_id": payload.get("model_id"),
                "vendor_id": payload.get("vendor_id"),
                "model_name": payload.get("model_name"),
                "customer_id": payload.get("customer_id"),
                "product_line": payload.get("product_line"),
                "category": payload.get("category"),
                "criticality": payload.get("criticality"),
                "eol_date": payload.get("eol_date"),
                "eos_date": payload.get("eos_date"),
                "lifecycle_status": payload.get("lifecycle_status"),
                "firmware_version": payload.get("firmware_version"),
                "vulnerability_count": payload.get("vulnerability_count", 0),
                "deployed_count": payload.get("deployed_count", 0),
            }
            exports.append(eq_data)

        return exports

    # =========================================================================
    # Reporting and Analytics (Day 6)
    # =========================================================================

    def get_dashboard_summary(self) -> Dict[str, Any]:
        """
        Get comprehensive dashboard summary for vendor equipment.

        Returns:
            Dictionary with counts, alerts, and key metrics
        """
        context = self._get_customer_context()

        # Get vendor count
        vendor_filter = self._build_customer_filter(
            customer_id=context.customer_id,
            include_system=True,
            additional_conditions=[
                FieldCondition(key="entity_type", match=MatchValue(value="vendor")),
            ],
        )
        vendor_results, _ = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=vendor_filter,
            limit=10000,
        )
        vendor_count = len(vendor_results)

        # Get equipment by lifecycle status
        eq_filter = self._build_customer_filter(
            customer_id=context.customer_id,
            include_system=True,
            additional_conditions=[
                FieldCondition(key="entity_type", match=MatchValue(value="equipment_model")),
            ],
        )
        eq_results, _ = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=eq_filter,
            limit=10000,
            with_payload=True,
        )

        lifecycle_counts = {"current": 0, "approaching_eol": 0, "eol": 0, "eos": 0}
        criticality_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
        total_deployed = 0
        total_vulnerabilities = 0

        for point in eq_results:
            payload = point.payload
            status = payload.get("lifecycle_status", "current")
            lifecycle_counts[status] = lifecycle_counts.get(status, 0) + 1
            crit = payload.get("criticality", "medium")
            criticality_counts[crit] = criticality_counts.get(crit, 0) + 1
            total_deployed += payload.get("deployed_count", 0)
            total_vulnerabilities += payload.get("vulnerability_count", 0)

        # Get alert summary
        alerts = self.get_all_lifecycle_alerts()

        # Get CVE summary
        cve_filter = self._build_customer_filter(
            customer_id=context.customer_id,
            include_system=True,
            additional_conditions=[
                FieldCondition(key="entity_type", match=MatchValue(value="cve")),
            ],
        )
        cve_results, _ = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=cve_filter,
            limit=10000,
            with_payload=True,
        )

        cve_severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
        for point in cve_results:
            payload = point.payload
            sev = payload.get("severity", "low")
            cve_severity_counts[sev] = cve_severity_counts.get(sev, 0) + 1

        return {
            "customer_id": context.customer_id,
            "summary": {
                "total_vendors": vendor_count,
                "total_equipment": len(eq_results),
                "total_deployed_assets": total_deployed,
                "total_vulnerabilities": total_vulnerabilities,
                "total_cves": len(cve_results),
            },
            "equipment_by_lifecycle": lifecycle_counts,
            "equipment_by_criticality": criticality_counts,
            "cves_by_severity": cve_severity_counts,
            "alerts": {
                "total": alerts["total_alerts"],
                "critical": alerts["total_critical"],
                "high": alerts["total_high"],
                "eol_alert_count": len(alerts["eol_alerts"]),
                "contract_alert_count": len(alerts["contract_alerts"]),
            },
        }

    def get_vendor_analytics(
        self,
        vendor_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get analytics for vendors including equipment counts and risk metrics.

        Args:
            vendor_id: Filter to specific vendor (optional)

        Returns:
            List of vendor analytics dictionaries
        """
        context = self._get_customer_context()

        conditions = [
            FieldCondition(key="entity_type", match=MatchValue(value="vendor")),
        ]

        if vendor_id:
            conditions.append(
                FieldCondition(key="vendor_id", match=MatchValue(value=vendor_id))
            )

        query_filter = self._build_customer_filter(
            customer_id=context.customer_id,
            include_system=True,
            additional_conditions=conditions,
        )

        results, _ = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=query_filter,
            limit=1000,
            with_payload=True,
        )

        analytics = []
        for point in results:
            payload = point.payload
            vid = payload.get("vendor_id")

            # Get equipment for this vendor
            eq_list = self.search_equipment(EquipmentSearchRequest(vendor_id=vid, limit=1000))

            lifecycle_counts = {"current": 0, "approaching_eol": 0, "eol": 0, "eos": 0}
            total_vulnerabilities = 0
            total_deployed = 0

            for eq in eq_list:
                status = eq.equipment.lifecycle_status.value
                lifecycle_counts[status] = lifecycle_counts.get(status, 0) + 1
                total_vulnerabilities += eq.equipment.vulnerability_count
                total_deployed += eq.equipment.deployed_count

            # Get CVE count
            cves = self.get_vendor_cves(vid)

            analytics.append({
                "vendor_id": vid,
                "vendor_name": payload.get("name"),
                "risk_score": payload.get("risk_score"),
                "risk_level": payload.get("risk_level"),
                "support_status": payload.get("support_status"),
                "equipment_count": len(eq_list),
                "equipment_by_lifecycle": lifecycle_counts,
                "total_deployed_assets": total_deployed,
                "total_vulnerabilities": total_vulnerabilities,
                "cve_count": len(cves),
                "critical_cve_count": len([c for c in cves if c.severity == "critical"]),
            })

        # Sort by risk score descending
        analytics.sort(key=lambda a: a.get("risk_score", 0), reverse=True)
        return analytics

    def get_lifecycle_report(
        self,
        days_ahead: int = 180,
    ) -> Dict[str, Any]:
        """
        Generate comprehensive lifecycle report for planning.

        Args:
            days_ahead: Look ahead window for EOL/EOS dates

        Returns:
            Report dictionary with timeline, impact, and recommendations
        """
        context = self._get_customer_context()

        # Get all EOL alerts
        eol_alerts = self.get_eol_alerts(days_ahead=days_ahead)
        contract_alerts = self.get_contract_expiration_alerts(days_ahead=days_ahead)

        # Group EOL alerts by time period
        timeline = {
            "past_due": [],
            "next_7_days": [],
            "next_30_days": [],
            "next_90_days": [],
            "next_180_days": [],
        }

        total_affected_assets = 0

        for alert in eol_alerts:
            entry = {
                "entity_id": alert.entity_id,
                "entity_name": alert.entity_name,
                "alert_type": alert.alert_type.value,
                "days_remaining": alert.days_remaining,
                "target_date": alert.target_date.isoformat() if alert.target_date else None,
                "affected_assets": alert.affected_asset_count,
                "severity": alert.severity.value,
            }
            total_affected_assets += alert.affected_asset_count

            if alert.days_remaining < 0:
                timeline["past_due"].append(entry)
            elif alert.days_remaining <= 7:
                timeline["next_7_days"].append(entry)
            elif alert.days_remaining <= 30:
                timeline["next_30_days"].append(entry)
            elif alert.days_remaining <= 90:
                timeline["next_90_days"].append(entry)
            else:
                timeline["next_180_days"].append(entry)

        # Generate recommendations
        recommendations = []
        if timeline["past_due"]:
            recommendations.append({
                "priority": "critical",
                "action": "Immediate replacement required",
                "affected_count": len(timeline["past_due"]),
                "description": f"{len(timeline['past_due'])} equipment past EOL/EOS - urgent migration needed",
            })

        if timeline["next_7_days"]:
            recommendations.append({
                "priority": "critical",
                "action": "Emergency planning",
                "affected_count": len(timeline["next_7_days"]),
                "description": f"{len(timeline['next_7_days'])} equipment reaching EOL within 7 days",
            })

        if timeline["next_30_days"]:
            recommendations.append({
                "priority": "high",
                "action": "Initiate migration projects",
                "affected_count": len(timeline["next_30_days"]),
                "description": f"{len(timeline['next_30_days'])} equipment reaching EOL within 30 days",
            })

        if contract_alerts:
            expiring_soon = [a for a in contract_alerts if 0 <= a.days_remaining <= 30]
            if expiring_soon:
                recommendations.append({
                    "priority": "high",
                    "action": "Contract renewal",
                    "affected_count": len(expiring_soon),
                    "description": f"{len(expiring_soon)} support contracts expiring within 30 days",
                })

        return {
            "customer_id": context.customer_id,
            "report_date": date.today().isoformat(),
            "look_ahead_days": days_ahead,
            "summary": {
                "total_eol_alerts": len(eol_alerts),
                "total_contract_alerts": len(contract_alerts),
                "total_affected_assets": total_affected_assets,
                "past_due_count": len(timeline["past_due"]),
                "critical_next_7_days": len(timeline["next_7_days"]),
            },
            "timeline": timeline,
            "contract_alerts": [
                {
                    "contract_id": a.entity_id,
                    "days_remaining": a.days_remaining,
                    "severity": a.severity.value,
                }
                for a in contract_alerts
            ],
            "recommendations": recommendations,
        }

    # =========================================================================
    # Maintenance Window Management (Day 7)
    # =========================================================================

    def create_maintenance_window(
        self,
        window: "MaintenanceWindow",
    ) -> str:
        """
        Create a maintenance window for scheduling maintenance activities.

        Args:
            window: MaintenanceWindow dataclass instance

        Returns:
            window_id of the created window
        """
        from .vendor_models import MaintenanceWindow as MWModel

        context = self._get_customer_context()

        # Override customer_id with current context
        window.customer_id = context.customer_id

        # Generate embedding from window name and description
        text = f"{window.name} {window.description or ''} {window.window_type.value}"
        embedding = self.embedding_service.encode(text)

        # Store in Qdrant
        point = PointStruct(
            id=str(uuid4()),
            vector=embedding,
            payload=window.to_qdrant_payload(),
        )

        self.qdrant_client.upsert(
            collection_name=self.COLLECTION_NAME,
            points=[point],
        )

        return window.window_id

    def get_maintenance_window(
        self,
        window_id: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Get a maintenance window by ID.

        Args:
            window_id: The window identifier

        Returns:
            Window data dictionary or None if not found
        """
        context = self._get_customer_context()

        query_filter = self._build_customer_filter(
            customer_id=context.customer_id,
            additional_conditions=[
                FieldCondition(key="entity_type", match=MatchValue(value="maintenance_window")),
                FieldCondition(key="window_id", match=MatchValue(value=window_id)),
            ],
        )

        results, _ = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=query_filter,
            limit=1,
            with_payload=True,
        )

        if results:
            return results[0].payload
        return None

    def list_maintenance_windows(
        self,
        active_only: bool = True,
        window_type: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        List maintenance windows for the current customer.

        Args:
            active_only: Only return active windows
            window_type: Filter by window type

        Returns:
            List of maintenance window dictionaries
        """
        context = self._get_customer_context()

        conditions = [
            FieldCondition(key="entity_type", match=MatchValue(value="maintenance_window")),
        ]

        if active_only:
            conditions.append(
                FieldCondition(key="is_active", match=MatchValue(value=True))
            )

        if window_type:
            # Use .value for enum types
            wt_value = window_type.value if hasattr(window_type, 'value') else window_type
            conditions.append(
                FieldCondition(key="window_type", match=MatchValue(value=wt_value))
            )

        query_filter = self._build_customer_filter(
            customer_id=context.customer_id,
            additional_conditions=conditions,
        )

        results, _ = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=query_filter,
            limit=1000,
            with_payload=True,
        )

        return [point.payload for point in results]

    def get_available_windows(
        self,
        equipment_id: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get available maintenance windows for equipment within a date range.

        Args:
            equipment_id: Filter for specific equipment
            start_date: Start of search range
            end_date: End of search range

        Returns:
            List of available windows with next occurrence dates
        """
        from datetime import timedelta

        windows = self.list_maintenance_windows(active_only=True)

        if start_date is None:
            start_date = date.today()
        if end_date is None:
            end_date = start_date + timedelta(days=30)

        start_dt = datetime.combine(start_date, datetime.min.time())
        end_dt = datetime.combine(end_date, datetime.max.time())

        available = []
        for window in windows:
            # Check if equipment is in scope
            if equipment_id:
                eq_ids = window.get("equipment_ids", [])
                if eq_ids and equipment_id not in eq_ids:
                    continue

            # Parse start time
            start_time_str = window.get("start_time")
            if start_time_str:
                try:
                    window_start = datetime.fromisoformat(start_time_str)
                except ValueError:
                    continue

                # Check if window is within range or has future occurrence
                is_recurring = window.get("is_recurring", False)

                if is_recurring:
                    pattern = window.get("recurrence_pattern", "weekly")
                    # Calculate next occurrence
                    next_occurrence = window_start
                    while next_occurrence < start_dt:
                        if pattern == "daily":
                            next_occurrence += timedelta(days=1)
                        elif pattern == "weekly":
                            next_occurrence += timedelta(weeks=1)
                        elif pattern == "monthly":
                            next_occurrence += timedelta(days=30)
                        elif pattern == "quarterly":
                            next_occurrence += timedelta(days=90)
                        else:
                            break

                    if next_occurrence <= end_dt:
                        window["next_occurrence"] = next_occurrence.isoformat()
                        available.append(window)
                else:
                    if start_dt <= window_start <= end_dt:
                        window["next_occurrence"] = window_start.isoformat()
                        available.append(window)

        # Sort by next occurrence
        available.sort(key=lambda w: w.get("next_occurrence", ""))
        return available

    def check_maintenance_conflict(
        self,
        equipment_id: str,
        proposed_start: datetime,
        proposed_end: datetime,
    ) -> Dict[str, Any]:
        """
        Check if proposed maintenance time conflicts with existing windows or work orders.

        Args:
            equipment_id: Equipment to check
            proposed_start: Proposed maintenance start time
            proposed_end: Proposed maintenance end time

        Returns:
            Dictionary with conflict status and details
        """
        conflicts = []

        # Check change freeze windows
        windows = self.list_maintenance_windows(active_only=True, window_type="change_freeze")

        for window in windows:
            eq_ids = window.get("equipment_ids", [])
            if eq_ids and equipment_id not in eq_ids:
                continue

            start_time_str = window.get("start_time")
            end_time_str = window.get("end_time")

            if start_time_str and end_time_str:
                try:
                    w_start = datetime.fromisoformat(start_time_str)
                    w_end = datetime.fromisoformat(end_time_str)

                    # Check for overlap
                    if proposed_start < w_end and proposed_end > w_start:
                        conflicts.append({
                            "type": "change_freeze",
                            "window_id": window.get("window_id"),
                            "window_name": window.get("name"),
                            "start": w_start.isoformat(),
                            "end": w_end.isoformat(),
                        })
                except ValueError:
                    pass

        # Check existing work orders
        work_orders = self.list_work_orders(equipment_id=equipment_id, status="approved")
        for wo in work_orders:
            wo_start_str = wo.get("scheduled_start")
            wo_end_str = wo.get("scheduled_end")

            if wo_start_str and wo_end_str:
                try:
                    wo_start = datetime.fromisoformat(wo_start_str)
                    wo_end = datetime.fromisoformat(wo_end_str)

                    if proposed_start < wo_end and proposed_end > wo_start:
                        conflicts.append({
                            "type": "work_order",
                            "work_order_id": wo.get("work_order_id"),
                            "title": wo.get("title"),
                            "start": wo_start.isoformat(),
                            "end": wo_end.isoformat(),
                        })
                except ValueError:
                    pass

        return {
            "has_conflict": len(conflicts) > 0,
            "conflict_count": len(conflicts),
            "conflicts": conflicts,
            "proposed_start": proposed_start.isoformat(),
            "proposed_end": proposed_end.isoformat(),
        }

    # =========================================================================
    # Predictive Maintenance (Day 8)
    # =========================================================================

    def predict_maintenance(
        self,
        equipment_id: Optional[str] = None,
        days_ahead: int = 90,
    ) -> List["MaintenancePrediction"]:
        """
        Generate predictive maintenance recommendations.

        Uses equipment age, vulnerability count, criticality, and maintenance
        schedule to predict when maintenance should be performed.

        Args:
            equipment_id: Specific equipment ID, or None for all equipment
            days_ahead: Prediction window in days

        Returns:
            List of MaintenancePrediction objects
        """
        from .vendor_models import MaintenancePrediction
        from datetime import timedelta

        context = self._get_customer_context()

        # Get equipment
        if equipment_id:
            request = EquipmentSearchRequest(limit=1)
            equipment_list = [eq for eq in self.search_equipment(request) if eq.equipment.model_id == equipment_id]
        else:
            request = EquipmentSearchRequest(limit=1000)
            equipment_list = self.search_equipment(request)

        predictions = []
        today = date.today()

        for eq_result in equipment_list:
            equipment = eq_result.equipment

            # Calculate maintenance interval based on schedule
            schedule_intervals = {
                "monthly": 30,
                "quarterly": 90,
                "semi_annual": 180,
                "annual": 365,
                "on_demand": 180,  # Default to semi-annual if on-demand
            }

            schedule_value = equipment.maintenance_schedule.value if hasattr(equipment.maintenance_schedule, 'value') else str(equipment.maintenance_schedule)
            base_interval = schedule_intervals.get(schedule_value, 90)

            # Adjust interval based on factors
            risk_factors = []
            adjustment = 0

            # Factor 1: Vulnerability count
            if equipment.vulnerability_count > 10:
                adjustment -= 30
                risk_factors.append("High vulnerability count")
            elif equipment.vulnerability_count > 5:
                adjustment -= 15
                risk_factors.append("Elevated vulnerability count")

            # Factor 2: Criticality
            criticality_value = equipment.criticality.value if hasattr(equipment.criticality, 'value') else str(equipment.criticality)
            if criticality_value == "critical":
                adjustment -= 15
                risk_factors.append("Critical asset")
            elif criticality_value == "high":
                adjustment -= 7
                risk_factors.append("High-priority asset")

            # Factor 3: EOL proximity
            if eq_result.days_to_eol is not None:
                if eq_result.days_to_eol <= 0:
                    adjustment -= 30
                    risk_factors.append("Past end-of-life")
                elif eq_result.days_to_eol <= 90:
                    adjustment -= 20
                    risk_factors.append("Approaching end-of-life")
                elif eq_result.days_to_eol <= 180:
                    adjustment -= 10
                    risk_factors.append("EOL within 6 months")

            # Factor 4: High deployment count (more instances = higher priority)
            if equipment.deployed_count > 50:
                adjustment -= 10
                risk_factors.append("Large deployment footprint")
            elif equipment.deployed_count > 20:
                adjustment -= 5
                risk_factors.append("Moderate deployment footprint")

            # Calculate adjusted interval
            adjusted_interval = max(base_interval + adjustment, 14)  # Minimum 14 days

            # Estimate last maintenance (use equipment age as proxy)
            # Assume last maintenance was at the normal interval
            last_maintenance = today - timedelta(days=adjusted_interval)

            # Calculate next maintenance date
            next_maintenance = last_maintenance + timedelta(days=adjusted_interval)
            if next_maintenance < today:
                next_maintenance = today + timedelta(days=7)  # Overdue, schedule soon

            days_until = (next_maintenance - today).days

            # Skip if beyond prediction window
            if days_until > days_ahead:
                continue

            # Calculate risk score (0-10)
            risk_score = min(10.0, len(risk_factors) * 2.0 + (equipment.vulnerability_count * 0.2))

            # Calculate confidence based on data quality
            confidence = 0.7  # Base confidence
            if risk_factors:
                confidence += 0.1
            if equipment.vulnerability_count > 0:
                confidence += 0.1
            confidence = min(1.0, confidence)

            # Generate recommended tasks
            recommended_tasks = []
            if equipment.vulnerability_count > 0:
                recommended_tasks.append("Apply security patches")
            if criticality_value in ["critical", "high"]:
                recommended_tasks.append("Verify backup systems")
            if eq_result.days_to_eol is not None and eq_result.days_to_eol <= 180:
                recommended_tasks.append("Assess migration options")
            recommended_tasks.append("Verify configuration compliance")
            recommended_tasks.append("Update documentation")

            # Estimate downtime based on maintenance type
            estimated_downtime = 2.0 if schedule_value in ["monthly", "quarterly"] else 4.0
            if equipment.vulnerability_count > 5:
                estimated_downtime += 1.0

            # Build prediction reason
            if risk_factors:
                reason = f"Due to {', '.join(risk_factors[:2])}"
            else:
                reason = f"Regular {schedule_value} maintenance schedule"

            prediction = MaintenancePrediction(
                equipment_id=equipment.model_id,
                equipment_name=equipment.model_name,
                customer_id=context.customer_id,
                next_maintenance_date=next_maintenance,
                confidence_score=confidence,
                prediction_reason=reason,
                days_until_maintenance=days_until,
                risk_score=risk_score,
                risk_factors=risk_factors,
                last_maintenance_date=last_maintenance,
                maintenance_count=0,  # Would need historical data
                avg_days_between_maintenance=float(adjusted_interval),
                recommended_tasks=recommended_tasks,
                estimated_downtime_hours=estimated_downtime,
                estimated_cost=estimated_downtime * 500.0,  # Simple cost estimate
            )

            predictions.append(prediction)

        # Sort by days until maintenance (soonest first)
        predictions.sort(key=lambda p: p.days_until_maintenance)
        return predictions

    def get_maintenance_forecast(
        self,
        months_ahead: int = 6,
    ) -> Dict[str, Any]:
        """
        Generate maintenance forecast for capacity planning.

        Args:
            months_ahead: Number of months to forecast

        Returns:
            Dictionary with monthly maintenance counts and resource estimates
        """
        from datetime import timedelta

        predictions = self.predict_maintenance(days_ahead=months_ahead * 30)

        # Group by month
        monthly_forecast = {}
        today = date.today()

        for i in range(months_ahead):
            month_start = date(today.year + (today.month + i - 1) // 12, (today.month + i - 1) % 12 + 1, 1)
            month_key = month_start.strftime("%Y-%m")
            monthly_forecast[month_key] = {
                "maintenance_count": 0,
                "critical_count": 0,
                "high_count": 0,
                "estimated_hours": 0.0,
                "estimated_cost": 0.0,
                "equipment_ids": [],
            }

        for pred in predictions:
            pred_date = pred.next_maintenance_date
            month_key = pred_date.strftime("%Y-%m")

            if month_key in monthly_forecast:
                monthly_forecast[month_key]["maintenance_count"] += 1
                monthly_forecast[month_key]["estimated_hours"] += pred.estimated_downtime_hours
                monthly_forecast[month_key]["estimated_cost"] += pred.estimated_cost
                monthly_forecast[month_key]["equipment_ids"].append(pred.equipment_id)

                if pred.risk_score >= 8:
                    monthly_forecast[month_key]["critical_count"] += 1
                elif pred.risk_score >= 5:
                    monthly_forecast[month_key]["high_count"] += 1

        # Calculate totals
        total_maintenance = sum(m["maintenance_count"] for m in monthly_forecast.values())
        total_hours = sum(m["estimated_hours"] for m in monthly_forecast.values())
        total_cost = sum(m["estimated_cost"] for m in monthly_forecast.values())

        return {
            "forecast_months": months_ahead,
            "total_maintenance_events": total_maintenance,
            "total_estimated_hours": total_hours,
            "total_estimated_cost": total_cost,
            "monthly_breakdown": monthly_forecast,
            "generated_at": datetime.utcnow().isoformat(),
        }

    # =========================================================================
    # Work Order Management (Day 9)
    # =========================================================================

    def create_work_order(
        self,
        work_order: "MaintenanceWorkOrder",
    ) -> str:
        """
        Create a maintenance work order.

        Args:
            work_order: MaintenanceWorkOrder dataclass instance

        Returns:
            work_order_id of the created work order
        """
        context = self._get_customer_context()

        # Override customer_id with current context
        work_order.customer_id = context.customer_id

        # Generate embedding from title and description
        text = f"{work_order.title} {work_order.description or ''}"
        embedding = self.embedding_service.encode(text)

        # Store in Qdrant
        point = PointStruct(
            id=str(uuid4()),
            vector=embedding,
            payload=work_order.to_qdrant_payload(),
        )

        self.qdrant_client.upsert(
            collection_name=self.COLLECTION_NAME,
            points=[point],
        )

        return work_order.work_order_id

    def get_work_order(
        self,
        work_order_id: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Get a work order by ID.

        Args:
            work_order_id: The work order identifier

        Returns:
            Work order data dictionary or None if not found
        """
        context = self._get_customer_context()

        query_filter = self._build_customer_filter(
            customer_id=context.customer_id,
            additional_conditions=[
                FieldCondition(key="entity_type", match=MatchValue(value="work_order")),
                FieldCondition(key="work_order_id", match=MatchValue(value=work_order_id)),
            ],
        )

        results, _ = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=query_filter,
            limit=1,
            with_payload=True,
        )

        if results:
            return results[0].payload
        return None

    def list_work_orders(
        self,
        equipment_id: Optional[str] = None,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        assigned_to: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        List work orders with optional filters.

        Args:
            equipment_id: Filter by equipment
            status: Filter by status
            priority: Filter by priority
            assigned_to: Filter by assignee

        Returns:
            List of work order dictionaries
        """
        context = self._get_customer_context()

        conditions = [
            FieldCondition(key="entity_type", match=MatchValue(value="work_order")),
        ]

        if status:
            # Use .value for enum types
            status_value = status.value if hasattr(status, 'value') else status
            conditions.append(
                FieldCondition(key="status", match=MatchValue(value=status_value))
            )

        if priority:
            # Use .value for enum types
            priority_value = priority.value if hasattr(priority, 'value') else priority
            conditions.append(
                FieldCondition(key="priority", match=MatchValue(value=priority_value))
            )

        if assigned_to:
            conditions.append(
                FieldCondition(key="assigned_to", match=MatchValue(value=assigned_to))
            )

        query_filter = self._build_customer_filter(
            customer_id=context.customer_id,
            additional_conditions=conditions,
        )

        results, _ = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=query_filter,
            limit=1000,
            with_payload=True,
        )

        work_orders = [point.payload for point in results]

        # Filter by equipment_id if specified (check list membership)
        if equipment_id:
            work_orders = [
                wo for wo in work_orders
                if equipment_id in wo.get("equipment_ids", [])
            ]

        return work_orders

    def update_work_order_status(
        self,
        work_order_id: str,
        new_status: str,
        notes: Optional[str] = None,
    ) -> bool:
        """
        Update work order status.

        Args:
            work_order_id: Work order to update
            new_status: New status value
            notes: Optional completion/status notes

        Returns:
            True if updated successfully
        """
        context = self._get_customer_context()

        # Find the work order
        query_filter = self._build_customer_filter(
            customer_id=context.customer_id,
            additional_conditions=[
                FieldCondition(key="entity_type", match=MatchValue(value="work_order")),
                FieldCondition(key="work_order_id", match=MatchValue(value=work_order_id)),
            ],
        )

        results, _ = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=query_filter,
            limit=1,
            with_payload=True,
            with_vectors=True,
        )

        if not results:
            return False

        point = results[0]
        payload = dict(point.payload)
        # Use .value for enum types
        status_value = new_status.value if hasattr(new_status, 'value') else new_status
        payload["status"] = status_value

        if notes:
            payload["completion_notes"] = notes

        # Track status change times
        if status_value == "in_progress" and not payload.get("actual_start"):
            payload["actual_start"] = datetime.utcnow().isoformat()
        elif status_value in ["completed", "failed", "cancelled"]:
            payload["actual_end"] = datetime.utcnow().isoformat()

        # Update in Qdrant
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

        return True

    def get_work_order_summary(self) -> Dict[str, Any]:
        """
        Get summary of work orders by status.

        Returns:
            Dictionary with status counts and metrics
        """
        context = self._get_customer_context()

        query_filter = self._build_customer_filter(
            customer_id=context.customer_id,
            additional_conditions=[
                FieldCondition(key="entity_type", match=MatchValue(value="work_order")),
            ],
        )

        results, _ = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=query_filter,
            limit=10000,
            with_payload=True,
        )

        status_counts = {
            "draft": 0,
            "pending": 0,
            "approved": 0,
            "in_progress": 0,
            "on_hold": 0,
            "completed": 0,
            "cancelled": 0,
            "failed": 0,
        }

        priority_counts = {
            "low": 0,
            "medium": 0,
            "high": 0,
            "critical": 0,
            "emergency": 0,
        }

        overdue_count = 0
        now = datetime.utcnow()

        for point in results:
            payload = point.payload
            status = payload.get("status", "draft")
            priority = payload.get("priority", "medium")

            status_counts[status] = status_counts.get(status, 0) + 1
            priority_counts[priority] = priority_counts.get(priority, 0) + 1

            # Check if overdue
            if status not in ["completed", "cancelled", "failed"]:
                scheduled_end_str = payload.get("scheduled_end")
                if scheduled_end_str:
                    try:
                        scheduled_end = datetime.fromisoformat(scheduled_end_str)
                        if now > scheduled_end:
                            overdue_count += 1
                    except ValueError:
                        pass

        return {
            "customer_id": context.customer_id,
            "total_work_orders": len(results),
            "status_breakdown": status_counts,
            "priority_breakdown": priority_counts,
            "overdue_count": overdue_count,
            "active_count": status_counts.get("in_progress", 0) + status_counts.get("approved", 0),
            "pending_approval": status_counts.get("pending", 0),
        }

    def create_work_order_from_prediction(
        self,
        prediction: "MaintenancePrediction",
        title_prefix: str = "Scheduled Maintenance",
        assigned_to: Optional[str] = None,
    ) -> str:
        """
        Create a work order from a maintenance prediction.

        Args:
            prediction: MaintenancePrediction to convert
            title_prefix: Prefix for work order title
            assigned_to: Optional assignee

        Returns:
            work_order_id of created work order
        """
        from .vendor_models import MaintenanceWorkOrder, WorkOrderStatus, WorkOrderPriority
        from datetime import timedelta

        # Determine priority from risk score
        if prediction.risk_score >= 8:
            priority = WorkOrderPriority.CRITICAL
        elif prediction.risk_score >= 6:
            priority = WorkOrderPriority.HIGH
        elif prediction.risk_score >= 4:
            priority = WorkOrderPriority.MEDIUM
        else:
            priority = WorkOrderPriority.LOW

        # Create scheduled times
        scheduled_start = datetime.combine(prediction.next_maintenance_date, datetime.min.time().replace(hour=9))
        scheduled_end = scheduled_start + timedelta(hours=prediction.estimated_downtime_hours)

        work_order = MaintenanceWorkOrder(
            work_order_id=f"WO-{uuid4().hex[:8].upper()}",
            customer_id=prediction.customer_id,
            title=f"{title_prefix}: {prediction.equipment_name}",
            equipment_ids=[prediction.equipment_id],
            status=WorkOrderStatus.DRAFT,
            priority=priority,
            scheduled_start=scheduled_start,
            scheduled_end=scheduled_end,
            description=prediction.prediction_reason,
            tasks=prediction.recommended_tasks,
            estimated_hours=prediction.estimated_downtime_hours,
            estimated_cost=prediction.estimated_cost,
            assigned_to=assigned_to,
        )

        return self.create_work_order(work_order)
