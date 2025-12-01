# PASTA Threat Modeling Framework
## Process for Attack Simulation and Threat Analysis - Risk-Centric Methodology

**Version:** 1.0 - October 2025
**Focus:** Business-aligned risk-centric threat modeling with 8-phase methodology
**Audience:** Enterprise security teams, risk managers, and compliance officers

---

## Breadcrumb Navigation
[Home](../../../../index.md) > [Threat Modeling](../../../index.md) > [Methodologies](../../index.md) > PASTA

---

## Table of Contents

### Framework Overview
- [[./phases|PASTA Phases]] - Detailed 8-phase methodology explanation
- [[./implementation|Implementation Guide]] - Code examples and automation
- [[./case-studies|Case Studies]] - Enterprise applications and scenarios

### Practical Application
- [[./template|PASTA Template]] - Ready-to-use threat modeling template
- [[./risk-analysis|Risk Analysis Framework]] - Quantitative risk assessment
- [[./business-alignment|Business Alignment]] - Linking security to business objectives

---

## 🎯 What is PASTA?

PASTA (Process for Attack Simulation and Threat Analysis) is a risk-centric threat modeling framework that focuses on business impact and aligns security activities with business objectives. Unlike technology-focused frameworks, PASTA starts with business context and works backward to identify technical threats.

### Framework Origins
- **Developed by:** Tony UcedaVelez, Marco M. Morana, and Rafael A. Jerusalemy
- **First introduced:** 2012 as a comprehensive threat modeling approach
- **Purpose:** Bridge the gap between business risk and technical security
- **Adoption:** Widely used in enterprise environments and regulated industries

### Core Philosophy
PASTA recognizes that security is a business problem, not just a technical one. It ensures that threat modeling activities directly support business objectives and risk management strategies.

---

## The Eight PASTA Phases

### Phase 1: Define Business Objectives
**Establish the business context and security requirements**

- Define business objectives and success criteria
- Identify compliance requirements and regulatory constraints
- Determine risk tolerance and security priorities
- Establish stakeholder expectations and success metrics

### Phase 2: Define Technical Scope
**Determine the technical boundaries and constraints**

- Identify system components and architecture
- Define trust boundaries and security domains
- Establish technical constraints and limitations
- Document assumptions and out-of-scope elements

### Phase 3: Application Decomposition
**Break down the application into analyzable components**

- Identify entry and exit points
- Map data flows and trust levels
- Define privilege levels and access controls
- Document component interactions and dependencies

### Phase 4: Threat Analysis
**Identify potential threat actors and their motivations**

- Analyze threat actor capabilities and resources
- Determine attack motivations and goals
- Assess threat actor sophistication levels
- Map threats to business impact scenarios

### Phase 5: Vulnerability Analysis
**Discover weaknesses that threats can exploit**

- Identify technical vulnerabilities
- Assess configuration weaknesses
- Evaluate process and procedural gaps
- Determine vulnerability exploitability

### Phase 6: Attack Modeling
**Simulate attack scenarios and exploitation paths**

- Develop attack trees and scenarios
- Model attack progression and lateral movement
- Assess attack success probabilities
- Identify critical attack paths

### Phase 7: Risk Analysis
**Quantify risks and assess business impact**

- Calculate risk scores using multiple factors
- Assess likelihood and impact combinations
- Prioritize risks based on business impact
- Generate risk mitigation recommendations

### Phase 8: Residual Risk Analysis
**Evaluate remaining risk after mitigations**

- Assess effectiveness of proposed controls
- Calculate residual risk levels
- Determine risk acceptance criteria
- Develop ongoing monitoring strategies

---

## PASTA Risk Factors

### Likelihood Assessment
- **Very Low (1):** Requires nation-state resources or zero-day exploits
- **Low (2):** Requires advanced technical skills or specific conditions
- **Medium (3):** Requires moderate technical skills, commonly available
- **High (4):** Requires basic technical skills, widely available tools
- **Very High (5):** Requires minimal technical skills, automated tools available

### Impact Assessment
- **Very Low (1):** Minimal business impact, easily contained
- **Low (2):** Limited impact to specific users or functions
- **Medium (3):** Significant impact to operations or revenue
- **High (4):** Major impact to business continuity or reputation
- **Very High (5):** Existential threat to business survival

### Exploitability Factors
- **Technical Complexity:** Required attacker skill level
- **Resource Requirements:** Tools, time, and access needed
- **Detection Risk:** Likelihood of detection during attack
- **Remediation Time:** Time required to implement fixes

---

## When to Use PASTA

### Ideal Use Cases
- **Enterprise Applications:** Large-scale business systems
- **Regulated Industries:** Healthcare, finance, critical infrastructure
- **Business-Critical Systems:** High-impact applications
- **Compliance-Driven Projects:** SOX, HIPAA, PCI-DSS requirements
- **Risk Management Integration:** Enterprise risk management frameworks

### Best Suited For
- **Large organizations** with complex risk management needs
- **Regulated environments** requiring detailed risk assessments
- **Business stakeholders** involved in security decisions
- **Long-term security strategy** development
- **Quantitative risk analysis** requirements

### Not Recommended For
- **Small applications** with simple architectures
- **Agile development** with 2-week sprint cycles
- **Resource-constrained** environments
- **Quick threat identification** needs

---

## PASTA vs. Other Methodologies

### Comparison with STRIDE
- **PASTA:** Business risk focus, comprehensive analysis
- **STRIDE:** Technical threat focus, quick analysis
- **Best Together:** PASTA for strategic analysis, STRIDE for tactical implementation

### Comparison with OCTAVE
- **PASTA:** Technical implementation with business alignment
- **OCTAVE:** Organizational risk management focus
- **Best Together:** PASTA for application security, OCTAVE for enterprise risk

### Integration with MITRE ATT&CK
- **PASTA Threat Analysis** maps to ATT&CK tactics and techniques
- **Risk-based prioritization** aligns with ATT&CK-based threat hunting
- **Business impact assessment** supports ATT&CK-informed defense

---

## Implementation Considerations

### Team Requirements
- **Security Architects:** Technical threat modeling expertise
- **Risk Managers:** Business impact assessment skills
- **Business Stakeholders:** Domain knowledge and risk tolerance
- **Compliance Officers:** Regulatory requirement understanding

### Resource Requirements
- **Time Investment:** 1-3 weeks per major application
- **Documentation:** Comprehensive artifacts and evidence
- **Tool Support:** Risk analysis and modeling tools
- **Training:** Specialized PASTA methodology training

### Success Factors
- **Executive Support:** Leadership commitment to risk-based security
- **Cross-Functional Teams:** Collaboration between business and technical teams
- **Process Integration:** Incorporation into SDLC and risk management
- **Measurement:** Clear metrics for success and effectiveness

---

## Navigation

| Previous | Current | Next |
|----------|---------|------|
| [[../stride/index|STRIDE Framework]] | PASTA Framework | [[./phases|PASTA Phases]] |

## See Also

### Related Topics
- [[../stride/index|STRIDE Framework]] - Technical threat identification
- [[../octave/index|OCTAVE Framework]] - Organizational risk assessment
- [[../../../risk-assessment-ics|ICS Risk Assessment]] - Industrial risk methodologies

### Implementation Resources
- [[./template|PASTA Template]] - Ready-to-use template
- [[./implementation|Implementation Guide]] - Code examples and automation
- [[../../../workflows/examples/compliance-monitoring|Compliance Workflows]] - Integration examples

---

**Tags:** #pasta #threat-modeling #risk-centric #business-alignment #enterprise-security #compliance

**Last Updated:** October 2025
**Version:** 1.0
**Reading Time:** 15 minutes
**Difficulty:** Intermediate to Advanced