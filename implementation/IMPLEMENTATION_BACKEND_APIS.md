# WAVE 4 Implementation: Backend APIs Architecture

**Document**: IMPLEMENTATION_BACKEND_APIS.md
**Created**: 2025-11-25 22:30:00 UTC
**Version**: v1.0.0
**Status**: ACTIVE

## Executive Summary

This document defines the FastAPI backend architecture for WAVE 4, implementing enterprise-grade REST and GraphQL APIs with comprehensive data integration, security, and scalability. The backend orchestrates data from 4 specialized databases and provides unified access to the integrated knowledge graph, threat intelligence, and operational systems.

**Target**: 1,000 lines of detailed API specifications, patterns, and implementations.

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Core API Structure](#core-api-structure)
3. [Authentication & Authorization](#authentication--authorization)
4. [Endpoint Specifications](#endpoint-specifications)
5. [Database Integration](#database-integration)
6. [Error Handling & Validation](#error-handling--validation)
7. [Performance Optimization](#performance-optimization)
8. [API Documentation](#api-documentation)
9. [Deployment Architecture](#deployment-architecture)

---

## Architecture Overview

### System Components

The FastAPI backend implements a microservices-oriented architecture with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────┐
│                     API Gateway (Traefik)                   │
│              Route Management & Load Balancing               │
└──────────┬──────────────────────────────────────────────────┘
           │
    ┌──────┴──────────────────────────────────────────┐
    │                                                   │
┌───┴────────────────────┐            ┌───────────────┴──────┐
│  REST API Service      │            │ GraphQL Service      │
│  (FastAPI)             │            │ (Strawberry)         │
└───┬────────────────────┘            └───────────┬──────────┘
    │                                             │
    └─────────────────┬──────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
┌───────┴────────┐ ┌──┴──────────┐ │
│ Neo4j Service  │ │ Auth Module │ │
│ (Knowledge     │ │ (JWT/OAuth) │ │
│  Graph)        │ └──────┬──────┘ │
└────────────────┘        │        │
                 ┌────────┼────────┴────────────┐
                 │        │                     │
          ┌──────┴─────┐ ┌┴──────────────┐ ┌───┴──────────┐
          │ PostgreSQL │ │ MongoDB       │ │ Redis Cache  │
          │ (Threat    │ │ (Operational) │ └──────────────┘
          │ Intel)     │ └───────────────┘
          └────────────┘
```

### Technology Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| Framework | FastAPI | 0.104+ | REST API framework |
| GraphQL | Strawberry | 0.223+ | GraphQL implementation |
| Validation | Pydantic | 2.0+ | Data validation |
| ORM | SQLAlchemy | 2.0+ | Database abstraction |
| Auth | Python-jose | 3.3+ | JWT handling |
| Async | asyncio/aiohttp | 3.9+ | Async operations |
| Caching | Redis | 7.0+ | Response caching |
| Testing | Pytest | 7.4+ | Testing framework |
| Documentation | Swagger/OpenAPI | 3.0.0 | API documentation |

---

## Core API Structure

### Project Layout

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                      # FastAPI application entry point
│   ├── config.py                    # Configuration management
│   ├── security.py                  # Security utilities
│   ├── middleware.py                # Custom middleware
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py                  # Dependency injection
│   │   ├── v1/                      # API v1 endpoints
│   │   │   ├── __init__.py
│   │   │   ├── knowledge_graph.py   # Knowledge graph endpoints
│   │   │   ├── threat_intel.py      # Threat intelligence endpoints
│   │   │   ├── infrastructure.py    # Infrastructure endpoints
│   │   │   ├── analytics.py         # Analytics endpoints
│   │   │   ├── users.py             # User management
│   │   │   └── admin.py             # Admin endpoints
│   │   └── v2/                      # API v2 (future)
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── domain.py                # Domain model definitions
│   │   ├── request.py               # Request models (Pydantic)
│   │   ├── response.py              # Response models (Pydantic)
│   │   └── database.py              # Database models (SQLAlchemy)
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── knowledge_graph.py       # Knowledge graph schemas
│   │   ├── threat_actor.py          # Threat actor schemas
│   │   ├── infrastructure.py        # Infrastructure schemas
│   │   └── common.py                # Common schemas
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── neo4j_service.py         # Neo4j integration
│   │   ├── postgres_service.py      # PostgreSQL integration
│   │   ├── mongodb_service.py       # MongoDB integration
│   │   ├── redis_cache.py           # Redis caching layer
│   │   ├── auth_service.py          # Authentication service
│   │   ├── threat_intel_service.py  # Threat intelligence
│   │   └── analytics_service.py     # Analytics calculations
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── neo4j.py                 # Neo4j connection pool
│   │   ├── postgres.py              # PostgreSQL session factory
│   │   ├── mongodb.py               # MongoDB client setup
│   │   └── redis.py                 # Redis connection
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── settings.py              # Settings/configuration
│   │   ├── logging.py               # Logging setup
│   │   └── constants.py             # Application constants
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── validators.py            # Custom validators
│   │   ├── converters.py            # Data converters
│   │   ├── pagination.py            # Pagination utilities
│   │   └── decorators.py            # Custom decorators
│   │
│   └── exceptions/
│       ├── __init__.py
│       ├── handlers.py              # Exception handlers
│       └── custom.py                # Custom exceptions
│
├── graphql/
│   ├── __init__.py
│   ├── schema.py                    # GraphQL schema definition
│   ├── queries.py                   # Query resolvers
│   ├── mutations.py                 # Mutation resolvers
│   └── types.py                     # GraphQL types
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py                  # Pytest configuration
│   ├── unit/                        # Unit tests
│   │   ├── test_models.py
│   │   ├── test_services.py
│   │   └── test_validators.py
│   ├── integration/                 # Integration tests
│   │   ├── test_api_endpoints.py
│   │   ├── test_database_ops.py
│   │   └── test_auth.py
│   └── performance/                 # Performance tests
│       └── test_benchmarks.py
│
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment variables template
├── Dockerfile                       # Container definition
├── docker-compose.yml               # Docker composition
└── README.md                        # Project documentation
```

### FastAPI Application Entry Point

```python
# app/main.py

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging

from app.api.v1 import (
    knowledge_graph, threat_intel, infrastructure,
    analytics, users, admin
)
from app.graphql.schema import schema
from app.core.settings import settings
from app.core.logging import setup_logging
from app.middleware import (
    RequestIDMiddleware, SecurityHeadersMiddleware,
    RateLimitMiddleware
)
from app.exceptions.handlers import setup_exception_handlers
from app.database import (
    init_neo4j, close_neo4j,
    init_postgres, close_postgres,
    init_mongodb, close_mongodb,
    init_redis, close_redis
)

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle."""
    # Startup
    logger.info("Initializing database connections...")
    await init_neo4j()
    await init_postgres()
    await init_mongodb()
    await init_redis()
    logger.info("✅ All databases initialized")

    yield

    # Shutdown
    logger.info("Closing database connections...")
    await close_neo4j()
    await close_postgres()
    await close_mongodb()
    await close_redis()
    logger.info("✅ All databases closed")

# Create FastAPI application
app = FastAPI(
    title="WAVE 4 Backend API",
    description="Enterprise Knowledge Graph & Threat Intelligence Platform",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    redoc_url="/api/redoc"
)

# Setup middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(RateLimitMiddleware, requests_per_minute=1000)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RequestIDMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup exception handlers
setup_exception_handlers(app)

# Include routers
app.include_router(
    knowledge_graph.router,
    prefix="/api/v1/knowledge-graph",
    tags=["Knowledge Graph"]
)
app.include_router(
    threat_intel.router,
    prefix="/api/v1/threat-intel",
    tags=["Threat Intelligence"]
)
app.include_router(
    infrastructure.router,
    prefix="/api/v1/infrastructure",
    tags=["Infrastructure"]
)
app.include_router(
    analytics.router,
    prefix="/api/v1/analytics",
    tags=["Analytics"]
)
app.include_router(
    users.router,
    prefix="/api/v1/users",
    tags=["Users"]
)
app.include_router(
    admin.router,
    prefix="/api/v1/admin",
    tags=["Admin"]
)

# GraphQL endpoint
from strawberry.asgi import GraphQL

graphql_app = GraphQL(schema)
app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)

# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.utcnow()
    }

# Ready check endpoint
@app.get("/ready", tags=["Health"])
async def readiness_check():
    """Readiness check endpoint."""
    # Check database connectivity
    try:
        from app.services.neo4j_service import neo4j_health_check
        await neo4j_health_check()
        return {"ready": True}
    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        return JSONResponse(
            status_code=503,
            content={"ready": False, "error": str(e)}
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        workers=settings.WORKERS,
        log_level=settings.LOG_LEVEL
    )
```

---

## Authentication & Authorization

### JWT Token Strategy

```python
# app/security.py

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

class TokenData(BaseModel):
    sub: str
    scopes: List[str] = []
    exp: Optional[datetime] = None
    iat: Optional[datetime] = None

class JWTManager:
    """Manage JWT token generation and validation."""

    def __init__(
        self,
        secret_key: str,
        algorithm: str = "HS256",
        access_token_expire_minutes: int = 30,
        refresh_token_expire_days: int = 7
    ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire = timedelta(minutes=access_token_expire_minutes)
        self.refresh_token_expire = timedelta(days=refresh_token_expire_days)
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_access_token(
        self,
        data: Dict[str, Any],
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create JWT access token."""
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or self.access_token_expire)
        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(
            to_encode, self.secret_key, algorithm=self.algorithm
        )
        return encoded_jwt

    def create_refresh_token(self, data: Dict[str, Any]) -> str:
        """Create JWT refresh token."""
        to_encode = data.copy()
        expire = datetime.utcnow() + self.refresh_token_expire
        to_encode.update({"exp": expire, "type": "refresh"})

        encoded_jwt = jwt.encode(
            to_encode, self.secret_key, algorithm=self.algorithm
        )
        return encoded_jwt

    def verify_token(self, token: str) -> Optional[TokenData]:
        """Verify and decode JWT token."""
        try:
            payload = jwt.decode(
                token, self.secret_key, algorithms=[self.algorithm]
            )
            subject: str = payload.get("sub")
            if subject is None:
                return None

            token_scopes = payload.get("scopes", [])
            return TokenData(
                scopes=token_scopes,
                sub=subject,
                exp=datetime.fromtimestamp(payload.get("exp")),
                iat=datetime.fromtimestamp(payload.get("iat"))
            )
        except JWTError:
            return None

    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt."""
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash."""
        return self.pwd_context.verify(plain_password, hashed_password)

# OAuth2 Configuration
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/users/token",
    scopes={
        "read:knowledge_graph": "Read knowledge graph data",
        "write:knowledge_graph": "Write knowledge graph data",
        "read:threat_intel": "Read threat intelligence",
        "write:threat_intel": "Write threat intelligence",
        "admin": "Administrator access"
    }
)
```

### Role-Based Access Control

```python
# app/api/deps.py

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.postgres import get_session
from app.security import oauth2_scheme, JWTManager
from app.models.database import User

class RBACManager:
    """Role-Based Access Control manager."""

    def __init__(self):
        self.role_permissions = {
            "admin": ["read:all", "write:all", "delete:all"],
            "analyst": ["read:all", "write:threat_intel", "write:notes"],
            "operator": ["read:all", "write:infrastructure"],
            "viewer": ["read:all"]
        }

    def has_permission(self, role: str, permission: str) -> bool:
        """Check if role has permission."""
        return permission in self.role_permissions.get(role, [])

    def check_permission(self, required_permission: str):
        """Dependency to check permission."""
        async def verify_permission(
            token: str = Depends(oauth2_scheme),
            session: AsyncSession = Depends(get_session)
        ) -> User:
            credentials_exception = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

            # Verify token and get user
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception

            # Get user from database
            user = await session.execute(
                select(User).where(User.username == username)
            )
            user = user.scalar_one_or_none()

            if user is None:
                raise credentials_exception

            # Check permission
            if not self.has_permission(user.role, required_permission):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions"
                )

            return user

        return verify_permission
```

---

## Endpoint Specifications

### Knowledge Graph Endpoints

```python
# app/api/v1/knowledge_graph.py

from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List, Optional
from app.schemas.knowledge_graph import NodeResponse, EdgeResponse
from app.services.neo4j_service import Neo4jService
from app.api.deps import RBACManager

router = APIRouter()
rbac = RBACManager()
neo4j_service = Neo4jService()

@router.get("/nodes", response_model=List[NodeResponse])
async def get_nodes(
    node_type: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    user = Depends(rbac.check_permission("read:knowledge_graph"))
):
    """Get knowledge graph nodes with filtering and pagination."""
    nodes = await neo4j_service.get_nodes(
        node_type=node_type,
        skip=skip,
        limit=limit
    )
    return nodes

@router.get("/nodes/{node_id}", response_model=NodeResponse)
async def get_node(
    node_id: str,
    user = Depends(rbac.check_permission("read:knowledge_graph"))
):
    """Get specific node by ID."""
    node = await neo4j_service.get_node_by_id(node_id)
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    return node

@router.post("/nodes/{node_id}/relationships", response_model=List[EdgeResponse])
async def get_node_relationships(
    node_id: str,
    relationship_type: Optional[str] = Query(None),
    direction: str = Query("both", regex="^(in|out|both)$"),
    user = Depends(rbac.check_permission("read:knowledge_graph"))
):
    """Get relationships for a specific node."""
    relationships = await neo4j_service.get_relationships(
        node_id=node_id,
        relationship_type=relationship_type,
        direction=direction
    )
    return relationships

@router.post("/search", response_model=List[NodeResponse])
async def search_nodes(
    query: str = Query(..., min_length=1),
    search_type: str = Query("text"),
    limit: int = Query(20, ge=1, le=100),
    user = Depends(rbac.check_permission("read:knowledge_graph"))
):
    """Search knowledge graph nodes."""
    results = await neo4j_service.search_nodes(
        query=query,
        search_type=search_type,
        limit=limit
    )
    return results

@router.post("/query")
async def execute_cypher_query(
    cypher: str,
    parameters: Optional[dict] = None,
    user = Depends(rbac.check_permission("read:knowledge_graph"))
):
    """Execute Cypher query on knowledge graph."""
    results = await neo4j_service.execute_query(
        cypher=cypher,
        parameters=parameters or {}
    )
    return {"results": results}

@router.post("/path")
async def find_path(
    source_id: str,
    target_id: str,
    max_depth: int = Query(5, ge=1, le=20),
    user = Depends(rbac.check_permission("read:knowledge_graph"))
):
    """Find path between two nodes."""
    path = await neo4j_service.find_shortest_path(
        source_id=source_id,
        target_id=target_id,
        max_depth=max_depth
    )
    if not path:
        raise HTTPException(status_code=404, detail="No path found")
    return path
```

### Threat Intelligence Endpoints

```python
# app/api/v1/threat_intel.py

@router.get("/threat-actors", response_model=List[ThreatActorResponse])
async def get_threat_actors(
    country: Optional[str] = Query(None),
    active: Optional[bool] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    user = Depends(rbac.check_permission("read:threat_intel"))
):
    """Get threat actors with filtering."""
    actors = await threat_intel_service.get_threat_actors(
        country=country,
        active=active,
        skip=skip,
        limit=limit
    )
    return actors

@router.get("/campaigns", response_model=List[CampaignResponse])
async def get_campaigns(
    threat_actor_id: Optional[str] = Query(None),
    year: Optional[int] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    user = Depends(rbac.check_permission("read:threat_intel"))
):
    """Get threat campaigns with filtering."""
    campaigns = await threat_intel_service.get_campaigns(
        threat_actor_id=threat_actor_id,
        year=year,
        skip=skip,
        limit=limit
    )
    return campaigns

@router.get("/indicators", response_model=List[IndicatorResponse])
async def get_indicators(
    indicator_type: Optional[str] = Query(None),
    severity: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    user = Depends(rbac.check_permission("read:threat_intel"))
):
    """Get indicators of compromise."""
    indicators = await threat_intel_service.get_indicators(
        indicator_type=indicator_type,
        severity=severity,
        skip=skip,
        limit=limit
    )
    return indicators

@router.post("/indicators/search")
async def search_indicators(
    search_query: str,
    user = Depends(rbac.check_permission("read:threat_intel"))
):
    """Search indicators across databases."""
    results = await threat_intel_service.search_indicators(search_query)
    return results
```

---

## Database Integration

### Multi-Database Service Layer

```python
# app/services/neo4j_service.py

from neo4j import AsyncDriver, AsyncSession
from app.database.neo4j import get_neo4j_driver

class Neo4jService:
    """Service for Neo4j knowledge graph operations."""

    def __init__(self):
        self.driver: AsyncDriver = None

    async def initialize(self):
        """Initialize Neo4j connection."""
        self.driver = await get_neo4j_driver()

    async def get_nodes(
        self,
        node_type: Optional[str] = None,
        skip: int = 0,
        limit: int = 10
    ) -> List[dict]:
        """Get nodes from knowledge graph."""
        async with self.driver.session() as session:
            query = "MATCH (n"
            params = {}

            if node_type:
                query += f":{node_type}"

            query += f") RETURN n SKIP $skip LIMIT $limit"
            params = {"skip": skip, "limit": limit}

            result = await session.run(query, params)
            nodes = await result.values()
            return nodes

    async def find_shortest_path(
        self,
        source_id: str,
        target_id: str,
        max_depth: int = 5
    ) -> Optional[List[dict]]:
        """Find shortest path between nodes."""
        query = """
        MATCH path = shortestPath(
            (source {id: $source_id})-[*..{max_depth}]-(target {id: $target_id})
        )
        RETURN path
        """

        async with self.driver.session() as session:
            result = await session.run(
                query,
                {
                    "source_id": source_id,
                    "target_id": target_id,
                    "max_depth": max_depth
                }
            )
            path = await result.single()
            return path

    async def search_nodes(
        self,
        query: str,
        search_type: str = "text",
        limit: int = 20
    ) -> List[dict]:
        """Search nodes using full-text search."""
        cypher = """
        CALL db.index.fulltext.queryNodes("nodeIndex", $query)
        YIELD node, score
        RETURN node, score
        ORDER BY score DESC
        LIMIT $limit
        """

        async with self.driver.session() as session:
            result = await session.run(
                cypher,
                {"query": query, "limit": limit}
            )
            nodes = await result.values()
            return nodes

# PostgreSQL Service
class PostgresService:
    """Service for PostgreSQL threat intelligence data."""

    async def get_threat_actors(
        self,
        country: Optional[str] = None,
        active: Optional[bool] = None,
        skip: int = 0,
        limit: int = 20
    ) -> List[dict]:
        """Get threat actors from PostgreSQL."""
        async with AsyncSession(engine) as session:
            query = select(ThreatActor)

            if country:
                query = query.where(ThreatActor.country == country)
            if active is not None:
                query = query.where(ThreatActor.is_active == active)

            query = query.offset(skip).limit(limit)
            result = await session.execute(query)
            return result.scalars().all()

# MongoDB Service
class MongodbService:
    """Service for MongoDB operational data."""

    async def get_incident_logs(
        self,
        start_date: datetime,
        end_date: datetime,
        severity: Optional[str] = None
    ) -> List[dict]:
        """Get incident logs from MongoDB."""
        query = {
            "timestamp": {
                "$gte": start_date,
                "$lte": end_date
            }
        }

        if severity:
            query["severity"] = severity

        collection = self.db["incident_logs"]
        logs = await collection.find(query).to_list(None)
        return logs
```

---

## Error Handling & Validation

### Custom Exception Handlers

```python
# app/exceptions/handlers.py

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class APIException(Exception):
    """Base API exception."""

    def __init__(
        self,
        message: str,
        status_code: int = 400,
        error_code: str = "UNKNOWN_ERROR"
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        super().__init__(message)

class DatabaseException(APIException):
    """Database operation exception."""

    def __init__(self, message: str):
        super().__init__(message, status_code=500, error_code="DATABASE_ERROR")

class ValidationException(APIException):
    """Data validation exception."""

    def __init__(self, message: str):
        super().__init__(message, status_code=422, error_code="VALIDATION_ERROR")

def setup_exception_handlers(app: FastAPI):
    """Setup all exception handlers."""

    @app.exception_handler(APIException)
    async def api_exception_handler(request: Request, exc: APIException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": exc.error_code,
                    "message": exc.message,
                    "timestamp": datetime.utcnow().isoformat(),
                    "path": str(request.url.path)
                }
            }
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError
    ):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Invalid request parameters",
                    "details": exc.errors(),
                    "timestamp": datetime.utcnow().isoformat()
                }
            }
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "An unexpected error occurred",
                    "timestamp": datetime.utcnow().isoformat()
                }
            }
        )
```

---

## Performance Optimization

### Response Caching Strategy

```python
# app/services/redis_cache.py

import redis.asyncio as redis
from datetime import timedelta
import json
from typing import Any, Optional

class CacheManager:
    """Redis caching manager."""

    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        value = await self.redis.get(key)
        if value:
            return json.loads(value)
        return None

    async def set(
        self,
        key: str,
        value: Any,
        ttl: int = 3600
    ) -> bool:
        """Set value in cache with TTL."""
        await self.redis.setex(
            key,
            ttl,
            json.dumps(value, default=str)
        )
        return True

    async def delete(self, key: str) -> int:
        """Delete value from cache."""
        return await self.redis.delete(key)

    async def clear_pattern(self, pattern: str) -> int:
        """Clear all keys matching pattern."""
        keys = await self.redis.keys(pattern)
        if keys:
            return await self.redis.delete(*keys)
        return 0

# Cache decorator
from functools import wraps

def cached(ttl: int = 3600, key_prefix: str = ""):
    """Decorator to cache function results."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = f"{key_prefix}:{func.__name__}:{args}:{kwargs}"

            # Try to get from cache
            cached_value = await cache_manager.get(cache_key)
            if cached_value is not None:
                return cached_value

            # Call function and cache result
            result = await func(*args, **kwargs)
            await cache_manager.set(cache_key, result, ttl)
            return result

        return wrapper
    return decorator
```

### Query Optimization

```python
# Database query optimization with pagination
class PaginationParams(BaseModel):
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=20, ge=1, le=100)
    sort_by: Optional[str] = None
    sort_order: str = Field(default="asc", regex="^(asc|desc)$")

async def get_paginated_results(
    query,
    pagination: PaginationParams
) -> Tuple[List[dict], int]:
    """Execute paginated query."""
    # Get total count
    total_count = await query.count()

    # Apply sorting
    if pagination.sort_by:
        order_func = asc if pagination.sort_order == "asc" else desc
        query = query.order_by(order_func(pagination.sort_by))

    # Apply pagination
    query = query.offset(pagination.skip).limit(pagination.limit)

    results = await query.all()
    return results, total_count
```

---

## API Documentation

### OpenAPI/Swagger Configuration

```python
# OpenAPI schema customization
app.openapi_schema = {
    "openapi": "3.0.0",
    "info": {
        "title": "WAVE 4 Backend API",
        "description": """
        Enterprise Knowledge Graph & Threat Intelligence Platform API

        ## Features
        - Knowledge Graph Query & Analysis
        - Threat Intelligence Management
        - Infrastructure Monitoring
        - Real-time Analytics
        - Multi-factor Authentication
        """,
        "version": "1.0.0",
        "contact": {
            "name": "API Support",
            "url": "https://docs.example.com"
        }
    },
    "servers": [
        {
            "url": "https://api.example.com",
            "description": "Production"
        },
        {
            "url": "https://staging-api.example.com",
            "description": "Staging"
        }
    ],
    "components": {
        "securitySchemes": {
            "bearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT"
            }
        }
    }
}
```

---

## Deployment Architecture

### Docker Configuration

```dockerfile
# Dockerfile

FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app/ ./app/
COPY graphql/ ./graphql/

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Kubernetes Deployment

```yaml
# kubernetes/deployment.yaml

apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend-api
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: backend-api
  template:
    metadata:
      labels:
        app: backend-api
    spec:
      containers:
      - name: api
        image: registry.example.com/backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: ENVIRONMENT
          value: "production"
        - name: NEO4J_URI
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: neo4j-uri
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 20
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 10
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
---
apiVersion: v1
kind: Service
metadata:
  name: backend-api-service
  namespace: production
spec:
  selector:
    app: backend-api
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: ClusterIP
```

---

## Summary

This Backend APIs implementation provides:

✅ **Enterprise-Grade FastAPI Framework** with modular structure
✅ **Multi-Database Integration** (Neo4j, PostgreSQL, MongoDB, Redis)
✅ **Comprehensive Security** with JWT, OAuth2, and RBAC
✅ **RESTful & GraphQL APIs** for flexible data access
✅ **Performance Optimization** with caching and query optimization
✅ **Production-Ready Deployment** with Docker and Kubernetes
✅ **Complete Documentation** with OpenAPI/Swagger

**Line Count**: ~1,000 lines of specifications and code patterns

---

**Document Version**: v1.0.0
**Last Updated**: 2025-11-25
**Status**: Implementation Ready
