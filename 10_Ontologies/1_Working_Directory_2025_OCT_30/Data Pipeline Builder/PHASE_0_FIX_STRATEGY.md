# PHASE 0.2-0.4: FIX STRATEGY & CORRECTED ARCHITECTURE

**Date:** 2025-01-05
**Session:** swarm-1762322591052
**Protocol:** AEON PROJECT TASK EXECUTION PROTOCOL - Phase 0 (Completion)
**Status:** 🎯 STRATEGY DEFINED

---

## PHASE 0.2: CRITICAL BLOCKER PRIORITIZATION

### Severity Classification

**BLOCKER (Must fix before ANY testing):**
1. Missing Python dependencies (lib4sbom, cyclonedx, spdx)
2. Missing Python modules (nlp_ingestion_pipeline, entity_resolver)

**CRITICAL (Must fix for correct architecture):**
3. Redis dependency (remove or replace)
4. Parallel processing (change to SERIAL as required)

**IMPORTANT (Must fix for deployment):**
5. TypeScript compilation errors
6. Jest type definitions

**VALIDATION (Final step):**
7. Run actual tests with real data
8. Verify NER extraction works

---

## FIX PRIORITY ORDER

### Priority 1: Python Dependencies (15 minutes)
**Blocker:** Tests can't import modules
**Fix:** Install missing packages
```bash
source venv/bin/activate
pip install lib4sbom cyclonedx-python-lib spdx-tools
```
**Success Criteria:** `python -c "import lib4sbom"` succeeds

---

### Priority 2: Missing Python Modules (45 minutes)
**Blocker:** Tests fail with ModuleNotFoundError
**Required Modules:**
1. `nlp_ingestion_pipeline.py` - NLPIngestionPipeline class
2. `entity_resolver.py` - EntityResolver class

**Fix Strategy:**
- Check if these were supposed to be created in previous work
- Create minimal working implementations
- Ensure imports work for ingestion_agent.py

---

### Priority 3: Remove Redis Dependency (30 minutes)
**Blocker:** Redis doesn't exist, BullMQ won't start
**User Requirement:** No Redis available

**Fix Strategy - Option A (Simple In-Memory):**
```typescript
// Replace BullMQ with simple in-memory queue
class SimpleDocumentQueue {
  private jobs: Map<string, DocumentJob> = new Map();
  async add(data: DocumentJobData) { /* ... */ }
  async process() { /* ... */ }
}
```

**Fix Strategy - Option B (File-Based):**
```typescript
// Use filesystem as simple queue
// Jobs stored as JSON files in /tmp/queue/
```

**Recommendation:** Option A (in-memory) for Tier 1 simplicity

---

### Priority 4: Serial Processing (15 minutes)
**User Requirement:** "we need to run serial, no parallel documents running"

**Current Code (WRONG):**
```typescript
// documentQueue.ts lines 155-165
await Promise.all([
  runPythonAgent('classifier_agent.py', {...}),
  runPythonAgent('ner_agent.py', {...})
]);
```

**Corrected Code (SERIAL):**
```typescript
// Sequential execution
await runPythonAgent('classifier_agent.py', {...});
await runPythonAgent('ner_agent.py', {...});
await runPythonAgent('ingestion_agent.py', {...});
```

---

### Priority 5: TypeScript Compilation (20 minutes)
**Errors to Fix:**
1. `documentQueue.ts(276,26): Property 'getLog' does not exist`
2. Install Jest types: `npm install --save-dev @types/jest`

---

### Priority 6: Run Actual Tests (30 minutes)
**After all fixes:**
```bash
source venv/bin/activate
pytest tests/ -v --tb=short
```
**Goal:** Get real test results, fix failures

---

## PHASE 0.3: CORRECTED ARCHITECTURE

### System Design (FACTS-BASED)

**Technology Stack (Verified):**
```yaml
backend:
  python: 3.12.3 ✅
  spacy: 3.8.7 ✅
  neo4j: accessible (568K nodes) ✅

frontend:
  nextjs: present ✅
  typescript: present ✅

NOT_AVAILABLE:
  redis: ❌ NOT RUNNING
  bullmq: ❌ DEPENDS ON REDIS
```

---

### Corrected Processing Flow (SERIAL)

```
Document Upload
    ↓
Simple Queue (in-memory Map)
    ↓
SERIAL Processing:
    ↓
[1] Classifier Agent → classify.json
    ↓
[2] NER Agent → entities.json + relationships.json
    ↓
[3] SBOM Agent (if SBOM file) → components.json + cves.json
    ↓
[4] Ingestion Agent → Neo4j
    ↓
Complete
```

**Key Changes from Previous (WRONG) Architecture:**
- ❌ Remove: Redis/BullMQ distributed queue
- ❌ Remove: Parallel document processing (4 workers)
- ❌ Remove: Promise.all() for classifier+NER
- ✅ Add: Simple in-memory queue (Map-based)
- ✅ Add: Sequential processing (one step after another)
- ✅ Add: Single document at a time

---

### File Structure (Corrected)

```
agents/
  base_agent.py ✅
  classifier_agent.py ✅
  ner_agent.py ✅
  sbom_agent.py ✅
  ingestion_agent.py ✅
  nlp_ingestion_pipeline.py ⚠️ TO CREATE
  entity_resolver.py ⚠️ TO CREATE

web_interface/
  lib/
    queue/
      documentQueue.ts ⚠️ TO FIX (remove Redis, add serial)
  config/
    redis.config.ts ❌ TO DELETE (Redis not used)

tests/
  test_*.py ⚠️ TO FIX (install deps, fix imports)
```

---

## PHASE 0.4: AGENT ASSIGNMENT STRATEGY

### RUV-SWARM Configuration

**Topology:** Hierarchical (1 coordinator → 6 specialists)

**Agent Roles:**

1. **Dependency Installer Agent** (backend-dev)
   - Install lib4sbom, cyclonedx, spdx
   - Verify imports work
   - 15 minutes

2. **Python Module Creator Agent** (coder)
   - Create nlp_ingestion_pipeline.py
   - Create entity_resolver.py
   - Ensure ingestion_agent imports work
   - 45 minutes

3. **Architecture Fixer Agent** (system-architect)
   - Remove Redis dependency from documentQueue.ts
   - Implement simple in-memory queue
   - Change parallel to serial processing
   - 30 minutes

4. **TypeScript Fixer Agent** (coder)
   - Fix documentQueue.ts getLog() error
   - Install @types/jest
   - Fix compilation errors
   - 20 minutes

5. **Test Runner Agent** (tester)
   - Run pytest with actual data
   - Document real test results
   - Fix failures found
   - 30 minutes

6. **Integration Validator Agent** (reviewer)
   - Test end-to-end flow with sample document
   - Verify serial processing works
   - Validate NER extraction
   - 30 minutes

**Total Estimated Time:** 2.5 hours (realistic, not aspirational)

---

## SUCCESS CRITERIA (FACTS-BASED)

### Phase 1 Success:
- ✅ All Python dependencies installed and importable
- ✅ Missing modules created and functional
- ✅ Redis removed, simple queue working
- ✅ Serial processing implemented

### Phase 2 Success:
- ✅ TypeScript compiles with zero errors
- ✅ Tests run (may have failures, but RUN)
- ✅ At least 1 integration test passes with real data

### Phase 3 Success:
- ✅ All results stored in Qdrant
- ✅ Honest status report generated
- ✅ Only claim what actually works

---

## ANTI-PATTERNS TO AVOID

**DON'T:**
- ❌ Claim tests pass without running them
- ❌ Document features that don't exist
- ❌ Trust agent output without verification
- ❌ Implement parallel when user needs serial
- ❌ Use technologies that aren't installed

**DO:**
- ✅ Run every test and show real output
- ✅ Verify every dependency is installed
- ✅ Read user requirements carefully
- ✅ Check actual system state before claiming
- ✅ Document only FACTS

---

## MEMORY PERSISTENCE PLAN

**Qdrant Namespace:** `aeon-pipeline-implementation`

**Checkpoints:**
- `phase0/verification-complete` ✅ STORED
- `phase0/strategy-defined` ← NEXT
- `phase1/swarm-initialized` ← PENDING
- `phase2/dependencies-installed` ← PENDING
- `phase2/modules-created` ← PENDING
- `phase2/redis-removed` ← PENDING
- `phase2/serial-processing` ← PENDING
- `phase2/tests-run` ← PENDING
- `phase3/final-results` ← PENDING

---

## PHASE 0 COMPLETION

**Status:** Phase 0 Complete
- ✅ Phase 0.1: System verification done
- ✅ Phase 0.2: Blockers prioritized
- ✅ Phase 0.3: Corrected architecture defined
- ✅ Phase 0.4: Agent strategy planned

**Next:** Phase 1 - Initialize RUV-SWARM and spawn specialist agents

---

**Generated:** 2025-01-05 08:01 UTC
**Protocol:** AEON PROJECT TASK EXECUTION PROTOCOL - Phase 0 Complete
**Session:** swarm-1762322591052
**Ready for:** Phase 1 Execution
