#!/bin/bash
# Test Health Check Endpoint

echo "🔍 Testing Health Check Endpoint..."
echo ""

# Test the endpoint
RESPONSE=$(curl -s -w "\n%{http_code}" http://localhost:3000/api/health)
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | head -n-1)

echo "📊 HTTP Status: $HTTP_CODE"
echo ""
echo "📋 Response:"
echo "$BODY" | jq . 2>/dev/null || echo "$BODY"
echo ""

# Check if all services are healthy
if [ "$HTTP_CODE" = "200" ]; then
  echo "✅ All services healthy!"
elif [ "$HTTP_CODE" = "207" ]; then
  echo "⚠️  Some services degraded"
else
  echo "❌ Services unhealthy"
fi

echo ""
echo "🔍 Service Details:"
echo "$BODY" | jq -r '.services | to_entries[] | "\(.key): \(.value.status) (\(.value.responseTime // "N/A")ms)"' 2>/dev/null

exit 0
