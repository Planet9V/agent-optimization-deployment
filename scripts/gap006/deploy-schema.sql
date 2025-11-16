-- GAP-006 Database Schema Deployment
-- File: deploy-schema.sql
-- Purpose: Create 5 job management tables in aeon_saas_dev
-- Database: aeon_saas_dev (EXTENDS existing database)
-- Created: 2025-11-16
-- Status: PRODUCTION READY

-- ======================================
-- Table 1: jobs - Core job storage
-- ======================================
CREATE TABLE IF NOT EXISTS jobs (
    job_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_type VARCHAR(100) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'PENDING',
    priority INTEGER DEFAULT 3 CHECK (priority BETWEEN 1 AND 5),
    payload JSONB NOT NULL,
    result JSONB,
    retry_count INTEGER DEFAULT 0,
    max_retries INTEGER DEFAULT 3,
    worker_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    scheduled_at TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    error_message TEXT,
    metadata JSONB DEFAULT '{}'::jsonb
);

-- Indexes for jobs table
CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(status);
CREATE INDEX IF NOT EXISTS idx_jobs_priority ON jobs(priority DESC, created_at ASC);
CREATE INDEX IF NOT EXISTS idx_jobs_scheduled ON jobs(scheduled_at) WHERE scheduled_at IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_jobs_type_status ON jobs(job_type, status);
CREATE INDEX IF NOT EXISTS idx_jobs_worker ON jobs(worker_id) WHERE worker_id IS NOT NULL;

-- ======================================
-- Table 2: workers - Worker registry
-- ======================================
CREATE TABLE IF NOT EXISTS workers (
    worker_id VARCHAR(100) PRIMARY KEY,
    worker_name VARCHAR(200) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'ACTIVE',
    capacity INTEGER DEFAULT 5,
    current_load INTEGER DEFAULT 0,
    health_score DECIMAL(3,2) DEFAULT 1.00,
    last_heartbeat TIMESTAMP DEFAULT NOW(),
    started_at TIMESTAMP DEFAULT NOW(),
    metadata JSONB DEFAULT '{}'::jsonb
);

-- Indexes for workers table
CREATE INDEX IF NOT EXISTS idx_workers_status ON workers(status);
CREATE INDEX IF NOT EXISTS idx_workers_heartbeat ON workers(last_heartbeat);
CREATE INDEX IF NOT EXISTS idx_workers_health ON workers(health_score DESC);

-- ======================================
-- Table 3: worker_health_logs - Health tracking
-- ======================================
CREATE TABLE IF NOT EXISTS worker_health_logs (
    log_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    worker_id VARCHAR(100) NOT NULL,
    metric_type VARCHAR(50) NOT NULL,
    metric_value DECIMAL(10,4) NOT NULL,
    metadata JSONB,
    logged_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for worker_health_logs
CREATE INDEX IF NOT EXISTS idx_health_logs_worker ON worker_health_logs(worker_id, logged_at DESC);
CREATE INDEX IF NOT EXISTS idx_health_logs_metric ON worker_health_logs(metric_type);

-- Foreign key constraint
ALTER TABLE worker_health_logs
    DROP CONSTRAINT IF EXISTS fk_health_worker;
ALTER TABLE worker_health_logs
    ADD CONSTRAINT fk_health_worker
    FOREIGN KEY (worker_id) REFERENCES workers(worker_id) ON DELETE CASCADE;

-- ======================================
-- Table 4: state_snapshots - State persistence
-- ======================================
CREATE TABLE IF NOT EXISTS state_snapshots (
    snapshot_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    snapshot_type VARCHAR(50) NOT NULL,
    state_data JSONB NOT NULL,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP
);

-- Indexes for state_snapshots
CREATE INDEX IF NOT EXISTS idx_snapshots_type ON state_snapshots(snapshot_type);
CREATE INDEX IF NOT EXISTS idx_snapshots_created ON state_snapshots(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_snapshots_expires ON state_snapshots(expires_at) WHERE expires_at IS NOT NULL;

-- ======================================
-- Table 5: job_dependencies - Job relationships
-- ======================================
CREATE TABLE IF NOT EXISTS job_dependencies (
    dependency_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_id UUID NOT NULL,
    depends_on_job_id UUID NOT NULL,
    dependency_type VARCHAR(50) DEFAULT 'sequential',
    created_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT unique_dependency UNIQUE(job_id, depends_on_job_id)
);

-- Indexes for job_dependencies
CREATE INDEX IF NOT EXISTS idx_dependencies_job ON job_dependencies(job_id);
CREATE INDEX IF NOT EXISTS idx_dependencies_depends_on ON job_dependencies(depends_on_job_id);

-- Foreign key constraints
ALTER TABLE job_dependencies
    DROP CONSTRAINT IF EXISTS fk_dependency_job;
ALTER TABLE job_dependencies
    ADD CONSTRAINT fk_dependency_job
    FOREIGN KEY (job_id) REFERENCES jobs(job_id) ON DELETE CASCADE;

ALTER TABLE job_dependencies
    DROP CONSTRAINT IF EXISTS fk_dependency_depends_on;
ALTER TABLE job_dependencies
    ADD CONSTRAINT fk_dependency_depends_on
    FOREIGN KEY (depends_on_job_id) REFERENCES jobs(job_id) ON DELETE CASCADE;

-- ======================================
-- Grant permissions
-- ======================================
GRANT SELECT, INSERT, UPDATE, DELETE ON jobs TO postgres;
GRANT SELECT, INSERT, UPDATE, DELETE ON workers TO postgres;
GRANT SELECT, INSERT, UPDATE, DELETE ON worker_health_logs TO postgres;
GRANT SELECT, INSERT, UPDATE, DELETE ON state_snapshots TO postgres;
GRANT SELECT, INSERT, UPDATE, DELETE ON job_dependencies TO postgres;

-- ======================================
-- Verification queries
-- ======================================
-- Verify tables created
SELECT table_name FROM information_schema.tables
WHERE table_schema = 'public'
AND table_name IN ('jobs', 'workers', 'worker_health_logs', 'state_snapshots', 'job_dependencies')
ORDER BY table_name;

-- Verify indexes created
SELECT tablename, indexname FROM pg_indexes
WHERE schemaname = 'public'
AND tablename IN ('jobs', 'workers', 'worker_health_logs', 'state_snapshots', 'job_dependencies')
ORDER BY tablename, indexname;
