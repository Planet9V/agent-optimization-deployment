# Monitoring and Alerting Procedures

**File:** MONITORING_ALERTING.md
**Created:** 2025-12-04
**Version:** v1.0.0
**Purpose:** System monitoring, metrics collection, and alerting procedures
**Status:** ACTIVE

## Executive Summary

Comprehensive monitoring procedures for tracking system health, performance metrics, resource utilization, and automated alerting for critical issues.

**Key Monitoring Principles:**
- Proactive monitoring prevents reactive firefighting
- Alerts must be actionable (no alert fatigue)
- Baselines enable anomaly detection
- Metrics guide capacity planning

---

## 1. Key Metrics to Monitor

### System Resource Metrics

```yaml
cpu_metrics:
  - cpu_usage_percent (alert > 80%)
  - load_average_1min (alert > 2.0)
  - load_average_5min (alert > 1.5)
  - cpu_steal_time (cloud instances)

memory_metrics:
  - memory_usage_percent (alert > 85%)
  - memory_available_mb (alert < 512MB)
  - swap_usage_percent (alert > 50%)
  - oom_kill_count (alert > 0)

disk_metrics:
  - disk_usage_percent (alert > 80%)
  - disk_free_gb (alert < 10GB)
  - inode_usage_percent (alert > 80%)
  - disk_io_wait_percent (alert > 20%)

network_metrics:
  - network_rx_errors (alert > 10/min)
  - network_tx_errors (alert > 10/min)
  - tcp_connections_count
  - tcp_time_wait_count (alert > 1000)
```

### Application Metrics

```yaml
api_metrics:
  - request_rate_per_second
  - response_time_p50 (alert > 200ms)
  - response_time_p95 (alert > 500ms)
  - response_time_p99 (alert > 1000ms)
  - error_rate_percent (alert > 1%)
  - 5xx_errors_count (alert > 10/min)
  - active_requests_count

database_metrics:
  - connection_pool_size
  - active_connections (alert > 80% of max)
  - idle_connections
  - connection_wait_time (alert > 100ms)
  - query_execution_time_p95 (alert > 1s)
  - deadlocks_count (alert > 0)
  - cache_hit_ratio (alert < 90%)
  - replication_lag_seconds (alert > 60s)

model_metrics:
  - model_load_time_seconds
  - inference_time_p95 (alert > 500ms)
  - model_memory_usage_mb
  - prediction_queue_depth (alert > 100)
```

---

## 2. Monitoring Dashboard Setup

### Install and Configure Prometheus + Grafana

**docker-compose.monitoring.yml:**

```yaml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    container_name: ner11_prometheus
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--storage.tsdb.retention.time=30d'
    ports:
      - "9090:9090"
    restart: unless-stopped

  grafana:
    image: grafana/grafana:latest
    container_name: ner11_grafana
    volumes:
      - grafana_data:/var/lib/grafana
      - ./monitoring/grafana/dashboards:/etc/grafana/provisioning/dashboards
      - ./monitoring/grafana/datasources:/etc/grafana/provisioning/datasources
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
      - GF_USERS_ALLOW_SIGN_UP=false
    ports:
      - "3001:3000"
    depends_on:
      - prometheus
    restart: unless-stopped

  node_exporter:
    image: prom/node-exporter:latest
    container_name: ner11_node_exporter
    command:
      - '--path.rootfs=/host'
    volumes:
      - '/:/host:ro,rslave'
    ports:
      - "9100:9100"
    restart: unless-stopped

  postgres_exporter:
    image: prometheuscommunity/postgres-exporter:latest
    container_name: ner11_postgres_exporter
    environment:
      - DATA_SOURCE_NAME=postgresql://postgres:password@postgres:5432/ner11_db?sslmode=disable
    ports:
      - "9187:9187"
    depends_on:
      - postgres
    restart: unless-stopped

volumes:
  prometheus_data:
  grafana_data:
```

**Prometheus Configuration (monitoring/prometheus.yml):**

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'node_exporter'
    static_configs:
      - targets: ['node_exporter:9100']

  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres_exporter:9187']

  - job_name: 'api'
    static_configs:
      - targets: ['api:8000']
    metrics_path: '/metrics'

  - job_name: 'docker'
    static_configs:
      - targets: ['docker_host:9323']
```

**Start Monitoring Stack:**

```bash
# Start monitoring services
docker-compose -f docker-compose.monitoring.yml up -d

# Verify Prometheus
curl http://localhost:9090/-/healthy
# Expected: HTTP 200 OK

# Verify Node Exporter
curl http://localhost:9100/metrics | head
# Expected: Metrics output

# Access Grafana
open http://localhost:3001
# Login: admin / admin
```

---

## 3. Real-Time Monitoring Commands

### Docker Container Monitoring

```bash
# Real-time container stats
docker stats

# Expected output:
# CONTAINER ID   NAME                CPU %   MEM USAGE / LIMIT     MEM %   NET I/O
# abc123         ner11_postgres_1    5.2%    250MiB / 2GiB         12.5%   1.2MB / 800KB
# def456         ner11_api_1         15.3%   1.2GiB / 4GiB         30.0%   5MB / 3MB
# ghi789         ner11_frontend_1    2.1%    150MiB / 1GiB         15.0%   800KB / 500KB

# Monitor specific container
docker stats ner11_api_1 --no-stream

# Container logs with timestamps
docker-compose logs -f --timestamps api

# Monitor container events
docker events --filter 'container=ner11_api_1'
```

---

### System Resource Monitoring

```bash
# CPU usage per core
mpstat -P ALL 1 5
# Monitor for cores consistently >80%

# Memory usage breakdown
free -h
# Alert if "available" < 512MB

# Disk usage and inodes
df -h
df -i
# Alert if any filesystem >80%

# Disk I/O statistics
iostat -x 1 5
# Monitor %util column (alert >80%)

# Network statistics
netstat -s | grep -E "failed|error|drop"
# Alert on increasing error counts

# Process-level resource usage
top -b -n 1 | head -20
# or
htop  # Interactive

# Database connections
docker-compose exec postgres psql -U postgres -c "SELECT count(*), state FROM pg_stat_activity GROUP BY state;"
# Expected: Mix of active and idle connections
```

---

### Application Health Monitoring

```bash
# API health endpoint
curl -X GET http://localhost:8000/health
# Expected: {"status": "healthy", "timestamp": "...", "uptime_seconds": 3600}

# Detailed metrics endpoint
curl -X GET http://localhost:8000/metrics
# Expected: Prometheus-formatted metrics

# Database health check
curl -X GET http://localhost:8000/api/v1/db/health
# Expected: {"database": "connected", "pool_size": 10, "active_connections": 2}

# Model status
curl -X GET http://localhost:8000/api/v1/models/status
# Expected: {"models_loaded": true, "load_time_seconds": 5.2}

# API response time test
time curl -X GET http://localhost:8000/api/v1/vendor-equipment/
# Expected: real time <200ms
```

---

## 4. Log Analysis Procedures

### Centralized Log Aggregation

**Setup Loki for Log Aggregation:**

```yaml
# Add to docker-compose.monitoring.yml

  loki:
    image: grafana/loki:latest
    container_name: ner11_loki
    ports:
      - "3100:3100"
    volumes:
      - ./monitoring/loki-config.yml:/etc/loki/local-config.yaml
      - loki_data:/loki
    restart: unless-stopped

  promtail:
    image: grafana/promtail:latest
    container_name: ner11_promtail
    volumes:
      - /var/log:/var/log
      - ./monitoring/promtail-config.yml:/etc/promtail/config.yml
      - /var/lib/docker/containers:/var/lib/docker/containers:ro
    command: -config.file=/etc/promtail/config.yml
    restart: unless-stopped
```

---

### Log Analysis Commands

```bash
# Find errors in API logs (last 1 hour)
docker-compose logs --since 1h api | grep -E "ERROR|CRITICAL|Exception"

# Count errors by type
docker-compose logs --since 1h api | grep ERROR | awk '{print $NF}' | sort | uniq -c | sort -rn

# Find slow database queries
docker-compose exec postgres psql -U postgres -c "SELECT query, mean_exec_time, calls FROM pg_stat_statements ORDER BY mean_exec_time DESC LIMIT 10;"

# Detect API endpoint failures
docker-compose logs --since 1h api | grep "500 Internal Server Error" | wc -l
# Alert if count >10

# Find memory issues
docker-compose logs --since 1h api | grep -E "MemoryError|OutOfMemory"

# Track API request patterns
docker-compose logs --since 1h api | grep "INFO.*GET\|POST\|PUT\|DELETE" | awk '{print $(NF-1)}' | sort | uniq -c | sort -rn

# Database deadlock detection
docker-compose exec postgres psql -U postgres -c "SELECT * FROM pg_stat_database_conflicts WHERE deadlocks > 0;"
```

---

### Log Rotation Configuration

```bash
# Configure logrotate for Docker logs
sudo tee /etc/logrotate.d/docker-ner11 << EOF
/var/lib/docker/containers/*/*.log {
    rotate 7
    daily
    compress
    size=50M
    missingok
    delaycompress
    copytruncate
}
EOF

# Test logrotate configuration
sudo logrotate -d /etc/logrotate.d/docker-ner11
```

---

## 5. Alert Thresholds and Escalation

### Alert Configuration (Prometheus alerting rules)

**monitoring/alert_rules.yml:**

```yaml
groups:
  - name: system_alerts
    interval: 30s
    rules:
      - alert: HighCPUUsage
        expr: 100 - (avg by(instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High CPU usage detected"
          description: "CPU usage is above 80% for 5 minutes on {{ $labels.instance }}"

      - alert: HighMemoryUsage
        expr: (node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100 > 85
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage detected"
          description: "Memory usage is above 85% on {{ $labels.instance }}"

      - alert: DiskSpaceLow
        expr: (node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"}) * 100 < 20
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Disk space critically low"
          description: "Less than 20% disk space available on {{ $labels.instance }}"

  - name: application_alerts
    interval: 30s
    rules:
      - alert: APIHighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.01
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "API error rate above 1%"
          description: "API is returning {{ $value }}% errors"

      - alert: APISlowResponse
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 0.5
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "API response time degraded"
          description: "95th percentile response time is {{ $value }}s"

      - alert: DatabaseConnectionPoolExhausted
        expr: pg_stat_database_numbackends / pg_settings_max_connections > 0.8
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Database connection pool nearly exhausted"
          description: "{{ $value }}% of database connections in use"

  - name: data_alerts
    interval: 60s
    rules:
      - alert: DatabaseReplicationLag
        expr: pg_replication_lag_seconds > 60
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Database replication lag high"
          description: "Replication lag is {{ $value }} seconds"
```

---

### Escalation Procedures

**Alert Severity Levels:**

```yaml
INFO:
  description: "Informational, no action required"
  examples:
    - Service restarted successfully
    - Scheduled maintenance completed
  notification: Log only

WARNING:
  description: "Potential issue, monitor closely"
  examples:
    - CPU usage >80% for 5 minutes
    - Memory usage >85%
    - Disk usage >80%
    - API response time >500ms
  notification: Slack/Email
  response_time: 30 minutes
  escalation: If not resolved in 1 hour

CRITICAL:
  description: "Service impact, immediate action required"
  examples:
    - Service down
    - Database connection failed
    - Disk space <10%
    - API error rate >1%
  notification: PagerDuty + SMS + Email
  response_time: 15 minutes
  escalation: Immediate escalation to on-call engineer

EMERGENCY:
  description: "Data loss risk, all hands on deck"
  examples:
    - Database corruption detected
    - Security breach
    - Complete system failure
  notification: All channels + phone calls
  response_time: 5 minutes
  escalation: Escalate to CTO immediately
```

---

### Alert Notification Configuration

**Slack Webhook Integration:**

```bash
# Install alertmanager
docker-compose -f docker-compose.monitoring.yml up -d alertmanager

# Configure Slack webhook in monitoring/alertmanager.yml
route:
  receiver: 'slack-notifications'
  group_by: ['alertname', 'severity']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 12h

receivers:
  - name: 'slack-notifications'
    slack_configs:
      - api_url: 'https://hooks.slack.com/services/YOUR/WEBHOOK/URL'
        channel: '#ner11-alerts'
        title: '{{ .GroupLabels.alertname }}'
        text: '{{ range .Alerts }}{{ .Annotations.description }}\n{{ end }}'
```

---

## 6. Performance Baseline Establishment

### Baseline Metrics Collection

```bash
#!/bin/bash
# save as: scripts/establish_baseline.sh

set -euo pipefail

BASELINE_DIR="/monitoring/baselines"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p "$BASELINE_DIR"

echo "📊 Establishing performance baseline..."

# System metrics baseline
cat > "$BASELINE_DIR/system_baseline_${TIMESTAMP}.txt" << EOF
=== System Baseline - $(date) ===

CPU:
$(mpstat -P ALL 1 1)

Memory:
$(free -h)

Disk:
$(df -h)
$(df -i)

Network:
$(netstat -s | grep -E "failed|error|drop")

Load Average:
$(uptime)
EOF

# Application metrics baseline
cat > "$BASELINE_DIR/app_baseline_${TIMESTAMP}.json" << EOF
{
  "timestamp": "$(date -Iseconds)",
  "api_health": $(curl -s http://localhost:8000/health),
  "db_health": $(curl -s http://localhost:8000/api/v1/db/health),
  "model_status": $(curl -s http://localhost:8000/api/v1/models/status)
}
EOF

# API response time baseline (100 requests)
echo "Testing API response times..."
for i in {1..100}; do
    curl -w "%{time_total}\n" -o /dev/null -s http://localhost:8000/api/v1/vendor-equipment/
done | awk '{sum+=$1; sumsq+=$1*$1} END {print "Mean:", sum/NR, "StdDev:", sqrt(sumsq/NR - (sum/NR)^2)}' > "$BASELINE_DIR/api_response_baseline_${TIMESTAMP}.txt"

# Database query performance baseline
docker-compose exec -T postgres psql -U postgres ner11_db << EOF > "$BASELINE_DIR/db_query_baseline_${TIMESTAMP}.txt"
SELECT
  schemaname,
  tablename,
  pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size,
  pg_size_pretty(pg_relation_size(schemaname||'.'||tablename)) AS table_size,
  pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename) - pg_relation_size(schemaname||'.'||tablename)) AS index_size
FROM pg_tables
WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
EOF

echo "✅ Baseline established in $BASELINE_DIR/"
ls -lh "$BASELINE_DIR/"
```

**Usage:**
```bash
chmod +x scripts/establish_baseline.sh

# Run during normal operation (not peak load)
./scripts/establish_baseline.sh

# Run weekly to track trends
crontab -e
# Add: 0 0 * * 0 /path/to/scripts/establish_baseline.sh
```

---

## 7. Monitoring Dashboards

### Grafana Dashboard Import

**Pre-built Dashboard IDs (import in Grafana):**

```yaml
system_monitoring:
  - dashboard_id: 1860  # Node Exporter Full
  - dashboard_id: 405   # Docker Containers

database_monitoring:
  - dashboard_id: 9628  # PostgreSQL Database
  - dashboard_id: 455   # PostgreSQL Statistics

application_monitoring:
  - dashboard_id: 6417  # FastAPI
  - dashboard_id: 3662  # API Performance
```

**Import in Grafana:**
1. Navigate to http://localhost:3001
2. Login (admin/admin)
3. Click "+" → Import
4. Enter dashboard ID
5. Select Prometheus data source
6. Click Import

---

## 8. Quick Reference Monitoring Commands

```bash
# Real-time container stats
docker stats

# Check all service health
./scripts/startup_verify.sh

# View recent errors
docker-compose logs --since 10m | grep -E "ERROR|CRITICAL"

# Database connection count
docker-compose exec postgres psql -U postgres -c "SELECT count(*) FROM pg_stat_activity;"

# API response time
time curl -s http://localhost:8000/api/v1/health > /dev/null

# Disk usage
df -h | grep -E "/$|/var"

# Memory pressure
free -h

# CPU load
uptime

# Network errors
netstat -s | grep -E "failed|error" | grep -v ": 0"

# Container resource limits
docker inspect ner11_api_1 | jq '.[0].HostConfig.Memory'
```

---

## Related Runbooks

- **Incident Response:** docs/runbooks/incident-response/
- **Performance Degradation:** docs/runbooks/incident-response/PERFORMANCE_DEGRADATION.md
- **Capacity Planning:** docs/runbooks/scaling/CAPACITY_PLANNING.md

---

**Document Version History:**
- v1.0.0 (2025-12-04): Initial monitoring and alerting procedures

**Last Verified:** 2025-12-04
**Next Review Date:** 2025-12-18
