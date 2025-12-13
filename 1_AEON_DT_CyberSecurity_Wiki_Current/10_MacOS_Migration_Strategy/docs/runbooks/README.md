# NER11 Gold Model Operational Runbooks

**Created:** 2025-12-04
**Version:** v1.0.0
**Purpose:** Complete operational documentation for system management
**Status:** ACTIVE

## Overview

This directory contains comprehensive operational runbooks for managing, maintaining, and troubleshooting the NER11 Gold Model system. All runbooks follow a standard format with decision trees, specific commands, expected outputs, and escalation criteria.

---

## Quick Reference Guide

### 🚀 Daily Operations

**Start System:**
```bash
# Complete startup procedure
cd docs/runbooks/daily
cat STARTUP_PROCEDURE.md

# Quick start (if system is healthy)
docker-compose up -d
./scripts/startup_verify.sh
```

**Check System Health:**
```bash
# Service status
docker-compose ps

# API health
curl http://localhost:8000/health

# Database health
curl http://localhost:8000/api/v1/db/health

# Container resources
docker stats --no-stream
```

---

### 🔧 Service Management

```bash
# Start individual service
docker-compose up -d <service_name>

# Stop service gracefully
docker-compose stop -t 60 <service_name>

# Restart with health verification
docker-compose restart -t 60 <service_name>
sleep 20
curl http://localhost:8000/health
```

See: [docs/runbooks/service-management/SERVICE_CONTROL.md](service-management/SERVICE_CONTROL.md)

---

### 💾 Backup Operations

**Daily Automated Backup:**
```bash
./scripts/backup_database.sh
./scripts/backup_models.sh
```

**Manual Backup:**
```bash
# Database
docker-compose exec -T postgres pg_dump -U postgres ner11_db | gzip > /backups/ner11/database/manual_$(date +%Y%m%d).sql.gz

# Verify backup
gunzip -t /backups/ner11/database/manual_*.sql.gz
```

See: [docs/runbooks/backup-recovery/BACKUP_PROCEDURES.md](backup-recovery/BACKUP_PROCEDURES.md)

---

### 🚨 Emergency Response

**API Not Responding:**
```bash
# Quick diagnosis
docker-compose ps api
docker-compose logs api --tail=50
curl -v http://localhost:8000/health

# Emergency restart
docker-compose restart -t 60 api
```

**Database Connection Issues:**
```bash
# Check PostgreSQL
docker-compose exec postgres pg_isready -U postgres

# Check connections
docker-compose exec postgres psql -U postgres -c "SELECT count(*) FROM pg_stat_activity;"

# Reset connection pool
docker-compose restart api
```

**Disk Space Critical:**
```bash
# Emergency cleanup
docker system prune -af --volumes
find /var/log -name "*.log" -mtime +7 -delete
docker-compose exec postgres psql -U postgres ner11_db -c "VACUUM FULL;"
```

---

## Runbook Directory Structure

```
docs/runbooks/
├── README.md (this file)
│
├── daily/
│   └── STARTUP_PROCEDURE.md                    # Complete startup process
│
├── service-management/
│   └── SERVICE_CONTROL.md                      # Service lifecycle management
│
├── backup-recovery/
│   └── BACKUP_PROCEDURES.md                    # Backup and restoration
│
├── monitoring/
│   └── MONITORING_ALERTING.md                  # Monitoring and alerting
│
├── incident-response/
│   ├── API_NOT_RESPONDING.md                   # API troubleshooting
│   ├── DATABASE_CONNECTION_ISSUES.md           # Database diagnostics
│   ├── DISK_SPACE_ISSUES.md                    # Disk space recovery
│   ├── MODEL_LOADING_FAILURES.md               # ML model issues
│   ├── NETWORK_CONNECTIVITY_ISSUES.md          # Network diagnostics
│   ├── PERFORMANCE_DEGRADATION.md              # Performance tuning
│   └── DATA_CORRUPTION.md                      # Data recovery
│
├── maintenance/
│   └── MAINTENANCE_WINDOWS.md                  # Scheduled maintenance
│
└── scaling/
    ├── RESOURCE_SCALING.md                     # Vertical/horizontal scaling
    └── CAPACITY_PLANNING.md                    # Growth planning
```

---

## Runbook Categories

### 1. Daily Operations

**STARTUP_PROCEDURE.md**
- Pre-startup checklist
- Service startup sequence (PostgreSQL → API → Frontend)
- Health verification procedures
- Troubleshooting startup delays
- Expected startup time: 3-5 minutes

**Key Commands:**
```bash
docker-compose up -d
./scripts/startup_verify.sh
docker-compose logs -f
```

---

### 2. Service Management

**SERVICE_CONTROL.md**
- Starting/stopping individual services
- Graceful vs hard restarts
- Dependency management and ordering
- Scaling services (horizontal/vertical)
- Health verification after changes

**Key Commands:**
```bash
docker-compose up -d <service>
docker-compose stop -t 60 <service>
docker-compose restart -t 60 <service>
docker-compose up -d --scale api=3
```

---

### 3. Backup and Recovery

**BACKUP_PROCEDURES.md**
- Automated daily backups
- Manual backup procedures
- Database restoration (full and selective)
- ML model backup and versioning
- Configuration and volume backups
- Disaster recovery procedures

**Key Commands:**
```bash
./scripts/backup_database.sh
./scripts/backup_models.sh
./scripts/backup_full_system.sh
# Restore from backup
gunzip -c /backups/ner11/database/backup.sql.gz | docker-compose exec -T postgres psql -U postgres ner11_db
```

---

### 4. Monitoring and Alerting

**MONITORING_ALERTING.md**
- Key metrics (CPU, memory, disk, network)
- Application metrics (API response time, error rates)
- Database metrics (connections, query performance)
- Dashboard setup (Prometheus + Grafana)
- Alert thresholds and escalation
- Performance baseline establishment

**Key Commands:**
```bash
docker stats
df -h
docker-compose logs --since 10m | grep ERROR
curl http://localhost:8000/metrics
./scripts/establish_baseline.sh
```

---

### 5. Incident Response

**API_NOT_RESPONDING.md**
- Symptoms: Timeout, 502/503 errors
- Decision tree for diagnosis
- Container, port, and application checks
- Recovery procedures (graceful/hard restart)
- Data consistency verification
- Root cause analysis

**DATABASE_CONNECTION_ISSUES.md**
- Symptoms: Connection refused, pool exhausted
- PostgreSQL health checks
- Network connectivity verification
- Connection pool management
- Long-running query handling
- Authentication troubleshooting

**DISK_SPACE_ISSUES.md**
- Emergency cleanup procedures
- Docker cleanup (images, containers, volumes)
- Log file management
- Database VACUUM for space reclamation
- Volume expansion procedures
- Growth investigation and prevention

**MODEL_LOADING_FAILURES.md** *(To be created)*
- Model file verification
- Memory allocation issues
- Model format compatibility
- Recovery from backup
- Validation procedures

**NETWORK_CONNECTIVITY_ISSUES.md** *(To be created)*
- Docker network diagnostics
- Port accessibility testing
- DNS resolution issues
- Network isolation problems
- Firewall and routing checks

**PERFORMANCE_DEGRADATION.md** *(To be created)*
- Slow API response diagnosis
- Database query optimization
- Resource bottleneck identification
- Cache tuning
- Profiling procedures

**DATA_CORRUPTION.md** *(To be created)*
- Corruption detection
- Database integrity checks
- Recovery from backups
- Transaction log analysis
- Prevention measures

---

### 6. Maintenance

**MAINTENANCE_WINDOWS.md**
- Weekly maintenance tasks (VACUUM, cleanup, logs)
- Monthly maintenance (VACUUM FULL, updates, REINDEX)
- Quarterly maintenance (upgrades, audits)
- Pre/post-maintenance checklists
- PostgreSQL performance tuning
- Rollback procedures

**Key Commands:**
```bash
./scripts/pre_maintenance.sh
docker-compose exec postgres psql -U postgres ner11_db -c "VACUUM ANALYZE;"
docker system prune -af
./scripts/post_maintenance.sh
```

---

### 7. Scaling and Capacity

**RESOURCE_SCALING.md** *(To be created)*
- Vertical scaling (increase resources)
- Horizontal scaling (multiple replicas)
- Load balancer configuration
- Resource limits and reservations
- Performance validation

**CAPACITY_PLANNING.md** *(To be created)*
- Growth rate tracking
- Resource usage trends
- Forecasting future needs
- Cost optimization
- Upgrade planning

---

## Standard Runbook Format

All runbooks follow this structure:

```markdown
# Title

**File:** FILENAME.md
**Created:** YYYY-MM-DD
**Version:** vX.Y.Z
**Purpose:** [Brief description]
**Status:** ACTIVE

## Executive Summary
[Quick overview and key information]

## Decision Tree
[Visual flowchart for diagnosis]

## Diagnostic Procedure
[Step-by-step diagnosis]

## Recovery Procedures
[Specific fix procedures]

## Root Cause Analysis
[Common causes and solutions]

## Prevention Measures
[Proactive monitoring and configuration]

## Escalation Criteria
[When to escalate and to whom]

## Post-Incident Checklist
[Verification and documentation]

## Quick Reference Commands
[Essential commands summary]

## Related Runbooks
[Links to related procedures]
```

---

## Severity and Response Time Guidelines

| Severity  | Response Time | Examples | Escalation |
|-----------|---------------|----------|------------|
| INFO      | N/A           | Scheduled maintenance, routine logs | Log only |
| WARNING   | 30 minutes    | CPU >80%, Memory >85%, Disk >80% | After 1 hour |
| CRITICAL  | 15 minutes    | Service down, Database unreachable | After 30 minutes |
| EMERGENCY | 5 minutes     | Data loss, Security breach | Immediate CTO |

---

## Escalation Contacts

```yaml
tier_1_support:
  role: Operations Team
  response_time: 15 minutes
  contact: ops-team@example.com
  phone: +1-XXX-XXX-XXXX

tier_2_support:
  role: DevOps Lead
  response_time: 30 minutes
  contact: devops-lead@example.com
  phone: +1-XXX-XXX-XXXX

tier_3_support:
  role: Database Administrator
  response_time: 1 hour
  contact: dba@example.com
  phone: +1-XXX-XXX-XXXX

emergency_escalation:
  role: CTO
  scenarios:
    - Data corruption confirmed
    - Security breach
    - Complete system failure
    - Potential data loss
  contact: cto@example.com
  phone: +1-XXX-XXX-XXXX (24/7)
```

---

## Common Commands Quick Reference

### System Status
```bash
# Overall health check
./scripts/startup_verify.sh

# Container status
docker-compose ps

# Resource usage
docker stats --no-stream

# Disk space
df -h

# Service logs
docker-compose logs -f --tail=50 <service>
```

### Service Control
```bash
# Start all services
docker-compose up -d

# Stop service gracefully
docker-compose stop -t 60 <service>

# Restart with health check
docker-compose restart -t 60 <service>
sleep 20
curl http://localhost:8000/health
```

### Database Operations
```bash
# Connection check
docker-compose exec postgres pg_isready -U postgres

# Active connections
docker-compose exec postgres psql -U postgres -c "SELECT count(*) FROM pg_stat_activity;"

# VACUUM
docker-compose exec postgres psql -U postgres ner11_db -c "VACUUM ANALYZE;"

# Backup
./scripts/backup_database.sh
```

### Monitoring
```bash
# API health
curl http://localhost:8000/health

# Database health
curl http://localhost:8000/api/v1/db/health

# API metrics
curl http://localhost:8000/metrics

# Check errors
docker-compose logs --since 10m | grep -E "ERROR|CRITICAL"
```

### Emergency Recovery
```bash
# Emergency cleanup
docker system prune -af --volumes

# Hard restart API
docker-compose kill api && docker-compose rm -f api && docker-compose up -d api

# Reset connection pool
docker-compose restart api

# Restore database
gunzip -c /backups/ner11/database/latest.sql.gz | docker-compose exec -T postgres psql -U postgres ner11_db
```

---

## Automation Scripts Directory

```bash
scripts/
├── startup_verify.sh              # Complete startup verification
├── backup_database.sh             # Automated database backup
├── backup_models.sh               # ML model backup
├── backup_config.sh               # Configuration backup
├── backup_volumes.sh              # Docker volume backup
├── backup_full_system.sh          # Complete system backup
├── verify_backups.sh              # Backup integrity verification
├── pre_maintenance.sh             # Pre-maintenance checklist
├── post_maintenance.sh            # Post-maintenance verification
├── rollback_maintenance.sh        # Rollback procedure
├── health_check.sh                # Service health verification
├── establish_baseline.sh          # Performance baseline
├── track_disk_growth.sh           # Disk usage tracking
└── check_disk_space.sh            # Disk space monitoring
```

**Make all scripts executable:**
```bash
chmod +x scripts/*.sh
```

---

## Training and Onboarding

### For New Operations Team Members

**Week 1: Familiarization**
- Read all runbooks in sequence
- Shadow experienced operator during startup
- Practice using monitoring dashboards
- Review common incident patterns

**Week 2: Hands-On Practice**
- Execute daily startup procedure
- Perform manual backup and verification
- Practice service restart procedures
- Simulate common incidents in test environment

**Week 3: Advanced Procedures**
- Execute maintenance window procedures
- Practice incident response with supervision
- Learn escalation protocols
- Review post-incident analyses

**Week 4: Independent Operation**
- Lead daily operations with oversight
- Respond to incidents independently
- Conduct weekly maintenance
- Document lessons learned

---

## Continuous Improvement

### Runbook Maintenance

**Monthly Review:**
- Update commands based on infrastructure changes
- Add newly discovered troubleshooting steps
- Refine decision trees based on incident patterns
- Verify automation scripts still functional

**After Each Incident:**
- Document what worked/didn't work
- Update diagnostic procedures
- Add new root causes if identified
- Improve prevention measures

**Quarterly Audit:**
- Validate all procedures still accurate
- Test disaster recovery procedures
- Review escalation effectiveness
- Update baselines and thresholds

---

## Related Documentation

- **API Documentation:** `/5_NER11_Gold_Model/docs/`
- **Architecture:** `/1_AEON_DT_CyberSecurity_Wiki_Current/04_APIs/`
- **Development Guide:** `/5_NER11_Gold_Model/README.md`
- **Frontend Documentation:** `/1_AEON_DT_Cybersecurity_Front_End_Development_2025_DEC_1/`

---

## Version History

| Version | Date       | Changes | Author |
|---------|------------|---------|--------|
| v1.0.0  | 2025-12-04 | Initial comprehensive runbook suite | System |

---

## Feedback and Updates

To request runbook updates or report issues:

1. Document the issue or improvement needed
2. Provide specific commands or procedures that need revision
3. Include incident reference if applicable
4. Submit to operations team for review

**Last Updated:** 2025-12-04
**Next Review Date:** 2025-12-18

---

**REMEMBER:**
- Always verify backups before maintenance
- Follow escalation procedures when stuck
- Document all incidents for continuous improvement
- When in doubt, consult the runbook and escalate early
