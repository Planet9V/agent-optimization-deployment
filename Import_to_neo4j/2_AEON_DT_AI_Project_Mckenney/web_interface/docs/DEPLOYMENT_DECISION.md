# Deployment Decision Summary
**File:** DEPLOYMENT_DECISION.md
**Created:** 2025-11-15
**Version:** v1.0.0
**Author:** System Architecture Designer
**Purpose:** Quick reference for deployment configuration decisions
**Status:** ACTIVE

## Decision Summary

**FINAL CONFIGURATION:**
- **IP Address:** 172.18.0.9 (changed from 172.18.0.8)
- **Host Port:** 3001 (changed from 3000)
- **Container Port:** 3000 (internal, unchanged)
- **Access URL:** http://localhost:3001
- **NextAuth URL:** http://localhost:3001

## Conflict Resolution

### IP Conflict
```
❌ 172.18.0.8 - Occupied by openspg-server
✅ 172.18.0.9 - SELECTED (available)
```

### Port Conflict
```
❌ 3000 - Occupied by aeon-saas-dev (unhealthy dev container)
✅ 3001 - SELECTED (available)
```

## Quick Deployment

```bash
# Deploy production UI
docker compose -f docker-compose.aeon-ui.yml up -d

# Verify
docker ps --filter "name=aeon-ui"
curl http://localhost:3001/api/health

# Access application
open http://localhost:3001
```

## Future Cleanup (Optional)

When ready to reclaim port 3000:
```bash
# Remove unhealthy dev container
docker stop aeon-saas-dev && docker rm aeon-saas-dev

# Update configuration to use port 3000
# Then redeploy
```

## Key Files Modified

1. `docker-compose.aeon-ui.yml`
   - IP: 172.18.0.8 → 172.18.0.9
   - Port: 3000:3000 → 3001:3000
   - NEXTAUTH_URL: localhost:3000 → localhost:3001

2. `docs/DEPLOYMENT_CONFLICT_RESOLUTION.md`
   - Complete conflict analysis
   - Resolution rationale
   - Architecture decision record

## Rationale

**Why not stop aeon-saas-dev?**
- Container is unhealthy but may contain dev work
- Non-disruptive approach allows temporary coexistence
- Port can be reclaimed later when safe

**Why IP 172.18.0.9?**
- Avoids conflict with openspg-server (172.18.0.8)
- Provides dedicated production IP
- Allows future service expansion

**Why port 3001?**
- Avoids conflict with aeon-saas-dev
- Standard practice for multi-instance deployments
- Can revert to 3000 after dev cleanup

---

*Quick Reference | Production Deployment | 2025-11-15*
