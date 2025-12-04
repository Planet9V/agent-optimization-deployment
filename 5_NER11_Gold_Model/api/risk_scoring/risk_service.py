"""
Risk Scoring Service
====================

Service layer for E05: Risk Scoring Engine.
Provides comprehensive risk assessment with multi-factor scoring,
asset criticality management, exposure scoring, and risk aggregation.

Version: 1.0.0
Created: 2025-12-04
"""

from dataclasses import dataclass
from datetime import datetime, date, timedelta
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

from ..customer_isolation import CustomerContext, CustomerContextManager
from .risk_models import (
    RiskScore,
    RiskFactor,
    AssetCriticality,
    ExposureScore,
    RiskAggregation,
    RiskLevel,
    RiskTrend,
    CriticalityLevel,
    AttackSurfaceArea,
    AggregationType,
)

logger = logging.getLogger(__name__)


@dataclass
class RiskScoreRequest:
    """Request to calculate risk score."""
    entity_type: str  # asset, vulnerability, threat, vendor
    entity_id: str
    entity_name: str
    factors: List[RiskFactor]
    asset_criticality: Optional[float] = None
    exposure_score: Optional[float] = None


@dataclass
class RiskSearchRequest:
    """Request parameters for risk search."""
    query: Optional[str] = None
    customer_id: Optional[str] = None
    entity_type: Optional[str] = None
    risk_level: Optional[RiskLevel] = None
    min_risk_score: Optional[float] = None
    max_risk_score: Optional[float] = None
    trend: Optional[RiskTrend] = None
    limit: int = 10
    include_system: bool = False


@dataclass
class RiskSearchResult:
    """Single risk score search result."""
    risk_score: RiskScore
    score: float = 1.0


class RiskScoringService:
    """
    Service for comprehensive risk scoring.

    Provides customer-isolated operations for:
    - Risk score calculation and storage
    - Asset criticality management
    - Exposure scoring
    - Risk aggregation by vendor, sector, asset type
    - Trend analysis and degradation detection
    """

    COLLECTION_NAME = "ner11_risk_scoring"
    VECTOR_SIZE = 384  # sentence-transformers/all-MiniLM-L6-v2

    def __init__(
        self,
        qdrant_url: str = "http://localhost:6333",
        embedding_service: Optional[Any] = None,
    ):
        """Initialize risk scoring service."""
        self.qdrant_client = QdrantClient(url=qdrant_url)
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
        include_system: bool = False,
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
        if self._embedding_service is not None:
            return self._embedding_service.encode(text)
        return [0.0] * self.VECTOR_SIZE

    # ===== Risk Score Operations =====

    def calculate_risk_score(self, request: RiskScoreRequest) -> RiskScore:
        """
        Calculate comprehensive risk score.

        Risk score = weighted average of factors × criticality multiplier × exposure multiplier
        """
        context = self._get_customer_context()

        if not context.can_write():
            raise PermissionError("Write access required to calculate risk score")

        # Calculate base score from factors
        if not request.factors:
            base_score = 0.0
        else:
            total_weight = sum(f.weight for f in request.factors)
            weighted_sum = sum(f.value * f.weight for f in request.factors)
            base_score = weighted_sum / total_weight if total_weight > 0 else 0.0

        # Apply criticality multiplier (1.0-2.0)
        criticality_multiplier = 1.0 + (request.asset_criticality or 0.0) / 10.0

        # Apply exposure multiplier (1.0-1.5)
        exposure_multiplier = 1.0 + (request.exposure_score or 0.0) / 20.0

        # Calculate final score
        final_score = min(base_score * criticality_multiplier * exposure_multiplier, 10.0)

        # Determine risk level
        if final_score >= 8.0:
            risk_level = RiskLevel.CRITICAL
        elif final_score >= 6.0:
            risk_level = RiskLevel.HIGH
        elif final_score >= 4.0:
            risk_level = RiskLevel.MEDIUM
        elif final_score >= 2.0:
            risk_level = RiskLevel.LOW
        else:
            risk_level = RiskLevel.MINIMAL

        risk_score = RiskScore(
            risk_id=str(uuid4()),
            entity_type=request.entity_type,
            entity_id=request.entity_id,
            entity_name=request.entity_name,
            customer_id=context.customer_id,
            risk_score=final_score,
            risk_level=risk_level,
            factors=request.factors,
            calculated_at=datetime.utcnow(),
        )

        # Store in Qdrant
        self._store_risk_score(risk_score)

        logger.info(f"Calculated risk score {final_score:.2f} ({risk_level.value}) for {request.entity_type}/{request.entity_id}")
        return risk_score

    def _store_risk_score(self, risk_score: RiskScore) -> None:
        """Store risk score in Qdrant."""
        embed_text = f"{risk_score.entity_type} {risk_score.entity_name}"
        embedding = self._generate_embedding(embed_text)

        point_id = str(uuid4())
        self.qdrant_client.upsert(
            collection_name=self.COLLECTION_NAME,
            points=[
                PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload=risk_score.to_qdrant_payload(),
                )
            ],
        )

    def get_risk_score(self, entity_type: str, entity_id: str) -> Optional[RiskScore]:
        """Get most recent risk score for entity."""
        context = self._get_customer_context()

        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(key="entity_type", match=MatchValue(value=entity_type)),
                    FieldCondition(key="entity_id", match=MatchValue(value=entity_id)),
                    FieldCondition(key="customer_id", match=MatchValue(value=context.customer_id)),
                    FieldCondition(key="record_type", match=MatchValue(value="risk_score")),
                ]
            ),
            limit=1,
            order_by="calculated_at",
        )

        if results[0]:
            return self._payload_to_risk_score(results[0][0].payload)
        return None

    def _payload_to_risk_score(self, payload: Dict[str, Any]) -> RiskScore:
        """Convert Qdrant payload to RiskScore."""
        return RiskScore(
            risk_id=payload["risk_id"],
            entity_type=payload["entity_type"],
            entity_id=payload["entity_id"],
            entity_name=payload["entity_name"],
            customer_id=payload["customer_id"],
            risk_score=payload["risk_score"],
            risk_level=RiskLevel(payload["risk_level"]),
            factors=[RiskFactor(**f) for f in payload.get("factors", [])],
            calculated_at=datetime.fromisoformat(payload["calculated_at"]),
            trend=RiskTrend(payload["trend"]) if payload.get("trend") else None,
        )

    def get_high_risk_entities(self, min_score: float = 7.0) -> List[RiskSearchResult]:
        """Get all entities with high risk scores."""
        request = RiskSearchRequest(
            min_risk_score=min_score,
            limit=100,
        )
        return self.search_risk_scores(request)

    def get_trending_entities(self, trend: RiskTrend = RiskTrend.INCREASING) -> List[RiskSearchResult]:
        """Get entities with specific risk trend."""
        request = RiskSearchRequest(
            trend=trend,
            limit=100,
        )
        return self.search_risk_scores(request)

    def search_risk_scores(self, request: RiskSearchRequest) -> List[RiskSearchResult]:
        """Search risk scores with filters."""
        context = self._get_customer_context()
        customer_id = request.customer_id or context.customer_id

        conditions = [
            FieldCondition(key="record_type", match=MatchValue(value="risk_score"))
        ]

        if request.entity_type:
            conditions.append(
                FieldCondition(key="entity_type", match=MatchValue(value=request.entity_type))
            )

        if request.risk_level:
            conditions.append(
                FieldCondition(key="risk_level", match=MatchValue(value=request.risk_level.value))
            )

        if request.min_risk_score is not None:
            conditions.append(
                FieldCondition(key="risk_score", range=Range(gte=request.min_risk_score))
            )

        if request.max_risk_score is not None:
            conditions.append(
                FieldCondition(key="risk_score", range=Range(lte=request.max_risk_score))
            )

        if request.trend:
            conditions.append(
                FieldCondition(key="trend", match=MatchValue(value=request.trend.value))
            )

        query_filter = self._build_customer_filter(
            customer_id=customer_id,
            include_system=request.include_system,
            additional_conditions=conditions,
        )

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

        risk_results = []
        for result in results:
            score = result.score if hasattr(result, 'score') else 1.0
            risk_score = self._payload_to_risk_score(result.payload)
            risk_results.append(RiskSearchResult(risk_score=risk_score, score=score))

        return risk_results

    def recalculate_risk_score(self, entity_type: str, entity_id: str) -> Optional[RiskScore]:
        """Force recalculation of risk score."""
        # Get existing score to retrieve factors
        existing = self.get_risk_score(entity_type, entity_id)
        if not existing:
            return None

        # Recalculate with same factors
        request = RiskScoreRequest(
            entity_type=entity_type,
            entity_id=entity_id,
            entity_name=existing.entity_name,
            factors=existing.factors,
        )
        return self.calculate_risk_score(request)

    def get_risk_history(self, entity_type: str, entity_id: str, days: int = 30) -> List[RiskScore]:
        """Get risk score history for entity."""
        context = self._get_customer_context()
        cutoff_date = datetime.utcnow() - timedelta(days=days)

        results, _ = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(key="entity_type", match=MatchValue(value=entity_type)),
                    FieldCondition(key="entity_id", match=MatchValue(value=entity_id)),
                    FieldCondition(key="customer_id", match=MatchValue(value=context.customer_id)),
                    FieldCondition(key="record_type", match=MatchValue(value="risk_score")),
                    FieldCondition(key="calculated_at", range=Range(gte=cutoff_date.isoformat())),
                ]
            ),
            limit=100,
        )

        history = [self._payload_to_risk_score(r.payload) for r in results]
        history.sort(key=lambda x: x.calculated_at, reverse=True)
        return history

    # ===== Asset Criticality Operations =====

    def set_asset_criticality(self, asset_id: str, asset_name: str, criticality: AssetCriticality) -> AssetCriticality:
        """Set asset criticality rating."""
        context = self._get_customer_context()

        if not context.can_write():
            raise PermissionError("Write access required to set asset criticality")

        criticality.customer_id = context.customer_id
        criticality.asset_id = asset_id
        criticality.asset_name = asset_name

        # Store in Qdrant
        embed_text = f"asset criticality {asset_name}"
        embedding = self._generate_embedding(embed_text)

        point_id = str(uuid4())
        self.qdrant_client.upsert(
            collection_name=self.COLLECTION_NAME,
            points=[
                PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload=criticality.to_qdrant_payload(),
                )
            ],
        )

        logger.info(f"Set criticality for asset {asset_id} to {criticality.criticality_level.value}")
        return criticality

    def get_asset_criticality(self, asset_id: str) -> Optional[AssetCriticality]:
        """Get asset criticality rating."""
        context = self._get_customer_context()

        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(key="asset_id", match=MatchValue(value=asset_id)),
                    FieldCondition(key="customer_id", match=MatchValue(value=context.customer_id)),
                    FieldCondition(key="record_type", match=MatchValue(value="asset_criticality")),
                ]
            ),
            limit=1,
        )

        if results[0]:
            payload = results[0][0].payload
            return AssetCriticality(
                asset_id=payload["asset_id"],
                asset_name=payload["asset_name"],
                customer_id=payload["customer_id"],
                criticality_level=CriticalityLevel(payload["criticality_level"]),
                criticality_score=payload["criticality_score"],
                business_impact=payload.get("business_impact"),
                data_classification=payload.get("data_classification"),
                availability_requirement=payload.get("availability_requirement"),
                justification=payload.get("justification"),
            )
        return None

    def get_mission_critical_assets(self) -> List[AssetCriticality]:
        """Get all mission-critical assets."""
        return self.get_assets_by_criticality(CriticalityLevel.MISSION_CRITICAL)

    def get_assets_by_criticality(self, level: CriticalityLevel) -> List[AssetCriticality]:
        """Get assets by criticality level."""
        context = self._get_customer_context()

        results, _ = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(key="customer_id", match=MatchValue(value=context.customer_id)),
                    FieldCondition(key="record_type", match=MatchValue(value="asset_criticality")),
                    FieldCondition(key="criticality_level", match=MatchValue(value=level.value)),
                ]
            ),
            limit=100,
        )

        assets = []
        for r in results:
            payload = r.payload
            assets.append(AssetCriticality(
                asset_id=payload["asset_id"],
                asset_name=payload["asset_name"],
                customer_id=payload["customer_id"],
                criticality_level=CriticalityLevel(payload["criticality_level"]),
                criticality_score=payload["criticality_score"],
                business_impact=payload.get("business_impact"),
                data_classification=payload.get("data_classification"),
                availability_requirement=payload.get("availability_requirement"),
                justification=payload.get("justification"),
            ))

        return assets

    def get_criticality_summary(self) -> Dict[str, int]:
        """Get distribution of assets by criticality level."""
        context = self._get_customer_context()

        summary = {
            "mission_critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0,
            "informational": 0,
        }

        results, _ = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(key="customer_id", match=MatchValue(value=context.customer_id)),
                    FieldCondition(key="record_type", match=MatchValue(value="asset_criticality")),
                ]
            ),
            limit=1000,
        )

        for r in results:
            level = r.payload.get("criticality_level", "low")
            if level in summary:
                summary[level] += 1

        return summary

    # ===== Exposure Score Operations =====

    def calculate_exposure_score(self, asset_id: str, asset_name: str, exposure: ExposureScore) -> ExposureScore:
        """Calculate and store asset exposure score."""
        context = self._get_customer_context()

        if not context.can_write():
            raise PermissionError("Write access required to calculate exposure")

        exposure.asset_id = asset_id
        exposure.asset_name = asset_name
        exposure.customer_id = context.customer_id

        # Calculate exposure score
        base_score = 0.0

        # Internet-facing adds significant exposure
        if exposure.is_internet_facing:
            base_score += 3.0

        # Attack surface area
        surface_scores = {
            AttackSurfaceArea.EXTENSIVE: 3.0,
            AttackSurfaceArea.LARGE: 2.5,
            AttackSurfaceArea.MODERATE: 2.0,
            AttackSurfaceArea.LIMITED: 1.0,
            AttackSurfaceArea.MINIMAL: 0.5,
        }
        base_score += surface_scores.get(exposure.attack_surface, 2.0)

        # Open ports increase exposure
        base_score += min(len(exposure.open_ports), 10) * 0.2

        # Unpatched vulnerabilities
        base_score += min(exposure.unpatched_vulnerabilities, 10) * 0.3

        # Network exposure
        if exposure.network_exposure:
            network_scores = {
                "public": 2.0,
                "dmz": 1.5,
                "internal": 0.5,
                "isolated": 0.0,
            }
            base_score += network_scores.get(exposure.network_exposure, 1.0)

        exposure.exposure_score = min(base_score, 10.0)

        # Store in Qdrant
        embed_text = f"asset exposure {asset_name}"
        embedding = self._generate_embedding(embed_text)

        point_id = str(uuid4())
        self.qdrant_client.upsert(
            collection_name=self.COLLECTION_NAME,
            points=[
                PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload=exposure.to_qdrant_payload(),
                )
            ],
        )

        logger.info(f"Calculated exposure score {exposure.exposure_score:.2f} for asset {asset_id}")
        return exposure

    def get_exposure_score(self, asset_id: str) -> Optional[ExposureScore]:
        """Get asset exposure score."""
        context = self._get_customer_context()

        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(key="asset_id", match=MatchValue(value=asset_id)),
                    FieldCondition(key="customer_id", match=MatchValue(value=context.customer_id)),
                    FieldCondition(key="record_type", match=MatchValue(value="exposure_score")),
                ]
            ),
            limit=1,
        )

        if results[0]:
            payload = results[0][0].payload
            return ExposureScore(
                asset_id=payload["asset_id"],
                asset_name=payload["asset_name"],
                customer_id=payload["customer_id"],
                is_internet_facing=payload.get("is_internet_facing", False),
                attack_surface=AttackSurfaceArea(payload["attack_surface"]),
                open_ports=payload.get("open_ports", []),
                unpatched_vulnerabilities=payload.get("unpatched_vulnerabilities", 0),
                network_exposure=payload.get("network_exposure"),
                exposure_score=payload["exposure_score"],
            )
        return None

    def get_internet_facing_assets(self) -> List[ExposureScore]:
        """Get all internet-facing assets."""
        context = self._get_customer_context()

        results, _ = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(key="customer_id", match=MatchValue(value=context.customer_id)),
                    FieldCondition(key="record_type", match=MatchValue(value="exposure_score")),
                    FieldCondition(key="is_internet_facing", match=MatchValue(value=True)),
                ]
            ),
            limit=100,
        )

        exposures = []
        for r in results:
            payload = r.payload
            exposures.append(ExposureScore(
                asset_id=payload["asset_id"],
                asset_name=payload["asset_name"],
                customer_id=payload["customer_id"],
                is_internet_facing=payload.get("is_internet_facing", False),
                attack_surface=AttackSurfaceArea(payload["attack_surface"]),
                open_ports=payload.get("open_ports", []),
                unpatched_vulnerabilities=payload.get("unpatched_vulnerabilities", 0),
                network_exposure=payload.get("network_exposure"),
                exposure_score=payload["exposure_score"],
            ))

        return exposures

    def get_high_exposure_assets(self, min_score: float = 6.0) -> List[ExposureScore]:
        """Get assets with high exposure scores."""
        context = self._get_customer_context()

        results, _ = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(key="customer_id", match=MatchValue(value=context.customer_id)),
                    FieldCondition(key="record_type", match=MatchValue(value="exposure_score")),
                    FieldCondition(key="exposure_score", range=Range(gte=min_score)),
                ]
            ),
            limit=100,
        )

        exposures = []
        for r in results:
            payload = r.payload
            exposures.append(ExposureScore(
                asset_id=payload["asset_id"],
                asset_name=payload["asset_name"],
                customer_id=payload["customer_id"],
                is_internet_facing=payload.get("is_internet_facing", False),
                attack_surface=AttackSurfaceArea(payload["attack_surface"]),
                open_ports=payload.get("open_ports", []),
                unpatched_vulnerabilities=payload.get("unpatched_vulnerabilities", 0),
                network_exposure=payload.get("network_exposure"),
                exposure_score=payload["exposure_score"],
            ))

        return exposures

    def get_attack_surface_summary(self) -> Dict[str, Any]:
        """Get attack surface summary."""
        context = self._get_customer_context()

        results, _ = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(key="customer_id", match=MatchValue(value=context.customer_id)),
                    FieldCondition(key="record_type", match=MatchValue(value="exposure_score")),
                ]
            ),
            limit=1000,
        )

        internet_facing = 0
        total_assets = len(results)
        avg_exposure = 0.0
        high_exposure = 0

        for r in results:
            if r.payload.get("is_internet_facing"):
                internet_facing += 1
            score = r.payload.get("exposure_score", 0.0)
            avg_exposure += score
            if score >= 6.0:
                high_exposure += 1

        return {
            "total_assets": total_assets,
            "internet_facing": internet_facing,
            "high_exposure_count": high_exposure,
            "avg_exposure_score": avg_exposure / total_assets if total_assets > 0 else 0.0,
        }

    # ===== Aggregation Operations =====

    def get_risk_by_vendor(self, vendor_id: str) -> Optional[RiskAggregation]:
        """Get aggregated risk for vendor."""
        context = self._get_customer_context()

        # Get all risk scores for vendor assets
        results, _ = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(key="customer_id", match=MatchValue(value=context.customer_id)),
                    FieldCondition(key="record_type", match=MatchValue(value="risk_score")),
                    FieldCondition(key="vendor_id", match=MatchValue(value=vendor_id)),
                ]
            ),
            limit=1000,
        )

        if not results:
            return None

        return self._aggregate_risk_scores(
            aggregation_type=AggregationType.VENDOR,
            group_id=vendor_id,
            results=results,
        )

    def _aggregate_risk_scores(
        self,
        aggregation_type: AggregationType,
        group_id: str,
        results: List[Any],
    ) -> RiskAggregation:
        """Aggregate risk scores."""
        total_score = 0.0
        max_score = 0.0
        risk_distribution = {"critical": 0, "high": 0, "medium": 0, "low": 0, "minimal": 0}

        for r in results:
            score = r.payload.get("risk_score", 0.0)
            level = r.payload.get("risk_level", "low")

            total_score += score
            max_score = max(max_score, score)
            if level in risk_distribution:
                risk_distribution[level] += 1

        count = len(results)
        avg_score = total_score / count if count > 0 else 0.0

        # Determine overall risk level from average
        if avg_score >= 8.0:
            risk_level = RiskLevel.CRITICAL
        elif avg_score >= 6.0:
            risk_level = RiskLevel.HIGH
        elif avg_score >= 4.0:
            risk_level = RiskLevel.MEDIUM
        elif avg_score >= 2.0:
            risk_level = RiskLevel.LOW
        else:
            risk_level = RiskLevel.MINIMAL

        context = self._get_customer_context()

        return RiskAggregation(
            aggregation_id=str(uuid4()),
            aggregation_type=aggregation_type,
            group_id=group_id,
            customer_id=context.customer_id,
            total_entities=count,
            avg_risk_score=avg_score,
            max_risk_score=max_score,
            risk_level=risk_level,
            risk_distribution=risk_distribution,
            calculated_at=datetime.utcnow(),
        )

    def get_dashboard_summary(self) -> Dict[str, Any]:
        """Get comprehensive risk dashboard summary."""
        context = self._get_customer_context()

        # Get all risk scores
        results, _ = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(key="customer_id", match=MatchValue(value=context.customer_id)),
                    FieldCondition(key="record_type", match=MatchValue(value="risk_score")),
                ]
            ),
            limit=1000,
        )

        risk_distribution = {"critical": 0, "high": 0, "medium": 0, "low": 0, "minimal": 0}
        total_score = 0.0

        for r in results:
            level = r.payload.get("risk_level", "low")
            if level in risk_distribution:
                risk_distribution[level] += 1
            total_score += r.payload.get("risk_score", 0.0)

        total_count = len(results)
        avg_score = total_score / total_count if total_count > 0 else 0.0

        return {
            "customer_id": context.customer_id,
            "total_entities": total_count,
            "avg_risk_score": round(avg_score, 2),
            "risk_distribution": risk_distribution,
            "critical_count": risk_distribution["critical"],
            "high_count": risk_distribution["high"],
            "generated_at": datetime.utcnow().isoformat(),
        }

    def get_risk_matrix(self) -> Dict[str, Any]:
        """Get risk matrix data (likelihood vs impact)."""
        context = self._get_customer_context()

        matrix = {
            "low_low": 0,
            "low_medium": 0,
            "low_high": 0,
            "medium_low": 0,
            "medium_medium": 0,
            "medium_high": 0,
            "high_low": 0,
            "high_medium": 0,
            "high_high": 0,
        }

        results, _ = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(key="customer_id", match=MatchValue(value=context.customer_id)),
                    FieldCondition(key="record_type", match=MatchValue(value="risk_score")),
                ]
            ),
            limit=1000,
        )

        for r in results:
            # Simplified: use risk score to determine position
            score = r.payload.get("risk_score", 0.0)

            if score >= 7.0:
                likelihood = "high"
                impact = "high"
            elif score >= 5.0:
                likelihood = "medium"
                impact = "high"
            elif score >= 3.0:
                likelihood = "medium"
                impact = "medium"
            else:
                likelihood = "low"
                impact = "low"

            key = f"{likelihood}_{impact}"
            if key in matrix:
                matrix[key] += 1

        return {
            "customer_id": context.customer_id,
            "matrix": matrix,
            "generated_at": datetime.utcnow().isoformat(),
        }
