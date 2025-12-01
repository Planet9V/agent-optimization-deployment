# Deployment Conflict Resolution
**File:** DEPLOYMENT_CONFLICT_RESOLUTION.md
**Created:** 2025-11-15 (Current System Date)
**Modified:** 2025-11-15
**Version:** v1.0.0
**Author:** System Architecture Designer
**Purpose:** Document deployment conflicts and resolution strategy for AEON UI production deployment
**Status:** ACTIVE

## Executive Summary

Resolved IP and port conflicts between AEON UI production deployment and existing development containers in the openspg-network.

## Conflict Analysis

### Initial Deployment Configuration
- **Target IP:** 172.18.0.8
- **Target Port:** 3000
- **Container:** aeon-ui (production)

### Identified Conflicts

#### IP Conflict
```
Requested: 172.18.0.8
Occupied by: openspg-server (172.18.0.8)
Status: Active production service
Resolution: Cannot disrupt
```

#### Port Conflict
```
Requested: 3000 (host) -> 3000 (container)
Occupied by: aeon-saas-dev (172.18.0.7)
Container Status: Up 2 days (unhealthy)
Container Type: Development environment
Resolution: Available for alternative strategy
```

### Network State Analysis
```
openspg-network IP allocations:
172.18.0.2 - openspg-minio
172.18.0.3 - openspg-qdrant
172.18.0.4 - openspg-mysql
172.18.0.5 - aeon-postgres-dev
172.18.0.6 - openspg-neo4j
172.18.0.7 - aeon-saas-dev (unhealthy dev container)
172.18.0.8 - openspg-server (CONFLICT)
172.18.0.9+ - AVAILABLE
```

## Resolution Strategy

### Selected Approach: Hybrid (IP Change + Port Change)

**Decision:** Use IP 172.18.0.9 + Host Port 3001

**Rationale:**
1. **IP Selection (172.18.0.9)**
   - Avoids conflict with openspg-server
   - Provides dedicated IP for production UI
   - Maintains network isolation
   - Allows future expansion (172.18.0.10+)

2. **Port Selection (3001)**
   - Avoids conflict with unhealthy aeon-saas-dev
   - Allows temporary coexistence with dev environment
   - Standard practice for multi-instance deployments
   - Can reclaim port 3000 after dev cleanup

3. **Non-Disruptive**
   - Does not require stopping aeon-saas-dev immediately
   - Does not impact openspg-server operations
   - Allows gradual migration from dev to production
   - Maintains service availability during transition

### Rejected Alternatives

#### Option A: Stop aeon-saas-dev + Use Port 3000
```
Pros:
- Clean port allocation (3000)
- Standard Next.js port
- Removes unhealthy container

Cons:
- Requires immediate dev environment shutdown
- Potential data loss if dev work in progress
- May disrupt ongoing development
- Premature cleanup decision
```

#### Option B: Keep IP 172.18.0.8 + Use Port 3001
```
Pros:
- Avoids port conflict
- Simple single change

Cons:
- IP conflict with openspg-server (CRITICAL)
- Would cause network failure
- Not viable solution
```

## Implementation Changes

### docker-compose.aeon-ui.yml Updates

#### Network Configuration
```yaml
# BEFORE
networks:
  openspg-network:
    ipv4_address: 172.18.0.8

# AFTER
networks:
  openspg-network:
    ipv4_address: 172.18.0.9  # Changed to avoid openspg-server conflict
```

#### Port Mapping
```yaml
# BEFORE
ports:
  - "3000:3000"

# AFTER
ports:
  - "3001:3000"  # Host port changed to avoid aeon-saas-dev conflict
```

#### Environment Variables
```yaml
# BEFORE
- NEXTAUTH_URL=http://localhost:3000

# AFTER
- NEXTAUTH_URL=http://localhost:3001  # Updated to reflect new port mapping
```

## Deployment Instructions

### 1. Verify Current State
```bash
# Check network allocations
docker network inspect openspg-network

# Verify port availability
netstat -tuln | grep 3001

# Check container status
docker ps -a --filter "name=aeon-saas-dev"
```

### 2. Deploy AEON UI
```bash
# Deploy with updated configuration
docker compose -f docker-compose.aeon-ui.yml up -d

# Verify deployment
docker ps --filter "name=aeon-ui"
docker logs aeon-ui
```

### 3. Access Application
```
Production UI: http://localhost:3001
Internal Network: http://172.18.0.9:3000
```

### 4. Optional: Cleanup Dev Environment
```bash
# When ready to reclaim port 3000 and cleanup dev environment:
docker stop aeon-saas-dev
docker rm aeon-saas-dev

# Then update docker-compose.aeon-ui.yml to use port 3000 if desired:
# ports:
#   - "3000:3000"  # After dev cleanup
```

## Network Architecture

### Production Network Topology
```
openspg-network (172.18.0.0/16)
├── 172.18.0.2  - openspg-minio (Object Storage)
├── 172.18.0.3  - openspg-qdrant (Vector DB)
├── 172.18.0.4  - openspg-mysql (Relational DB)
├── 172.18.0.5  - aeon-postgres-dev (Dev DB)
├── 172.18.0.6  - openspg-neo4j (Graph DB)
├── 172.18.0.7  - aeon-saas-dev (Dev UI - unhealthy)
├── 172.18.0.8  - openspg-server (Backend API)
└── 172.18.0.9  - aeon-ui (Production UI) ← NEW
```

### Port Mapping
```
Host Ports:
- 3000: aeon-saas-dev (dev environment, unhealthy)
- 3001: aeon-ui (production environment) ← NEW

Container Ports:
- Both containers expose port 3000 internally
- Host port mapping differentiates them
```

## Risk Assessment

### Deployment Risks
| Risk | Severity | Mitigation |
|------|----------|------------|
| Port 3001 already in use | Low | Pre-deployment port check |
| IP 172.18.0.9 conflict | Low | Network inspection verification |
| NEXTAUTH_URL misconfiguration | Medium | Health check validation |
| Dev/Prod environment confusion | Medium | Clear documentation, naming conventions |

### Operational Risks
| Risk | Severity | Mitigation |
|------|----------|------------|
| Users access wrong port | Low | Clear access documentation |
| Dev container cleanup breaks prod | Low | Separate IP allocation |
| Network performance degradation | Low | Resource limits configured |

## Monitoring & Validation

### Health Checks
```bash
# Container health
docker ps --filter "name=aeon-ui" --format "{{.Status}}"

# Application health
curl http://localhost:3001/api/health

# Network connectivity
docker exec aeon-ui sh -c "wget --quiet --tries=1 --spider http://openspg-server:8887"
```

### Performance Metrics
- Response time: < 200ms (target)
- Memory usage: < 2GB (limit configured)
- CPU usage: < 2.0 cores (limit configured)
- Health check: 30s intervals

## Future Considerations

### Port 3000 Reclamation
When development environment is no longer needed:
1. Stop and remove aeon-saas-dev
2. Update aeon-ui port mapping to 3000:3000
3. Update NEXTAUTH_URL to http://localhost:3000
4. Redeploy with updated configuration

### IP Allocation Strategy
- Reserve 172.18.0.10-172.18.0.20 for future AEON services
- Document IP allocations in network management file
- Implement IP Address Management (IPAM) for larger deployments

### Development Environment Cleanup
```bash
# Complete dev environment removal script
docker stop aeon-saas-dev aeon-postgres-dev
docker rm aeon-saas-dev aeon-postgres-dev
docker volume prune -f  # Remove unused volumes
```

## Architecture Decision Record (ADR)

### ADR-001: Production UI IP and Port Allocation

**Context:**
Deploying production AEON UI into existing openspg-network with multiple active services and development containers.

**Decision:**
Allocate IP 172.18.0.9 and host port 3001 for production AEON UI deployment.

**Consequences:**

**Positive:**
- No disruption to existing production services
- Clean separation between dev and production environments
- Allows gradual migration strategy
- Preserves development environment for testing
- Provides dedicated IP for production UI

**Negative:**
- Non-standard port (3001 vs 3000) for production access
- Potential user confusion about correct access port
- Manual port reclamation required later

**Alternatives Considered:**
- Stop dev container and use port 3000 (too disruptive)
- Use IP 172.18.0.8 (conflicts with openspg-server)
- Use random available port (poor UX, harder to document)

**Status:** ACCEPTED

**Date:** 2025-11-15

## References & Sources

### Docker Network Documentation
- Docker networking: https://docs.docker.com/network/
- Static IP assignment: https://docs.docker.com/compose/networking/

### Next.js Configuration
- Environment variables: https://nextjs.org/docs/basic-features/environment-variables
- NextAuth.js configuration: https://next-auth.js.org/configuration/options

### Related Documentation
- [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) - General deployment instructions
- [docker-compose.aeon-ui.yml](../docker-compose.aeon-ui.yml) - Production configuration
- [.env.production](../.env.production) - Environment configuration

## Version History
- v1.0.0 (2025-11-15): Initial conflict analysis and resolution strategy

---

*AEON FORGE ULTRATHINK v2.0.0 | Fact-Based Analysis | Production Deployment*
*Updated: 2025-11-15 | Status: OPERATIONAL*
