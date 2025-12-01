# WAVE 4 Implementation: Production Deployment Guide

**Document**: IMPLEMENTATION_DEPLOYMENT_GUIDE.md
**Created**: 2025-11-25 22:30:00 UTC
**Version**: v1.0.0
**Status**: ACTIVE

## Executive Summary

This document provides comprehensive production deployment procedures for WAVE 4, covering infrastructure setup, containerization, Kubernetes orchestration, CI/CD pipelines, monitoring, and disaster recovery. All components are configured for high availability, scalability, and enterprise-grade security compliance.

**Target**: 900 lines of deployment specifications and operational procedures.

---

## Table of Contents

1. [Deployment Architecture](#deployment-architecture)
2. [Infrastructure Setup](#infrastructure-setup)
3. [Container Orchestration](#container-orchestration)
4. [CI/CD Pipeline](#cicd-pipeline)
5. [Security & Compliance](#security--compliance)
6. [Monitoring & Logging](#monitoring--logging)
7. [Disaster Recovery](#disaster-recovery)
8. [Operations & Maintenance](#operations--maintenance)

---

## Deployment Architecture

### Production Infrastructure

```
┌─────────────────────────────────────────────────────────────┐
│                   Production Environment                    │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │          Load Balancer (AWS NLB / Traefik)           │   │
│  │              Terminates TLS/SSL                      │   │
│  └──────────────────────────────────────────────────────┘   │
│                          ↓                                   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │          Kubernetes Cluster (3+ nodes)               │   │
│  │     ┌─────────────────┬─────────────────┐            │   │
│  │     │  Node 1         │  Node 2         │  Node 3    │   │
│  │     │  ┌───────────┐  │  ┌───────────┐  │            │   │
│  │     │  │API Pod (3)│  │  │API Pod (3)│  │            │   │
│  │     │  │Frontend(3)│  │  │Frontend(3)│  │            │   │
│  │     │  │GraphQL(2) │  │  │Monitoring │  │            │   │
│  │     │  └───────────┘  │  └───────────┘  │            │   │
│  │     └─────────────────┴─────────────────┘            │   │
│  └──────────────────────────────────────────────────────┘   │
│                          ↓                                   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │            Persistent Storage Layer                   │   │
│  │     ┌──────────────┬──────────────┬──────────────┐   │   │
│  │     │Neo4j Cluster │PostgreSQL HA │MongoDB Shard │   │   │
│  │     │   (3 nodes)  │  (3 replicas)│  (3 shards)  │   │   │
│  │     └──────────────┴──────────────┴──────────────┘   │   │
│  │     ┌──────────────────────────────────────────┐   │   │
│  │     │      Redis Cluster (6 nodes)              │   │   │
│  │     └──────────────────────────────────────────┘   │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │   Monitoring & Logging (Prometheus, Grafana, ELK)    │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Environment Tiers

| Environment | Purpose | Nodes | Replicas | Backups |
|-------------|---------|-------|----------|---------|
| Development | Testing & Development | 1 | 1 | Daily |
| Staging | Pre-production Testing | 3 | 2 | Daily |
| Production | Live System | 5+ | 3+ | Hourly |

---

## Infrastructure Setup

### AWS Infrastructure as Code (Terraform)

```hcl
# terraform/main.tf

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.20"
    }
  }

  backend "s3" {
    bucket         = "wave4-terraform-state"
    key            = "production/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}

provider "aws" {
  region = var.aws_region
  default_tags {
    tags = {
      Project     = "WAVE4"
      Environment = var.environment
      ManagedBy   = "Terraform"
    }
  }
}

# VPC Configuration
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "wave4-vpc-${var.environment}"
  }
}

# EKS Cluster
resource "aws_eks_cluster" "main" {
  name            = "wave4-${var.environment}"
  version         = "1.27"
  role_arn        = aws_iam_role.eks_cluster_role.arn
  vpc_config {
    subnet_ids              = concat(aws_subnet.private[*].id, aws_subnet.public[*].id)
    endpoint_private_access = true
    endpoint_public_access  = true
    public_access_cidrs     = var.allowed_cidrs
  }

  enabled_cluster_log_types = [
    "api",
    "audit",
    "authenticator",
    "controllerManager",
    "scheduler"
  ]

  depends_on = [
    aws_iam_role_policy_attachment.eks_cluster_policy
  ]

  tags = {
    Name = "wave4-eks-${var.environment}"
  }
}

# EKS Node Group
resource "aws_eks_node_group" "main" {
  cluster_name    = aws_eks_cluster.main.name
  node_group_name = "wave4-node-group"
  node_role_arn   = aws_iam_role.eks_node_role.arn
  subnet_ids      = aws_subnet.private[*].id
  version         = "1.27"

  scaling_config {
    desired_size = 5
    max_size     = 10
    min_size     = 3
  }

  instance_types = ["c5.2xlarge"]

  disk_size = 100

  tags = {
    Name = "wave4-node-group"
  }

  depends_on = [
    aws_iam_role_policy_attachment.eks_node_policy,
    aws_iam_role_policy_attachment.eks_cni_policy
  ]
}

# RDS (PostgreSQL)
resource "aws_db_instance" "postgres" {
  identifier              = "wave4-postgres-${var.environment}"
  engine                  = "postgres"
  engine_version          = "15.3"
  instance_class          = "db.r5.2xlarge"
  allocated_storage       = 200
  storage_type            = "gp3"
  storage_encrypted       = true
  skip_final_snapshot     = false
  final_snapshot_identifier = "wave4-postgres-final-${var.environment}"

  db_name  = "wave4_threat_intel"
  username = "admin"
  password = random_password.postgres_password.result

  multi_az            = true
  publicly_accessible = false
  vpc_security_group_ids = [aws_security_group.rds.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name

  backup_retention_period = 30
  backup_window          = "03:00-04:00"
  maintenance_window     = "mon:04:00-mon:05:00"
  copy_tags_to_snapshot  = true
  enable_iam_database_authentication = true

  tags = {
    Name = "wave4-postgres-${var.environment}"
  }
}

# DocumentDB (MongoDB)
resource "aws_docdb_cluster" "main" {
  cluster_identifier      = "wave4-docdb-${var.environment}"
  engine                  = "docdb"
  master_username         = "admin"
  master_password         = random_password.docdb_password.result
  backup_retention_period = 30
  preferred_backup_window = "03:00-04:00"
  skip_final_snapshot     = false

  db_subnet_group_name            = aws_docdb_subnet_group.main.name
  db_cluster_parameter_group_name = aws_docdb_cluster_parameter_group.main.name
  vpc_security_group_ids          = [aws_security_group.docdb.id]

  storage_encrypted = true
  kms_key_id        = aws_kms_key.docdb.arn

  tags = {
    Name = "wave4-docdb-${var.environment}"
  }
}

# ElastiCache (Redis)
resource "aws_elasticache_replication_group" "redis" {
  replication_group_description = "WAVE4 Redis Cluster"
  replication_group_id           = "wave4-redis-${var.environment}"
  engine                         = "redis"
  engine_version                 = "7.0"
  node_type                      = "cache.r6g.xlarge"
  num_cache_clusters             = 3
  parameter_group_name           = aws_elasticache_parameter_group.redis.name
  port                           = 6379
  parameter_group_family         = "redis7"

  automatic_failover_enabled = true
  multi_az_enabled           = true
  transit_encryption_enabled = true
  auth_token                 = random_password.redis_auth_token.result

  subnet_group_name          = aws_elasticache_subnet_group.main.name
  security_group_ids         = [aws_security_group.redis.id]

  at_rest_encryption_enabled = true
  kms_key_id                 = aws_kms_key.redis.arn

  automatic_minor_version_upgrade = true
  maintenance_window              = "mon:04:00-mon:05:00"

  log_delivery_configuration {
    destination      = aws_cloudwatch_log_group.redis.name
    destination_type = "cloudwatch-logs"
    log_format       = "json"
    log_type         = "engine-log"
  }

  tags = {
    Name = "wave4-redis-${var.environment}"
  }
}

# S3 for backups
resource "aws_s3_bucket" "backups" {
  bucket = "wave4-backups-${var.environment}-${data.aws_caller_identity.current.account_id}"

  tags = {
    Name = "wave4-backups"
  }
}

resource "aws_s3_bucket_versioning" "backups" {
  bucket = aws_s3_bucket.backups.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "backups" {
  bucket = aws_s3_bucket.backups.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kmaster_key_id    = aws_kms_key.s3.arn
    }
  }
}
```

---

## Container Orchestration

### Kubernetes Deployment Manifests

```yaml
# kubernetes/backend-deployment.yaml

apiVersion: v1
kind: Namespace
metadata:
  name: wave4-production

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend-api
  namespace: wave4-production
  labels:
    app: backend-api
    version: v1
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: backend-api
  template:
    metadata:
      labels:
        app: backend-api
        version: v1
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8000"
        prometheus.io/path: "/metrics"
    spec:
      serviceAccountName: backend-api
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000

      containers:
      - name: api
        image: 534359854279.dkr.ecr.us-east-1.amazonaws.com/wave4/backend:latest
        imagePullPolicy: Always

        ports:
        - containerPort: 8000
          name: http
          protocol: TCP

        env:
        - name: ENVIRONMENT
          value: "production"
        - name: LOG_LEVEL
          value: "info"
        - name: NEO4J_URI
          valueFrom:
            secretKeyRef:
              name: databases
              key: neo4j-uri
        - name: POSTGRES_URL
          valueFrom:
            secretKeyRef:
              name: databases
              key: postgres-url
        - name: MONGODB_URL
          valueFrom:
            secretKeyRef:
              name: databases
              key: mongodb-url
        - name: REDIS_URL
          valueFrom:
            secretKeyRef:
              name: databases
              key: redis-url
        - name: JWT_SECRET
          valueFrom:
            secretKeyRef:
              name: api-secrets
              key: jwt-secret

        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3

        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 2

        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"

        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          runAsNonRoot: true
          capabilities:
            drop:
              - ALL

        volumeMounts:
        - name: tmp
          mountPath: /tmp
        - name: cache
          mountPath: /app/cache

      volumes:
      - name: tmp
        emptyDir: {}
      - name: cache
        emptyDir: {}

      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - backend-api
              topologyKey: kubernetes.io/hostname

---
apiVersion: v1
kind: Service
metadata:
  name: backend-api-service
  namespace: wave4-production
spec:
  selector:
    app: backend-api
  ports:
  - port: 80
    targetPort: 8000
    protocol: TCP
  type: ClusterIP

---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: backend-api-hpa
  namespace: wave4-production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: backend-api
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15

---
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: backend-api-pdb
  namespace: wave4-production
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: backend-api

---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: backend-api-network-policy
  namespace: wave4-production
spec:
  podSelector:
    matchLabels:
      app: backend-api
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: wave4-production
    ports:
    - protocol: TCP
      port: 8000
  egress:
  - to:
    - namespaceSelector: {}
    ports:
    - protocol: TCP
      port: 7687  # Neo4j
    - protocol: TCP
      port: 5432  # PostgreSQL
    - protocol: TCP
      port: 27017 # MongoDB
    - protocol: TCP
      port: 6379  # Redis
  - to:
    - namespaceSelector: {}
    ports:
    - protocol: TCP
      port: 53   # DNS
    protocol: UDP
```

---

## CI/CD Pipeline

### GitHub Actions Workflow

```yaml
# .github/workflows/deploy-production.yml

name: Deploy to Production

on:
  push:
    branches: [ main ]
    paths:
      - 'backend/**'
      - 'frontend/**'
      - 'kubernetes/**'
  workflow_dispatch:

env:
  AWS_REGION: us-east-1
  ECR_REGISTRY: 534359854279.dkr.ecr.us-east-1.amazonaws.com
  DOCKER_BUILDKIT: 1

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read

    steps:
    - uses: actions/checkout@v4

    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v2
      with:
        role-to-assume: arn:aws:iam::534359854279:role/github-actions-role
        aws-region: ${{ env.AWS_REGION }}

    - name: Login to Amazon ECR
      id: login-ecr
      uses: aws-actions/amazon-ecr-login@v2

    - name: Build, tag, and push backend image
      env:
        ECR_REPOSITORY: wave4/backend
        IMAGE_TAG: ${{ github.sha }}
      run: |
        docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG \
          -t $ECR_REGISTRY/$ECR_REPOSITORY:latest \
          -f backend/Dockerfile backend/
        docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
        docker push $ECR_REGISTRY/$ECR_REPOSITORY:latest

    - name: Build, tag, and push frontend image
      env:
        ECR_REPOSITORY: wave4/frontend
        IMAGE_TAG: ${{ github.sha }}
      run: |
        docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG \
          -t $ECR_REGISTRY/$ECR_REPOSITORY:latest \
          -f frontend/Dockerfile frontend/
        docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
        docker push $ECR_REGISTRY/$ECR_REPOSITORY:latest

    - name: Update Kubernetes manifests
      run: |
        cd kubernetes
        sed -i "s|image:.*|image: $ECR_REGISTRY/wave4/backend:${{ github.sha }}|g" backend-deployment.yaml
        sed -i "s|image:.*|image: $ECR_REGISTRY/wave4/frontend:${{ github.sha }}|g" frontend-deployment.yaml

    - name: Deploy to EKS
      run: |
        aws eks update-kubeconfig --region $AWS_REGION --name wave4-production
        kubectl apply -f kubernetes/
        kubectl rollout status deployment/backend-api -n wave4-production --timeout=5m
        kubectl rollout status deployment/frontend -n wave4-production --timeout=5m

    - name: Verify deployment
      run: |
        kubectl get deployments,pods,services -n wave4-production
        kubectl describe nodes

  integration-tests:
    needs: build-and-push
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4

    - name: Run integration tests
      run: |
        npm install
        npm run test:integration

    - name: Run smoke tests
      run: |
        ./scripts/smoke-tests.sh https://api.wave4.com

  monitoring:
    needs: build-and-push
    runs-on: ubuntu-latest
    steps:
    - name: Create deployment annotation in Datadog
      run: |
        curl -X POST https://api.datadoghq.com/api/v1/events \
          -H "DD-API-KEY: ${{ secrets.DATADOG_API_KEY }}" \
          -d "{
            \"title\": \"WAVE4 Deployment\",
            \"text\": \"Deployed to production: ${{ github.sha }}\",
            \"priority\": \"normal\",
            \"tags\": [\"environment:production\", \"service:wave4\"]
          }"
```

---

## Security & Compliance

### Security Scanning

```yaml
# .github/workflows/security-scan.yml

name: Security Scan

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 2 * * *'

jobs:
  trivy-scan:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4

    - name: Run Trivy vulnerability scanner
      uses: aquasecurity/trivy-action@master
      with:
        scan-type: 'fs'
        scan-ref: '.'
        format: 'sarif'
        output: 'trivy-results.sarif'

    - name: Upload Trivy results to GitHub Security
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: 'trivy-results.sarif'

  sonarqube-scan:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
      with:
        fetch-depth: 0

    - name: SonarQube scan
      uses: SonarSource/sonarqube-scan-action@master
      env:
        SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }}
        SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}

  sast-scan:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4

    - name: Run SAST with Semgrep
      uses: returntocorp/semgrep-action@v1
      with:
        config: >-
          p/security-audit
          p/owasp-top-ten
          p/python
```

### Pod Security Policy

```yaml
# kubernetes/pod-security-policy.yaml

apiVersion: policy/v1beta1
kind: PodSecurityPolicy
metadata:
  name: restricted
spec:
  privileged: false
  allowPrivilegeEscalation: false
  requiredDropCapabilities:
    - ALL
  allowedCapabilities: []
  volumes:
    - 'configMap'
    - 'emptyDir'
    - 'projected'
    - 'secret'
    - 'downwardAPI'
    - 'persistentVolumeClaim'
  hostNetwork: false
  hostIPC: false
  hostPID: false
  runAsUser:
    rule: 'MustRunAsNonRoot'
  seLinux:
    rule: 'MustRunAs'
    seLinuxOptions:
      level: "s0:c123,c456"
  supplementalGroups:
    rule: 'MustRunAs'
    ranges:
      - min: 1
        max: 65535
  fsGroup:
    rule: 'MustRunAs'
    ranges:
      - min: 1
        max: 65535
  readOnlyRootFilesystem: true
```

---

## Monitoring & Logging

### Prometheus Configuration

```yaml
# kubernetes/prometheus-config.yaml

apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
  namespace: monitoring
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s
      evaluation_interval: 15s
      external_labels:
        cluster: 'wave4-production'
        environment: 'production'

    alerting:
      alertmanagers:
      - static_configs:
        - targets:
          - alertmanager:9093

    rule_files:
      - '/etc/prometheus/rules/*.yml'

    scrape_configs:
    - job_name: 'kubernetes-apiservers'
      kubernetes_sd_configs:
      - role: endpoints
      scheme: https
      tls_config:
        ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
      bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
      relabel_configs:
      - source_labels: [__meta_kubernetes_namespace, __meta_kubernetes_service_name, __meta_kubernetes_endpoint_port_name]
        action: keep
        regex: default;kubernetes;https

    - job_name: 'wave4-api'
      static_configs:
      - targets: ['backend-api-service:8000']
      metrics_path: '/metrics'

    - job_name: 'neo4j'
      static_configs:
      - targets: ['neo4j:7474']

    - job_name: 'postgres'
      static_configs:
      - targets: ['postgres-exporter:9187']

    - job_name: 'mongodb'
      static_configs:
      - targets: ['mongodb-exporter:9216']

    - job_name: 'redis'
      static_configs:
      - targets: ['redis-exporter:9121']
```

### Alert Rules

```yaml
# kubernetes/alert-rules.yaml

apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: wave4-alerts
  namespace: monitoring
spec:
  groups:
  - name: wave4
    interval: 30s
    rules:
    - alert: HighAPILatency
      expr: histogram_quantile(0.95, http_request_duration_seconds_bucket{job="wave4-api"}) > 1
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "High API latency detected"

    - alert: APIErrorRate
      expr: rate(http_requests_total{job="wave4-api",status=~"5.."}[5m]) > 0.01
      for: 5m
      labels:
        severity: critical
      annotations:
        summary: "High API error rate: {{ $value | humanizePercentage }}"

    - alert: DatabaseConnectionPoolExhausted
      expr: db_connection_pool_usage{job=~"postgres|mongodb|neo4j"} > 0.8
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "Database connection pool nearing exhaustion: {{ $labels.instance }}"

    - alert: RedisMemoryUsage
      expr: redis_memory_used_bytes / redis_memory_max_bytes > 0.85
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "Redis memory usage high: {{ $value | humanizePercentage }}"
```

---

## Disaster Recovery

### Backup Strategy

```bash
#!/bin/bash
# scripts/backup-all.sh

set -e

BACKUP_DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_BUCKET="s3://wave4-backups-production"

echo "Starting backup: $BACKUP_DATE"

# Backup EKS cluster
echo "Backing up EKS configuration..."
kubectl get all --all-namespaces -o yaml > /tmp/eks-backup-${BACKUP_DATE}.yaml
aws s3 cp /tmp/eks-backup-${BACKUP_DATE}.yaml ${BACKUP_BUCKET}/eks/

# Backup PostgreSQL
echo "Backing up PostgreSQL..."
kubectl exec -it -n wave4-production $(kubectl get pod -n wave4-production -l app=postgres -o jsonpath="{.items[0].metadata.name}") \
  -- pg_dump -U admin wave4_threat_intel | gzip | aws s3 cp - ${BACKUP_BUCKET}/postgres/backup-${BACKUP_DATE}.sql.gz

# Backup MongoDB
echo "Backing up MongoDB..."
kubectl exec -it -n wave4-production $(kubectl get pod -n wave4-production -l app=mongodb -o jsonpath="{.items[0].metadata.name}") \
  -- mongodump --archive | aws s3 cp - ${BACKUP_BUCKET}/mongodb/backup-${BACKUP_DATE}.archive

# Backup Neo4j
echo "Backing up Neo4j..."
kubectl exec -it -n wave4-production $(kubectl get pod -n wave4-production -l app=neo4j -o jsonpath="{.items[0].metadata.name}") \
  -- neo4j-admin database backup neo4j --to-path=/backup
kubectl cp wave4-production/$(kubectl get pod -n wave4-production -l app=neo4j -o jsonpath="{.items[0].metadata.name}"):/backup /tmp/neo4j-backup-${BACKUP_DATE}
aws s3 sync /tmp/neo4j-backup-${BACKUP_DATE} ${BACKUP_BUCKET}/neo4j/

echo "Backup completed: $BACKUP_DATE"
```

### Disaster Recovery Plan

```markdown
# WAVE4 Disaster Recovery Plan

## RTO/RPO Targets
- Recovery Time Objective (RTO): 4 hours
- Recovery Point Objective (RPO): 1 hour

## Failure Scenarios

### Scenario 1: Single Pod Failure
- **Detection**: Kubernetes automatically restarts pod
- **Action**: Monitor logs, investigate root cause
- **Recovery Time**: < 5 minutes

### Scenario 2: Node Failure
- **Detection**: K8s health checks fail
- **Action**: Automatically reschedule pods to healthy nodes
- **Recovery Time**: < 15 minutes

### Scenario 3: Database Failure
- **Detection**: Connection pool exhaustion, errors
- **Action**: Failover to read replica
- **Recovery Time**: < 30 minutes

### Scenario 4: Regional Outage
- **Detection**: Multiple pod failures, connectivity loss
- **Action**: Activate secondary region
- **Recovery Time**: 2-4 hours

## Recovery Procedures

### From PostgreSQL Backup
```bash
# Restore from latest backup
aws s3 cp s3://wave4-backups-production/postgres/latest.sql.gz - | gunzip | psql -U admin wave4_threat_intel
```

### From MongoDB Backup
```bash
# Restore from latest backup
aws s3 cp s3://wave4-backups-production/mongodb/latest.archive - | mongorestore --archive
```

### From Neo4j Backup
```bash
# Restore from latest backup
aws s3 sync s3://wave4-backups-production/neo4j/latest/ /backup/
neo4j-admin database restore --from-path=/backup neo4j
```
```

---

## Operations & Maintenance

### Health Checks & Monitoring

```bash
#!/bin/bash
# scripts/health-check.sh

API_ENDPOINT="https://api.wave4.com"
SLACK_WEBHOOK="${SLACK_WEBHOOK_URL}"

echo "Running health checks..."

# API Health
response=$(curl -s -o /dev/null -w "%{http_code}" ${API_ENDPOINT}/health)
if [ "$response" != "200" ]; then
  curl -X POST $SLACK_WEBHOOK \
    -H 'Content-Type: application/json' \
    -d "{\"text\": \"ALERT: API health check failed with status $response\"}"
else
  echo "✓ API healthy"
fi

# Database connectivity
kubectl exec -it -n wave4-production $(kubectl get pod -n wave4-production -l app=backend-api -o jsonpath="{.items[0].metadata.name}") \
  -- python -c "
import asyncio
from app.database import neo4j_pool, get_session
async def check():
  try:
    await neo4j_pool.initialize()
    print('✓ Neo4j connected')
  except Exception as e:
    print(f'✗ Neo4j failed: {e}')
asyncio.run(check())
"

echo "Health checks complete"
```

### Scaling Operations

```bash
#!/bin/bash
# scripts/scale-deployment.sh

DEPLOYMENT=$1
REPLICAS=$2

echo "Scaling $DEPLOYMENT to $REPLICAS replicas..."

kubectl scale deployment $DEPLOYMENT -n wave4-production --replicas=$REPLICAS

# Wait for rollout
kubectl rollout status deployment/$DEPLOYMENT -n wave4-production --timeout=10m

echo "Scaling complete"
```

---

## Summary

This Production Deployment implementation provides:

✅ **Enterprise Infrastructure** with AWS EKS and managed services
✅ **Kubernetes Orchestration** with HA and auto-scaling
✅ **CI/CD Automation** with GitHub Actions
✅ **Security & Compliance** with PSPs and scanning
✅ **Comprehensive Monitoring** with Prometheus and Alerting
✅ **Disaster Recovery** with backup and failover procedures
✅ **Operations Tooling** for day-2 management

**Line Count**: ~900 lines of deployment specifications and procedures

---

**Document Version**: v1.0.0
**Last Updated**: 2025-11-25
**Status**: Implementation Ready
