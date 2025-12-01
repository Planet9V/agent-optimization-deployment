"""
GAP-ML-011: Batch Prediction API
Fast API server for batch Ising and EWS predictions
Uses APOC batch patterns from cypher library
"""
import os
import uuid
import time
import asyncio
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
from enum import Enum

from fastapi import FastAPI, HTTPException, BackgroundTasks, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
import redis.asyncio as redis
from neo4j import AsyncGraphDatabase
import uvicorn
import logging
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration from environment
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

# Initialize FastAPI
app = FastAPI(
    title="Batch Prediction API - GAP-ML-011",
    description="Batch processing for Ising dynamics and EWS predictions",
    version="1.0.0",
    docs_url="/api/v1/docs"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global connections
_neo4j_driver = None
_redis_client = None


class JobStatus(str, Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class BatchIsingRequest(BaseModel):
    """Request for batch Ising spin prediction"""
    entity_ids: List[str] = Field(..., description="List of entity IDs to predict", min_items=1)
    parameters: Dict[str, float] = Field(
        default={"temperature": 0.5, "beta": 1.5, "coupling": 0.8, "field": 0.2},
        description="Ising model parameters"
    )

    @validator('parameters')
    def validate_parameters(cls, v):
        if 'temperature' in v and (v['temperature'] < 0 or v['temperature'] > 2):
            raise ValueError('temperature must be between 0 and 2')
        if 'beta' in v and (v['beta'] < 0 or v['beta'] > 5):
            raise ValueError('beta must be between 0 and 5')
        return v


class BatchEWSRequest(BaseModel):
    """Request for batch Early Warning Signals"""
    entity_ids: List[str] = Field(..., description="List of entity IDs to analyze", min_items=1)
    metrics: List[str] = Field(
        default=["variance", "autocorrelation"],
        description="EWS metrics to calculate"
    )
    window_size: int = Field(default=30, description="Time window for EWS calculation")


class JobResponse(BaseModel):
    """Response with job ID"""
    job_id: str
    status: JobStatus
    created_at: datetime
    estimated_completion: Optional[datetime] = None
    message: str


class JobStatusResponse(BaseModel):
    """Detailed job status"""
    job_id: str
    status: JobStatus
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    total_entities: int
    processed_entities: int
    failed_entities: int
    progress_percent: float
    error_message: Optional[str] = None


class JobResultsResponse(BaseModel):
    """Job results"""
    job_id: str
    status: JobStatus
    results: List[Dict[str, Any]]
    total_entities: int
    successful: int
    failed: int
    execution_time_seconds: float


async def get_neo4j_driver():
    """Get Neo4j driver (singleton)"""
    global _neo4j_driver
    if _neo4j_driver is None:
        _neo4j_driver = AsyncGraphDatabase.driver(
            NEO4J_URI,
            auth=(NEO4J_USER, NEO4J_PASSWORD)
        )
    return _neo4j_driver


async def get_redis_client():
    """Get Redis client (singleton)"""
    global _redis_client
    if _redis_client is None:
        _redis_client = await redis.from_url(REDIS_URL, decode_responses=True)
    return _redis_client


@app.on_event("startup")
async def startup_event():
    """Initialize connections on startup"""
    logger.info("Initializing connections...")
    await get_neo4j_driver()
    await get_redis_client()
    logger.info("Connections initialized")


@app.on_event("shutdown")
async def shutdown_event():
    """Close connections on shutdown"""
    global _neo4j_driver, _redis_client
    if _neo4j_driver:
        await _neo4j_driver.close()
    if _redis_client:
        await _redis_client.close()


async def execute_batch_ising_query(entity_ids: List[str], parameters: Dict[str, float]) -> List[Dict]:
    """
    Execute Ising prediction using APOC batch pattern
    Uses apoc.periodic.iterate from cypher library line 590
    """
    driver = await get_neo4j_driver()

    beta = parameters.get('beta', 1.5)
    coupling = parameters.get('coupling', 0.8)
    field = parameters.get('field', 0.2)

    # APOC batch pattern - matches library line 590+
    query = """
    CALL apoc.periodic.iterate(
        // Inner query: get entities to process
        'UNWIND $entity_ids AS entity_id
         MATCH (n)
         WHERE elementId(n) = entity_id OR n.id = entity_id
         RETURN n, entity_id',

        // Outer query: calculate Ising spin flip probability
        'WITH n, entity_id,
              size([(n)-[]-() | 1]) AS degree,
              coalesce(n.opinion_state, 0.0) AS current_state
         WITH n, entity_id, degree, current_state,
              // Ising dynamics: dm/dt = -m + tanh(β(Jzm + h))
              -current_state + tanh($beta * ($coupling * degree * current_state + $field)) AS dm_dt,
              // Spin flip probability from Ising model
              1.0 / (1.0 + exp(-2.0 * $beta * ($coupling * degree * current_state + $field))) AS spin_flip_prob
         SET n.ising_prediction = spin_flip_prob,
             n.predicted_state = current_state + (dm_dt * 0.1)
         RETURN entity_id,
                current_state,
                n.predicted_state AS predicted_state,
                spin_flip_prob,
                degree,
                dm_dt',

        // Batch configuration
        {batchSize: 100, params: {entity_ids: $entity_ids, beta: $beta, coupling: $coupling, field: $field}}
    )
    YIELD batches, total, errorMessages
    RETURN batches, total, errorMessages
    """

    async with driver.session() as session:
        result = await session.run(query, {
            'entity_ids': entity_ids,
            'beta': beta,
            'coupling': coupling,
            'field': field
        })

        batch_result = await result.single()

        # Get actual results
        results_query = """
        MATCH (n)
        WHERE elementId(n) IN $entity_ids OR n.id IN $entity_ids
        RETURN elementId(n) AS entity_id,
               coalesce(n.ising_prediction, 0.0) AS spin_flip_probability,
               coalesce(n.predicted_state, 0.0) AS predicted_state,
               size([(n)-[]-() | 1]) AS degree
        """

        results = await session.run(results_query, {'entity_ids': entity_ids})
        records = [record.data() async for record in results]

        return records


async def execute_batch_ews_query(entity_ids: List[str], metrics: List[str], window_size: int) -> List[Dict]:
    """
    Execute EWS calculation using APOC batch pattern
    """
    driver = await get_neo4j_driver()

    # APOC batch pattern for EWS calculation
    query = """
    CALL apoc.periodic.iterate(
        // Inner query: get entities
        'UNWIND $entity_ids AS entity_id
         MATCH (n)
         WHERE elementId(n) = entity_id OR n.id = entity_id
         RETURN n, entity_id',

        // Outer query: calculate EWS metrics
        'WITH n, entity_id
         MATCH (n)-[r]-()
         WITH n, entity_id,
              collect(coalesce(r.weight, 1.0)) AS connection_weights,
              count(r) AS degree
         WITH n, entity_id, degree,
              // Variance (EWS metric 1)
              CASE WHEN size(connection_weights) > 1
                   THEN reduce(s = 0.0, w IN connection_weights | s + (w - reduce(sum = 0.0, x IN connection_weights | sum + x) / size(connection_weights))^2) / size(connection_weights)
                   ELSE 0.0 END AS variance,
              // Mean connection strength
              reduce(sum = 0.0, w IN connection_weights | sum + w) / CASE WHEN size(connection_weights) > 0 THEN size(connection_weights) ELSE 1 END AS mean_strength
         WITH n, entity_id, degree, variance, mean_strength,
              // Autocorrelation approximation
              CASE WHEN variance > 0 THEN 0.8 + (variance * 0.2) ELSE 0.5 END AS autocorrelation,
              // Critical slowing indicator
              CASE WHEN variance > 0.5 THEN 1.0 - (1.0 / (1.0 + exp(5 * (variance - 0.5)))) ELSE 0.0 END AS critical_slowing
         SET n.ews_variance = variance,
             n.ews_autocorrelation = autocorrelation,
             n.ews_critical_slowing = critical_slowing
         RETURN entity_id, degree, variance, autocorrelation, critical_slowing',

        // Batch configuration
        {batchSize: 100, params: {entity_ids: $entity_ids}}
    )
    YIELD batches, total, errorMessages
    RETURN batches, total, errorMessages
    """

    async with driver.session() as session:
        result = await session.run(query, {'entity_ids': entity_ids})
        batch_result = await result.single()

        # Get actual results
        results_query = """
        MATCH (n)
        WHERE elementId(n) IN $entity_ids OR n.id IN $entity_ids
        RETURN elementId(n) AS entity_id,
               coalesce(n.ews_variance, 0.0) AS variance,
               coalesce(n.ews_autocorrelation, 0.0) AS autocorrelation,
               coalesce(n.ews_critical_slowing, 0.0) AS critical_slowing,
               CASE
                   WHEN n.ews_critical_slowing > 0.7 THEN 'HIGH_RISK'
                   WHEN n.ews_critical_slowing > 0.4 THEN 'MODERATE_RISK'
                   ELSE 'LOW_RISK'
               END AS risk_level
        """

        results = await session.run(results_query, {'entity_ids': entity_ids})
        records = [record.data() async for record in results]

        return records


async def process_batch_ising_job(job_id: str, entity_ids: List[str], parameters: Dict[str, float]):
    """Background task to process batch Ising predictions"""
    redis_client = await get_redis_client()

    try:
        # Update job status
        await redis_client.hset(f"job:{job_id}", mapping={
            "status": JobStatus.PROCESSING.value,
            "started_at": datetime.utcnow().isoformat()
        })

        start_time = time.time()

        # Execute batch query
        results = await execute_batch_ising_query(entity_ids, parameters)

        execution_time = time.time() - start_time

        # Store results
        await redis_client.hset(f"job:{job_id}", mapping={
            "status": JobStatus.COMPLETED.value,
            "completed_at": datetime.utcnow().isoformat(),
            "processed_entities": len(results),
            "failed_entities": 0,
            "execution_time": execution_time
        })

        # Store results data (expires in 1 hour)
        await redis_client.setex(
            f"job:{job_id}:results",
            3600,
            json.dumps(results)
        )

        logger.info(f"Job {job_id} completed successfully in {execution_time:.2f}s")

    except Exception as e:
        logger.error(f"Job {job_id} failed: {str(e)}")
        await redis_client.hset(f"job:{job_id}", mapping={
            "status": JobStatus.FAILED.value,
            "completed_at": datetime.utcnow().isoformat(),
            "error_message": str(e)
        })


async def process_batch_ews_job(job_id: str, entity_ids: List[str], metrics: List[str], window_size: int):
    """Background task to process batch EWS calculations"""
    redis_client = await get_redis_client()

    try:
        # Update job status
        await redis_client.hset(f"job:{job_id}", mapping={
            "status": JobStatus.PROCESSING.value,
            "started_at": datetime.utcnow().isoformat()
        })

        start_time = time.time()

        # Execute batch query
        results = await execute_batch_ews_query(entity_ids, metrics, window_size)

        execution_time = time.time() - start_time

        # Store results
        await redis_client.hset(f"job:{job_id}", mapping={
            "status": JobStatus.COMPLETED.value,
            "completed_at": datetime.utcnow().isoformat(),
            "processed_entities": len(results),
            "failed_entities": 0,
            "execution_time": execution_time
        })

        # Store results data (expires in 1 hour)
        await redis_client.setex(
            f"job:{job_id}:results",
            3600,
            json.dumps(results)
        )

        logger.info(f"Job {job_id} completed successfully in {execution_time:.2f}s")

    except Exception as e:
        logger.error(f"Job {job_id} failed: {str(e)}")
        await redis_client.hset(f"job:{job_id}", mapping={
            "status": JobStatus.FAILED.value,
            "completed_at": datetime.utcnow().isoformat(),
            "error_message": str(e)
        })


@app.post("/api/v1/predict/batch/ising", response_model=JobResponse, status_code=status.HTTP_202_ACCEPTED)
async def batch_predict_ising(request: BatchIsingRequest, background_tasks: BackgroundTasks):
    """
    Submit batch Ising spin prediction job

    Uses APOC batch processing pattern from cypher library (line 590+)
    Returns job ID for status tracking
    """
    redis_client = await get_redis_client()

    job_id = str(uuid.uuid4())
    created_at = datetime.utcnow()

    # Estimate completion time (rough estimate: 100 entities per second)
    estimated_seconds = len(request.entity_ids) / 100
    estimated_completion = created_at + timedelta(seconds=estimated_seconds)

    # Store job metadata
    await redis_client.hset(f"job:{job_id}", mapping={
        "job_id": job_id,
        "type": "ising",
        "status": JobStatus.QUEUED.value,
        "created_at": created_at.isoformat(),
        "total_entities": len(request.entity_ids),
        "processed_entities": 0,
        "failed_entities": 0
    })

    # Queue background task
    background_tasks.add_task(
        process_batch_ising_job,
        job_id,
        request.entity_ids,
        request.parameters
    )

    return JobResponse(
        job_id=job_id,
        status=JobStatus.QUEUED,
        created_at=created_at,
        estimated_completion=estimated_completion,
        message=f"Batch Ising prediction job queued for {len(request.entity_ids)} entities"
    )


@app.post("/api/v1/predict/batch/ews", response_model=JobResponse, status_code=status.HTTP_202_ACCEPTED)
async def batch_predict_ews(request: BatchEWSRequest, background_tasks: BackgroundTasks):
    """
    Submit batch Early Warning Signals calculation job

    Uses APOC batch processing pattern
    Returns job ID for status tracking
    """
    redis_client = await get_redis_client()

    job_id = str(uuid.uuid4())
    created_at = datetime.utcnow()

    # Estimate completion time
    estimated_seconds = len(request.entity_ids) / 100
    estimated_completion = created_at + timedelta(seconds=estimated_seconds)

    # Store job metadata
    await redis_client.hset(f"job:{job_id}", mapping={
        "job_id": job_id,
        "type": "ews",
        "status": JobStatus.QUEUED.value,
        "created_at": created_at.isoformat(),
        "total_entities": len(request.entity_ids),
        "processed_entities": 0,
        "failed_entities": 0
    })

    # Queue background task
    background_tasks.add_task(
        process_batch_ews_job,
        job_id,
        request.entity_ids,
        request.metrics,
        request.window_size
    )

    return JobResponse(
        job_id=job_id,
        status=JobStatus.QUEUED,
        created_at=created_at,
        estimated_completion=estimated_completion,
        message=f"Batch EWS calculation job queued for {len(request.entity_ids)} entities"
    )


@app.get("/api/v1/jobs/{job_id}", response_model=JobStatusResponse)
async def get_job_status(job_id: str):
    """
    Get detailed status of a batch job
    """
    redis_client = await get_redis_client()

    job_data = await redis_client.hgetall(f"job:{job_id}")

    if not job_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job {job_id} not found"
        )

    total_entities = int(job_data.get('total_entities', 0))
    processed_entities = int(job_data.get('processed_entities', 0))
    progress_percent = (processed_entities / total_entities * 100) if total_entities > 0 else 0

    return JobStatusResponse(
        job_id=job_id,
        status=JobStatus(job_data['status']),
        created_at=datetime.fromisoformat(job_data['created_at']),
        started_at=datetime.fromisoformat(job_data['started_at']) if job_data.get('started_at') else None,
        completed_at=datetime.fromisoformat(job_data['completed_at']) if job_data.get('completed_at') else None,
        total_entities=total_entities,
        processed_entities=processed_entities,
        failed_entities=int(job_data.get('failed_entities', 0)),
        progress_percent=progress_percent,
        error_message=job_data.get('error_message')
    )


@app.get("/api/v1/jobs/{job_id}/results", response_model=JobResultsResponse)
async def get_job_results(job_id: str):
    """
    Get results from completed batch job
    """
    redis_client = await get_redis_client()

    # Check job status
    job_data = await redis_client.hgetall(f"job:{job_id}")

    if not job_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job {job_id} not found"
        )

    if job_data['status'] != JobStatus.COMPLETED.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Job {job_id} is not completed (status: {job_data['status']})"
        )

    # Get results
    results_json = await redis_client.get(f"job:{job_id}:results")

    if not results_json:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Results for job {job_id} not found or expired"
        )

    results = json.loads(results_json)

    return JobResultsResponse(
        job_id=job_id,
        status=JobStatus.COMPLETED,
        results=results,
        total_entities=int(job_data['total_entities']),
        successful=int(job_data['processed_entities']),
        failed=int(job_data.get('failed_entities', 0)),
        execution_time_seconds=float(job_data.get('execution_time', 0))
    )


@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }


if __name__ == "__main__":
    uvicorn.run(
        "batch_prediction_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
