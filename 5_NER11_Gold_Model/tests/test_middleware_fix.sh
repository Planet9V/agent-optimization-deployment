#!/bin/bash
# Test Customer Context Middleware Fix
# Tests all Phase B2/B3 API categories

CUSTOMER_ID="dev"
BASE_URL="http://localhost:8000"

echo "=================================="
echo "Testing Customer Context Middleware"
echo "=================================="
echo ""

# Test 1: Health Check (no customer ID needed)
echo "1. Testing Health Check..."
HEALTH=$(curl -s "$BASE_URL/health")
STATUS=$(echo "$HEALTH" | python3 -c "import sys, json; print(json.load(sys.stdin)['status'])" 2>/dev/null)
if [ "$STATUS" = "healthy" ]; then
    echo "   ✅ Health check passed"
else
    echo "   ❌ Health check failed: $STATUS"
fi
echo ""

# Test 2: SBOM APIs (Phase B2)
echo "2. Testing SBOM APIs (Phase B2)..."
SBOM=$(curl -s -H "x-customer-id: $CUSTOMER_ID" "$BASE_URL/api/v2/sbom/sboms")
if echo "$SBOM" | grep -q "customer_id"; then
    echo "   ✅ SBOM API working - customer context detected"
else
    echo "   ❌ SBOM API failed: $SBOM"
fi
echo ""

# Test 3: Threat Intel Dashboard (Phase B3)
echo "3. Testing Threat Intel Dashboard (Phase B3)..."
THREAT=$(curl -s -H "x-customer-id: $CUSTOMER_ID" "$BASE_URL/api/v2/threat-intel/dashboard/summary")
if echo "$THREAT" | grep -q "customer_id"; then
    echo "   ✅ Threat Intel Dashboard working - customer context detected"
else
    echo "   ❌ Threat Intel Dashboard failed: $THREAT"
fi
echo ""

# Test 4: Risk Dashboard (Phase B3)
echo "4. Testing Risk Dashboard (Phase B3)..."
RISK=$(curl -s -H "x-customer-id: $CUSTOMER_ID" "$BASE_URL/api/v2/risk/dashboard/summary")
if echo "$RISK" | grep -q "customer_id"; then
    echo "   ✅ Risk Dashboard working - customer context detected"
else
    echo "   ❌ Risk Dashboard failed: $RISK"
fi
echo ""

# Test 5: Test without customer ID (should fail gracefully)
echo "5. Testing SBOM without customer ID (should fail)..."
NO_CUSTOMER=$(curl -s "$BASE_URL/api/v2/sbom/sboms")
if echo "$NO_CUSTOMER" | grep -q "Customer context required"; then
    echo "   ✅ Proper error handling - customer context required"
else
    echo "   ⚠️  Unexpected response: $NO_CUSTOMER"
fi
echo ""

# Test 6: Test with alternative header format
echo "6. Testing with X-Customer-ID header..."
ALT_HEADER=$(curl -s -H "X-Customer-ID: $CUSTOMER_ID" "$BASE_URL/api/v2/sbom/sboms")
if echo "$ALT_HEADER" | grep -q "customer_id"; then
    echo "   ✅ Alternative header format working"
else
    echo "   ❌ Alternative header failed: $ALT_HEADER"
fi
echo ""

# Test 7: Multiple API Categories
echo "7. Testing Multiple API Categories..."
CATEGORIES=(
    "/api/v2/sbom/sboms:SBOM"
    "/api/v2/threat-intel/dashboard/summary:Threat Intel"
    "/api/v2/risk/dashboard/summary:Risk Scoring"
)

for CAT in "${CATEGORIES[@]}"; do
    IFS=':' read -r ENDPOINT NAME <<< "$CAT"
    RESPONSE=$(curl -s -H "x-customer-id: $CUSTOMER_ID" "$BASE_URL$ENDPOINT")
    if echo "$RESPONSE" | grep -q "customer_id"; then
        echo "   ✅ $NAME: Working"
    else
        echo "   ❌ $NAME: Failed"
    fi
done
echo ""

echo "=================================="
echo "Middleware Test Complete"
echo "=================================="
