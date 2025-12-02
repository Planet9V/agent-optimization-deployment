# Verification System Quick Start Guide

## Setup (One-Time)

```bash
# Navigate to project directory
cd /home/jim/2_OXOT_Projects_Dev/1_2025_11-25_documentation_no_NER11/enhancements/Enhancement_27_Entity_Expansion_Psychohistory

# Make scripts executable (already done)
chmod +x verification_system/scripts/*.sh

# Create evidence directory
mkdir -p verification_system/evidence

# Install dependencies (if not already installed)
sudo apt-get install -y curl jq
```

## Daily Usage

### Before Starting Any Task

```bash
# Verify prerequisites before executing task
./verification_system/scripts/pre_task_check.sh <task_id> TASKMASTER.md

# Example for Task 2.2:
./verification_system/scripts/pre_task_check.sh 2.2 TASKMASTER.md

# If it exits with code 0 (✅), you can proceed
# If it exits with code 1 (❌), prerequisites not met - BLOCKED
```

### After Completing Any Task

```bash
# Verify outcomes match expected results
./verification_system/scripts/post_task_verify.sh <task_id> TASKMASTER.md

# Example for Task 2.2:
./verification_system/scripts/post_task_verify.sh 2.2 TASKMASTER.md

# If it exits with code 0 (✅), task verified - mark complete
# If it exits with code 1 (❌), verification failed - re-execute task
```

### Before Moving to Next Phase

```bash
# Run checkpoint gate to verify ALL tasks in phase
./verification_system/scripts/checkpoint_gate.sh TASKMASTER.md <phase>

# Example for Phase 2:
./verification_system/scripts/checkpoint_gate.sh TASKMASTER.md 2

# Example for ALL phases:
./verification_system/scripts/checkpoint_gate.sh TASKMASTER.md all

# If it exits with code 0 (✅), all tasks verified - proceed
# If it exits with code 1 (❌), incomplete tasks - BLOCKED
```

### Verify BLOTTER Accuracy

```bash
# Cross-check BLOTTER claims against database reality
./verification_system/scripts/blotter_verify.sh BLOTTER.md TASKMASTER.md

# If it exits with code 0 (✅), BLOTTER accurate
# If it exits with code 1 (❌), discrepancies found - update BLOTTER
```

## Complete Task Execution Pattern

```bash
#!/bin/bash
# Example: Execute Task 2.2 with full verification

TASK_ID="2.2"
TASKMASTER="TASKMASTER.md"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Executing Task ${TASK_ID} with Verification"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Step 1: Pre-task verification
echo "Step 1: Checking prerequisites..."
./verification_system/scripts/pre_task_check.sh "$TASK_ID" "$TASKMASTER" || {
    echo "❌ Prerequisites not met. Cannot proceed."
    exit 1
}

# Step 2: Execute the actual task
echo "Step 2: Executing task..."
# YOUR TASK EXECUTION HERE
# Example: python scripts/expand_entities.py

# Step 3: Post-task verification
echo "Step 3: Verifying outcomes..."
./verification_system/scripts/post_task_verify.sh "$TASK_ID" "$TASKMASTER" || {
    echo "❌ Task verification failed. Re-execute required."
    exit 1
}

# Step 4: Update taskmaster
echo "Step 4: Updating taskmaster..."
# Mark task as ✅ in TASKMASTER.md

echo "✅ Task ${TASK_ID} completed and verified!"
```

## Verification Workflow Diagram

```
┌─────────────────────────────────────────┐
│  Start Task N                           │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│  Run: pre_task_check.sh N               │
│  Checks:                                │
│  • Dependencies complete?               │
│  • Database prerequisites met?          │
└─────────────────┬───────────────────────┘
                  │
        ┌─────────┴─────────┐
        │                   │
    Exit 0              Exit 1
    (PASS)              (FAIL)
        │                   │
        ▼                   ▼
    ┌───────┐         ┌──────────┐
    │Proceed│         │ BLOCKED  │
    └───┬───┘         └──────────┘
        │
        ▼
┌─────────────────────────────────────────┐
│  Execute Task N                         │
│  (Do the actual work)                   │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│  Run: post_task_verify.sh N             │
│  Checks:                                │
│  • Database state correct?              │
│  • Success criteria met?                │
└─────────────────┬───────────────────────┘
                  │
        ┌─────────┴─────────┐
        │                   │
    Exit 0              Exit 1
    (PASS)              (FAIL)
        │                   │
        ▼                   ▼
    ┌───────┐         ┌──────────┐
    │Mark ✅│         │Re-execute│
    └───┬───┘         └──────────┘
        │
        ▼
┌─────────────────────────────────────────┐
│  Move to Next Task                      │
└─────────────────────────────────────────┘
```

## Phase Checkpoint Workflow

```
┌─────────────────────────────────────────┐
│  Complete all tasks in Phase N          │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│  Run: checkpoint_gate.sh TASKMASTER N   │
│  Checks:                                │
│  • All tasks marked complete?           │
│  • All tasks have verification?         │
│  • Database state matches all tasks?    │
└─────────────────┬───────────────────────┘
                  │
        ┌─────────┴─────────┐
        │                   │
    Exit 0              Exit 1
    (PASS)              (FAIL)
        │                   │
        ▼                   ▼
    ┌───────┐         ┌──────────┐
    │ Next  │         │ BLOCKED  │
    │ Phase │         │Fix Failed│
    └───────┘         └──────────┘
```

## Interpreting Results

### Pre-Task Check Output

```
✅ VERIFICATION PASSED
• All dependencies complete
• Database prerequisites met
• Task may proceed

❌ VERIFICATION FAILED
• Failed dependencies: 1.1, 2.1
• Database prerequisites not met
• Task BLOCKED
```

### Post-Task Verification Output

```
✅ VERIFICATION PASSED
• Checks passed: 3
• Checks failed: 0
• Task completed successfully

❌ VERIFICATION FAILED
• Checks passed: 1
• Checks failed: 2
• Task must be re-executed
```

### Checkpoint Gate Output

```
✅ CHECKPOINT PASSED
• Total tasks: 4
• Tasks passed: 4
• Tasks failed: 0
• Pass rate: 100.0%

❌ CHECKPOINT FAILED
• Total tasks: 4
• Tasks passed: 2
• Tasks failed: 2
• FAILED TASKS:
  • 2.2: Not marked complete
  • 2.4: Database verification failed
```

### BLOTTER Verification Output

```
✅ BLOTTER VERIFIED
• Total claims: 5
• Claims verified: 5
• Discrepancies: 0

❌ BLOTTER DISCREPANCIES
• Total claims: 5
• Claims verified: 3
• Discrepancies: 2
• Discrepancy details: [see report]
```

## Evidence Files

All verification runs create evidence files in `verification_system/evidence/`:

```
verification_system/evidence/
├── pre_check_2.2_2025-11-28_14-30-45.json
├── post_check_2.2_2025-11-28_15-45-20.json
├── blotter_verification_2025-11-28_16-00-10.txt
└── ...
```

These files provide audit trail for all verification activities.

## Common Scenarios

### Scenario 1: Starting Task 2.2

```bash
# Check if can start
./verification_system/scripts/pre_task_check.sh 2.2 TASKMASTER.md

# If BLOCKED:
# - Complete dependency tasks first (1.1, 2.1)
# - Verify Qdrant has entities loaded

# If PASSED:
# - Proceed with task execution
```

### Scenario 2: Completed Task but Verification Failed

```bash
# After running task, verify
./verification_system/scripts/post_task_verify.sh 2.2 TASKMASTER.md

# If FAILED:
# - Review verification output
# - Check database state with manual queries
# - Re-execute task to fix issues
# - Verify again until PASS
```

### Scenario 3: Ready to Move to Next Phase

```bash
# Verify all Phase 2 tasks complete
./verification_system/scripts/checkpoint_gate.sh TASKMASTER.md 2

# If BLOCKED:
# - Review failed tasks list
# - Execute/fix failed tasks
# - Verify each with post_task_verify.sh
# - Re-run checkpoint until PASS

# If PASSED:
# - Proceed to Phase 3
```

### Scenario 4: BLOTTER Claims Don't Match Reality

```bash
# Verify BLOTTER accuracy
./verification_system/scripts/blotter_verify.sh BLOTTER.md TASKMASTER.md

# If DISCREPANCIES:
# - Review discrepancy report
# - Fix database state or update BLOTTER
# - Re-verify until claims match reality
```

## Integration with Existing Scripts

### Update Task Execution Scripts

Add verification to your existing task scripts:

```python
# expand_entities.py (example)
import subprocess
import sys

def verify_prerequisites():
    """Run pre-task verification"""
    result = subprocess.run(
        ['./verification_system/scripts/pre_task_check.sh', '2.2', 'TASKMASTER.md'],
        capture_output=True
    )
    if result.returncode != 0:
        print("❌ Prerequisites not met")
        sys.exit(1)

def verify_outcomes():
    """Run post-task verification"""
    result = subprocess.run(
        ['./verification_system/scripts/post_task_verify.sh', '2.2', 'TASKMASTER.md'],
        capture_output=True
    )
    if result.returncode != 0:
        print("❌ Task verification failed")
        sys.exit(1)

if __name__ == "__main__":
    verify_prerequisites()
    # ... do actual work ...
    verify_outcomes()
```

## Best Practices

1. ✅ **Always run pre-check before task execution**
2. ✅ **Always run post-verification after task completion**
3. ✅ **Run checkpoint gate before phase transitions**
4. ✅ **Run BLOTTER verification periodically (daily/weekly)**
5. ✅ **Review evidence files when verification fails**
6. ✅ **Don't mark tasks complete without post-verification PASS**
7. ✅ **Store evidence files in version control for audit trail**

## Summary

This verification system ensures **no task can be skipped** by:

1. **Pre-checks** verify prerequisites before execution
2. **Post-checks** verify outcomes match expectations
3. **Checkpoint gates** block progress if tasks incomplete
4. **BLOTTER verification** detects false completion claims
5. **Evidence storage** creates audit trail

**Use the scripts religiously to maintain task execution discipline.**
