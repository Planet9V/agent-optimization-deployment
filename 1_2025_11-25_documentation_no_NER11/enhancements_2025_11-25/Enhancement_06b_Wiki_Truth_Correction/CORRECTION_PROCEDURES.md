# Wiki Correction Procedures & Governance
**Document Version:** 1.0.0 | **Created:** 2025-11-25 | **Effective Date:** 2025-12-01

---

## Executive Summary

This document establishes the procedures for correcting wiki documentation to align with verified database reality. It ensures that:
1. All wiki claims are evidence-based
2. Corrections follow a systematic process
3. No future discrepancies emerge
4. All changes are properly documented and auditable

**Key Principle:** **"No claim without database evidence"**

---

## SECTION 1: CORE GOVERNANCE PRINCIPLES

### Principle 1: Evidence-Based Documentation

**Statement:** Every factual claim in wiki documentation must be supported by verifiable database evidence.

**Implementation:**
- Before adding any metric to wiki: Execute database query
- Before updating any count: Verify with current database state
- Before claiming any capability: Test and document results
- Before publishing: Attach evidence reference

**Validation:** All wiki updates require inline citation to DATA_SOURCES.md query

**Enforcement Level:** MANDATORY for metrics and quantitative claims

---

### Principle 2: Single Source of Truth

**Statement:** Database is the single source of truth for all quantitative claims about the system.

**Implementation:**
- Wiki draws metrics from database queries only
- No estimates, projections, or theoretical values without explicit labeling
- Database state on specific date = fact for that date forward
- Any changes to database reflected in updated wiki metrics

**Validation:** Quarterly verification of all wiki metrics against database

**Enforcement Level:** MANDATORY for all counts, sizes, and metrics

---

### Principle 3: Transparency About Limitations

**Statement:** Documentation must be honest about what we know and don't know.

**Implementation:**
- Unverified claims marked as "unverified" or "pending verification"
- Theoretical vs. proven capabilities clearly distinguished
- Assumptions explicitly stated
- Confidence levels included with metrics

**Example:**
```
CORRECT: "Database supports up to 1 billion nodes (theoretical, unproven - current system: 1.1M nodes)"
WRONG:   "Scales to billions of nodes"
```

**Validation:** No marketing language; professional documentation standards

**Enforcement Level:** MANDATORY for all capability claims

---

### Principle 4: Audit Trail & Accountability

**Statement:** All changes to wiki documentation must be traceable and accountable.

**Implementation:**
- Every change logged in blotter.md with timestamp
- Change approval documented
- Evidence reference included
- Reason for change documented
- Changed-by user tracked

**Validation:** Complete audit trail maintained for every change

**Enforcement Level:** MANDATORY for all wiki updates

---

## SECTION 2: CORRECTING EXISTING CLAIMS

### Step 1: Identify Potential Discrepancy

**When:**
- During regular wiki audit
- When someone questions a claim
- When database changes significantly
- Monthly metric verification

**How:**
1. Read the wiki claim carefully
2. Identify the specific quantitative or capability statement
3. Note the wiki source document and location
4. Write down the exact claim to be verified

**Example:**
- **Source:** AEON_CONSTITUTION.md, line 47
- **Claim:** "537,043 Equipment entities across all sectors"
- **Type:** Quantitative metric

---

### Step 2: Query the Database

**Procedure:**

1. **Write the Query**
   - Determine which node types or properties to check
   - Write the most accurate Cypher query
   - Include filters that match the claim (e.g., "with sector")
   - Test query syntax before execution

2. **Execute the Query**
   - Run against production database
   - Timestamp the execution
   - Record the result
   - Run again to verify consistency

3. **Document the Result**
   - Query text (in TASKMASTER or DATA_SOURCES)
   - Execution timestamp
   - Result value
   - Performance metrics

**Template for Documenting:**
```markdown
**Query:** [Cypher code]
**Executed:** 2025-11-25 11:46:32 UTC
**Result:** [value]
**Consistency Verified:** [yes/no - multiple executions]
**Confidence Level:** [%]
**Performance:** [execution time]
```

**Example - Equipment Count:**
```cypher
MATCH (n:Equipment)
WHERE n.sector IS NOT NULL
RETURN count(n) AS equipment_count
```
Result: 29,774 (vs. wiki claim: 537,043)

---

### Step 3: Assess the Discrepancy

**Decision Framework:**

| Result vs. Claim | Action | Example |
|------------------|--------|---------|
| Match | Document as verified | 5,001 = 5,001 ✓ |
| Minor difference (≤5%) | Clarify claim | 5,050 vs. 5,001 - verify filter |
| Significant difference (5-50%) | Investigate root cause | 14,000 vs. 15,000 - count type issue? |
| Major difference (>50%) | CRITICAL CORRECTION | 29,774 vs. 537,043 - systematic error |

**Root Cause Analysis:**

When discrepancy found, investigate:
1. **Counting Method:** Did wiki use different counting method?
2. **Date:** Is wiki data from different time period?
3. **Filters:** Did wiki apply different filters (e.g., with/without sector)?
4. **Calculation:** Did wiki do calculation that database disproves?
5. **Source:** Did wiki cite source for the number?

**Documentation:**

Record findings in DISCREPANCIES.md:
```markdown
## DISCREPANCY: [Name]
**Wiki Claim:** [exact text]
**Database Reality:** [verified result]
**Discrepancy:** [difference and percentage]
**Root Cause:** [investigation finding]
**Evidence:** [query executed, confidence level]
```

---

### Step 4: Get Approval for Correction

**Approval Required From:**

| Severity | Approver | Timeline |
|----------|----------|----------|
| CRITICAL (>50% error) | Executive Sponsor | 24 hours |
| HIGH (20-50% error) | Department Lead | 48 hours |
| MEDIUM (5-20% error) | Team Lead | 3 days |
| LOW (<5% error) | Database Team | 1 day |

**Approval Process:**

1. **Prepare Correction Brief**
   - Current wiki claim
   - Database evidence
   - Why the correction is needed
   - Impact if not corrected

2. **Submit for Review**
   - Email stakeholders with brief
   - Include database query and result
   - Request approval/feedback

3. **Collect Signatures**
   - Maintain approval record in blotter.md
   - Document any objections/modifications
   - Get final sign-off before implementing

**Approval Template:**
```
CORRECTION APPROVAL

Change ID: CHG-XXX
Wiki Claim: "[original claim]"
Correction: "[new claim]"
Evidence: [query and result]

Approvals:
[ ] Stakeholder 1 - [name/date]
[ ] Stakeholder 2 - [name/date]
[ ] Stakeholder 3 - [name/date]

Status: [APPROVED / PENDING / REJECTED]
```

---

### Step 5: Implement the Correction

**Find All Instances:**

1. **Search for exact phrase**
   ```bash
   grep -r "537,043" /wiki/documents/
   grep -r "537043" /wiki/documents/
   ```

2. **Search for related variations**
   ```bash
   grep -r "Equipment entities" /wiki/documents/
   grep -r "537 thousand" /wiki/documents/
   grep -r "over 500 thousand" /wiki/documents/
   ```

3. **Search for paragraph context**
   - Look for broader discussions of equipment scale
   - Check tables and charts with this number
   - Find any analysis that depends on this number

4. **Document all locations**
   - List every file and line number
   - Note different variations of the claim
   - Identify if each instance needs updating

**Update Each Instance:**

For each location found:

1. **Review context** - Understand how claim is used in this specific location
2. **Determine appropriate correction** - May need different wording in different contexts
3. **Update the text**
   - Replace old claim with new claim
   - Add verification note if needed
   - Maintain document tone and style
4. **Add source reference** - Include footer noting database evidence
5. **Verify update** - Read corrected passage to ensure accuracy

**Example Update:**

**BEFORE:**
> "The AEON Digital Twin represents 537,043 Equipment entities across all critical infrastructure sectors"

**AFTER:**
> "The AEON Digital Twin represents 29,774 Equipment entities with sector classification across all critical infrastructure sectors. ¹"
>
> ¹ Equipment count verified: Database query executed 2025-11-25 11:46:32 UTC returned 29,774 Equipment nodes with sector property set

---

### Step 6: Document the Change

**Update blotter.md:**

Add entry with:
- Change ID (CHG-NNN)
- Timestamp of implementation
- Files modified (list each with line numbers)
- Exact change made (before/after)
- Why change was made
- Database evidence
- Approver sign-off
- Status (COMPLETED)

**Example Entry:**
```markdown
### COMPLETED CHANGE: CHG-XXX - [Change Name]

**Status:** ✅ COMPLETED
**Completion Timestamp:** 2025-11-25 16:45:00 UTC
**Files Updated:**
  1. AEON_CONSTITUTION.md (line 47, 89, 156)
  2. WIKI_COMPLETE_SUMMARY.md (section: Infrastructure Scale)
  3. [other files...]

**Change Made:**
  FROM: "537,043 Equipment entities"
  TO:   "29,774 Equipment entities with sector classification"

**Evidence:** Database query MATCH (n:Equipment) WHERE n.sector IS NOT NULL RETURN count(n)
**Executed:** 2025-11-25 11:46:32 UTC
**Result:** 29,774

**Approved By:** [names/dates]
**Updated By:** [name/date]
**Status:** COMPLETED
```

---

### Step 7: Verify the Corrections

**Quality Checks:**

- [ ] All instances updated
- [ ] No orphaned references remain
- [ ] Document reads naturally after changes
- [ ] Tone consistent with rest of document
- [ ] No contradictions introduced
- [ ] Source citations included where needed
- [ ] Grammar and spelling correct
- [ ] Version number incremented (if applicable)

**Verification Process:**

1. **Full text search** - Verify old claim no longer appears anywhere
2. **Context check** - Read each updated passage in full context
3. **Cross-reference check** - Ensure no other documents contradict this change
4. **Link check** - If document linked from elsewhere, verify it still makes sense

---

## SECTION 3: ADDING NEW CLAIMS

### Requirement: Database Evidence First

**Before adding ANY new quantitative claim to wiki:**

1. **Write the database query** that would verify the claim
2. **Execute the query** against current database
3. **Document the result** in DATA_SOURCES.md
4. **Include the evidence** in wiki when publishing claim

**Procedure:**

```
Step 1: Write claim you want to make
Step 2: Identify what database evidence would prove it
Step 3: Execute database query
Step 4: Compare expected result vs. actual result
Step 5: If match: Include query evidence in wiki
Step 6: If no match: Revise claim to match reality
```

**Examples:**

**Correct Process:**
```
1. Proposed claim: "System has 50,000 threat events"
2. Query: MATCH (n:ThreatEvent) RETURN count(n)
3. Execute: Returns 45,623
4. Action: Publish claim as "System has 45,623 documented threat events"
5. Include: Database evidence query in document
```

**Incorrect Process (Do NOT Do This):**
```
1. Proposed claim: "System has 50,000 threat events"
2. Publish without verification
3. Later discover actual count is 45,623
4. Credibility damaged
```

---

## SECTION 4: CAPABILITY CLAIMS

### Unverified vs. Proven Claims

**PROVEN CLAIM (What to Publish):**
> "The system stores and manages 1,104,066 nodes of critical infrastructure data. Verified 2025-11-25."

**UNPROVEN CLAIM (What NOT to Publish):**
> "The system can handle billions of nodes"

**CORRECT WAY TO STATE UNPROVEN CAPABILITY:**
> "The system is architected to scale to billions of nodes (unproven in production; current verified capacity: 1.1M nodes)"

### Capability Verification Template

Before claiming any capability, fill this out:

```
CAPABILITY CLAIM VERIFICATION

Capability Claimed: "[description]"

Verification Method:
  [ ] Tested in production
  [ ] Tested in staging
  [ ] Theoretical (architecture supports)
  [ ] Aspirational (planned but not implemented)
  [ ] Vendor claim (not independently verified)

Testing Date: [date or "not tested"]
Test Results: [what happened]
Confidence Level: [%]

Publication Version:
"[exact text to publish, including confidence caveat]"
```

---

## SECTION 5: QUALITY STANDARDS

### Documentation Standards for All Claims

**Quantitative Claims:**
```
✓ GOOD:   "Equipment entities: 29,774 (verified 2025-11-25)"
✓ GOOD:   "Equipment entities: 29,774¹" + footnote with evidence
✗ BAD:    "Over 25,000 Equipment entities"
✗ BAD:    "Equipment entities: ~30,000"
✗ BAD:    "Equipment entities: 537,043" [if database contradicts]
```

**Performance Claims:**
```
✓ GOOD:   "Average query response: 2.3 seconds (measured 2025-11-25)"
✓ GOOD:   "Query response time: 1.7-3.1 seconds"
✗ BAD:    "Sub-second response times" [when measured reality is 1.7-3.1 seconds]
✗ BAD:    "Real-time query execution" [without defining "real-time"]
```

**Capability Claims:**
```
✓ GOOD:   "Supports 1.1M nodes in production (verified), designed for 1B+ (unproven)"
✓ GOOD:   "Currently covers 10 sectors, with architecture for 50+ sectors"
✗ BAD:    "Covers 50+ sectors" [if only 10 implemented]
✗ BAD:    "Scales to billions" [without caveat about unproven scale]
```

### Confidence Level Standards

| Confidence | Standard | What This Means |
|-----------|----------|-----------------|
| 99%+ | Verified multiple times, consistent | This is definitely true |
| 95-98% | Verified with good certainty | Very high confidence |
| 80-94% | Verified with reasonable certainty | Good confidence |
| 50-79% | Partially verified or theoretical | Some uncertainty |
| <50% | Unverified or speculative | Should NOT be published as fact |

---

## SECTION 6: MONTHLY VERIFICATION PROCESS

### Every Month: Metric Re-Verification

**Schedule:** First Wednesday of each month

**Process:**

1. **Identify all quantitative claims** in wiki
2. **Execute verification queries** for each claim
3. **Compare results** to published numbers
4. **Flag any changes** >5% from previous month
5. **Investigate** any significant changes
6. **Update wiki** if changes warrant
7. **Document findings** in monthly verification report

**Monthly Verification Checklist:**

- [ ] Total node count verified
- [ ] InformationEvent count verified
- [ ] HistoricalPattern count verified
- [ ] FutureThreat count verified
- [ ] WhatIfScenario count verified
- [ ] Equipment (with sector) count verified
- [ ] Relationship type count verified
- [ ] Performance benchmarks re-run
- [ ] Geographic coverage verified
- [ ] Sector coverage verified

### Annual Comprehensive Audit

**Schedule:** January of each year

**Scope:**
- Re-verify ALL wiki claims
- Check for any new discrepancies
- Update documentation standards if needed
- Assess governance effectiveness

---

## SECTION 7: ESCALATION PROCEDURES

### What to Do When Discrepancies Are Found

**Minor Discrepancy Found (<5% difference):**
1. Document in notes
2. Investigate root cause
3. Clarify claim if needed
4. Update wiki if necessary
5. Low priority correction

**Significant Discrepancy Found (5-50% difference):**
1. Immediately notify database team
2. Investigate root cause thoroughly
3. Determine if database or wiki is wrong
4. Medium priority correction
5. Stakeholder notification

**Critical Discrepancy Found (>50% difference):**
1. IMMEDIATELY escalate to executive sponsor
2. Assess impact and risk
3. Halt publication of any related claims
4. Develop correction plan
5. HIGH priority correction
6. Executive communication

---

## SECTION 8: CONTINUOUS IMPROVEMENT

### Governance Feedback Loop

**Monthly Review:**
- Are corrections being made on schedule?
- Are new discrepancies emerging?
- Is governance working?
- What improvements needed?

**Process Improvements:**
- Track metrics on governance effectiveness
- Gather team feedback on procedures
- Refine process based on learnings
- Update this document as needed

---

## APPENDIX A: VERIFICATION QUERY TEMPLATES

### Total Count Verification
```cypher
MATCH (n)
RETURN count(n) AS total_count
```

### By Label Count
```cypher
MATCH (n:LABEL_NAME)
RETURN count(n) AS label_count
```

### By Property Value
```cypher
MATCH (n)
WHERE n.property_name = 'value'
RETURN count(n) AS count
```

### With Multiple Filters
```cypher
MATCH (n:LABEL_NAME)
WHERE n.property1 IS NOT NULL AND n.property2 = 'value'
RETURN count(n) AS filtered_count
```

### Distribution by Category
```cypher
MATCH (n)
WHERE n.category IS NOT NULL
RETURN n.category AS category, count(n) AS count
ORDER BY count DESC
```

---

## APPENDIX B: APPROVAL FORMS

### Standard Correction Approval Form

```
WIKI CORRECTION APPROVAL

Change ID: CHG-___
Date: _________

CHANGE DETAILS:
Wiki Document: _______________
Current Claim: _______________
Proposed Change: _______________
Reason for Change: _______________

DATABASE EVIDENCE:
Query: _______________
Result: _______________
Execution Date/Time: _______________
Confidence Level: ____%

IMPACT ASSESSMENT:
Users Affected: _______________
Risk if Not Corrected: _______________
Risk of Correction: _______________

APPROVALS:
[ ] _____________ Date: ___ (Stakeholder 1)
[ ] _____________ Date: ___ (Stakeholder 2)
[ ] _____________ Date: ___ (Stakeholder 3)

IMPLEMENTATION:
Implemented By: _____________ Date: ___
Verification Completed: [ ] Yes [ ] No
Status: [ ] COMPLETED [ ] IN PROGRESS [ ] PENDING
```

---

## GLOSSARY

| Term | Definition |
|------|-----------|
| **Evidence-Based** | Supported by verified database query results |
| **Discrepancy** | Difference between wiki claim and database reality |
| **Verification** | Running database query to confirm claim |
| **Audit Trail** | Complete record of all changes and approvals |
| **Single Source of Truth** | Database is authoritative for system metrics |
| **Confidence Level** | Percentage certainty of a claim's accuracy |
| **Root Cause** | The underlying reason for a discrepancy |

---

**Document Owner:** Code Implementation Agent
**Effective Date:** 2025-12-01
**Last Updated:** 2025-11-25 16:00:00 UTC
**Status:** READY FOR TEAM ADOPTION
**Version:** 1.0.0

### Next Steps for Teams:
1. Review and provide feedback
2. Schedule training on new procedures
3. Implement for all future wiki updates
4. Begin monthly verification process
