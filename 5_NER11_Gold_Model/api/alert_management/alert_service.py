"""
Alert Management Service
=========================

Service layer for E09: Alert Management.
Provides CRUD operations, semantic search, and alert correlation
with customer isolation and Qdrant vector storage.

Version: 1.0.0
Created: 2025-12-04
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
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
class AlertSearchRequest:
    """Request parameters for alert search."""
    query: Optional[str] = None
    customer_id: Optional[str] = None
    severity: Optional[str] = None
    status: Optional[str] = None
    event_type: Optional[str] = None
    source: Optional[str] = None
    limit: int = 50


@dataclass
class AlertSearchResult:
    """Single alert search result."""
    alert: Any  # Alert object
    score: float = 0.0


# =============================================================================
# Alert Service
# =============================================================================


class AlertService:
    """
    Service for alert management and correlation.

    Provides customer-isolated operations for:
    - Alert lifecycle management
    - Alert rule configuration
    - Notification rule management
    - Escalation policies
    - Alert correlation and pattern detection
    """

    COLLECTION_NAME = "ner11_alerts"
    VECTOR_SIZE = 384  # sentence-transformers/all-MiniLM-L6-v2

    def __init__(
        self,
        qdrant_url: str = "http://localhost:6333",
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
    ):
        """
        Initialize alert service.

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
        additional_conditions: Optional[List[FieldCondition]] = None,
    ) -> Filter:
        """Build Qdrant filter with customer isolation."""
        conditions = [
            FieldCondition(
                key="customer_id",
                match=MatchValue(value=customer_id),
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
    # Alert Operations
    # =========================================================================

    def create_alert(self, alert: Any) -> Any:
        """Create a new alert with customer isolation."""
        context = self._get_customer_context()

        if not context.can_write():
            raise PermissionError("Write access required to create alert")

        if alert.customer_id != context.customer_id:
            raise ValueError("Alert customer_id must match context customer_id")

        # Generate embedding from alert title and description
        embed_text = f"{alert.title} {alert.description or ''} {alert.event_type}"
        embedding = self._generate_embedding(embed_text)

        # Store in Qdrant
        point_id = self._generate_point_id()
        self.qdrant_client.upsert(
            collection_name=self.COLLECTION_NAME,
            points=[
                PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload=alert.to_qdrant_payload(),
                )
            ],
        )

        logger.info(f"Created alert {alert.alert_id}: {alert.title}")
        return alert

    def get_alert(self, alert_id: str) -> Optional[Any]:
        """Get alert by ID with customer isolation."""
        context = self._get_customer_context()

        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(key="alert_id", match=MatchValue(value=alert_id)),
                    FieldCondition(
                        key="customer_id",
                        match=MatchValue(value=context.customer_id),
                    ),
                    FieldCondition(key="entity_type", match=MatchValue(value="alert")),
                ]
            ),
            limit=1,
        )

        if results[0]:
            payload = results[0][0].payload
            return self._payload_to_alert(payload)
        return None

    def update_alert(self, alert_id: str, update_data: Dict[str, Any]) -> Optional[Any]:
        """Update an existing alert."""
        context = self._get_customer_context()

        if not context.can_write():
            raise PermissionError("Write access required to update alert")

        # Get existing alert
        alert = self.get_alert(alert_id)
        if not alert:
            return None

        # Update fields
        for key, value in update_data.items():
            if hasattr(alert, key) and value is not None:
                setattr(alert, key, value)

        alert.updated_at = datetime.utcnow()

        # Regenerate embedding if title or description changed
        if 'title' in update_data or 'description' in update_data:
            embed_text = f"{alert.title} {alert.description or ''} {alert.event_type}"
            embedding = self._generate_embedding(embed_text)
        else:
            # Use existing embedding
            results = self.qdrant_client.scroll(
                collection_name=self.COLLECTION_NAME,
                scroll_filter=Filter(
                    must=[
                        FieldCondition(key="alert_id", match=MatchValue(value=alert_id)),
                        FieldCondition(key="customer_id", match=MatchValue(value=context.customer_id)),
                    ]
                ),
                limit=1,
            )
            point_id = results[0][0].id
            embedding = None  # Will use existing vector

        # Update in Qdrant
        if embedding:
            # Find and update point
            results = self.qdrant_client.scroll(
                collection_name=self.COLLECTION_NAME,
                scroll_filter=Filter(
                    must=[
                        FieldCondition(key="alert_id", match=MatchValue(value=alert_id)),
                        FieldCondition(key="customer_id", match=MatchValue(value=context.customer_id)),
                    ]
                ),
                limit=1,
            )
            if results[0]:
                point_id = results[0][0].id
                self.qdrant_client.upsert(
                    collection_name=self.COLLECTION_NAME,
                    points=[
                        PointStruct(
                            id=point_id,
                            vector=embedding,
                            payload=alert.to_qdrant_payload(),
                        )
                    ],
                )

        logger.info(f"Updated alert {alert_id}")
        return alert

    def delete_alert(self, alert_id: str) -> bool:
        """Delete an alert."""
        context = self._get_customer_context()

        if not context.can_admin():
            raise PermissionError("Admin access required to delete alert")

        # Find alert point
        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(key="alert_id", match=MatchValue(value=alert_id)),
                    FieldCondition(key="customer_id", match=MatchValue(value=context.customer_id)),
                ]
            ),
            limit=1,
        )

        if not results[0]:
            return False

        point_id = results[0][0].id
        self.qdrant_client.delete(
            collection_name=self.COLLECTION_NAME,
            points_selector=[point_id],
        )

        logger.info(f"Deleted alert {alert_id}")
        return True

    def _payload_to_alert(self, payload: Dict[str, Any]) -> Any:
        """Convert Qdrant payload to Alert object."""
        from .alert_models import Alert, AlertSeverity, AlertStatus

        return Alert(
            alert_id=payload["alert_id"],
            customer_id=payload["customer_id"],
            title=payload["title"],
            description=payload.get("description"),
            severity=AlertSeverity(payload.get("severity", "medium")),
            status=AlertStatus(payload.get("status", "open")),
            source=payload["source"],
            event_type=payload["event_type"],
            affected_assets=payload.get("affected_assets", []),
            tags=payload.get("tags", []),
            metadata=payload.get("metadata", {}),
            created_at=datetime.fromisoformat(payload["created_at"]) if payload.get("created_at") else datetime.utcnow(),
            updated_at=datetime.fromisoformat(payload["updated_at"]) if payload.get("updated_at") else datetime.utcnow(),
            assigned_to=payload.get("assigned_to"),
            acknowledged_at=datetime.fromisoformat(payload["acknowledged_at"]) if payload.get("acknowledged_at") else None,
            resolved_at=datetime.fromisoformat(payload["resolved_at"]) if payload.get("resolved_at") else None,
        )

    def search_alerts(self, request: AlertSearchRequest) -> List[AlertSearchResult]:
        """Search alerts with filters and optional semantic search."""
        context = self._get_customer_context()
        customer_id = request.customer_id or context.customer_id

        conditions = [
            FieldCondition(key="entity_type", match=MatchValue(value="alert"))
        ]

        if request.severity:
            conditions.append(
                FieldCondition(key="severity", match=MatchValue(value=request.severity))
            )

        if request.status:
            conditions.append(
                FieldCondition(key="status", match=MatchValue(value=request.status))
            )

        if request.event_type:
            conditions.append(
                FieldCondition(key="event_type", match=MatchValue(value=request.event_type))
            )

        if request.source:
            conditions.append(
                FieldCondition(key="source", match=MatchValue(value=request.source))
            )

        search_filter = self._build_customer_filter(
            customer_id,
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
                AlertSearchResult(
                    alert=self._payload_to_alert(result.payload),
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
                AlertSearchResult(
                    alert=self._payload_to_alert(point.payload),
                    score=1.0,
                )
                for point in results[0]
            ]

    def get_alerts_by_severity(self, severity: str, limit: int = 100) -> List[AlertSearchResult]:
        """Get alerts by severity level."""
        context = self._get_customer_context()

        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=self._build_customer_filter(
                context.customer_id,
                additional_conditions=[
                    FieldCondition(key="entity_type", match=MatchValue(value="alert")),
                    FieldCondition(key="severity", match=MatchValue(value=severity)),
                ]
            ),
            limit=limit,
        )

        return [
            AlertSearchResult(
                alert=self._payload_to_alert(point.payload),
                score=1.0,
            )
            for point in results[0]
        ]

    def get_alerts_by_status(self, status: str, limit: int = 100) -> List[AlertSearchResult]:
        """Get alerts by status."""
        context = self._get_customer_context()

        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=self._build_customer_filter(
                context.customer_id,
                additional_conditions=[
                    FieldCondition(key="entity_type", match=MatchValue(value="alert")),
                    FieldCondition(key="status", match=MatchValue(value=status)),
                ]
            ),
            limit=limit,
        )

        return [
            AlertSearchResult(
                alert=self._payload_to_alert(point.payload),
                score=1.0,
            )
            for point in results[0]
        ]

    def acknowledge_alert(self, alert_id: str, user_id: Optional[str] = None) -> Optional[Any]:
        """Acknowledge an alert."""
        from .alert_models import AlertStatus

        update_data = {
            "status": "acknowledged",
            "acknowledged_at": datetime.utcnow(),
        }
        if user_id:
            update_data["assigned_to"] = user_id

        return self.update_alert(alert_id, update_data)

    def resolve_alert(self, alert_id: str) -> Optional[Any]:
        """Resolve an alert."""
        from .alert_models import AlertStatus

        update_data = {
            "status": "resolved",
            "resolved_at": datetime.utcnow(),
        }

        return self.update_alert(alert_id, update_data)

    def assign_alert(self, alert_id: str, assigned_to: str) -> Optional[Any]:
        """Assign an alert to a user."""
        update_data = {
            "assigned_to": assigned_to,
        }

        return self.update_alert(alert_id, update_data)

    # =========================================================================
    # Alert Rule Operations
    # =========================================================================

    def create_alert_rule(self, rule: Any) -> Any:
        """Create a new alert rule."""
        context = self._get_customer_context()

        if not context.can_write():
            raise PermissionError("Write access required to create alert rule")

        if rule.customer_id != context.customer_id:
            raise ValueError("Rule customer_id must match context customer_id")

        # Generate embedding from rule name and description
        embed_text = f"{rule.name} {rule.description or ''}"
        embedding = self._generate_embedding(embed_text)

        # Store in Qdrant
        point_id = self._generate_point_id()
        self.qdrant_client.upsert(
            collection_name=self.COLLECTION_NAME,
            points=[
                PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload=rule.to_qdrant_payload(),
                )
            ],
        )

        logger.info(f"Created alert rule {rule.rule_id}: {rule.name}")
        return rule

    def get_alert_rule(self, rule_id: str) -> Optional[Any]:
        """Get alert rule by ID."""
        context = self._get_customer_context()

        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(key="rule_id", match=MatchValue(value=rule_id)),
                    FieldCondition(key="customer_id", match=MatchValue(value=context.customer_id)),
                    FieldCondition(key="entity_type", match=MatchValue(value="alert_rule")),
                ]
            ),
            limit=1,
        )

        if results[0]:
            payload = results[0][0].payload
            return self._payload_to_alert_rule(payload)
        return None

    def update_alert_rule(self, rule_id: str, update_data: Dict[str, Any]) -> Optional[Any]:
        """Update an alert rule."""
        context = self._get_customer_context()

        if not context.can_write():
            raise PermissionError("Write access required to update alert rule")

        rule = self.get_alert_rule(rule_id)
        if not rule:
            return None

        for key, value in update_data.items():
            if hasattr(rule, key) and value is not None:
                setattr(rule, key, value)

        rule.updated_at = datetime.utcnow()

        # Update in Qdrant (simplified - find and update)
        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(key="rule_id", match=MatchValue(value=rule_id)),
                    FieldCondition(key="customer_id", match=MatchValue(value=context.customer_id)),
                ]
            ),
            limit=1,
        )
        if results[0]:
            point_id = results[0][0].id
            embed_text = f"{rule.name} {rule.description or ''}"
            embedding = self._generate_embedding(embed_text)
            self.qdrant_client.upsert(
                collection_name=self.COLLECTION_NAME,
                points=[
                    PointStruct(
                        id=point_id,
                        vector=embedding,
                        payload=rule.to_qdrant_payload(),
                    )
                ],
            )

        return rule

    def delete_alert_rule(self, rule_id: str) -> bool:
        """Delete an alert rule."""
        context = self._get_customer_context()

        if not context.can_admin():
            raise PermissionError("Admin access required to delete alert rule")

        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(key="rule_id", match=MatchValue(value=rule_id)),
                    FieldCondition(key="customer_id", match=MatchValue(value=context.customer_id)),
                ]
            ),
            limit=1,
        )

        if not results[0]:
            return False

        point_id = results[0][0].id
        self.qdrant_client.delete(
            collection_name=self.COLLECTION_NAME,
            points_selector=[point_id],
        )

        return True

    def list_alert_rules(self, limit: int = 50) -> List[Any]:
        """List alert rules."""
        context = self._get_customer_context()

        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=self._build_customer_filter(
                context.customer_id,
                additional_conditions=[
                    FieldCondition(key="entity_type", match=MatchValue(value="alert_rule")),
                ]
            ),
            limit=limit,
        )

        return [self._payload_to_alert_rule(p.payload) for p in results[0]]

    def enable_alert_rule(self, rule_id: str) -> Optional[Any]:
        """Enable an alert rule."""
        return self.update_alert_rule(rule_id, {"enabled": True})

    def disable_alert_rule(self, rule_id: str) -> Optional[Any]:
        """Disable an alert rule."""
        return self.update_alert_rule(rule_id, {"enabled": False})

    def _payload_to_alert_rule(self, payload: Dict[str, Any]) -> Any:
        """Convert Qdrant payload to AlertRule object."""
        from .alert_models import AlertRule

        return AlertRule(
            rule_id=payload["rule_id"],
            customer_id=payload["customer_id"],
            name=payload["name"],
            description=payload.get("description"),
            enabled=payload.get("enabled", True),
            severity=payload.get("severity", "medium"),
            conditions=payload.get("conditions", {}),
            actions=payload.get("actions", []),
            created_at=datetime.fromisoformat(payload["created_at"]) if payload.get("created_at") else datetime.utcnow(),
            updated_at=datetime.fromisoformat(payload["updated_at"]) if payload.get("updated_at") else datetime.utcnow(),
            triggered_count=payload.get("triggered_count", 0),
        )

    # =========================================================================
    # Notification Rule Operations
    # =========================================================================

    def create_notification_rule(self, notification: Any) -> Any:
        """Create a new notification rule."""
        context = self._get_customer_context()

        if not context.can_write():
            raise PermissionError("Write access required to create notification rule")

        if notification.customer_id != context.customer_id:
            raise ValueError("Notification customer_id must match context customer_id")

        embed_text = f"{notification.name} {' '.join(notification.channels)}"
        embedding = self._generate_embedding(embed_text)

        point_id = self._generate_point_id()
        self.qdrant_client.upsert(
            collection_name=self.COLLECTION_NAME,
            points=[
                PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload=notification.to_qdrant_payload(),
                )
            ],
        )

        logger.info(f"Created notification rule {notification.notification_id}")
        return notification

    def get_notification_rule(self, notification_id: str) -> Optional[Any]:
        """Get notification rule by ID."""
        context = self._get_customer_context()

        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(key="notification_id", match=MatchValue(value=notification_id)),
                    FieldCondition(key="customer_id", match=MatchValue(value=context.customer_id)),
                    FieldCondition(key="entity_type", match=MatchValue(value="notification_rule")),
                ]
            ),
            limit=1,
        )

        if results[0]:
            return self._payload_to_notification_rule(results[0][0].payload)
        return None

    def update_notification_rule(self, notification_id: str, update_data: Dict[str, Any]) -> Optional[Any]:
        """Update a notification rule."""
        context = self._get_customer_context()

        if not context.can_write():
            raise PermissionError("Write access required to update notification rule")

        notification = self.get_notification_rule(notification_id)
        if not notification:
            return None

        for key, value in update_data.items():
            if hasattr(notification, key) and value is not None:
                setattr(notification, key, value)

        # Update in Qdrant
        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(key="notification_id", match=MatchValue(value=notification_id)),
                    FieldCondition(key="customer_id", match=MatchValue(value=context.customer_id)),
                ]
            ),
            limit=1,
        )
        if results[0]:
            point_id = results[0][0].id
            embed_text = f"{notification.name} {' '.join(notification.channels)}"
            embedding = self._generate_embedding(embed_text)
            self.qdrant_client.upsert(
                collection_name=self.COLLECTION_NAME,
                points=[
                    PointStruct(
                        id=point_id,
                        vector=embedding,
                        payload=notification.to_qdrant_payload(),
                    )
                ],
            )

        return notification

    def delete_notification_rule(self, notification_id: str) -> bool:
        """Delete a notification rule."""
        context = self._get_customer_context()

        if not context.can_admin():
            raise PermissionError("Admin access required to delete notification rule")

        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(key="notification_id", match=MatchValue(value=notification_id)),
                    FieldCondition(key="customer_id", match=MatchValue(value=context.customer_id)),
                ]
            ),
            limit=1,
        )

        if not results[0]:
            return False

        point_id = results[0][0].id
        self.qdrant_client.delete(
            collection_name=self.COLLECTION_NAME,
            points_selector=[point_id],
        )

        return True

    def list_notification_rules(self, limit: int = 50) -> List[Any]:
        """List notification rules."""
        context = self._get_customer_context()

        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=self._build_customer_filter(
                context.customer_id,
                additional_conditions=[
                    FieldCondition(key="entity_type", match=MatchValue(value="notification_rule")),
                ]
            ),
            limit=limit,
        )

        return [self._payload_to_notification_rule(p.payload) for p in results[0]]

    def _payload_to_notification_rule(self, payload: Dict[str, Any]) -> Any:
        """Convert Qdrant payload to NotificationRule object."""
        from .alert_models import NotificationRule

        return NotificationRule(
            notification_id=payload["notification_id"],
            customer_id=payload["customer_id"],
            name=payload["name"],
            enabled=payload.get("enabled", True),
            channels=payload.get("channels", []),
            severity_filter=payload.get("severity_filter"),
            event_type_filter=payload.get("event_type_filter"),
            recipients=payload.get("recipients", []),
            configuration=payload.get("configuration", {}),
            created_at=datetime.fromisoformat(payload["created_at"]) if payload.get("created_at") else datetime.utcnow(),
            sent_count=payload.get("sent_count", 0),
        )

    # =========================================================================
    # Escalation Policy Operations
    # =========================================================================

    def create_escalation_policy(self, policy: Any) -> Any:
        """Create a new escalation policy."""
        context = self._get_customer_context()

        if not context.can_write():
            raise PermissionError("Write access required to create escalation policy")

        if policy.customer_id != context.customer_id:
            raise ValueError("Policy customer_id must match context customer_id")

        embed_text = f"{policy.name} {policy.description or ''}"
        embedding = self._generate_embedding(embed_text)

        point_id = self._generate_point_id()
        self.qdrant_client.upsert(
            collection_name=self.COLLECTION_NAME,
            points=[
                PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload=policy.to_qdrant_payload(),
                )
            ],
        )

        logger.info(f"Created escalation policy {policy.policy_id}")
        return policy

    def get_escalation_policy(self, policy_id: str) -> Optional[Any]:
        """Get escalation policy by ID."""
        context = self._get_customer_context()

        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(key="policy_id", match=MatchValue(value=policy_id)),
                    FieldCondition(key="customer_id", match=MatchValue(value=context.customer_id)),
                    FieldCondition(key="entity_type", match=MatchValue(value="escalation_policy")),
                ]
            ),
            limit=1,
        )

        if results[0]:
            return self._payload_to_escalation_policy(results[0][0].payload)
        return None

    def update_escalation_policy(self, policy_id: str, update_data: Dict[str, Any]) -> Optional[Any]:
        """Update an escalation policy."""
        context = self._get_customer_context()

        if not context.can_write():
            raise PermissionError("Write access required to update escalation policy")

        policy = self.get_escalation_policy(policy_id)
        if not policy:
            return None

        for key, value in update_data.items():
            if hasattr(policy, key) and value is not None:
                setattr(policy, key, value)

        # Update in Qdrant
        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(key="policy_id", match=MatchValue(value=policy_id)),
                    FieldCondition(key="customer_id", match=MatchValue(value=context.customer_id)),
                ]
            ),
            limit=1,
        )
        if results[0]:
            point_id = results[0][0].id
            embed_text = f"{policy.name} {policy.description or ''}"
            embedding = self._generate_embedding(embed_text)
            self.qdrant_client.upsert(
                collection_name=self.COLLECTION_NAME,
                points=[
                    PointStruct(
                        id=point_id,
                        vector=embedding,
                        payload=policy.to_qdrant_payload(),
                    )
                ],
            )

        return policy

    def delete_escalation_policy(self, policy_id: str) -> bool:
        """Delete an escalation policy."""
        context = self._get_customer_context()

        if not context.can_admin():
            raise PermissionError("Admin access required to delete escalation policy")

        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(key="policy_id", match=MatchValue(value=policy_id)),
                    FieldCondition(key="customer_id", match=MatchValue(value=context.customer_id)),
                ]
            ),
            limit=1,
        )

        if not results[0]:
            return False

        point_id = results[0][0].id
        self.qdrant_client.delete(
            collection_name=self.COLLECTION_NAME,
            points_selector=[point_id],
        )

        return True

    def list_escalation_policies(self, limit: int = 50) -> List[Any]:
        """List escalation policies."""
        context = self._get_customer_context()

        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=self._build_customer_filter(
                context.customer_id,
                additional_conditions=[
                    FieldCondition(key="entity_type", match=MatchValue(value="escalation_policy")),
                ]
            ),
            limit=limit,
        )

        return [self._payload_to_escalation_policy(p.payload) for p in results[0]]

    def _payload_to_escalation_policy(self, payload: Dict[str, Any]) -> Any:
        """Convert Qdrant payload to EscalationPolicy object."""
        from .alert_models import EscalationPolicy

        return EscalationPolicy(
            policy_id=payload["policy_id"],
            customer_id=payload["customer_id"],
            name=payload["name"],
            description=payload.get("description"),
            enabled=payload.get("enabled", True),
            escalation_levels=payload.get("escalation_levels", []),
            severity_filter=payload.get("severity_filter"),
            created_at=datetime.fromisoformat(payload["created_at"]) if payload.get("created_at") else datetime.utcnow(),
            triggered_count=payload.get("triggered_count", 0),
        )

    # =========================================================================
    # Alert Correlation Operations
    # =========================================================================

    def create_alert_correlation(self, correlation: Any) -> Any:
        """Create a new alert correlation."""
        context = self._get_customer_context()

        if not context.can_write():
            raise PermissionError("Write access required to create alert correlation")

        if correlation.customer_id != context.customer_id:
            raise ValueError("Correlation customer_id must match context customer_id")

        embed_text = f"{correlation.name} {correlation.correlation_type} {correlation.description or ''}"
        embedding = self._generate_embedding(embed_text)

        point_id = self._generate_point_id()
        self.qdrant_client.upsert(
            collection_name=self.COLLECTION_NAME,
            points=[
                PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload=correlation.to_qdrant_payload(),
                )
            ],
        )

        logger.info(f"Created alert correlation {correlation.correlation_id}")
        return correlation

    def get_alert_correlation(self, correlation_id: str) -> Optional[Any]:
        """Get alert correlation by ID."""
        context = self._get_customer_context()

        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(key="correlation_id", match=MatchValue(value=correlation_id)),
                    FieldCondition(key="customer_id", match=MatchValue(value=context.customer_id)),
                    FieldCondition(key="entity_type", match=MatchValue(value="alert_correlation")),
                ]
            ),
            limit=1,
        )

        if results[0]:
            return self._payload_to_alert_correlation(results[0][0].payload)
        return None

    def list_alert_correlations(self, limit: int = 50) -> List[Any]:
        """List alert correlations."""
        context = self._get_customer_context()

        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=self._build_customer_filter(
                context.customer_id,
                additional_conditions=[
                    FieldCondition(key="entity_type", match=MatchValue(value="alert_correlation")),
                ]
            ),
            limit=limit,
        )

        return [self._payload_to_alert_correlation(p.payload) for p in results[0]]

    def _payload_to_alert_correlation(self, payload: Dict[str, Any]) -> Any:
        """Convert Qdrant payload to AlertCorrelation object."""
        from .alert_models import AlertCorrelation

        return AlertCorrelation(
            correlation_id=payload["correlation_id"],
            customer_id=payload["customer_id"],
            name=payload["name"],
            alert_ids=payload.get("alert_ids", []),
            correlation_type=payload.get("correlation_type", "pattern"),
            confidence=payload.get("confidence", 0.8),
            root_cause_alert_id=payload.get("root_cause_alert_id"),
            description=payload.get("description"),
            created_at=datetime.fromisoformat(payload["created_at"]) if payload.get("created_at") else datetime.utcnow(),
        )

    # =========================================================================
    # Dashboard & Analytics
    # =========================================================================

    def get_dashboard_summary(self) -> Dict[str, Any]:
        """Get alert dashboard summary."""
        context = self._get_customer_context()

        # Get all alerts
        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=self._build_customer_filter(
                context.customer_id,
                additional_conditions=[
                    FieldCondition(key="entity_type", match=MatchValue(value="alert")),
                ]
            ),
            limit=5000,
        )

        alerts = results[0]
        total_alerts = len(alerts)

        # Count by status
        open_alerts = sum(1 for a in alerts if a.payload.get("status") == "open")
        acknowledged_alerts = sum(1 for a in alerts if a.payload.get("status") == "acknowledged")
        investigating_alerts = sum(1 for a in alerts if a.payload.get("status") == "investigating")
        resolved_alerts = sum(1 for a in alerts if a.payload.get("status") == "resolved")

        # Count by severity
        critical_alerts = sum(1 for a in alerts if a.payload.get("severity") == "critical")
        high_alerts = sum(1 for a in alerts if a.payload.get("severity") == "high")
        medium_alerts = sum(1 for a in alerts if a.payload.get("severity") == "medium")
        low_alerts = sum(1 for a in alerts if a.payload.get("severity") == "low")

        # Count recent alerts (last 24 hours)
        now = datetime.utcnow()
        day_ago = now - timedelta(hours=24)
        alerts_last_24h = sum(
            1 for a in alerts
            if datetime.fromisoformat(a.payload.get("created_at", now.isoformat())) > day_ago
        )

        # Count correlations
        correlation_results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=self._build_customer_filter(
                context.customer_id,
                additional_conditions=[
                    FieldCondition(key="entity_type", match=MatchValue(value="alert_correlation")),
                ]
            ),
            limit=1000,
        )
        active_correlations = len(correlation_results[0])

        # Calculate average resolution time
        resolved_with_times = [
            a for a in alerts
            if a.payload.get("status") == "resolved" and a.payload.get("resolved_at")
        ]
        if resolved_with_times:
            total_resolution_time = sum(
                (datetime.fromisoformat(a.payload["resolved_at"]) -
                 datetime.fromisoformat(a.payload["created_at"])).total_seconds() / 60
                for a in resolved_with_times
            )
            avg_resolution_time = total_resolution_time / len(resolved_with_times)
        else:
            avg_resolution_time = 0.0

        return {
            "total_alerts": total_alerts,
            "open_alerts": open_alerts,
            "acknowledged_alerts": acknowledged_alerts,
            "investigating_alerts": investigating_alerts,
            "resolved_alerts": resolved_alerts,
            "critical_alerts": critical_alerts,
            "high_alerts": high_alerts,
            "medium_alerts": medium_alerts,
            "low_alerts": low_alerts,
            "alerts_last_24h": alerts_last_24h,
            "active_correlations": active_correlations,
            "avg_resolution_time_minutes": round(avg_resolution_time, 2),
        }
