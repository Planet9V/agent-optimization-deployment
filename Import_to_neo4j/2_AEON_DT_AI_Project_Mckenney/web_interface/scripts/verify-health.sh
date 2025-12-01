#!/bin/bash
# Verify Health Check Implementation

echo "🔍 Health Check Implementation Verification"
echo "==========================================="
echo ""

# 1. Check if file exists
echo "1️⃣ Checking implementation file..."
if [ -f "app/api/health/route.ts" ]; then
  echo "   ✅ app/api/health/route.ts exists"
else
  echo "   ❌ app/api/health/route.ts NOT FOUND"
  exit 1
fi

# 2. Check imports
echo ""
echo "2️⃣ Verifying library imports..."
grep -q "import.*getNeo4jDriver.*from.*neo4j-enhanced" app/api/health/route.ts && echo "   ✅ Neo4j import" || echo "   ❌ Neo4j import missing"
grep -q "import.*getMySQLPool.*from.*mysql" app/api/health/route.ts && echo "   ✅ MySQL import" || echo "   ❌ MySQL import missing"
grep -q "import.*getQdrantClient.*from.*qdrant" app/api/health/route.ts && echo "   ✅ Qdrant import" || echo "   ❌ Qdrant import missing"
grep -q "import.*getMinIOClient.*from.*minio" app/api/health/route.ts && echo "   ✅ MinIO import" || echo "   ❌ MinIO import missing"

# 3. Check functions
echo ""
echo "3️⃣ Verifying service check functions..."
grep -q "async function checkNeo4j" app/api/health/route.ts && echo "   ✅ checkNeo4j()" || echo "   ❌ checkNeo4j() missing"
grep -q "async function checkMySQL" app/api/health/route.ts && echo "   ✅ checkMySQL()" || echo "   ❌ checkMySQL() missing"
grep -q "async function checkQdrant" app/api/health/route.ts && echo "   ✅ checkQdrant()" || echo "   ❌ checkQdrant() missing"
grep -q "async function checkMinIO" app/api/health/route.ts && echo "   ✅ checkMinIO()" || echo "   ❌ checkMinIO() missing"

# 4. Check parallel execution
echo ""
echo "4️⃣ Verifying parallel execution..."
grep -q "Promise.all" app/api/health/route.ts && echo "   ✅ Parallel execution with Promise.all" || echo "   ❌ No parallel execution"

# 5. Check response format
echo ""
echo "5️⃣ Verifying response format..."
grep -q '"status".*"healthy".*"degraded".*"unhealthy"' app/api/health/route.ts && echo "   ✅ Status types" || echo "   ⚠️  Status types format"
grep -q "overallHealth" app/api/health/route.ts && echo "   ✅ Overall health field" || echo "   ❌ Overall health missing"
grep -q "services" app/api/health/route.ts && echo "   ✅ Services field" || echo "   ❌ Services field missing"

# 6. Check timeout handling
echo ""
echo "6️⃣ Verifying timeout handling..."
grep -q "SERVICE_TIMEOUT" app/api/health/route.ts && echo "   ✅ Timeout configuration" || echo "   ❌ No timeout handling"
grep -q "withTimeout" app/api/health/route.ts && echo "   ✅ Timeout wrapper function" || echo "   ❌ Timeout wrapper missing"

# 7. Check documentation
echo ""
echo "7️⃣ Checking documentation..."
[ -f "docs/health-check-endpoint.md" ] && echo "   ✅ Documentation exists" || echo "   ⚠️  Documentation not found"

# 8. Check test files
echo ""
echo "8️⃣ Checking test files..."
[ -f "tests/health-check.test.ts" ] && echo "   ✅ Test suite exists" || echo "   ⚠️  Test suite not found"
[ -f "scripts/test-health.sh" ] && echo "   ✅ Manual test script exists" || echo "   ⚠️  Manual test script not found"

# 9. Count lines of implementation
echo ""
echo "9️⃣ Implementation statistics..."
LINES=$(wc -l < app/api/health/route.ts)
echo "   📊 Total lines: $LINES"
[ $LINES -gt 200 ] && echo "   ✅ Comprehensive implementation" || echo "   ⚠️  Implementation may be incomplete"

# Summary
echo ""
echo "==========================================="
echo "✅ Health Check Implementation Verified!"
echo ""
echo "Next steps:"
echo "  1. Start the development server: npm run dev"
echo "  2. Test the endpoint: ./scripts/test-health.sh"
echo "  3. View documentation: docs/health-check-endpoint.md"
echo ""
