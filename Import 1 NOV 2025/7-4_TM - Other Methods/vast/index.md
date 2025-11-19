# VAST Threat Modeling Methodology
## Visual, Agile, and Simple Threat Modeling for Fast-Paced Development

**Version:** 1.0 - October 2025
**Focus:** Agile threat modeling with visual diagrams and iterative refinement
**Audience:** Development teams, agile practitioners, and fast-moving organizations

---

## Breadcrumb Navigation
[Home](../../../../index.md) > [Threat Modeling](../../../index.md) > [Methodologies](../../index.md) > VAST

---

## Table of Contents

### Framework Overview
- [[./phases|VAST Phases]] - Four-phase agile methodology
- [[./visual-diagrams|Visual Diagrams]] - Diagram types and usage
- [[./implementation|Implementation Guide]] - Code examples and automation

### Practical Application
- [[./template|VAST Template]] - Ready-to-use agile template
- [[./sprint-integration|Sprint Integration]] - Agile development integration
- [[./case-studies|Case Studies]] - Agile team implementations

---

## 🎯 What is VAST?

VAST (Visual, Agile, and Simple Threat Modeling) is a threat modeling methodology specifically designed for agile development environments. It emphasizes visual representations, iterative refinement, and simplicity to enable fast-paced teams to identify and address security threats without slowing down development velocity.

### Framework Origins
- **Developed by:** Security practitioners for agile environments
- **First introduced:** As a response to traditional threat modeling being too slow for agile
- **Purpose:** Enable security analysis in fast-paced development cycles
- **Adoption:** Widely used in agile teams and DevOps environments

### Core Philosophy
VAST recognizes that security analysis must keep pace with development speed. Rather than comprehensive analysis, VAST focuses on identifying the most important threats quickly and iteratively refining the security posture as the system evolves.

---

## VAST Core Principles

### 1. Visual Approach
**Diagrams and visual representations over text-heavy documentation**

- Simple, intuitive diagrams that anyone can understand
- Visual threat identification and communication
- Quick diagram creation and modification
- Stakeholder-friendly representations

### 2. Agile Integration
**Iterative and incremental security analysis**

- Sprint-based threat modeling activities
- Continuous refinement as features evolve
- Just-enough analysis for current needs
- Integration with agile ceremonies and artifacts

### 3. Simplicity First
**Focus on essential threats and practical mitigations**

- Identify most important threats quickly
- Avoid analysis paralysis with over-complication
- Practical, implementable security recommendations
- Minimal documentation overhead

### 4. Speed and Efficiency
**Fast threat identification and mitigation planning**

- 1-2 hour analysis sessions per sprint
- Immediate actionable results
- Quick iteration on security decisions
- Minimal disruption to development flow

---

## The Four VAST Phases

### Phase 1: Asset Identification
**Quickly identify critical assets in scope**

- Focus on sprint backlog items and user stories
- Identify data, systems, and processes at risk
- Determine asset criticality and business value
- Create initial visual asset map

### Phase 2: Threat Identification
**Rapid threat identification using visual techniques**

- Apply simplified threat categories to assets
- Use visual diagrams to identify attack vectors
- Focus on most likely and impactful threats
- Document threats with simple visual notation

### Phase 3: Mitigation Planning
**Develop practical mitigation strategies**

- Identify existing security controls
- Design simple, effective mitigations
- Prioritize based on implementation effort vs. risk reduction
- Create actionable backlog items for development team

### Phase 4: Validation
**Quick validation and iteration planning**

- Validate threat model against current sprint goals
- Identify gaps and areas needing more analysis
- Plan for next iteration's threat modeling activities
- Document lessons learned for continuous improvement

---

## VAST Visual Diagrams

### Asset Map
**Simple diagram showing system components and data flows**

```
[User] → [Web App] → [API] → [Database]
                    ↓
               [Auth Service]
```

### Threat Overlay
**Visual representation of threats against assets**

```
[User] → [Web App] → [API] → [Database]
   ⚠️      🔓       🚫       💀
Spoofing  Injection  Auth Bypass  Data Breach
```

### Mitigation Map
**Security controls and their coverage**

```
[User] → [WAF] → [Web App] → [API] → [Database]
                    ↓           ↓
               [Auth Service] [Encryption]
```

---

## When to Use VAST

### Ideal Use Cases
- **Agile Development Teams:** 2-week sprint cycles with continuous delivery
- **DevOps Environments:** Fast deployment pipelines requiring quick security analysis
- **Startup Development:** Rapid prototyping and feature development
- **Feature Development:** New feature security analysis before implementation
- **Sprint Planning:** Security considerations in sprint planning meetings

### Best Suited For
- **Development teams** with security awareness but limited security expertise
- **Fast-paced environments** where comprehensive analysis slows delivery
- **Iterative development** with frequent changes and updates
- **Cross-functional teams** including developers, product owners, and security
- **Continuous integration** environments with automated security testing

### Not Recommended For
- **High-assurance systems** requiring formal security verification
- **Regulated environments** needing detailed security documentation
- **Large enterprise systems** with complex architectures
- **Safety-critical systems** requiring exhaustive analysis
- **Academic research** requiring formal mathematical approaches

---

## VAST vs. Other Methodologies

### Comparison with STRIDE
- **VAST:** Visual, agile approach with simplified analysis
- **STRIDE:** Comprehensive technical threat categorization
- **Best Together:** VAST for sprint-level analysis, STRIDE for detailed component analysis

### Comparison with PASTA
- **VAST:** Quick, visual analysis for agile teams
- **PASTA:** Comprehensive business risk analysis
- **Best Together:** VAST for development speed, PASTA for strategic planning

### Integration with Agile
- **Sprint Planning:** Threat modeling during backlog refinement
- **Daily Standups:** Quick security check-ins
- **Sprint Reviews:** Security validation of delivered features
- **Retrospectives:** Continuous security process improvement

---

## Implementation Considerations

### Team Integration
- **Cross-Functional Teams:** Include developers, QA, product owners, and security
- **Security Champions:** Train team members as security advocates
- **Agile Coaches:** Integrate security into agile coaching
- **DevSecOps Culture:** Embed security in development culture

### Tool Support
- **Visual Tools:** Simple diagramming tools (draw.io, Lucidchart)
- **Collaboration Platforms:** Shared whiteboards and digital sticky notes
- **Agile Tools:** Integration with Jira, Azure DevOps, and similar platforms
- **Documentation:** Lightweight wiki or shared document systems

### Success Factors
- **Executive Support:** Leadership commitment to security in agile
- **Training Investment:** Regular security awareness training for teams
- **Process Integration:** Security as part of definition of done
- **Measurement:** Track security metrics alongside agile metrics

---

## Navigation

| Previous | Current | Next |
|----------|---------|------|
| [[../trike/index|Trike Methodology]] | VAST Methodology | [[./phases|VAST Phases]] |

## See Also

### Related Topics
- [[../stride/index|STRIDE Framework]] - Technical threat identification
- [[../pasta/index|PASTA Framework]] - Risk-centric threat modeling
- [[../../../agile-security|Agile Security Practices]] - Security in agile environments

### Implementation Resources
- [[./template|VAST Template]] - Agile threat modeling template
- [[./sprint-integration|Sprint Integration]] - Agile development integration
- [[../../../workflows/examples/devsecops|DevSecOps Workflows]] - Automation examples

---

**Tags:** #vast #agile-threat-modeling #visual-diagrams #sprint-security #devsecops #fast-development

**Last Updated:** October 2025
**Version:** 1.0
**Reading Time:** 15 minutes
**Difficulty:** Intermediate