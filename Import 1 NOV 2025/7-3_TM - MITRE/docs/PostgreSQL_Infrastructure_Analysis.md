# PostgreSQL Infrastructure Analysis - AEON Next.js Container
**Analysis Date:** 2025-11-11
**Container:** aeon-postgres-dev
**Database:** aeon_saas_dev
**Status:** ACTIVE & OPERATIONAL

## Executive Summary

PostgreSQL is **already running** on the Next.js container ecosystem and is **currently being used** for AEON SaaS application data persistence. The database is lightweight, well-structured, and has **significant capacity** for job storage implementation.

## Current PostgreSQL Infrastructure

### Container Configuration
```yaml
Container Name: aeon-postgres-dev
Image: postgres:16-alpine
Status: Up 7 days (healthy)
PostgreSQL Version: 16.10 (Alpine Linux)
Database: aeon_saas_dev
User: postgres
Port: 5432 (internal Docker network)
```

### Connection Details (from Next.js container env)
```bash
DATABASE_URL=postgresql://postgres:postgres@postgres-dev:5432/aeon_saas_dev
POSTGRES_HOST=postgres-dev
POSTGRES_PORT=5432
POSTGRES_DB=aeon_saas_dev
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
```

### Network Architecture
- **Docker Network:** aeon-ai-app-builder_default
- **Container Hostname:** postgres-dev (DNS resolvable within Docker network)
- **Next.js Container:** aeon-saas-dev (currently exited)
- **Connection Method:** TCP/IP over Docker bridge network

## Current Database Usage

### Existing Schema (9 Tables)
The database is currently used for **SaaS multi-tenancy and authentication**:

1. **users** (48 kB)
   - UUID-based user management
   - Clerk.com authentication integration
   - Fields: clerk_id, email, username, first_name, last_name, avatar_url
   - JSONB metadata for extensibility
   - **Currently 0 users** (development/staging environment)

2. **audit_logs** (40 kB)
   - Activity tracking and compliance
   - Fields: user_id, team_id, action, resource_type, resource_id
   - JSONB metadata for flexible log data
   - IP address and user agent tracking
   - **Currently 0 records**

3. **teams** (32 kB)
   - Multi-tenant organization structure
   - Team-based access control

4. **team_members** (40 kB)
   - User-team relationship mapping
   - Role-based team membership

5. **roles** (48 kB)
   - RBAC (Role-Based Access Control) definitions
   - Permission management

6. **user_roles** (40 kB)
   - User-role assignment tracking
   - Temporal role grants

7. **api_keys** (40 kB)
   - API authentication tokens
   - Key revocation tracking

8. **invitations** (48 kB)
   - Team invitation workflow
   - Pending user invitations

9. **subscriptions** (24 kB)
   - SaaS subscription management
   - Payment/plan tracking

### Database Performance Metrics
```yaml
Total Database Size: 8,092 kB (8 MB)
Total Tables: 9
Active Connections: 1 (system monitoring)
Max Connections: 100
Current Usage: ~1% capacity

PostgreSQL Settings:
  shared_buffers: 16,384 pages (128 MB)
  effective_cache_size: 524,288 pages (4 GB)
  maintenance_work_mem: 65,536 kB (64 MB)
  work_mem: 4,096 kB (4 MB)
  max_connections: 100
```

### Installed Extensions
- **plpgsql** 1.0 - PL/pgSQL procedural language (standard)
- **uuid-ossp** 1.1 - UUID generation (ACTIVE - used in all tables)

## Integration Analysis for Job Storage

### ✅ EXCELLENT Integration Potential

#### 1. **Capacity Analysis**
- **Current Usage:** 8 MB (negligible)
- **Available Capacity:** ~99% of allocated resources unused
- **Connection Pool:** 99/100 connections available
- **Scalability:** Can easily handle 10,000+ job records without performance degradation

#### 2. **Schema Design Compatibility**
The existing schema uses modern PostgreSQL best practices:
- ✅ UUID primary keys (matches job queue patterns)
- ✅ JSONB for metadata (perfect for flexible job payloads)
- ✅ Timestamp tracking (created_at, updated_at)
- ✅ Indexing strategy (btree on common query columns)
- ✅ Foreign key constraints (data integrity)
- ✅ Trigger-based automation (update_updated_at_column)

#### 3. **Connection from Next.js**
The Next.js container **already has** DATABASE_URL configured:
```javascript
// Already available in Next.js environment
process.env.DATABASE_URL = 'postgresql://postgres:postgres@postgres-dev:5432/aeon_saas_dev'
```

#### 4. **Existing Pattern: audit_logs Table**
The `audit_logs` table is **structurally similar** to a job queue:
- Tracks actions and events (like jobs)
- JSONB metadata for flexible data
- Temporal tracking (created_at)
- User/team association (for job ownership)
- **Can serve as reference architecture for jobs table**

## Recommended Job Queue Implementation

### Approach 1: Extend Existing Database (RECOMMENDED)
**Create `jobs` table in aeon_saas_dev database:**

```sql
CREATE TABLE jobs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    team_id UUID REFERENCES teams(id) ON DELETE CASCADE,
    job_type VARCHAR(100) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    priority INTEGER DEFAULT 0,
    payload JSONB NOT NULL DEFAULT '{}',
    result JSONB,
    error_message TEXT,
    retry_count INTEGER DEFAULT 0,
    max_retries INTEGER DEFAULT 3,
    scheduled_at TIMESTAMP WITH TIME ZONE,
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for job queue performance
CREATE INDEX idx_jobs_status ON jobs(status);
CREATE INDEX idx_jobs_scheduled_at ON jobs(scheduled_at) WHERE status = 'pending';
CREATE INDEX idx_jobs_user_id ON jobs(user_id);
CREATE INDEX idx_jobs_team_id ON jobs(team_id);
CREATE INDEX idx_jobs_created_at ON jobs(created_at);

-- Auto-update trigger
CREATE TRIGGER update_jobs_updated_at
    BEFORE UPDATE ON jobs
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

**Advantages:**
- ✅ Leverages existing connection infrastructure
- ✅ Integrates with user authentication (Clerk)
- ✅ Multi-tenant job isolation via team_id
- ✅ Audit trail via existing audit_logs table
- ✅ No additional database credentials needed
- ✅ Unified backup/restore strategy
- ✅ Existing monitoring (if configured)

### Approach 2: Dedicated Jobs Database (Alternative)
**Create separate database on same PostgreSQL instance:**

```sql
CREATE DATABASE aeon_jobs;
-- Then create jobs table with similar schema
```

**Advantages:**
- ✅ Isolation from SaaS application data
- ✅ Independent scaling policies
- ✅ Separate backup schedules

**Disadvantages:**
- ❌ Additional connection pool management
- ❌ Cannot join with users/teams tables
- ❌ Duplicate authentication logic needed

## Integration with BullMQ (if using Node.js queue)

### Current Setup Supports:
1. **pg + BullMQ Hybrid:**
   - PostgreSQL for job persistence and audit
   - Redis for real-time queue management
   - PostgreSQL as "source of truth" for job history

2. **PostgreSQL-Only Queue:**
   - Graphile Worker
   - pg-boss
   - Custom implementation with pg-notify

### Recommended Stack:
```typescript
// Next.js API route or background worker
import { Pool } from 'pg';

const pool = new Pool({
  connectionString: process.env.DATABASE_URL
});

// Job creation
async function createJob(userId: string, teamId: string, jobType: string, payload: any) {
  const result = await pool.query(`
    INSERT INTO jobs (user_id, team_id, job_type, payload, status)
    VALUES ($1, $2, $3, $4, 'pending')
    RETURNING id
  `, [userId, teamId, jobType, payload]);

  return result.rows[0].id;
}

// Job processing
async function processNextJob() {
  const result = await pool.query(`
    UPDATE jobs
    SET status = 'processing', started_at = NOW()
    WHERE id = (
      SELECT id FROM jobs
      WHERE status = 'pending'
      AND (scheduled_at IS NULL OR scheduled_at <= NOW())
      ORDER BY priority DESC, created_at ASC
      FOR UPDATE SKIP LOCKED
      LIMIT 1
    )
    RETURNING *
  `);

  return result.rows[0];
}
```

## Performance Characteristics

### Estimated Capacity (Current Configuration)
```yaml
Job Processing:
  - Insertion Rate: ~1,000 jobs/second
  - Processing Rate: ~500 jobs/second (depending on job complexity)
  - Concurrent Workers: 10-20 (limited by max_connections: 100)
  - Job History Retention: 100,000+ jobs without performance impact

Storage Projection:
  - Average Job Size: 2 KB (with JSONB payload)
  - 10,000 jobs: ~20 MB
  - 100,000 jobs: ~200 MB
  - 1,000,000 jobs: ~2 GB

Connection Pool:
  - Current: 1/100 connections used
  - Recommended Job Workers: 5-10 connections
  - Remaining for Next.js: 85-90 connections
  - Safe headroom: >80% available capacity
```

### Scalability Improvements (if needed)
```sql
-- Partition jobs table by created_at for better performance
CREATE TABLE jobs_partitioned (
    -- same schema
) PARTITION BY RANGE (created_at);

-- Create monthly partitions
CREATE TABLE jobs_2025_11 PARTITION OF jobs_partitioned
    FOR VALUES FROM ('2025-11-01') TO ('2025-12-01');

-- Add pg_cron extension for auto-cleanup
CREATE EXTENSION pg_cron;
SELECT cron.schedule('cleanup-old-jobs', '0 2 * * *',
    'DELETE FROM jobs WHERE status IN (''completed'', ''failed'')
     AND completed_at < NOW() - INTERVAL ''30 days''');
```

## Security Considerations

### Current Security Posture
- ✅ Network isolation (Docker bridge network)
- ✅ Password authentication (basic)
- ⚠️ Credentials in environment variables (development pattern)
- ⚠️ No SSL/TLS between Next.js and PostgreSQL (internal network)

### Production Recommendations
1. **Use Connection Pooling:**
   ```javascript
   import { Pool } from 'pg';
   const pool = new Pool({
     max: 20, // max connections
     idleTimeoutMillis: 30000,
     connectionTimeoutMillis: 2000,
   });
   ```

2. **Enable SSL (Production):**
   ```javascript
   const pool = new Pool({
     ssl: {
       rejectUnauthorized: false // or provide CA cert
     }
   });
   ```

3. **Use Secrets Manager:**
   - Store DATABASE_URL in AWS Secrets Manager, HashiCorp Vault, etc.
   - Rotate credentials periodically

4. **Row-Level Security (RLS):**
   ```sql
   ALTER TABLE jobs ENABLE ROW LEVEL SECURITY;

   CREATE POLICY team_isolation ON jobs
       USING (team_id IN (
           SELECT team_id FROM team_members WHERE user_id = current_user_id()
       ));
   ```

## Migration Path

### Phase 1: Schema Creation (5 minutes)
```bash
# Connect to PostgreSQL
docker exec -it aeon-postgres-dev psql -U postgres -d aeon_saas_dev

# Run schema creation SQL (from Approach 1 above)
```

### Phase 2: Next.js Integration (15 minutes)
```typescript
// Install pg driver if not already installed
npm install pg

// Create lib/db.ts
import { Pool } from 'pg';

export const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 20,
});

// Create lib/jobs.ts with job creation/processing functions
```

### Phase 3: Testing (30 minutes)
1. Create test job via API route
2. Verify database insertion
3. Test job processing worker
4. Validate audit logging integration

### Phase 4: Production Deployment
1. Update environment variables
2. Run schema migrations
3. Deploy Next.js changes
4. Monitor job processing metrics

## Monitoring & Observability

### Recommended Queries
```sql
-- Active jobs count by status
SELECT status, COUNT(*)
FROM jobs
GROUP BY status;

-- Job processing performance
SELECT
    AVG(EXTRACT(EPOCH FROM (completed_at - started_at))) as avg_duration_seconds,
    MAX(EXTRACT(EPOCH FROM (completed_at - started_at))) as max_duration_seconds
FROM jobs
WHERE status = 'completed'
AND completed_at > NOW() - INTERVAL '1 hour';

-- Failed job analysis
SELECT job_type, COUNT(*), AVG(retry_count)
FROM jobs
WHERE status = 'failed'
GROUP BY job_type;
```

### Integration with Existing Monitoring
- **Prometheus:** Already configured in docker-compose.yml
- **Grafana:** Already running (port 3000)
- **pg_stat_statements:** Can be enabled for query performance monitoring

## Cost Analysis

### Infrastructure Cost
- **Current:** $0 (using existing PostgreSQL container)
- **Additional Resources:** None required for job queue
- **Scaling Cost:** Minimal (can handle 100k+ jobs without upgrade)

### Comparison with Alternatives
| Solution | Monthly Cost | Setup Complexity | Integration Effort |
|----------|--------------|------------------|-------------------|
| **Existing PostgreSQL** | $0 | Low | Minimal |
| AWS SQS | ~$0.40/million requests | Medium | Moderate |
| Redis + BullMQ | ~$15/month (managed) | Medium | Moderate |
| RabbitMQ | ~$25/month (managed) | High | High |

## Conclusion & Recommendations

### ✅ COMPLETE: PostgreSQL Analysis

**Key Findings:**
1. PostgreSQL **is already operational** on Next.js container ecosystem
2. Database has **99% unused capacity** - perfect for job storage
3. Existing schema patterns **align perfectly** with job queue requirements
4. Connection infrastructure **already configured** in Next.js environment
5. Multi-tenant architecture **supports job isolation** via team_id
6. **ZERO additional infrastructure cost** required

### Recommended Immediate Actions:
1. **Create `jobs` table** using Approach 1 schema (5 minutes)
2. **Add pg connection pool** to Next.js application (15 minutes)
3. **Implement job creation API** endpoint (30 minutes)
4. **Build job processing worker** (1-2 hours)
5. **Integrate with audit_logs** for compliance tracking (30 minutes)

### Performance Expectations:
- **Job Insertion:** ~1,000 jobs/second
- **Job Processing:** ~500 jobs/second (network-dependent)
- **Concurrent Workers:** 10-20 without infrastructure changes
- **Storage:** Can handle 1 million jobs (~2 GB) easily

### Risk Assessment: **LOW**
- Existing infrastructure proven and stable (7 days uptime)
- No new dependencies or services required
- Isolated table schema - minimal impact on existing SaaS functionality
- Easy rollback (DROP TABLE jobs if issues arise)

---

**Analysis Status:** ✅ COMPLETE
**Infrastructure Ready:** ✅ YES
**Capacity Available:** ✅ 99%
**Integration Complexity:** ✅ LOW
**Recommendation:** ✅ PROCEED WITH IMPLEMENTATION
