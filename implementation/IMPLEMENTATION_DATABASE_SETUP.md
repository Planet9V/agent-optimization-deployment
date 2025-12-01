# WAVE 4 Implementation: Database Setup & Configuration

**Document**: IMPLEMENTATION_DATABASE_SETUP.md
**Created**: 2025-11-25 22:30:00 UTC
**Version**: v1.0.0
**Status**: ACTIVE

## Executive Summary

This document specifies the setup, configuration, and management of the 4 specialized databases that comprise WAVE 4's data layer: Neo4j (Knowledge Graph), PostgreSQL (Threat Intelligence), MongoDB (Operational Data), and Redis (Caching). Each database serves a distinct purpose with optimized schemas, indexing strategies, and replication configurations for production deployment.

**Target**: 800 lines of database specifications and setup procedures.

---

## Table of Contents

1. [Database Architecture Overview](#database-architecture-overview)
2. [Neo4j: Knowledge Graph Database](#neo4j-knowledge-graph-database)
3. [PostgreSQL: Threat Intelligence](#postgresql-threat-intelligence)
4. [MongoDB: Operational Data](#mongodb-operational-data)
5. [Redis: Caching Layer](#redis-caching-layer)
6. [Backup & Recovery](#backup--recovery)
7. [Monitoring & Maintenance](#monitoring--maintenance)
8. [Scaling Strategies](#scaling-strategies)

---

## Database Architecture Overview

### Multi-Database Strategy

```
┌─────────────────────────────────────────────────────────────┐
│                   Application Layer (FastAPI)               │
│                                                               │
├─────────────────────────────────────────────────────────────┤
│
├─── Neo4j 4.4+              ├─── PostgreSQL 15+
│    Knowledge Graph         │    Threat Intelligence
│    - 320K+ nodes           │    - 500K+ records
│    - 1.8M+ relationships   │    - Actor profiles
│    - Real-time queries     │    - Campaign metadata
│    - 12GB+ data            │    - Compliance data
│
├─── MongoDB 6.0+            ├─── Redis 7.0+
│    Operational Data        │    Caching Layer
│    - Incident logs         │    - Session cache
│    - Audit trails          │    - Query results
│    - Configuration         │    - Rate limiting
│    - Time-series data      │    - 64GB+ memory
│
└─────────────────────────────────────────────────────────────┘
```

### Hardware Requirements

| Database | CPU | Memory | Storage | Purpose |
|----------|-----|--------|---------|---------|
| Neo4j | 8 cores | 32GB | 500GB SSD | Knowledge graph |
| PostgreSQL | 4 cores | 16GB | 200GB SSD | Threat intel |
| MongoDB | 4 cores | 16GB | 300GB SSD | Operations |
| Redis | 2 cores | 64GB | 50GB SSD | Caching |

---

## Neo4j: Knowledge Graph Database

### Installation & Configuration

```bash
# Docker Compose setup for Neo4j

version: '3.8'
services:
  neo4j:
    image: neo4j:4.4.19-enterprise
    container_name: wave4-neo4j
    environment:
      NEO4J_AUTH: neo4j/ChangeMe@123
      NEO4J_ACCEPT_LICENSE_AGREEMENT: "yes"
      NEO4J_dbms_memory_heap_initial__size: 16g
      NEO4J_dbms_memory_heap_max__size: 32g
      NEO4J_dbms_memory_pagecache_size: 16g
      NEO4J_dbms_jvm_additional: "-XX:+UseG1GC -XX:G1ReservedPercentage=30"
      NEO4J_server_bolt_listen__address: 0.0.0.0:7687
      NEO4J_server_http_listen__address: 0.0.0.0:7474
      NEO4J_dbms_query__execution_timeout: "600000ms"
    ports:
      - "7474:7474"  # HTTP browser
      - "7687:7687"  # Bolt protocol
    volumes:
      - neo4j-data:/data
      - neo4j-logs:/logs
      - neo4j-import:/import
    networks:
      - wave4-network
    healthcheck:
      test: ["CMD", "cypher-shell", "-u", "neo4j", "-p", "ChangeMe@123", "RETURN 1"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  neo4j-data:
  neo4j-logs:
  neo4j-import:

networks:
  wave4-network:
    driver: bridge
```

### Neo4j Schema Definition

```cypher
// Create indexes for performance
CREATE INDEX idx_node_id FOR (n) ON (n.id);
CREATE INDEX idx_node_type FOR (n) ON (n.type);
CREATE INDEX idx_threat_actor_country FOR (t:ThreatActor) ON (t.country);
CREATE INDEX idx_campaign_date FOR (c:Campaign) ON (c.start_date);
CREATE INDEX idx_cve_severity FOR (v:CVE) ON (v.severity);
CREATE FULLTEXT INDEX nodeIndex FOR (n) ON EACH [n.label, n.description];

// Create uniqueness constraints
CREATE CONSTRAINT unique_node_id ON (n) ASSERT n.id IS UNIQUE;
CREATE CONSTRAINT unique_cve_id ON (c:CVE) ASSERT c.cve_id IS UNIQUE;
CREATE CONSTRAINT unique_threat_actor_id ON (t:ThreatActor) ASSERT t.id IS UNIQUE;

// Node type definitions with properties
CREATE (:NodeType {
  name: 'ThreatActor',
  properties: ['id', 'name', 'country', 'type', 'aliases', 'first_seen', 'last_seen', 'is_active']
});

CREATE (:NodeType {
  name: 'Campaign',
  properties: ['id', 'name', 'start_date', 'end_date', 'description', 'attribution']
});

CREATE (:NodeType {
  name: 'AttackPattern',
  properties: ['id', 'name', 'mitre_id', 'description', 'platform', 'impact']
});

CREATE (:NodeType {
  name: 'DetectionSignature',
  properties: ['id', 'name', 'rule_type', 'content', 'false_positive_rate']
});

CREATE (:NodeType {
  name: 'Indicator',
  properties: ['id', 'type', 'value', 'source', 'confidence', 'timestamp']
});

// Relationship definitions
CREATE (:RelationshipType {
  name: 'ORCHESTRATES_CAMPAIGN',
  source: 'ThreatActor',
  target: 'Campaign'
});

CREATE (:RelationshipType {
  name: 'USES_ATTACK_PATTERN',
  source: 'ThreatActor',
  target: 'AttackPattern'
});

CREATE (:RelationshipType {
  name: 'TARGETS_DEVICE',
  source: 'AttackPattern',
  target: 'InfrastructureDevice'
});
```

### Connection Pooling Configuration

```python
# app/database/neo4j.py

from neo4j import AsyncGraphDatabase, AsyncDriver
from contextlib import asynccontextmanager

class Neo4jConnectionPool:
    """Neo4j connection pool manager."""

    def __init__(self, uri: str, user: str, password: str):
        self.uri = uri
        self.user = user
        self.password = password
        self.driver: AsyncDriver = None

    async def initialize(self):
        """Initialize Neo4j driver with connection pooling."""
        self.driver = AsyncGraphDatabase.driver(
            self.uri,
            auth=(self.user, self.password),
            max_connection_lifetime=3600,
            max_connection_pool_size=50,
            connection_acquisition_timeout=30,
            connection_timeout=30,
            trust="TRUST_SYSTEM_CA_SIGNED_CERTIFICATES",
            encrypted=True
        )
        # Verify connectivity
        await self.driver.verify_connectivity()

    async def close(self):
        """Close the driver."""
        if self.driver:
            await self.driver.close()

    @asynccontextmanager
    async def session(self, database: str = "neo4j"):
        """Get a session from the pool."""
        session = self.driver.session(database=database)
        try:
            yield session
        finally:
            await session.close()

# Initialize globally
neo4j_pool = Neo4jConnectionPool(
    uri="bolt+s://localhost:7687",
    user="neo4j",
    password=os.getenv("NEO4J_PASSWORD")
)

async def get_neo4j_driver() -> AsyncDriver:
    """Get Neo4j driver instance."""
    if not neo4j_pool.driver:
        await neo4j_pool.initialize()
    return neo4j_pool.driver
```

### Query Patterns

```cypher
// Example 1: Find all threat actors targeting specific infrastructure
MATCH (ta:ThreatActor)-[:USES_ATTACK_PATTERN]->(ap:AttackPattern)-[:TARGETS_DEVICE]->(id:InfrastructureDevice)
WHERE id.type = 'SCADA'
RETURN DISTINCT ta.name, COUNT(ap) as pattern_count
ORDER BY pattern_count DESC

// Example 2: Find attack paths between two threat actors
MATCH path = shortestPath(
  (ta1:ThreatActor {name: 'APT33'})-[*..5]-(ta2:ThreatActor {name: 'APT41'})
)
RETURN path

// Example 3: Get comprehensive threat actor profile
MATCH (ta:ThreatActor {name: 'Lazarus'})
OPTIONAL MATCH (ta)-[:ORCHESTRATES_CAMPAIGN]->(c:Campaign)
OPTIONAL MATCH (ta)-[:USES_ATTACK_PATTERN]->(ap:AttackPattern)
OPTIONAL MATCH (ap)-[:IMPLEMENTS]->(ttp:TTP)
RETURN {
  actor: ta,
  campaigns: COLLECT(DISTINCT c),
  patterns: COLLECT(DISTINCT ap),
  ttps: COLLECT(DISTINCT ttp)
}
```

---

## PostgreSQL: Threat Intelligence

### Installation & Configuration

```bash
# Docker Compose for PostgreSQL

services:
  postgres:
    image: postgres:15-alpine
    container_name: wave4-postgres
    environment:
      POSTGRES_DB: wave4_threat_intel
      POSTGRES_USER: threat_user
      POSTGRES_PASSWORD: SecurePassword@123
      PGDATA: /var/lib/postgresql/data/pgdata
    ports:
      - "5432:5432"
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    command:
      - "postgres"
      - "-c"
      - "max_connections=200"
      - "-c"
      - "shared_buffers=4GB"
      - "-c"
      - "effective_cache_size=12GB"
      - "-c"
      - "work_mem=20MB"
      - "-c"
      - "maintenance_work_mem=1GB"
    networks:
      - wave4-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U threat_user"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres-data:
```

### PostgreSQL Schema

```sql
-- Create database and extensions
CREATE DATABASE wave4_threat_intel;

\c wave4_threat_intel

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "citext";

-- Threat Actors Table
CREATE TABLE threat_actors (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) UNIQUE NOT NULL,
    country VARCHAR(2) NOT NULL,
    actor_type VARCHAR(50) NOT NULL, -- 'nation-state', 'cybercriminal', 'hacktivism'
    aliases TEXT[] NOT NULL DEFAULT '{}',
    description TEXT,
    first_seen TIMESTAMP WITH TIME ZONE,
    last_seen TIMESTAMP WITH TIME ZONE,
    is_active BOOLEAN DEFAULT true,
    confidence_score FLOAT CHECK (confidence_score >= 0 AND confidence_score <= 1),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_threat_actors_country ON threat_actors(country);
CREATE INDEX idx_threat_actors_active ON threat_actors(is_active);
CREATE INDEX idx_threat_actors_name ON threat_actors USING GIN (aliases gin__int_ops);

-- Campaigns Table
CREATE TABLE campaigns (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    threat_actor_id UUID NOT NULL REFERENCES threat_actors(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    description TEXT,
    objective VARCHAR(255),
    target_industries TEXT[],
    target_countries TEXT[],
    attack_patterns TEXT[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_campaigns_threat_actor ON campaigns(threat_actor_id);
CREATE INDEX idx_campaigns_date_range ON campaigns(start_date, end_date);
CREATE INDEX idx_campaigns_industries ON campaigns USING GIN (target_industries);

-- Indicators of Compromise Table
CREATE TABLE indicators (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    campaign_id UUID REFERENCES campaigns(id) ON DELETE SET NULL,
    indicator_type VARCHAR(50) NOT NULL, -- 'ip', 'domain', 'hash', 'email', 'file'
    indicator_value VARCHAR(1000) NOT NULL,
    source VARCHAR(255),
    confidence_score FLOAT CHECK (confidence_score >= 0 AND confidence_score <= 1),
    severity VARCHAR(20) NOT NULL, -- 'critical', 'high', 'medium', 'low'
    first_seen TIMESTAMP WITH TIME ZONE,
    last_seen TIMESTAMP WITH TIME ZONE,
    is_current BOOLEAN DEFAULT true,
    context JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_indicators_type ON indicators(indicator_type);
CREATE INDEX idx_indicators_value ON indicators USING GIN (indicator_value gin_trgm_ops);
CREATE INDEX idx_indicators_severity ON indicators(severity);
CREATE INDEX idx_indicators_campaign ON indicators(campaign_id);
CREATE INDEX idx_indicators_context ON indicators USING GIN (context);

-- Malware Samples Table
CREATE TABLE malware_samples (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    campaign_id UUID REFERENCES campaigns(id),
    name VARCHAR(255) NOT NULL,
    hash_md5 VARCHAR(32),
    hash_sha256 VARCHAR(64) UNIQUE,
    first_seen TIMESTAMP WITH TIME ZONE,
    last_seen TIMESTAMP WITH TIME ZONE,
    malware_family VARCHAR(100),
    behavior JSONB,
    detected_by INTEGER, -- Count of AV engines
    confidence_score FLOAT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_malware_campaign ON malware_samples(campaign_id);
CREATE INDEX idx_malware_sha256 ON malware_samples(hash_sha256);
CREATE INDEX idx_malware_family ON malware_samples(malware_family);

-- Create audit trigger
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER threat_actors_timestamp BEFORE UPDATE ON threat_actors
    FOR EACH ROW EXECUTE FUNCTION update_timestamp();

CREATE TRIGGER campaigns_timestamp BEFORE UPDATE ON campaigns
    FOR EACH ROW EXECUTE FUNCTION update_timestamp();

CREATE TRIGGER indicators_timestamp BEFORE UPDATE ON indicators
    FOR EACH ROW EXECUTE FUNCTION update_timestamp();
```

### SQLAlchemy Models

```python
# app/models/database.py

from sqlalchemy import Column, String, DateTime, Boolean, Float, JSON, ForeignKey, Index, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()

class ThreatActor(Base):
    __tablename__ = "threat_actors"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), unique=True, nullable=False)
    country = Column(String(2), nullable=False)
    actor_type = Column(String(50), nullable=False)
    aliases = Column(ARRAY(String), default=[])
    description = Column(String, nullable=True)
    first_seen = Column(DateTime, nullable=True)
    last_seen = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    confidence_score = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index('idx_threat_actors_country', 'country'),
        Index('idx_threat_actors_active', 'is_active'),
    )

class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    threat_actor_id = Column(UUID(as_uuid=True), ForeignKey('threat_actors.id'), nullable=False)
    name = Column(String(255), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)
    description = Column(String, nullable=True)
    objective = Column(String(255), nullable=True)
    target_industries = Column(ARRAY(String), default=[])
    target_countries = Column(ARRAY(String), default=[])
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index('idx_campaigns_threat_actor', 'threat_actor_id'),
        Index('idx_campaigns_date_range', 'start_date', 'end_date'),
    )

class Indicator(Base):
    __tablename__ = "indicators"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    campaign_id = Column(UUID(as_uuid=True), ForeignKey('campaigns.id'))
    indicator_type = Column(String(50), nullable=False)
    indicator_value = Column(String(1000), nullable=False)
    source = Column(String(255), nullable=True)
    confidence_score = Column(Float, nullable=True)
    severity = Column(String(20), nullable=False)
    first_seen = Column(DateTime, nullable=True)
    last_seen = Column(DateTime, nullable=True)
    is_current = Column(Boolean, default=True)
    context = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index('idx_indicators_type', 'indicator_type'),
        Index('idx_indicators_severity', 'severity'),
        Index('idx_indicators_campaign', 'campaign_id'),
    )
```

---

## MongoDB: Operational Data

### Docker Setup

```yaml
# MongoDB in Docker Compose

services:
  mongodb:
    image: mongo:6.0.5-alpine
    container_name: wave4-mongodb
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: SecurePassword@123
      MONGO_INITDB_DATABASE: wave4_operations
    ports:
      - "27017:27017"
    volumes:
      - mongodb-data:/data/db
      - ./mongo-init.js:/docker-entrypoint-initdb.d/mongo-init.js
    networks:
      - wave4-network
    command: --replSet rs0
    healthcheck:
      test: echo 'db.runCommand("ping").ok' | mongosh localhost:27017 -u admin -p SecurePassword@123
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  mongodb-data:
```

### MongoDB Schema & Collections

```javascript
// mongo-init.js

// Initialize Replica Set
db.adminCommand({
  replSetInitiate: {
    _id: "rs0",
    members: [
      {
        _id: 0,
        host: "mongodb:27017"
      }
    ]
  }
});

// Create admin user
db.createUser({
  user: "admin",
  pwd: "SecurePassword@123",
  roles: ["root"]
});

// Use operational database
db = db.getSiblingDB("wave4_operations");

// Create collections with schema validation
db.createCollection("incident_logs", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["timestamp", "incident_type", "severity", "source"],
      properties: {
        _id: { bsonType: "objectId" },
        timestamp: { bsonType: "date" },
        incident_type: { enum: ["alert", "detection", "threat", "system"] },
        severity: { enum: ["critical", "high", "medium", "low"] },
        source: { bsonType: "string" },
        description: { bsonType: "string" },
        details: { bsonType: "object" },
        related_indicators: { bsonType: "array" },
        status: { enum: ["open", "investigating", "closed"] },
        assigned_to: { bsonType: "string" }
      }
    }
  }
});

// Create audit logs collection
db.createCollection("audit_logs", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["timestamp", "action", "user_id"],
      properties: {
        timestamp: { bsonType: "date" },
        action: { bsonType: "string" },
        user_id: { bsonType: "string" },
        resource: { bsonType: "string" },
        changes: { bsonType: "object" }
      }
    }
  }
});

// Create time-series collection for metrics
db.createCollection("metrics", {
  timeseries: {
    timeField: "timestamp",
    metaField: "metadata",
    granularity: "minutes"
  }
});

// Create indexes
db.incident_logs.createIndex({ timestamp: -1 });
db.incident_logs.createIndex({ severity: 1 });
db.incident_logs.createIndex({ status: 1 });
db.incident_logs.createIndex({ source: 1 });

db.audit_logs.createIndex({ timestamp: -1 });
db.audit_logs.createIndex({ user_id: 1 });
db.audit_logs.createIndex({ action: 1 });

db.metrics.createIndex({ "metadata.host": 1, timestamp: -1 });

// Enable TTL for incident logs (90-day retention)
db.incident_logs.createIndex(
  { timestamp: 1 },
  { expireAfterSeconds: 7776000 }
);
```

### Motor (Async MongoDB) Integration

```python
# app/database/mongodb.py

from motor.motor_asyncio import AsyncClient, AsyncDatabase
import os

class MongoDBConnection:
    """MongoDB async connection manager."""

    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.client: AsyncClient = None
        self.db: AsyncDatabase = None

    async def connect(self):
        """Connect to MongoDB."""
        self.client = AsyncClient(self.connection_string)
        self.db = self.client["wave4_operations"]
        # Verify connection
        await self.db.command("ping")

    async def close(self):
        """Close MongoDB connection."""
        if self.client:
            self.client.close()

    async def get_incident_logs(
        self,
        filters: dict = None,
        limit: int = 100
    ):
        """Get incident logs."""
        collection = self.db["incident_logs"]
        query = filters or {}
        return await collection.find(query).limit(limit).to_list(None)

    async def create_audit_log(self, log_data: dict):
        """Create audit log entry."""
        collection = self.db["audit_logs"]
        result = await collection.insert_one(log_data)
        return str(result.inserted_id)

# Initialize connection
mongodb = MongoDBConnection(
    os.getenv("MONGODB_URL", "mongodb://admin:password@localhost:27017")
)

async def get_mongodb() -> AsyncDatabase:
    """Get MongoDB database instance."""
    if not mongodb.client:
        await mongodb.connect()
    return mongodb.db
```

---

## Redis: Caching Layer

### Docker Configuration

```yaml
services:
  redis:
    image: redis:7.2-alpine
    container_name: wave4-redis
    command:
      - redis-server
      - "--maxmemory"
      - "64gb"
      - "--maxmemory-policy"
      - "allkeys-lru"
      - "--appendonly"
      - "yes"
      - "--requirepass"
      - "SecurePassword@123"
      - "--timeout"
      - "300"
      - "--tcp-keepalive"
      - "60"
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    networks:
      - wave4-network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  redis-data:
```

### Redis Caching Patterns

```python
# app/services/redis_cache.py

import redis.asyncio as redis
import json
from typing import Any, Optional
from datetime import timedelta

class RedisCache:
    """Redis caching service."""

    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.redis: Optional[redis.Redis] = None

    async def connect(self):
        """Connect to Redis."""
        self.redis = await redis.from_url(self.connection_string)

    async def close(self):
        """Close Redis connection."""
        if self.redis:
            await self.redis.close()

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
        """Set value in cache."""
        await self.redis.setex(
            key,
            ttl,
            json.dumps(value, default=str)
        )
        return True

    async def delete(self, key: str) -> int:
        """Delete key from cache."""
        return await self.redis.delete(key)

    async def exists(self, key: str) -> bool:
        """Check if key exists."""
        return await self.redis.exists(key) > 0

    async def incr(self, key: str, amount: int = 1) -> int:
        """Increment counter."""
        return await self.redis.incrby(key, amount)

    async def expire(self, key: str, ttl: int) -> bool:
        """Set expiration on key."""
        return await self.redis.expire(key, ttl)

# Caching patterns
CACHE_PATTERNS = {
    "threat_actor": "threat_actor:{id}",
    "campaign": "campaign:{id}",
    "node": "node:{id}",
    "search_results": "search:{query}:{limit}",
    "user_session": "session:{user_id}",
    "rate_limit": "ratelimit:{user_id}:{endpoint}",
}

async def cache_threat_actor(actor_id: str, data: dict, ttl: int = 3600):
    """Cache threat actor data."""
    key = CACHE_PATTERNS["threat_actor"].format(id=actor_id)
    await redis_cache.set(key, data, ttl)

async def get_cached_threat_actor(actor_id: str) -> Optional[dict]:
    """Get cached threat actor."""
    key = CACHE_PATTERNS["threat_actor"].format(id=actor_id)
    return await redis_cache.get(key)
```

---

## Backup & Recovery

### Backup Strategy

```bash
#!/bin/bash
# backup-all-databases.sh

BACKUP_DIR="/backups/wave4"
DATE=$(date +%Y%m%d_%H%M%S)

# Neo4j backup
echo "Backing up Neo4j..."
docker exec wave4-neo4j neo4j-admin database backup neo4j \
  --to-path=/backup/${DATE}/neo4j

# PostgreSQL backup
echo "Backing up PostgreSQL..."
docker exec wave4-postgres pg_dump \
  -U threat_user wave4_threat_intel \
  | gzip > ${BACKUP_DIR}/postgres_${DATE}.sql.gz

# MongoDB backup
echo "Backing up MongoDB..."
docker exec wave4-mongodb mongodump \
  --authenticationDatabase admin \
  --out /backup/${DATE}/mongodb

# Redis backup
echo "Backing up Redis..."
docker exec wave4-redis redis-cli \
  --rdb /backup/${DATE}/redis.rdb

# Upload to S3
echo "Uploading backups to S3..."
aws s3 sync ${BACKUP_DIR} s3://wave4-backups/

echo "Backup completed: ${DATE}"
```

### Recovery Procedures

```bash
#!/bin/bash
# restore-database.sh

BACKUP_DIR=$1
RESTORE_DATE=$2

# Restore Neo4j
echo "Restoring Neo4j..."
docker exec wave4-neo4j neo4j-admin database restore \
  --from-path=/backup/${RESTORE_DATE}/neo4j neo4j

# Restore PostgreSQL
echo "Restoring PostgreSQL..."
gunzip < ${BACKUP_DIR}/postgres_${RESTORE_DATE}.sql.gz | \
  docker exec -i wave4-postgres psql \
  -U threat_user wave4_threat_intel

# Restore MongoDB
echo "Restoring MongoDB..."
docker exec wave4-mongodb mongorestore \
  --authenticationDatabase admin \
  /backup/${RESTORE_DATE}/mongodb

# Restore Redis
echo "Restoring Redis..."
docker exec wave4-redis redis-cli --rdb < /backup/${RESTORE_DATE}/redis.rdb

echo "Restore completed"
```

---

## Monitoring & Maintenance

### Database Monitoring Queries

```sql
-- PostgreSQL: Check table sizes
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- PostgreSQL: Check slow queries
SELECT
    query,
    calls,
    mean_exec_time,
    max_exec_time
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;

-- PostgreSQL: Check connection count
SELECT
    datname,
    usename,
    application_name,
    state,
    COUNT(*) as count
FROM pg_stat_activity
GROUP BY datname, usename, application_name, state;
```

```python
# app/monitoring/database_health.py

async def check_database_health():
    """Check health of all databases."""
    health_status = {
        "neo4j": await check_neo4j_health(),
        "postgres": await check_postgres_health(),
        "mongodb": await check_mongodb_health(),
        "redis": await check_redis_health(),
    }
    return health_status

async def check_neo4j_health():
    """Check Neo4j health."""
    async with neo4j_pool.session() as session:
        result = await session.run("CALL dbms.system.kernel.runtime()")
        return {"status": "healthy", "info": result}

async def check_postgres_health():
    """Check PostgreSQL health."""
    async with get_session() as session:
        result = await session.execute(
            "SELECT NOW() as server_time, version() as version"
        )
        return {"status": "healthy", "info": result.first()}

async def check_mongodb_health():
    """Check MongoDB health."""
    try:
        db = await get_mongodb()
        await db.command("ping")
        return {"status": "healthy"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

async def check_redis_health():
    """Check Redis health."""
    try:
        result = await redis_cache.redis.ping()
        return {"status": "healthy", "ping": result}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
```

---

## Scaling Strategies

### Neo4j Clustering

```yaml
# Docker Compose for Neo4j Cluster

services:
  neo4j-core-1:
    image: neo4j:4.4.19-enterprise
    environment:
      NEO4J_ACCEPT_LICENSE_AGREEMENT: "yes"
      NEO4J_causal__clustering_enabled: "true"
      NEO4J_dbms_mode: "CORE"
      NEO4J_causal__clustering_core__address: "neo4j-core-1:5000"
      NEO4J_causal__clustering_discovery__service__address: "neo4j-core-1:5000"
      NEO4J_causal__clustering_initial__discovery__members: "neo4j-core-1:5000,neo4j-core-2:5000,neo4j-core-3:5000"

  neo4j-core-2:
    image: neo4j:4.4.19-enterprise
    environment:
      NEO4J_ACCEPT_LICENSE_AGREEMENT: "yes"
      NEO4J_causal__clustering_enabled: "true"
      NEO4J_dbms_mode: "CORE"
      NEO4J_causal__clustering_core__address: "neo4j-core-2:5000"
      NEO4J_causal__clustering_discovery__service__address: "neo4j-core-2:5000"
      NEO4J_causal__clustering_initial__discovery__members: "neo4j-core-1:5000,neo4j-core-2:5000,neo4j-core-3:5000"

  neo4j-core-3:
    image: neo4j:4.4.19-enterprise
    environment:
      NEO4J_ACCEPT_LICENSE_AGREEMENT: "yes"
      NEO4J_causal__clustering_enabled: "true"
      NEO4J_dbms_mode: "CORE"
      NEO4J_causal__clustering_core__address: "neo4j-core-3:5000"
      NEO4J_causal__clustering_discovery__service__address: "neo4j-core-3:5000"
      NEO4J_causal__clustering_initial__discovery__members: "neo4j-core-1:5000,neo4j-core-2:5000,neo4j-core-3:5000"
```

### PostgreSQL Replication

```sql
-- Primary database setup
ALTER SYSTEM SET wal_level = 'replica';
ALTER SYSTEM SET max_wal_senders = 10;
ALTER SYSTEM SET max_replication_slots = 10;

-- Create replication user
CREATE ROLE replication_user WITH REPLICATION LOGIN PASSWORD 'ReplicationPassword@123';

-- On standby database
SELECT * FROM pg_basebackup(
    slot_name => 'standby_slot',
    timeline => 'latest'
);
```

---

## Summary

This Database Setup implementation provides:

✅ **Multi-Database Architecture** optimized for each data type
✅ **Neo4j Knowledge Graph** with 320K+ nodes and relationships
✅ **PostgreSQL Threat Intelligence** with 500K+ records
✅ **MongoDB Operational Data** with audit and incident logs
✅ **Redis Caching Layer** with 64GB memory
✅ **Comprehensive Backup & Recovery** strategies
✅ **Production-Ready Monitoring** and health checks
✅ **Enterprise Scaling** with clustering and replication

**Line Count**: ~800 lines of database specifications and configurations

---

**Document Version**: v1.0.0
**Last Updated**: 2025-11-25
**Status**: Implementation Ready
