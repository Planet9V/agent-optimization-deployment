# TASKMASTER INSTRUCTIONS

**Role**: Create detailed test inventory for 181+ APIs

**Your Mission**:
Create a comprehensive, line-by-line test plan for every API across all services.

**Input Data**:
1. FastAPI (ner11-gold-api): 140 operations
   - File: /home/jim/2_OXOT_Projects_Dev/docs/api-testing/fastapi-full-inventory.csv
   
2. Next.js (aeon-saas-dev): 41+ routes
   - Directory: /home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney/web_interface/app/api/

3. OpenSPG server: TBD (needs extraction)
4. Neo4j: Standard REST + Bolt APIs
5. Qdrant: Vector database API
6. MinIO: S3-compatible API

**Your Deliverables**:

1. **Complete Test Matrix** (CSV format)
```csv
test_id,service,endpoint,method,category,priority,estimated_time_sec,dependencies,notes
001,ner11-gold-api,/health,GET,health,P0,5,none,Health check endpoint
002,ner11-gold-api,/api/v2/threat_intel/campaigns/active,GET,threat-intel,P1,30,auth,Active threat campaigns
...
```

2. **Priority Breakdown**:
   - P0 (Critical): Health checks, core auth (20 APIs)
   - P1 (High): Main business logic (80 APIs)
   - P2 (Medium): Analytics, reporting (60 APIs)
   - P3 (Low): Documentation, utilities (21 APIs)

3. **Category Summary**:
   - Group APIs by functional category
   - Identify test dependencies
   - Estimate testing time per category
   - Flag complex/risky endpoints

4. **Execution Sequence**:
   - Order tests by dependencies
   - Group parallel-testable APIs
   - Identify blocking tests

**Output Files**:
- `/home/jim/2_OXOT_Projects_Dev/docs/api-testing/test-matrix-complete.csv`
- `/home/jim/2_OXOT_Projects_Dev/docs/api-testing/test-plan-summary.md`
- `/home/jim/2_OXOT_Projects_Dev/docs/api-testing/test-execution-order.md`

**Quality Requirements**:
- Every API must have a test ID
- All 181+ APIs must be listed
- Priorities must be assigned
- Time estimates required
- Dependencies documented

**Timeline**: Complete within 30 minutes

DO THE ACTUAL WORK - Create the complete test matrix, do not build frameworks.
