# MySQL Database - OpenSPG Container

**File:** MySQL-Database.md
**Created:** 2025-11-03 17:11:58 CST
**Modified:** 2025-11-03 17:11:58 CST
**Version:** v1.0.0
**Author:** AEON FORGE System
**Purpose:** Professional API documentation for MySQL database container in OpenSPG stack
**Status:** ACTIVE

**Tags:** #mysql #database #relational #openspg #mariadb #container
**Backlinks:** [[Docker-Architecture]] [[OpenSPG-Server]] [[AEON-UI]]

---

## Executive Summary

The OpenSPG MySQL container provides relational database services for the OpenSPG knowledge graph platform. Running MariaDB 10.5.8, it manages metadata, configuration, ontology definitions, and application state for the entire knowledge graph ecosystem.

**Current System State:**
- **System Time:** 2025-11-03 17:11:58 CST
- **Container:** openspg-mysql (Healthy)
- **Database Version:** MariaDB 10.5.8
- **Port:** 3306 (Internal: 172.18.0.3)
- **Network:** spg-network
- **Status:** Operational

---

## Table of Contents

1. [Container Information](#container-information)
2. [Database Architecture](#database-architecture)
3. [Connection Configuration](#connection-configuration)
4. [Schema Overview](#schema-overview)
5. [Common Operations](#common-operations)
6. [Backup and Restore](#backup-and-restore)
7. [Performance Tuning](#performance-tuning)
8. [Integration Points](#integration-points)
9. [Troubleshooting](#troubleshooting)
10. [References](#references)

---

## Container Information

### Container Details
```yaml
container_name: openspg-mysql
image: spg-registry.cn-hangzhou.cr.aliyuncs.com/spg/openspg-mysql:latest
version: MariaDB 10.5.8
status: Healthy
network: spg-network
internal_ip: 172.18.0.3
exposed_port: 3306
```

### Database Version
```sql
-- Version Information
MariaDB: 10.5.8-MariaDB-1:10.5.8+maria~focal
Platform: Ubuntu Focal (20.04)
Architecture: x86_64
```

### Health Check
```bash
# Container health status
docker inspect openspg-mysql --format='{{.State.Health.Status}}'
# Output: healthy

# Database connectivity test
docker exec openspg-mysql mysqladmin -uroot -popenspg ping
# Output: mysqld is alive
```

---

## Database Architecture

### Available Databases
```
information_schema  # System metadata
mysql               # User authentication and privileges
openspg             # Main application database
performance_schema  # Performance monitoring
```

### OpenSPG Database Schema

The `openspg` database contains **33 tables** organized into functional domains:

#### 1. Knowledge Graph Core (kg_*)
```
kg_app                    # Application configurations
kg_biz_domain             # Business domain definitions
kg_builder_job            # Knowledge graph construction jobs
kg_config                 # System configuration
kg_data_source            # External data sources
kg_ontology_entity        # Entity type definitions
kg_ontology_property_*    # Property and constraint definitions
kg_project_entity         # Project-specific entities
kg_project_info           # Project metadata
```

#### 2. Semantic and Reasoning (kg_semantic_*, kg_reason_*)
```
kg_semantic_rule          # Semantic reasoning rules
kg_reason_session         # Reasoning session tracking
kg_reason_task            # Reasoning task management
kg_reason_tutorial        # Reasoning tutorials
kg_ontology_semantic      # Semantic type definitions
```

#### 3. Scheduling and Jobs (kg_scheduler_*)
```
kg_scheduler_info         # Scheduler configuration
kg_scheduler_instance     # Running scheduler instances
kg_scheduler_job          # Scheduled job definitions
kg_scheduler_task         # Task execution records
```

#### 4. User Management and Security
```
kg_user                   # User accounts
kg_role                   # Role definitions
kg_resource_permission    # Resource access control
kg_user_model             # User model associations
```

#### 5. AI/ML Integration
```
kg_model_detail           # Model configurations
kg_model_provider         # Model provider settings
kg_provider_param         # Provider-specific parameters
kg_retrieval              # Retrieval configurations
kg_feedback               # User feedback data
```

#### 6. System Management
```
kg_sys_lock               # Distributed locks
kg_statistics             # System statistics
kg_ref                    # Reference data
kg_ontology_ext           # Ontology extensions
kg_ontology_release       # Version management
```

### Table Sizes (Top 10)
```
kg_ontology_entity_property_range    0.11 MB
kg_scheduler_task                     0.09 MB
kg_retrieval                          0.08 MB
kg_ontology_entity                    0.08 MB
kg_scheduler_instance                 0.06 MB
kg_reason_task                        0.06 MB
kg_user                               0.06 MB
kg_project_entity                     0.06 MB
kg_builder_job                        0.05 MB
kg_resource_permission                0.05 MB
```

**Total Database Size:** ~0.70 MB (current state)

---

## Connection Configuration

### Internal Connection (Docker Network)
```bash
# From other containers on spg-network
Host: openspg-mysql
Port: 3306
User: root
Password: openspg
Database: openspg
```

### Connection String Examples

#### MySQL CLI
```bash
# From host system
docker exec -it openspg-mysql mysql -uroot -popenspg openspg

# From within container
mysql -h openspg-mysql -P 3306 -u root -popenspg openspg
```

#### JDBC Connection
```java
String url = "jdbc:mysql://openspg-mysql:3306/openspg?useSSL=false&serverTimezone=UTC";
String user = "root";
String password = "openspg";

Connection conn = DriverManager.getConnection(url, user, password);
```

#### Python (PyMySQL)
```python
import pymysql

connection = pymysql.connect(
    host='openspg-mysql',
    port=3306,
    user='root',
    password='openspg',
    database='openspg',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)
```

#### Node.js (mysql2)
```javascript
const mysql = require('mysql2');

const connection = mysql.createConnection({
  host: 'openspg-mysql',
  port: 3306,
  user: 'root',
  password: 'openspg',
  database: 'openspg'
});
```

#### SQLAlchemy (Python)
```python
from sqlalchemy import create_engine

engine = create_engine(
    'mysql+pymysql://root:openspg@openspg-mysql:3306/openspg',
    pool_pre_ping=True,
    pool_recycle=3600
)
```

---

## Common Operations

### Database Management

#### List All Databases
```sql
SHOW DATABASES;
```

#### Use OpenSPG Database
```sql
USE openspg;
```

#### List Tables
```sql
SHOW TABLES;
```

#### Table Structure
```sql
DESCRIBE kg_ontology_entity;
-- or
SHOW CREATE TABLE kg_ontology_entity;
```

### Query Examples

#### Get All Projects
```sql
SELECT * FROM kg_project_info;
```

#### List Ontology Entities
```sql
SELECT id, name, type, create_time
FROM kg_ontology_entity
ORDER BY create_time DESC;
```

#### Check Scheduler Jobs
```sql
SELECT job_id, job_name, status, create_time
FROM kg_scheduler_job
WHERE status = 'RUNNING';
```

#### User and Role Information
```sql
SELECT u.id, u.username, r.role_name
FROM kg_user u
LEFT JOIN kg_role r ON u.role_id = r.id;
```

#### Model Provider Configuration
```sql
SELECT provider_name, model_type, status
FROM kg_model_provider
WHERE status = 'ACTIVE';
```

### Data Manipulation

#### Insert Project
```sql
INSERT INTO kg_project_info (name, description, create_time)
VALUES ('MyProject', 'Project description', NOW());
```

#### Update Configuration
```sql
UPDATE kg_config
SET config_value = 'new_value'
WHERE config_key = 'system.setting';
```

#### Delete Completed Jobs
```sql
DELETE FROM kg_builder_job
WHERE status = 'COMPLETED'
AND create_time < DATE_SUB(NOW(), INTERVAL 30 DAY);
```

---

## Backup and Restore

### Full Database Backup

#### Backup to File
```bash
# Backup openspg database
docker exec openspg-mysql mysqldump \
  -uroot -popenspg openspg \
  > openspg_backup_$(date +%Y%m%d_%H%M%S).sql

# Backup with gzip compression
docker exec openspg-mysql mysqldump \
  -uroot -popenspg openspg \
  | gzip > openspg_backup_$(date +%Y%m%d_%H%M%S).sql.gz
```

#### Backup All Databases
```bash
docker exec openspg-mysql mysqldump \
  -uroot -popenspg --all-databases \
  > all_databases_backup_$(date +%Y%m%d_%H%M%S).sql
```

### Restore from Backup

#### Restore Single Database
```bash
# From uncompressed backup
docker exec -i openspg-mysql mysql \
  -uroot -popenspg openspg \
  < openspg_backup_20251103_171158.sql

# From compressed backup
gunzip < openspg_backup_20251103_171158.sql.gz \
  | docker exec -i openspg-mysql mysql -uroot -popenspg openspg
```

### Automated Backup Script

```bash
#!/bin/bash
# backup_mysql.sh - Automated MySQL backup script

BACKUP_DIR="/home/jim/backups/mysql"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=7

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Perform backup
docker exec openspg-mysql mysqldump \
  -uroot -popenspg openspg \
  | gzip > "$BACKUP_DIR/openspg_$TIMESTAMP.sql.gz"

# Delete old backups
find "$BACKUP_DIR" -name "openspg_*.sql.gz" \
  -type f -mtime +$RETENTION_DAYS -delete

echo "Backup completed: openspg_$TIMESTAMP.sql.gz"
```

### Schedule with Cron
```bash
# Add to crontab
# Backup daily at 2 AM
0 2 * * * /home/jim/scripts/backup_mysql.sh
```

---

## Performance Tuning

### Current Configuration

#### Connection Settings
```sql
-- Maximum concurrent connections
SHOW VARIABLES LIKE 'max_connections';
-- Value: 1000
```

#### Buffer Pool Configuration
```sql
-- InnoDB buffer pool size
SHOW VARIABLES LIKE 'innodb_buffer_pool_size';
-- Value: 2147483648 (2 GB)
```

### Performance Optimization

#### Query Performance Analysis
```sql
-- Enable slow query log
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 2;

-- Check slow queries
SELECT * FROM mysql.slow_log
ORDER BY start_time DESC
LIMIT 10;
```

#### Index Analysis
```sql
-- Check missing indexes
SELECT
  table_schema,
  table_name,
  ROUND(((data_length + index_length) / 1024 / 1024), 2) AS 'Size (MB)',
  table_rows
FROM information_schema.TABLES
WHERE table_schema = 'openspg'
ORDER BY table_rows DESC;
```

#### Connection Pool Monitoring
```sql
-- Active connections
SHOW PROCESSLIST;

-- Connection statistics
SHOW STATUS LIKE 'Threads_connected';
SHOW STATUS LIKE 'Max_used_connections';
```

### Recommended Tuning Parameters

```sql
-- Increase buffer pool for better caching
SET GLOBAL innodb_buffer_pool_size = 4294967296;  -- 4 GB

-- Optimize query cache
SET GLOBAL query_cache_size = 67108864;  -- 64 MB
SET GLOBAL query_cache_type = 1;

-- Adjust connection limits
SET GLOBAL max_connections = 2000;
SET GLOBAL max_connect_errors = 100000;

-- Log settings
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 1;
```

### Table Optimization

```sql
-- Analyze tables for optimization
ANALYZE TABLE kg_ontology_entity;

-- Optimize table storage
OPTIMIZE TABLE kg_scheduler_task;

-- Check table status
SHOW TABLE STATUS WHERE Name = 'kg_builder_job';
```

---

## Integration Points

### OpenSPG Server Integration

The MySQL database serves as the persistence layer for the OpenSPG server container.

**Connection Flow:**
```
OpenSPG Server (172.18.0.2:8887)
    ↓
MySQL Database (172.18.0.3:3306)
    ↓
openspg database
```

**Configuration in OpenSPG:**
```yaml
# Server configuration
database:
  type: mysql
  host: openspg-mysql
  port: 3306
  username: root
  password: openspg
  database: openspg
  pool_size: 50
  max_overflow: 100
```

### AEON UI Integration

The AEON UI (port 8888) connects to MySQL via the OpenSPG server API layer.

**Data Flow:**
```
AEON UI (Port 8888)
    ↓ HTTP/REST API
OpenSPG Server (Port 8887)
    ↓ JDBC/SQL
MySQL Database (Port 3306)
```

### ElasticSearch Sync

Knowledge graph data is replicated to ElasticSearch for search functionality.

```sql
-- Tables synced to ElasticSearch
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'openspg'
AND table_name LIKE 'kg_ontology_%';
```

### Cloudbeaver Integration

Database administration via Cloudbeaver on port 8978.

**Connection Details:**
- **Host:** openspg-mysql
- **Port:** 3306
- **Database:** openspg
- **Auth:** root / openspg

---

## Troubleshooting

### Common Issues

#### Connection Refused
```bash
# Check container status
docker ps | grep openspg-mysql

# Check container logs
docker logs openspg-mysql --tail 50

# Test connectivity
docker exec openspg-mysql mysqladmin -uroot -popenspg ping
```

#### Slow Queries
```sql
-- Identify slow queries
SELECT * FROM mysql.slow_log
ORDER BY query_time DESC
LIMIT 10;

-- Check table locks
SHOW OPEN TABLES WHERE In_use > 0;
```

#### Disk Space Issues
```bash
# Check database size
docker exec openspg-mysql mysql -uroot -popenspg -e "
SELECT
  table_schema AS 'Database',
  ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS 'Size (MB)'
FROM information_schema.TABLES
GROUP BY table_schema;"

# Check container disk usage
docker exec openspg-mysql df -h
```

#### Lock Timeouts
```sql
-- Check InnoDB lock waits
SELECT * FROM information_schema.innodb_lock_waits;

-- Show running transactions
SELECT * FROM information_schema.innodb_trx;

-- Kill long-running query
KILL <process_id>;
```

### Health Check Commands

```bash
# Container health
docker inspect openspg-mysql | grep -A 10 Health

# Database connectivity
docker exec openspg-mysql mysqladmin -uroot -popenspg status

# Table integrity check
docker exec openspg-mysql mysqlcheck -uroot -popenspg --all-databases

# Process list
docker exec openspg-mysql mysql -uroot -popenspg -e "SHOW PROCESSLIST;"
```

---

## References

### Documentation
- **MariaDB Official Docs:** https://mariadb.com/kb/en/documentation/
- **MySQL Reference Manual:** https://dev.mysql.com/doc/
- **OpenSPG GitHub:** https://github.com/OpenSPG/openspg

### Related Documentation
- [[Docker-Architecture]] - Container infrastructure
- [[OpenSPG-Server]] - Application server integration
- [[AEON-UI]] - Frontend application
- [[ElasticSearch-Database]] - Search index integration
- [[Cloudbeaver-Admin]] - Database administration tool

### Performance Resources
- **InnoDB Tuning:** https://mariadb.com/kb/en/innodb-system-variables/
- **Query Optimization:** https://mariadb.com/kb/en/query-optimization/
- **Replication Setup:** https://mariadb.com/kb/en/replication/

---

## Version History

- **v1.0.0** (2025-11-03): Initial professional API documentation with complete schema analysis and operational procedures

---

**Document Maintenance:**
- **Next Review:** 2025-11-10
- **Update Frequency:** Weekly or upon schema changes
- **Owner:** AEON FORGE System Team

**Status:** ACTIVE | Last verified: 2025-11-03 17:11:58 CST
