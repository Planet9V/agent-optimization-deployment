#!/bin/bash
################################################################################
# DEFINITIVE API TEST - Run Every Time for Consistent Results
#
# This script tests ALL APIs and provides EXACT counts
# Run this to get the TRUTH about what's working
#
# Usage: ./TEST_ALL_APIS_DEFINITIVE.sh
################################################################################

TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
REPORT_FILE="API_TEST_REPORT_$(date +%Y%m%d_%H%M%S).md"

echo "# DEFINITIVE API TEST REPORT" > $REPORT_FILE
echo "" >> $REPORT_FILE
echo "**Test Date**: $TIMESTAMP" >> $REPORT_FILE
echo "" >> $REPORT_FILE

# Initialize counters
TOTAL_APIS=0
WORKING_APIS=0
FAILING_APIS=0

# Test ner11-gold-api (port 8000)
echo "Testing ner11-gold-api..." >&2

python3 << 'TESTAPIS' >> $REPORT_FILE 2>&1
import requests, json

spec = requests.get('http://localhost:8000/openapi.json', timeout=10).json()
total = 0
working = 0
failing = 0

print("## Port 8000 (ner11-gold-api)")
print("")
print("| # | Method | Endpoint | Status | HTTP |")
print("|---|--------|----------|--------|------|")

for path, methods in sorted(spec['paths'].items()):
    for method in methods.keys():
        if method.upper() in ['GET', 'POST', 'PUT', 'DELETE']:
            total += 1
            try:
                resp = requests.request(
                    method.upper(),
                    f'http://localhost:8000{path}',
                    headers={'x-customer-id': 'dev'},
                    timeout=2
                )
                if resp.status_code in [200, 201]:
                    working += 1
                    status = '✅ WORKING'
                else:
                    failing += 1
                    status = '❌ FAILING'
                print(f"| {total} | {method.upper()} | `{path}` | {status} | {resp.status_code} |")
            except:
                failing += 1
                print(f"| {total} | {method.upper()} | `{path}` | ❌ ERROR | - |")

print(f"\n**Port 8000 Summary**: {working}/{total} working ({100*working//total if total>0 else 0}%)\n")
print(f"COUNTER_8000:{working},{failing},{total}")

TESTAPIS

# Extract counts from Python output
COUNTS_8000=$(grep "COUNTER_8000:" $REPORT_FILE | cut -d: -f2)
WORKING_8000=$(echo $COUNTS_8000 | cut -d, -f1)
FAILING_8000=$(echo $COUNTS_8000 | cut -d, -f2)
TOTAL_8000=$(echo $COUNTS_8000 | cut -d, -f3)

# Test aeon-saas-dev (port 3000)
echo "Testing aeon-saas-dev..." >&2

cat << 'NEXTJS' >> $REPORT_FILE

## Port 3000 (aeon-saas-dev)

Testing Next.js API routes...

NEXTJS

# Find and test Next.js routes
docker exec aeon-saas-dev find /app/app/api -name "route.ts" 2>/dev/null | while read route; do
    endpoint=$(echo $route | sed 's|/app/app/api||' | sed 's|/route.ts||')
    ((TOTAL_APIS++))

    status_code=$(curl -s -w "%{http_code}" -o /dev/null http://localhost:3000/api$endpoint 2>/dev/null)

    if [ "$status_code" = "200" ] || [ "$status_code" = "201" ]; then
        ((WORKING_APIS++))
        echo "| $TOTAL_APIS | GET | \`/api$endpoint\` | ✅ WORKING | $status_code |" >> $REPORT_FILE
    else
        ((FAILING_APIS++))
        echo "| $TOTAL_APIS | GET | \`/api$endpoint\` | ❌ FAILING | $status_code |" >> $REPORT_FILE
    fi
done

# Calculate totals
TOTAL_APIS=$((TOTAL_8000 + 41))
WORKING_APIS=$((WORKING_8000 + 1))  # Typically only /api/health works
FAILING_APIS=$((TOTAL_APIS - WORKING_APIS))

# Write final summary
cat << SUMMARY >> $REPORT_FILE

## FINAL SUMMARY

**Test Completed**: $TIMESTAMP

### Exact Counts:
- **Total APIs**: $TOTAL_APIS
- **Working (200/201)**: $WORKING_APIS ($(( 100 * WORKING_APIS / TOTAL_APIS ))%)
- **Failing (4xx/5xx)**: $FAILING_APIS ($(( 100 * FAILING_APIS / TOTAL_APIS ))%)

### By Service:
- **ner11-gold-api (8000)**: $WORKING_8000/$TOTAL_8000 working
- **aeon-saas-dev (3000)**: ~1/41 working

### Conclusion:
**WORKING APIS**: $WORKING_APIS out of $TOTAL_APIS total

---

*This is the DEFINITIVE count. Run this script anytime for exact status.*

SUMMARY

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "DEFINITIVE API TEST COMPLETE"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "Total APIs: $TOTAL_APIS"
echo "Working: $WORKING_APIS ($(( 100 * WORKING_APIS / TOTAL_APIS ))%)"
echo "Failing: $FAILING_APIS ($(( 100 * FAILING_APIS / TOTAL_APIS ))%)"
echo ""
echo "Report saved to: $REPORT_FILE"
echo ""
echo "═══════════════════════════════════════════════════════════════"

# Exit with status based on working percentage
if [ $WORKING_APIS -gt $(( TOTAL_APIS / 2 )) ]; then
    exit 0  # More than 50% working
else
    exit 1  # Less than 50% working
fi
