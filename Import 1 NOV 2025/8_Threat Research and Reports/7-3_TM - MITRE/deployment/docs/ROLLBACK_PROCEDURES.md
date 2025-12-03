# AEON Backend API Rollback Procedures

**File:** ROLLBACK_PROCEDURES.md
**Created:** 2025-11-08
**Purpose:** When and how to rollback deployments
**Status:** ACTIVE

## When to Rollback

### Critical Issues (Immediate Rollback)

- **Service Unavailability:** API not responding after 3 health check retries
- **Data Corruption:** Database integrity compromised
- **Security Breach:** Active security vulnerability discovered
- **Critical Functionality Broken:** Core features completely non-functional
- **Cascading Failures:** Multiple systems affected

### Major Issues (Rollback After Assessment)

- **High Error Rate:** Error rate > 5% sustained for 10+ minutes
- **Performance Degradation:** Response time p95 > 5 seconds sustained
- **Memory Leaks:** Memory usage growth > 10% per hour
- **Database Connection Failures:** > 10% of connections failing
- **Integration Failures:** Third-party integrations broken

### Minor Issues (Consider Hotfix Instead)

- **Low Error Rate:** Error rate 1-5%
- **Moderate Performance Issues:** Response time p95 2-5 seconds
- **Non-critical Feature Broken:** Minor functionality affected
- **Cosmetic Issues:** UI/UX problems without functionality impact

## Rollback Decision Matrix

| Impact | Urgency | Action |
|--------|---------|--------|
| Critical | High | Immediate rollback |
| Critical | Medium | Rollback within 15 minutes |
| Major | High | Rollback within 30 minutes |
| Major | Medium | Assess and rollback within 1 hour |
| Minor | High | Consider hotfix or rollback within 2 hours |
| Minor | Medium | Plan hotfix or rollback in next deployment |

---

## Automated Rollback Procedure

### Using Rollback Script

```bash
cd "/home/jim/2_OXOT_Projects_Dev/Import 1 NOV 2025/7-3_TM - MITRE"

# Run rollback script
./deployment/scripts/rollback_deployment.sh
```

**Interactive Menu Options:**
1. Rollback NER API
2. Rollback Query API
3. Rollback Both APIs
4. Rollback to specific Docker tag
5. Emergency stop all services

### Automated Rollback Process

The script automatically:
1. Creates snapshot of current state
2. Stops failed containers
3. Restores backup images
4. Redeploys services
5. Validates deployment
6. Reports status

---

## Manual Rollback Procedures

### Option 1: Restore from Backup Images

```bash
# Stop current containers
docker stop aeon-ner-api aeon-query-api
docker rm aeon-ner-api aeon-query-api

# List available backup images
docker images | grep aeon-ner-api
docker images | grep aeon-query-api

# Restore from backup (automatic .backup tag)
docker tag aeon-ner-api:latest.backup aeon-ner-api:latest
docker tag aeon-query-api:latest.backup aeon-query-api:latest

# Redeploy using deployment scripts
./deployment/scripts/deploy_ner_v8_api.sh
./deployment/scripts/deploy_query_api.sh

# Verify
./deployment/scripts/health_check_all.sh
```

### Option 2: Rollback to Specific Version

```bash
# List available versions
docker images | grep aeon

# Example output:
# aeon-ner-api    v1.2.3    abc123    2 hours ago    1.2GB
# aeon-ner-api    v1.2.2    def456    1 day ago      1.2GB

# Tag specific version as latest
docker tag aeon-ner-api:v1.2.2 aeon-ner-api:latest
docker tag aeon-query-api:v1.2.2 aeon-query-api:latest

# Redeploy
./deployment/scripts/deploy_ner_v8_api.sh
./deployment/scripts/deploy_query_api.sh
```

### Option 3: Docker Compose Rollback

```bash
cd deployment/docker

# Stop all services
docker-compose down

# Switch to previous version in git
git log --oneline
git checkout <previous-commit-hash>

# Rebuild and deploy
docker-compose build
docker-compose up -d

# Verify
cd ../..
./deployment/scripts/health_check_all.sh
```

---

## Component-Specific Rollback

### NER API Only

```bash
# Stop NER API
docker stop aeon-ner-api
docker rm aeon-ner-api

# Restore backup
docker tag aeon-ner-api:latest.backup aeon-ner-api:latest

# Redeploy
./deployment/scripts/deploy_ner_v8_api.sh

# Verify
curl http://localhost:8000/health
```

### Query API Only

```bash
# Stop Query API
docker stop aeon-query-api
docker rm aeon-query-api

# Restore backup
docker tag aeon-query-api:latest.backup aeon-query-api:latest

# Redeploy
./deployment/scripts/deploy_query_api.sh

# Verify
curl http://localhost:8001/health
```

### Neo4j Rollback

```bash
# Stop Neo4j
docker stop neo4j

# Restore from backup
# Option 1: Restore data volume
docker run --rm -v neo4j_data:/data -v /path/to/backup:/backup \
  ubuntu bash -c "cd /data && tar xvf /backup/neo4j-backup.tar.gz"

# Option 2: Use Neo4j backup tools
neo4j-admin restore --from=/path/to/backup --database=neo4j

# Restart Neo4j
docker start neo4j

# Verify
curl http://localhost:7474
```

---

## Emergency Procedures

### Emergency Stop All Services

```bash
# Quick stop
docker stop aeon-ner-api aeon-query-api neo4j

# Or use script
./deployment/scripts/rollback_deployment.sh
# Select option 5: Emergency stop all services
```

### Emergency Recovery

```bash
# 1. Stop everything
docker-compose down

# 2. Remove all containers and networks
docker rm -f aeon-ner-api aeon-query-api neo4j
docker network prune -f

# 3. Restore from last known good configuration
git checkout <last-good-commit>

# 4. Fresh deployment
./deployment/scripts/setup_environment.sh
./deployment/scripts/deploy_ner_v8_api.sh
./deployment/scripts/deploy_query_api.sh

# 5. Verify
./deployment/scripts/health_check_all.sh
```

---

## Post-Rollback Validation

### Immediate Checks (0-5 minutes)

```bash
# Container status
docker ps

# Health checks
curl http://localhost:8000/health
curl http://localhost:8001/health

# Run comprehensive check
./deployment/scripts/health_check_all.sh

# Check logs for errors
docker logs aeon-ner-api --tail 50
docker logs aeon-query-api --tail 50
```

### Functional Tests (5-15 minutes)

```bash
# Test NER API
curl -X POST http://localhost:8000/api/v1/extract-entities \
  -H "Content-Type: application/json" \
  -d '{"text": "APT29 uses MITRE ATT&CK technique T1566"}'

# Test Query API
curl -X POST http://localhost:8001/api/v1/query/execute \
  -H "Content-Type: application/json" \
  -d '{"query": "MATCH (n:Technique) RETURN n.name LIMIT 5"}'

# Run integration tests
python tests/integration/test_api_endpoints.py
```

### Extended Monitoring (15-60 minutes)

- Monitor error rates
- Check resource usage
- Review logs continuously
- Verify database connectivity
- Test all critical endpoints
- Monitor user reports

---

## Rollback Validation Checklist

- [ ] All containers running
- [ ] Health checks passing
- [ ] No errors in logs
- [ ] Database connectivity verified
- [ ] API endpoints responding correctly
- [ ] Integration tests passing
- [ ] Performance metrics acceptable
- [ ] No memory leaks detected
- [ ] Resource usage normal
- [ ] User-facing functionality working

---

## Communication During Rollback

### Internal Communication

**Immediately notify:**
- Development team
- DevOps team
- QA team
- Team lead/manager

**Communication channels:**
- Slack/Teams incident channel
- Email (for major incidents)
- Phone (for critical incidents)

### External Communication (if applicable)

**Status page update:**
```
Title: Service Degradation - Rolling Back Deployment
Status: Investigating/Degraded
Message: We are experiencing issues with recent deployment
and are rolling back to previous version. Expected recovery:
[TIME]. We apologize for any inconvenience.
```

---

## Root Cause Analysis (Post-Rollback)

### Investigation Steps

1. **Collect Evidence**
   - Container logs
   - Application logs
   - Database logs
   - Metrics and monitoring data
   - Error reports

2. **Timeline Analysis**
   - When did issue start?
   - What changed?
   - When was it detected?
   - When was rollback initiated?
   - When was service restored?

3. **Root Cause Identification**
   - Code changes
   - Configuration changes
   - Infrastructure changes
   - External dependencies
   - Data issues

4. **Impact Assessment**
   - Users affected
   - Duration of impact
   - Data integrity
   - Business impact

### Documentation

Create incident report including:
- **Summary:** Brief description of incident
- **Timeline:** Detailed timeline of events
- **Root Cause:** Technical root cause
- **Impact:** Scope and severity of impact
- **Resolution:** How it was resolved
- **Prevention:** How to prevent recurrence
- **Action Items:** Follow-up tasks

---

## Prevention Strategies

### Pre-Deployment

- Comprehensive testing (unit, integration, e2e)
- Staging environment validation
- Load testing
- Security scanning
- Code review
- Configuration validation

### Deployment Process

- Blue-green deployment
- Canary releases
- Feature flags
- Gradual rollout
- Automated testing in production
- Continuous monitoring

### Post-Deployment

- Extended monitoring period
- Automated alerts
- Performance baselines
- Error rate tracking
- User feedback monitoring

---

## Rollback Performance Metrics

### Target Metrics

- **Detection Time:** < 5 minutes
- **Decision Time:** < 10 minutes
- **Rollback Execution Time:** < 15 minutes
- **Total Time to Recovery:** < 30 minutes
- **Success Rate:** > 95%

### Track and Improve

- Log all rollback incidents
- Measure rollback times
- Identify bottlenecks
- Automate manual steps
- Update procedures based on lessons learned

---

## Emergency Contacts

**Critical Issues (24/7)**
- On-Call Engineer: [Contact]
- DevOps Lead: [Contact]
- CTO/Technical Director: [Contact]

**Major Issues (Business Hours)**
- Backend Team Lead: [Contact]
- QA Lead: [Contact]
- Product Manager: [Contact]

**Support Resources**
- Incident Slack Channel: #incidents
- Runbook: [Link]
- Monitoring Dashboard: [Link]
- Documentation: /deployment/docs/

---

**Last Updated:** 2025-11-08
**Version:** 1.0
**Review Frequency:** Quarterly or after each major incident
