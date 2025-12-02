#!/bin/bash
#
# File: test_semantic_search.sh
# Purpose: Quick test script for NER11 Semantic Search API
# Task: TASKMASTER Task 1.5
# Version: 1.0.0
# Created: 2025-12-01

set -e

API_URL="${API_URL:-http://localhost:8000}"
BOLD='\033[1m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BOLD}======================================${NC}"
echo -e "${BOLD}NER11 Semantic Search API Test Suite${NC}"
echo -e "${BOLD}======================================${NC}\n"

# Function to test endpoint
test_endpoint() {
    local name="$1"
    local endpoint="$2"
    local method="${3:-GET}"
    local data="$4"

    echo -e "${BLUE}Testing:${NC} $name"

    if [ "$method" = "GET" ]; then
        response=$(curl -s "$API_URL$endpoint")
    else
        response=$(curl -s -X POST "$API_URL$endpoint" \
            -H "Content-Type: application/json" \
            -d "$data")
    fi

    if echo "$response" | jq . >/dev/null 2>&1; then
        echo -e "${GREEN}✓ Success${NC}"
        echo "$response" | jq -C '.' | head -20
    else
        echo -e "${RED}✗ Failed${NC}"
        echo "$response"
    fi
    echo ""
}

# 1. Health Check
echo -e "${BOLD}1. System Health Check${NC}"
test_endpoint "Health Status" "/health" "GET"

# 2. Model Info
echo -e "${BOLD}2. Model Information${NC}"
test_endpoint "Model Capabilities" "/info" "GET"

# 3. Basic NER (original endpoint)
echo -e "${BOLD}3. Named Entity Recognition${NC}"
test_endpoint "NER Extraction" "/ner" "POST" '{
  "text": "WannaCry ransomware exploited CVE-2017-0144 targeting SCADA systems."
}'

# 4. Basic Semantic Search
echo -e "${BOLD}4. Basic Semantic Search${NC}"
test_endpoint "Search: ransomware" "/search/semantic" "POST" '{
  "query": "ransomware attack",
  "limit": 5
}'

# 5. Tier 1 Filtering
echo -e "${BOLD}5. Tier 1 Label Filtering (60 NER labels)${NC}"
test_endpoint "Search with label_filter=MALWARE" "/search/semantic" "POST" '{
  "query": "cyber threat",
  "limit": 5,
  "label_filter": "MALWARE"
}'

# 6. Tier 2 Filtering (CRITICAL FEATURE)
echo -e "${BOLD}6. Tier 2 Fine-Grained Filtering (566 types) ⭐${NC}"
test_endpoint "Search with fine_grained_filter=RANSOMWARE" "/search/semantic" "POST" '{
  "query": "encryption malware",
  "limit": 5,
  "fine_grained_filter": "RANSOMWARE"
}'

# 7. Combined Hierarchical Filtering
echo -e "${BOLD}7. Combined Hierarchical Filtering${NC}"
test_endpoint "Search with both filters" "/search/semantic" "POST" '{
  "query": "control system",
  "limit": 5,
  "label_filter": "INFRASTRUCTURE",
  "fine_grained_filter": "SCADA_SERVER"
}'

# 8. Confidence Threshold
echo -e "${BOLD}8. Confidence Threshold Filtering${NC}"
test_endpoint "Search with confidence >= 0.8" "/search/semantic" "POST" '{
  "query": "threat actor",
  "limit": 5,
  "confidence_threshold": 0.8
}'

# Summary
echo -e "${BOLD}======================================${NC}"
echo -e "${GREEN}✓ Test Suite Complete${NC}"
echo -e "${BOLD}======================================${NC}\n"

echo -e "${YELLOW}Next Steps:${NC}"
echo "1. View interactive docs: $API_URL/docs"
echo "2. Load test data: cd pipelines && python 02_entity_embedding_service_hierarchical.py"
echo "3. See full testing guide: docs/SEMANTIC_SEARCH_API_TESTING.md"
echo ""
