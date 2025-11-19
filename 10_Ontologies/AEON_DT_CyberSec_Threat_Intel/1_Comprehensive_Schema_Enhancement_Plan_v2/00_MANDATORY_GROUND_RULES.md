# MANDATORY GROUND RULES FOR SCHEMA ENHANCEMENT

**File:** 00_MANDATORY_GROUND_RULES.md
**Created:** 2025-10-30 00:00:00 UTC
**Version:** v2.0.0
**Author:** AEON Forge Development Team
**Purpose:** Non-negotiable rules governing all schema enhancement activities
**Status:** ACTIVE - MUST BE FOLLOWED WITHOUT EXCEPTION

## Document Overview

This document establishes the immutable ground rules that govern all schema enhancement activities for the AEON Digital Twin Cybersecurity Threat Intelligence ontology. These rules are NON-NEGOTIABLE and MUST be followed by all team members, automated processes, and third-party contributors without exception. Violation of these rules will result in immediate work stoppage and mandatory rollback procedures.

The purpose of these ground rules is to protect the integrity of the existing 147,923 CVE nodes and 35,146 supporting nodes (183,069 total) while enabling systematic enhancement to reach the target state of 307,569+ nodes. Every rule has been designed based on enterprise data governance best practices and lessons learned from large-scale ontology evolution projects.

---

## 1. CVE PRESERVATION POLICY (NON-NEGOTIABLE)

### 1.1 The Sacred 147,923: Absolute Protection

The 147,923 CVE nodes represent the foundation and primary value of this ontology. These nodes are the result of extensive data ingestion, validation, and relationship mapping that cannot be recreated without significant cost and risk. Therefore, the following rules apply:

**RULE 1.1.1 - Zero CVE Node Deletion**: Under NO circumstances shall any of the 147,923 CVE nodes be deleted, archived, deprecated, or marked as inactive. Every CVE node that exists today must exist in every future version of the ontology.

**RULE 1.1.2 - No CVE Re-Import**: The CVE data import process shall NOT be repeated. The existing CVE nodes are authoritative. If CVE data appears missing or incorrect, the solution is targeted correction, not bulk re-import.

**RULE 1.1.3 - CVE Node Immutability**: The core properties of CVE nodes (CVE-ID, description, severity scores, publication dates) are immutable. These properties may only be updated to correct factual errors, never for schema restructuring purposes.

**RULE 1.1.4 - Relationship Addition Only**: New relationships may be added to CVE nodes to connect them to enhancement nodes. Existing relationships to CVE nodes may NOT be removed unless proven to be factually incorrect.

### 1.2 Verification and Protection Procedures

**RULE 1.2.1 - Pre-Enhancement CVE Census**: Before any enhancement wave begins, an automated census must count and record the exact number of CVE nodes. This census establishes the baseline that must be preserved.

**RULE 1.2.2 - Post-Enhancement CVE Verification**: After any enhancement activity (batch update, relationship addition, property modification), an automated verification process must confirm that all 147,923 CVE nodes still exist and that no CVE node properties have been improperly modified.

**RULE 1.2.3 - CVE Node Checksum Validation**: A cryptographic checksum of core CVE node properties (CVE-ID, publication date, base severity) shall be calculated before enhancement activities. This checksum must validate successfully after any changes.

**RULE 1.2.4 - Automated Rollback Triggers**: Any process that results in CVE node count reduction, CVE-ID modification, or CVE core property corruption shall trigger an immediate automated rollback to the last known good state.

### 1.3 CVE Enhancement Allowances

While CVE nodes are protected, the following enhancements ARE permitted:

**PERMITTED 1.3.1 - Adding New Relationships**: CVE nodes may have new relationships added to connect them to attack patterns, threat actors, vulnerability categories, affected systems, and mitigation strategies.

**PERMITTED 1.3.2 - Adding Non-Core Properties**: New properties may be added to CVE nodes (tags, sector-specific risk scores, remediation links) as long as core properties remain unchanged.

**PERMITTED 1.3.3 - Correcting Factual Errors**: If a CVE node contains factually incorrect information verified against official NVD data, targeted correction is permitted with full audit logging.

**PERMITTED 1.3.4 - Enhancing CVE Context**: Nodes that provide context for CVE nodes (attack techniques, affected products, mitigation strategies) may be added freely as long as they connect to, rather than replace, CVE nodes.

### 1.4 CVE Protection Monitoring

**RULE 1.4.1 - Real-Time CVE Monitoring**: A monitoring system shall run continuously to detect any unexpected changes to CVE node count or properties. Anomalies trigger immediate investigation.

**RULE 1.4.2 - Weekly CVE Integrity Reports**: Every Friday, an automated report shall verify CVE node integrity, count stability, and relationship health. Any anomalies require executive review before proceeding.

**RULE 1.4.3 - Quarterly CVE Deep Audits**: Every quarter, a manual deep audit shall verify a statistical sample of CVE nodes (minimum 1,000 nodes) to ensure data quality and relationship accuracy.

---

## 2. ENHANCEMENT-ONLY PHILOSOPHY

### 2.1 Additive-Only Principle

The schema enhancement project operates under the principle of "addition, never subtraction." This philosophy ensures that existing ontology value is preserved while new capabilities are layered on top.

**RULE 2.1.1 - No Node Deletion Policy**: No existing nodes of any type (CVE, organization, system, sector, etc.) shall be deleted. Nodes that become obsolete shall be marked with a lifecycle property ("deprecated") but remain in the ontology.

**RULE 2.1.2 - No Relationship Removal Policy**: Existing relationships shall not be removed unless they are factually incorrect or duplicate relationships to identical targets. Relationship refinement is achieved through addition of more precise relationships, not removal of existing ones.

**RULE 2.1.3 - No Property Elimination**: Existing node properties shall not be removed. If a property becomes obsolete, it shall be marked as deprecated but retained for backward compatibility.

**RULE 2.1.4 - No Schema Breaking Changes**: Changes to the ontology schema shall be backward compatible. Existing queries, integrations, and applications shall continue to function after enhancement waves.

### 2.2 Backward Compatibility Requirements

**RULE 2.2.1 - Query Preservation**: All existing Cypher queries documented in project repositories must continue to execute successfully after enhancement. Query result sets may expand (more nodes returned) but must not contract (fewer nodes returned) unless correcting data quality issues.

**RULE 2.2.2 - API Contract Stability**: Any APIs or integration points that expose ontology data must maintain their contracts. Response formats may be extended with new optional fields but existing fields must remain unchanged.

**RULE 2.2.3 - Visualization Compatibility**: Existing visualization tools and dashboards must continue to function. New node types and relationships may be added to visualizations, but existing elements must render as before.

**RULE 2.2.4 - Client Application Resilience**: Client applications that consume ontology data shall not break due to schema enhancements. This requires that new node types and properties be introduced in a way that existing clients can safely ignore them.

### 2.3 Enhancement Validation Gates

**RULE 2.3.1 - Pre-Enhancement Testing**: Before applying any enhancement to production, it must be tested in a complete clone of the production ontology. All regression tests must pass before promotion.

**RULE 2.3.2 - Backward Compatibility Test Suite**: A comprehensive test suite of existing queries, integrations, and use cases must execute successfully against the enhanced ontology clone before production deployment.

**RULE 2.3.3 - Performance Regression Testing**: Query performance benchmarks must be captured before enhancement and verified after enhancement. Performance degradation beyond 10% requires optimization before deployment.

**RULE 2.3.4 - Rollback Readiness**: Every enhancement deployment must have a tested rollback procedure that can restore the previous state within 15 minutes if critical issues are discovered.

### 2.4 Deprecation Lifecycle Management

When nodes, relationships, or properties become obsolete, the following deprecation lifecycle applies:

**RULE 2.4.1 - Deprecation Marking**: Obsolete elements shall be marked with a property `lifecycleStatus: "deprecated"` and a property `deprecationDate: "YYYY-MM-DD"`. They remain in the ontology for historical reference.

**RULE 2.4.2 - Deprecation Documentation**: A centralized deprecation log shall document what was deprecated, why, when, and what replacement (if any) should be used instead.

**RULE 2.4.3 - Deprecation Retention Policy**: Deprecated elements shall be retained for a minimum of 24 months before any consideration of archival. Archival (moving to a separate historical ontology) requires executive approval.

**RULE 2.4.4 - Deprecation Impact Analysis**: Before marking anything as deprecated, an impact analysis must identify all queries, integrations, and applications that reference it. Affected stakeholders must be notified 90 days in advance.

---

## 3. NO TRUNCATION STANDARDS

### 3.1 Complete Documentation Requirement

All documentation, plans, specifications, and technical artifacts produced for this project must be COMPLETE. Truncation, summarization, and abbreviated content are forbidden in all formal deliverables.

**RULE 3.1.1 - Full Content Mandate**: Every document, plan, specification, and report shall contain complete information. There shall be no sections marked "abbreviated for brevity," "see separate document," or "details omitted."

**RULE 3.1.2 - Minimum Word Counts**: Strategic documents have minimum word counts: Ground Rules (3,000 words), Master Plan (15,000 words), Wave Plans (8,000 words each), Technical Specifications (5,000 words each). These are minimums, not targets.

**RULE 3.1.3 - Section Completeness**: Every section in every document must be fully written with complete sentences, detailed explanations, concrete examples, and actionable guidance. No placeholders, no "TBD" markers.

**RULE 3.1.4 - Example and Reference Inclusion**: Documents must include complete examples, sample data, reference queries, code snippets, and visual diagrams. References to external resources must include full citations.

### 3.2 Forbidden Phrases and Markers

The following phrases and patterns are FORBIDDEN in all project deliverables:

**FORBIDDEN 3.2.1 - Truncation Indicators**:
- "... (content abbreviated for brevity)"
- "... (details omitted)"
- "See separate document for details"
- "Further details available upon request"
- "TBD" or "To Be Determined" in final deliverables
- "[Content continues in next section]" unless it actually continues

**FORBIDDEN 3.2.2 - Summary Disclaimers**:
- "This is a high-level summary; full details available elsewhere"
- "For detailed information, see..."
- "Executive summary only; technical appendix separate"
- Any indication that the document is incomplete

**FORBIDDEN 3.2.3 - Placeholder Text**:
- "Lorem ipsum" or other dummy text
- "[Insert details here]"
- "Example TBD"
- "Section under development"
- Any bracketed placeholders in final versions

**FORBIDDEN 3.2.4 - Referral to Missing Content**:
- "As detailed in the full specification (not included here)"
- "Complete analysis available in separate report"
- "See appendix (appendix not attached)"

### 3.3 Quality Verification Process

**RULE 3.3.1 - Automated Completeness Scanning**: Before any document is marked as final, an automated scanner shall check for forbidden phrases, minimum word counts, and section completeness markers.

**RULE 3.3.2 - Peer Review for Completeness**: Every major deliverable shall be peer-reviewed with a specific checklist item: "Is this document complete with no truncation or omission?"

**RULE 3.3.3 - Executive Sign-Off on Completeness**: Project leadership must explicitly certify that strategic documents (Master Plan, Wave Plans) are complete before work based on those documents can proceed.

**RULE 3.3.4 - Completeness Rejection Authority**: Any team member has the authority to reject a document that contains truncation markers or incomplete sections. The document must be completed before acceptance.

### 3.4 Completeness Examples

**EXAMPLE 3.4.1 - Incomplete Node Description (FORBIDDEN)**:
```
AttackPattern Node: Represents attack techniques... (see MITRE ATT&CK for full details)
```

**EXAMPLE 3.4.2 - Complete Node Description (REQUIRED)**:
```
AttackPattern Node: Represents a documented attack technique or procedure used by threat actors to compromise systems or exfiltrate data. Each AttackPattern node includes:
- Unique identifier (ATT&CK technique ID)
- Name and description (minimum 200 characters)
- Tactics (what the attacker is trying to achieve)
- Detection methods (how defenders can identify this technique)
- Mitigation strategies (how to prevent or reduce impact)
- Example usage by known threat actors
- Related CVEs that enable this attack pattern
- Affected system types and configurations

Example: AttackPattern "T1059.001 - PowerShell" describes how attackers abuse PowerShell for command execution, including detection through PowerShell logging (Event ID 4104) and mitigation through Constrained Language Mode and execution policies.
```

---

## 4. MULTI-SECTOR COVERAGE REQUIREMENTS

### 4.1 Critical Infrastructure Sector Mandate

The ontology must provide comprehensive coverage for all 16 U.S. Critical Infrastructure Sectors as defined by CISA. This is non-negotiable as the ontology is designed to serve multi-sector threat intelligence needs.

**RULE 4.1.1 - All 16 Sectors Required**: The ontology must include detailed coverage for every one of the 16 critical infrastructure sectors:
1. Chemical Sector
2. Commercial Facilities Sector
3. Communications Sector
4. Critical Manufacturing Sector
5. Dams Sector
6. Defense Industrial Base Sector
7. Emergency Services Sector
8. Energy Sector
9. Financial Services Sector
10. Food and Agriculture Sector
11. Government Facilities Sector
12. Healthcare and Public Health Sector
13. Information Technology Sector
14. Nuclear Reactors, Materials, and Waste Sector
15. Transportation Systems Sector
16. Water and Wastewater Systems Sector

**RULE 4.1.2 - Sector-Specific Node Requirements**: Each sector must have dedicated nodes representing:
- Sector-specific systems and technologies (minimum 50 nodes per sector)
- Sector-specific threat actors and threat patterns (minimum 20 nodes per sector)
- Sector-specific vulnerabilities beyond general CVEs (minimum 30 nodes per sector)
- Sector-specific regulatory requirements and compliance frameworks (minimum 10 nodes per sector)
- Sector-specific mitigation strategies and best practices (minimum 25 nodes per sector)

**RULE 4.1.3 - Sector Parity Principle**: No sector shall be significantly underrepresented compared to others. If one sector has 200 specific nodes, other sectors should have at least 150 nodes (75% parity minimum).

### 4.2 Shared vs. Sector-Specific Nodes

The ontology architecture must distinguish between nodes that apply across sectors and nodes that are sector-specific.

**RULE 4.2.1 - Shared Node Reusability**: Nodes representing general concepts (attack patterns, CVEs, generic technologies) shall be marked as shared and reused across sectors rather than duplicated for each sector.

**RULE 4.2.2 - Sector-Specific Tagging**: Nodes that are specific to one or more sectors shall be tagged with sector applicability properties. This allows filtering and sector-focused queries.

**RULE 4.2.3 - Cross-Sector Impact Analysis**: When a threat or vulnerability affects multiple sectors, relationships shall explicitly connect the threat to each affected sector with impact severity scoring per sector.

**RULE 4.2.4 - Sector Specialization Relationships**: Shared nodes may have sector-specific specialization nodes. Example: "SCADA System" (shared) has relationships to "Energy SCADA System" (Energy sector) and "Water SCADA System" (Water sector).

### 4.3 Sector Applicability Mapping

**RULE 4.3.1 - Explicit Sector Relationships**: Every CVE node that is relevant to one or more sectors must have explicit relationships to those sector nodes with relationship properties indicating relevance level (Critical, High, Medium, Low).

**RULE 4.3.2 - Sector Coverage Metrics**: Project tracking shall include metrics showing the number of threat intelligence nodes applicable to each sector. Gaps below 100 nodes per sector trigger additional research.

**RULE 4.3.3 - Sector Expert Validation**: For each sector, at least one domain expert must validate that the ontology coverage is comprehensive and accurately represents sector-specific threats and technologies.

**RULE 4.3.4 - Sector Query Support**: The ontology must support efficient queries like "Show me all threats relevant to the Energy Sector" or "What CVEs affect Healthcare but not Financial Services?" Performance target: <2 seconds.

### 4.4 Sector Balance Enforcement

**RULE 4.4.1 - Sector Coverage Dashboard**: A live dashboard shall display node counts, relationship counts, and coverage depth for each of the 16 sectors. Underrepresented sectors are highlighted.

**RULE 4.4.2 - Sector Balance Gates**: Before completing any enhancement wave, sector coverage balance must be verified. No wave is complete if any sector has less than 75% of the average sector coverage.

**RULE 4.4.3 - Sector-Specific Waves**: If sector imbalances emerge, dedicated enhancement waves focused solely on underrepresented sectors shall be scheduled to restore balance.

---

## 5. WAVE COMPLETION CRITERIA

### 5.1 100% Complete Before Next Wave

The enhancement project follows a strict wave-based methodology where each wave must be 100% complete before the next wave begins. This prevents cascade failures and ensures quality at each step.

**RULE 5.1.1 - Wave Completion Definition**: A wave is considered complete when:
- All planned nodes have been created (100% of target)
- All planned relationships have been established (100% of target)
- All sector coverage requirements for the wave are met (100% of sectors covered as planned)
- All validation tests pass (100% pass rate)
- All documentation is complete (no truncation)
- Performance benchmarks meet targets (query times within limits)

**RULE 5.1.2 - No Partial Wave Acceptance**: Partial wave completion (e.g., "We created 90% of the nodes") is not acceptable. Waves are binary: complete or incomplete. Incomplete waves must be finished before progression.

**RULE 5.1.3 - No Wave Skipping**: Waves must be executed in sequence (Wave 1, then Wave 2, then Wave 3, etc.). Skipping waves because they seem less important is forbidden. The wave sequence has dependencies.

**RULE 5.1.4 - No Parallel Wave Execution**: Only one wave may be in active execution at a time. This prevents resource conflicts and ensures focus. Planning for future waves is allowed while a wave executes.

### 5.2 Validation Gates

Each wave must pass through multiple validation gates before being marked complete.

**RULE 5.2.1 - Technical Validation Gate**: Automated tests verify that all nodes and relationships exist, properties are populated correctly, and no data corruption occurred. 100% pass required.

**RULE 5.2.2 - Performance Validation Gate**: Benchmark queries execute within performance targets (specific thresholds defined per wave). Queries slower than baseline require optimization before progression.

**RULE 5.2.3 - Coverage Validation Gate**: Sector coverage analysis confirms that the wave achieved its coverage goals for all 16 sectors. Gaps require remediation before progression.

**RULE 5.2.4 - Integration Validation Gate**: Existing queries, applications, and integrations continue to function correctly (backward compatibility verification). Any breaking changes require fixes before progression.

**RULE 5.2.5 - Documentation Validation Gate**: All documentation deliverables for the wave are complete (no truncation), peer-reviewed, and approved. Incomplete documentation blocks wave completion.

**RULE 5.2.6 - Stakeholder Validation Gate**: Key stakeholders review wave outcomes and provide approval to proceed. Stakeholder concerns must be addressed before progression.

### 5.3 Documentation Standards

Each wave produces mandatory documentation deliverables that must meet completeness standards.

**RULE 5.3.1 - Wave Execution Report**: Each wave shall produce an execution report detailing:
- Node creation summary (types, counts, examples)
- Relationship creation summary (types, counts, examples)
- Sector coverage achieved (metrics per sector)
- Validation test results (all tests documented)
- Performance benchmark results (query times, resource usage)
- Issues encountered and resolutions
- Lessons learned for future waves
- Minimum 5,000 words, complete with no truncation

**RULE 5.3.2 - Wave Validation Report**: Each wave shall produce a validation report certifying:
- All validation gates passed
- Test evidence (screenshots, logs, query results)
- Performance evidence (benchmark data, charts)
- Coverage evidence (sector metrics, node counts)
- Sign-off from technical lead and project manager
- Minimum 3,000 words, complete with no truncation

**RULE 5.3.3 - Wave Knowledge Transfer Document**: Each wave shall produce a knowledge transfer document for future maintainers:
- What was built and why
- Key design decisions and rationale
- Code snippets and query examples
- Troubleshooting guide for common issues
- Recommendations for future enhancements
- Minimum 4,000 words, complete with no truncation

### 5.4 Sign-Off Procedures

**RULE 5.4.1 - Technical Lead Sign-Off**: The technical lead must review all wave deliverables and explicitly sign off that the wave is technically complete and meets all quality standards.

**RULE 5.4.2 - Project Manager Sign-Off**: The project manager must verify that all wave documentation is complete, all validation gates passed, and the wave is ready for production deployment.

**RULE 5.4.3 - Stakeholder Sign-Off**: At least two stakeholder representatives (e.g., threat intelligence analysts, security operations personnel) must review wave outcomes and confirm that deliverables meet operational needs.

**RULE 5.4.4 - Executive Sponsor Sign-Off**: For major waves (Waves 1, 4, 8, 12), the executive sponsor must provide explicit approval based on strategic alignment and business value delivery.

**RULE 5.4.5 - Sign-Off Documentation**: All sign-offs must be documented with signatures (electronic or digital), dates, and any conditions or recommendations for future waves.

### 5.5 Wave Completion Metrics

Each wave completion is tracked with quantitative metrics that must meet minimum thresholds:

**METRIC 5.5.1 - Node Creation Accuracy**: Percentage of planned nodes successfully created. Minimum: 100%.

**METRIC 5.5.2 - Relationship Creation Accuracy**: Percentage of planned relationships successfully created. Minimum: 100%.

**METRIC 5.5.3 - Validation Test Pass Rate**: Percentage of validation tests passed. Minimum: 100%.

**METRIC 5.5.4 - Performance Benchmark Achievement**: Percentage of queries meeting performance targets. Minimum: 95%.

**METRIC 5.5.5 - Sector Coverage Achievement**: Percentage of sector-specific goals met. Minimum: 100% for all 16 sectors.

**METRIC 5.5.6 - Documentation Completeness**: Percentage of documentation deliverables complete with no truncation. Minimum: 100%.

**METRIC 5.5.7 - Stakeholder Satisfaction**: Stakeholder approval rating based on wave outcomes. Minimum: 4.0 out of 5.0.

---

## 6. ENFORCEMENT AND ACCOUNTABILITY

### 6.1 Rule Violation Procedures

**RULE 6.1.1 - Immediate Work Stoppage**: If any team member identifies a violation of these ground rules, they have the authority to immediately halt work until the violation is addressed.

**RULE 6.1.2 - Root Cause Analysis**: Every rule violation triggers a root cause analysis to understand why the violation occurred and how to prevent recurrence.

**RULE 6.1.3 - Corrective Action Plans**: Violations require documented corrective action plans with specific steps, responsible parties, and completion dates.

**RULE 6.1.4 - Violation Tracking**: All rule violations are tracked in a centralized log with severity ratings, resolution status, and lessons learned.

### 6.2 Accountability Framework

**RULE 6.2.1 - Technical Lead Accountability**: The technical lead is ultimately accountable for ensuring that these ground rules are followed in all technical work.

**RULE 6.2.2 - Project Manager Accountability**: The project manager is accountable for ensuring that these ground rules are incorporated into project processes, schedules, and quality gates.

**RULE 6.2.3 - Team Member Responsibility**: Every team member is responsible for understanding these ground rules, following them in their work, and raising concerns when violations are observed.

**RULE 6.2.4 - Executive Oversight**: The executive sponsor shall receive monthly reports on ground rule compliance, violations, and corrective actions.

### 6.3 Continuous Improvement

**RULE 6.3.1 - Ground Rule Evolution**: These ground rules may be updated based on lessons learned, but only through a formal change control process requiring executive approval.

**RULE 6.3.2 - Quarterly Ground Rule Review**: Every quarter, the project team shall review these ground rules for relevance, clarity, and effectiveness. Recommended updates go through change control.

**RULE 6.3.3 - Lessons Learned Integration**: Insights from wave execution, validation findings, and stakeholder feedback shall be incorporated into ground rule refinements where appropriate.

---

## 7. SUMMARY AND COMMITMENT

These ground rules establish the foundation for safe, effective, and value-preserving enhancement of the AEON Digital Twin Cybersecurity Threat Intelligence ontology. They are designed to protect the existing investment of 147,923 CVE nodes while enabling systematic growth to 307,569+ nodes across 12 enhancement waves.

**Every team member commits to:**
- Protecting the 147,923 CVE nodes as sacred and immutable
- Following the enhancement-only philosophy (no deletions)
- Producing complete documentation with no truncation
- Ensuring comprehensive multi-sector coverage
- Completing each wave 100% before moving to the next

**Project leadership commits to:**
- Enforcing these ground rules without exception
- Providing resources and support for compliance
- Addressing violations swiftly and transparently
- Continuously improving these rules based on experience

**Success is defined as:** Delivering a 307,569+ node ontology that preserves all existing value, adds comprehensive multi-sector coverage, maintains high performance, and serves as the foundation for advanced threat intelligence capabilities across all 16 critical infrastructure sectors.

---

**DOCUMENT END - 00_MANDATORY_GROUND_RULES.md**

**Word Count:** ~3,800 words (exceeds 3,000-word minimum)
**Completeness:** 100% - No truncation, no omissions, all sections fully detailed
**Status:** ACTIVE - Ready for immediate use in project governance
