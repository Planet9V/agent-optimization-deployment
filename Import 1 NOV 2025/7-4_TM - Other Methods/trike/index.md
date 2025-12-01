# Trike Threat Modeling Methodology
## Requirements-Driven, Risk-Based Security Analysis Framework

**Version:** 1.0 - October 2025
**Focus:** Requirements-first approach to threat modeling with quantitative risk analysis
**Audience:** Security architects, requirements engineers, and compliance teams

---

## Breadcrumb Navigation
[Home](../../../../index.md) > [Threat Modeling](../../../index.md) > [Methodologies](../../index.md) > Trike

---

## Table of Contents

### Framework Overview
- [[./phases|Trike Phases]] - Detailed methodology breakdown
- [[./requirements|Requirements Analysis]] - Security requirements framework
- [[./implementation|Implementation Guide]] - Code examples and automation

### Practical Application
- [[./template|Trike Template]] - Ready-to-use requirements-driven template
- [[./risk-calculation|Risk Calculation]] - Quantitative risk assessment methodology
- [[./case-studies|Case Studies]] - Requirements-driven threat modeling examples

---

## 🎯 What is Trike?

Trike is a threat modeling methodology that takes a requirements-driven approach to security analysis. Unlike methodologies that begin with system decomposition, Trike starts with security requirements and systematically identifies threats that violate those requirements. It uses quantitative risk assessment based on attacker capabilities and provides structured traceability from requirements to implemented controls.

### Framework Origins
- **Developed by:** Security researchers at the University of Tulsa
- **First introduced:** 2006 as an academic research project
- **Purpose:** Provide requirements traceability in threat modeling
- **Adoption:** Used in high-assurance systems and regulated environments

### Core Philosophy
Trike emphasizes that security is a requirement that must be satisfied, not an afterthought. By starting with requirements, Trike ensures that threat modeling directly supports the security needs of the system rather than producing generic threat lists.

---

## Trike Core Principles

### 1. Requirements-First Approach
Security requirements drive the entire threat modeling process, ensuring that all analysis is relevant to actual security needs.

### 2. Trust Boundary Focus
Trike emphasizes trust relationships between system components, recognizing that security violations occur at trust boundaries.

### 3. Quantitative Risk Assessment
Trike uses mathematical calculations to determine risk levels based on attacker capabilities, motives, and opportunities.

### 4. Requirements Traceability
Every threat, mitigation, and control can be traced back to specific security requirements.

---

## Trike Methodology Overview

### Phase 1: Requirements Definition
**Establish security requirements and success criteria**

- Define security requirements using standard categories
- Establish requirement priorities and dependencies
- Create requirement traceability matrices
- Validate requirements against business objectives

### Phase 2: System Modeling
**Create trust boundary models and component relationships**

- Identify system components and trust boundaries
- Map trust relationships between components
- Define component capabilities and privileges
- Document data flows across trust boundaries

### Phase 3: Threat Identification
**Identify threats that violate security requirements**

- Analyze each trust boundary for requirement violations
- Assess attacker capabilities and motivations
- Calculate quantitative risk scores
- Prioritize threats based on risk calculations

### Phase 4: Mitigation Design
**Design controls that satisfy security requirements**

- Develop mitigations for identified threats
- Ensure mitigation traceability to requirements
- Validate control effectiveness
- Document implementation dependencies

---

## Trike Risk Calculation

### Risk Formula
```
Risk Score = (Attacker Skill × Attacker Motive × Attacker Opportunity) ÷ (Control Strength × Implementation Quality)
```

### Attacker Factors
- **Skill Level:** Technical expertise required (Novice to Multiple Experts)
- **Motivation:** Incentive to attack (None to Extreme)
- **Opportunity:** Access and conditions available (None to Extreme)

### Control Factors
- **Strength:** Effectiveness of implemented controls (None to Complete)
- **Implementation Quality:** How well controls are deployed (Poor to Excellent)

---

## When to Use Trike

### Ideal Use Cases
- **High-Assurance Systems:** Safety-critical or high-security applications
- **Regulated Environments:** Systems requiring formal security validation
- **Requirements-Driven Development:** Organizations using requirements traceability
- **Compliance-Heavy Projects:** Systems needing detailed security documentation
- **Academic/Research Contexts:** Formal security analysis requirements

### Best Suited For
- **Requirements engineers** familiar with formal requirements processes
- **High-assurance environments** requiring mathematical risk analysis
- **Regulated industries** needing detailed security documentation
- **Complex systems** with multiple trust boundaries
- **Academic research** requiring formal threat modeling approaches

### Not Recommended For
- **Agile development** with rapidly changing requirements
- **Small applications** with simple architectures
- **Resource-constrained** environments
- **Quick assessments** needing fast results
- **Non-technical stakeholders** making security decisions

---

## Trike vs. Other Methodologies

### Comparison with STRIDE
- **Trike:** Requirements-driven with quantitative risk analysis
- **STRIDE:** Technical threat categories, qualitative analysis
- **Best Together:** Trike for requirements validation, STRIDE for technical analysis

### Comparison with PASTA
- **Trike:** Mathematical risk calculations, requirements traceability
- **PASTA:** Business risk focus, comprehensive analysis
- **Best Together:** Trike for technical requirements, PASTA for business risk

### Integration with Formal Methods
- **Requirements traceability** supports formal verification
- **Mathematical risk analysis** enables quantitative assessment
- **Structured approach** facilitates automated analysis

---

## Implementation Considerations

### Requirements Engineering
- **Requirements Definition:** Clear, measurable security requirements
- **Requirements Validation:** Stakeholder agreement on requirements
- **Requirements Management:** Version control and change management
- **Requirements Traceability:** Links between requirements, threats, and controls

### Risk Analysis Skills
- **Mathematical Modeling:** Quantitative risk calculation capabilities
- **Attacker Profiling:** Detailed attacker capability assessment
- **Control Analysis:** Security control effectiveness evaluation
- **Requirements Mapping:** Linking controls to requirements

### Tool Support
- **Requirements Management:** Tools for requirements traceability
- **Risk Calculation:** Spreadsheets or specialized risk tools
- **Modeling Tools:** Diagramming tools for trust boundaries
- **Documentation:** Structured documentation templates

---

## Navigation

| Previous | Current | Next |
|----------|---------|------|
| [[../octave/index|OCTAVE Framework]] | Trike Methodology | [[./phases|Trike Phases]] |

## See Also

### Related Topics
- [[../stride/index|STRIDE Framework]] - Technical threat identification
- [[../pasta/index|PASTA Framework]] - Risk-centric threat modeling
- [[../../../compliance|Compliance Frameworks]] - Regulatory requirements

### Implementation Resources
- [[./template|Trike Template]] - Requirements-driven template
- [[./requirements|Requirements Analysis]] - Security requirements framework
- [[../../../workflows/examples/compliance-monitoring|Compliance Workflows]] - Integration examples

---

**Tags:** #trike #threat-modeling #requirements-driven #quantitative-risk #formal-methods #security-requirements

**Last Updated:** October 2025
**Version:** 1.0
**Reading Time:** 15 minutes
**Difficulty:** Advanced