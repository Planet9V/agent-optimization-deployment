# GAP-006 Architecture Design: Distributed Worker & Job Queue System

**File:** GAP-006_ARCHITECTURE_DESIGN_2025-11-15.md
**Created:** 2025-11-15 14:30:00 UTC
**Version:** v1.0.0
**Author:** System Architecture Designer
**Purpose:** Complete architecture design for persistent job storage, distributed worker system, and error recovery
**Status:** ACTIVE

---

## Executive Summary

This document defines the complete architecture for GAP-006, extending the existing AEON infrastructure with:
- **Persistent Job Storage** using existing PostgreSQL (aeon-postgres-dev)
- **Redis-based Job Queue** integrated into existing docker network
- **Distributed Worker Architecture** leveraging current services
- **Comprehensive Error Recovery** with retry logic and dead letter queues
- **Job Monitoring & Observability** system

**Key Constraint:** EXTENDS existing infrastructure, does NOT duplicate services.

---

## 1. Current Infrastructure Analysis

### 1.1 Existing Services (openspg-network)

```
┌─────────────────────────────────────────────────────────────────┐
│                     EXISTING INFRASTRUCTURE                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────┐    ┌──────────────────┐                   │
│  │  aeon-saas-dev   │    │ aeon-postgres-dev│                   │
│  │   (Next.js)      │───>│  postgres:16     │                   │
│  │  Port: 3000      │    │  Port: 5432      │                   │
│  └──────────────────┘    │  DB: aeon_saas   │                   │
│                          └──────────────────┘                   │
│                                                                   │
│  ┌──────────────────┐    ┌──────────────────┐                   │
│  │  openspg-neo4j   │    │  openspg-mysql   │                   │
│  │  Port: 7687      │    │  Port: 3306      │                   │
│  └──────────────────┘    └──────────────────┘                   │
│                                                                   │
│  ┌──────────────────┐    ┌──────────────────┐                   │
│  │  openspg-minio   │    │  openspg-qdrant  │                   │
│  │  Port: 9000      │    │  Port: 6333      │                   │
│  └──────────────────┘    └──────────────────┘                   │
│                                                                   │
│  ┌──────────────────┐                                            │
│  │  openspg-server  │                                            │
│  │  Port: 8887      │                                            │
│  └──────────────────┘                                            │
│                                                                   │
│  Network: openspg-network (bridge driver)                        │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Existing PostgreSQL Schema

**Database:** `aeon_saas_dev`
**User:** `postgres`
**Password:** `postgres`

**Current Tables:**
- users, teams, team_members
- roles, user_roles
- subscriptions, invitations
- audit_logs, api_keys

---

## 2. GAP-006 Architecture Design

### 2.1 High-Level Architecture

```
┌───────────────────────────────────────────────────────────────────────┐
│                    GAP-006 DISTRIBUTED JOB SYSTEM                     │
├───────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │                      JOB SUBMISSION LAYER                        │  │
│  │  ┌──────────────────┐          ┌──────────────────┐             │  │
│  │  │  Next.js API     │          │   CLI Tools      │             │  │
│  │  │  /api/jobs/*     │          │   (Future)       │             │  │
│  │  └────────┬─────────┘          └────────┬─────────┘             │  │
│  └───────────┼──────────────────────────────┼────────────────────────┘  │
│              │                              │                           │
│              v                              v                           │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │                    JOB QUEUE LAYER (Redis)                       │  │
│  │  ┌──────────────────────────────────────────────────────────┐   │  │
│  │  │  aeon-redis (redis:7-alpine)                              │   │  │
│  │  │  ┌────────────┐  ┌────────────┐  ┌────────────┐          │   │  │
│  │  │  │ Pending    │  │ Active     │  │ Completed  │          │   │  │
│  │  │  │ Queue      │  │ Queue      │  │ Queue      │          │   │  │
│  │  │  └────────────┘  └────────────┘  └────────────┘          │   │  │
│  │  │  ┌────────────┐  ┌────────────┐                           │   │  │
│  │  │  │ Failed     │  │ Dead Letter│                           │   │  │
│  │  │  │ Queue      │  │ Queue      │                           │   │  │
│  │  │  └────────────┘  └────────────┘                           │   │  │
│  │  │  Port: 6379                                               │   │  │
│  │  └──────────────────────────────────────────────────────────┘   │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│              │                                                         │
│              v                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │                   WORKER POOL LAYER                              │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │  │
│  │  │  Worker 1    │  │  Worker 2    │  │  Worker N    │          │  │
│  │  │  (Node.js)   │  │  (Node.js)   │  │  (Node.js)   │          │  │
│  │  │              │  │              │  │              │          │  │
│  │  │ - Poll Queue │  │ - Poll Queue │  │ - Poll Queue │          │  │
│  │  │ - Execute    │  │ - Execute    │  │ - Execute    │          │  │
│  │  │ - Update DB  │  │ - Update DB  │  │ - Update DB  │          │  │
│  │  │ - Retry      │  │ - Retry      │  │ - Retry      │          │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘          │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│              │                                                         │
│              v                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │              PERSISTENT STORAGE LAYER (PostgreSQL)               │  │
│  │  ┌──────────────────────────────────────────────────────────┐   │  │
│  │  │  aeon-postgres-dev (postgres:16-alpine)                   │   │  │
│  │  │  Database: aeon_saas_dev (EXTENDED)                       │   │  │
│  │  │                                                            │   │  │
│  │  │  NEW TABLES:                                               │   │  │
│  │  │  ├─ jobs                  (main job records)              │   │  │
│  │  │  ├─ job_executions        (execution attempts)            │   │  │
│  │  │  ├─ job_dependencies      (job relationships)             │   │  │
│  │  │  ├─ job_schedules         (recurring jobs)                │   │  │
│  │  │  └─ dead_letter_jobs      (permanent failures)            │   │  │
│  │  │                                                            │   │  │
│  │  │  Port: 5432                                                │   │  │
│  │  └──────────────────────────────────────────────────────────┘   │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │                   MONITORING & OBSERVABILITY                     │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │  │
│  │  │  Job Status  │  │  Metrics     │  │  Alerts      │          │  │
│  │  │  Dashboard   │  │  (Redis)     │  │  (Future)    │          │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘          │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                                                         │
└───────────────────────────────────────────────────────────────────────┘
```

### 2.2 Component Interaction Flow

```
┌──────────────┐
│   Client     │
│  (Browser)   │
└──────┬───────┘
       │ 1. Submit Job
       v
┌─────────────────────────────────────┐
│  Next.js API Route                  │
│  POST /api/jobs/create              │
│  ┌───────────────────────────────┐  │
│  │ 1. Validate request           │  │
│  │ 2. Create job record in DB    │  │
│  │ 3. Push to Redis queue        │  │
│  │ 4. Return job_id              │  │
│  └───────────────────────────────┘  │
└──────┬──────────────────────────────┘
       │
       v
┌─────────────────────────────────────┐
│  PostgreSQL (aeon-postgres-dev)     │
│  ┌───────────────────────────────┐  │
│  │ INSERT INTO jobs              │  │
│  │ status = 'pending'            │  │
│  │ created_at = NOW()            │  │
│  └───────────────────────────────┘  │
└──────┬──────────────────────────────┘
       │
       v
┌─────────────────────────────────────┐
│  Redis Queue (aeon-redis)           │
│  ┌───────────────────────────────┐  │
│  │ LPUSH pending:queue job_id    │  │
│  │ SET job:{id}:data {...}       │  │
│  └───────────────────────────────┘  │
└──────┬──────────────────────────────┘
       │
       │ 2. Worker polls queue
       v
┌─────────────────────────────────────┐
│  Worker Process                     │
│  ┌───────────────────────────────┐  │
│  │ BRPOPLPUSH pending active     │  │
│  │ GET job:{id}:data             │  │
│  │                               │  │
│  │ BEGIN TRANSACTION             │  │
│  │   UPDATE jobs SET             │  │
│  │     status = 'running'        │  │
│  │   INSERT INTO job_executions  │  │
│  │ COMMIT                        │  │
│  └───────────────────────────────┘  │
└──────┬──────────────────────────────┘
       │
       │ 3. Execute job
       v
┌─────────────────────────────────────┐
│  Job Handler                        │
│  ┌───────────────────────────────┐  │
│  │ try {                         │  │
│  │   executeJobLogic()           │  │
│  │   updateJobSuccess()          │  │
│  │ } catch (error) {             │  │
│  │   updateJobFailure()          │  │
│  │   handleRetry()               │  │
│  │ }                             │  │
│  └───────────────────────────────┘  │
└──────┬──────────────────────────────┘
       │
       v
┌─────────────────────────────────────┐
│  Result Processing                  │
│  ┌───────────────────────────────┐  │
│  │ IF SUCCESS:                   │  │
│  │   UPDATE jobs                 │  │
│  │     status = 'completed'      │  │
│  │   LREM active:queue           │  │
│  │   LPUSH completed:queue       │  │
│  │                               │  │
│  │ IF FAILURE (retriable):       │  │
│  │   UPDATE jobs                 │  │
│  │     retry_count++             │  │
│  │   IF retry_count < max:       │  │
│  │     LPUSH pending:queue       │  │
│  │   ELSE:                       │  │
│  │     LPUSH dlq:queue           │  │
│  │     INSERT dead_letter_jobs   │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

---

## 3. PostgreSQL Schema Design

### 3.1 New Tables for Job Management

```sql
-- ============================================================================
-- GAP-006 JOB MANAGEMENT SCHEMA
-- Extends existing aeon_saas_dev database
-- ============================================================================

-- Enable required extensions (if not already enabled)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ============================================================================
-- 3.1.1 JOBS TABLE (Main job records)
-- ============================================================================
CREATE TABLE IF NOT EXISTS jobs (
    -- Primary identification
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    -- Job type and classification
    job_type VARCHAR(100) NOT NULL,
    job_category VARCHAR(50) DEFAULT 'general',
    priority INTEGER DEFAULT 5 CHECK (priority BETWEEN 1 AND 10),

    -- Job data
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    result JSONB,
    error_details JSONB,

    -- Status tracking
    status VARCHAR(50) NOT NULL DEFAULT 'pending'
        CHECK (status IN ('pending', 'queued', 'running', 'completed',
                         'failed', 'cancelled', 'paused', 'dead_letter')),

    -- Progress tracking
    progress_percent INTEGER DEFAULT 0 CHECK (progress_percent BETWEEN 0 AND 100),
    progress_message TEXT,

    -- Retry configuration
    max_retries INTEGER DEFAULT 3,
    retry_count INTEGER DEFAULT 0,
    retry_delay_ms INTEGER DEFAULT 1000,
    backoff_multiplier DECIMAL(3,2) DEFAULT 2.0,

    -- Timeout configuration
    timeout_ms INTEGER DEFAULT 300000, -- 5 minutes default

    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    queued_at TIMESTAMP WITH TIME ZONE,
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    failed_at TIMESTAMP WITH TIME ZONE,

    -- Ownership and context
    created_by UUID REFERENCES users(id) ON DELETE SET NULL,
    team_id UUID REFERENCES teams(id) ON DELETE CASCADE,

    -- Dependencies
    parent_job_id UUID REFERENCES jobs(id) ON DELETE CASCADE,

    -- Scheduling
    schedule_id UUID,
    scheduled_for TIMESTAMP WITH TIME ZONE,

    -- Metadata
    tags TEXT[] DEFAULT '{}',
    metadata JSONB DEFAULT '{}'::jsonb,

    -- Execution context
    worker_id VARCHAR(255),
    execution_node VARCHAR(255),

    -- Indexes for performance
    CONSTRAINT jobs_retry_check CHECK (retry_count <= max_retries)
);

-- Indexes for jobs table
CREATE INDEX idx_jobs_status ON jobs(status) WHERE status IN ('pending', 'queued', 'running');
CREATE INDEX idx_jobs_job_type ON jobs(job_type);
CREATE INDEX idx_jobs_priority ON jobs(priority DESC);
CREATE INDEX idx_jobs_created_at ON jobs(created_at DESC);
CREATE INDEX idx_jobs_team_id ON jobs(team_id);
CREATE INDEX idx_jobs_created_by ON jobs(created_by);
CREATE INDEX idx_jobs_parent_job ON jobs(parent_job_id);
CREATE INDEX idx_jobs_schedule ON jobs(schedule_id) WHERE schedule_id IS NOT NULL;
CREATE INDEX idx_jobs_scheduled_for ON jobs(scheduled_for) WHERE scheduled_for IS NOT NULL;
CREATE INDEX idx_jobs_tags ON jobs USING GIN(tags);
CREATE INDEX idx_jobs_payload ON jobs USING GIN(payload);

-- ============================================================================
-- 3.1.2 JOB_EXECUTIONS TABLE (Execution attempt history)
-- ============================================================================
CREATE TABLE IF NOT EXISTS job_executions (
    -- Primary identification
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    job_id UUID NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,

    -- Execution details
    attempt_number INTEGER NOT NULL,
    status VARCHAR(50) NOT NULL
        CHECK (status IN ('started', 'completed', 'failed', 'timeout', 'cancelled')),

    -- Timing
    started_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITH TIME ZONE,
    duration_ms INTEGER,

    -- Results
    result JSONB,
    error_message TEXT,
    error_stack TEXT,
    error_code VARCHAR(100),

    -- Execution context
    worker_id VARCHAR(255),
    execution_node VARCHAR(255),

    -- Resource usage
    memory_used_mb INTEGER,
    cpu_time_ms INTEGER,

    -- Metadata
    metadata JSONB DEFAULT '{}'::jsonb,

    -- Constraints
    CONSTRAINT job_executions_unique_attempt UNIQUE(job_id, attempt_number)
);

-- Indexes for job_executions
CREATE INDEX idx_job_executions_job_id ON job_executions(job_id);
CREATE INDEX idx_job_executions_status ON job_executions(status);
CREATE INDEX idx_job_executions_started_at ON job_executions(started_at DESC);
CREATE INDEX idx_job_executions_worker ON job_executions(worker_id);

-- ============================================================================
-- 3.1.3 JOB_DEPENDENCIES TABLE (Job relationships and dependencies)
-- ============================================================================
CREATE TABLE IF NOT EXISTS job_dependencies (
    -- Primary identification
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    -- Dependency relationship
    job_id UUID NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    depends_on_job_id UUID NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,

    -- Dependency type
    dependency_type VARCHAR(50) DEFAULT 'completion'
        CHECK (dependency_type IN ('completion', 'success', 'data', 'conditional')),

    -- Conditional dependencies
    condition JSONB,

    -- Status
    satisfied BOOLEAN DEFAULT FALSE,
    satisfied_at TIMESTAMP WITH TIME ZONE,

    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB DEFAULT '{}'::jsonb,

    -- Prevent circular dependencies
    CONSTRAINT job_dependencies_no_self CHECK (job_id != depends_on_job_id),
    CONSTRAINT job_dependencies_unique UNIQUE(job_id, depends_on_job_id)
);

-- Indexes for job_dependencies
CREATE INDEX idx_job_dependencies_job_id ON job_dependencies(job_id);
CREATE INDEX idx_job_dependencies_depends_on ON job_dependencies(depends_on_job_id);
CREATE INDEX idx_job_dependencies_unsatisfied ON job_dependencies(job_id) WHERE satisfied = FALSE;

-- ============================================================================
-- 3.1.4 JOB_SCHEDULES TABLE (Recurring job schedules)
-- ============================================================================
CREATE TABLE IF NOT EXISTS job_schedules (
    -- Primary identification
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    -- Schedule details
    name VARCHAR(255) NOT NULL,
    job_type VARCHAR(100) NOT NULL,
    payload_template JSONB NOT NULL DEFAULT '{}'::jsonb,

    -- Schedule configuration
    schedule_type VARCHAR(50) NOT NULL
        CHECK (schedule_type IN ('cron', 'interval', 'once')),
    cron_expression VARCHAR(255),
    interval_ms INTEGER,

    -- Status
    enabled BOOLEAN DEFAULT TRUE,

    -- Execution tracking
    last_run_at TIMESTAMP WITH TIME ZONE,
    next_run_at TIMESTAMP WITH TIME ZONE,
    run_count INTEGER DEFAULT 0,

    -- Limits
    max_runs INTEGER,
    expires_at TIMESTAMP WITH TIME ZONE,

    -- Ownership
    created_by UUID REFERENCES users(id) ON DELETE SET NULL,
    team_id UUID REFERENCES teams(id) ON DELETE CASCADE,

    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB DEFAULT '{}'::jsonb,

    -- Validation
    CONSTRAINT job_schedules_cron_check CHECK (
        (schedule_type = 'cron' AND cron_expression IS NOT NULL) OR
        (schedule_type = 'interval' AND interval_ms IS NOT NULL) OR
        (schedule_type = 'once')
    ),
    CONSTRAINT job_schedules_max_runs_check CHECK (
        max_runs IS NULL OR run_count <= max_runs
    )
);

-- Indexes for job_schedules
CREATE INDEX idx_job_schedules_enabled ON job_schedules(enabled) WHERE enabled = TRUE;
CREATE INDEX idx_job_schedules_next_run ON job_schedules(next_run_at) WHERE enabled = TRUE;
CREATE INDEX idx_job_schedules_team_id ON job_schedules(team_id);
CREATE INDEX idx_job_schedules_job_type ON job_schedules(job_type);

-- ============================================================================
-- 3.1.5 DEAD_LETTER_JOBS TABLE (Permanently failed jobs)
-- ============================================================================
CREATE TABLE IF NOT EXISTS dead_letter_jobs (
    -- Primary identification
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    -- Original job reference
    original_job_id UUID NOT NULL,

    -- Job snapshot
    job_type VARCHAR(100) NOT NULL,
    payload JSONB NOT NULL,

    -- Failure details
    failure_reason TEXT NOT NULL,
    final_error_message TEXT,
    final_error_stack TEXT,
    total_attempts INTEGER NOT NULL,

    -- Execution history
    execution_history JSONB,

    -- Resolution tracking
    status VARCHAR(50) DEFAULT 'pending'
        CHECK (status IN ('pending', 'investigating', 'resolved', 'ignored')),
    resolution_notes TEXT,
    resolved_by UUID REFERENCES users(id) ON DELETE SET NULL,
    resolved_at TIMESTAMP WITH TIME ZONE,

    -- Context
    team_id UUID REFERENCES teams(id) ON DELETE CASCADE,

    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB DEFAULT '{}'::jsonb
);

-- Indexes for dead_letter_jobs
CREATE INDEX idx_dead_letter_jobs_status ON dead_letter_jobs(status);
CREATE INDEX idx_dead_letter_jobs_job_type ON dead_letter_jobs(job_type);
CREATE INDEX idx_dead_letter_jobs_created_at ON dead_letter_jobs(created_at DESC);
CREATE INDEX idx_dead_letter_jobs_team_id ON dead_letter_jobs(team_id);
CREATE INDEX idx_dead_letter_jobs_original_job ON dead_letter_jobs(original_job_id);

-- ============================================================================
-- 3.2 TRIGGERS
-- ============================================================================

-- Update updated_at timestamp
CREATE OR REPLACE FUNCTION update_jobs_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_jobs_updated_at
    BEFORE UPDATE ON jobs
    FOR EACH ROW
    EXECUTE FUNCTION update_jobs_updated_at();

CREATE TRIGGER trigger_job_schedules_updated_at
    BEFORE UPDATE ON job_schedules
    FOR EACH ROW
    EXECUTE FUNCTION update_jobs_updated_at();

-- Auto-populate execution duration
CREATE OR REPLACE FUNCTION calculate_execution_duration()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.completed_at IS NOT NULL AND NEW.started_at IS NOT NULL THEN
        NEW.duration_ms = EXTRACT(EPOCH FROM (NEW.completed_at - NEW.started_at)) * 1000;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_calculate_duration
    BEFORE UPDATE ON job_executions
    FOR EACH ROW
    EXECUTE FUNCTION calculate_execution_duration();

-- ============================================================================
-- 3.3 FUNCTIONS
-- ============================================================================

-- Get jobs ready for execution
CREATE OR REPLACE FUNCTION get_ready_jobs(
    p_limit INTEGER DEFAULT 10,
    p_job_types TEXT[] DEFAULT NULL
)
RETURNS TABLE (
    job_id UUID,
    job_type VARCHAR,
    priority INTEGER,
    payload JSONB
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        j.id,
        j.job_type,
        j.priority,
        j.payload
    FROM jobs j
    WHERE j.status = 'pending'
        AND (p_job_types IS NULL OR j.job_type = ANY(p_job_types))
        AND (j.scheduled_for IS NULL OR j.scheduled_for <= CURRENT_TIMESTAMP)
        AND NOT EXISTS (
            SELECT 1 FROM job_dependencies jd
            WHERE jd.job_id = j.id
                AND jd.satisfied = FALSE
        )
    ORDER BY j.priority DESC, j.created_at ASC
    LIMIT p_limit
    FOR UPDATE SKIP LOCKED;
END;
$$ LANGUAGE plpgsql;

-- Check if all dependencies are satisfied
CREATE OR REPLACE FUNCTION check_dependencies_satisfied(p_job_id UUID)
RETURNS BOOLEAN AS $$
DECLARE
    v_unsatisfied_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO v_unsatisfied_count
    FROM job_dependencies
    WHERE job_id = p_job_id AND satisfied = FALSE;

    RETURN v_unsatisfied_count = 0;
END;
$$ LANGUAGE plpgsql;

-- Get job statistics
CREATE OR REPLACE FUNCTION get_job_statistics(
    p_team_id UUID DEFAULT NULL,
    p_time_window INTERVAL DEFAULT '24 hours'
)
RETURNS TABLE (
    total_jobs BIGINT,
    pending_jobs BIGINT,
    running_jobs BIGINT,
    completed_jobs BIGINT,
    failed_jobs BIGINT,
    dead_letter_jobs BIGINT,
    avg_duration_ms NUMERIC
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        COUNT(*) FILTER (WHERE created_at >= CURRENT_TIMESTAMP - p_time_window) as total_jobs,
        COUNT(*) FILTER (WHERE status = 'pending') as pending_jobs,
        COUNT(*) FILTER (WHERE status = 'running') as running_jobs,
        COUNT(*) FILTER (WHERE status = 'completed') as completed_jobs,
        COUNT(*) FILTER (WHERE status = 'failed') as failed_jobs,
        COUNT(*) FILTER (WHERE status = 'dead_letter') as dead_letter_jobs,
        COALESCE(AVG(
            EXTRACT(EPOCH FROM (completed_at - started_at)) * 1000
        ) FILTER (WHERE status = 'completed' AND completed_at IS NOT NULL), 0) as avg_duration_ms
    FROM jobs
    WHERE (p_team_id IS NULL OR team_id = p_team_id);
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- 3.4 GRANT PERMISSIONS
-- ============================================================================
GRANT ALL PRIVILEGES ON TABLE jobs TO postgres;
GRANT ALL PRIVILEGES ON TABLE job_executions TO postgres;
GRANT ALL PRIVILEGES ON TABLE job_dependencies TO postgres;
GRANT ALL PRIVILEGES ON TABLE job_schedules TO postgres;
GRANT ALL PRIVILEGES ON TABLE dead_letter_jobs TO postgres;

GRANT EXECUTE ON FUNCTION get_ready_jobs TO postgres;
GRANT EXECUTE ON FUNCTION check_dependencies_satisfied TO postgres;
GRANT EXECUTE ON FUNCTION get_job_statistics TO postgres;

-- ============================================================================
-- 3.5 COMMENTS (Documentation)
-- ============================================================================
COMMENT ON TABLE jobs IS 'Main job queue table storing all job records';
COMMENT ON TABLE job_executions IS 'Execution attempt history for jobs';
COMMENT ON TABLE job_dependencies IS 'Job dependency relationships';
COMMENT ON TABLE job_schedules IS 'Recurring job schedules';
COMMENT ON TABLE dead_letter_jobs IS 'Permanently failed jobs requiring manual intervention';

COMMENT ON FUNCTION get_ready_jobs IS 'Returns jobs ready for execution, respecting dependencies and priorities';
COMMENT ON FUNCTION check_dependencies_satisfied IS 'Checks if all dependencies for a job are satisfied';
COMMENT ON FUNCTION get_job_statistics IS 'Returns job queue statistics for monitoring';
```

### 3.2 Migration Script

Save as: `/home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney/web_interface/scripts/migrations/001_gap006_job_tables.sql`

```sql
-- GAP-006 Migration: Add job management tables to existing aeon_saas_dev database
-- This script is idempotent and safe to run multiple times

BEGIN;

-- Include the complete schema from section 3.1 above

COMMIT;

-- Verification
SELECT 'Migration 001_gap006_job_tables completed successfully' as status;
SELECT tablename FROM pg_tables WHERE schemaname = 'public' AND tablename LIKE 'job%' ORDER BY tablename;
```

---

## 4. Redis Integration Design

### 4.1 Update docker-compose.redis.yml

**Current Issues:**
- Uses separate `aeon-network` instead of `openspg-network`
- Not integrated with existing services

**Required Changes:**

```yaml
version: '3.8'

services:
  redis:
    image: redis:7-alpine
    container_name: aeon-redis
    command: redis-server --appendonly yes --requirepass ${REDIS_PASSWORD:-aeon_redis_dev}
    ports:
      - "${REDIS_PORT:-6379}:6379"
    volumes:
      - redis-data:/data
      - ./config/redis.conf:/usr/local/etc/redis/redis.conf:ro
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "--raw", "incr", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5
    networks:
      - openspg-network  # CHANGED: Use existing network

  redis-commander:
    image: rediscommander/redis-commander:latest
    container_name: aeon-redis-commander
    environment:
      - REDIS_HOSTS=local:aeon-redis:6379:0:${REDIS_PASSWORD:-aeon_redis_dev}
      - HTTP_USER=admin
      - HTTP_PASSWORD=${REDIS_COMMANDER_PASSWORD:-admin}
    ports:
      - "8081:8081"
    depends_on:
      redis:
        condition: service_healthy
    restart: unless-stopped
    networks:
      - openspg-network  # CHANGED: Use existing network

volumes:
  redis-data:
    name: aeon_redis_data
    driver: local

networks:
  openspg-network:  # CHANGED: Reference existing network
    external: true
    name: openspg-network
```

### 4.2 Redis Configuration File

Create: `/home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney/web_interface/config/redis.conf`

```conf
# Redis configuration for AEON Job Queue
# Optimized for job processing workload

# Memory management
maxmemory 512mb
maxmemory-policy allkeys-lru

# Persistence
save 900 1
save 300 10
save 60 10000
appendonly yes
appendfsync everysec

# Performance
tcp-backlog 511
timeout 0
tcp-keepalive 300

# Limits
maxclients 10000

# Slow log
slowlog-log-slower-than 10000
slowlog-max-len 128

# Event notification for job queue
notify-keyspace-events Ex

# Disable dangerous commands in production
rename-command FLUSHDB ""
rename-command FLUSHALL ""
rename-command CONFIG ""
```

### 4.3 Redis Queue Structure

```
┌─────────────────────────────────────────────────────────────┐
│                    REDIS KEY STRUCTURE                       │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  QUEUES (Lists):                                             │
│  ├─ queue:pending          (LPUSH new jobs)                 │
│  ├─ queue:active           (BRPOPLPUSH during processing)   │
│  ├─ queue:completed        (LPUSH after success)            │
│  ├─ queue:failed           (LPUSH after retriable failure)  │
│  └─ queue:dlq              (LPUSH after max retries)        │
│                                                               │
│  JOB DATA (Hashes):                                          │
│  ├─ job:{id}:data          (Full job payload)               │
│  ├─ job:{id}:status        (Current status)                 │
│  ├─ job:{id}:progress      (Progress percentage)            │
│  └─ job:{id}:locks         (Worker lock)                    │
│                                                               │
│  WORKER TRACKING (Sets/Hashes):                              │
│  ├─ workers:active         (Set of active worker IDs)       │
│  ├─ worker:{id}:heartbeat  (Last heartbeat timestamp)       │
│  └─ worker:{id}:jobs       (Set of jobs being processed)    │
│                                                               │
│  METRICS (Sorted Sets):                                      │
│  ├─ metrics:completed      (Completion timestamps)          │
│  ├─ metrics:failed         (Failure timestamps)             │
│  └─ metrics:durations      (Execution durations)            │
│                                                               │
│  LOCKS (Strings with TTL):                                   │
│  └─ lock:job:{id}          (Prevents duplicate processing)  │
│                                                               │
│  TTL SETTINGS:                                               │
│  ├─ job:{id}:*             → 7 days                         │
│  ├─ worker:{id}:*          → 1 hour                         │
│  ├─ lock:job:{id}          → 5 minutes                      │
│  └─ metrics:*              → 30 days                        │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### 4.4 Redis Operations

**Job Submission:**
```javascript
// Pseudo-code
async function enqueueJob(jobId, payload) {
  const redis = await getRedisClient();

  // Atomic operation using MULTI/EXEC
  const multi = redis.multi();
  multi.hset(`job:${jobId}:data`, payload);
  multi.set(`job:${jobId}:status`, 'queued');
  multi.lpush('queue:pending', jobId);
  multi.expire(`job:${jobId}:data`, 604800); // 7 days

  await multi.exec();
}
```

**Job Processing:**
```javascript
async function processNextJob(workerId) {
  const redis = await getRedisClient();

  // Atomically move from pending to active
  const jobId = await redis.brpoplpush('queue:pending', 'queue:active', 5);

  if (!jobId) return null;

  // Acquire lock
  const locked = await redis.set(
    `lock:job:${jobId}`,
    workerId,
    'NX',
    'EX',
    300
  );

  if (!locked) {
    // Lock failed, job taken by another worker
    await redis.lrem('queue:active', 1, jobId);
    return null;
  }

  // Get job data
  const jobData = await redis.hgetall(`job:${jobId}:data`);
  return { jobId, ...jobData };
}
```

**Job Completion:**
```javascript
async function completeJob(jobId, result, success) {
  const redis = await getRedisClient();
  const multi = redis.multi();

  if (success) {
    multi.hset(`job:${jobId}:data`, 'result', JSON.stringify(result));
    multi.set(`job:${jobId}:status`, 'completed');
    multi.lrem('queue:active', 1, jobId);
    multi.lpush('queue:completed', jobId);
    multi.zadd('metrics:completed', Date.now(), jobId);
  } else {
    multi.hset(`job:${jobId}:data`, 'error', JSON.stringify(result));
    multi.set(`job:${jobId}:status`, 'failed');
    multi.lrem('queue:active', 1, jobId);
    multi.lpush('queue:failed', jobId);
    multi.zadd('metrics:failed', Date.now(), jobId);
  }

  multi.del(`lock:job:${jobId}`);
  await multi.exec();
}
```

---

## 5. Worker Architecture Design

### 5.1 Worker Process Structure

```
┌─────────────────────────────────────────────────────────────┐
│                    WORKER PROCESS                            │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Worker Lifecycle Manager                             │  │
│  │  ├─ Initialize                                        │  │
│  │  ├─ Register with coordinator                         │  │
│  │  ├─ Start heartbeat                                   │  │
│  │  ├─ Start job polling loop                            │  │
│  │  └─ Graceful shutdown handler                         │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                               │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Job Polling Engine                                   │  │
│  │  ├─ BRPOPLPUSH queue:pending → queue:active          │  │
│  │  ├─ Acquire job lock                                  │  │
│  │  ├─ Fetch job data from PostgreSQL                   │  │
│  │  ├─ Validate job                                      │  │
│  │  └─ Route to handler                                  │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                               │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Job Execution Engine                                 │  │
│  │  ├─ Update status: running                            │  │
│  │  ├─ Create execution record                           │  │
│  │  ├─ Execute job handler                               │  │
│  │  ├─ Handle timeout                                    │  │
│  │  └─ Capture metrics                                   │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                               │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Error Recovery Manager                               │  │
│  │  ├─ Catch execution errors                            │  │
│  │  ├─ Determine if retriable                            │  │
│  │  ├─ Implement exponential backoff                     │  │
│  │  ├─ Update retry count                                │  │
│  │  ├─ Re-queue OR send to DLQ                          │  │
│  │  └─ Log failure details                               │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                               │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Result Handler                                       │  │
│  │  ├─ Update job status                                 │  │
│  │  ├─ Store result in PostgreSQL                        │  │
│  │  ├─ Update Redis queues                               │  │
│  │  ├─ Release job lock                                  │  │
│  │  ├─ Trigger dependent jobs                            │  │
│  │  └─ Emit metrics                                      │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                               │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Health Monitor                                       │  │
│  │  ├─ Heartbeat to Redis (every 10s)                   │  │
│  │  ├─ Monitor memory usage                              │  │
│  │  ├─ Monitor CPU usage                                 │  │
│  │  ├─ Job timeout watchdog                              │  │
│  │  └─ Self-restart on errors                            │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### 5.2 Worker Implementation Structure

```
/workers
├── /src
│   ├── /core
│   │   ├── worker.ts              # Main worker class
│   │   ├── job-executor.ts        # Job execution engine
│   │   ├── error-handler.ts       # Error recovery logic
│   │   └── health-monitor.ts      # Health checking
│   │
│   ├── /handlers                  # Job type handlers
│   │   ├── base-handler.ts        # Abstract base handler
│   │   ├── data-import-handler.ts # Example: data import jobs
│   │   ├── report-handler.ts      # Example: report generation
│   │   └── index.ts               # Handler registry
│   │
│   ├── /services
│   │   ├── postgres.ts            # PostgreSQL client
│   │   ├── redis.ts               # Redis client
│   │   └── metrics.ts             # Metrics collection
│   │
│   ├── /config
│   │   ├── worker-config.ts       # Worker configuration
│   │   └── retry-config.ts        # Retry strategies
│   │
│   └── index.ts                   # Entry point
│
├── /tests
│   ├── /unit
│   └── /integration
│
├── Dockerfile                     # Worker container image
├── package.json
└── tsconfig.json
```

### 5.3 Worker Configuration

```typescript
// worker-config.ts
export const workerConfig = {
  // Worker identification
  workerId: process.env.WORKER_ID || `worker-${process.pid}`,
  workerType: process.env.WORKER_TYPE || 'general',

  // Polling configuration
  pollInterval: parseInt(process.env.POLL_INTERVAL || '1000'),
  batchSize: parseInt(process.env.BATCH_SIZE || '1'),

  // Job types this worker can handle
  jobTypes: process.env.JOB_TYPES?.split(',') || ['*'],

  // Concurrency limits
  maxConcurrentJobs: parseInt(process.env.MAX_CONCURRENT_JOBS || '5'),

  // Timeout configuration
  defaultTimeout: parseInt(process.env.DEFAULT_TIMEOUT || '300000'), // 5 min
  maxTimeout: parseInt(process.env.MAX_TIMEOUT || '3600000'), // 1 hour

  // Retry configuration
  maxRetries: parseInt(process.env.MAX_RETRIES || '3'),
  retryDelay: parseInt(process.env.RETRY_DELAY || '1000'),
  backoffMultiplier: parseFloat(process.env.BACKOFF_MULTIPLIER || '2.0'),

  // Health monitoring
  heartbeatInterval: parseInt(process.env.HEARTBEAT_INTERVAL || '10000'),
  healthCheckInterval: parseInt(process.env.HEALTH_CHECK_INTERVAL || '30000'),

  // Resource limits
  memoryLimitMB: parseInt(process.env.MEMORY_LIMIT_MB || '512'),

  // Database connections
  postgres: {
    host: process.env.POSTGRES_HOST || 'postgres-dev',
    port: parseInt(process.env.POSTGRES_PORT || '5432'),
    database: process.env.POSTGRES_DB || 'aeon_saas_dev',
    user: process.env.POSTGRES_USER || 'postgres',
    password: process.env.POSTGRES_PASSWORD || 'postgres',
    max: 10, // connection pool size
  },

  redis: {
    host: process.env.REDIS_HOST || 'aeon-redis',
    port: parseInt(process.env.REDIS_PORT || '6379'),
    password: process.env.REDIS_PASSWORD || 'aeon_redis_dev',
  },

  // Graceful shutdown
  shutdownTimeout: parseInt(process.env.SHUTDOWN_TIMEOUT || '30000'),
};
```

### 5.4 Worker Deployment

**Docker Compose Addition:**

Add to `/home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney/web_interface/docker-compose.workers.yml`:

```yaml
version: '3.8'

services:
  # General purpose worker
  worker-general:
    build:
      context: ./workers
      dockerfile: Dockerfile
    container_name: aeon-worker-general-1
    environment:
      - NODE_ENV=production
      - WORKER_ID=worker-general-1
      - WORKER_TYPE=general
      - JOB_TYPES=*
      - MAX_CONCURRENT_JOBS=5

      # PostgreSQL
      - POSTGRES_HOST=postgres-dev
      - POSTGRES_PORT=5432
      - POSTGRES_DB=aeon_saas_dev
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres

      # Redis
      - REDIS_HOST=aeon-redis
      - REDIS_PORT=6379
      - REDIS_PASSWORD=aeon_redis_dev

    depends_on:
      postgres-dev:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - openspg-network
    restart: unless-stopped
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '1.0'
        reservations:
          memory: 256M
          cpus: '0.5'

  # Specialized worker for data import
  worker-data-import:
    build:
      context: ./workers
      dockerfile: Dockerfile
    container_name: aeon-worker-data-import-1
    environment:
      - NODE_ENV=production
      - WORKER_ID=worker-data-import-1
      - WORKER_TYPE=data-import
      - JOB_TYPES=data_import,file_processing
      - MAX_CONCURRENT_JOBS=3

      # Same PostgreSQL and Redis config
      - POSTGRES_HOST=postgres-dev
      - POSTGRES_PORT=5432
      - POSTGRES_DB=aeon_saas_dev
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - REDIS_HOST=aeon-redis
      - REDIS_PORT=6379
      - REDIS_PASSWORD=aeon_redis_dev

    depends_on:
      postgres-dev:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - openspg-network
    restart: unless-stopped
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: '2.0'
        reservations:
          memory: 512M
          cpus: '1.0'

networks:
  openspg-network:
    external: true
    name: openspg-network
```

### 5.5 Worker Scaling Strategy

```
┌─────────────────────────────────────────────────────────────┐
│                 WORKER SCALING STRATEGY                      │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  HORIZONTAL SCALING:                                         │
│  ├─ Add more worker containers                              │
│  ├─ Each worker polls from same Redis queue                 │
│  ├─ Redis BRPOPLPUSH ensures no duplicate processing        │
│  └─ Load balances automatically                             │
│                                                               │
│  VERTICAL SCALING:                                           │
│  ├─ Increase MAX_CONCURRENT_JOBS per worker                 │
│  ├─ Increase memory/CPU limits                              │
│  └─ Monitor resource usage                                   │
│                                                               │
│  SPECIALIZED WORKERS:                                        │
│  ├─ worker-general: handles all job types                   │
│  ├─ worker-data-import: optimized for large data jobs       │
│  ├─ worker-reports: optimized for report generation         │
│  └─ worker-priority: only handles high-priority jobs        │
│                                                               │
│  AUTO-SCALING TRIGGERS:                                      │
│  ├─ queue:pending length > 100 → scale up                  │
│  ├─ queue:pending length < 10 → scale down                 │
│  ├─ avg job wait time > 5min → scale up                    │
│  └─ worker CPU > 80% → add workers                         │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 6. Error Recovery & Retry Logic

### 6.1 Error Classification

```typescript
// error-types.ts
export enum ErrorType {
  // Retriable errors
  TRANSIENT_NETWORK = 'transient_network',      // Retry with backoff
  RATE_LIMIT = 'rate_limit',                     // Retry with delay
  TEMPORARY_RESOURCE = 'temporary_resource',     // Retry immediately
  TIMEOUT = 'timeout',                           // Retry with increased timeout

  // Non-retriable errors
  VALIDATION_ERROR = 'validation_error',         // DLQ
  AUTHENTICATION_ERROR = 'authentication_error', // DLQ
  NOT_FOUND = 'not_found',                       // DLQ
  PERMISSION_DENIED = 'permission_denied',       // DLQ
  INVALID_INPUT = 'invalid_input',               // DLQ

  // System errors
  INTERNAL_ERROR = 'internal_error',             // Retry limited
  DATABASE_ERROR = 'database_error',             // Retry with backoff
  UNKNOWN = 'unknown',                           // Retry limited
}

export interface ErrorClassification {
  type: ErrorType;
  retriable: boolean;
  maxRetries: number;
  retryDelay: number;
  backoffMultiplier: number;
}

export function classifyError(error: Error): ErrorClassification {
  // Network errors
  if (error.message.includes('ECONNREFUSED') ||
      error.message.includes('ETIMEDOUT')) {
    return {
      type: ErrorType.TRANSIENT_NETWORK,
      retriable: true,
      maxRetries: 5,
      retryDelay: 2000,
      backoffMultiplier: 2.0,
    };
  }

  // Rate limiting
  if (error.message.includes('rate limit') ||
      error.message.includes('429')) {
    return {
      type: ErrorType.RATE_LIMIT,
      retriable: true,
      maxRetries: 3,
      retryDelay: 60000, // 1 minute
      backoffMultiplier: 1.5,
    };
  }

  // Validation errors
  if (error.name === 'ValidationError' ||
      error.message.includes('invalid')) {
    return {
      type: ErrorType.VALIDATION_ERROR,
      retriable: false,
      maxRetries: 0,
      retryDelay: 0,
      backoffMultiplier: 1.0,
    };
  }

  // Default: limited retry
  return {
    type: ErrorType.UNKNOWN,
    retriable: true,
    maxRetries: 2,
    retryDelay: 5000,
    backoffMultiplier: 2.0,
  };
}
```

### 6.2 Retry Strategy Implementation

```typescript
// retry-handler.ts
export class RetryHandler {
  async handleJobFailure(
    jobId: string,
    error: Error,
    currentRetry: number
  ): Promise<void> {
    const classification = classifyError(error);

    // Record execution attempt
    await this.recordExecution(jobId, {
      status: 'failed',
      error_message: error.message,
      error_stack: error.stack,
      error_code: classification.type,
    });

    if (!classification.retriable) {
      // Send to dead letter queue
      await this.sendToDeadLetterQueue(jobId, error, currentRetry);
      return;
    }

    if (currentRetry >= classification.maxRetries) {
      // Max retries exceeded
      await this.sendToDeadLetterQueue(jobId, error, currentRetry);
      return;
    }

    // Calculate retry delay with exponential backoff
    const delay = this.calculateRetryDelay(
      classification.retryDelay,
      currentRetry,
      classification.backoffMultiplier
    );

    // Update job for retry
    await this.scheduleRetry(jobId, delay, currentRetry + 1);
  }

  private calculateRetryDelay(
    baseDelay: number,
    attempt: number,
    multiplier: number
  ): number {
    // Exponential backoff: delay * (multiplier ^ attempt)
    const exponentialDelay = baseDelay * Math.pow(multiplier, attempt);

    // Add jitter (±20%) to prevent thundering herd
    const jitter = exponentialDelay * 0.2 * (Math.random() - 0.5);

    return Math.floor(exponentialDelay + jitter);
  }

  private async scheduleRetry(
    jobId: string,
    delayMs: number,
    nextRetry: number
  ): Promise<void> {
    const scheduledFor = new Date(Date.now() + delayMs);

    // Update database
    await db.query(`
      UPDATE jobs
      SET
        status = 'pending',
        retry_count = $1,
        scheduled_for = $2,
        updated_at = NOW()
      WHERE id = $3
    `, [nextRetry, scheduledFor, jobId]);

    // Re-queue in Redis with delay
    await redis.zadd(
      'queue:delayed',
      scheduledFor.getTime(),
      jobId
    );
  }

  private async sendToDeadLetterQueue(
    jobId: string,
    error: Error,
    attempts: number
  ): Promise<void> {
    // Get job data
    const job = await db.query(`
      SELECT * FROM jobs WHERE id = $1
    `, [jobId]);

    // Get execution history
    const executions = await db.query(`
      SELECT * FROM job_executions
      WHERE job_id = $1
      ORDER BY attempt_number
    `, [jobId]);

    // Insert into dead letter queue
    await db.query(`
      INSERT INTO dead_letter_jobs (
        original_job_id,
        job_type,
        payload,
        failure_reason,
        final_error_message,
        final_error_stack,
        total_attempts,
        execution_history,
        team_id
      ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
    `, [
      jobId,
      job.job_type,
      job.payload,
      classifyError(error).type,
      error.message,
      error.stack,
      attempts,
      JSON.stringify(executions),
      job.team_id,
    ]);

    // Update original job
    await db.query(`
      UPDATE jobs
      SET
        status = 'dead_letter',
        failed_at = NOW(),
        updated_at = NOW()
      WHERE id = $1
    `, [jobId]);

    // Move to DLQ in Redis
    await redis.multi()
      .lrem('queue:active', 1, jobId)
      .lrem('queue:failed', 1, jobId)
      .lpush('queue:dlq', jobId)
      .exec();
  }
}
```

### 6.3 Delayed Job Processor

```typescript
// delayed-job-processor.ts
export class DelayedJobProcessor {
  private readonly checkInterval = 1000; // Check every second

  async start(): Promise<void> {
    setInterval(() => this.processDelayedJobs(), this.checkInterval);
  }

  private async processDelayedJobs(): Promise<void> {
    const now = Date.now();

    // Get jobs ready to run from Redis sorted set
    const readyJobs = await redis.zrangebyscore(
      'queue:delayed',
      '-inf',
      now,
      'LIMIT',
      0,
      100
    );

    if (readyJobs.length === 0) return;

    // Move to pending queue
    const multi = redis.multi();
    for (const jobId of readyJobs) {
      multi.zrem('queue:delayed', jobId);
      multi.lpush('queue:pending', jobId);
      multi.set(`job:${jobId}:status`, 'queued');
    }
    await multi.exec();

    console.log(`Moved ${readyJobs.length} delayed jobs to pending queue`);
  }
}
```

---

## 7. Job Monitoring & Observability

### 7.1 Monitoring Dashboard Structure

```
┌─────────────────────────────────────────────────────────────┐
│                  JOB MONITORING DASHBOARD                    │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  OVERVIEW METRICS                                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ Total Jobs  │  │ Success     │  │ Failed      │         │
│  │   12,458    │  │   Rate 94%  │  │   Rate 6%   │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│                                                               │
│  QUEUE DEPTHS                                                │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Pending: ████████░░ 1,234                            │   │
│  │ Active:  ██░░░░░░░░    45                            │   │
│  │ Failed:  █░░░░░░░░░     8                            │   │
│  │ DLQ:     ░░░░░░░░░░     2                            │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
│  WORKER STATUS                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ worker-general-1     ✓  5 jobs   CPU: 45%  Mem: 312M│   │
│  │ worker-general-2     ✓  4 jobs   CPU: 38%  Mem: 289M│   │
│  │ worker-data-import-1 ✓  2 jobs   CPU: 72%  Mem: 654M│   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
│  PERFORMANCE METRICS                                         │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Avg Duration:    2.3s                                │   │
│  │ P95 Duration:   12.7s                                │   │
│  │ P99 Duration:   45.2s                                │   │
│  │ Throughput:     85 jobs/min                          │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
│  DEAD LETTER QUEUE                                           │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ ID        Type           Error         Attempts      │   │
│  │ abc-123   data_import    VALIDATION    3             │   │
│  │ def-456   report_gen     TIMEOUT        5             │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### 7.2 Metrics Collection

```typescript
// metrics-collector.ts
export class MetricsCollector {
  async collectMetrics(): Promise<JobMetrics> {
    const [queueDepths, workerStatus, performance, dlq] = await Promise.all([
      this.getQueueDepths(),
      this.getWorkerStatus(),
      this.getPerformanceMetrics(),
      this.getDeadLetterQueue(),
    ]);

    return {
      timestamp: new Date(),
      queueDepths,
      workerStatus,
      performance,
      dlq,
    };
  }

  private async getQueueDepths(): Promise<QueueDepths> {
    const [pending, active, failed, completed, dlq] = await Promise.all([
      redis.llen('queue:pending'),
      redis.llen('queue:active'),
      redis.llen('queue:failed'),
      redis.llen('queue:completed'),
      redis.llen('queue:dlq'),
    ]);

    return { pending, active, failed, completed, dlq };
  }

  private async getWorkerStatus(): Promise<WorkerStatus[]> {
    const workerIds = await redis.smembers('workers:active');

    return Promise.all(workerIds.map(async (workerId) => {
      const [heartbeat, jobs, stats] = await Promise.all([
        redis.get(`worker:${workerId}:heartbeat`),
        redis.smembers(`worker:${workerId}:jobs`),
        redis.hgetall(`worker:${workerId}:stats`),
      ]);

      return {
        workerId,
        alive: Date.now() - parseInt(heartbeat || '0') < 30000,
        activeJobs: jobs.length,
        stats,
      };
    }));
  }

  private async getPerformanceMetrics(): Promise<PerformanceMetrics> {
    const stats = await db.query(`
      SELECT
        COUNT(*) as total_jobs,
        AVG(EXTRACT(EPOCH FROM (completed_at - started_at)) * 1000) as avg_duration_ms,
        PERCENTILE_CONT(0.95) WITHIN GROUP (
          ORDER BY EXTRACT(EPOCH FROM (completed_at - started_at)) * 1000
        ) as p95_duration_ms,
        PERCENTILE_CONT(0.99) WITHIN GROUP (
          ORDER BY EXTRACT(EPOCH FROM (completed_at - started_at)) * 1000
        ) as p99_duration_ms,
        COUNT(*) FILTER (WHERE status = 'completed') as successful,
        COUNT(*) FILTER (WHERE status = 'failed') as failed
      FROM jobs
      WHERE created_at >= NOW() - INTERVAL '24 hours'
    `);

    return stats.rows[0];
  }

  private async getDeadLetterQueue(): Promise<DeadLetterJob[]> {
    const result = await db.query(`
      SELECT
        id,
        original_job_id,
        job_type,
        failure_reason,
        total_attempts,
        created_at
      FROM dead_letter_jobs
      WHERE status = 'pending'
      ORDER BY created_at DESC
      LIMIT 100
    `);

    return result.rows;
  }
}
```

### 7.3 Alert Configuration

```typescript
// alert-rules.ts
export const alertRules = [
  {
    name: 'high_queue_depth',
    condition: (metrics) => metrics.queueDepths.pending > 1000,
    severity: 'warning',
    message: 'Pending queue depth exceeds 1000 jobs',
    action: 'consider_scaling_workers',
  },
  {
    name: 'critical_queue_depth',
    condition: (metrics) => metrics.queueDepths.pending > 5000,
    severity: 'critical',
    message: 'Pending queue depth exceeds 5000 jobs',
    action: 'immediate_scaling_required',
  },
  {
    name: 'worker_down',
    condition: (metrics) => metrics.workerStatus.some(w => !w.alive),
    severity: 'critical',
    message: 'One or more workers are not responding',
    action: 'restart_worker',
  },
  {
    name: 'high_failure_rate',
    condition: (metrics) => {
      const total = metrics.performance.successful + metrics.performance.failed;
      return total > 100 && (metrics.performance.failed / total) > 0.1;
    },
    severity: 'warning',
    message: 'Job failure rate exceeds 10%',
    action: 'investigate_failures',
  },
  {
    name: 'dlq_accumulation',
    condition: (metrics) => metrics.queueDepths.dlq > 50,
    severity: 'warning',
    message: 'Dead letter queue has >50 jobs',
    action: 'review_dlq_jobs',
  },
  {
    name: 'slow_jobs',
    condition: (metrics) => metrics.performance.p95_duration_ms > 60000,
    severity: 'warning',
    message: 'P95 job duration exceeds 1 minute',
    action: 'optimize_job_handlers',
  },
];
```

---

## 8. Migration Plan

### 8.1 Migration Phases

```
┌─────────────────────────────────────────────────────────────┐
│                    MIGRATION ROADMAP                         │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  PHASE 1: Infrastructure Setup (Week 1)                     │
│  ├─ ✓ Update docker-compose.redis.yml                      │
│  ├─ ✓ Configure Redis for openspg-network                  │
│  ├─ ✓ Test Redis connectivity                              │
│  └─ ✓ Deploy Redis Commander                               │
│                                                               │
│  PHASE 2: Database Schema (Week 1)                          │
│  ├─ ✓ Create migration script                              │
│  ├─ ✓ Run migration on dev database                        │
│  ├─ ✓ Verify tables created correctly                      │
│  ├─ ✓ Test functions and triggers                          │
│  └─ ✓ Create indexes                                       │
│                                                               │
│  PHASE 3: Worker Development (Week 2)                       │
│  ├─ □ Implement base worker class                          │
│  ├─ □ Implement job handlers                               │
│  ├─ □ Implement error recovery                             │
│  ├─ □ Implement monitoring                                 │
│  └─ □ Write tests                                           │
│                                                               │
│  PHASE 4: API Integration (Week 2)                          │
│  ├─ □ Create job submission API                            │
│  ├─ □ Create job status API                                │
│  ├─ □ Create job cancellation API                          │
│  ├─ □ Create monitoring dashboard                          │
│  └─ □ Write API tests                                       │
│                                                               │
│  PHASE 5: Testing & Validation (Week 3)                     │
│  ├─ □ Unit tests                                            │
│  ├─ □ Integration tests                                     │
│  ├─ □ Load tests                                            │
│  ├─ □ Failure scenario tests                               │
│  └─ □ Performance benchmarks                                │
│                                                               │
│  PHASE 6: Deployment (Week 3-4)                             │
│  ├─ □ Deploy to staging                                     │
│  ├─ □ Smoke tests                                           │
│  ├─ □ Production deployment                                 │
│  ├─ □ Monitoring setup                                      │
│  └─ □ Documentation                                         │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### 8.2 Immediate Next Steps

1. **Update Redis Configuration**
   ```bash
   cd /home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney/web_interface

   # Update docker-compose.redis.yml (use updated version from section 4.1)

   # Start Redis
   docker-compose -f docker-compose.redis.yml up -d

   # Verify Redis is on openspg-network
   docker network inspect openspg-network
   ```

2. **Run Database Migration**
   ```bash
   # Apply migration
   docker exec -i aeon-postgres-dev psql -U postgres -d aeon_saas_dev < \
     /home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney/web_interface/scripts/migrations/001_gap006_job_tables.sql

   # Verify tables created
   docker exec aeon-postgres-dev psql -U postgres -d aeon_saas_dev -c "\dt job*"
   ```

3. **Create Worker Scaffold**
   ```bash
   mkdir -p workers/src/{core,handlers,services,config}

   # Initialize package.json
   cd workers
   npm init -y
   npm install --save typescript @types/node pg ioredis bull dotenv
   npm install --save-dev @types/pg @types/ioredis jest ts-jest
   ```

4. **Update Environment Configuration**
   ```bash
   # Add to .env
   cat >> .env << 'EOF'

   # GAP-006 Job Queue Configuration
   REDIS_HOST=aeon-redis
   REDIS_PORT=6379
   REDIS_PASSWORD=aeon_redis_dev

   WORKER_ENABLED=true
   WORKER_CONCURRENCY=5
   WORKER_POLL_INTERVAL=1000
   EOF
   ```

### 8.3 Validation Checklist

- [ ] Redis running on openspg-network
- [ ] Redis accessible from aeon-saas-dev
- [ ] PostgreSQL tables created successfully
- [ ] Functions and triggers working
- [ ] Indexes created
- [ ] Can insert test job record
- [ ] Can query ready jobs
- [ ] Worker scaffold created
- [ ] Worker can connect to Redis
- [ ] Worker can connect to PostgreSQL

---

## 9. Technology Evaluation

### 9.1 Redis vs Alternatives

| Feature | Redis | RabbitMQ | AWS SQS | Kafka |
|---------|-------|----------|---------|-------|
| **Simplicity** | ✓✓✓ | ✓✓ | ✓✓✓ | ✓ |
| **Performance** | ✓✓✓ | ✓✓ | ✓✓ | ✓✓✓ |
| **Persistence** | ✓✓ | ✓✓✓ | ✓✓✓ | ✓✓✓ |
| **Existing Use** | ✓✓✓ | ✗ | ✗ | ✗ |
| **Infrastructure** | Minimal | Heavy | Cloud-only | Heavy |
| **Learning Curve** | Low | Medium | Low | High |

**Decision: Redis** - Already planned for use, simple, performant, fits requirements.

### 9.2 PostgreSQL Job Storage vs Alternatives

| Feature | PostgreSQL | MongoDB | DynamoDB | Separate Queue DB |
|---------|-----------|---------|----------|-------------------|
| **Existing Use** | ✓✓✓ | ✗ | ✗ | ✗ |
| **ACID** | ✓✓✓ | ✓ | ✓✓ | ✓✓ |
| **Query Power** | ✓✓✓ | ✓✓ | ✓ | ✓✓ |
| **Infrastructure** | Minimal | New service | Cloud-only | New service |
| **Operational Overhead** | Low | Medium | Low | High |

**Decision: PostgreSQL** - Use existing database, avoid operational complexity.

---

## 10. Risks & Mitigation

### 10.1 Risk Matrix

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| **Redis failure** | Low | High | Persistence enabled, regular backups, monitor health |
| **Database bottleneck** | Medium | Medium | Index optimization, connection pooling, read replicas |
| **Worker crashes** | Medium | Low | Auto-restart, health checks, monitoring alerts |
| **Job duplication** | Low | Medium | Redis locks, PostgreSQL constraints, idempotent handlers |
| **DLQ accumulation** | Medium | Low | Regular DLQ review, automated triage, alerts |
| **Memory leaks** | Low | High | Resource limits, monitoring, auto-restart on threshold |

### 10.2 Disaster Recovery

**Backup Strategy:**
- PostgreSQL: Daily full backups, continuous WAL archiving
- Redis: AOF persistence, daily RDB snapshots
- Job data: Retained for 30 days, then archived to S3

**Recovery Procedures:**
1. **Redis failure**: Restart from AOF, workers resume polling
2. **Database failure**: Restore from backup, replay Redis queue
3. **Worker failure**: Auto-restart, jobs return to queue after timeout
4. **Complete system failure**: Restore database, restore Redis, restart workers

---

## 11. Performance Targets

### 11.1 Service Level Objectives (SLOs)

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Job submission latency** | < 100ms P95 | API response time |
| **Job execution start** | < 5s P95 | Time from submit to start |
| **Job completion rate** | > 95% | Successful / Total |
| **Worker uptime** | > 99.5% | Heartbeat monitoring |
| **DLQ rate** | < 1% | DLQ jobs / Total jobs |
| **System throughput** | > 100 jobs/min | Completed jobs per minute |

### 11.2 Capacity Planning

**Current Scale:**
- Expected job volume: 1,000 - 10,000 jobs/day
- Peak throughput: 50-100 jobs/minute
- Workers: 2-5 general workers, 1-2 specialized

**Growth Plan:**
- 6 months: 50,000 jobs/day → add 3-5 workers
- 12 months: 100,000 jobs/day → add 10-15 workers, consider sharding

---

## 12. Architecture Decision Records

### ADR-001: Use Redis for Job Queue

**Context:** Need distributed job queue with minimal operational overhead.

**Decision:** Use Redis with BRPOPLPUSH pattern.

**Rationale:**
- Already planned for AEON infrastructure
- Simple, well-understood
- Excellent performance for our scale
- Built-in persistence options
- Strong community support

**Consequences:**
- Positive: Simple architecture, easy to operate
- Negative: Not as feature-rich as specialized queue systems
- Mitigation: Custom logic for advanced features (scheduling, dependencies)

### ADR-002: Extend Existing PostgreSQL Database

**Context:** Need persistent job storage.

**Decision:** Add job tables to existing aeon_saas_dev database.

**Rationale:**
- Reduce operational complexity
- Leverage existing backups and monitoring
- Simplify database access for Next.js app
- Avoid data duplication

**Consequences:**
- Positive: Simpler architecture, easier operations
- Negative: Potential database load increase
- Mitigation: Proper indexing, connection pooling, monitoring

### ADR-003: Node.js Workers

**Context:** Need worker processes to execute jobs.

**Decision:** Implement workers in Node.js/TypeScript.

**Rationale:**
- Consistency with Next.js frontend
- Share code between API and workers
- Strong ecosystem for job processing
- Team familiarity

**Consequences:**
- Positive: Code reuse, easier debugging
- Negative: Not ideal for CPU-intensive jobs
- Mitigation: Offload heavy computation to specialized workers or services

---

## Appendix A: File Locations

```
/home/jim/2_OXOT_Projects_Dev/
├── docs/
│   └── GAP-006_ARCHITECTURE_DESIGN_2025-11-15.md (THIS FILE)
│
└── Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney/web_interface/
    ├── docker-compose.dev.yml (EXISTING - No changes)
    ├── docker-compose.redis.yml (UPDATE - Use openspg-network)
    ├── docker-compose.workers.yml (NEW - Worker deployment)
    │
    ├── config/
    │   └── redis.conf (NEW - Redis configuration)
    │
    ├── scripts/
    │   └── migrations/
    │       └── 001_gap006_job_tables.sql (NEW - Database schema)
    │
    └── workers/
        ├── Dockerfile (NEW)
        ├── package.json (NEW)
        ├── tsconfig.json (NEW)
        └── src/
            ├── index.ts
            ├── core/
            │   ├── worker.ts
            │   ├── job-executor.ts
            │   ├── error-handler.ts
            │   └── health-monitor.ts
            ├── handlers/
            │   ├── base-handler.ts
            │   └── index.ts
            ├── services/
            │   ├── postgres.ts
            │   ├── redis.ts
            │   └── metrics.ts
            └── config/
                ├── worker-config.ts
                └── retry-config.ts
```

---

## Appendix B: Glossary

- **DLQ (Dead Letter Queue)**: Queue for jobs that failed permanently after all retry attempts
- **BRPOPLPUSH**: Redis command for atomically moving items between lists (blocking right pop, left push)
- **Idempotent**: Operation that can be applied multiple times without changing result
- **Exponential Backoff**: Retry strategy where delay increases exponentially with each attempt
- **Job Dependency**: Relationship where one job must complete before another can start
- **Worker Pool**: Collection of worker processes polling from shared queue
- **Heartbeat**: Periodic signal indicating worker is alive and healthy

---

**END OF DOCUMENT**

---

**Next Steps:**
1. Review architecture with stakeholders
2. Begin Phase 1: Infrastructure setup
3. Create detailed implementation tickets
4. Set up monitoring and alerting
5. Begin worker development

**Questions/Feedback:** Contact system architect or open GitHub issue in project repository.