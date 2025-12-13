"""
E08 Automated Scanning Service
Business logic for automated security scanning operations
Integrates with Qdrant collection 'ner11_scanning'
"""
import uuid
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from fastapi import HTTPException
from qdrant_client import QdrantClient
from api.database_manager import get_qdrant_client
from qdrant_client.models import PointStruct, Filter, FieldCondition, MatchValue, Range

from .scanning_router import (
    ScanProfileCreate, ScanProfileUpdate, ScanProfileResponse,
    ScheduleCreate, ScheduleUpdate, ScheduleResponse,
    ScanJobCreate, ScanJobResponse, ScanStatus,
    FindingResponse, FindingStatusUpdate, FindingSearchRequest,
    TargetCreate, TargetUpdate, TargetResponse,
    DashboardSummary, ScanType, FindingSeverity, FindingStatus
)


class ScanningService:
    """Service layer for automated scanning operations"""

    COLLECTION_NAME = "ner11_scanning"

    def __init__(self, qdrant_url: str = "http://openspg-qdrant:6333"):
        """Initialize service with Qdrant client"""
        self.client = get_qdrant_client()

    def _generate_id(self) -> str:
        """Generate unique ID"""
        return str(uuid.uuid4())

    def _build_customer_filter(self, customer_id: str) -> Filter:
        """Build Qdrant filter for customer isolation"""
        return Filter(
            must=[
                FieldCondition(
                    key="customer_id",
                    match=MatchValue(value=customer_id)
                )
            ]
        )

    def _build_combined_filter(self, customer_id: str, additional_conditions: List[FieldCondition]) -> Filter:
        """Build combined filter with customer ID and additional conditions"""
        conditions = [
            FieldCondition(key="customer_id", match=MatchValue(value=customer_id))
        ] + additional_conditions
        return Filter(must=conditions)

    # ========================================================================
    # SCAN PROFILES
    # ========================================================================

    async def create_profile(self, customer_id: str, profile: ScanProfileCreate) -> ScanProfileResponse:
        """Create a new scan profile"""
        profile_id = self._generate_id()
        now = datetime.utcnow()

        point = PointStruct(
            id=profile_id,
            vector=[0.0] * 384,  # Placeholder vector
            payload={
                "entity_type": "scan_profile",
                "customer_id": customer_id,
                "profile_id": profile_id,
                "name": profile.name,
                "scan_type": profile.scan_type.value,
                "description": profile.description,
                "configuration": profile.configuration,
                "enabled": profile.enabled,
                "created_at": now.isoformat(),
                "updated_at": now.isoformat()
            }
        )

        self.client.upsert(
            collection_name=self.COLLECTION_NAME,
            points=[point]
        )

        return ScanProfileResponse(
            profile_id=profile_id,
            customer_id=customer_id,
            name=profile.name,
            scan_type=profile.scan_type,
            description=profile.description,
            configuration=profile.configuration,
            enabled=profile.enabled,
            created_at=now,
            updated_at=now
        )

    async def get_profile(self, customer_id: str, profile_id: str) -> ScanProfileResponse:
        """Get scan profile by ID"""
        results = self.client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=self._build_combined_filter(
                customer_id,
                [
                    FieldCondition(key="entity_type", match=MatchValue(value="scan_profile")),
                    FieldCondition(key="profile_id", match=MatchValue(value=profile_id))
                ]
            ),
            limit=1
        )

        if not results[0]:
            raise HTTPException(status_code=404, detail=f"Profile {profile_id} not found")

        payload = results[0][0].payload
        return ScanProfileResponse(
            profile_id=payload["profile_id"],
            customer_id=payload["customer_id"],
            name=payload["name"],
            scan_type=ScanType(payload["scan_type"]),
            description=payload.get("description"),
            configuration=payload["configuration"],
            enabled=payload["enabled"],
            created_at=datetime.fromisoformat(payload["created_at"]),
            updated_at=datetime.fromisoformat(payload["updated_at"])
        )

    async def update_profile(self, customer_id: str, profile_id: str,
                           profile_update: ScanProfileUpdate) -> ScanProfileResponse:
        """Update scan profile"""
        # Get existing profile
        existing = await self.get_profile(customer_id, profile_id)

        # Build updated payload
        now = datetime.utcnow()
        updated_payload = {
            "name": profile_update.name if profile_update.name is not None else existing.name,
            "description": profile_update.description if profile_update.description is not None else existing.description,
            "configuration": profile_update.configuration if profile_update.configuration is not None else existing.configuration,
            "enabled": profile_update.enabled if profile_update.enabled is not None else existing.enabled,
            "updated_at": now.isoformat()
        }

        # Update in Qdrant
        self.client.set_payload(
            collection_name=self.COLLECTION_NAME,
            payload=updated_payload,
            points=[profile_id]
        )

        return await self.get_profile(customer_id, profile_id)

    async def delete_profile(self, customer_id: str, profile_id: str):
        """Delete scan profile"""
        # Verify exists
        await self.get_profile(customer_id, profile_id)

        self.client.delete(
            collection_name=self.COLLECTION_NAME,
            points_selector=[profile_id]
        )

    async def list_profiles(self, customer_id: str, scan_type: Optional[ScanType] = None,
                          enabled: Optional[bool] = None, limit: int = 100,
                          offset: int = 0) -> List[ScanProfileResponse]:
        """List scan profiles with filters"""
        conditions = [
            FieldCondition(key="entity_type", match=MatchValue(value="scan_profile"))
        ]

        if scan_type:
            conditions.append(
                FieldCondition(key="scan_type", match=MatchValue(value=scan_type.value))
            )
        if enabled is not None:
            conditions.append(
                FieldCondition(key="enabled", match=MatchValue(value=enabled))
            )

        results = self.client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=self._build_combined_filter(customer_id, conditions),
            limit=limit,
            offset=offset
        )

        profiles = []
        for point in results[0]:
            payload = point.payload
            profiles.append(ScanProfileResponse(
                profile_id=payload["profile_id"],
                customer_id=payload["customer_id"],
                name=payload["name"],
                scan_type=ScanType(payload["scan_type"]),
                description=payload.get("description"),
                configuration=payload["configuration"],
                enabled=payload["enabled"],
                created_at=datetime.fromisoformat(payload["created_at"]),
                updated_at=datetime.fromisoformat(payload["updated_at"])
            ))

        return profiles

    async def get_profiles_by_type(self, customer_id: str,
                                  scan_type: ScanType) -> List[ScanProfileResponse]:
        """Get all profiles of specific scan type"""
        return await self.list_profiles(customer_id, scan_type=scan_type, limit=1000)

    async def clone_profile(self, customer_id: str, profile_id: str,
                          new_name: str) -> ScanProfileResponse:
        """Clone an existing scan profile"""
        # Get original profile
        original = await self.get_profile(customer_id, profile_id)

        # Create new profile with cloned data
        cloned = ScanProfileCreate(
            name=new_name,
            scan_type=original.scan_type,
            description=f"Cloned from {original.name}",
            configuration=original.configuration.copy(),
            enabled=original.enabled
        )

        return await self.create_profile(customer_id, cloned)

    # ========================================================================
    # SCHEDULES
    # ========================================================================

    async def create_schedule(self, customer_id: str, schedule: ScheduleCreate) -> ScheduleResponse:
        """Create a new scan schedule"""
        schedule_id = self._generate_id()
        now = datetime.utcnow()

        point = PointStruct(
            id=schedule_id,
            vector=[0.0] * 384,
            payload={
                "entity_type": "schedule",
                "customer_id": customer_id,
                "schedule_id": schedule_id,
                "name": schedule.name,
                "profile_id": schedule.profile_id,
                "frequency": schedule.frequency.value,
                "target_ids": schedule.target_ids,
                "cron_expression": schedule.cron_expression,
                "enabled": schedule.enabled,
                "last_run": None,
                "next_run": (now + timedelta(hours=1)).isoformat(),  # Simple default
                "created_at": now.isoformat(),
                "updated_at": now.isoformat()
            }
        )

        self.client.upsert(
            collection_name=self.COLLECTION_NAME,
            points=[point]
        )

        return ScheduleResponse(
            schedule_id=schedule_id,
            customer_id=customer_id,
            name=schedule.name,
            profile_id=schedule.profile_id,
            frequency=schedule.frequency,
            target_ids=schedule.target_ids,
            cron_expression=schedule.cron_expression,
            enabled=schedule.enabled,
            last_run=None,
            next_run=now + timedelta(hours=1),
            created_at=now,
            updated_at=now
        )

    async def get_schedule(self, customer_id: str, schedule_id: str) -> ScheduleResponse:
        """Get schedule by ID"""
        results = self.client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=self._build_combined_filter(
                customer_id,
                [
                    FieldCondition(key="entity_type", match=MatchValue(value="schedule")),
                    FieldCondition(key="schedule_id", match=MatchValue(value=schedule_id))
                ]
            ),
            limit=1
        )

        if not results[0]:
            raise HTTPException(status_code=404, detail=f"Schedule {schedule_id} not found")

        payload = results[0][0].payload
        return ScheduleResponse(
            schedule_id=payload["schedule_id"],
            customer_id=payload["customer_id"],
            name=payload["name"],
            profile_id=payload["profile_id"],
            frequency=payload["frequency"],
            target_ids=payload["target_ids"],
            cron_expression=payload.get("cron_expression"),
            enabled=payload["enabled"],
            last_run=datetime.fromisoformat(payload["last_run"]) if payload.get("last_run") else None,
            next_run=datetime.fromisoformat(payload["next_run"]) if payload.get("next_run") else None,
            created_at=datetime.fromisoformat(payload["created_at"]),
            updated_at=datetime.fromisoformat(payload["updated_at"])
        )

    async def update_schedule(self, customer_id: str, schedule_id: str,
                            schedule_update: ScheduleUpdate) -> ScheduleResponse:
        """Update scan schedule"""
        existing = await self.get_schedule(customer_id, schedule_id)

        now = datetime.utcnow()
        updated_payload = {
            "name": schedule_update.name if schedule_update.name is not None else existing.name,
            "frequency": schedule_update.frequency.value if schedule_update.frequency else existing.frequency.value,
            "target_ids": schedule_update.target_ids if schedule_update.target_ids is not None else existing.target_ids,
            "cron_expression": schedule_update.cron_expression if schedule_update.cron_expression is not None else existing.cron_expression,
            "enabled": schedule_update.enabled if schedule_update.enabled is not None else existing.enabled,
            "updated_at": now.isoformat()
        }

        self.client.set_payload(
            collection_name=self.COLLECTION_NAME,
            payload=updated_payload,
            points=[schedule_id]
        )

        return await self.get_schedule(customer_id, schedule_id)

    async def delete_schedule(self, customer_id: str, schedule_id: str):
        """Delete scan schedule"""
        await self.get_schedule(customer_id, schedule_id)

        self.client.delete(
            collection_name=self.COLLECTION_NAME,
            points_selector=[schedule_id]
        )

    async def list_schedules(self, customer_id: str, enabled: Optional[bool] = None,
                           limit: int = 100, offset: int = 0) -> List[ScheduleResponse]:
        """List scan schedules"""
        conditions = [
            FieldCondition(key="entity_type", match=MatchValue(value="schedule"))
        ]

        if enabled is not None:
            conditions.append(
                FieldCondition(key="enabled", match=MatchValue(value=enabled))
            )

        results = self.client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=self._build_combined_filter(customer_id, conditions),
            limit=limit,
            offset=offset
        )

        schedules = []
        for point in results[0]:
            payload = point.payload
            schedules.append(ScheduleResponse(
                schedule_id=payload["schedule_id"],
                customer_id=payload["customer_id"],
                name=payload["name"],
                profile_id=payload["profile_id"],
                frequency=payload["frequency"],
                target_ids=payload["target_ids"],
                cron_expression=payload.get("cron_expression"),
                enabled=payload["enabled"],
                last_run=datetime.fromisoformat(payload["last_run"]) if payload.get("last_run") else None,
                next_run=datetime.fromisoformat(payload["next_run"]) if payload.get("next_run") else None,
                created_at=datetime.fromisoformat(payload["created_at"]),
                updated_at=datetime.fromisoformat(payload["updated_at"])
            ))

        return schedules

    async def toggle_schedule(self, customer_id: str, schedule_id: str,
                            enabled: bool) -> ScheduleResponse:
        """Enable or disable schedule"""
        await self.get_schedule(customer_id, schedule_id)

        self.client.set_payload(
            collection_name=self.COLLECTION_NAME,
            payload={
                "enabled": enabled,
                "updated_at": datetime.utcnow().isoformat()
            },
            points=[schedule_id]
        )

        return await self.get_schedule(customer_id, schedule_id)

    # ========================================================================
    # SCAN JOBS
    # ========================================================================

    async def start_job(self, customer_id: str, job: ScanJobCreate) -> ScanJobResponse:
        """Start a new scan job"""
        job_id = self._generate_id()
        now = datetime.utcnow()

        point = PointStruct(
            id=job_id,
            vector=[0.0] * 384,
            payload={
                "entity_type": "scan_job",
                "customer_id": customer_id,
                "job_id": job_id,
                "profile_id": job.profile_id,
                "target_ids": job.target_ids,
                "status": ScanStatus.PENDING.value,
                "priority": job.priority,
                "scheduled": job.scheduled,
                "progress": 0.0,
                "started_at": None,
                "completed_at": None,
                "findings_count": 0,
                "error_message": None,
                "created_at": now.isoformat(),
                "updated_at": now.isoformat()
            }
        )

        self.client.upsert(
            collection_name=self.COLLECTION_NAME,
            points=[point]
        )

        return ScanJobResponse(
            job_id=job_id,
            customer_id=customer_id,
            profile_id=job.profile_id,
            target_ids=job.target_ids,
            status=ScanStatus.PENDING,
            priority=job.priority,
            scheduled=job.scheduled,
            progress=0.0,
            started_at=None,
            completed_at=None,
            findings_count=0,
            error_message=None,
            created_at=now,
            updated_at=now
        )

    async def get_job(self, customer_id: str, job_id: str) -> ScanJobResponse:
        """Get scan job by ID"""
        results = self.client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=self._build_combined_filter(
                customer_id,
                [
                    FieldCondition(key="entity_type", match=MatchValue(value="scan_job")),
                    FieldCondition(key="job_id", match=MatchValue(value=job_id))
                ]
            ),
            limit=1
        )

        if not results[0]:
            raise HTTPException(status_code=404, detail=f"Job {job_id} not found")

        payload = results[0][0].payload
        return ScanJobResponse(
            job_id=payload["job_id"],
            customer_id=payload["customer_id"],
            profile_id=payload["profile_id"],
            target_ids=payload["target_ids"],
            status=ScanStatus(payload["status"]),
            priority=payload["priority"],
            scheduled=payload["scheduled"],
            progress=payload["progress"],
            started_at=datetime.fromisoformat(payload["started_at"]) if payload.get("started_at") else None,
            completed_at=datetime.fromisoformat(payload["completed_at"]) if payload.get("completed_at") else None,
            findings_count=payload["findings_count"],
            error_message=payload.get("error_message"),
            created_at=datetime.fromisoformat(payload["created_at"]),
            updated_at=datetime.fromisoformat(payload["updated_at"])
        )

    async def list_jobs(self, customer_id: str, status: Optional[ScanStatus] = None,
                       profile_id: Optional[str] = None, limit: int = 100,
                       offset: int = 0) -> List[ScanJobResponse]:
        """List scan jobs with filters"""
        conditions = [
            FieldCondition(key="entity_type", match=MatchValue(value="scan_job"))
        ]

        if status:
            conditions.append(
                FieldCondition(key="status", match=MatchValue(value=status.value))
            )
        if profile_id:
            conditions.append(
                FieldCondition(key="profile_id", match=MatchValue(value=profile_id))
            )

        results = self.client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=self._build_combined_filter(customer_id, conditions),
            limit=limit,
            offset=offset
        )

        jobs = []
        for point in results[0]:
            payload = point.payload
            jobs.append(ScanJobResponse(
                job_id=payload["job_id"],
                customer_id=payload["customer_id"],
                profile_id=payload["profile_id"],
                target_ids=payload["target_ids"],
                status=ScanStatus(payload["status"]),
                priority=payload["priority"],
                scheduled=payload["scheduled"],
                progress=payload["progress"],
                started_at=datetime.fromisoformat(payload["started_at"]) if payload.get("started_at") else None,
                completed_at=datetime.fromisoformat(payload["completed_at"]) if payload.get("completed_at") else None,
                findings_count=payload["findings_count"],
                error_message=payload.get("error_message"),
                created_at=datetime.fromisoformat(payload["created_at"]),
                updated_at=datetime.fromisoformat(payload["updated_at"])
            ))

        return jobs

    async def cancel_job(self, customer_id: str, job_id: str) -> ScanJobResponse:
        """Cancel a running scan job"""
        job = await self.get_job(customer_id, job_id)

        if job.status not in [ScanStatus.PENDING, ScanStatus.RUNNING]:
            raise HTTPException(
                status_code=400,
                detail=f"Cannot cancel job with status {job.status.value}"
            )

        self.client.set_payload(
            collection_name=self.COLLECTION_NAME,
            payload={
                "status": ScanStatus.CANCELLED.value,
                "completed_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            },
            points=[job_id]
        )

        return await self.get_job(customer_id, job_id)

    async def get_job_findings(self, customer_id: str, job_id: str) -> List[FindingResponse]:
        """Get all findings for a specific job"""
        results = self.client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=self._build_combined_filter(
                customer_id,
                [
                    FieldCondition(key="entity_type", match=MatchValue(value="finding")),
                    FieldCondition(key="job_id", match=MatchValue(value=job_id))
                ]
            ),
            limit=1000
        )

        findings = []
        for point in results[0]:
            payload = point.payload
            findings.append(FindingResponse(
                finding_id=payload["finding_id"],
                customer_id=payload["customer_id"],
                job_id=payload["job_id"],
                target_id=payload["target_id"],
                severity=FindingSeverity(payload["severity"]),
                status=FindingStatus(payload["status"]),
                title=payload["title"],
                description=payload["description"],
                affected_resource=payload["affected_resource"],
                recommendation=payload["recommendation"],
                cve_ids=payload.get("cve_ids", []),
                references=payload.get("references", []),
                first_detected=datetime.fromisoformat(payload["first_detected"]),
                last_detected=datetime.fromisoformat(payload["last_detected"]),
                created_at=datetime.fromisoformat(payload["created_at"]),
                updated_at=datetime.fromisoformat(payload["updated_at"])
            ))

        return findings

    async def list_running_jobs(self, customer_id: str) -> List[ScanJobResponse]:
        """List all currently running scan jobs"""
        return await self.list_jobs(customer_id, status=ScanStatus.RUNNING, limit=1000)

    # ========================================================================
    # FINDINGS
    # ========================================================================

    async def list_findings(self, customer_id: str,
                          severity: Optional[List[FindingSeverity]] = None,
                          status: Optional[List[FindingStatus]] = None,
                          limit: int = 100, offset: int = 0) -> List[FindingResponse]:
        """List all findings with filters"""
        conditions = [
            FieldCondition(key="entity_type", match=MatchValue(value="finding"))
        ]

        # Note: Qdrant doesn't have built-in "IN" operator for lists
        # This is a simplified implementation

        results = self.client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=self._build_combined_filter(customer_id, conditions),
            limit=limit,
            offset=offset
        )

        findings = []
        for point in results[0]:
            payload = point.payload

            # Apply filters in code
            if severity and FindingSeverity(payload["severity"]) not in severity:
                continue
            if status and FindingStatus(payload["status"]) not in status:
                continue

            findings.append(FindingResponse(
                finding_id=payload["finding_id"],
                customer_id=payload["customer_id"],
                job_id=payload["job_id"],
                target_id=payload["target_id"],
                severity=FindingSeverity(payload["severity"]),
                status=FindingStatus(payload["status"]),
                title=payload["title"],
                description=payload["description"],
                affected_resource=payload["affected_resource"],
                recommendation=payload["recommendation"],
                cve_ids=payload.get("cve_ids", []),
                references=payload.get("references", []),
                first_detected=datetime.fromisoformat(payload["first_detected"]),
                last_detected=datetime.fromisoformat(payload["last_detected"]),
                created_at=datetime.fromisoformat(payload["created_at"]),
                updated_at=datetime.fromisoformat(payload["updated_at"])
            ))

        return findings

    async def get_finding(self, customer_id: str, finding_id: str) -> FindingResponse:
        """Get finding by ID"""
        results = self.client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=self._build_combined_filter(
                customer_id,
                [
                    FieldCondition(key="entity_type", match=MatchValue(value="finding")),
                    FieldCondition(key="finding_id", match=MatchValue(value=finding_id))
                ]
            ),
            limit=1
        )

        if not results[0]:
            raise HTTPException(status_code=404, detail=f"Finding {finding_id} not found")

        payload = results[0][0].payload
        return FindingResponse(
            finding_id=payload["finding_id"],
            customer_id=payload["customer_id"],
            job_id=payload["job_id"],
            target_id=payload["target_id"],
            severity=FindingSeverity(payload["severity"]),
            status=FindingStatus(payload["status"]),
            title=payload["title"],
            description=payload["description"],
            affected_resource=payload["affected_resource"],
            recommendation=payload["recommendation"],
            cve_ids=payload.get("cve_ids", []),
            references=payload.get("references", []),
            first_detected=datetime.fromisoformat(payload["first_detected"]),
            last_detected=datetime.fromisoformat(payload["last_detected"]),
            created_at=datetime.fromisoformat(payload["created_at"]),
            updated_at=datetime.fromisoformat(payload["updated_at"])
        )

    async def update_finding_status(self, customer_id: str, finding_id: str,
                                   status_update: FindingStatusUpdate) -> FindingResponse:
        """Update finding status"""
        await self.get_finding(customer_id, finding_id)

        now = datetime.utcnow()
        self.client.set_payload(
            collection_name=self.COLLECTION_NAME,
            payload={
                "status": status_update.status.value,
                "status_notes": status_update.notes,
                "updated_at": now.isoformat()
            },
            points=[finding_id]
        )

        return await self.get_finding(customer_id, finding_id)

    async def get_findings_by_severity(self, customer_id: str,
                                      severity: FindingSeverity,
                                      limit: int = 100) -> List[FindingResponse]:
        """Get findings by severity level"""
        return await self.list_findings(customer_id, severity=[severity], limit=limit)

    async def search_findings(self, customer_id: str,
                            search_request: FindingSearchRequest) -> List[FindingResponse]:
        """Search findings with advanced filters"""
        # This is a simplified implementation
        # In production, you would use Qdrant's vector search capabilities

        conditions = [
            FieldCondition(key="entity_type", match=MatchValue(value="finding"))
        ]

        results = self.client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=self._build_combined_filter(customer_id, conditions),
            limit=search_request.limit
        )

        findings = []
        for point in results[0]:
            payload = point.payload

            # Apply search filters
            if search_request.query and search_request.query.lower() not in payload["title"].lower() and search_request.query.lower() not in payload["description"].lower():
                continue

            if search_request.severity and FindingSeverity(payload["severity"]) not in search_request.severity:
                continue

            if search_request.status and FindingStatus(payload["status"]) not in search_request.status:
                continue

            if search_request.target_ids and payload["target_id"] not in search_request.target_ids:
                continue

            findings.append(FindingResponse(
                finding_id=payload["finding_id"],
                customer_id=payload["customer_id"],
                job_id=payload["job_id"],
                target_id=payload["target_id"],
                severity=FindingSeverity(payload["severity"]),
                status=FindingStatus(payload["status"]),
                title=payload["title"],
                description=payload["description"],
                affected_resource=payload["affected_resource"],
                recommendation=payload["recommendation"],
                cve_ids=payload.get("cve_ids", []),
                references=payload.get("references", []),
                first_detected=datetime.fromisoformat(payload["first_detected"]),
                last_detected=datetime.fromisoformat(payload["last_detected"]),
                created_at=datetime.fromisoformat(payload["created_at"]),
                updated_at=datetime.fromisoformat(payload["updated_at"])
            ))

        return findings

    # ========================================================================
    # TARGETS
    # ========================================================================

    async def create_target(self, customer_id: str, target: TargetCreate) -> TargetResponse:
        """Create a new scan target"""
        target_id = self._generate_id()
        now = datetime.utcnow()

        point = PointStruct(
            id=target_id,
            vector=[0.0] * 384,
            payload={
                "entity_type": "target",
                "customer_id": customer_id,
                "target_id": target_id,
                "name": target.name,
                "target_type": target.target_type,
                "address": target.address,
                "description": target.description,
                "tags": target.tags,
                "metadata": target.metadata,
                "last_scanned": None,
                "created_at": now.isoformat(),
                "updated_at": now.isoformat()
            }
        )

        self.client.upsert(
            collection_name=self.COLLECTION_NAME,
            points=[point]
        )

        return TargetResponse(
            target_id=target_id,
            customer_id=customer_id,
            name=target.name,
            target_type=target.target_type,
            address=target.address,
            description=target.description,
            tags=target.tags,
            metadata=target.metadata,
            last_scanned=None,
            created_at=now,
            updated_at=now
        )

    async def list_targets(self, customer_id: str, target_type: Optional[str] = None,
                         limit: int = 100, offset: int = 0) -> List[TargetResponse]:
        """List scan targets with filters"""
        conditions = [
            FieldCondition(key="entity_type", match=MatchValue(value="target"))
        ]

        if target_type:
            conditions.append(
                FieldCondition(key="target_type", match=MatchValue(value=target_type))
            )

        results = self.client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=self._build_combined_filter(customer_id, conditions),
            limit=limit,
            offset=offset
        )

        targets = []
        for point in results[0]:
            payload = point.payload
            targets.append(TargetResponse(
                target_id=payload["target_id"],
                customer_id=payload["customer_id"],
                name=payload["name"],
                target_type=payload["target_type"],
                address=payload["address"],
                description=payload.get("description"),
                tags=payload.get("tags", []),
                metadata=payload.get("metadata", {}),
                last_scanned=datetime.fromisoformat(payload["last_scanned"]) if payload.get("last_scanned") else None,
                created_at=datetime.fromisoformat(payload["created_at"]),
                updated_at=datetime.fromisoformat(payload["updated_at"])
            ))

        return targets

    async def update_target(self, customer_id: str, target_id: str,
                          target_update: TargetUpdate) -> TargetResponse:
        """Update scan target"""
        results = self.client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=self._build_combined_filter(
                customer_id,
                [
                    FieldCondition(key="entity_type", match=MatchValue(value="target")),
                    FieldCondition(key="target_id", match=MatchValue(value=target_id))
                ]
            ),
            limit=1
        )

        if not results[0]:
            raise HTTPException(status_code=404, detail=f"Target {target_id} not found")

        existing = results[0][0].payload

        now = datetime.utcnow()
        updated_payload = {
            "name": target_update.name if target_update.name is not None else existing["name"],
            "description": target_update.description if target_update.description is not None else existing.get("description"),
            "tags": target_update.tags if target_update.tags is not None else existing.get("tags", []),
            "metadata": target_update.metadata if target_update.metadata is not None else existing.get("metadata", {}),
            "updated_at": now.isoformat()
        }

        self.client.set_payload(
            collection_name=self.COLLECTION_NAME,
            payload=updated_payload,
            points=[target_id]
        )

        # Fetch and return updated target
        results = self.client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=self._build_combined_filter(
                customer_id,
                [
                    FieldCondition(key="entity_type", match=MatchValue(value="target")),
                    FieldCondition(key="target_id", match=MatchValue(value=target_id))
                ]
            ),
            limit=1
        )

        payload = results[0][0].payload
        return TargetResponse(
            target_id=payload["target_id"],
            customer_id=payload["customer_id"],
            name=payload["name"],
            target_type=payload["target_type"],
            address=payload["address"],
            description=payload.get("description"),
            tags=payload.get("tags", []),
            metadata=payload.get("metadata", {}),
            last_scanned=datetime.fromisoformat(payload["last_scanned"]) if payload.get("last_scanned") else None,
            created_at=datetime.fromisoformat(payload["created_at"]),
            updated_at=datetime.fromisoformat(payload["updated_at"])
        )

    async def delete_target(self, customer_id: str, target_id: str):
        """Delete scan target"""
        results = self.client.scroll(
            collection_name=self.COLLECTION_NAME,
            scroll_filter=self._build_combined_filter(
                customer_id,
                [
                    FieldCondition(key="entity_type", match=MatchValue(value="target")),
                    FieldCondition(key="target_id", match=MatchValue(value=target_id))
                ]
            ),
            limit=1
        )

        if not results[0]:
            raise HTTPException(status_code=404, detail=f"Target {target_id} not found")

        self.client.delete(
            collection_name=self.COLLECTION_NAME,
            points_selector=[target_id]
        )

    # ========================================================================
    # DASHBOARD
    # ========================================================================

    async def get_dashboard_summary(self, customer_id: str) -> DashboardSummary:
        """Get comprehensive scanning dashboard summary"""
        # Get all entity counts
        profiles = await self.list_profiles(customer_id, limit=10000)
        schedules = await self.list_schedules(customer_id, limit=10000)
        jobs = await self.list_jobs(customer_id, limit=10000)
        findings = await self.list_findings(customer_id, limit=10000)

        # Calculate metrics
        now = datetime.utcnow()
        yesterday = now - timedelta(hours=24)

        completed_24h = len([j for j in jobs if j.status == ScanStatus.COMPLETED and j.completed_at and j.completed_at > yesterday])
        failed_24h = len([j for j in jobs if j.status == ScanStatus.FAILED and j.completed_at and j.completed_at > yesterday])

        # Findings by severity
        critical_findings = len([f for f in findings if f.severity == FindingSeverity.CRITICAL])
        high_findings = len([f for f in findings if f.severity == FindingSeverity.HIGH])
        medium_findings = len([f for f in findings if f.severity == FindingSeverity.MEDIUM])
        low_findings = len([f for f in findings if f.severity == FindingSeverity.LOW])

        # Findings by status
        findings_by_status = {
            "new": len([f for f in findings if f.status == FindingStatus.NEW]),
            "acknowledged": len([f for f in findings if f.status == FindingStatus.ACKNOWLEDGED]),
            "in_progress": len([f for f in findings if f.status == FindingStatus.IN_PROGRESS]),
            "resolved": len([f for f in findings if f.status == FindingStatus.RESOLVED]),
            "false_positive": len([f for f in findings if f.status == FindingStatus.FALSE_POSITIVE])
        }

        # Recent jobs (last 10)
        recent_jobs = sorted(jobs, key=lambda j: j.created_at, reverse=True)[:10]

        return DashboardSummary(
            total_profiles=len(profiles),
            active_profiles=len([p for p in profiles if p.enabled]),
            total_schedules=len(schedules),
            active_schedules=len([s for s in schedules if s.enabled]),
            running_jobs=len([j for j in jobs if j.status == ScanStatus.RUNNING]),
            completed_jobs_24h=completed_24h,
            failed_jobs_24h=failed_24h,
            total_findings=len(findings),
            critical_findings=critical_findings,
            high_findings=high_findings,
            medium_findings=medium_findings,
            low_findings=low_findings,
            findings_by_status=findings_by_status,
            recent_jobs=recent_jobs
        )
