"""
Threat Intelligence Correlation Service
========================================

Service layer for E04: Threat Intelligence Correlation.
Provides CRUD operations, semantic search, and threat correlation
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
class ThreatActorSearchRequest:
    """Request parameters for threat actor search."""
    query: Optional[str] = None
    customer_id: Optional[str] = None
    actor_type: Optional[str] = None
    country: Optional[str] = None
    target_sector: Optional[str] = None
    is_active: Optional[bool] = None
    limit: int = 20
    include_system: bool = True


@dataclass
class ThreatActorSearchResult:
    """Single threat actor search result."""
    actor: Any  # ThreatActor object
    score: float = 0.0
    match_reason: Optional[str] = None


@dataclass
class CampaignSearchRequest:
    """Request parameters for campaign search."""
    query: Optional[str] = None
    customer_id: Optional[str] = None
    threat_actor_id: Optional[str] = None
    target_sector: Optional[str] = None
    is_active: Optional[bool] = None
    limit: int = 20
    include_system: bool = True


@dataclass
class CampaignSearchResult:
    """Single campaign search result."""
    campaign: Any  # ThreatCampaign object
    score: float = 0.0


@dataclass
class IOCSearchRequest:
    """Request parameters for IOC search."""
    query: Optional[str] = None
    customer_id: Optional[str] = None
    ioc_type: Optional[str] = None
    threat_actor_id: Optional[str] = None
    campaign_id: Optional[str] = None
    min_confidence: Optional[int] = None
    is_active: Optional[bool] = None
    limit: int = 50
    include_system: bool = True


@dataclass
class IOCSearchResult:
    """Single IOC search result."""
    ioc: Any  # IOC object
    score: float = 0.0


# =============================================================================
# Threat Intelligence Service
# =============================================================================


class ThreatIntelligenceService:
    """
    Service for threat intelligence correlation and management.

    Provides customer-isolated operations for:
    - Threat actor tracking
    - Campaign monitoring
    - IOC management and correlation
    - MITRE ATT&CK mapping
    - Threat feed integration
    """

    COLLECTION_NAME = "ner11_threat_intel"
    VECTOR_SIZE = 384  # sentence-transformers/all-MiniLM-L6-v2

    def __init__(
        self,
        qdrant_url: str = "http://localhost:6333",
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
    ):
        """
        Initialize threat intelligence service.

        Args:
            qdrant_url: Qdrant server URL
            embedding_model: Sentence transformer model name
        """
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
        """Generate embedding for text using sentence transformer."""
        embedding = self._embedding_model.encode(text)
        return embedding.tolist()

    def _generate_point_id(self) -> str:
        """Generate unique point ID."""
        return str(uuid4())

    # =========================================================================
    # Threat Actor Operations
    # =========================================================================

    def create_threat_actor(self, actor: Any) -> Any:
        """Create a new threat actor with customer isolation."""
        context = self._get_customer_context()

        if not context.can_write():
            raise PermissionError("Write access required to create threat actor")

        if actor.customer_id != context.customer_id:
            raise ValueError("Actor customer_id must match context customer_id")

        # Generate embedding from actor name, aliases, and description
        embed_text = f"{actor.name} {' '.join(actor.aliases)} {actor.description or ''}"
        embedding = self._generate_embedding(embed_text)

        # Store in Qdrant
        point_id = self._generate_point_id()
        self.qdrant_client.upsert(
            collection_name=self.COLLECTION_NAME,
            points=[
                PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload=actor.to_qdrant_payload(),
                )
            ],
        )

        logger.info(f"Created threat actor {actor.actor_id}: {actor.name}")
        return actor

    def get_threat_actor(self, actor_id: str) -> Optional[Any]:
        """Get threat actor by ID with customer isolation."""
        context = self._get_customer_context()

        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(key="actor_id", match=MatchValue(value=actor_id)),
                    FieldCondition(
                        key="customer_id",
                        match=MatchAny(any=context.get_customer_ids()),
                    ),
                    FieldCondition(key="entity_type", match=MatchValue(value="threat_actor")),
                ]
            ),
            limit=1,
        )

        if results[0]:
            payload = results[0][0].payload
            return self._payload_to_threat_actor(payload)
        return None

    def _payload_to_threat_actor(self, payload: Dict[str, Any]) -> Any:
        """Convert Qdrant payload to ThreatActor object."""
        from .threat_models import ThreatActor, ActorType, SophisticationLevel

        return ThreatActor(
            actor_id=payload["actor_id"],
            customer_id=payload["customer_id"],
            name=payload["name"],
            aliases=payload.get("aliases", []),
            actor_type=ActorType(payload.get("actor_type", "apt")),
            country=payload.get("country"),
            motivation=payload.get("motivation", []),
            sophistication=SophisticationLevel(payload.get("sophistication", "medium")),
            target_sectors=payload.get("target_sectors", []),
            target_regions=payload.get("target_regions", []),
            first_seen=datetime.fromisoformat(payload["first_seen"]) if payload.get("first_seen") else None,
            is_active=payload.get("is_active", True),
            campaign_count=payload.get("campaign_count", 0),
            cve_count=payload.get("cve_count", 0),
            ioc_count=payload.get("ioc_count", 0),
        )

    def search_threat_actors(self, request: ThreatActorSearchRequest) -> List[ThreatActorSearchResult]:
        """Search threat actors with filters and optional semantic search."""
        context = self._get_customer_context()
        customer_id = request.customer_id or context.customer_id

        conditions = [
            FieldCondition(key="entity_type", match=MatchValue(value="threat_actor"))
        ]

        if request.actor_type:
            conditions.append(
                FieldCondition(key="actor_type", match=MatchValue(value=request.actor_type))
            )

        if request.country:
            conditions.append(
                FieldCondition(key="country", match=MatchValue(value=request.country))
            )

        if request.target_sector:
            conditions.append(
                FieldCondition(key="target_sectors", match=MatchAny(any=[request.target_sector]))
            )

        if request.is_active is not None:
            conditions.append(
                FieldCondition(key="is_active", match=MatchValue(value=request.is_active))
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
                ThreatActorSearchResult(
                    actor=self._payload_to_threat_actor(result.payload),
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
                ThreatActorSearchResult(
                    actor=self._payload_to_threat_actor(point.payload),
                    score=1.0,
                    match_reason="filter_match",
                )
                for point in results[0]
            ]

    def get_active_threat_actors(self) -> List[ThreatActorSearchResult]:
        """Get all currently active threat actors."""
        context = self._get_customer_context()

        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=self._build_customer_filter(
                context.customer_id,
                additional_conditions=[
                    FieldCondition(key="entity_type", match=MatchValue(value="threat_actor")),
                    FieldCondition(key="is_active", match=MatchValue(value=True)),
                ]
            ),
            limit=100,
        )

        return [
            ThreatActorSearchResult(
                actor=self._payload_to_threat_actor(point.payload),
                score=1.0,
            )
            for point in results[0]
        ]

    def get_actors_by_sector(self, sector: str) -> List[ThreatActorSearchResult]:
        """Get threat actors targeting a specific sector."""
        context = self._get_customer_context()

        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=self._build_customer_filter(
                context.customer_id,
                additional_conditions=[
                    FieldCondition(key="entity_type", match=MatchValue(value="threat_actor")),
                    FieldCondition(key="target_sectors", match=MatchAny(any=[sector])),
                ]
            ),
            limit=100,
        )

        return [
            ThreatActorSearchResult(
                actor=self._payload_to_threat_actor(point.payload),
                score=1.0,
            )
            for point in results[0]
        ]

    def get_actor_campaigns(self, actor_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get campaigns associated with a threat actor."""
        context = self._get_customer_context()

        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(key="entity_type", match=MatchValue(value="threat_campaign")),
                    FieldCondition(key="threat_actor_ids", match=MatchAny(any=[actor_id])),
                    FieldCondition(
                        key="customer_id",
                        match=MatchAny(any=context.get_customer_ids()),
                    ),
                ]
            ),
            limit=limit,
        )

        return [
            {
                "campaign_id": p.payload["campaign_id"],
                "name": p.payload["name"],
                "start_date": p.payload.get("start_date"),
                "is_active": p.payload.get("is_active", False),
            }
            for p in results[0]
        ]

    def get_actor_cves(self, actor_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get CVEs associated with a threat actor."""
        # This would typically query the SBOM/vulnerability service
        # For now, return placeholder
        return []

    # =========================================================================
    # Campaign Operations
    # =========================================================================

    def create_campaign(self, campaign: Any) -> Any:
        """Create a new threat campaign with customer isolation."""
        context = self._get_customer_context()

        if not context.can_write():
            raise PermissionError("Write access required to create campaign")

        if campaign.customer_id != context.customer_id:
            raise ValueError("Campaign customer_id must match context customer_id")

        # Generate embedding from campaign name and description
        embed_text = f"{campaign.name} {campaign.description or ''}"
        embedding = self._generate_embedding(embed_text)

        # Store in Qdrant
        point_id = self._generate_point_id()
        self.qdrant_client.upsert(
            collection_name=self.COLLECTION_NAME,
            points=[
                PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload=campaign.to_qdrant_payload(),
                )
            ],
        )

        logger.info(f"Created campaign {campaign.campaign_id}: {campaign.name}")
        return campaign

    def get_campaign(self, campaign_id: str) -> Optional[Any]:
        """Get campaign by ID with customer isolation."""
        context = self._get_customer_context()

        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(key="campaign_id", match=MatchValue(value=campaign_id)),
                    FieldCondition(
                        key="customer_id",
                        match=MatchAny(any=context.get_customer_ids()),
                    ),
                    FieldCondition(key="entity_type", match=MatchValue(value="threat_campaign")),
                ]
            ),
            limit=1,
        )

        if results[0]:
            payload = results[0][0].payload
            return self._payload_to_campaign(payload)
        return None

    def _payload_to_campaign(self, payload: Dict[str, Any]) -> Any:
        """Convert Qdrant payload to ThreatCampaign object."""
        from .threat_models import ThreatCampaign

        return ThreatCampaign(
            campaign_id=payload["campaign_id"],
            customer_id=payload["customer_id"],
            name=payload["name"],
            threat_actor_ids=payload.get("threat_actor_ids", []),
            start_date=datetime.fromisoformat(payload["start_date"]).date() if payload.get("start_date") else None,
            end_date=datetime.fromisoformat(payload["end_date"]).date() if payload.get("end_date") else None,
            target_sectors=payload.get("target_sectors", []),
            target_regions=payload.get("target_regions", []),
            is_active=payload.get("is_active", True),
            ioc_count=payload.get("ioc_count", 0),
            cve_count=payload.get("cve_count", 0),
        )

    def search_campaigns(self, request: CampaignSearchRequest) -> List[CampaignSearchResult]:
        """Search campaigns with filters and optional semantic search."""
        context = self._get_customer_context()
        customer_id = request.customer_id or context.customer_id

        conditions = [
            FieldCondition(key="entity_type", match=MatchValue(value="threat_campaign"))
        ]

        if request.threat_actor_id:
            conditions.append(
                FieldCondition(key="threat_actor_ids", match=MatchAny(any=[request.threat_actor_id]))
            )

        if request.target_sector:
            conditions.append(
                FieldCondition(key="target_sectors", match=MatchAny(any=[request.target_sector]))
            )

        if request.is_active is not None:
            conditions.append(
                FieldCondition(key="is_active", match=MatchValue(value=request.is_active))
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
                CampaignSearchResult(
                    campaign=self._payload_to_campaign(result.payload),
                    score=result.score,
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
                CampaignSearchResult(
                    campaign=self._payload_to_campaign(point.payload),
                    score=1.0,
                )
                for point in results[0]
            ]

    def get_active_campaigns(self) -> List[CampaignSearchResult]:
        """Get all currently active campaigns."""
        context = self._get_customer_context()

        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=self._build_customer_filter(
                context.customer_id,
                additional_conditions=[
                    FieldCondition(key="entity_type", match=MatchValue(value="threat_campaign")),
                    FieldCondition(key="is_active", match=MatchValue(value=True)),
                ]
            ),
            limit=100,
        )

        return [
            CampaignSearchResult(
                campaign=self._payload_to_campaign(point.payload),
                score=1.0,
            )
            for point in results[0]
        ]

    def get_campaign_iocs(self, campaign_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get IOCs associated with a campaign."""
        context = self._get_customer_context()

        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(key="entity_type", match=MatchValue(value="ioc")),
                    FieldCondition(key="campaign_id", match=MatchValue(value=campaign_id)),
                    FieldCondition(
                        key="customer_id",
                        match=MatchAny(any=context.get_customer_ids()),
                    ),
                ]
            ),
            limit=limit,
        )

        return [
            {
                "ioc_id": p.payload["ioc_id"],
                "ioc_type": p.payload["ioc_type"],
                "value": p.payload["value"],
                "confidence": p.payload.get("confidence", 0),
            }
            for p in results[0]
        ]

    # =========================================================================
    # IOC Operations
    # =========================================================================

    def create_ioc(self, ioc: Any) -> Any:
        """Create a new IOC with customer isolation."""
        context = self._get_customer_context()

        if not context.can_write():
            raise PermissionError("Write access required to create IOC")

        if ioc.customer_id != context.customer_id:
            raise ValueError("IOC customer_id must match context customer_id")

        # Generate embedding from IOC value and description
        embed_text = f"{ioc.value} {ioc.ioc_type} {ioc.description or ''}"
        embedding = self._generate_embedding(embed_text)

        # Store in Qdrant
        point_id = self._generate_point_id()
        self.qdrant_client.upsert(
            collection_name=self.COLLECTION_NAME,
            points=[
                PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload=ioc.to_qdrant_payload(),
                )
            ],
        )

        logger.info(f"Created IOC {ioc.ioc_id}: {ioc.value}")
        return ioc

    def bulk_import_iocs(self, iocs: List[Any]) -> Dict[str, Any]:
        """Bulk import IOCs."""
        context = self._get_customer_context()

        if not context.can_write():
            raise PermissionError("Write access required to import IOCs")

        imported = 0
        failed = []

        for ioc_data in iocs:
            try:
                from .threat_models import IOC, IOCType

                ioc = IOC(
                    ioc_id=ioc_data.ioc_id,
                    customer_id=context.customer_id,
                    ioc_type=IOCType(ioc_data.ioc_type),
                    value=ioc_data.value,
                    threat_actor_id=ioc_data.threat_actor_id,
                    campaign_id=ioc_data.campaign_id,
                    first_seen=ioc_data.first_seen,
                    last_seen=ioc_data.last_seen,
                    confidence=ioc_data.confidence,
                    description=ioc_data.description,
                    tags=ioc_data.tags,
                )
                self.create_ioc(ioc)
                imported += 1
            except Exception as e:
                failed.append({
                    "ioc_id": ioc_data.ioc_id,
                    "value": ioc_data.value,
                    "error": str(e),
                })

        return {
            "imported_count": imported,
            "failed_count": len(failed),
            "failed_iocs": failed,
        }

    def search_iocs(self, request: IOCSearchRequest) -> List[IOCSearchResult]:
        """Search IOCs with filters and optional semantic search."""
        context = self._get_customer_context()
        customer_id = request.customer_id or context.customer_id

        conditions = [
            FieldCondition(key="entity_type", match=MatchValue(value="ioc"))
        ]

        if request.ioc_type:
            conditions.append(
                FieldCondition(key="ioc_type", match=MatchValue(value=request.ioc_type))
            )

        if request.threat_actor_id:
            conditions.append(
                FieldCondition(key="threat_actor_id", match=MatchValue(value=request.threat_actor_id))
            )

        if request.campaign_id:
            conditions.append(
                FieldCondition(key="campaign_id", match=MatchValue(value=request.campaign_id))
            )

        if request.min_confidence is not None:
            conditions.append(
                FieldCondition(key="confidence", range=Range(gte=request.min_confidence))
            )

        if request.is_active is not None:
            conditions.append(
                FieldCondition(key="is_active", match=MatchValue(value=request.is_active))
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
                IOCSearchResult(
                    ioc=self._payload_to_ioc(result.payload),
                    score=result.score,
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
                IOCSearchResult(
                    ioc=self._payload_to_ioc(point.payload),
                    score=1.0,
                )
                for point in results[0]
            ]

    def _payload_to_ioc(self, payload: Dict[str, Any]) -> Any:
        """Convert Qdrant payload to IOC object."""
        from .threat_models import IOC, IOCType

        return IOC(
            ioc_id=payload["ioc_id"],
            customer_id=payload["customer_id"],
            ioc_type=IOCType(payload.get("ioc_type", "ip")),
            value=payload["value"],
            threat_actor_id=payload.get("threat_actor_id"),
            campaign_id=payload.get("campaign_id"),
            first_seen=datetime.fromisoformat(payload["first_seen"]).date() if payload.get("first_seen") else None,
            last_seen=datetime.fromisoformat(payload["last_seen"]).date() if payload.get("last_seen") else None,
            confidence=payload.get("confidence", 50),
            is_active=payload.get("is_active", True),
            tags=payload.get("tags", []),
        )

    def get_active_iocs(self) -> List[IOCSearchResult]:
        """Get all currently active IOCs."""
        context = self._get_customer_context()

        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=self._build_customer_filter(
                context.customer_id,
                additional_conditions=[
                    FieldCondition(key="entity_type", match=MatchValue(value="ioc")),
                    FieldCondition(key="is_active", match=MatchValue(value=True)),
                ]
            ),
            limit=500,
        )

        return [
            IOCSearchResult(
                ioc=self._payload_to_ioc(point.payload),
                score=1.0,
            )
            for point in results[0]
        ]

    def get_iocs_by_type(self, ioc_type: str, limit: int = 100) -> List[IOCSearchResult]:
        """Get IOCs by type."""
        context = self._get_customer_context()

        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=self._build_customer_filter(
                context.customer_id,
                additional_conditions=[
                    FieldCondition(key="entity_type", match=MatchValue(value="ioc")),
                    FieldCondition(key="ioc_type", match=MatchValue(value=ioc_type)),
                ]
            ),
            limit=limit,
        )

        return [
            IOCSearchResult(
                ioc=self._payload_to_ioc(point.payload),
                score=1.0,
            )
            for point in results[0]
        ]

    # =========================================================================
    # MITRE ATT&CK Operations
    # =========================================================================

    def create_mitre_mapping(self, mapping: Any) -> Any:
        """Create a new MITRE ATT&CK mapping."""
        context = self._get_customer_context()

        if not context.can_write():
            raise PermissionError("Write access required to create MITRE mapping")

        if mapping.customer_id != context.customer_id:
            raise ValueError("Mapping customer_id must match context customer_id")

        # Generate embedding from technique name and description
        embed_text = f"{mapping.technique_id} {mapping.technique_name} {mapping.description or ''}"
        embedding = self._generate_embedding(embed_text)

        # Store in Qdrant
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

        logger.info(f"Created MITRE mapping {mapping.mapping_id}")
        return mapping

    def get_entity_mitre_mappings(self, entity_type: str, entity_id: str) -> List[Any]:
        """Get MITRE ATT&CK mappings for an entity."""
        context = self._get_customer_context()

        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(key="entity_type", match=MatchValue(value="mitre_mapping")),
                    FieldCondition(key="mapped_entity_type", match=MatchValue(value=entity_type)),
                    FieldCondition(key="mapped_entity_id", match=MatchValue(value=entity_id)),
                    FieldCondition(
                        key="customer_id",
                        match=MatchAny(any=context.get_customer_ids()),
                    ),
                ]
            ),
            limit=100,
        )

        from .threat_models import MITREMapping
        return [
            MITREMapping(
                mapping_id=p.payload["mapping_id"],
                customer_id=p.payload["customer_id"],
                technique_id=p.payload["technique_id"],
                technique_name=p.payload["technique_name"],
                tactic=p.payload["tactic"],
                entity_type=p.payload["mapped_entity_type"],
                entity_id=p.payload["mapped_entity_id"],
            )
            for p in results[0]
        ]

    def get_actors_using_technique(self, technique_id: str) -> List[Dict[str, Any]]:
        """Get threat actors using a specific MITRE ATT&CK technique."""
        context = self._get_customer_context()

        # First get all mappings for this technique
        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(key="entity_type", match=MatchValue(value="mitre_mapping")),
                    FieldCondition(key="technique_id", match=MatchValue(value=technique_id)),
                    FieldCondition(key="mapped_entity_type", match=MatchValue(value="threat_actor")),
                    FieldCondition(
                        key="customer_id",
                        match=MatchAny(any=context.get_customer_ids()),
                    ),
                ]
            ),
            limit=100,
        )

        actor_ids = [p.payload["mapped_entity_id"] for p in results[0]]

        actors = []
        for actor_id in actor_ids:
            actor = self.get_threat_actor(actor_id)
            if actor:
                actors.append({
                    "actor_id": actor.actor_id,
                    "name": actor.name,
                    "actor_type": actor.actor_type.value if hasattr(actor.actor_type, 'value') else actor.actor_type,
                    "is_active": actor.is_active,
                })

        return actors

    def get_mitre_coverage(self) -> Dict[str, Any]:
        """Get MITRE ATT&CK coverage summary."""
        context = self._get_customer_context()

        # Get all mappings for customer
        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=self._build_customer_filter(
                context.customer_id,
                additional_conditions=[
                    FieldCondition(key="entity_type", match=MatchValue(value="mitre_mapping")),
                ]
            ),
            limit=1000,
        )

        mappings = results[0]
        unique_techniques = set(p.payload["technique_id"] for p in mappings)
        tactics_coverage = {}

        for p in mappings:
            tactic = p.payload.get("tactic", "unknown")
            tactics_coverage[tactic] = tactics_coverage.get(tactic, 0) + 1

        # MITRE ATT&CK has ~200 techniques in Enterprise matrix
        total_techniques = 200
        covered_techniques = len(unique_techniques)
        coverage_percentage = (covered_techniques / total_techniques) * 100 if total_techniques > 0 else 0

        # Get top techniques by usage
        technique_counts = {}
        for p in mappings:
            tech_id = p.payload["technique_id"]
            technique_counts[tech_id] = technique_counts.get(tech_id, 0) + 1

        top_techniques = [
            {"technique_id": tech_id, "usage_count": count}
            for tech_id, count in sorted(technique_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        ]

        return {
            "total_techniques": total_techniques,
            "covered_techniques": covered_techniques,
            "coverage_percentage": round(coverage_percentage, 2),
            "tactics_coverage": tactics_coverage,
            "top_techniques": top_techniques,
        }

    def get_mitre_gaps(self) -> Dict[str, Any]:
        """Get MITRE ATT&CK coverage gaps."""
        coverage = self.get_mitre_coverage()

        uncovered_count = coverage["total_techniques"] - coverage["covered_techniques"]

        # Critical gaps would be high-impact techniques not covered
        critical_gaps = [
            {"technique_id": "T1566", "name": "Phishing", "reason": "Common initial access vector"},
            {"technique_id": "T1059", "name": "Command and Scripting Interpreter", "reason": "Widely used execution technique"},
            {"technique_id": "T1055", "name": "Process Injection", "reason": "Common persistence mechanism"},
        ]

        recommendations = [
            "Implement detection for phishing attempts (T1566)",
            "Monitor command-line execution patterns (T1059)",
            "Track process injection behaviors (T1055)",
            "Enhance logging for uncovered techniques",
        ]

        return {
            "uncovered_techniques": uncovered_count,
            "critical_gaps": critical_gaps,
            "recommendations": recommendations,
        }

    # =========================================================================
    # Threat Feed Operations
    # =========================================================================

    def create_threat_feed(self, feed: Any) -> Any:
        """Create a new threat feed."""
        context = self._get_customer_context()

        if not context.can_write():
            raise PermissionError("Write access required to create threat feed")

        if feed.customer_id != context.customer_id:
            raise ValueError("Feed customer_id must match context customer_id")

        # Generate embedding from feed name
        embed_text = f"{feed.name} {feed.feed_type}"
        embedding = self._generate_embedding(embed_text)

        # Store in Qdrant
        point_id = self._generate_point_id()
        self.qdrant_client.upsert(
            collection_name=self.COLLECTION_NAME,
            points=[
                PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload=feed.to_qdrant_payload(),
                )
            ],
        )

        logger.info(f"Created threat feed {feed.feed_id}: {feed.name}")
        return feed

    def list_threat_feeds(self, limit: int = 50) -> List[Any]:
        """List threat feeds."""
        context = self._get_customer_context()

        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=self._build_customer_filter(
                context.customer_id,
                additional_conditions=[
                    FieldCondition(key="entity_type", match=MatchValue(value="threat_feed")),
                ]
            ),
            limit=limit,
        )

        from .threat_models import ThreatFeed, FeedType
        return [
            ThreatFeed(
                feed_id=p.payload["feed_id"],
                name=p.payload["name"],
                customer_id=p.payload["customer_id"],
                feed_url=p.payload["feed_url"],
                feed_type=FeedType(p.payload.get("feed_type", "osint")),
                refresh_interval=p.payload.get("refresh_interval", 3600),
                enabled=p.payload.get("enabled", True),
                last_refresh=datetime.fromisoformat(p.payload["last_refresh"]) if p.payload.get("last_refresh") else None,
            )
            for p in results[0]
        ]

    def refresh_threat_feed(self, feed_id: str) -> bool:
        """Trigger threat feed refresh."""
        context = self._get_customer_context()

        if not context.can_write():
            raise PermissionError("Write access required to refresh feed")

        # In production, this would trigger an async job to fetch and process feed data
        logger.info(f"Triggering refresh for feed {feed_id}")
        return True

    # =========================================================================
    # Dashboard & Analytics
    # =========================================================================

    def get_dashboard_summary(self) -> Dict[str, Any]:
        """Get threat intelligence dashboard summary."""
        context = self._get_customer_context()

        # Count threat actors
        actor_results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=self._build_customer_filter(
                context.customer_id,
                additional_conditions=[
                    FieldCondition(key="entity_type", match=MatchValue(value="threat_actor")),
                ]
            ),
            limit=1000,
        )
        total_actors = len(actor_results[0])
        active_actors = sum(1 for p in actor_results[0] if p.payload.get("is_active", False))

        # Count campaigns
        campaign_results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=self._build_customer_filter(
                context.customer_id,
                additional_conditions=[
                    FieldCondition(key="entity_type", match=MatchValue(value="threat_campaign")),
                ]
            ),
            limit=1000,
        )
        active_campaigns = sum(1 for p in campaign_results[0] if p.payload.get("is_active", False))

        # Count IOCs
        ioc_results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=self._build_customer_filter(
                context.customer_id,
                additional_conditions=[
                    FieldCondition(key="entity_type", match=MatchValue(value="ioc")),
                ]
            ),
            limit=5000,
        )
        total_iocs = len(ioc_results[0])
        active_iocs = sum(1 for p in ioc_results[0] if p.payload.get("is_active", False))
        high_confidence_iocs = sum(1 for p in ioc_results[0] if p.payload.get("confidence", 0) >= 75)

        # Get MITRE coverage
        coverage = self.get_mitre_coverage()

        return {
            "total_threat_actors": total_actors,
            "active_threat_actors": active_actors,
            "active_campaigns": active_campaigns,
            "total_iocs": total_iocs,
            "active_iocs": active_iocs,
            "total_cves": 0,  # Would query from SBOM service
            "mitre_coverage": coverage.get("coverage_percentage", 0.0),
            "high_confidence_iocs": high_confidence_iocs,
            "recent_activity_count": active_campaigns + active_actors,
        }
