# AEON Backend API Monitoring Setup

**File:** MONITORING_SETUP.md
**Created:** 2025-11-08
**Purpose:** Metrics collection, alerting, and dashboard configuration
**Status:** ACTIVE

## Overview

Comprehensive monitoring setup for AEON backend APIs using:
- **Prometheus** - Metrics collection and storage
- **Grafana** - Visualization and dashboards
- **Docker** - Built-in health checks
- **Application Logs** - Structured logging

---

## Architecture

```
┌─────────────────┐
│   NER API       │─────┐
│   :8000         │     │
└─────────────────┘     │
                        ├──> Prometheus ──> Grafana
┌─────────────────┐     │      :9090          :3000
│   Query API     │─────┤
│   :8001         │     │
└─────────────────┘     │
                        │
┌─────────────────┐     │
│   Neo4j         │─────┘
│   :7474,:7687   │
└─────────────────┘
```

---

## Quick Start

### Option 1: With Production Docker Compose

```bash
cd deployment/docker

# Start with monitoring
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Access dashboards
# Prometheus: http://localhost:9090
# Grafana: http://localhost:3000 (admin/admin)
```

### Option 2: Standalone Monitoring

```bash
# Start APIs first
./deployment/scripts/deploy_ner_v8_api.sh
./deployment/scripts/deploy_query_api.sh

# Start monitoring stack
cd deployment/monitoring
docker-compose up -d
```

---

## Prometheus Configuration

### Setup

Create `/deployment/monitoring/prometheus/prometheus.yml`:

```yaml
# File: prometheus.yml
# Purpose: Prometheus scrape configuration

global:
  scrape_interval: 15s
  evaluation_interval: 15s
  external_labels:
    cluster: 'aeon-backend'
    environment: 'production'

# Alertmanager configuration
alerting:
  alertmanagers:
    - static_configs:
        - targets:
          # - alertmanager:9093

# Load rules
rule_files:
  - "alerts.yml"

# Scrape configurations
scrape_configs:
  # Prometheus self-monitoring
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  # NER API metrics
  - job_name: 'ner-api'
    static_configs:
      - targets: ['aeon-ner-api:8000']
    metrics_path: '/metrics'
    scrape_interval: 10s

  # Query API metrics
  - job_name: 'query-api'
    static_configs:
      - targets: ['aeon-query-api:8000']
    metrics_path: '/metrics'
    scrape_interval: 10s

  # Neo4j metrics
  - job_name: 'neo4j'
    static_configs:
      - targets: ['neo4j:2004']
    metrics_path: '/metrics'
    scrape_interval: 30s

  # Docker metrics (if enabled)
  - job_name: 'docker'
    static_configs:
      - targets: ['docker-host:9323']
    scrape_interval: 30s
```

### Alert Rules

Create `/deployment/monitoring/prometheus/alerts.yml`:

```yaml
# File: alerts.yml
# Purpose: Prometheus alert rules

groups:
  - name: aeon_api_alerts
    interval: 30s
    rules:
      # API Availability
      - alert: APIDown
        expr: up{job=~"ner-api|query-api"} == 0
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "{{ $labels.job }} is down"
          description: "{{ $labels.job }} has been down for more than 2 minutes"

      # High Error Rate
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High error rate on {{ $labels.job }}"
          description: "Error rate is {{ $value }}% over the last 5 minutes"

      # High Response Time
      - alert: HighResponseTime
        expr: histogram_quantile(0.95, http_request_duration_seconds_bucket) > 5
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "High response time on {{ $labels.job }}"
          description: "95th percentile response time is {{ $value }}s"

      # High Memory Usage
      - alert: HighMemoryUsage
        expr: container_memory_usage_bytes / container_spec_memory_limit_bytes > 0.9
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage on {{ $labels.container_name }}"
          description: "Memory usage is {{ $value | humanizePercentage }}"

      # High CPU Usage
      - alert: HighCPUUsage
        expr: rate(container_cpu_usage_seconds_total[5m]) > 0.8
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "High CPU usage on {{ $labels.container_name }}"
          description: "CPU usage is {{ $value | humanizePercentage }}"

      # Database Connection Issues
      - alert: DatabaseConnectionErrors
        expr: rate(neo4j_connection_errors_total[5m]) > 0.1
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Database connection errors"
          description: "{{ $value }} connection errors per second"

      # Low Disk Space
      - alert: LowDiskSpace
        expr: (node_filesystem_avail_bytes / node_filesystem_size_bytes) < 0.1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Low disk space on {{ $labels.instance }}"
          description: "Only {{ $value | humanizePercentage }} disk space remaining"
```

---

## Grafana Configuration

### Initial Setup

```bash
# Access Grafana
open http://localhost:3000

# Default credentials
Username: admin
Password: admin (change on first login)
```

### Add Prometheus Data Source

1. Navigate to **Configuration** → **Data Sources**
2. Click **Add data source**
3. Select **Prometheus**
4. Configure:
   - **Name:** Prometheus
   - **URL:** http://prometheus:9090
   - **Access:** Server (default)
5. Click **Save & Test**

### Import Dashboard

Save this as `/deployment/monitoring/grafana/dashboards/aeon-api-dashboard.json`:

```json
{
  "dashboard": {
    "title": "AEON Backend API Dashboard",
    "tags": ["aeon", "api", "backend"],
    "timezone": "browser",
    "panels": [
      {
        "id": 1,
        "title": "API Requests per Second",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])",
            "legendFormat": "{{ job }}"
          }
        ]
      },
      {
        "id": 2,
        "title": "Response Time (p95)",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, http_request_duration_seconds_bucket)",
            "legendFormat": "{{ job }}"
          }
        ]
      },
      {
        "id": 3,
        "title": "Error Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total{status=~\"5..\"}[5m])",
            "legendFormat": "{{ job }}"
          }
        ]
      },
      {
        "id": 4,
        "title": "Memory Usage",
        "type": "graph",
        "targets": [
          {
            "expr": "container_memory_usage_bytes",
            "legendFormat": "{{ container_name }}"
          }
        ]
      },
      {
        "id": 5,
        "title": "CPU Usage",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(container_cpu_usage_seconds_total[5m])",
            "legendFormat": "{{ container_name }}"
          }
        ]
      },
      {
        "id": 6,
        "title": "Active Connections",
        "type": "stat",
        "targets": [
          {
            "expr": "http_connections_active",
            "legendFormat": "{{ job }}"
          }
        ]
      }
    ]
  }
}
```

---

## Application Metrics

### FastAPI Metrics Endpoint

Add to both NER and Query APIs:

```python
# src/api/metrics.py

from prometheus_client import Counter, Histogram, Gauge
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response
import time

# Metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint']
)

ACTIVE_CONNECTIONS = Gauge(
    'http_connections_active',
    'Active HTTP connections'
)

NEO4J_QUERIES = Counter(
    'neo4j_queries_total',
    'Total Neo4j queries',
    ['query_type', 'status']
)

NEO4J_QUERY_DURATION = Histogram(
    'neo4j_query_duration_seconds',
    'Neo4j query duration',
    ['query_type']
)

# Metrics endpoint
@app.get("/metrics")
async def metrics():
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )

# Middleware for request metrics
@app.middleware("http")
async def metrics_middleware(request, call_next):
    ACTIVE_CONNECTIONS.inc()
    start_time = time.time()

    response = await call_next(request)

    duration = time.time() - start_time
    REQUEST_DURATION.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(duration)

    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()

    ACTIVE_CONNECTIONS.dec()

    return response
```

---

## Health Check Endpoints

### Enhanced Health Check

```python
# src/api/health.py

from fastapi import APIRouter
from datetime import datetime
import psutil

router = APIRouter()

@router.get("/health")
async def health_check():
    """Comprehensive health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "aeon-ner-api",  # or "aeon-query-api"
        "version": "8.0",
        "uptime": get_uptime(),
        "checks": {
            "database": await check_database(),
            "memory": check_memory(),
            "disk": check_disk()
        }
    }

@router.get("/health/ready")
async def readiness_check():
    """Readiness probe"""
    if not await check_database():
        return {"ready": False, "reason": "database_unavailable"}
    return {"ready": True}

@router.get("/health/live")
async def liveness_check():
    """Liveness probe"""
    return {"alive": True}

async def check_database():
    """Check Neo4j connectivity"""
    try:
        # Test connection
        result = await neo4j_driver.execute_query("RETURN 1")
        return True
    except Exception:
        return False

def check_memory():
    """Check memory usage"""
    memory = psutil.virtual_memory()
    return {
        "percent": memory.percent,
        "available_mb": memory.available / (1024 * 1024)
    }

def check_disk():
    """Check disk usage"""
    disk = psutil.disk_usage('/')
    return {
        "percent": disk.percent,
        "free_gb": disk.free / (1024 * 1024 * 1024)
    }
```

---

## Log Aggregation

### Structured Logging

```python
# src/utils/logging_config.py

import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    """Format logs as JSON"""

    def format(self, record):
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }

        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        if hasattr(record, "extra"):
            log_data.update(record.extra)

        return json.dumps(log_data)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("/app/logs/app.log")
    ]
)

# Use JSON formatter
for handler in logging.root.handlers:
    handler.setFormatter(JSONFormatter())
```

### Log Collection

```bash
# View logs
docker logs -f aeon-ner-api

# Filter by level
docker logs aeon-ner-api 2>&1 | grep ERROR

# Export logs
docker logs aeon-ner-api > ner-api.log

# Tail logs with jq
docker logs -f aeon-ner-api 2>&1 | jq '.'
```

---

## Monitoring Checklist

### Daily Monitoring

- [ ] Check Grafana dashboards
- [ ] Review error logs
- [ ] Check alert status
- [ ] Verify health endpoints
- [ ] Review resource usage

### Weekly Monitoring

- [ ] Analyze performance trends
- [ ] Review alert history
- [ ] Check disk space trends
- [ ] Review slow queries
- [ ] Update dashboards if needed

### Monthly Monitoring

- [ ] Capacity planning review
- [ ] Performance optimization review
- [ ] Alert rule tuning
- [ ] Dashboard cleanup
- [ ] Monitoring infrastructure updates

---

## Alert Response Procedures

### Critical Alerts

1. **Acknowledge alert**
2. **Check service status** - Run health check
3. **Review logs** - Check for errors
4. **Assess impact** - User-facing or internal
5. **Escalate if needed** - Contact on-call engineer
6. **Document in incident log**

### Warning Alerts

1. **Investigate cause**
2. **Monitor trend**
3. **Plan remediation**
4. **Document findings**
5. **Schedule fix if needed**

---

## Troubleshooting Monitoring

### Prometheus Not Scraping Targets

```bash
# Check Prometheus targets
curl http://localhost:9090/api/v1/targets

# Check API metrics endpoint
curl http://localhost:8000/metrics

# Check Prometheus logs
docker logs prometheus
```

### Grafana Not Showing Data

```bash
# Test Prometheus connection
curl http://prometheus:9090/api/v1/query?query=up

# Check Grafana logs
docker logs grafana

# Verify data source configuration
```

### Metrics Not Updating

```bash
# Check application logs
docker logs aeon-ner-api

# Verify metrics endpoint
curl http://localhost:8000/metrics

# Check Prometheus configuration
docker exec -it prometheus cat /etc/prometheus/prometheus.yml
```

---

**Last Updated:** 2025-11-08
**Version:** 1.0
