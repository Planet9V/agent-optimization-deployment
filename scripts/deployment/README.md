# Deployment Automation Scripts

Comprehensive deployment automation for agent optimization implementations with monitoring, rollback, and validation capabilities.

## Scripts Overview

### 1. deploy-to-dev.sh
Main deployment automation script with full lifecycle management.

**Features:**
- Repository synchronization
- Dependency management
- TypeScript compilation
- Test execution
- Automated deployment
- Backup creation
- Validation checks
- Notification system

**Usage:**
```bash
# Standard deployment
./deploy-to-dev.sh

# Dry-run mode (simulate without changes)
./deploy-to-dev.sh --dry-run

# View help
./deploy-to-dev.sh --help
```

**Workflow:**
1. Validates environment (Node.js, disk space, permissions)
2. Creates backup of current state
3. Pulls latest code from repository
4. Installs dependencies with npm ci
5. Compiles TypeScript to dist/
6. Runs test suite with coverage
7. Deploys build artifacts
8. Verifies deployment success
9. Sends notifications

**Exit Codes:**
- `0` - Success
- `1` - Deployment failed
- `2` - Validation failed

---

### 2. setup-monitoring.sh
Performance monitoring infrastructure setup.

**Features:**
- Metrics collection system
- Real-time dashboard server
- WebSocket live updates
- Alert rule configuration
- systemd service integration
- Prometheus-compatible metrics

**Usage:**
```bash
# Full monitoring setup
./setup-monitoring.sh

# Dry-run mode
./setup-monitoring.sh --dry-run

# View help
./setup-monitoring.sh --help
```

**Components Created:**
- **Metrics Collector** (`monitoring/metrics-collector.js`)
  - Agent performance tracking
  - System resource monitoring
  - Token efficiency metrics
  - Automated metric storage

- **Dashboard Server** (`monitoring/dashboard-server.js`)
  - Real-time web dashboard (port 3030)
  - REST API endpoints
  - WebSocket streaming
  - Historical metrics

- **Dashboard HTML** (`monitoring/dashboard/templates/index.html`)
  - Live performance visualization
  - System health indicators
  - Agent status tracking

- **Alert Configuration** (`monitoring/config/alert-rules.json`)
  - CPU/Memory thresholds
  - Failure rate monitoring
  - Response time alerts
  - Token efficiency warnings

**Accessing Dashboard:**
```bash
# Start monitoring
cd monitoring
./start-monitoring.sh

# Access dashboard
http://localhost:3030

# API endpoints
http://localhost:3030/metrics          # Prometheus format
http://localhost:3030/api/metrics      # JSON format
http://localhost:3030/health           # Health check
```

**systemd Service:**
```bash
# Install service
sudo cp monitoring/config/agent-monitoring.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable agent-monitoring
sudo systemctl start agent-monitoring

# Check status
sudo systemctl status agent-monitoring
```

---

### 3. rollback.sh
Emergency rollback with state preservation.

**Features:**
- Immediate rollback capability
- Current state preservation
- Log archival
- Metrics backup
- Database state restoration
- Dependency reinstallation
- Service restart
- Health validation

**Usage:**
```bash
# Rollback to last known good
./rollback.sh

# List available backups
./rollback.sh --list

# Rollback to specific version
./rollback.sh --to backup-20251112-1045

# Dry-run mode
./rollback.sh --dry-run

# Force rollback (skip confirmations)
./rollback.sh --force

# View help
./rollback.sh --help
```

**Workflow:**
1. Validates backup availability
2. Creates emergency backup of current state
3. Preserves logs and metrics
4. Backs up database state
5. Stops running services
6. Restores files from target backup
7. Restores database if needed
8. Reinstalls dependencies
9. Rebuilds project
10. Restarts services
11. Validates rollback success

**Backup Preservation:**
- Current deployment → `backups/emergency-YYYYMMDD-HHMMSS/`
- Logs → `backups/logs-YYYYMMDD-HHMMSS/`
- Metrics → `backups/metrics/metrics-YYYYMMDD-HHMMSS/`
- Database → `backups/database/db-YYYYMMDD-HHMMSS/`

**Exit Codes:**
- `0` - Rollback successful
- `1` - Rollback failed (validation)
- `2` - Critical failure (manual intervention required)

---

### 4. health-check.sh
Post-deployment validation and system health verification.

**Features:**
- File system validation
- Dependency security scanning
- Build artifact verification
- Syntax validation
- Smoke test execution
- Service health checks
- Process monitoring
- System resource checks
- Configuration validation
- Performance benchmarking

**Usage:**
```bash
# Full health check
./health-check.sh

# Quick check (skip tests and performance)
./health-check.sh --quick

# Post-rollback validation
./health-check.sh --post-rollback

# Verbose output
./health-check.sh --verbose

# View help
./health-check.sh --help
```

**Check Categories:**

1. **File System Checks**
   - Critical files present
   - Build output validation
   - Dependency installation
   - File permissions
   - Disk space usage

2. **Dependency Checks**
   - Security vulnerability scan
   - Outdated package detection
   - Dependency integrity

3. **Build Validation**
   - TypeScript compilation output
   - Implementation artifacts
   - File size validation

4. **Syntax Validation**
   - JavaScript syntax checking
   - All build artifacts validated

5. **Test Execution**
   - Smoke tests with timeout
   - Test suite pass rate
   - Coverage reporting

6. **Service Health**
   - Monitoring service status
   - Port availability
   - Health endpoint response

7. **Process Health**
   - Node.js process detection
   - Memory usage validation
   - Process health metrics

8. **System Resources**
   - CPU usage monitoring
   - Memory usage checking
   - Load average tracking

9. **Configuration Validation**
   - JSON file integrity
   - Configuration syntax
   - Config completeness

10. **Performance Validation**
    - Benchmark execution
    - Performance metrics

**Output Format:**
- Color-coded results (✓ pass, ⚠ warning, ✗ fail)
- Summary statistics
- Pass rate percentage
- Overall health status
- Detailed log file

**Thresholds:**
- CPU: 80% warning threshold
- Memory: 85% warning threshold
- Disk: 90% warning threshold
- Response time: 5000ms threshold

**Exit Codes:**
- `0` - All checks passed (or warnings only)
- `1` - One or more critical failures

---

## Complete Deployment Workflow

### Initial Setup
```bash
# 1. Setup monitoring infrastructure
./setup-monitoring.sh

# 2. Verify monitoring is running
curl http://localhost:3030/health

# 3. Run initial deployment
./deploy-to-dev.sh

# 4. Validate deployment
./health-check.sh
```

### Standard Deployment
```bash
# Deploy new version
./deploy-to-dev.sh

# Health check (automated by deploy script)
./health-check.sh --quick
```

### Emergency Rollback
```bash
# List available backups
./rollback.sh --list

# Rollback to last known good
./rollback.sh

# Verify rollback
./health-check.sh --post-rollback
```

### Monitoring Operations
```bash
# Start monitoring
cd monitoring
./start-monitoring.sh

# View dashboard
open http://localhost:3030

# Check metrics API
curl http://localhost:3030/api/metrics

# Stop monitoring
kill $(cat dashboard.pid)
```

---

## Environment Variables

Optional environment variables for enhanced functionality:

```bash
# Notification configuration
export NOTIFY_EMAIL="admin@example.com"
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."

# Repository configuration
export REPO_URL="https://github.com/yourusername/agent-optimization.git"

# Custom paths
export PROJECT_ROOT="/custom/path/to/project"
export LOG_DIR="/custom/log/directory"
export BACKUP_DIR="/custom/backup/directory"
```

---

## Logging

All scripts create detailed logs in `/var/log/deployment/`:

```
/var/log/deployment/
├── deploy-YYYYMMDD-HHMMSS.log
├── rollback-YYYYMMDD-HHMMSS.log
├── health-check-YYYYMMDD-HHMMSS.log
└── smoke-tests-YYYYMMDD-HHMMSS.log
```

**Log Rotation:**
- Logs are timestamped automatically
- Old logs should be archived manually or via logrotate
- Consider setting up log rotation for production

---

## Error Handling

All scripts implement comprehensive error handling:

1. **Set Options**: `set -euo pipefail`
   - Exit on error
   - Exit on undefined variable
   - Exit on pipe failure

2. **Trap Handlers**: Cleanup on failure
   - Rollback on deployment failure
   - State preservation on rollback failure
   - Resource cleanup on interruption

3. **Validation**: Pre-flight checks
   - Environment validation
   - Dependency verification
   - Disk space checking
   - Permission validation

---

## Security Considerations

1. **No Hardcoded Secrets**: All sensitive data via environment variables
2. **Permission Checks**: Validates file permissions before operations
3. **Backup Verification**: Ensures backups exist before destructive operations
4. **Audit Trail**: Complete operation logging for compliance
5. **Safe Mode**: Dry-run capability for testing

---

## Performance Metrics

Expected execution times:

- **deploy-to-dev.sh**: 2-5 minutes (full deployment)
- **setup-monitoring.sh**: 1-2 minutes (initial setup)
- **rollback.sh**: 1-3 minutes (emergency rollback)
- **health-check.sh**: 30-60 seconds (quick), 2-3 minutes (full)

---

## Troubleshooting

### Deployment Fails
```bash
# Check logs
tail -f /var/log/deployment/deploy-*.log

# Verify environment
./deploy-to-dev.sh --dry-run

# Manual rollback if needed
./rollback.sh
```

### Monitoring Not Starting
```bash
# Check port availability
netstat -tuln | grep 3030

# Check Node.js processes
ps aux | grep node

# Review monitoring logs
tail -f monitoring/logs/dashboard.log
```

### Rollback Issues
```bash
# List available backups
./rollback.sh --list

# Force rollback (skip checks)
./rollback.sh --force

# Manual restoration
cp -r backups/last_known_good/* .
```

### Health Check Failures
```bash
# Verbose output
./health-check.sh --verbose

# Quick check only
./health-check.sh --quick

# Review specific failures
grep "ERROR" /var/log/deployment/health-check-*.log
```

---

## Integration with CI/CD

### GitHub Actions Example
```yaml
name: Deploy to Development

on:
  push:
    branches: [develop]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Setup Node.js
        uses: actions/setup-node@v2
        with:
          node-version: '18'

      - name: Deploy
        run: ./scripts/deployment/deploy-to-dev.sh

      - name: Health Check
        run: ./scripts/deployment/health-check.sh --quick

      - name: Rollback on Failure
        if: failure()
        run: ./scripts/deployment/rollback.sh --force
```

---

## Maintenance

### Regular Tasks
- Review deployment logs weekly
- Clean old backups (keep last 5-10)
- Update alert thresholds based on metrics
- Monitor disk space in backup directory
- Review and update dependencies

### Backup Management
```bash
# Clean old backups (manual)
cd backups
ls -t | grep "backup-" | tail -n +6 | xargs rm -rf

# Check backup disk usage
du -sh backups/*

# Verify backup integrity
./rollback.sh --list
```

---

## Support

For issues or questions:
1. Check logs in `/var/log/deployment/`
2. Run health checks with `--verbose`
3. Review this README for troubleshooting steps
4. Check monitoring dashboard for system metrics

---

**Version**: 1.0.0
**Created**: 2025-11-12
**Status**: PRODUCTION READY

---

## Latest Deployment Status (2025-01-13)

### Week 12-14: Healthcare, Chemical, Manufacturing

**Deployment Complete**: 1,200 equipment, 149 facilities, 100% success rate

**Sector Breakdown**:
- Healthcare: 500 equipment across 60 facilities (hospitals, medical centers, urgent care, clinics)
- Chemical: 300 equipment across 40 facilities (manufacturing, petrochemical, pharmaceutical)
- Manufacturing: 400 equipment across 50 facilities (automotive, aerospace, steel mills, shipbuilding)

**Technical Achievement**: 5-dimensional tagging system (GEO, OPS, REG, TECH, TIME) with avg 13.75 tags per equipment

### Current Total Status

**7 Sectors Deployed** (43.75% of 16 CISA sectors):
1. Energy (800 equipment)
2. Transportation (1,000 equipment)
3. Water (600 equipment)
4. Government Facilities (400 equipment)
5. Healthcare (500 equipment)
6. Chemical (300 equipment)
7. Critical Manufacturing (400 equipment)

**Total**: ~4,000 equipment, ~300 facilities

**9 Sectors Remaining** (56.25%): Communications, Commercial Facilities, Dams, Defense Industrial Base, Emergency Services, Financial Services, Food & Agriculture, Government (expanded), Nuclear

**Target Completion**: Week 24 (all 16 CISA sectors)

### Documentation

See `/docs/INDEX_DEPLOYMENT_DOCUMENTATION.md` for complete documentation index.
