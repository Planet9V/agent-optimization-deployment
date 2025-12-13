"""
Prioritization Service
=====================

Business logic for E12: NOW-NEXT-NEVER Prioritization Framework.
Handles priority calculation, categorization, and Qdrant operations.

Version: 1.0.0
Created: 2025-12-04
"""

import os
import logging
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from uuid import uuid4

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue

from ..customer_isolation import CustomerContextManager
from .schemas import (
    PriorityItem,
    PriorityScore,
    PriorityCategory,
    EntityType,
    SLAStatus,
    UrgencyFactor,
    RiskFactor,
    EconomicFactor,
    ScoringFactor,
    PrioritizationConfig,
)

logger = logging.getLogger(__name__)


class PrioritizationService:
    """
    Service for NOW-NEXT-NEVER prioritization operations.

    Integrates with E05 (risk scoring), E10 (economic), E03 (SBOM),
    and E08 (RAMS reliability) for comprehensive prioritization.
    """

    COLLECTION_NAME = "ner11_prioritization"
    VECTOR_SIZE = 384  # MiniLM embedding dimension

    def __init__(self):
        """Initialize prioritization service with Qdrant client."""
        qdrant_url = os.getenv("QDRANT_URL", "http://openspg-qdrant:6333")
        self.client = QdrantClient(url=qdrant_url)
        self._ensure_collection()

    def _ensure_collection(self):
        """Ensure Qdrant collection exists with proper configuration."""
        try:
            collections = self.client.get_collections().collections
            collection_names = [c.name for c in collections]

            if self.COLLECTION_NAME not in collection_names:
                self.client.create_collection(
                    collection_name=self.COLLECTION_NAME,
                    vectors_config=VectorParams(
                        size=self.VECTOR_SIZE,
                        distance=Distance.COSINE
                    ),
                )
                logger.info(f"Created collection: {self.COLLECTION_NAME}")
        except Exception as e:
            logger.error(f"Failed to ensure collection: {e}")
            raise

    def _get_embedding(self, text: str) -> List[float]:
        """Generate embedding for text using sentence-transformers."""
        # In production, use actual embedding model
        # For now, return dummy embedding
        import random
        random.seed(hash(text) % (2**32))
        return [random.random() for _ in range(self.VECTOR_SIZE)]

    def calculate_priority_score(
        self,
        entity_type: EntityType,
        entity_id: str,
        entity_name: str,
        urgency_factors: List[UrgencyFactor],
        risk_factors: List[RiskFactor],
        economic_factors: List[EconomicFactor],
        config: Optional[PrioritizationConfig] = None,
    ) -> PriorityItem:
        """
        Calculate priority score and categorize entity.

        Combines risk, urgency, impact, effort, and ROI factors.
        """
        context = CustomerContextManager.get_context()
        context.validate_write_access()

        # Use default config if not provided
        if not config:
            config = PrioritizationConfig(customer_id=context.customer_id)

        # Calculate component scores
        urgency_score = self._calculate_urgency_score(urgency_factors)
        risk_score = self._calculate_risk_score(risk_factors)
        impact_score = self._calculate_impact_score(risk_factors, economic_factors)
        effort_score = self._calculate_effort_score(entity_type, entity_id)
        roi_score = self._calculate_roi_score(economic_factors, effort_score)

        # Weighted composite score (0-100)
        weights = config.scoring_weights
        priority_score = (
            urgency_score * weights["urgency_weight"] * 100 +
            risk_score * weights["risk_weight"] * 10 +
            impact_score * weights["impact_weight"] * 10 +
            (10 - effort_score) * weights["effort_weight"] * 10 +  # Lower effort = higher priority
            roi_score * weights["roi_weight"] * 10
        )

        # Categorize based on thresholds
        if priority_score >= config.thresholds["now_threshold"]:
            category = PriorityCategory.NOW
            sla_hours = config.sla_config["now_sla_hours"]
        elif priority_score >= config.thresholds["next_threshold"]:
            category = PriorityCategory.NEXT
            sla_hours = config.sla_config["next_sla_hours"]
        else:
            category = PriorityCategory.NEVER
            sla_hours = None

        # Calculate SLA deadline
        sla_deadline = datetime.utcnow() + timedelta(hours=sla_hours) if sla_hours else None

        # Determine earliest deadline from urgency factors
        deadlines = [f.deadline for f in urgency_factors if f.deadline]
        earliest_deadline = min(deadlines) if deadlines else None

        # Determine SLA status
        sla_status = self._calculate_sla_status(sla_deadline)

        # Create priority item
        item = PriorityItem(
            item_id=str(uuid4()),
            customer_id=context.customer_id,
            entity_type=entity_type,
            entity_id=entity_id,
            entity_name=entity_name,
            priority_category=category,
            priority_score=priority_score,
            urgency_factors=urgency_factors,
            risk_factors=risk_factors,
            economic_factors=economic_factors,
            deadline=earliest_deadline,
            sla_status=sla_status,
            sla_deadline=sla_deadline,
        )

        # Store in Qdrant
        self._store_priority_item(item)

        return item

    def _calculate_urgency_score(self, factors: List[UrgencyFactor]) -> float:
        """Calculate urgency score (0-10) from urgency factors."""
        if not factors:
            return 0.0

        weighted_sum = sum(f.value * f.weight for f in factors)
        total_weight = sum(f.weight for f in factors)

        return weighted_sum / total_weight if total_weight > 0 else 0.0

    def _calculate_risk_score(self, factors: List[RiskFactor]) -> float:
        """Calculate risk score (0-10) from risk factors."""
        if not factors:
            return 0.0

        weighted_sum = sum(f.value * f.weight for f in factors)
        total_weight = sum(f.weight for f in factors)

        return weighted_sum / total_weight if total_weight > 0 else 0.0

    def _calculate_impact_score(
        self,
        risk_factors: List[RiskFactor],
        economic_factors: List[EconomicFactor]
    ) -> float:
        """Calculate business impact score (0-10)."""
        # Use risk factors as proxy for impact
        risk_score = self._calculate_risk_score(risk_factors)

        # Adjust based on economic factors
        if economic_factors:
            max_economic_value = max(abs(f.value) for f in economic_factors)
            # Normalize to 0-10 range (assuming max $1M impact)
            economic_impact = min(max_economic_value / 100000, 10.0)
            return (risk_score + economic_impact) / 2

        return risk_score

    def _calculate_effort_score(self, entity_type: EntityType, entity_id: str) -> float:
        """Calculate remediation effort score (0-10, higher = more effort)."""
        # Simplified effort estimation
        # In production, integrate with remediation planning system
        effort_map = {
            EntityType.VULNERABILITY: 5.0,
            EntityType.REMEDIATION: 6.0,
            EntityType.COMPLIANCE: 7.0,
            EntityType.RISK: 5.0,
            EntityType.INCIDENT: 8.0,
        }
        return effort_map.get(entity_type, 5.0)

    def _calculate_roi_score(
        self,
        economic_factors: List[EconomicFactor],
        effort_score: float
    ) -> float:
        """Calculate ROI score (0-10)."""
        if not economic_factors:
            return 5.0  # Neutral ROI

        # Calculate total economic value
        total_value = sum(f.value * f.weight for f in economic_factors)

        # ROI = value / effort (normalized)
        roi = total_value / (effort_score * 10000) if effort_score > 0 else 0.0

        # Normalize to 0-10 range
        return min(max(roi * 10, 0.0), 10.0)

    def _calculate_sla_status(self, sla_deadline: Optional[datetime]) -> SLAStatus:
        """Calculate SLA status based on deadline."""
        if not sla_deadline:
            return SLAStatus.WITHIN_SLA

        now = datetime.utcnow()
        time_remaining = (sla_deadline - now).total_seconds() / 3600  # hours

        if time_remaining < 0:
            return SLAStatus.BREACHED
        elif time_remaining < 4:  # Less than 4 hours
            return SLAStatus.AT_RISK
        else:
            return SLAStatus.WITHIN_SLA

    def _store_priority_item(self, item: PriorityItem):
        """Store priority item in Qdrant."""
        # Generate embedding from entity name + description
        text = f"{item.entity_name} {item.entity_type.value} priority:{item.priority_category.value}"
        embedding = self._get_embedding(text)

        point = PointStruct(
            id=item.item_id,
            vector=embedding,
            payload=item.to_qdrant_payload(),
        )

        self.client.upsert(
            collection_name=self.COLLECTION_NAME,
            points=[point],
        )

    def get_now_items(self, limit: int = 100) -> List[PriorityItem]:
        """Get all items requiring immediate action (NOW category)."""
        context = CustomerContextManager.get_context()

        results = self.client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(
                        key="customer_id",
                        match=MatchValue(value=context.customer_id)
                    ),
                    FieldCondition(
                        key="priority_category",
                        match=MatchValue(value="NOW")
                    ),
                ]
            ),
            limit=limit,
        )

        return [self._payload_to_priority_item(r.payload) for r in results[0]]

    def get_next_items(self, limit: int = 100) -> List[PriorityItem]:
        """Get all items scheduled for next action cycle."""
        context = CustomerContextManager.get_context()

        results = self.client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(
                        key="customer_id",
                        match=MatchValue(value=context.customer_id)
                    ),
                    FieldCondition(
                        key="priority_category",
                        match=MatchValue(value="NEXT")
                    ),
                ]
            ),
            limit=limit,
        )

        return [self._payload_to_priority_item(r.payload) for r in results[0]]

    def get_never_items(self, limit: int = 100) -> List[PriorityItem]:
        """Get all items designated as NEVER."""
        context = CustomerContextManager.get_context()

        results = self.client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(
                        key="customer_id",
                        match=MatchValue(value=context.customer_id)
                    ),
                    FieldCondition(
                        key="priority_category",
                        match=MatchValue(value="NEVER")
                    ),
                ]
            ),
            limit=limit,
        )

        return [self._payload_to_priority_item(r.payload) for r in results[0]]

    def get_sla_status_items(self, sla_status: SLAStatus, limit: int = 100) -> List[PriorityItem]:
        """Get items by SLA status."""
        context = CustomerContextManager.get_context()

        results = self.client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(
                        key="customer_id",
                        match=MatchValue(value=context.customer_id)
                    ),
                    FieldCondition(
                        key="sla_status",
                        match=MatchValue(value=sla_status.value)
                    ),
                ]
            ),
            limit=limit,
        )

        return [self._payload_to_priority_item(r.payload) for r in results[0]]

    def escalate_to_now(self, item_id: str) -> PriorityItem:
        """Escalate item to NOW priority."""
        context = CustomerContextManager.get_context()
        context.validate_write_access()

        # Retrieve item
        result = self.client.retrieve(
            collection_name=self.COLLECTION_NAME,
            ids=[item_id],
        )

        if not result or result[0].payload["customer_id"] != context.customer_id:
            raise ValueError(f"Item {item_id} not found")

        # Update priority
        payload = result[0].payload
        payload["priority_category"] = "NOW"
        payload["sla_status"] = "within_sla"
        payload["sla_deadline"] = (datetime.utcnow() + timedelta(hours=24)).isoformat()

        # Update in Qdrant
        self.client.set_payload(
            collection_name=self.COLLECTION_NAME,
            payload=payload,
            points=[item_id],
        )

        return self._payload_to_priority_item(payload)

    def promote_next_to_now(self, item_id: str) -> PriorityItem:
        """Promote NEXT item to NOW priority."""
        return self.escalate_to_now(item_id)

    def classify_as_never(self, item_id: str, reason: str) -> PriorityItem:
        """Classify item as NEVER priority."""
        context = CustomerContextManager.get_context()
        context.validate_write_access()

        # Retrieve item
        result = self.client.retrieve(
            collection_name=self.COLLECTION_NAME,
            ids=[item_id],
        )

        if not result or result[0].payload["customer_id"] != context.customer_id:
            raise ValueError(f"Item {item_id} not found")

        # Update priority
        payload = result[0].payload
        payload["priority_category"] = "NEVER"
        payload["sla_status"] = "within_sla"
        payload["sla_deadline"] = None

        # Update in Qdrant
        self.client.set_payload(
            collection_name=self.COLLECTION_NAME,
            payload=payload,
            points=[item_id],
        )

        return self._payload_to_priority_item(payload)

    def get_dashboard_summary(self) -> Dict[str, Any]:
        """Get prioritization dashboard summary."""
        context = CustomerContextManager.get_context()

        # Get counts by category
        now_items = self.get_now_items()
        next_items = self.get_next_items()
        never_items = self.get_never_items()

        # Calculate distributions
        total_items = len(now_items) + len(next_items) + len(never_items)

        distribution = {
            "NOW": len(now_items),
            "NEXT": len(next_items),
            "NEVER": len(never_items),
        }

        # Calculate SLA metrics
        sla_breached = len([i for i in now_items + next_items if i.sla_status == SLAStatus.BREACHED])
        sla_at_risk = len([i for i in now_items + next_items if i.sla_status == SLAStatus.AT_RISK])

        return {
            "customer_id": context.customer_id,
            "total_items": total_items,
            "distribution": distribution,
            "sla_breached": sla_breached,
            "sla_at_risk": sla_at_risk,
            "generated_at": datetime.utcnow().isoformat(),
        }

    def _payload_to_priority_item(self, payload: Dict[str, Any]) -> PriorityItem:
        """Convert Qdrant payload to PriorityItem."""
        return PriorityItem(
            item_id=payload["item_id"],
            customer_id=payload["customer_id"],
            entity_type=EntityType(payload["entity_type"]),
            entity_id=payload["entity_id"],
            entity_name=payload["entity_name"],
            priority_category=PriorityCategory(payload["priority_category"]),
            priority_score=payload["priority_score"],
            urgency_factors=[],  # Would need to deserialize from payload
            risk_factors=[],
            economic_factors=[],
            deadline=datetime.fromisoformat(payload["deadline"]) if payload.get("deadline") else None,
            sla_status=SLAStatus(payload["sla_status"]),
            sla_deadline=datetime.fromisoformat(payload["sla_deadline"]) if payload.get("sla_deadline") else None,
            calculated_at=datetime.fromisoformat(payload["calculated_at"]),
        )
