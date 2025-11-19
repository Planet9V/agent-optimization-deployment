# Deployment Scripts - Quick Reference

## One-Line Commands

### Deploy
```bash
./deploy-to-dev.sh                    # Full deployment
./deploy-to-dev.sh --dry-run          # Test without changes
```

### Monitor
```bash
./setup-monitoring.sh                 # Setup monitoring
cd monitoring && ./start-monitoring.sh # Start dashboard
open http://localhost:3030            # View dashboard
```

### Rollback
```bash
./rollback.sh --list                  # List backups
./rollback.sh                         # Rollback to last good
./rollback.sh --to backup-20251112    # Rollback to specific
```

### Health Check
```bash
./health-check.sh                     # Full check
./health-check.sh --quick             # Quick check (30s)
```

## Common Scenarios

### New Deployment
```bash
./deploy-to-dev.sh && ./health-check.sh --quick
```

### Emergency Rollback
```bash
./rollback.sh && ./health-check.sh --post-rollback
```

### Setup New Environment
```bash
./setup-monitoring.sh && ./deploy-to-dev.sh && ./health-check.sh
```

### Test Before Deploy
```bash
./deploy-to-dev.sh --dry-run
```

## Monitoring Quick Start

```bash
# Setup (one-time)
./setup-monitoring.sh

# Start
cd monitoring
./start-monitoring.sh

# Access
http://localhost:3030              # Dashboard
http://localhost:3030/metrics      # Prometheus metrics
http://localhost:3030/api/metrics  # JSON API

# Stop
kill $(cat dashboard.pid)
```

## Troubleshooting

### Deployment Failed
```bash
tail -f /var/log/deployment/deploy-*.log
./rollback.sh
```

### Check System Health
```bash
./health-check.sh --verbose
```

### View Backups
```bash
./rollback.sh --list
ls -lh backups/
```

### Check Disk Space
```bash
df -h .
du -sh backups/*
```

## File Locations

| Item | Location |
|------|----------|
| Scripts | `/home/jim/2_OXOT_Projects_Dev/scripts/deployment/` |
| Logs | `/var/log/deployment/` |
| Backups | `/home/jim/2_OXOT_Projects_Dev/tests/backups/` |
| Monitoring | `/home/jim/2_OXOT_Projects_Dev/tests/monitoring/` |

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Failure (recoverable) |
| 2 | Critical failure (manual intervention) |

## Help Commands

```bash
./deploy-to-dev.sh --help
./setup-monitoring.sh --help
./rollback.sh --help
./health-check.sh --help
```

## Environment Variables (Optional)

```bash
export NOTIFY_EMAIL="admin@example.com"
export SLACK_WEBHOOK_URL="https://hooks.slack.com/..."
```

## Safety Features

- ✓ Dry-run mode for all scripts
- ✓ Automatic backups before deployment
- ✓ Emergency rollback capability
- ✓ Comprehensive logging
- ✓ Health validation
- ✓ Resource monitoring

## Best Practices

1. **Always test first**: Use `--dry-run` mode
2. **Monitor resources**: Check dashboard after deployment
3. **Keep backups**: Don't delete recent backups
4. **Review logs**: Check logs after operations
5. **Regular health checks**: Run weekly health checks

---

**Quick Start**: `./setup-monitoring.sh && ./deploy-to-dev.sh && open http://localhost:3030`
