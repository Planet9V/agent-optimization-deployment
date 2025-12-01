# Task Verification System

## Purpose

This verification system makes it **IMPOSSIBLE** to skip tasks without detection. It provides automated, executable scripts that verify prerequisites, outcomes, and create blocking checkpoints.

## The Problem It Solves

**Task 2.2 was skipped** because:
1. No pre-task verification that prerequisites existed
2. No post-task verification that outcomes were achieved
3. No checkpoint gate to block progress when tasks incomplete
4. No cross-check between BLOTTER claims and database reality

This system prevents all four failure modes.

## Architecture

```
verification_system/
├── scripts/
│   ├── pre_task_check.sh      # Verify prerequisites before execution
│   ├── post_task_verify.sh    # Verify outcomes after execution
│   ├── checkpoint_gate.sh     # Block progress if tasks incomplete
│   └── blotter_verify.sh      # Cross-check BLOTTER vs reality
├── configs/
│   └── task_requirements.json # Task-specific requirements
└── evidence/
    ├── pre_check_*.json       # Pre-task verification evidence
    ├── post_check_*.json      # Post-task verification evidence
    └── blotter_verification_*.txt # BLOTTER verification reports
```

## How It Works

### 1. Pre-Task Verification (`pre_task_check.sh`)

**Blocks execution if prerequisites not met**

```bash
./verification_system/scripts/pre_task_check.sh <task_id> <taskmaster_file>
```

**What it checks:**
- All dependency tasks marked complete in taskmaster
- Verification evidence exists for dependencies
- Database prerequisites met (Qdrant collections, Neo4j nodes)
- Required data exists before task can proceed

**Example:**
```bash
./verification_system/scripts/pre_task_check.sh 2.2 TASKMASTER.md

# Output:
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PRE-TASK VERIFICATION: 2.2
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Task: Expand entities with Claude
# Dependencies: 1.1
#
# Checking dependency: 1.1
#   ✓ PASS: Dependency 1.1 completed
#   ✓ PASS: Evidence exists for 1.1
#
# Checking database prerequisites...
# Verifying Qdrant collection 'ner11_entities' exists...
#   ✓ PASS: Qdrant collection exists with 245 entities
#
# ✅ VERIFICATION PASSED: Task 2.2 may proceed
```

**Exit codes:**
- `0` = Verification passed, task may proceed
- `1` = Verification failed, task BLOCKED

### 2. Post-Task Verification (`post_task_verify.sh`)

**Verifies outcomes match expected results**

```bash
./verification_system/scripts/post_task_verify.sh <task_id> <taskmaster_file>
```

**What it checks:**
- Task-specific success criteria met
- Database state matches expectations
- Data quality and structure correct
- Outcomes verifiable with queries

**Task-specific checks:**

| Task | Verification |
|------|-------------|
| 1.1 | Qdrant collection exists with entities, proper structure |
| 2.2 | Entities have expansion_data field with description |
| 2.3 | Neo4j has Entity nodes with description properties |
| 2.4 | Neo4j has psychohistory relationships (INFLUENCES, PREDICTS, SHAPES) with confidence scores |

**Example:**
```bash
./verification_system/scripts/post_task_verify.sh 2.2 TASKMASTER.md

# Output:
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# POST-TASK VERIFICATION: 2.2
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Task: Expand entities with Claude
# Success Criteria: All entities have expansion data
#
# Verifying Task 2.2: Expanded entities in Qdrant...
# ✓ Found 245 expanded entities in Qdrant
# ✓ Expansion data has 'description' field
#
# ✅ VERIFICATION PASSED: Task 2.2 completed successfully
```

**Exit codes:**
- `0` = Verification passed, task successfully completed
- `1` = Verification failed, task must be re-executed

### 3. Checkpoint Gate (`checkpoint_gate.sh`)

**Blocks forward progress if ANY task incomplete**

```bash
./verification_system/scripts/checkpoint_gate.sh <taskmaster_file> [phase_number]
```

**What it checks:**
- All tasks in phase (or all tasks) marked complete
- Verification evidence exists for each task
- Database state matches all task requirements
- Displays comprehensive status table

**Example:**
```bash
./verification_system/scripts/checkpoint_gate.sh TASKMASTER.md 2

# Output:
# ╔════════════════════════════════════════════════════════════╗
# ║          CHECKPOINT GATE - TASK VERIFICATION              ║
# ╚════════════════════════════════════════════════════════════╝
#
# Checking Phase 2 tasks only
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TASK     DESCRIPTION                          REQUIRED        ACTUAL          STATUS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 2.1      Load catalog to Qdrant              Complete        Marked Complete ✅ PASS (Qdrant: 245 entities)
# 2.2      Expand entities with Claude         Complete        Incomplete      ❌ FAIL
# 2.3      Load to Neo4j                       Complete        No Verification ⚠️  WARN
# 2.4      Add psychohistory relationships     Complete        Incomplete      ❌ FAIL
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# Total tasks checked:    4
# Tasks passed:           1
# Tasks failed:           3
# Pass rate:              25.0%
#
# ╔════════════════════════════════════════════════════════════╗
# ║  ❌ CHECKPOINT FAILED - BLOCKING FORWARD PROGRESS          ║
# ╚════════════════════════════════════════════════════════════╝
#
# FAILED TASKS:
#   • 2.2: Not marked complete
#   • 2.3: Missing verification evidence
#   • 2.4: Database verification failed (Neo4j empty)
```

**Exit codes:**
- `0` = All tasks verified, may proceed
- `1` = Tasks incomplete, forward progress BLOCKED

### 4. BLOTTER Verification (`blotter_verify.sh`)

**Cross-checks BLOTTER claims against database reality**

```bash
./verification_system/scripts/blotter_verify.sh <blotter_file> <taskmaster_file>
```

**What it checks:**
- Completion claims in BLOTTER match taskmaster
- Verification evidence exists for claimed completions
- Database state supports completion claims
- No tasks marked complete without evidence

**Example:**
```bash
./verification_system/scripts/blotter_verify.sh BLOTTER.md TASKMASTER.md

# Output:
# ╔════════════════════════════════════════════════════════════╗
# ║        BLOTTER VERIFICATION - CLAIMS vs REALITY           ║
# ╚════════════════════════════════════════════════════════════╝
#
# Extracting completion claims from BLOTTER...
# Found completion claims:
# ✅ Task 1.1 COMPLETE
# ✅ Task 2.1 COMPLETE
# ✅ Task 2.2 COMPLETE
#
# Cross-checking claims against database state...
#
# ━━━ Task 1.1 ━━━
# BLOTTER Claim: ✅ Task 1.1 COMPLETE
# Taskmaster Status: ✅
# Verification Evidence: 1 file(s)
# Database Status: Qdrant has 245 entities
# ✅ VERIFIED: Claim matches reality
#
# ━━━ Task 2.2 ━━━
# BLOTTER Claim: ✅ Task 2.2 COMPLETE
# Taskmaster Status: ⏳
# Verification Evidence: 0 file(s)
# Database Status: No expanded entities in Qdrant
# ❌ DISCREPANCY: Claim does not match reality
# Discrepancy Details:
#   • Taskmaster not marked complete
#   • No verification evidence
#   • Database verification failed: No expanded entities in Qdrant
```

## Usage Workflow

### Standard Task Execution Flow

```bash
# 1. Before starting task: Verify prerequisites
./verification_system/scripts/pre_task_check.sh 2.2 TASKMASTER.md
# Exit 0 = proceed, Exit 1 = blocked

# 2. Execute the task
# ... do the actual work ...

# 3. After completing task: Verify outcomes
./verification_system/scripts/post_task_verify.sh 2.2 TASKMASTER.md
# Exit 0 = success, Exit 1 = failed

# 4. Update taskmaster if verification passed
# Mark task 2.2 as ✅ in TASKMASTER.md

# 5. Before moving to next phase: Run checkpoint
./verification_system/scripts/checkpoint_gate.sh TASKMASTER.md 2
# Exit 0 = proceed, Exit 1 = blocked
```

### Complete Workflow Example

```bash
#!/bin/bash
# Execute Task 2.2 with full verification

set -e  # Exit on any error

echo "Step 1: Pre-task verification"
./verification_system/scripts/pre_task_check.sh 2.2 TASKMASTER.md || {
    echo "❌ Prerequisites not met. Cannot proceed."
    exit 1
}

echo "Step 2: Execute task"
python scripts/expand_entities.py

echo "Step 3: Post-task verification"
./verification_system/scripts/post_task_verify.sh 2.2 TASKMASTER.md || {
    echo "❌ Task verification failed. Re-execute required."
    exit 1
}

echo "Step 4: Update taskmaster"
# Update task 2.2 status to ✅

echo "✅ Task 2.2 completed and verified"
```

## Integration with Existing System

### Qdrant Integration

The scripts directly query Qdrant REST API:

```bash
# Check collection exists
curl -s http://localhost:6333/collections | jq -r '.result.collections[].name'

# Get entity count
curl -s http://localhost:6333/collections/ner11_entities | jq -r '.result.points_count'

# Query for expanded entities
curl -s -X POST http://localhost:6333/collections/ner11_entities/points/scroll \
  -H "Content-Type: application/json" \
  -d '{"filter": {"must": [{"key": "expansion_data", "match": {"any": ["*"]}}]}, "limit": 100}'
```

### Neo4j Integration

The scripts use `cypher-shell` for verification:

```bash
# Count entity nodes
cypher-shell -u neo4j -p your_password \
  "MATCH (e:Entity) RETURN count(e) as count" \
  --format plain

# Count psychohistory relationships
cypher-shell -u neo4j -p your_password \
  "MATCH ()-[r:INFLUENCES|PREDICTS|SHAPES]->() RETURN count(r) as count" \
  --format plain
```

**Note:** Update Neo4j password in scripts as needed.

## Evidence Storage

All verification runs store evidence in JSON format:

```json
{
  "task_id": "2.2",
  "task_description": "Expand entities with Claude",
  "timestamp": "2025-11-28_14-30-45",
  "verification_type": "post_task",
  "checks_passed": 2,
  "checks_failed": 0,
  "verification_details": [
    "Expanded entities count: 245 PASS",
    "Expansion structure: PASS"
  ],
  "overall_result": "PASS"
}
```

Evidence files:
- `pre_check_<task_id>_<timestamp>.json` - Pre-task verification
- `post_check_<task_id>_<timestamp>.json` - Post-task verification
- `blotter_verification_<timestamp>.txt` - BLOTTER verification report

## Configuration

### Task Requirements

Create `verification_system/configs/task_requirements.json`:

```json
{
  "1.1": {
    "prerequisites": {
      "qdrant_running": true,
      "input_files": ["NER11_Gold_Full_Entity_Inventory/"]
    },
    "success_criteria": {
      "qdrant_collection": "ner11_entities",
      "min_entity_count": 100,
      "required_fields": ["entity_name", "entity_type"]
    }
  },
  "2.2": {
    "prerequisites": {
      "dependencies": ["1.1"],
      "qdrant_collection_exists": true,
      "min_entities": 100
    },
    "success_criteria": {
      "expansion_field": "expansion_data",
      "required_subfields": ["description", "context"],
      "min_expanded_count": 100
    }
  }
}
```

## Making Scripts Executable

```bash
chmod +x verification_system/scripts/*.sh
```

## Benefits

1. **Impossible to Skip Tasks**: Pre-checks block execution if prerequisites missing
2. **Verifiable Outcomes**: Post-checks verify database state matches expectations
3. **Automated Enforcement**: Checkpoint gates block progress if any task incomplete
4. **Audit Trail**: All verifications stored as evidence for review
5. **BLOTTER Integrity**: Cross-check prevents false completion claims

## Future Enhancements

1. **Integration with Taskmaster**: Auto-update taskmaster on verification success
2. **CI/CD Integration**: Run verification in automated pipelines
3. **Slack/Email Notifications**: Alert on verification failures
4. **Rollback Automation**: Auto-revert on verification failure
5. **Performance Tracking**: Measure verification execution time
6. **Database Snapshots**: Create snapshots on verification success

## Troubleshooting

### Common Issues

**Issue**: Scripts fail with "curl: command not found"
**Solution**: Install curl: `sudo apt-get install curl`

**Issue**: Scripts fail with "jq: command not found"
**Solution**: Install jq: `sudo apt-get install jq`

**Issue**: Qdrant connection refused
**Solution**: Ensure Qdrant running: `docker-compose up -d qdrant`

**Issue**: Neo4j authentication failed
**Solution**: Update password in scripts or set NEO4J_PASSWORD environment variable

**Issue**: Permission denied executing scripts
**Solution**: Make executable: `chmod +x verification_system/scripts/*.sh`

## Summary

This verification system makes task skipping **IMPOSSIBLE** by:

1. ✅ **Pre-task checks** block execution without prerequisites
2. ✅ **Post-task verification** confirms outcomes with database queries
3. ✅ **Checkpoint gates** block phase progression if tasks incomplete
4. ✅ **BLOTTER verification** detects false completion claims
5. ✅ **Evidence storage** creates audit trail for all verifications

**The system enforces task execution discipline through automated, executable verification.**
