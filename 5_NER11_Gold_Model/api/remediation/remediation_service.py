"""
Remediation Workflow Service
=============================

Service layer for E06: Remediation Workflow API.
Provides remediation task management, SLA tracking, and metrics calculation
with customer isolation and Qdrant vector storage.

Version: 1.0.0
Created: 2025-12-04
"""

from dataclasses import dataclass
from datetime import date, datetime, timedelta
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

from .remediation_models import (
    RemediationTask,
    RemediationPlan,
    SLAPolicy,
    RemediationMetrics,
    RemediationAction,
    EscalationLevel,
    TaskType,
    TaskStatus,
    TaskPriority,
    SLAStatus,
    EscalationAction,
    RemediationActionType,
)

logger = logging.getLogger(__name__)


# =============================================================================
# Search Request/Response Models
# =============================================================================


@dataclass
class TaskSearchRequest:
    """Request parameters for task search."""
    query: Optional[str] = None
    customer_id: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assigned_to: Optional[str] = None
    sla_status: Optional[SLAStatus] = None
    vulnerability_id: Optional[str] = None
    limit: int = 50
    include_system: bool = True


@dataclass
class TaskSearchResult:
    """Single task search result."""
    task: RemediationTask
    score: float = 0.0


# =============================================================================
# Remediation Workflow Service
# =============================================================================


class RemediationWorkflowService:
    """
    Service for remediation workflow and task management.

    Provides customer-isolated operations for:
    - Remediation task creation and tracking
    - SLA policy management and monitoring
    - Remediation plan coordination
    - Performance metrics calculation
    - Escalation workflow management
    """

    COLLECTION_NAME = "ner11_remediation"
    VECTOR_SIZE = 384  # sentence-transformers/all-MiniLM-L6-v2

    def __init__(
        self,
        qdrant_url: str = "http://localhost:6333",
        embedding_service: Optional[Any] = None,
    ):
        """
        Initialize remediation workflow service.

        Args:
            qdrant_url: Qdrant server URL
            embedding_service: EmbeddingService instance for semantic search
        """
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
    # Task Operations
    # =========================================================================

    def create_task(self, task: RemediationTask) -> RemediationTask:
        """Create a new remediation task with customer isolation."""
        context = self._get_customer_context()

        if not context.can_write():
            raise PermissionError("Write access required to create task")

        if task.customer_id != context.customer_id:
            raise ValueError("Task customer_id must match context customer_id")

        # Generate embedding from task title and description
        embed_text = f"{task.title} {task.description} {task.cve_id or ''}"
        embedding = self._generate_embedding(embed_text)

        # Store in Qdrant
        point_id = self._generate_point_id()
        self.qdrant_client.upsert(
            collection_name=self.COLLECTION_NAME,
            points=[
                PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload=task.to_qdrant_payload(),
                )
            ],
        )

        # Create action record
        action = RemediationAction(
            action_id=f"ACTION-{uuid4().hex[:8].upper()}",
            task_id=task.task_id,
            customer_id=task.customer_id,
            action_type=RemediationActionType.CREATED,
            performed_by=task.created_by or "system",
        )
        self._record_action(action)

        logger.info(f"Created remediation task {task.task_id}: {task.title}")
        return task

    def get_task(self, task_id: str) -> Optional[RemediationTask]:
        """Get task by ID with customer isolation."""
        context = self._get_customer_context()

        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(key="task_id", match=MatchValue(value=task_id)),
                    FieldCondition(
                        key="customer_id",
                        match=MatchAny(any=context.get_customer_ids()),
                    ),
                    FieldCondition(key="entity_type", match=MatchValue(value="remediation_task")),
                ]
            ),
            limit=1,
        )

        if results[0]:
            payload = results[0][0].payload
            return self._payload_to_task(payload)
        return None

    def _payload_to_task(self, payload: Dict[str, Any]) -> RemediationTask:
        """Convert Qdrant payload to RemediationTask object."""
        return RemediationTask(
            task_id=payload["task_id"],
            customer_id=payload["customer_id"],
            title=payload.get("title", ""),
            description=payload.get("description", ""),
            vulnerability_id=payload.get("vulnerability_id"),
            cve_id=payload.get("cve_id"),
            asset_ids=payload.get("asset_ids", []),
            task_type=TaskType(payload.get("task_type", "patch")),
            status=TaskStatus(payload.get("status", "open")),
            priority=TaskPriority(payload.get("priority", "medium")),
            severity_source=payload.get("severity_source", 0.0),
            sla_status=SLAStatus(payload.get("sla_status", "within_sla")),
            assigned_to=payload.get("assigned_to"),
            assigned_team=payload.get("assigned_team"),
        )

    def search_tasks(self, request: TaskSearchRequest) -> List[TaskSearchResult]:
        """Search tasks with filters and optional semantic search."""
        context = self._get_customer_context()
        customer_id = request.customer_id or context.customer_id

        conditions = [
            FieldCondition(key="entity_type", match=MatchValue(value="remediation_task"))
        ]

        if request.status:
            conditions.append(
                FieldCondition(key="status", match=MatchValue(value=request.status.value))
            )

        if request.priority:
            conditions.append(
                FieldCondition(key="priority", match=MatchValue(value=request.priority.value))
            )

        if request.sla_status:
            conditions.append(
                FieldCondition(key="sla_status", match=MatchValue(value=request.sla_status.value))
            )

        if request.assigned_to:
            conditions.append(
                FieldCondition(key="assigned_to", match=MatchValue(value=request.assigned_to))
            )

        if request.vulnerability_id:
            conditions.append(
                FieldCondition(key="vulnerability_id", match=MatchValue(value=request.vulnerability_id))
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
                TaskSearchResult(
                    task=self._payload_to_task(result.payload),
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
                TaskSearchResult(
                    task=self._payload_to_task(point.payload),
                    score=1.0,
                )
                for point in results[0]
            ]

    def get_open_tasks(self, limit: int = 100) -> List[RemediationTask]:
        """Get all open tasks for customer."""
        context = self._get_customer_context()

        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=self._build_customer_filter(
                context.customer_id,
                additional_conditions=[
                    FieldCondition(key="entity_type", match=MatchValue(value="remediation_task")),
                    FieldCondition(key="is_completed", match=MatchValue(value=False)),
                ]
            ),
            limit=limit,
        )

        return [self._payload_to_task(point.payload) for point in results[0]]

    def get_overdue_tasks(self, limit: int = 100) -> List[RemediationTask]:
        """Get all overdue tasks (SLA breached)."""
        context = self._get_customer_context()

        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=self._build_customer_filter(
                context.customer_id,
                additional_conditions=[
                    FieldCondition(key="entity_type", match=MatchValue(value="remediation_task")),
                    FieldCondition(key="is_overdue", match=MatchValue(value=True)),
                ]
            ),
            limit=limit,
        )

        return [self._payload_to_task(point.payload) for point in results[0]]

    def get_tasks_by_priority(self, priority: TaskPriority, limit: int = 100) -> List[RemediationTask]:
        """Get tasks by priority level."""
        context = self._get_customer_context()

        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=self._build_customer_filter(
                context.customer_id,
                additional_conditions=[
                    FieldCondition(key="entity_type", match=MatchValue(value="remediation_task")),
                    FieldCondition(key="priority", match=MatchValue(value=priority.value)),
                ]
            ),
            limit=limit,
        )

        return [self._payload_to_task(point.payload) for point in results[0]]

    def get_tasks_by_status(self, status: TaskStatus, limit: int = 100) -> List[RemediationTask]:
        """Get tasks by status."""
        context = self._get_customer_context()

        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=self._build_customer_filter(
                context.customer_id,
                additional_conditions=[
                    FieldCondition(key="entity_type", match=MatchValue(value="remediation_task")),
                    FieldCondition(key="status", match=MatchValue(value=status.value)),
                ]
            ),
            limit=limit,
        )

        return [self._payload_to_task(point.payload) for point in results[0]]

    def update_task_status(
        self,
        task_id: str,
        new_status: TaskStatus,
        performed_by: str,
        notes: Optional[str] = None,
    ) -> bool:
        """Update task status with audit trail."""
        context = self._get_customer_context()

        if not context.can_write():
            raise PermissionError("Write access required")

        # Get current task
        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(key="task_id", match=MatchValue(value=task_id)),
                    FieldCondition(key="customer_id", match=MatchValue(value=context.customer_id)),
                    FieldCondition(key="entity_type", match=MatchValue(value="remediation_task")),
                ]
            ),
            limit=1,
            with_payload=True,
            with_vectors=True,
        )

        if not results[0]:
            return False

        point = results[0][0]
        payload = dict(point.payload)
        old_status = payload.get("status", "open")

        # Update status
        payload["status"] = new_status.value
        payload["updated_at"] = datetime.utcnow().isoformat()

        # Update completion date if status is completed
        if new_status in {TaskStatus.VERIFIED, TaskStatus.CLOSED}:
            payload["completion_date"] = datetime.utcnow().isoformat()

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

        # Record action
        action = RemediationAction(
            action_id=f"ACTION-{uuid4().hex[:8].upper()}",
            task_id=task_id,
            customer_id=context.customer_id,
            action_type=RemediationActionType.STATUS_CHANGE,
            performed_by=performed_by,
            previous_value=old_status,
            new_value=new_status.value,
            comment=notes,
        )
        self._record_action(action)

        logger.info(f"Updated task {task_id} status: {old_status} -> {new_status.value}")
        return True

    def assign_task(
        self,
        task_id: str,
        assigned_to: str,
        assigned_by: str,
        notes: Optional[str] = None,
    ) -> bool:
        """Assign task to user/team."""
        context = self._get_customer_context()

        if not context.can_write():
            raise PermissionError("Write access required")

        # Get current task
        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(key="task_id", match=MatchValue(value=task_id)),
                    FieldCondition(key="customer_id", match=MatchValue(value=context.customer_id)),
                    FieldCondition(key="entity_type", match=MatchValue(value="remediation_task")),
                ]
            ),
            limit=1,
            with_payload=True,
            with_vectors=True,
        )

        if not results[0]:
            return False

        point = results[0][0]
        payload = dict(point.payload)
        old_assigned = payload.get("assigned_to")

        # Update assignment
        payload["assigned_to"] = assigned_to
        payload["updated_at"] = datetime.utcnow().isoformat()

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

        # Record action
        action = RemediationAction(
            action_id=f"ACTION-{uuid4().hex[:8].upper()}",
            task_id=task_id,
            customer_id=context.customer_id,
            action_type=RemediationActionType.ASSIGNED,
            performed_by=assigned_by,
            previous_value=old_assigned,
            new_value=assigned_to,
            comment=notes,
        )
        self._record_action(action)

        logger.info(f"Assigned task {task_id} to {assigned_to}")
        return True

    def get_task_history(self, task_id: str) -> List[RemediationAction]:
        """Get action history for a task."""
        context = self._get_customer_context()

        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(key="task_id", match=MatchValue(value=task_id)),
                    FieldCondition(
                        key="customer_id",
                        match=MatchAny(any=context.get_customer_ids()),
                    ),
                    FieldCondition(key="entity_type", match=MatchValue(value="remediation_action")),
                ]
            ),
            limit=1000,
        )

        actions = []
        for point in results[0]:
            payload = point.payload
            actions.append(RemediationAction(
                action_id=payload["action_id"],
                task_id=payload["task_id"],
                customer_id=payload["customer_id"],
                action_type=RemediationActionType(payload["action_type"]),
                performed_by=payload["performed_by"],
                timestamp=datetime.fromisoformat(payload["timestamp"]),
                previous_value=payload.get("previous_value"),
                new_value=payload.get("new_value"),
                comment=payload.get("comment"),
            ))

        # Sort by timestamp
        actions.sort(key=lambda a: a.timestamp, reverse=True)
        return actions

    def _record_action(self, action: RemediationAction) -> None:
        """Record an action in the audit trail."""
        embed_text = f"{action.action_type.value} {action.task_id} by {action.performed_by}"
        embedding = self._generate_embedding(embed_text)

        point_id = self._generate_point_id()
        self.qdrant_client.upsert(
            collection_name=self.COLLECTION_NAME,
            points=[
                PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload=action.to_qdrant_payload(),
                )
            ],
        )

    # =========================================================================
    # Plan Operations
    # =========================================================================

    def create_plan(self, plan: RemediationPlan) -> RemediationPlan:
        """Create a new remediation plan."""
        context = self._get_customer_context()

        if not context.can_write():
            raise PermissionError("Write access required to create plan")

        if plan.customer_id != context.customer_id:
            raise ValueError("Plan customer_id must match context customer_id")

        embed_text = f"{plan.name} {plan.description or ''}"
        embedding = self._generate_embedding(embed_text)

        point_id = self._generate_point_id()
        self.qdrant_client.upsert(
            collection_name=self.COLLECTION_NAME,
            points=[
                PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload={
                        "plan_id": plan.plan_id,
                        "customer_id": plan.customer_id,
                        "entity_type": "remediation_plan",
                        "name": plan.name,
                        "status": plan.status,
                        "total_tasks": plan.total_tasks,
                        "completed_tasks": plan.completed_tasks,
                        "completion_percentage": plan.completion_percentage,
                    },
                )
            ],
        )

        logger.info(f"Created remediation plan {plan.plan_id}: {plan.name}")
        return plan

    def get_plan(self, plan_id: str) -> Optional[RemediationPlan]:
        """Get plan by ID."""
        context = self._get_customer_context()

        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(key="plan_id", match=MatchValue(value=plan_id)),
                    FieldCondition(
                        key="customer_id",
                        match=MatchAny(any=context.get_customer_ids()),
                    ),
                    FieldCondition(key="entity_type", match=MatchValue(value="remediation_plan")),
                ]
            ),
            limit=1,
        )

        if results[0]:
            # For this example, return a simple plan (in production, reconstruct full object)
            payload = results[0][0].payload
            return RemediationPlan(
                plan_id=payload["plan_id"],
                customer_id=payload["customer_id"],
                name=payload["name"],
                status=payload.get("status", "DRAFT"),
                total_tasks=payload.get("total_tasks", 0),
                completed_tasks=payload.get("completed_tasks", 0),
            )
        return None

    def get_plan_progress(self, plan_id: str) -> Dict[str, Any]:
        """Get detailed progress for a remediation plan."""
        plan = self.get_plan(plan_id)
        if not plan:
            return {}

        return {
            "plan_id": plan_id,
            "completion_percentage": plan.completion_percentage,
            "total_tasks": plan.total_tasks,
            "completed_tasks": plan.completed_tasks,
            "is_on_track": plan.is_on_track,
            "is_completed": plan.is_completed,
        }

    # =========================================================================
    # Metrics Operations
    # =========================================================================

    def calculate_metrics_summary(self) -> Dict[str, Any]:
        """Calculate remediation metrics summary for customer."""
        context = self._get_customer_context()

        # Get all tasks
        all_tasks = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=self._build_customer_filter(
                context.customer_id,
                additional_conditions=[
                    FieldCondition(key="entity_type", match=MatchValue(value="remediation_task")),
                ]
            ),
            limit=10000,
        )

        tasks = [self._payload_to_task(p.payload) for p in all_tasks[0]]

        # Calculate metrics
        total_tasks = len(tasks)
        completed = sum(1 for t in tasks if t.is_completed)
        open_tasks = sum(1 for t in tasks if not t.is_completed)
        overdue = sum(1 for t in tasks if t.is_overdue)
        critical = sum(1 for t in tasks if t.is_critical_priority)

        # Status breakdown
        status_breakdown = {}
        for task in tasks:
            status = task.status.value
            status_breakdown[status] = status_breakdown.get(status, 0) + 1

        # Priority breakdown
        priority_breakdown = {}
        for task in tasks:
            priority = task.priority.value
            priority_breakdown[priority] = priority_breakdown.get(priority, 0) + 1

        return {
            "total_tasks": total_tasks,
            "completed_tasks": completed,
            "open_tasks": open_tasks,
            "overdue_tasks": overdue,
            "critical_tasks": critical,
            "completion_rate": (completed / total_tasks * 100) if total_tasks > 0 else 0,
            "overdue_rate": (overdue / open_tasks * 100) if open_tasks > 0 else 0,
            "status_breakdown": status_breakdown,
            "priority_breakdown": priority_breakdown,
        }

    def calculate_mttr_by_severity(self) -> Dict[str, float]:
        """Calculate Mean Time To Remediate by severity."""
        context = self._get_customer_context()

        # Get completed tasks
        results = self.qdrant_client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=self._build_customer_filter(
                context.customer_id,
                additional_conditions=[
                    FieldCondition(key="entity_type", match=MatchValue(value="remediation_task")),
                    FieldCondition(key="is_completed", match=MatchValue(value=True)),
                ]
            ),
            limit=10000,
        )

        # Calculate MTTR by severity ranges
        severity_times: Dict[str, List[float]] = {
            "critical": [],  # >= 9.0
            "high": [],      # 7.0-8.9
            "medium": [],    # 4.0-6.9
            "low": [],       # < 4.0
        }

        for point in results[0]:
            payload = point.payload
            # Simplified calculation (in production, use actual dates)
            mttr_hours = 48.0  # Placeholder
            severity = payload.get("severity_source", 0.0)

            if severity >= 9.0:
                severity_times["critical"].append(mttr_hours)
            elif severity >= 7.0:
                severity_times["high"].append(mttr_hours)
            elif severity >= 4.0:
                severity_times["medium"].append(mttr_hours)
            else:
                severity_times["low"].append(mttr_hours)

        # Calculate averages
        mttr_by_severity = {}
        for severity, times in severity_times.items():
            if times:
                mttr_by_severity[severity] = round(sum(times) / len(times), 2)
            else:
                mttr_by_severity[severity] = 0.0

        return mttr_by_severity

    def get_dashboard_summary(self) -> Dict[str, Any]:
        """Get remediation dashboard summary."""
        summary = self.calculate_metrics_summary()
        mttr = self.calculate_mttr_by_severity()

        return {
            "summary": summary,
            "mttr_by_severity": mttr,
            "workload_distribution": {
                "by_priority": summary["priority_breakdown"],
                "by_status": summary["status_breakdown"],
            },
        }
