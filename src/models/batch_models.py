"""
Data models for batch prediction
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum


class JobStatus(Enum):
    """Job status enumeration"""
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Priority(Enum):
    """Job priority levels"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"


@dataclass
class PredictionRequest:
    """Request for batch prediction"""
    entities: List[Dict[str, Any]]
    model_id: str
    prediction_type: str
    priority: str = "normal"


@dataclass
class BatchJob:
    """Batch prediction job"""
    job_id: str
    status: JobStatus
    prediction_type: str
    entity_count: int
    priority: Priority
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    failed_at: Optional[datetime] = None
    cancelled_at: Optional[datetime] = None
    error: Optional[str] = None
    result_count: Optional[int] = None


@dataclass
class PredictionResult:
    """Individual prediction result"""
    entity_id: str
    prediction: str
    confidence: float
    timestamp: datetime
    metadata: Optional[Dict[str, Any]] = None
