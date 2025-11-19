# Threat Modeling Methodologies
## Framework Comparison and Selection Guide

**Version:** 1.0 - October 2025
**Focus:** Comprehensive comparison of threat modeling methodologies
**Audience:** Security professionals selecting appropriate frameworks

---

## Breadcrumb Navigation
[Home](../../index.md) > [Threat Modeling](../index.md) > Methodologies

---

## Table of Contents

### Methodology Frameworks
- [[./stride/index|STRIDE Framework]] - Microsoft's six-category threat model
- [[./pasta/index|PASTA Framework]] - Risk-centric threat modeling
- [[./octave/index|OCTAVE Framework]] - Organizational threat modeling
- [[./trike/index|Trike Methodology]] - Requirements-driven threat modeling
- [[./vast/index|VAST Methodology]] - Visual, Agile, Simple threat modeling

### Advanced Integration
- [[./mitre-integration|MITRE ATT&CK Integration]] - Threat actor tactics mapping
- [[./automation|Automation & Integration]] - n8n workflow integration

### Selection & Comparison
- [[./comparison|Methodology Comparison Matrix]] - Detailed framework analysis
- [[./selection-guide|Selection Guide]] - Choosing the right methodology

---

## Methodology Overview

Threat modeling methodologies provide structured approaches to identifying, analyzing, and mitigating security threats. Each framework has unique strengths and is suited for different contexts, team compositions, and organizational requirements.

### Framework Categories

#### **Property-Based Frameworks**
Focus on security properties that must be maintained:
- **STRIDE:** Microsoft's six security properties
- **PASTA:** Business-aligned security properties

#### **Risk-Based Frameworks**
Focus on business risk and organizational impact:
- **OCTAVE:** Organizational risk assessment
- **Trike:** Requirements-driven risk analysis

#### **Agile Frameworks**
Designed for fast-paced development environments:
- **VAST:** Visual, Agile, Simple threat modeling

---

## Methodology Comparison Matrix

### Overview Comparison

| Methodology | Primary Focus | Best For | Complexity | Time Investment | Team Skills Required | Output Format |
|-------------|---------------|----------|------------|-----------------|---------------------|---------------|
| **STRIDE** | Security Properties | Application Security | Low | 2-4 hours | Basic Security Knowledge | Threat Lists |
| **PASTA** | Business Risk | Enterprise Applications | High | 1-2 weeks | Advanced Security + Business | Risk Assessments |
| **OCTAVE** | Organizational Risk | Enterprise-wide | Medium | 2-4 weeks | Mixed Technical/Business | Security Strategy |
| **Trike** | Requirements-driven | Compliance-heavy Systems | High | 1-3 weeks | Security Architects | Requirements Traceability |
| **VAST** | Agile Development | Fast-paced Teams | Low | 1-2 hours per sprint | Development Teams | Actionable Backlog Items |

### Detailed Feature Comparison

#### Threat Identification Approach
| Methodology | Threat Categories | Actor Analysis | Attack Vectors | Prerequisites | Examples Provided |
|-------------|------------------|---------------|---------------|---------------|-------------------|
| **STRIDE** | 6 Categories (Spoofing, Tampering, etc.) | Basic | Limited | Basic | Extensive |
| **PASTA** | Business Impact-based | Comprehensive | Detailed | Comprehensive | Scenario-based |
| **OCTAVE** | Asset-based | Organizational | Infrastructure-focused | Environmental | Case-based |
| **Trike** | Requirements Violation | Capability-based | Trust Boundary | Detailed | Technical |
| **VAST** | Feature-based | Sprint Context | User Story-driven | Minimal | Practical |

#### Risk Assessment Methodology
| Methodology | Risk Calculation | Quantitative | Qualitative | Business Impact | Prioritization |
|-------------|-----------------|--------------|-------------|----------------|---------------|
| **STRIDE** | Impact × Likelihood | Basic Scoring | Category-based | Limited | Manual |
| **PASTA** | Multi-factor Analysis | Advanced Metrics | Business-aligned | Comprehensive | Automated |
| **OCTAVE** | Asset Value × Threat Impact | Moderate | Organizational | High | Criteria-based |
| **Trike** | Attacker Capability × Requirements Weight | Advanced | Requirements-driven | Medium | Mathematical |
| **VAST** | Sprint Impact × Implementation Cost | Simple | Team Consensus | Sprint-focused | Story Points |

#### Mitigation Strategy Approach
| Methodology | Control Types | Implementation Guidance | Validation | Maintenance | Automation Potential |
|-------------|---------------|----------------------|------------|-------------|---------------------|
| **STRIDE** | Security Controls | Basic | Manual Review | Limited | Low |
| **PASTA** | Risk-based Controls | Detailed | Testing Required | Moderate | High |
| **OCTAVE** | Strategic Controls | Comprehensive | Audit-based | High | Medium |
| **Trike** | Requirements Controls | Technical | Formal Verification | High | High |
| **VAST** | Sprint Controls | Agile | Demo-based | Continuous | Very High |

---

## Methodology Selection Guide

### Choose STRIDE When:
- Building traditional web applications
- Team has basic security knowledge
- Need quick threat identification
- Working with well-understood technologies
- Compliance requirements are minimal

### Choose PASTA When:
- Business risk is the primary concern
- Large enterprise applications
- Complex regulatory environments
- Need detailed risk quantification
- Executive stakeholder involvement required

### Choose OCTAVE When:
- Organization-wide security assessment needed
- Mixed technical and business teams
- Long-term security strategy development
- Limited security expertise available
- Focus on operational risk management

### Choose Trike When:
- Security requirements drive architecture
- Formal verification required
- Compliance-heavy environments
- Academic or research contexts
- Mathematical risk analysis needed

### Choose VAST When:
- Agile development environment
- 2-week sprint cycles
- Development team drives security
- Continuous integration required
- Rapid feature development

---

## Hybrid Approach Recommendations

### Enterprise Agile Development
```
Primary: VAST (for sprint-level modeling)
Secondary: PASTA (for release planning)
Tertiary: STRIDE (for detailed component analysis)
```

### Compliance-Driven Development
```
Primary: Trike (for requirements traceability)
Secondary: OCTAVE (for organizational compliance)
Tertiary: PASTA (for risk quantification)
```

### Cloud-Native Applications
```
Primary: STRIDE (for component security)
Secondary: VAST (for agile delivery)
Tertiary: PASTA (for business risk)
```

### Industrial Control Systems
```
Primary: OCTAVE (for operational risk)
Secondary: PASTA (for business impact)
Tertiary: STRIDE (for technical threats)
```

---

## Implementation Considerations

### Team Readiness Assessment
- **Security Expertise:** Available security knowledge and experience
- **Business Acumen:** Understanding of business impact and risk tolerance
- **Technical Skills:** Development and infrastructure knowledge
- **Process Maturity:** Existing security processes and procedures

### Organizational Factors
- **Industry Requirements:** Regulatory compliance needs
- **System Complexity:** Architecture complexity and scale
- **Development Methodology:** Agile, waterfall, or hybrid approaches
- **Resource Availability:** Time, budget, and personnel constraints

### Success Factors
- **Executive Support:** Leadership commitment to security
- **Cross-Functional Teams:** Collaboration between security, development, and operations
- **Training Investment:** Ongoing education and skill development
- **Tool Integration:** Automation and workflow integration

---

## Navigation

| Previous | Current | Next |
|----------|---------|------|
| [[../core-concepts|Core Concepts]] | Methodologies | [[./stride/index|STRIDE Framework]] |

## See Also

### Related Topics
- [[../core-concepts|Core Concepts]] - Threat modeling fundamentals
- [[../workshops/index|Workshops]] - Hands-on training
- [[../resources/tools|Tools & Software]] - Implementation tools

### Integration Areas
- [[../methodologies/automation|Automation Integration]] - n8n workflow integration
- [[../methodologies/mitre-integration|MITRE ATT&CK]] - Threat actor mapping
- [[Cybersecurity/Risk Assessment ICS]] - Risk assessment methodologies

---

**Tags:** #threat-modeling #methodologies #framework-comparison #security-methodologies

**Last Updated:** October 2025
**Version:** 1.0
**Reading Time:** 20 minutes
**Difficulty:** Intermediate