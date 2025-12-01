# Batch Execution Quick Reference - Weeks 2-5

**File:** BATCH_EXECUTION_QUICK_REFERENCE.md
**Created:** 2025-11-23
**Version:** v1.0.0
**Purpose:** Daily reference for batch sequencing and validation procedures
**Status:** ACTIVE

---

## WEEK 2: BATCHES 1-2 (Cognitive Biases Foundation)

### BATCH 1: Core Cognitive Biases (Days 1-3, 25 files)

```
Files:           1-25
Categories:      Confirmation Bias (15) + Anchoring Bias (10)
Hours:           15 (0.6 hrs/file)
Entities Target: 375 (15 per file avg)
Validation:      100% - DUAL REVIEW REQUIRED

Annotation Checklist:
✓ Identify all cognitive bias manifestations
✓ Mark psychological entities (8 types)
✓ Link decision consequences
✓ Note contextual triggers
✓ Flag relationship chains

Quality Gate - ALL required:
✓ Every entity span marked
✓ No entity type missing
✓ IAA >0.85 on overlaps
✓ Conflict resolution documented
✓ Annotator comments clear
```

**Deliverable:** 25 annotated files + IAA report

---

### BATCH 2: Decision Context Biases (Days 4-6, 25 files)

```
Files:           26-50
Categories:      Dunning-Kruger (13) + False Consensus (12)
Hours:           15 (0.6 hrs/file)
Entities Target: 375 (15 per file avg)
Validation:      100% - CONSISTENCY CHECK vs BATCH 1

Dependency:      BATCH 1 must be complete
Quality Gate:    Consistency with BATCH 1 patterns established

Annotation Checklist:
✓ Apply BATCH 1 learned patterns
✓ Confirm terminology consistency
✓ Mark confidence/expertise entities
✓ Link social pressure triggers
✓ Maintain entity span standards

Quality Gate - ALL required:
✓ Same pattern consistency as BATCH 1
✓ Terminology variations documented
✓ IAA >0.85 maintained
✓ Ready for Phase 2
```

**Deliverable:** 50 annotated files + Week 2 completion report

---

## WEEK 3: BATCHES 3-5 (Cognitive Bias Completion + Incident Reports Start)

### BATCH 3: Advanced Cognitive Biases (Days 1-3, 25 files)

```
Files:           51-75
Categories:      Availability (8) + Sunk Cost (6) + In-Group (6) + Hindsight (5)
Hours:           15 (0.6 hrs/file)
Entities Target: 375
Validation:      100% - Final cognitive bias tier validation

Dependency:      BATCHES 1-2 complete
Quality Gate:    Cognitive bias tier consistency confirmed

Annotation Pattern (Established):
✓ 8 psychological entities per file
✓ Decision context entities
✓ Relationship chains (3-5 per file)
✓ Bias manifestation clarity
✓ Risk impact assessment

Quality Gate - ALL required:
✓ All 8 cognitive bias types covered
✓ Terminology consistent across tier
✓ Entity span accuracy >95%
✓ IAA >0.85
✓ Tier 1 ready for training
```

**Deliverable:** 75 cognitive bias files ready for model training

---

### BATCH 4: Risk Assessment Biases (Days 3-5, 25 files)

```
Files:           76-100
Categories:      Risk Assessment Biases (15) + Threat Perception Distortions (10)
Hours:           15 (0.6 hrs/file)
Entities Target: 375
Validation:      100% - TIER 1 COMPLETION GATE

Dependency:      BATCH 3 complete
Quality Gate:    Tier 1 quality validation

Annotation Focus (Advanced Patterns):
✓ Complex risk decision chains
✓ Threat perception entities
✓ Cognitive distortion sequences
✓ Escalation/de-escalation triggers
✓ Expert vs novice bias patterns

Quality Gate - GATE 1 VALIDATION:
✓ 100 cognitive bias files complete
✓ All 8 psychological entities present
✓ IAA >0.85 across 100 files
✓ Baseline F1 >0.70 estimated
✓ TIER 1 SIGNATURE: Gate 1 PASSED
```

**Deliverable:** 100 cognitive bias files + Gate 1 report

---

### BATCH 5: Incident Reports Introduction (Days 6-7+, 25 files)

```
Files:           101-125
Categories:      APT Campaigns (15) + Major Breaches (10)
Hours:           20 (0.8 hrs/file) - NEW COMPLEXITY
Entities Target: 500 (20 per file avg) - SCALE UP
Validation:      100% - ESTABLISH TECHNICAL ENTITY BASELINE

Dependency:      BATCH 4 complete (cognitive bias patterns internalized)
Quality Gate:    Technical entity extraction baseline validated

NEW ENTITY TYPES (10 technical):
✓ Threat_Actor
✓ Malware_Type
✓ Attack_Vector
✓ Vulnerability
✓ Compromised_Asset
✓ Indicator_of_Compromise
✓ Defense_Evasion
✓ Impact_Category
✓ Remediation_Action
✓ Information_System

Annotation Procedure (New):
✓ Attack chain sequencing
✓ Timeline entities
✓ Technical terminology accuracy
✓ Threat actor identification
✓ Relationship mapping (20+ types)
✓ Impact assessment

Quality Gate - TECHNICAL BASELINE:
✓ Attack chains clearly sequenced
✓ All 10 technical entities attempted
✓ 20+ relationship types used
✓ IAA >0.85 on entity boundaries
✓ Span accuracy >90%
✓ Ready for incident scale-up
```

**Deliverable:** 125 total annotated files + technical entity validation report

---

## WEEK 4: BATCHES 6-9 (Incident Scale + Sector Introduction)

### BATCH 6: Ransomware Analysis (Days 1-3, 25 files)

```
Files:           126-150
Categories:      Ransomware Cases (15) + Extortion Timelines (10)
Hours:           20 (0.8 hrs/file)
Entities Target: 500 (20 per file avg)
Validation:      75% (Reduce from 100% - baseline proven)

Dependency:      BATCH 5 complete
Quality Gate:    Ransomware-specific patterns established

Specialized Entities:
✓ Ransom_Demand (amount, deadline)
✓ Negotiation_Events
✓ Exfiltration_Details
✓ Encryption_Method
✓ Threat_Actor_Infrastructure
✓ Payment_Method
✓ Data_Type_Compromised

Validation Sampling:
- Sample 19 files (75%) for dual review
- Check: Entity consistency, attack pattern logic
- IAA threshold: >0.80 (relax from 0.85)

Quality Gate - RANSOMWARE FOCUS:
✓ Attack lifecycle entities clear
✓ Ransom negotiation captured
✓ Payment infrastructure marked
✓ Data exfiltration sequenced
✓ IAA >0.80
✓ Ready for supply chain complexity
```

**Deliverable:** 150 total files + ransomware pattern report

---

### BATCH 7: Supply Chain & ICS (Days 3-5, 25 files)

```
Files:           151-175
Categories:      Supply Chain Attacks (13) + ICS Incidents (12)
Hours:           20 (0.8 hrs/file)
Entities Target: 500 (20 per file avg)
Validation:      75% (19 files)

Dependency:      BATCH 6 complete
Quality Gate:    Multi-stage attack relationships mapped

Complex Entity Chains:
✓ Vendor_Dependency (A→B→C relationships)
✓ Software_Supply_Chain_Component
✓ ICS_Protocol (MODBUS, DNP3, OPC-UA)
✓ OT_Network_Segment
✓ Safety_Critical_System
✓ Production_Impact

Relationship Focus (Multi-hop):
- Vendor A → Software Component → Vulnerable Version → Attack Vector → Impact
- ICS Protocol → PLC → Production System → Safety Impact

Quality Gate - RELATIONSHIP VALIDATION:
✓ Vendor chains 3+ hops documented
✓ ICS protocol accuracy
✓ Dependency paths clear
✓ Safety impact entities marked
✓ IAA >0.80
✓ Complex relationships proven
```

**Deliverable:** 175 total files + supply chain/ICS relationship report

---

### BATCH 8: Zero-Day & Exploits (Days 5-7, 25 files)

```
Files:           176-200
Categories:      Zero-Day Analysis (15) + Exploit Code Studies (10)
Hours:           20 (0.8 hrs/file)
Entities Target: 500 (20 per file avg)
Validation:      50% (13 files) - Technical accuracy sampling

Dependency:      BATCH 7 complete
Quality Gate:    Technical exploit details validated

Technical Deep-Dive Entities:
✓ CVE_ID / CWE_ID
✓ Vulnerability_Type
✓ Root_Cause_Analysis
✓ Exploit_Technique
✓ Shellcode_Pattern
✓ Defense_Bypass_Method
✓ Patch_Details
✓ CVSS_Score

Annotation Complexity (High):
- Code snippet entity boundaries
- Technical accuracy critical
- Security impact clarity
- Patch/remediation linking

Quality Gate - TECHNICAL VALIDATION:
✓ CVE mapping accurate
✓ Vulnerability type correct
✓ Exploit mechanism clear
✓ Patch details linked
✓ IAA >0.80 on boundaries
✓ Ready for sector specialization
```

**Deliverable:** 200 total files + exploit technical validation report

---

### BATCH 9: Sector-Specific Introduction (Days 6-7+, 25 files)

```
Files:           201-225
Categories:      Critical Infrastructure Overview (10) + Energy Grid (8) + Water (7)
Hours:           18 (0.72 hrs/file) - Different timeline
Entities Target: 450 (18 per file avg)
Validation:      50% (13 files)

Dependency:      BATCH 5 baseline established (sector can start in parallel)
Quality Gate:    Sector-specific entity taxonomy established

Sector-Specific Entities (NEW vocabulary):
✓ Infrastructure_Asset_Type
✓ Sector_Regulation
✓ Critical_Function
✓ Asset_Criticality_Level
✓ Sector_Threat_Profile
✓ Compliance_Requirement

Critical Infrastructure Focus:
- Asset inventory entities
- Regulatory requirement mapping
- Threat landscape per sector
- Impact severity (Safety, Availability, Integrity)

Quality Gate - SECTOR FOUNDATION:
✓ CI terminology consistent
✓ Asset types accurately categorized
✓ Regulatory requirements marked
✓ Threat landscape for sectors clear
✓ IAA >0.75
✓ Foundation for sector scale-up
```

**Deliverable:** 225 total files + sector introduction report

---

## WEEK 5: BATCHES 10-13 (Incident Completion + Sector Expansion)

### BATCH 10: Threat Actor Profiles (Days 1-2, 20 files)

```
Files:           226-245
Categories:      APT Group Profiles (12) + Attribution Analysis (8)
Hours:           16 (0.8 hrs/file)
Entities Target: 400 (20 per file avg)
Validation:      50% (10 files)

Dependency:      BATCHES 5-8 complete (Incident Tier 2 closing)
Quality Gate:    Threat actor relationship networks mapped

Actor Profile Entities:
✓ Threat_Actor_ID (main identifier)
✓ Actor_Alias (alternative names)
✓ Attribution_Confidence (HIGH/MEDIUM/LOW)
✓ Known_TTPs (Tactics/Techniques/Procedures)
✓ Infrastructure_Indicators
✓ Geopolitical_Context
✓ Sponsorship_Indicator (State/Criminal/Hacktivist)

Relationship Networks:
- Actor A ≡ Alias B ≡ Alias C (Identity relationships)
- Actor A --uses--> Malware X
- Actor A --targets--> Sector Y
- Actor A --sponsors--> Actor B (Group relationships)

Quality Gate - GATE 2 (INCIDENT TIER COMPLETE):
✓ 145 incident files complete (Tiers 1-2 done)
✓ Technical entity accuracy >0.80
✓ 20+ relationship types mapped across incidents
✓ Attack chain sequencing validated
✓ IAA >0.80 on complex files
✓ GATE 2 SIGNATURE: Incident Tier PASSED
```

**Deliverable:** 245 total files + Gate 2 incident completion report

---

### BATCH 11: Healthcare & Biomedical (Days 2-3, 25 files)

```
Files:           246-270
Categories:      Healthcare Threats (13) + Medical Devices (12)
Hours:           18 (0.72 hrs/file)
Entities Target: 450 (18 per file avg)
Validation:      50% (13 files)

Dependency:      BATCH 9 complete (sector foundation)
Quality Gate:    Healthcare-specific threat landscape established

Healthcare-Specific Entities:
✓ Healthcare_Asset_Type (Hospital, Clinic, Medical Device)
✓ HIPAA_Compliance_Entity
✓ Medical_Device_Category
✓ Clinical_Impact_Type (Patient Safety, Data Privacy, Service Availability)
✓ Health_Information_Type
✓ Threat_Actor_Motivation_Healthcare (Criminal, State-sponsored, Activist)

Healthcare Threat Patterns:
- Ransomware impact on patient care
- Medical device manipulation
- Prescription drug manipulation
- Patient data exfiltration
- Insider threats

Quality Gate - HEALTHCARE SPECIALIZATION:
✓ HIPAA compliance entities accurate
✓ Medical device terminology correct
✓ Patient safety impact clear
✓ Threat actors for sector identified
✓ IAA >0.75
✓ Ready for other sectors
```

**Deliverable:** 270 total files + healthcare sector report

---

### BATCH 12: Finance & Government (Days 4-5, 25 files)

```
Files:           271-295
Categories:      Financial Institutions (13) + Government Systems (12)
Hours:           18 (0.72 hrs/file)
Entities Target: 450 (18 per file avg)
Validation:      40% (10 files) - Confidence in patterns growing

Dependency:      BATCH 11 complete
Quality Gate:    Finance/government threat patterns validated

Finance-Specific Entities:
✓ Financial_Asset_Type (Bank, Payment System, Trading Platform)
✓ Financial_Transaction_Component
✓ Regulatory_Framework (SOX, PCI-DSS, GLBA)
✓ Financial_Impact_Type (Loss, Fraud, Compliance Violation)
✓ Payment_Infrastructure

Government-Specific Entities:
✓ Government_System_Classification
✓ Classified_Information_Level
✓ Government_Regulation (FISMA, FedRAMP)
✓ Government_Compliance_Requirement

Cross-Domain Threats:
- Nation-state targeting both sectors
- APT group infrastructure patterns
- Regulatory compliance implications

Quality Gate - FINANCE/GOVERNMENT COVERAGE:
✓ Compliance framework accuracy
✓ Financial transaction entities clear
✓ Classified information handling correct
✓ Regulatory requirement mapping
✓ IAA >0.75
✓ Foundation for final sectors
```

**Deliverable:** 295 total files + finance/government report

---

### BATCH 13: Manufacturing & ICS Systems (Days 6-7, 25 files)

```
Files:           296-320
Categories:      Manufacturing (13) + Industrial Control Systems (12)
Hours:           18 (0.72 hrs/file)
Entities Target: 450 (18 per file avg)
Validation:      40% (10 files)

Dependency:      BATCH 12 complete
Quality Gate:    ICS-specific threat vocabulary and relationships

ICS/Manufacturing Entities:
✓ ICS_Component_Type (SCADA, PLC, DCS, HMI)
✓ ICS_Protocol (MODBUS, DNP3, OPC-UA, Profibus)
✓ OT_Network_Architecture
✓ Manufacturing_Asset_Type
✓ Production_Process_Impact
✓ Safety_System_Entity
✓ Asset_Criticality (Safety-Critical, Mission-Critical)

ICS Attack Patterns:
- PLC firmware manipulation
- SCADA data falsification
- Safety system bypass
- Production line sabotage
- Dual-use tool identification

Quality Gate - GATE 3 (SECTOR TIER COMPLETE):
✓ 100 sector-specific files complete
✓ All 16 CISA sectors represented (4 completed in detail, foundation for others)
✓ Sector-specific vocabulary consistent per domain
✓ Threat landscape per sector accurate
✓ IAA >0.75
✓ GATE 3 SIGNATURE: Sector Tier PASSED

Overall Status After Week 5:
✓ 345 files annotated (51% of 678)
✓ All 18 entity types validated
✓ Cognitive bias tier (100 files) - Complete
✓ Incident reports tier (145 files) - Complete
✓ Sector-specific (100 files) - Started, 4 sectors deep
✓ All 3 quality gates passed
✓ Ready for Weeks 6-7 final coverage
```

**Deliverable:** 320 total files + Gate 3 sector completion report

---

## VALIDATION PROCEDURE (Standard)

### 100% Validation (Week 2)
1. Both annotators independently mark entities
2. Calculate IAA (Cohen's Kappa) on overlapping spans
3. Resolve conflicts via consensus review
4. Document disagreement reasoning
5. Verify all 18 entity types present

### 75% Validation (Week 4 BATCHES 6-7)
1. Sample 75% of batch (19 of 25 files)
2. Both annotators review samples
3. Random sampling ensures no systematic bias
4. Same conflict resolution procedure
5. Full batch reviewed if IAA <0.80

### 50% Validation (Week 4 BATCH 8, Week 5 BATCHES 11-12)
1. Sample 50% of batch (13 of 25, 10 of 20)
2. Focus on complex entity types
3. Verify consistency with prior batches
4. Random sampling for objectivity
5. Escalate if patterns misaligned

### 40% Validation (Week 5 BATCH 13)
1. Sample 40% of batch (10 of 25)
2. Confidence in patterns high
3. Focus on sector-specific accuracy
4. Rapid spot-check procedure
5. Escalate immediately if IAA <0.75

---

## DAILY CHECKLIST TEMPLATE

```
DATE: ______________________
BATCH: ______________________

Morning (Pre-Annotation):
□ Files staged and accessible
□ Entity guidelines open
□ Prior batch conflicts resolved
□ Annotators briefed on focus areas
□ Prodigy/tool running

During Annotation:
□ Entity spans accurate
□ No placeholder entries
□ All entity types attempted
□ Relationships linked
□ Comments clear

End of Day:
□ Files saved and backed up
□ Progress logged
□ Blockers documented
□ Next day prep completed
□ IAA calculation queued (if validation day)
```

---

## SUCCESS SIGNALS

### Week 2 Complete ✓
- 50 cognitive bias files annotated
- IAA >0.85 established
- All 8 psychological entities in every file
- Foundation patterns documented

### Week 3 Complete ✓
- 100 cognitive bias files complete (TIER 1 DONE)
- 25 incident report files started (TIER 2 begun)
- Technical entity extraction validated
- Gate 1 PASSED - Cognitive bias tier quality confirmed

### Week 4 Complete ✓
- 100 incident report files processed
- 25 sector-specific files started
- 200 cumulative files (30%)
- Technical entity accuracy >0.80
- Relationship mapping validated

### Week 5 Complete ✓
- 145 incident files complete (TIER 2 DONE)
- 100 sector files complete (4 sectors)
- 295 cumulative files (44%)
- All quality gates passed
- Ready for Weeks 6-7 final coverage

---

## ESCALATION PROCEDURE

**If IAA <target threshold:**
1. Stop annotation, review last 10 files
2. Identify specific entity type confusion
3. Revise guidelines with examples
4. Re-annotate problem files
5. Re-calculate IAA
6. Document lesson learned

**If batch takes >estimated hours:**
1. Assess file complexity
2. Break files into smaller chunks
3. Reduce validation % (if allowed)
4. Resample for efficiency
5. Adjust future hour estimates

**If entity type missing from files:**
1. Check if entity type applies
2. If applies: retrain annotators, re-annotate
3. If doesn't apply: document exemption
4. Verify in prior batches

---

## DOCUMENT CONTROL

**Status:** ACTIVE - Ready for Week 2 execution
**Last Updated:** 2025-11-23
**Next Review:** End of Week 2 (validation of first gate)

