#!/bin/bash
# =============================================================================
# Security Audit Script for AEON Cybersecurity System
# =============================================================================
# Purpose: Verify security configuration and identify credential risks
# Created: 2025-12-12
# Version: v1.0.0
# =============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Emoji indicators
CHECK="✅"
WARN="⚠️"
FAIL="❌"
INFO="ℹ️"

echo -e "${BLUE}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║        AEON CYBERSECURITY SYSTEM - SECURITY AUDIT         ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""

# Counter for issues
WARNINGS=0
FAILURES=0
PASSED=0

# =============================================================================
# 1. CHECK FOR EXPOSED CREDENTIALS
# =============================================================================
echo -e "${BLUE}[1/10] Checking for exposed credentials in Git...${NC}"

# Check if .env is in .gitignore
if grep -q "^\.env$" .gitignore 2>/dev/null; then
    echo -e "${GREEN}${CHECK} .env is in .gitignore${NC}"
    ((PASSED++))
else
    echo -e "${RED}${FAIL} .env NOT in .gitignore - CRITICAL${NC}"
    ((FAILURES++))
fi

# Check if .env exists but not tracked
if [ -f .env ]; then
    if git ls-files --error-unmatch .env 2>/dev/null; then
        echo -e "${RED}${FAIL} .env is tracked by Git - CRITICAL${NC}"
        ((FAILURES++))
    else
        echo -e "${GREEN}${CHECK} .env exists but not tracked by Git${NC}"
        ((PASSED++))
    fi
else
    echo -e "${YELLOW}${WARN} .env file not found (using defaults?)${NC}"
    ((WARNINGS++))
fi

# Check for hardcoded credentials in code
echo -e "\n${BLUE}Scanning for hardcoded credentials in Python files...${NC}"
if grep -r -i "password.*=.*['\"]" --include="*.py" . 2>/dev/null | grep -v ".env" | grep -v "example" | grep -v "#"; then
    echo -e "${RED}${FAIL} Found potential hardcoded passwords${NC}"
    ((FAILURES++))
else
    echo -e "${GREEN}${CHECK} No hardcoded passwords found${NC}"
    ((PASSED++))
fi

# =============================================================================
# 2. CHECK DOCKER CONTAINER SECURITY
# =============================================================================
echo -e "\n${BLUE}[2/10] Checking Docker container security...${NC}"

# Check if containers are running
if docker ps > /dev/null 2>&1; then
    RUNNING_CONTAINERS=$(docker ps --format "{{.Names}}" | wc -l)
    echo -e "${GREEN}${CHECK} Docker is running (${RUNNING_CONTAINERS} containers)${NC}"
    ((PASSED++))
else
    echo -e "${RED}${FAIL} Docker is not running${NC}"
    ((FAILURES++))
fi

# Check for default passwords in container environment
if docker ps > /dev/null 2>&1; then
    echo -e "\n${BLUE}Checking for default passwords in containers...${NC}"

    # Neo4j
    if docker ps | grep -q "neo4j"; then
        NEO4J_AUTH=$(docker inspect openspg-neo4j --format='{{json .Config.Env}}' 2>/dev/null | grep -o "NEO4J_AUTH=[^\"]*" | cut -d'=' -f2)
        if [[ "$NEO4J_AUTH" == "neo4j/neo4j" ]] || [[ "$NEO4J_AUTH" == "neo4j/password" ]]; then
            echo -e "${RED}${FAIL} Neo4j using DEFAULT password${NC}"
            ((FAILURES++))
        elif [[ "$NEO4J_AUTH" == "neo4j/neo4j@openspg" ]]; then
            echo -e "${YELLOW}${WARN} Neo4j using development password${NC}"
            ((WARNINGS++))
        else
            echo -e "${GREEN}${CHECK} Neo4j password appears custom${NC}"
            ((PASSED++))
        fi
    fi

    # PostgreSQL
    if docker ps | grep -q "postgres"; then
        POSTGRES_PASS=$(docker inspect aeon-postgres-dev --format='{{json .Config.Env}}' 2>/dev/null | grep -o "POSTGRES_PASSWORD=[^\"]*" | cut -d'=' -f2)
        if [[ "$POSTGRES_PASS" == "postgres" ]] || [[ "$POSTGRES_PASS" == "password" ]]; then
            echo -e "${YELLOW}${WARN} PostgreSQL using weak password${NC}"
            ((WARNINGS++))
        else
            echo -e "${GREEN}${CHECK} PostgreSQL password set${NC}"
            ((PASSED++))
        fi
    fi
fi

# =============================================================================
# 3. CHECK PORT EXPOSURE
# =============================================================================
echo -e "\n${BLUE}[3/10] Checking exposed ports...${NC}"

# List all exposed ports
if docker ps > /dev/null 2>&1; then
    echo -e "${INFO} Exposed ports:"
    docker ps --format "table {{.Names}}\t{{.Ports}}" | grep -v "NAMES"

    # Check if databases are exposed to 0.0.0.0
    if docker ps --format "{{.Ports}}" | grep -q "0.0.0.0"; then
        echo -e "${YELLOW}${WARN} Services exposed to all interfaces (0.0.0.0)${NC}"
        echo -e "${YELLOW}    This is OK for development, but NOT for production${NC}"
        ((WARNINGS++))
    fi
fi

# =============================================================================
# 4. CHECK FILE PERMISSIONS
# =============================================================================
echo -e "\n${BLUE}[4/10] Checking file permissions...${NC}"

# Check .env permissions
if [ -f .env ]; then
    ENV_PERMS=$(stat -c "%a" .env 2>/dev/null || stat -f "%A" .env 2>/dev/null)
    if [ "$ENV_PERMS" != "600" ] && [ "$ENV_PERMS" != "400" ]; then
        echo -e "${YELLOW}${WARN} .env permissions are ${ENV_PERMS} (should be 600 or 400)${NC}"
        ((WARNINGS++))
    else
        echo -e "${GREEN}${CHECK} .env has secure permissions (${ENV_PERMS})${NC}"
        ((PASSED++))
    fi
fi

# Check for world-readable credential files
CREDENTIAL_FILES=$(find . -type f \( -name "*.key" -o -name "*.pem" -o -name "credentials.*" \) 2>/dev/null)
if [ -n "$CREDENTIAL_FILES" ]; then
    echo -e "${INFO} Found credential files:"
    echo "$CREDENTIAL_FILES" | while read file; do
        PERMS=$(stat -c "%a" "$file" 2>/dev/null || stat -f "%A" "$file" 2>/dev/null)
        if [ "${PERMS: -1}" != "0" ]; then
            echo -e "${YELLOW}${WARN} $file is world-readable (${PERMS})${NC}"
            ((WARNINGS++))
        else
            echo -e "${GREEN}${CHECK} $file has secure permissions${NC}"
            ((PASSED++))
        fi
    done
fi

# =============================================================================
# 5. CHECK DATABASE AUTHENTICATION
# =============================================================================
echo -e "\n${BLUE}[5/10] Checking database authentication...${NC}"

# Neo4j
if docker ps | grep -q "neo4j"; then
    if docker exec openspg-neo4j cypher-shell -u neo4j -p neo4j@openspg "RETURN 1" > /dev/null 2>&1; then
        echo -e "${GREEN}${CHECK} Neo4j authentication is enabled${NC}"
        ((PASSED++))
    else
        echo -e "${RED}${FAIL} Neo4j authentication check failed${NC}"
        ((FAILURES++))
    fi
fi

# Qdrant (check if authentication is enabled)
if docker ps | grep -q "qdrant"; then
    if curl -s http://localhost:6333/collections > /dev/null 2>&1; then
        echo -e "${YELLOW}${WARN} Qdrant has NO authentication (OK for dev)${NC}"
        ((WARNINGS++))
    fi
fi

# Redis (check if password required)
if docker ps | grep -q "redis"; then
    if docker exec openspg-redis redis-cli ping > /dev/null 2>&1; then
        echo -e "${YELLOW}${WARN} Redis has NO password (OK for dev)${NC}"
        ((WARNINGS++))
    fi
fi

# =============================================================================
# 6. CHECK SSL/TLS CONFIGURATION
# =============================================================================
echo -e "\n${BLUE}[6/10] Checking SSL/TLS configuration...${NC}"

# Check Neo4j SSL
if docker ps | grep -q "neo4j"; then
    NEO4J_SSL=$(docker inspect openspg-neo4j --format='{{json .Config.Env}}' 2>/dev/null | grep -o "NEO4J_dbms_ssl_policy_bolt_enabled=[^\"]*" | cut -d'=' -f2)
    if [[ "$NEO4J_SSL" == "true" ]]; then
        echo -e "${GREEN}${CHECK} Neo4j SSL is enabled${NC}"
        ((PASSED++))
    else
        echo -e "${YELLOW}${WARN} Neo4j SSL is disabled (OK for dev)${NC}"
        ((WARNINGS++))
    fi
fi

# Check MinIO SSL
if docker ps | grep -q "minio"; then
    MINIO_SSL=$(docker inspect openspg-minio --format='{{json .Config.Env}}' 2>/dev/null | grep -i "ssl\|tls")
    if [ -z "$MINIO_SSL" ]; then
        echo -e "${YELLOW}${WARN} MinIO SSL not configured (OK for dev)${NC}"
        ((WARNINGS++))
    fi
fi

# =============================================================================
# 7. CHECK BACKUP CONFIGURATION
# =============================================================================
echo -e "\n${BLUE}[7/10] Checking backup configuration...${NC}"

# Check for Docker volumes
VOLUMES=$(docker volume ls --format "{{.Name}}" | grep -E "neo4j|postgres|mysql|qdrant|minio|redis" | wc -l)
if [ "$VOLUMES" -gt 0 ]; then
    echo -e "${GREEN}${CHECK} Found ${VOLUMES} data volumes${NC}"
    ((PASSED++))
else
    echo -e "${RED}${FAIL} No data volumes found${NC}"
    ((FAILURES++))
fi

# Check if backup scripts exist
if [ -d "backups" ] || [ -f "scripts/backup.sh" ]; then
    echo -e "${GREEN}${CHECK} Backup scripts found${NC}"
    ((PASSED++))
else
    echo -e "${YELLOW}${WARN} No backup scripts found${NC}"
    ((WARNINGS++))
fi

# =============================================================================
# 8. CHECK NETWORK ISOLATION
# =============================================================================
echo -e "\n${BLUE}[8/10] Checking network isolation...${NC}"

# Check Docker networks
NETWORKS=$(docker network ls --format "{{.Name}}" | grep -E "aeon|openspg" | wc -l)
if [ "$NETWORKS" -gt 0 ]; then
    echo -e "${GREEN}${CHECK} Found ${NETWORKS} isolated networks${NC}"
    ((PASSED++))
    docker network ls --format "table {{.Name}}\t{{.Driver}}" | grep -E "aeon|openspg"
else
    echo -e "${YELLOW}${WARN} No custom networks found${NC}"
    ((WARNINGS++))
fi

# =============================================================================
# 9. CHECK LOGGING CONFIGURATION
# =============================================================================
echo -e "\n${BLUE}[9/10] Checking logging configuration...${NC}"

# Check if log volumes exist
LOG_VOLUMES=$(docker volume ls --format "{{.Name}}" | grep -i "log" | wc -l)
if [ "$LOG_VOLUMES" -gt 0 ]; then
    echo -e "${GREEN}${CHECK} Found ${LOG_VOLUMES} log volumes${NC}"
    ((PASSED++))
else
    echo -e "${YELLOW}${WARN} No dedicated log volumes found${NC}"
    ((WARNINGS++))
fi

# =============================================================================
# 10. CHECK DOCUMENTATION
# =============================================================================
echo -e "\n${BLUE}[10/10] Checking security documentation...${NC}"

if [ -f "docs/CREDENTIALS_AND_SECRETS_GUIDE.md" ]; then
    echo -e "${GREEN}${CHECK} Credentials guide exists${NC}"
    ((PASSED++))
else
    echo -e "${RED}${FAIL} Credentials guide missing${NC}"
    ((FAILURES++))
fi

if [ -f ".env.example" ]; then
    echo -e "${GREEN}${CHECK} .env.example template exists${NC}"
    ((PASSED++))
else
    echo -e "${YELLOW}${WARN} .env.example template missing${NC}"
    ((WARNINGS++))
fi

if [ -f "docs/CREDENTIALS_QUICK_REFERENCE.md" ]; then
    echo -e "${GREEN}${CHECK} Quick reference exists${NC}"
    ((PASSED++))
else
    echo -e "${YELLOW}${WARN} Quick reference missing${NC}"
    ((WARNINGS++))
fi

# =============================================================================
# SUMMARY
# =============================================================================
echo -e "\n${BLUE}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                    AUDIT SUMMARY                          ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}Passed:   ${PASSED}${NC}"
echo -e "${YELLOW}Warnings: ${WARNINGS}${NC}"
echo -e "${RED}Failures: ${FAILURES}${NC}"
echo ""

# Recommendations
echo -e "${BLUE}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                  RECOMMENDATIONS                          ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""

if [ "$FAILURES" -gt 0 ]; then
    echo -e "${RED}🚨 CRITICAL ISSUES FOUND - Must fix before production${NC}"
    echo -e "   • Review failures above and take immediate action"
fi

if [ "$WARNINGS" -gt 0 ]; then
    echo -e "${YELLOW}⚠️  WARNINGS DETECTED${NC}"
    echo -e "   • Current configuration is OK for development"
    echo -e "   • MUST address all warnings before production deployment"
fi

echo ""
echo -e "${BLUE}For Production Deployment:${NC}"
echo -e "  1. Change ALL default passwords"
echo -e "  2. Enable authentication on Qdrant and Redis"
echo -e "  3. Configure SSL/TLS for all services"
echo -e "  4. Remove 0.0.0.0 port bindings"
echo -e "  5. Use secrets management system"
echo -e "  6. Enable access logging and monitoring"
echo -e "  7. Set up automated backups"
echo -e "  8. Review docs/CREDENTIALS_AND_SECRETS_GUIDE.md"
echo ""

# Exit code
if [ "$FAILURES" -gt 0 ]; then
    exit 1
elif [ "$WARNINGS" -gt 5 ]; then
    exit 2
else
    exit 0
fi
