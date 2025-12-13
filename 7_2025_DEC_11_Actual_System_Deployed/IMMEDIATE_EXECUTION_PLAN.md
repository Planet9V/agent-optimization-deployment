# IMMEDIATE EXECUTION PLAN - DO NOW

**Created**: 2025-12-12
**Priority**: CRITICAL - Execute immediately
**Status**: READY FOR EXECUTION

---

## ✅ TASK 1: FIX MIDDLEWARE (5 minutes)

**File**: `/home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/serve_model.py`

**Action**: Add customer context middleware

**Code to Add** (after line ~140, after app initialization):
```python
from api.customer_isolation.customer_context import CustomerContext

# Set default customer context for development
@app.middleware("http")
async def dev_customer_context(request: Request, call_next):
    # For development: use 'dev' if no customer ID provided
    customer_id = request.headers.get("x-customer-id", "dev")
    # Simple pass-through for now
    response = await call_next(request)
    return response
```

**Deploy**:
```bash
docker cp /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/serve_model.py ner11-gold-api:/app/
docker restart ner11-gold-api
```

**Verify**:
```bash
sleep 10
curl http://localhost:8000/api/v2/sbom/dashboard/summary -H "x-customer-id: dev"
# Should return data (not error)
```

---

## ✅ TASK 2: FIX IMPORTS (15 minutes)

**Files with circular import issues**:
1. `/app/api/risk_scoring/risk_models.py` - RiskTrend enum
2. `/app/api/remediation/remediation_service.py` - Context manager

**Fix 1**: Add to risk_models.py:
```python
class RiskTrend(str, Enum):
    INCREASING = "increasing"
    DECREASING = "decreasing"
    STABLE = "stable"
    IMPROVING = "improving"
    DEGRADING = "degrading"
```

**Fix 2**: Make Qdrant optional in remediation_service.py (already done)

**Deploy**: Already in container, just needs restart

---

## ✅ TASK 3: TEST ALL 232 APIS (30 minutes)

**Execute test script**:
```bash
cd /home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed
./SYSTEM_HEALTH_CHECK.sh > health_check_results.txt 2>&1

# Then test each API endpoint
curl -s http://localhost:8000/openapi.json | \
  python3 -c "
import json, sys
spec = json.load(sys.stdin)
for path in spec['paths']:
    for method in spec['paths'][path]:
        print(f'{method.upper()}\t{path}')
" > all_endpoints.txt

# Test each endpoint
while IFS=$'\t' read -r method path; do
    response=$(curl -s -w "%{http_code}" -X $method \
        "http://localhost:8000$path" \
        -H "x-customer-id: dev" \
        -H "Content-Type: application/json")
    echo "$method $path: $response"
done < all_endpoints.txt > api_test_results.txt
```

**Capture**:
- HTTP status for each API
- Pass/fail count
- Error messages

---

## ✅ TASK 4: ADD TEST BADGES (10 minutes)

**Update**: ALL_APIS_MASTER_TABLE.md

**For each API, add status**:
- ✅ WORKING (returns 200/201)
- ❌ FAILING (returns 400/500)
- ⏳ NOT TESTED

**Script**:
```bash
# Parse api_test_results.txt and update table
python3 << 'EOF'
with open('api_test_results.txt') as f:
    results = {}
    for line in f:
        parts = line.strip().split(': ')
        if len(parts) == 2:
            endpoint = parts[0]
            status = parts[1]
            if '200' in status or '201' in status:
                results[endpoint] = '✅ WORKING'
            else:
                results[endpoint] = '❌ FAILING'

# Update master table with results
# (Manual update or script)
EOF
```

---

## ✅ TASK 5: UPDATE DOCUMENTATION (20 minutes)

**Files to update**:

1. **ALL_APIS_MASTER_TABLE.md**:
   - Add test status column
   - Update with actual results

2. **FINAL_STATUS_SUMMARY.md**:
   - Update API counts (X working, Y failing)
   - Update ratings based on actual tests

3. **README.md**:
   - Update with accurate counts
   - Remove any unverified claims

---

## 📋 EXECUTION CHECKLIST

```
[ ] 1. Fix middleware in serve_model.py
[ ] 2. Deploy to container
[ ] 3. Restart container
[ ] 4. Verify middleware working
[ ] 5. Fix RiskTrend enum
[ ] 6. Test all 232 APIs systematically
[ ] 7. Capture all results
[ ] 8. Update ALL_APIS_MASTER_TABLE.md with badges
[ ] 9. Update FINAL_STATUS_SUMMARY.md
[ ] 10. Update README.md
[ ] 11. Commit all changes
[ ] 12. Verify record of note is accurate
```

---

## ⏱️ TOTAL TIME: ~80 minutes

**Timeline**:
- Task 1: 5 min
- Task 2: 15 min
- Task 3: 30 min
- Task 4: 10 min
- Task 5: 20 min

**Expected Result**:
- 90%+ APIs working
- All tested and documented
- Accurate record of note

---

## 🚀 START NOW

Execute tasks 1-5 in sequence.
No planning - just execution.

**BEGIN** ⬇️
