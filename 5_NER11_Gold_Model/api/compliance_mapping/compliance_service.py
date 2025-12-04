"""
Compliance Mapping Service
===========================

Service layer for E07: Compliance Framework Mapping.
Provides CRUD operations, semantic search, and compliance tracking
with customer isolation and Qdrant vector storage.

Version: 1.0.0
Created: 2025-12-04
"""

from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional, List, Dict, Any
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
)
from sentence_transformers import SentenceTransformer

from ..customer_isolation import CustomerContext, CustomerContextManager

logger = logging.getLogger(__name__)


# =============================================================================
# Search Request/Response Models
# =============================================================================


@dataclass
class ControlSearchRequest:
    """Request parameters for control search."""
    query: Optional[str] = None
    customer_id: Optional[str] = None
    framework: Optional[str] = None
    control_family: Optional[str] = None
    priority: Optional[str] = None
    implementation_status: Optional[str] = None
    limit: int = 50
    include_system: bool = True


@dataclass
class ControlSearchResult:
    """Single control search result."""
    control: Any
    score: float = 0.0


@dataclass
class AssessmentSearchRequest:
    """Request parameters for assessment search."""
    customer_id: Optional[str] = None
    control_id: Optional[str] = None
    status: Optional[str] = None
    limit: int = 50


@dataclass
class AssessmentSearchResult:
    """Single assessment search result."""
    assessment: Any
    score: float = 0.0


# =============================================================================
# Compliance Service
# =============================================================================


class ComplianceService:
    """
    Service for compliance framework mapping and management.

    Provides customer-isolated operations for:
    - Control management
    - Framework mappings
    - Compliance assessments
    - Evidence tracking
    - Gap analysis
    """

    COLLECTION_NAME = "ner11_compliance"
    VECTOR_SIZE = 384  # sentence-transformers/all-MiniLM-L6-v2

    def __init__(
        self,
        qdrant_url: str = "http://localhost:6333",
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
    ):
        """Initialize compliance service."""
        self.qdrant_client = QdrantClient(url=qdrant_url)
        self._embedding_model = SentenceTransformer(embedding_model)
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
        """Generate embedding for text."""
        embedding = self._embedding_model.encode(text)
        return embedding.tolist()

    def _generate_point_id(self) -> str:
        """Generate unique point ID."""
        return str(uuid4())

    # =========================================================================
    # Control Operations
    # =========================================================================

    def create_control(self, control: Any) -> Any:
        """Create a new control with customer isolation."""
        context = self._get_customer_context()

        if not context.can_write():
            raise PermissionError("Write access required to create control")

        if control.customer_id != context.customer_id:
            raise ValueError("Control customer_id must match context customer_id")

        embed_text = f"{control.control_number} {control.title} {control.description}"
        embedding = self._generate_embedding(embed_text)

        point_id = self._generate_point_id()
        self.qdrant_client.upsert(
            collection_name=self.COLLECTION_NAME,
            points=[
                PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload=control.to_qdrant_payload(),
                )
            ],
        )

        logger.info(f"Created control {control.control_id}: {control.control_number}")
        return control

    def get_control(self, control_id: str) -> Optional[Any]:
        """Get control by ID with customer isolation."""
        context = self._get_customer_context()

        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(key="control_id", match=MatchValue(value=control_id)),
                    FieldCondition(
                        key="customer_id",
                        match=MatchAny(any=context.get_customer_ids()),
                    ),
                    FieldCondition(key="entity_type", match=MatchValue(value="control")),
                ]
            ),
            limit=1,
        )

        if results[0]:
            from .compliance_models import ComplianceControl, ControlPriority, ImplementationStatus, ControlType
            payload = results[0][0].payload
            return ComplianceControl(
                control_id=payload["control_id"],
                control_number=payload["control_number"],
                customer_id=payload["customer_id"],
                framework=payload["framework"],
                title=payload["title"],
                description=payload.get("description", ""),
                control_family=payload["control_family"],
                priority=ControlPriority(payload.get("priority", "medium")),
                implementation_status=ImplementationStatus(payload.get("implementation_status", "not_started")),
                control_type=ControlType(payload.get("control_type", "preventive")),
                automated=payload.get("automated", False),
                responsible_party=payload.get("responsible_party"),
                review_frequency=payload.get("review_frequency"),
                last_assessment=datetime.fromisoformat(payload["last_assessment"]).date() if payload.get("last_assessment") else None,
            )
        return None

    def update_control(self, control: Any) -> Any:
        """Update an existing control."""
        context = self._get_customer_context()

        if not context.can_write():
            raise PermissionError("Write access required to update control")

        # Delete old version and insert new one
        self.delete_control(control.control_id)
        return self.create_control(control)

    def delete_control(self, control_id: str) -> bool:
        """Delete a control."""
        context = self._get_customer_context()

        if not context.can_write():
            raise PermissionError("Write access required to delete control")

        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(key="control_id", match=MatchValue(value=control_id)),
                    FieldCondition(key="customer_id", match=MatchValue(value=context.customer_id)),
                    FieldCondition(key="entity_type", match=MatchValue(value="control")),
                ]
            ),
            limit=1,
        )

        if results[0]:
            point_id = results[0][0].id
            self.qdrant_client.delete(
                collection_name=self.COLLECTION_NAME,
                points_selector=[point_id],
            )
            return True
        return False

    def search_controls(self, request: ControlSearchRequest) -> List[ControlSearchResult]:
        """Search controls with filters and optional semantic search."""
        from .compliance_models import ComplianceControl, ControlPriority, ImplementationStatus, ControlType

        context = self._get_customer_context()
        customer_id = request.customer_id or context.customer_id

        conditions = [
            FieldCondition(key="entity_type", match=MatchValue(value="control"))
        ]

        if request.framework:
            conditions.append(
                FieldCondition(key="framework", match=MatchValue(value=request.framework))
            )

        if request.control_family:
            conditions.append(
                FieldCondition(key="control_family", match=MatchValue(value=request.control_family))
            )

        if request.priority:
            conditions.append(
                FieldCondition(key="priority", match=MatchValue(value=request.priority))
            )

        if request.implementation_status:
            conditions.append(
                FieldCondition(key="implementation_status", match=MatchValue(value=request.implementation_status))
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
                ControlSearchResult(
                    control=ComplianceControl(
                        control_id=r.payload["control_id"],
                        control_number=r.payload["control_number"],
                        customer_id=r.payload["customer_id"],
                        framework=r.payload["framework"],
                        title=r.payload["title"],
                        description=r.payload.get("description", ""),
                        control_family=r.payload["control_family"],
                        priority=ControlPriority(r.payload.get("priority", "medium")),
                        implementation_status=ImplementationStatus(r.payload.get("implementation_status", "not_started")),
                        control_type=ControlType(r.payload.get("control_type", "preventive")),
                        automated=r.payload.get("automated", False),
                        responsible_party=r.payload.get("responsible_party"),
                        review_frequency=r.payload.get("review_frequency"),
                    ),
                    score=r.score,
                )
                for r in results
            ]
        else:
            results = self.qdrant_client.scroll(
                collection_name=self.COLLECTION_NAME,
                scroll_filter=search_filter,
                limit=request.limit,
            )
            return [
                ControlSearchResult(
                    control=ComplianceControl(
                        control_id=p.payload["control_id"],
                        control_number=p.payload["control_number"],
                        customer_id=p.payload["customer_id"],
                        framework=p.payload["framework"],
                        title=p.payload["title"],
                        description=p.payload.get("description", ""),
                        control_family=p.payload["control_family"],
                        priority=ControlPriority(p.payload.get("priority", "medium")),
                        implementation_status=ImplementationStatus(p.payload.get("implementation_status", "not_started")),
                        control_type=ControlType(p.payload.get("control_type", "preventive")),
                        automated=p.payload.get("automated", False),
                        responsible_party=p.payload.get("responsible_party"),
                        review_frequency=p.payload.get("review_frequency"),
                    ),
                    score=1.0,
                )
                for p in results[0]
            ]

    def get_controls_by_framework(self, framework: str, limit: int = 100) -> List[ControlSearchResult]:
        """Get controls for a specific framework."""
        request = ControlSearchRequest(
            framework=framework,
            limit=limit,
        )
        return self.search_controls(request)

    # =========================================================================
    # Framework Mapping Operations
    # =========================================================================

    def create_mapping(self, mapping: Any) -> Any:
        """Create a new framework mapping."""
        context = self._get_customer_context()

        if not context.can_write():
            raise PermissionError("Write access required to create mapping")

        embed_text = f"{mapping.source_framework} {mapping.source_control_id} {mapping.target_framework} {mapping.target_control_id}"
        embedding = self._generate_embedding(embed_text)

        point_id = self._generate_point_id()
        self.qdrant_client.upsert(
            collection_name=self.COLLECTION_NAME,
            points=[
                PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload=mapping.to_qdrant_payload(),
                )
            ],
        )

        logger.info(f"Created mapping {mapping.mapping_id}")
        return mapping

    def get_mapping(self, mapping_id: str) -> Optional[Any]:
        """Get mapping by ID."""
        context = self._get_customer_context()

        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(key="mapping_id", match=MatchValue(value=mapping_id)),
                    FieldCondition(
                        key="customer_id",
                        match=MatchAny(any=context.get_customer_ids()),
                    ),
                    FieldCondition(key="entity_type", match=MatchValue(value="framework_mapping")),
                ]
            ),
            limit=1,
        )

        if results[0]:
            from .compliance_models import FrameworkMapping, RelationshipType
            payload = results[0][0].payload
            return FrameworkMapping(
                mapping_id=payload["mapping_id"],
                customer_id=payload["customer_id"],
                source_framework=payload["source_framework"],
                source_control_id=payload["source_control_id"],
                target_framework=payload["target_framework"],
                target_control_id=payload["target_control_id"],
                relationship_type=RelationshipType(payload.get("relationship_type", "equivalent")),
                confidence=payload.get("confidence", 80),
                notes=payload.get("notes"),
            )
        return None

    def get_cross_framework_mappings(
        self, source: str, target: str, min_confidence: int = 0, limit: int = 50
    ) -> List[Any]:
        """Get cross-framework mappings."""
        from .compliance_models import FrameworkMapping, RelationshipType
        context = self._get_customer_context()

        conditions = [
            FieldCondition(key="entity_type", match=MatchValue(value="framework_mapping")),
            FieldCondition(key="source_framework", match=MatchValue(value=source)),
            FieldCondition(key="target_framework", match=MatchValue(value=target)),
        ]

        if min_confidence > 0:
            conditions.append(
                FieldCondition(key="confidence", range=Range(gte=min_confidence))
            )

        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=self._build_customer_filter(
                context.customer_id,
                additional_conditions=conditions,
            ),
            limit=limit,
        )

        return [
            FrameworkMapping(
                mapping_id=p.payload["mapping_id"],
                customer_id=p.payload["customer_id"],
                source_framework=p.payload["source_framework"],
                source_control_id=p.payload["source_control_id"],
                target_framework=p.payload["target_framework"],
                target_control_id=p.payload["target_control_id"],
                relationship_type=RelationshipType(p.payload.get("relationship_type", "equivalent")),
                confidence=p.payload.get("confidence", 80),
                notes=p.payload.get("notes"),
            )
            for p in results[0]
        ]

    def get_mappings_for_control(self, control_id: str) -> List[Any]:
        """Get all mappings for a control."""
        from .compliance_models import FrameworkMapping, RelationshipType
        context = self._get_customer_context()

        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(key="entity_type", match=MatchValue(value="framework_mapping")),
                    FieldCondition(
                        key="customer_id",
                        match=MatchAny(any=context.get_customer_ids()),
                    ),
                ]
            ),
            limit=100,
        )

        mappings = []
        for p in results[0]:
            if p.payload.get("source_control_id") == control_id or p.payload.get("target_control_id") == control_id:
                mappings.append(
                    FrameworkMapping(
                        mapping_id=p.payload["mapping_id"],
                        customer_id=p.payload["customer_id"],
                        source_framework=p.payload["source_framework"],
                        source_control_id=p.payload["source_control_id"],
                        target_framework=p.payload["target_framework"],
                        target_control_id=p.payload["target_control_id"],
                        relationship_type=RelationshipType(p.payload.get("relationship_type", "equivalent")),
                        confidence=p.payload.get("confidence", 80),
                        notes=p.payload.get("notes"),
                    )
                )

        return mappings

    def auto_generate_mappings(
        self, source_framework: str, target_framework: str, min_confidence: int = 60
    ) -> Dict[str, Any]:
        """Auto-generate framework mappings using semantic similarity."""
        context = self._get_customer_context()

        if not context.can_write():
            raise PermissionError("Write access required to generate mappings")

        # Get source controls
        source_request = ControlSearchRequest(
            customer_id=context.customer_id,
            framework=source_framework,
            limit=100,
        )
        source_controls = self.search_controls(source_request)

        # Get target controls
        target_request = ControlSearchRequest(
            customer_id=context.customer_id,
            framework=target_framework,
            limit=100,
        )
        target_controls = self.search_controls(target_request)

        mappings_created = 0
        total_confidence = 0.0
        created_mappings = []

        for source in source_controls:
            source_text = f"{source.control.title} {source.control.description}"
            source_embedding = self._generate_embedding(source_text)

            best_match = None
            best_score = 0.0

            for target in target_controls:
                target_text = f"{target.control.title} {target.control.description}"
                target_embedding = self._generate_embedding(target_text)

                # Compute cosine similarity
                import numpy as np
                similarity = np.dot(source_embedding, target_embedding)
                confidence_score = int(similarity * 100)

                if confidence_score >= min_confidence and confidence_score > best_score:
                    best_match = target.control
                    best_score = confidence_score

            if best_match:
                from .compliance_models import FrameworkMapping, RelationshipType

                mapping = FrameworkMapping(
                    mapping_id=self._generate_point_id(),
                    customer_id=context.customer_id,
                    source_framework=source_framework,
                    source_control_id=source.control.control_id,
                    target_framework=target_framework,
                    target_control_id=best_match.control_id,
                    relationship_type=RelationshipType.SIMILAR if best_score < 80 else RelationshipType.EQUIVALENT,
                    confidence=best_score,
                    notes=f"Auto-generated mapping with {best_score}% confidence",
                )
                self.create_mapping(mapping)
                mappings_created += 1
                total_confidence += best_score
                created_mappings.append({
                    "source_control": source.control.control_number,
                    "target_control": best_match.control_number,
                    "confidence": best_score,
                })

        avg_confidence = total_confidence / mappings_created if mappings_created > 0 else 0.0

        return {
            "mappings_created": mappings_created,
            "average_confidence": round(avg_confidence, 2),
            "mappings": created_mappings,
        }

    # =========================================================================
    # Assessment Operations
    # =========================================================================

    def create_assessment(self, assessment: Any) -> Any:
        """Create a new assessment."""
        context = self._get_customer_context()

        if not context.can_write():
            raise PermissionError("Write access required to create assessment")

        embed_text = f"{assessment.control_id} {assessment.assessor} {' '.join(assessment.findings)}"
        embedding = self._generate_embedding(embed_text)

        point_id = self._generate_point_id()
        self.qdrant_client.upsert(
            collection_name=self.COLLECTION_NAME,
            points=[
                PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload=assessment.to_qdrant_payload(),
                )
            ],
        )

        logger.info(f"Created assessment {assessment.assessment_id}")
        return assessment

    def get_assessment(self, assessment_id: str) -> Optional[Any]:
        """Get assessment by ID."""
        from .compliance_models import ComplianceAssessment, AssessmentStatus
        context = self._get_customer_context()

        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(key="assessment_id", match=MatchValue(value=assessment_id)),
                    FieldCondition(
                        key="customer_id",
                        match=MatchAny(any=context.get_customer_ids()),
                    ),
                    FieldCondition(key="entity_type", match=MatchValue(value="assessment")),
                ]
            ),
            limit=1,
        )

        if results[0]:
            payload = results[0][0].payload
            return ComplianceAssessment(
                assessment_id=payload["assessment_id"],
                customer_id=payload["customer_id"],
                control_id=payload["control_id"],
                assessment_date=datetime.fromisoformat(payload["assessment_date"]).date(),
                assessor=payload["assessor"],
                status=AssessmentStatus(payload.get("status", "in_progress")),
                compliance_score=payload.get("compliance_score", 0),
                findings=payload.get("findings", []),
                recommendations=payload.get("recommendations", []),
                evidence_ids=payload.get("evidence_ids", []),
            )
        return None

    def update_assessment(self, assessment: Any) -> Any:
        """Update an existing assessment."""
        context = self._get_customer_context()

        if not context.can_write():
            raise PermissionError("Write access required to update assessment")

        # Delete and recreate
        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(key="assessment_id", match=MatchValue(value=assessment.assessment_id)),
                    FieldCondition(key="customer_id", match=MatchValue(value=context.customer_id)),
                ]
            ),
            limit=1,
        )

        if results[0]:
            self.qdrant_client.delete(
                collection_name=self.COLLECTION_NAME,
                points_selector=[results[0][0].id],
            )

        return self.create_assessment(assessment)

    def search_assessments(self, request: AssessmentSearchRequest) -> List[AssessmentSearchResult]:
        """Search assessments."""
        from .compliance_models import ComplianceAssessment, AssessmentStatus
        context = self._get_customer_context()

        conditions = [
            FieldCondition(key="entity_type", match=MatchValue(value="assessment"))
        ]

        if request.control_id:
            conditions.append(
                FieldCondition(key="control_id", match=MatchValue(value=request.control_id))
            )

        if request.status:
            conditions.append(
                FieldCondition(key="status", match=MatchValue(value=request.status))
            )

        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=self._build_customer_filter(
                context.customer_id,
                additional_conditions=conditions,
            ),
            limit=request.limit,
        )

        return [
            AssessmentSearchResult(
                assessment=ComplianceAssessment(
                    assessment_id=p.payload["assessment_id"],
                    customer_id=p.payload["customer_id"],
                    control_id=p.payload["control_id"],
                    assessment_date=datetime.fromisoformat(p.payload["assessment_date"]).date(),
                    assessor=p.payload["assessor"],
                    status=AssessmentStatus(p.payload.get("status", "in_progress")),
                    compliance_score=p.payload.get("compliance_score", 0),
                    findings=p.payload.get("findings", []),
                    recommendations=p.payload.get("recommendations", []),
                    evidence_ids=p.payload.get("evidence_ids", []),
                ),
                score=1.0,
            )
            for p in results[0]
        ]

    def get_assessments_by_framework(self, framework: str, limit: int = 100) -> List[AssessmentSearchResult]:
        """Get assessments for controls in a specific framework."""
        from .compliance_models import ComplianceAssessment, AssessmentStatus
        context = self._get_customer_context()

        # First get controls for the framework
        controls_request = ControlSearchRequest(
            customer_id=context.customer_id,
            framework=framework,
            limit=200,
        )
        controls = self.search_controls(controls_request)
        control_ids = [c.control.control_id for c in controls]

        if not control_ids:
            return []

        # Get assessments for these controls
        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(key="entity_type", match=MatchValue(value="assessment")),
                    FieldCondition(
                        key="customer_id",
                        match=MatchAny(any=context.get_customer_ids()),
                    ),
                ]
            ),
            limit=limit,
        )

        assessments = []
        for p in results[0]:
            if p.payload.get("control_id") in control_ids:
                assessments.append(
                    AssessmentSearchResult(
                        assessment=ComplianceAssessment(
                            assessment_id=p.payload["assessment_id"],
                            customer_id=p.payload["customer_id"],
                            control_id=p.payload["control_id"],
                            assessment_date=datetime.fromisoformat(p.payload["assessment_date"]).date(),
                            assessor=p.payload["assessor"],
                            status=AssessmentStatus(p.payload.get("status", "in_progress")),
                            compliance_score=p.payload.get("compliance_score", 0),
                            findings=p.payload.get("findings", []),
                            recommendations=p.payload.get("recommendations", []),
                            evidence_ids=p.payload.get("evidence_ids", []),
                        ),
                        score=1.0,
                    )
                )

        return assessments

    def complete_assessment(self, assessment_id: str) -> bool:
        """Mark an assessment as completed."""
        from .compliance_models import AssessmentStatus

        assessment = self.get_assessment(assessment_id)
        if not assessment:
            return False

        assessment.status = AssessmentStatus.COMPLETED
        self.update_assessment(assessment)
        return True

    # =========================================================================
    # Evidence Operations
    # =========================================================================

    def create_evidence(self, evidence: Any) -> Any:
        """Create new evidence."""
        context = self._get_customer_context()

        if not context.can_write():
            raise PermissionError("Write access required to create evidence")

        embed_text = f"{evidence.control_id} {evidence.title} {evidence.description or ''}"
        embedding = self._generate_embedding(embed_text)

        point_id = self._generate_point_id()
        self.qdrant_client.upsert(
            collection_name=self.COLLECTION_NAME,
            points=[
                PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload=evidence.to_qdrant_payload(),
                )
            ],
        )

        logger.info(f"Created evidence {evidence.evidence_id}")
        return evidence

    def get_evidence(self, evidence_id: str) -> Optional[Any]:
        """Get evidence by ID."""
        from .compliance_models import ComplianceEvidence, EvidenceType
        context = self._get_customer_context()

        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(key="evidence_id", match=MatchValue(value=evidence_id)),
                    FieldCondition(
                        key="customer_id",
                        match=MatchAny(any=context.get_customer_ids()),
                    ),
                    FieldCondition(key="entity_type", match=MatchValue(value="evidence")),
                ]
            ),
            limit=1,
        )

        if results[0]:
            payload = results[0][0].payload
            return ComplianceEvidence(
                evidence_id=payload["evidence_id"],
                customer_id=payload["customer_id"],
                control_id=payload["control_id"],
                evidence_type=EvidenceType(payload["evidence_type"]),
                title=payload["title"],
                description=payload.get("description"),
                file_path=payload.get("file_path"),
                collection_date=datetime.fromisoformat(payload["collection_date"]).date(),
                expiration_date=datetime.fromisoformat(payload["expiration_date"]).date() if payload.get("expiration_date") else None,
            )
        return None

    def get_evidence_for_control(self, control_id: str, limit: int = 50) -> List[Any]:
        """Get evidence for a control."""
        from .compliance_models import ComplianceEvidence, EvidenceType
        context = self._get_customer_context()

        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(key="entity_type", match=MatchValue(value="evidence")),
                    FieldCondition(key="control_id", match=MatchValue(value=control_id)),
                    FieldCondition(
                        key="customer_id",
                        match=MatchAny(any=context.get_customer_ids()),
                    ),
                ]
            ),
            limit=limit,
        )

        return [
            ComplianceEvidence(
                evidence_id=p.payload["evidence_id"],
                customer_id=p.payload["customer_id"],
                control_id=p.payload["control_id"],
                evidence_type=EvidenceType(p.payload["evidence_type"]),
                title=p.payload["title"],
                description=p.payload.get("description"),
                file_path=p.payload.get("file_path"),
                collection_date=datetime.fromisoformat(p.payload["collection_date"]).date(),
                expiration_date=datetime.fromisoformat(p.payload["expiration_date"]).date() if p.payload.get("expiration_date") else None,
            )
            for p in results[0]
        ]

    def delete_evidence(self, evidence_id: str) -> bool:
        """Delete evidence."""
        context = self._get_customer_context()

        if not context.can_write():
            raise PermissionError("Write access required to delete evidence")

        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(key="evidence_id", match=MatchValue(value=evidence_id)),
                    FieldCondition(key="customer_id", match=MatchValue(value=context.customer_id)),
                ]
            ),
            limit=1,
        )

        if results[0]:
            self.qdrant_client.delete(
                collection_name=self.COLLECTION_NAME,
                points_selector=[results[0][0].id],
            )
            return True
        return False

    # =========================================================================
    # Gap Operations
    # =========================================================================

    def create_gap(self, gap: Any) -> Any:
        """Create a new gap."""
        context = self._get_customer_context()

        if not context.can_write():
            raise PermissionError("Write access required to create gap")

        embed_text = f"{gap.control_id} {gap.gap_type} {gap.description} {gap.impact}"
        embedding = self._generate_embedding(embed_text)

        point_id = self._generate_point_id()
        self.qdrant_client.upsert(
            collection_name=self.COLLECTION_NAME,
            points=[
                PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload=gap.to_qdrant_payload(),
                )
            ],
        )

        logger.info(f"Created gap {gap.gap_id}")
        return gap

    def search_gaps(
        self,
        control_id: Optional[str] = None,
        severity: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 50,
    ) -> List[Any]:
        """Search gaps with filters."""
        from .compliance_models import ComplianceGap, GapSeverity, GapStatus
        context = self._get_customer_context()

        conditions = [
            FieldCondition(key="entity_type", match=MatchValue(value="gap"))
        ]

        if control_id:
            conditions.append(
                FieldCondition(key="control_id", match=MatchValue(value=control_id))
            )

        if severity:
            conditions.append(
                FieldCondition(key="severity", match=MatchValue(value=severity))
            )

        if status:
            conditions.append(
                FieldCondition(key="status", match=MatchValue(value=status))
            )

        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=self._build_customer_filter(
                context.customer_id,
                additional_conditions=conditions,
            ),
            limit=limit,
        )

        return [
            ComplianceGap(
                gap_id=p.payload["gap_id"],
                customer_id=p.payload["customer_id"],
                control_id=p.payload["control_id"],
                gap_type=p.payload["gap_type"],
                severity=GapSeverity(p.payload.get("severity", "medium")),
                description=p.payload["description"],
                impact=p.payload["impact"],
                remediation_plan=p.payload.get("remediation_plan"),
                target_date=datetime.fromisoformat(p.payload["target_date"]).date() if p.payload.get("target_date") else None,
                status=GapStatus(p.payload.get("status", "open")),
            )
            for p in results[0]
        ]

    def get_gaps_by_framework(self, framework: str, limit: int = 100) -> List[Any]:
        """Get gaps for controls in a specific framework."""
        context = self._get_customer_context()

        # Get controls for framework
        controls_request = ControlSearchRequest(
            customer_id=context.customer_id,
            framework=framework,
            limit=200,
        )
        controls = self.search_controls(controls_request)
        control_ids = [c.control.control_id for c in controls]

        if not control_ids:
            return []

        # Get gaps for these controls
        from .compliance_models import ComplianceGap, GapSeverity, GapStatus
        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(key="entity_type", match=MatchValue(value="gap")),
                    FieldCondition(
                        key="customer_id",
                        match=MatchAny(any=context.get_customer_ids()),
                    ),
                ]
            ),
            limit=limit,
        )

        gaps = []
        for p in results[0]:
            if p.payload.get("control_id") in control_ids:
                gaps.append(
                    ComplianceGap(
                        gap_id=p.payload["gap_id"],
                        customer_id=p.payload["customer_id"],
                        control_id=p.payload["control_id"],
                        gap_type=p.payload["gap_type"],
                        severity=GapSeverity(p.payload.get("severity", "medium")),
                        description=p.payload["description"],
                        impact=p.payload["impact"],
                        remediation_plan=p.payload.get("remediation_plan"),
                        target_date=datetime.fromisoformat(p.payload["target_date"]).date() if p.payload.get("target_date") else None,
                        status=GapStatus(p.payload.get("status", "open")),
                    )
                )

        return gaps

    def update_gap_remediation(
        self,
        gap_id: str,
        status: str,
        remediation_notes: str,
        completion_date: Optional[date],
        evidence_ids: List[str],
    ) -> bool:
        """Update gap remediation status."""
        from .compliance_models import GapStatus

        gap = None
        context = self._get_customer_context()

        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(key="gap_id", match=MatchValue(value=gap_id)),
                    FieldCondition(key="customer_id", match=MatchValue(value=context.customer_id)),
                ]
            ),
            limit=1,
        )

        if not results[0]:
            return False

        payload = results[0][0].payload
        from .compliance_models import ComplianceGap, GapSeverity

        gap = ComplianceGap(
            gap_id=payload["gap_id"],
            customer_id=payload["customer_id"],
            control_id=payload["control_id"],
            gap_type=payload["gap_type"],
            severity=GapSeverity(payload.get("severity", "medium")),
            description=payload["description"],
            impact=payload["impact"],
            remediation_plan=f"{payload.get('remediation_plan', '')} | {remediation_notes}",
            target_date=completion_date,
            status=GapStatus(status),
        )

        # Delete old and create new
        self.qdrant_client.delete(
            collection_name=self.COLLECTION_NAME,
            points_selector=[results[0][0].id],
        )
        self.create_gap(gap)
        return True

    # =========================================================================
    # Dashboard & Analytics
    # =========================================================================

    def get_dashboard_summary(self) -> Dict[str, Any]:
        """Get compliance dashboard summary."""
        context = self._get_customer_context()

        # Count controls by status
        controls_results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=self._build_customer_filter(
                context.customer_id,
                additional_conditions=[
                    FieldCondition(key="entity_type", match=MatchValue(value="control")),
                ]
            ),
            limit=500,
        )

        total_controls = len(controls_results[0])
        implemented = sum(1 for p in controls_results[0] if p.payload.get("implementation_status") == "implemented")
        in_progress = sum(1 for p in controls_results[0] if p.payload.get("implementation_status") == "in_progress")
        not_started = sum(1 for p in controls_results[0] if p.payload.get("implementation_status") == "not_started")

        # Framework breakdown
        framework_counts = {}
        for p in controls_results[0]:
            fw = p.payload.get("framework", "unknown")
            framework_counts[fw] = framework_counts.get(fw, 0) + 1

        # Count assessments
        assessment_results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=self._build_customer_filter(
                context.customer_id,
                additional_conditions=[
                    FieldCondition(key="entity_type", match=MatchValue(value="assessment")),
                ]
            ),
            limit=500,
        )

        total_assessments = len(assessment_results[0])
        total_score = sum(p.payload.get("compliance_score", 0) for p in assessment_results[0])
        avg_score = total_score / total_assessments if total_assessments > 0 else 0.0

        # Count gaps
        gap_results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=self._build_customer_filter(
                context.customer_id,
                additional_conditions=[
                    FieldCondition(key="entity_type", match=MatchValue(value="gap")),
                ]
            ),
            limit=500,
        )

        total_gaps = len(gap_results[0])
        critical_gaps = sum(1 for p in gap_results[0] if p.payload.get("severity") == "critical")

        return {
            "total_controls": total_controls,
            "implemented_controls": implemented,
            "in_progress_controls": in_progress,
            "not_started_controls": not_started,
            "average_compliance_score": round(avg_score, 2),
            "total_assessments": total_assessments,
            "total_gaps": total_gaps,
            "critical_gaps": critical_gaps,
            "framework_breakdown": framework_counts,
        }

    def get_compliance_posture(self) -> Dict[str, Any]:
        """Get compliance posture analysis."""
        summary = self.get_dashboard_summary()

        # Calculate posture score
        impl_rate = summary["implemented_controls"] / summary["total_controls"] if summary["total_controls"] > 0 else 0
        posture_score = (impl_rate * 0.6) + (summary["average_compliance_score"] / 100 * 0.4)
        posture_score = round(posture_score * 100, 2)

        # Determine overall posture
        if posture_score >= 90:
            overall_posture = "excellent"
            risk_level = "low"
        elif posture_score >= 75:
            overall_posture = "good"
            risk_level = "medium"
        elif posture_score >= 60:
            overall_posture = "fair"
            risk_level = "medium"
        else:
            overall_posture = "poor"
            risk_level = "high"

        # Framework compliance percentages
        framework_compliance = {}
        for framework, count in summary["framework_breakdown"].items():
            framework_compliance[framework] = {
                "total_controls": count,
                "compliance_rate": round((count / summary["total_controls"]) * 100, 2) if summary["total_controls"] > 0 else 0,
            }

        # Top gaps
        context = self._get_customer_context()
        gap_results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=self._build_customer_filter(
                context.customer_id,
                additional_conditions=[
                    FieldCondition(key="entity_type", match=MatchValue(value="gap")),
                    FieldCondition(key="severity", match=MatchAny(any=["critical", "high"])),
                ]
            ),
            limit=10,
        )

        top_gaps = [
            {
                "gap_id": p.payload["gap_id"],
                "control_id": p.payload["control_id"],
                "severity": p.payload.get("severity", "unknown"),
                "description": p.payload.get("description", ""),
            }
            for p in gap_results[0]
        ]

        recommendations = []
        if summary["critical_gaps"] > 0:
            recommendations.append(f"Address {summary['critical_gaps']} critical compliance gaps immediately")
        if summary["not_started_controls"] > 10:
            recommendations.append(f"Initiate implementation for {summary['not_started_controls']} pending controls")
        if summary["average_compliance_score"] < 70:
            recommendations.append("Improve assessment scores through enhanced evidence collection")

        return {
            "overall_posture": overall_posture,
            "posture_score": posture_score,
            "risk_level": risk_level,
            "framework_compliance": framework_compliance,
            "top_gaps": top_gaps,
            "recommendations": recommendations,
            "trend": "improving" if impl_rate > 0.6 else "stable",
        }
