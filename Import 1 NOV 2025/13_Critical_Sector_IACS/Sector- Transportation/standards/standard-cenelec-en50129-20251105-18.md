---
title: "CENELEC EN 50129 - Safety-Related Electronic Systems for Signaling"
category: "standards"
sector: "transportation"
domain: "rail-safety"
standard_type: "functional-safety"
issuing_organization: "CENELEC"
current_version: "EN 50129:2018"
safety_critical: true
related_standards:
  - "EN 50126"
  - "EN 50128"
  - "IEC 61508"
  - "EN 50159"
revision: "1.0"
date: "2025-11-05"
author: "Transportation Standards Team"
keywords:
  - functional-safety
  - SIL
  - safety-integrity-level
  - electronic-systems
  - signaling-safety
  - fail-safe
---

# CENELEC EN 50129 - Railway Applications: Safety-Related Electronic Systems for Signaling

## Standard Overview and Scope

CENELEC EN 50129 is the definitive European standard specifying requirements for the development, manufacture, and validation of safety-related electronic systems used in railway signaling and train control applications. The standard establishes rigorous safety integrity requirements ensuring that electronic signaling systems operate safely throughout their lifecycle, from concept through decommissioning.

EN 50129 addresses the critical challenge of using complex electronic and programmable systems in railway safety applications where human lives depend on correct operation. The standard defines requirements for achieving Safety Integrity Levels (SIL) ranging from SIL 1 (lowest) to SIL 4 (highest), with SIL 4 representing the most stringent safety requirements applied to train control systems where failure could result in catastrophic accidents.

### Current Version
**EN 50129:2018** - Railway applications — Communication, signalling and processing systems — Safety related electronic systems for signalling

**Supersedes:** EN 50129:2003 (first edition consolidated from prEN 50129 series)

**Effective Date:** December 2018 with transition period through 2020

### Scope of Application

EN 50129 applies to all safety-related electronic systems in railway signaling including:

**Train Control and Protection:**
- ETCS (European Train Control System) onboard and trackside equipment
- CBTC (Communications-Based Train Control) systems
- ATP (Automatic Train Protection) systems
- ATO (Automatic Train Operation) systems (safety-related functions only)
- PTC (Positive Train Control) systems

**Signaling Infrastructure:**
- Electronic interlocking systems (computer-based interlocking)
- Radio Block Centres (RBC) for ETCS Level 2/3
- Trackside control systems and object controllers
- Level crossing protection systems
- Train detection systems (electronic axle counters, track circuits)

**Control Center Systems:**
- Traffic Management Systems (TMS) with safety functions
- Operations control systems with route setting authority
- Automatic Train Supervision (ATS) systems with safety-critical functions

**Communication Systems:**
- GSM-R communication systems (safety-related aspects)
- Safety-related communication protocols and interfaces (per EN 50159)
- Vital data transmission systems

**Field Equipment Controllers:**
- Signal controllers and drivers
- Point machine controllers with safety logic
- Electronic relay rooms and equipment rooms

### Relationship to Safety Standards Family

EN 50129 is part of the integrated CENELEC railway safety standards suite:

**EN 50126 (RAMS):** Overall RAMS lifecycle management and requirements allocation
**EN 50128 (Software):** Software development and validation for safety-related systems (software component of EN 50129 systems)
**EN 50129 (Electronic Systems):** Hardware and system-level safety requirements (this standard)
**EN 50159 (Communication):** Safety-related communication in transmission systems (data communication safety)

EN 50129 also builds upon the generic functional safety standard:
**IEC 61508:** Functional safety of E/E/PE safety-related systems (EN 50129 is railway-specific application of IEC 61508 principles)

## Key Requirements Summary

### Safety Integrity Levels (SIL)

EN 50129 defines four Safety Integrity Levels, each corresponding to a tolerable hazard rate:

**SIL 4 - Catastrophic:** THR < 10⁻⁹ hazardous failures per hour
- **Application:** Train control preventing collisions, SPAD (Signal Passed At Danger), derailments
- **Examples:** ETCS Vital Computer, Interlocking safety logic, ATP braking systems
- **Risk Category:** Multiple fatalities or major environmental damage

**SIL 3 - Critical:** THR 10⁻⁹ to 10⁻⁸ hazardous failures per hour
- **Application:** Secondary protection systems, level crossing controls, platform screen doors
- **Examples:** Level crossing obstacle detection, platform edge protection
- **Risk Category:** Single or few fatalities

**SIL 2 - Marginal:** THR 10⁻⁸ to 10⁻⁷ hazardous failures per hour
- **Application:** Systems with immediate backup protection, non-critical safety functions
- **Examples:** Train detection with multiple independent systems, redundant sensors
- **Risk Category:** Major injuries, no fatalities expected

**SIL 1 - Negligible:** THR 10⁻⁷ to 10⁻⁶ hazardous failures per hour
- **Application:** Low-criticality safety functions with human supervision as backup
- **Examples:** Advisory systems monitored by operators, low-risk shunting controls
- **Risk Category:** Minor injuries only

**SIL 0 - Non-Safety-Related:** No SIL requirement
- **Application:** Non-safety functions (passenger information, comfort, efficiency)
- **Examples:** Passenger displays, HVAC controls, energy optimization

### Safety Principles and Techniques

**Fail-Safe Principles:**
EN 50129 requires all safety-critical systems default to safe state on failure:

- **De-energize to Safe:** Signal relays fail to "danger" aspect when power lost
- **Restrictive Default:** Interlocking defaults to no routes permitted on failure
- **Brake Application:** Train control applies emergency brake on system failure
- **Monitored Fail-Safe:** Continuous monitoring ensures fail-safe behavior maintained

**Architectural Safety Techniques:**

**1. Redundancy:**
- **Dual/Triple Modular Redundancy (2oo2, 2oo3):** Multiple independent channels with voting
- **Hot Standby:** Redundant system ready for immediate takeover
- **Diverse Redundancy:** Different technologies or designs for same function (defense against common mode failures)

**2. Diverse Monitoring:**
- Independent monitoring channel using different technology than main channel
- Example: Watchdog processor monitoring main CPU using different architecture
- Cross-checking between diverse channels

**3. Defensive Programming:**
- Software techniques detecting and recovering from errors (see EN 50128 for details)
- Input validation, range checking, plausibility checks
- Temporal and logical monitoring

**4. Fail-Safe Hardware:**
- Components selected for predictable failure modes
- Failure Mode, Effects and Criticality Analysis (FMECA) to verify fail-safe behavior
- Testing to confirm fail-safe characteristics

**5. Safe Communication:**
- Implementation of EN 50159 safety-related communication principles
- Sequence numbering, timeout, message authentication
- Detection of repetition, deletion, insertion, re-sequencing, corruption, delay, masquerade

### Safety Case and Evidence

**Safety Case Requirement:**
EN 50129 mandates comprehensive Safety Case documenting safety arguments and supporting evidence:

**Safety Case Structure:**
1. **Definition of System:** Scope, boundaries, interfaces, operating environment
2. **Quality Management Report:** Evidence of rigorous development process per ISO 9001 or equivalent
3. **Safety Management Report:** Evidence of safety management throughout lifecycle per EN 50126-2
4. **Technical Safety Report:** Detailed technical safety analysis and evidence
5. **Related Safety Cases:** References to subsystem and equipment safety cases
6. **Conclusion:** Summary argument demonstrating system acceptably safe

**Technical Safety Report Contents:**
- **System Description:** Architecture, hardware, software, interfaces
- **Hazard Log:** Complete register of hazards, risk assessment, mitigation measures
- **Safety Requirements Specification:** All safety functions and integrity requirements
- **Safety Analysis:** FMECA, FTA, common cause failure analysis, software safety analysis (per EN 50128)
- **Verification Evidence:** Test reports, reviews, inspections, analysis results
- **Safety Validation:** Independent assessment confirming safety requirements met
- **Operation and Maintenance Evidence:** Procedures ensuring ongoing safety in operation

**Independent Safety Assessment:**
EN 50129 requires independent safety assessor (not involved in development) to review and validate Safety Case:
- Assessor competence requirements specified
- Assessment scope covers complete Safety Case
- Assessor issues Safety Assessment Report with acceptance recommendation
- Assessor independence maintained throughout project

### Development Lifecycle Requirements

**Lifecycle Phases per EN 50126:**
EN 50129 requires adherence to EN 50126 14-phase RAMS lifecycle with additional safety-specific requirements:

**Phase 1-5: Concept through Requirements Apportionment**
- Risk analysis identifying all hazards
- SIL determination based on risk assessment
- Safety requirements specification with SIL allocation
- Verification planning (test specifications, acceptance criteria)

**Phase 6: Design and Implementation**
- Design complying with EN 50129 techniques and measures
- Hardware design per EN 50129 principles
- Software design per EN 50128 (if software present)
- Safety-related communication per EN 50159
- Design reviews and verification activities
- Configuration management and change control

**Phase 7-8: Manufacturing and Installation**
- Manufacturing quality control per ISO 9001
- Installation verification and testing
- As-built documentation

**Phase 9: Validation**
- Comprehensive safety validation testing
- Demonstrate SIL requirements achieved
- Independent safety assessment
- Safety Case completion and approval

**Phase 10-14: Acceptance through Decommissioning**
- Formal acceptance based on demonstrated safety performance
- Operational safety monitoring
- Change management for modifications
- Safe decommissioning at end-of-life

## Compliance Testing and Validation

### SIL Verification Testing

**Hardware Safety Testing:**

**Random Hardware Failure Analysis:**
- Calculate dangerous failure rate using component failure rate data (IEC 61709, manufacturer data)
- Apply architectural constraints (minimum hardware safety integrity requirements)
- Prove dangerous failure rate < SIL threshold
- Account for common cause failures (β-factor, 10-20% typical)

**Systematic Failure Avoidance:**
- Design reviews (peer review, HAZOP, FMECA)
- Extensive testing at component, subsystem, and system levels
- Environmental stress testing (temperature, vibration, EMC, power variations)
- Proof testing demonstrating > 99% dangerous failure detection coverage

**Example SIL 4 Requirements:**
- Hardware Fault Tolerance (HFT) ≥ 1 (redundancy required)
- Safe Failure Fraction (SFF) ≥ 99%
- Architectural Constraints met (per IEC 61508 Table 3 or EN 50129 Annex A)
- Dangerous failure rate < 10⁻⁹ per hour proven by analysis

**Software Safety Testing (per EN 50128):**
- See EN 50128 standard for detailed software safety requirements
- Module testing with 100% statement and decision coverage (MC/DC for SIL 3/4)
- Integration testing verifying interfaces
- Software safety validation testing per software safety requirements
- Independent software assessment

**Integration Testing:**
- Hardware-software integration testing
- Interface testing (all interfaces to other systems or equipment)
- System-level functional testing (all safety functions verified)
- Failure mode testing (inject faults and verify fail-safe behavior)
- Performance testing under maximum load conditions

### Environmental and Stress Testing

**EN 50155 Railway Equipment Testing:**
Railway electronic equipment must withstand harsh operating environment:

**Temperature Testing:**
- Operating temperature range: -40°C to +70°C (typical railway equipment)
- Storage temperature range: -40°C to +85°C
- Thermal shock testing (rapid temperature changes)
- Verification of performance across full temperature range

**Vibration and Shock Testing:**
- Vibration per EN 61373 (railway vibration and shock standard)
- Random vibration simulating track-induced vibration
- Shock testing simulating coupling impacts and emergency braking
- Endurance testing over equivalent lifecycle (typically 20 years simulated vibration)

**Electromagnetic Compatibility (EMC) Testing per EN 50121:**
- Conducted and radiated emissions (equipment must not interfere with other systems)
- Conducted and radiated immunity (equipment must operate correctly in EMI environment)
- ESD (Electrostatic Discharge) immunity
- Surge and transient immunity (lightning, switching transients)

**Power Supply Variations:**
- Voltage variation testing: ±25% of nominal (e.g., 18-30V DC for 24V nominal)
- Voltage interruptions and brownouts
- Power-on/power-off transient testing
- Verification of correct operation throughout voltage range

**Climatic and Environmental Testing:**
- Humidity testing: up to 95% relative humidity non-condensing
- Salt fog testing (for equipment in coastal environments)
- Ingress Protection (IP) rating verification (typically IP54 or higher for trackside equipment)
- UV exposure testing (for outdoor equipment)
- Chemical resistance (oil, fuel, cleaning agents)

### Reliability and Safety Validation

**Reliability Demonstration:**
- Accelerated life testing proving hardware MTBF targets met
- Statistical confidence calculation (typically 90% confidence)
- Field data collection supporting reliability predictions

**Safety Validation:**
- Fault injection testing: deliberately inject faults and verify fail-safe response
- Residual fault testing: attempt to create hazardous condition, verify prevention
- Boundary condition testing: test system at operational limits
- Stress testing: exceed design limits to identify failure modes

**Independent Safety Validation:**
- Independent Safety Assessor reviews all verification evidence
- Witnesses key validation tests
- Reviews Safety Case completeness and adequacy
- Issues Safety Assessment Report with acceptance or rejection recommendation

## Certification Process

### Regulatory Approval Process

**Step 1: Preliminary Safety Case Submission**
- Submit preliminary Safety Case during design phase (typically after Critical Design Review)
- Railway authority and/or Independent Safety Assessor review
- Feedback and required revisions documented
- Establishes basis for final Safety Case

**Step 2: Development Phase Audits**
- Quality system audits per ISO 9001 (typically annual)
- Development process audits verifying EN 50129 compliance
- Safety management system audits per EN 50126-2
- Design review participation by assessor or authority representative

**Step 3: Type Approval Testing**
- Complete product testing per EN 50129 requirements
- Environmental testing per EN 50155 and EN 50121
- SIL verification testing demonstrating safety integrity requirements met
- Independent test witnessing by Notified Body or assessor

**Step 4: Final Safety Case Submission**
- Complete Safety Case with all verification evidence
- All open issues from preliminary Safety Case resolved
- Test reports, analysis results, design documentation included
- Configuration management baseline documented

**Step 5: Independent Safety Assessment**
- Independent Safety Assessor conducts comprehensive Safety Case review
- Assessor may request additional evidence or testing
- Assessor issues Safety Assessment Report with findings and recommendation
- Findings must be resolved before acceptance (or justified as acceptable risk)

**Step 6: Regulatory Authorization**
- Railway Authority (ERA or National Safety Authority) reviews Safety Case and Assessment Report
- Authority may conduct additional audits or request information
- Authorization granted (potentially with conditions or restrictions)
- Certificate of Conformity or Authorization for Placing into Service issued

### Certification Bodies and Authorities

**European Union Agency for Railways (ERA):**
- Type approval for ERTMS/ETCS systems (interoperability constituents)
- EC Certificate of Conformity for compliance with Control-Command and Signaling TSI
- Website: www.era.europa.eu

**National Safety Authorities (NSAs) - Examples:**
- **Office of Rail and Road (ORR) - United Kingdom**
- **Eisenbahn-Bundesamt (EBA) - Germany**
- **Agence Nationale de Sécurité Ferroviaire (ANSF) - France**
- **Agenzia Nazionale per la Sicurezza delle Ferrovie (ANSF) - Italy**
- **Agencia Estatal de Seguridad Ferroviaria (AESF) - Spain**

**Notified Bodies for Railway Interoperability:**
Accredited independent organizations conducting conformity assessment:
- **TÜV SÜD Rail** (Germany/International)
- **Lloyd's Register Rail** (UK/International)
- **Bureau Veritas** (France/International)
- **DEKRA** (Germany/International)
- **Intertek** (Sweden/International)
- **RINA** (Italy)

**Notified Body Services:**
- EC Type Examination (Module B)
- Conformity to Type (Module D - production quality)
- Product Verification (Module F - product testing)
- Independent Safety Assessment per EN 50129
- ISO 9001 quality system certification

### Certification Documentation Requirements

**Essential Safety Case Documents:**

1. **System Definition:**
   - System boundary and scope
   - Operating environment and conditions
   - Interfaces to other systems (detailed interface specifications)
   - Architecture (hardware, software, communication)

2. **Quality Management Report:**
   - ISO 9001 certificate or equivalent
   - Quality plan for project
   - Audit reports demonstrating quality compliance
   - Configuration management procedures and records

3. **Safety Management Report:**
   - Safety management plan per EN 50126-2
   - Organization, roles, and responsibilities
   - Safety culture and competency management
   - Safety review and audit records

4. **Technical Safety Report:**
   - **Part A: Safety Requirements**
     - Hazard Log with complete risk assessment
     - Safety requirements specification with SIL allocation
     - Safety integrity requirements for each safety function
   - **Part B: Design and Implementation**
     - Design description (hardware, software, communication)
     - Application of EN 50129 safety techniques
     - FMECA proving fail-safe behavior
     - Fault Tree Analysis (FTA) for critical hazards
     - Common Cause Failure (CCF) analysis
   - **Part C: Verification Evidence**
     - Test specifications and test reports
     - Review and inspection reports
     - Analysis results (reliability, safety, performance)
     - Software Safety Case (per EN 50128) if applicable
     - Environmental test reports (EN 50155, EN 50121)
   - **Part D: Validation**
     - Validation test reports (SIL demonstration)
     - Field trial results (if applicable)
     - Operational experience (for existing designs)

5. **Related Safety Cases:**
   - References to subsystem Safety Cases (commercial-off-the-shelf components, previous certifications)
   - Interface agreements for systems supplied by different organizations

6. **Independent Safety Assessment Report:**
   - Assessor credentials and independence statement
   - Assessment scope and methodology
   - Findings and recommendations
   - Acceptance or conditional acceptance conclusion

7. **Operations and Maintenance Evidence:**
   - Operations manual with safety-critical procedures
   - Maintenance manual ensuring safety integrity maintained
   - Training requirements for operations and maintenance personnel
   - Configuration control procedures for modifications

## Industry Adoption and Implementation

### Global Adoption Status

**European Union (Mandatory):**
EN 50129 is legally mandated for all railway signaling systems requiring interoperability authorization within the EU. The standard is referenced directly in the Control-Command and Signaling Technical Specification for Interoperability (CCS TSI).

**Countries with Mandatory EN 50129 Compliance:**
- All 27 EU member states
- Norway, Switzerland (EFTA countries with railway interoperability agreements)
- United Kingdom (post-Brexit continuation of EU railway safety standards)
- Turkey, Serbia (candidate countries aligning with EU acquis)

**International Adoption:**
Many countries have adopted EN 50129 or harmonized equivalent:
- **Australia:** AS 7671 series based on EN 50129 principles
- **Japan:** Adapted into Japanese railway safety standards (interpretive guidelines)
- **China:** GB/T standards for urban rail signaling influenced by EN 50129
- **India:** Mandated for metro rail projects and ETCS deployments
- **Middle East:** Required for major metro projects (Dubai, Doha, Riyadh, Saudi Arabia)
- **Southeast Asia:** Singapore, Malaysia, Thailand adopt EN 50129 for urban rail
- **Latin America:** Argentina, Brazil, Chile adopting for metro and mainline projects

**North America:**
Not formally adopted, but EN 50129 principles inform:
- AREMA (American Railway Engineering and Maintenance-of-Way Association) guidelines
- AAR (Association of American Railroads) standards
- FRA (Federal Railroad Administration) PTC safety requirements
- Growing adoption for major urban transit projects

### Vendor Implementation

**Major Railway Signaling Vendors:**

**Alstom:**
- All signaling products developed per EN 50129 (Atlas ETCS, Smartlock interlocking, Urbalis CBTC)
- Product-level Safety Cases certified by multiple Notified Bodies
- Generic Product Safety Cases leveraged across projects
- SIL 4 certification for Vital Computer platforms
- Over 3,000 Smartlock installations with EN 50129 certification

**Siemens Mobility:**
- Comprehensive EN 50129 compliance for Trainguard family and Simis interlocking
- Certified SIL 4 vital computer platforms
- Notified Body approvals from TÜV, Lloyd's Register, Bureau Veritas
- Generic Safety Cases for standard products reducing project certification effort
- Documented operational track record supporting safety case claims

**Hitachi Rail:**
- EN 50129 application for ETCS and interlocking products
- SIL 4 interlocking platform with Notified Body approval
- Project-specific Safety Cases building on generic product safety cases

**Thales Ground Transportation:**
- SelTrac CBTC platform EN 50129 certified
- Mainline signaling products compliant with EN 50129
- Extensive operational safety data supporting reliability claims

**CAF Signalling (formerly Dimetronic):**
- Spanish-origin signaling vendor with growing international presence
- EN 50129 compliant interlocking and CBTC systems
- Cost-competitive while maintaining safety certification

### Railway Authority Implementation

**Network Rail (United Kingdom):**
- Mandates EN 50129 compliance for all new signaling installations
- Requires Independent Safety Assessment by competent assessor
- Project-specific Safety Case required even for generic products
- Railway Safety and Standards Board (RSSB) provides guidance and governance

**Deutsche Bahn (Germany):**
- Requires EN 50129 certification for signaling systems
- DB-specific requirements in addition to EN 50129 baseline
- Long approval process with extensive documentation review
- Focus on interoperability with existing DB infrastructure

**SNCF/SNCF Réseau (France):**
- EN 50129 mandatory with French-specific interpretations
- Requires French language Safety Case documentation
- ANSF (French NSA) authorization required
- Emphasis on harmonization with French railway safety principles

**Trenitalia/RFI (Italy):**
- EN 50129 compliance required for signaling projects
- ANSF (Italian NSA) conducts thorough Safety Case review
- Notified Body assessment required (typically RINA or international body)

**ADIF (Spain):**
- EN 50129 standard applied to high-speed and conventional signaling
- Spanish NSA (AESF) authorization process
- Emphasis on ERTMS deployment compliance

## Version History and Evolution

### EN 50129:2003 (First Edition)
**Published:** February 2003 (consolidated from prEN 50129-1 and prEN 50129-2 drafts)

**Key Features:**
- Established SIL framework for railway signaling (SIL 0 through SIL 4)
- Defined Safety Case structure and content
- Specified safety principles and techniques for electronic systems
- Established Independent Safety Assessment requirement
- Harmonized with IEC 61508 functional safety principles

**Limitations:**
- Less detailed guidance on specific techniques and measures
- Limited consideration of complex software-intensive systems (addressed more in EN 50128)
- Less clarity on application of generic safety cases to projects
- Pre-dated widespread ETCS deployment (experience base limited)

### EN 50129:2018 (Current Edition)
**Published:** December 2018, effective 2020 after transition period

**Major Enhancements:**
- **Clearer Application Guidance:** More detailed guidance on applying EN 50129 to specific system types (interlocking, ETCS, CBTC)
- **Generic Safety Case Approach:** Better definition of how generic product safety cases applied to projects
- **Pre-Existing Software/Hardware:** Guidance on using commercial off-the-shelf (COTS) components and legacy systems
- **Safety Case Proportionality:** Risk-based approach to Safety Case detail (higher risk = more detailed evidence)
- **Integration with EN 50128/50159:** Clearer interfaces between hardware (EN 50129), software (EN 50128), and communication (EN 50159) safety requirements
- **Operational Phase Emphasis:** Enhanced requirements for maintaining safety in operation (modifications, obsolescence management)
- **Updated References:** Alignment with EN 50126-1:2017 and current IEC 61508 edition
- **Cybersecurity Considerations:** Preliminary guidance on cybersecurity threats (though dedicated cybersecurity standard IEC 62443 referenced)

**Backward Compatibility:**
- Systems certified to EN 50129:2003 remain valid
- Transition period allowed existing projects to complete under 2003 edition
- New projects from 2020 must use 2018 edition

### Future Development Directions

**Anticipated Updates (Next Revision Expected ~2028-2030):**
- **Autonomous Train Operation:** Specific guidance for GoA4 (fully driverless) systems and safety assurance approaches
- **Artificial Intelligence/Machine Learning:** Safety requirements for AI/ML in safety-critical functions (deterministic behavior vs. probabilistic AI)
- **Cybersecurity Integration:** Full integration with IEC 62443 railway cybersecurity requirements (cyber-physical safety)
- **Continuous Evolution:** Managing safety of continuously updated software-defined systems (over-the-air updates)
- **Digital Twin and Simulation:** Use of digital twins for safety validation and operational safety monitoring
- **V2X Communication Safety:** Vehicle-to-everything communication safety for future train control

**Harmonization Efforts:**
- Greater alignment with IEC 62425 (international railway functional safety standard)
- Closer integration with automotive functional safety ISO 26262 (shared autonomous vehicle principles)
- Alignment with emerging cybersecurity standards IEC 62443-4-1 and IEC 62443-4-2

## References and Related Standards

### Primary Standard
1. **EN 50129:2018** - Railway applications — Communication, signalling and processing systems — Safety related electronic systems for signalling

### CENELEC Railway Safety Standards Family
2. **EN 50126-1:2017** - Railway applications — RAMS specification and demonstration — Part 1: Generic RAMS process
3. **EN 50126-2:2017** - Railway applications — RAMS specification and demonstration — Part 2: Systems approach to safety
4. **EN 50128:2011** - Railway applications — Software for railway control and protection systems
5. **EN 50159:2010** - Railway applications — Communication, signalling and processing systems — Safety-related communication in transmission systems

### Railway Equipment Standards
6. **EN 50155:2017** - Railway applications — Electronic equipment used on rolling stock
7. **EN 50121 series** - Railway applications — Electromagnetic compatibility (EMC standards for railway)
8. **EN 61373:2010** - Railway applications — Rolling stock equipment — Shock and vibration tests

### Generic Functional Safety Standards
9. **IEC 61508:2010** (all parts) - Functional safety of electrical/electronic/programmable electronic safety-related systems
10. **IEC 62425:2021** - Railway applications — Communication, signalling and processing systems — Safety related electronic systems for signalling (International harmonized version of EN 50129)

### Component Reliability and Failure Data
11. **IEC 61709:2017** - Electric components — Reliability — Reference conditions for failure rates and stress models for conversion
12. **IEC TR 62380:2004** - Reliability data handbook — Universal model for reliability prediction of electronics components, PCBs and equipment
13. **MIL-HDBK-217F** - Reliability Prediction of Electronic Equipment (widely used historical reference)

### Safety Analysis Techniques
14. **IEC 60812:2018** - Failure modes and effects analysis (FMEA and FMECA)
15. **IEC 61025:2006** - Fault tree analysis (FTA)
16. **IEC 61078:2016** - Analysis techniques for dependability — Reliability block diagram and Boolean methods
17. **IEC 62551:2012** - Analysis techniques for dependability — Petri net techniques

### Quality Management
18. **ISO 9001:2015** - Quality management systems — Requirements
19. **ISO/TS 22163:2020** - Railway applications — Quality management system — Business management system requirements for rail organizations (IRIS - International Railway Industry Standard)

### European Railway Regulations
20. **Directive (EU) 2016/797** - Interoperability Directive (railway system interoperability framework)
21. **Directive (EU) 2016/798** - Railway Safety Directive (common safety framework)
22. **Commission Regulation (EU) 2016/919** - Technical Specification for Interoperability - Control-Command and Signalling (CCS TSI) (directly references EN 50129)

### Best Practice Guides
23. **ERA Practical Arrangements for the Approval of Projects** - European Railway Agency guidance on authorization process
24. **CENELEC Guide 29** - Safety-related electrical control systems for machinery (industrial safety principles applicable to railway)
25. **UK Railway Safety and Standards Board (RSSB) Guidance Notes** - UK-specific EN 50129 interpretation and application guides

---

**Document Classification:** Technical Standard Reference - Public
**Distribution:** General Distribution - Railway Engineering and Safety Community
**Review Cycle:** Updated when standard revised (EN 50129 approximately every 15 years, next revision expected ~2028-2030)
**Version Control:** 1.0 (2025-11-05) - Comprehensive standard overview based on EN 50129:2018
**Official Standard:** Available from CENELEC national members (BSI, DIN, AFNOR, UNE, etc.) or IEC webstore (IEC 62425 international version)