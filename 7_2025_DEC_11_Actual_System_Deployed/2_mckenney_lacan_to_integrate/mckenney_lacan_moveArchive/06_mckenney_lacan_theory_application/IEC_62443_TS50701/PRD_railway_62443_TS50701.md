# **Operationalizing Railway Cybersecurity: A Lifecycle Workshop Framework Integrating IEC 62443 and CLC/TS 50701**

## **1\. Strategic Convergence: The Necessity of a Unified Workshop Architecture**

The digitalization of the global railway sector has fundamentally altered the risk landscape of critical infrastructure. As railway systems transition from bespoke, isolated proprietary architectures to interconnected systems utilizing Commercial Off-The-Shelf (COTS) components and standard communication protocols—such as the European Rail Traffic Management System (ERTMS) and Communications-Based Train Control (CBTC)—the "air gap" that historically protected safety-critical assets has effectively evaporated.1 This technological shift necessitates a rigorous alignment between the well-established discipline of Functional Safety (governed by EN 50126, EN 50128, EN 50129\) and the emerging imperatives of Cybersecurity (governed by IEC 62443 and CLC/TS 50701).

The challenge facing asset owners, integrators, and suppliers is not merely technical but procedural and cultural. Safety engineers operate on timescales of decades, prioritizing determinism and reliability, whereas cybersecurity practitioners operate in a landscape of rapidly evolving threats requiring agility and frequent patching.3 To bridge this chasm, a structured workshop series is required—one that does not merely "add" security to a project but weaves it into the systems engineering V-cycle.

This report establishes a comprehensive framework for such a workshop series. It is designed to guide stakeholders from the initial definition of the System Under Consideration (SuC) through to the handover of a validated Cybersecurity Case. Central to this framework is the methodology of "ingesting" existing safety artifacts—Hazard Logs, RAMS (Reliability, Availability, Maintainability, and Safety) analyses, and architectural diagrams—to inform a consequence-driven cybersecurity strategy.5 By anchoring cybersecurity discussions in the physical reality of railway hazards (derailment, collision, fire), the workshops prioritize risks that matter most, moving beyond abstract IT security concerns to concrete Operational Technology (OT) resilience.

### **1.1 The Regulatory and Standards Landscape**

The framework proposed herein is grounded in the specific requirements of CLC/TS 50701, the railway-specific implementation of the IEC 62443 industrial security standard. TS 50701 serves as the "Rosetta Stone," translating the generic concepts of Zones, Conduits, and Security Levels from IEC 62443 into the specific context of rolling stock, signaling, and fixed installations.5

The regulatory pressure to adopt this approach is intensifying. The European Union’s NIS2 Directive and the Cyber Resilience Act (CRA) mandate that operators of essential services and manufacturers of critical products demonstrate a high level of cybersecurity hygiene and "security by design".7 Furthermore, national regulations and industry guidelines, such as the TSA Security Directives in the United States and the Rail Cyber Security Guidance in the UK, reinforce the need for a risk-based, defensible cybersecurity posture.9 This workshop series provides the evidentiary basis for compliance with these overlapping regimes.

## ---

**2\. The Standards Nexus: A Narrative Sequence Diagram**

To manage the complexity of a rail project, the cybersecurity lifecycle must be synchronized with the EN 50126 RAMS lifecycle. This synchronization prevents the "bolting on" of security at the Factory Acceptance Test (FAT) stage, where it is often too late or too expensive to implement architectural changes. The following sequence analysis identifies the critical "Nexus Points"—moments where Safety and Security disciplines must converge to exchange data and validate assumptions.11

### **2.1 The Nexus Point Architecture**

The lifecycle interaction between IEC 62443/TS 50701 and EN 50126 can be visualized as a sequence of data exchanges. The Safety team provides the "Consequence" (what happens if it fails), and the Security team provides the "Likelihood" (how can it be made to fail maliciously).

| Sequence Phase | EN 50126 Stage (Safety) | TS 50701/IEC 62443 Activity (Security) | Nexus Point (Data Exchange) | Primary Participants |
| :---- | :---- | :---- | :---- | :---- |
| **1\. Concept** | Phase 1: Concept | **ZCR 1:** SuC Identification | **NP-1: Asset Definition.** Security team ingests the Preliminary System Definition to identify the boundary of the System Under Consideration (SuC). | Owner, Operator, Systems Engineer |
| **2\. Definition** | Phase 2: System Definition & App. Conditions | **ZCR 2:** Initial Risk Assessment (IRA) | **NP-2: The Consequence Mapping.** Safety Hazard Log (PHA) is uploaded. "Catastrophic" hazards are mapped to cyber assets. "Worst Case" scenarios are defined. | Safety Mgr, Cyber Architect, Owner |
| **3\. Risk Analysis** | Phase 3: Risk Analysis | **ZCR 3:** Partitioning (Zones & Conduits) | **NP-3: The Zoning Architecture.** Functional architecture is segmented based on criticality (SIL levels) and exposure. | Integrator, Network Architect |
| **4\. Specification** | Phase 4: System Requirements | **ZCR 4/5:** Detailed Risk Assessment (DRA) | **NP-4: Requirements Apportionment.** Cybersecurity requirements (CSRS) are drafted to mitigate specific threat vectors identified in the DRA. | Supplier, Integrator, Cyber Lead |
| **5\. Design** | Phase 5: Architecture & Design | **ZCR 6:** Capability Assessment (SL-C) | **NP-5: Capability Check.** Suppliers confirm their products meet the Security Level Target (SL-T). Gaps become "Application Conditions." | Supplier, Integrator |
| **6\. Implementation** | Phase 6/7: Design & Manufacture | **Build:** Secure Development Lifecycle (SDL) | **NP-6: Vulnerability Management.** Code scanning and hardening during manufacturing (IEC 62443-4-1). | Supplier (Product Cert) |
| **7\. Validation** | Phase 9: System Validation | **Verify:** Security Level Achieved (SL-A) | **NP-7: The Integrated Test.** Pen-testing and functional testing to verify that security controls do not degrade safety performance (latency/availability). | ISA, Pentester, Commissioning Mgr |
| **8\. Handover** | Phase 10: System Acceptance | **Deliver:** Cybersecurity Case | **NP-8: The Handover.** The Cybersecurity Case is referenced by the Safety Case. Transfer of residual risk to Operations. | Owner, Operator, Maintainer |

### **2.2 Phase-by-Phase Sequence Narrative**

#### **Phase A: System Definition & The "Upload" (Nexus Point 1\)**

The sequence begins with the **System Definition**. In EN 50126, the physical scope is defined—track layout, rolling stock fleet, signaling type. The cybersecurity workshop series initiates here by defining the **System Under Consideration (SuC)**. This is not merely a list of servers; it is a boundary definition. The "Nexus" occurs when the Safety team’s asset register is "uploaded" to the cybersecurity scope. If the Safety definition includes "Wayside Object Controller," the Security definition must include the specific interfaces (Ethernet, Serial, GSM-R) of that controller. The output is a unified asset list that serves as the foundation for both disciplines.5

#### **Phase B: The Consequence-Driven Risk Assessment (Nexus Point 2\)**

Once the system is defined, the sequence moves to **Risk Analysis**. In the safety world, this generates the **Preliminary Hazard Analysis (PHA)**, identifying events like collision or derailment. The cybersecurity team consumes this PHA. Instead of inventing new consequences (like "data loss"), the cybersecurity workshop adopts the Safety consequences. The logic is explicit: if a cyber-attack can cause a specific hazard found in the log, the impact rating of that cyber-attack defaults to the safety severity (e.g., Catastrophic). This ensures that the **Initial Risk Assessment (IRA)**—the "Worst Case" analysis—is grounded in physical reality.14

#### **Phase C: Partitioning and Architecture (Nexus Point 3\)**

With risks identified, the system must be architected to contain them. This is the **Zoning and Conduit** phase (IEC 62443-3-2). The Nexus Point here is the alignment of **Safety Integrity Levels (SIL)** with **Security Levels (SL)**. Typically, assets with high SIL requirements (SIL 3/4) are grouped into high-security zones (SL 3/4). The workshop sequence dictates that the Zone design must be validated against the Safety architecture to ensuring that redundancy mechanisms (e.g., A/B plane switching) are not compromised by security segmentation (e.g., firewalls blocking heartbeat messages).2

#### **Phase D: Detailed Assessment and Implementation (Nexus Points 4-6)**

As the project moves into detailed design, the sequence involves deep interaction with suppliers. The **Detailed Risk Assessment (DRA)** analyzes specific vulnerabilities in the selected products. Here, the sequence requires "interrogating" the supply chain. The Nexus Point involves the exchange of **Implementation Conformance Statements**. The supplier must prove that the specific "Black Box" provided has been hardened according to IEC 62443-4-2. Any inability to meet the requirement (e.g., "Legacy device cannot support encryption") triggers a feedback loop, requiring the system integrator to design a Compensating Countermeasure (e.g., placing the device behind a Deep Packet Inspection firewall).11

#### **Phase E: Assurance and Handover (Nexus Points 7-8)**

The final sequence is the validation. The **Cybersecurity Case** is assembled, aggregating evidence from all previous phases. This document is not standalone; it is a child-dependency of the **Safety Case**. The Safety Case cannot be closed until the Cybersecurity Case demonstrates that the risk of cyber-induced safety failures has been reduced to As Low As Reasonably Practicable (ALARP). The sequence concludes with the **Handover**, where the project team transfers the "Residual Risk Register" and the "Cybersecurity Management Plan" to the Operations team.16

## ---

**3\. Methodology: The Data Ingestion Engine**

A critical failure mode in cybersecurity workshops is the lack of specific engineering data, leading to generic and unhelpful risk assessments. To counter this, a robust "Ingestion Engine" methodology is required to "upload" and reference existing project documentation. This process transforms static documents into dynamic inputs for the risk workshop.

### **3.1 Constructing the Unified Risk Register (URR)**

The URR is the central database for the workshop series. It links Safety Hazards, Technical Assets, and Cyber Threats.

#### **3.1.1 Ingesting the Hazard Log (RAMS Data)**

* **Source:** Safety Hazard Log (EN 50126 Artifact).  
* **Mechanism:** Extract columns for *Hazard ID*, *Description*, *Severity*, and *Cause*.  
* **Transformation:** Filter for causes related to "Human Error," "Control Failure," "False Command," or "Corruption." These are potential cyber-proxies.  
* **Workshop Input:** These filtered hazards become the "Impact" columns in the IEC 62443 Risk Matrix.  
  * *Example:* Hazard H-04 "Train detection lost" (Critical) \-\> Cyber Impact "Loss of Integrity/Availability" (Critical).1

#### **3.1.2 Ingesting System Documentation (Architecture)**

* **Source:** Network Topology Diagrams, Bill of Materials (BOM), Interface Control Documents (ICD).  
* **Mechanism:** Create an "Asset Inventory" table. For each asset, tag its attributes:  
  * *Physical Location* (Onboard, Trackside, Station).  
  * *Logical Interface* (Ethernet, MVB, CAN bus, Radio).  
  * *Operating System/Firmware* (Windows, Linux, Proprietary).  
* **Transformation:** Map each asset to the Safety Function it supports.  
* **Workshop Input:** This defines the "Attack Surface." If an asset supports a Critical Hazard (from 3.1.1) and has a broad Attack Surface (e.g., Wi-Fi enabled), it becomes a "Critical Asset" for the IRA.5

#### **3.1.3 Ingesting Design Choices and Risks (Assumptions)**

* **Source:** Design Specification, Assumption Register.  
* **Mechanism:** Extract design decisions that trade security for functionality.  
  * *Example:* "Use of legacy unencrypted protocol (UDP) for speed."  
* **Transformation:** Convert these into "Vulnerabilities" for the Detailed Risk Assessment.  
* **Workshop Input:** These become the focal point of the "Compensating Controls" discussion.11

### **3.2 The "Upload" Reference Structure**

To facilitate the workshops, creating a standardized indexing system is essential.

| Document Class | Reference ID | Content Description | Ingestion Target |
| :---- | :---- | :---- | :---- |
| **Safety** | DOC-SAFE-01 | Preliminary Hazard Analysis (PHA) | **IRA Consequence** |
| **Safety** | DOC-SAFE-02 | Tolerable Hazard Rate (THR) Definitions | **Risk Acceptance Criteria** |
| **Architecture** | DOC-ARCH-01 | High-Level Network Topology | **Zoning (ZCR 3\)** |
| **Architecture** | DOC-ARCH-02 | Data Flow Diagram (DFD) | **Conduits (ZCR 3\)** |
| **Product** | DOC-PROD-XX | Supplier Security Certificates (IEC 62443-4-1) | **Capability Assessment** |
| **Operations** | DOC-OPS-01 | Concept of Operations (ConOps) | **Threat Modeling (Context)** |

## ---

**4\. Workshop Phase I: The "Worst Case" Disaster (Initial Risk Assessment)**

**Objective:** The primary goal of this first workshop is to shatter the "complacency bias" often found in engineering teams by confronting them with the maximum possible consequence of a successful cyber-attack. This aligns with IEC 62443-3-2 ZCR 2, which mandates an assessment of the "worst-case unmitigated risk".18

**Attendees:**

* Asset Owner (Risk Owner)  
* Head of Safety (RAMS)  
* Lead Systems Engineer  
* Cybersecurity Architect (Facilitator)  
* Operations Director

### **4.1 Session 1: The "Disaster" Brainstorming (Consequence Identification)**

This session ignores the *likelihood* of an attack and focuses entirely on the *impact*. The facilitator uses the Ingested Hazard Log (DOC-SAFE-01) to drive the conversation.

**Guided Conversation Questions:**

* **To the Safety Manager:** "Looking at Hazard H-1A (Collision), relying on the interlocking logic: If I am an attacker with 'God-mode' access to the interlocking, can I bypass the safety logic by forcing the memory state? Is the safety logic purely software, or is there a hardware relay backstop?".1  
* **To the Operator:** "Scenario: It is rush hour. A ransomware attack encrypts all workstations in the Operation Control Center (OCC). The screens go black. Do you have visibility of the trains? Can you manually stop them? How long before a safety incident occurs due to lack of visibility?".14  
* **To the Engineer:** "We utilize GSM-R for signaling. If I jam this signal or inject false packets (Man-in-the-Middle), does the train apply emergency braking (Fail-Safe) or does it continue using stale data (Fail-Unsafe)?".19

**Output:** A prioritized list of "Top Consequence Scenarios" (e.g., Uncommanded Switch Move, False Clear Signal, Loss of Supervision).

### **4.2 Session 2: The Initial Risk Assessment (IRA)**

Using the defined consequences, the team performs the IEC 62443-3-2 High-Level Risk Assessment.

* **Assumption:** For the IRA, we assume the likelihood of a threat attempting the attack is **High (1)**. This forces the assessment to rely on *consequence* reduction or robust *design* rather than hoping no one attacks.18  
* **Matrix Mapping:**  
  * *Vertical Axis:* Safety Consequence (Catastrophic, Critical, Marginal).  
  * *Horizontal Axis:* Likelihood (Certain/Frequent \- assumed for IRA).  
  * *Result:* Most safety-critical functions will land in the "Intolerable" or "Critical" risk zone.

**Insight:** This session typically reveals that "Air Gaps" are a myth. The ingestion of the Architecture (DOC-ARCH-01) usually shows maintenance gateways, passenger Wi-Fi bridges, or remote diagnostic links that pierce the gap.

### **4.3 Session 3: Initial Zoning (ZCR 3\)**

To mitigate the "Intolerable" risks identified, the system is compartmentalized.

**Guided Conversation:**

* "We identified that the Passenger Information System (PIS) is high-risk (internet connected) but low safety impact. The Interlocking is low connectivity but 'Catastrophic' impact. We must separate them."  
* **Drafting the Zone Model:**  
  * **Zone 1: Safety Critical (SIL 4).** Interlockings, RBCs. **Target:** SL-T 4\.  
  * **Zone 2: Critical Supervision.** OCC Servers, Traffic Management. **Target:** SL-T 3\.  
  * **Zone 3: Non-Critical Ops.** Station PIS, CCTV. **Target:** SL-T 1/2.  
  * **Zone 4: External/Untrusted.** Public Internet, Enterprise IT.

**Output:** A Draft Zone and Conduit Diagram (ZCR 3\) and an Initial Risk Assessment Report indicating the need for specific countermeasures.5

## ---

**5\. Workshop Phase II: Detailed Risk Assessment and Supplier Interrogation**

**Objective:** To validate if the proposed technologies can actually support the security zones defined in Phase I. This moves from the abstract to the concrete, analyzing specific hardware and software vulnerabilities. This aligns with IEC 62443-3-2 ZCR 5\.18

**Attendees:**

* System Integrator (Technical Lead)  
* Product Suppliers (Signaling, Comms, Scada)  
* Cybersecurity Specialist  
* Network Architect

### **5.1 Session 1: The Gap Analysis (SL-T vs. SL-C)**

The project has set a Target (SL-T). The Suppliers offer products with a Capability (SL-C). This session measures the gap.

**Guided Conversation (Supplier Interrogation):**

* **To the Signaling Supplier:** "We set the Interlocking Zone to SL-T 4\. Your interlocking hardware uses a maintenance port. Does this port support multi-factor authentication (MFA)? If not, it does not meet SL-C 4\. How do we mitigate this?".21  
* **To the Network Provider:** "We have a conduit between Trackside and Central. What encryption standard is used? Is it quantum-resistant, or at least AES-256? How do you manage the keys? Are keys hardcoded in the firmware?".5  
* **To the Integrator:** "Referencing the Ingested Design (DOC-ARCH-02), we see a 'Data Diode' is planned. Does this diode block *all* return traffic, including TCP handshakes? If so, how does the historian confirm data receipt?".22

### **5.2 Session 2: Threat Modeling (The "Upload" Integration)**

This session uses the STRIDE methodology (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege) applied to specific data flows identified in the "Upload" phase.

**Scenario Drill-Down:**

* **Scenario A (Tampering):** "Reference Asset. An attacker gains physical access to the trackside cabinet. Can they unplug the Ethernet cable and plug in a laptop to inject 'Switch Move' commands?"  
  * *Supplier Response:* "We use 802.1X Network Access Control (NAC)."  
  * *Follow-up:* "Is the NAC MAC-based (spoofable) or Certificate-based?"  
* **Scenario B (DoS):** "Reference Hazard. If an attacker floods the RBC (Radio Block Centre) with UDP packets, does it crash? If it crashes, do all trains emergency brake?"  
  * *Mitigation Discussion:* Rate limiting, storm control, industrial firewalls.

**Output:** A Detailed Risk Assessment (DRA) Register listing specific vulnerabilities, the planned mitigation, and the "Residual Risk".11

## ---

**6\. Workshop Phase III: Consensus, Mitigation, and Trade-offs**

**Objective:** To resolve the inevitable conflicts between Security, Safety, and Operations. High security often degrades availability or performance (latency). This workshop builds consensus on "Compensating Countermeasures".19

**Attendees:**

* Safety Manager (Decision Maker)  
* Operations Manager (Decision Maker)  
* Cybersecurity Lead (Advisor)  
* Project Manager

### **6.1 Session 1: The Friction Points (Safety vs. Security)**

**Guided Conversation:**

* **Latency vs. Encryption:** "The Cyber team wants to encrypt all ETCS Level 2 radio traffic. The Safety team says this adds 50ms of latency, which violates the braking curve requirement. **Consensus:** We accept unencrypted traffic *inside* the closed proprietary tunnel but enforce strict mutual authentication (integrity over confidentiality).".19  
* **Patching vs. Availability:** "IEC 62443-2-4 requires patching critical vulnerabilities within 14 days. Operations says we cannot reboot the Traffic Management System (TMS) outside of the annual blockade. **Consensus:** We implement a 'Virtual Patch' at the firewall level (IPS signature) to protect the vulnerability until the next maintenance window.".23

### **6.2 Session 2: Refining the Residual Risk**

Once mitigations are agreed upon, the risk is recalculated.

* **Residual Risk:** The risk remaining after mitigations.  
* **ALARP Demonstration:** The team must document *why* further mitigation is not possible (e.g., cost, technical feasibility) and why the remaining risk is tolerable.  
* **Reference:** TS 50701 Annex E (Risk Acceptance Methods).24

**Output:** A signed "Risk Acceptance Declaration" covering all residual risks.

## ---

**7\. Workshop Phase IV: The Cybersecurity Case and Handover**

**Objective:** To assemble the evidence required for certification and to prepare the organization for the "Run" phase. The project ends, but the risk remains.11

**Attendees:**

* Integrator (Handing over)  
* Asset Owner / Maintainer (Receiving)  
* Independent Safety Assessor (ISA) \- Optional Observer

### **7.1 Session 1: Structuring the Cybersecurity Case**

The Cybersecurity Case (TS 50701 Clause 9\) must be a structured argument supported by evidence.

**Table of Contents (Template for Workshop Output):**

1. **Executive Summary:** Declaration of Security Level Achieved (SL-A).  
2. **System Definition:** Scope, Boundaries, and Assumptions (from Workshop I).  
3. **Security Environment:** Threat Landscape and Risk Assessment Results (IRA/DRA).  
4. **Security Requirements Specification (CSRS):** The list of controls implemented.  
5. **Verification and Validation Evidence:**  
   * Test Reports (Penetration Testing, Vulnerability Scanning).  
   * Supplier Certificates (IEC 62443-4-1).  
   * Configuration Reviews.  
6. **Traceability Matrix:** Mapping Controls \-\> Threats \-\> Hazards.  
7. **Application Conditions (SecRAC):** What the operator *must* do to keep the system secure (e.g., "Change passwords every 90 days").  
8. **Residual Risk Statement:** The accepted risks.

**Activity:** Review the draft case. Does every "Catastrophic" hazard from the original Hazard Log have a corresponding entry in the Cybersecurity Case demonstrating mitigation?.6

### **7.2 Session 2: The Handover Plan (Transition to Opex)**

**Guided Conversation (The "Run" Phase):**

* **Patch Management:** "When the project team dissolves, who receives the CVE alerts for the Linux kernel in the Wayside Controller? Is there a contract with the supplier for 20 years of patches?".23  
* **Incident Response:** "We need a 'Rail-Specific' Incident Response Plan. If the signaling system acts erratically, the first step is usually 'Reset.' The new plan must include 'Disconnect and Preserve Logs' before resetting. Who is trained on this?".25  
* **Key Management:** "Who holds the root keys for the PKI (Public Key Infrastructure)? How are they rotated? Where are the backups kept?"

**Output:**

* **Cybersecurity Management Plan (CMP) for Operations.**  
* **Secure Deployment Guidelines.**  
* **Training Plan for Operators.**

## ---

**8\. Comprehensive Questionnaires and Guided Conversations**

To facilitate the workshops and "interrogate" the stakeholders effectively, the following detailed questionnaires should be used. These are derived from IEC 62443 requirements.

### **8.1 Questionnaire for Suppliers (Product Hardening)**

*Focus: IEC 62443-4-1 (Lifecycle) & 4-2 (Technical)* 21

| Ref ID | Category | Question for Supplier | Rationale (Standard Ref) |
| :---- | :---- | :---- | :---- |
| **SUP-01** | **Lifecycle** | Can you provide an independent certificate or assessment report demonstrating compliance with IEC 62443-4-1 (Secure Development Lifecycle)? | Ensures "Security by Design" (IEC 62443-4-1). |
| **SUP-02** | **Auth** | Does the device support centralized authentication (RADIUS/TACACS+) or strictly local accounts? Can default passwords be disabled? | Identification & Authentication (IAC) \- IEC 62443-4-2. |
| **SUP-03** | **Integrity** | How is firmware integrity verified? Is there a hardware root of trust (TPM/Secure Boot) to prevent persistent malware? | System Integrity (SI) \- IEC 62443-4-2. |
| **SUP-04** | **Ports** | Are all physical and logical ports (USB, Telnet, FTP) disabled by default? Can they be locked down via configuration? | Use Control (UC) \- IEC 62443-4-2. |
| **SUP-05** | **Logs** | specific logging capabilities does the device have? Can it send Syslog to a central SIEM? What events are logged (login failures, config changes)? | Timely Response to Events (TRE) \- IEC 62443-4-2. |
| **SUP-06** | **Vuln Mgt** | What is your guaranteed SLA for providing a security patch after a Critical CVE is published? Do you provide a hash for verification? | Patch Management (TS 50701 Cl. 10). |
| **SUP-07** | **Legacy** | If this is a legacy product, what specific external compensations (e.g., firewall rules, protocol converters) do you mandate? | Legacy Handling (TS 50701 Annex B). |

### **8.2 Questionnaire for System Integrators (Architecture)**

*Focus: IEC 62443-3-3 (System Security) & TS 50701 Zoning* 5

| Ref ID | Category | Question for Integrator | Rationale (Standard Ref) |
| :---- | :---- | :---- | :---- |
| **INT-01** | **Zoning** | Have you grouped assets into zones based on Criticality (Safety Impact) and Exposure? Are SIL 4 assets in a separate zone from SIL 0 assets? | Zoning & Conduits (IEC 62443-3-2). |
| **INT-02** | **Boundary** | What specific boundary protection devices (Firewalls, Unidirectional Gateways) are placed between the OT Zone and the Enterprise/Public Network? | Restricted Data Flow (RDF) \- IEC 62443-3-3. |
| **INT-03** | **Remote** | Describe the remote access solution. Does it use a Jump Host/DMZ? Is MFA enforced? Is the session recorded? | Remote Access (TS 50701). |
| **INT-04** | **Safety** | Have you performed a latency analysis to confirm that encryption/firewalling does not exceed the Maximum Tolerable Downtime (MTD) or safety response times? | Safety/Security Interface (TS 50701 Annex D). |
| **INT-05** | **Backup** | Is there an automated backup solution for the system configuration? Is the backup repository offline (air-gapped) or immutable? | Resource Availability (RA) \- IEC 62443-3-3. |
| **INT-06** | **Malware** | How is malware protection handled? Endpoint Protection (AV) or Application Whitelisting (Lockdown)? | Malicious Code Protection (SI). |

### **8.3 Questionnaire for Asset Owners/Operators (Operations)**

*Focus: IEC 62443-2-1 (Policies) & 2-4 (Maintenance)* 10

| Ref ID | Category | Question for Operator | Rationale (Standard Ref) |
| :---- | :---- | :---- | :---- |
| **OPS-01** | **Gov** | Is there a formal Cybersecurity Management System (CSMS) in place? Who is the "Risk Owner" for OT security (CISO or Engineering Director)? | Security Program (IEC 62443-2-1). |
| **OPS-02** | **People** | Are operators trained to distinguish between a "Signaling Fault" and a "Cyber Attack"? Is there a playbook for "Cyber-Safety" response? | Awareness & Training. |
| **OPS-03** | **Access** | How are employees off-boarded? Is there a process to revoke physical and digital access to the railway system immediately upon termination? | Account Management. |
| **OPS-04** | **Supply** | Do maintenance contracts with third parties (suppliers) include strict cybersecurity clauses (right to audit, patching obligations)? | Service Providers (IEC 62443-2-4). |
| **OPS-05** | **Incident** | Is there a 24/7 contact point for cyber incidents? Is this integrated with the National CERT or Rail ISAC? | Incident Response. |

## ---

**9\. Conclusion**

The cybersecurity of railway systems is not a product that can be bought; it is a process that must be engineered. By implementing the workshop series outlined in this report—anchored in the sequence of IEC 62443 and TS 50701—organizations can move from a reactive, compliance-based stance to a proactive, risk-based posture.

The key to success lies in the "Nexus Points"—the deliberate synchronization of Safety and Security data. By ingesting the Hazard Log and forcing the "Worst Case" conversation, stakeholders are compelled to treat cybersecurity with the same rigor as physical safety. The output—a robust Cybersecurity Case and a practical Handover Plan—ensures that the railway remains resilient in the face of an evolving threat landscape, protecting not just data, but lives.

#### **Works cited**

1. Understanding Railway Cybersecurity, accessed December 8, 2025, [https://gca.isa.org/blog/understanding-railway-cybersecurity](https://gca.isa.org/blog/understanding-railway-cybersecurity)  
2. Securing the Future of Railway Systems: A Comprehensive Cybersecurity Strategy for Critical On-Board and Track-Side Infrastructure \- PMC \- PubMed Central, accessed December 8, 2025, [https://pmc.ncbi.nlm.nih.gov/articles/PMC11680022/](https://pmc.ncbi.nlm.nih.gov/articles/PMC11680022/)  
3. (PDF) Railway cyber security and TS50701 \- ResearchGate, accessed December 8, 2025, [https://www.researchgate.net/publication/361006662\_Railway\_cyber\_security\_and\_TS50701](https://www.researchgate.net/publication/361006662_Railway_cyber_security_and_TS50701)  
4. The risk assessment of ERTMS-based railway systems from a cyber security perspective: methodology and lessons learned \- Adelard, accessed December 8, 2025, [https://www.adelard.com/media/ngznpfx4/adelard\_rssrail\_2016.pdf](https://www.adelard.com/media/ngznpfx4/adelard_rssrail_2016.pdf)  
5. How to conduct an IEC 62443-based assessment for metro rail infrastructure \- Shieldworkz, accessed December 8, 2025, [https://shieldworkz.com/blogs/how-to-conduct-an-iec-62443-based-assessment-for-metro-rail-infrastructure](https://shieldworkz.com/blogs/how-to-conduct-an-iec-62443-based-assessment-for-metro-rail-infrastructure)  
6. A deep dive into CENELEC TS 50701 for railway cybersecurity, accessed December 8, 2025, [https://shieldworkz.com/blogs/a-deep-dive-into-cenelec-ts-50701-for-railway-cybersecurity](https://shieldworkz.com/blogs/a-deep-dive-into-cenelec-ts-50701-for-railway-cybersecurity)  
7. The future of rail cybersecurity – building cyber resilience across the rail ecosystem \- Rail Business Daily, accessed December 8, 2025, [https://news.railbusinessdaily.com/the-future-of-rail-cybersecurity-building-cyber-resilience-across-the-rail-ecosystem/?print=pdf](https://news.railbusinessdaily.com/the-future-of-rail-cybersecurity-building-cyber-resilience-across-the-rail-ecosystem/?print=pdf)  
8. From EN IEC 62443 to CRA: OT Cybersecurity for Important products \- CEN-CENELEC, accessed December 8, 2025, [https://www.cencenelec.eu/media/CEN-CENELEC/Events/Webinars/2025/2025-09-08\_webinar\_unlocking\_cra\_iec62443-series-for-cra.pdf](https://www.cencenelec.eu/media/CEN-CENELEC/Events/Webinars/2025/2025-09-08_webinar_unlocking_cra_iec62443-series-for-cra.pdf)  
9. Rail Cyber Security Guidance to Industry \- Railway Cybersecurity, accessed December 8, 2025, [https://www.railway-cybersecurity.com/Rail\_Cyber\_Security\_Guidance.html](https://www.railway-cybersecurity.com/Rail_Cyber_Security_Guidance.html)  
10. Cybersecurity Assessment Tool for Transit Webinar Participant Questions, accessed December 8, 2025, [https://www.transit.dot.gov/sites/fta.dot.gov/files/2023-03/Cybersecurity-Assessment-Tool-for-Transit-Webinar-Participant-Questions\_0.pdf](https://www.transit.dot.gov/sites/fta.dot.gov/files/2023-03/Cybersecurity-Assessment-Tool-for-Transit-Webinar-Participant-Questions_0.pdf)  
11. Navigating TS 50701: Unpacking the Impact of the Cybersecurity Standard for Rail \- Cylus, accessed December 8, 2025, [https://www.cylus.com/post/navigating-ts-50701-unpacking-the-impact-of-the-cybersecurity-standard-for-rail](https://www.cylus.com/post/navigating-ts-50701-unpacking-the-impact-of-the-cybersecurity-standard-for-rail)  
12. (PDF) Railway Infrastructure Cybersecurity: An Overview \- ResearchGate, accessed December 8, 2025, [https://www.researchgate.net/publication/381651585\_Railway\_Infrastructure\_Cybersecurity\_An\_Overview](https://www.researchgate.net/publication/381651585_Railway_Infrastructure_Cybersecurity_An_Overview)  
13. ZONING AND CONDUITS FOR RAILWAYS \- ENISA, accessed December 8, 2025, [https://www.enisa.europa.eu/sites/default/files/publications/Zoning%20and%20Conduits%20for%20Railways%20-%20Security%20Architecture.pdf](https://www.enisa.europa.eu/sites/default/files/publications/Zoning%20and%20Conduits%20for%20Railways%20-%20Security%20Architecture.pdf)  
14. Top Cyber Threats in the Freight Rail Sector \- HALOCK Security Labs, accessed December 8, 2025, [https://www.halock.com/top-cyber-threats-in-the-freight-rail-sector/](https://www.halock.com/top-cyber-threats-in-the-freight-rail-sector/)  
15. Risk Assessment Matrix: How to Calculate & Use a Risk Matrix Effectively \- Vector Solutions, accessed December 8, 2025, [https://www.vectorsolutions.com/resources/blogs/risk-matrix-calculations-severity-probability-risk-assessment/](https://www.vectorsolutions.com/resources/blogs/risk-matrix-calculations-severity-probability-risk-assessment/)  
16. CLC TS50701 (2021) e | PDF | Security \- Scribd, accessed December 8, 2025, [https://www.scribd.com/document/713110977/CLC-TS50701-2021-e](https://www.scribd.com/document/713110977/CLC-TS50701-2021-e)  
17. Hands-On CLC/TS 50701 (Railway applications – CyberSecurity), accessed December 8, 2025, [https://www.era.europa.eu/system/files/2023-12/05%20Standards%20-%2002%20CENELEC%20Christian%20Schlehuber.pdf?t=1720627291](https://www.era.europa.eu/system/files/2023-12/05%20Standards%20-%2002%20CENELEC%20Christian%20Schlehuber.pdf?t=1720627291)  
18. Cybersecurity Risk Assessment According to ISA/IEC 62443-3-2, accessed December 8, 2025, [https://gca.isa.org/blog/cybersecurity-risk-assessment-according-to-isa-iec-62443-3-2](https://gca.isa.org/blog/cybersecurity-risk-assessment-according-to-isa-iec-62443-3-2)  
19. Cybersecurity Challenges in Modern Railway Signaling- A Comprehensive Review, accessed December 8, 2025, [https://www.researchgate.net/publication/395929856\_Cybersecurity\_Challenges\_in\_Modern\_Railway\_Signaling-\_A\_Comprehensive\_Review](https://www.researchgate.net/publication/395929856_Cybersecurity_Challenges_in_Modern_Railway_Signaling-_A_Comprehensive_Review)  
20. Practical Guide to Performing Risk Assessment as per IEC 62443-3-2 and NIST 800-30, accessed December 8, 2025, [https://hardhatsecurity.com/2024/05/15/practical-guide-to-performing-high-and-detailed-level-risk-assessment-as-per-iec-62443-3-2-and-nist-800-30/](https://hardhatsecurity.com/2024/05/15/practical-guide-to-performing-high-and-detailed-level-risk-assessment-as-per-iec-62443-3-2-and-nist-800-30/)  
21. IEC 62443: Ultimate OT Security Guide | Rockwell Automation | UK, accessed December 8, 2025, [https://www.rockwellautomation.com/en-gb/company/news/blogs/iec-62443-security-guide.html](https://www.rockwellautomation.com/en-gb/company/news/blogs/iec-62443-security-guide.html)  
22. Cybersecurity Lifecycle Services for Industrial Plants | ISA/IEC-62443 Experts \- WisePlant, accessed December 8, 2025, [https://wiseplant.com/rms-risk-managemet-system/](https://wiseplant.com/rms-risk-managemet-system/)  
23. CLC/TS 50701:2023 \- Railway applications \- Cybersecurity \- iTeh Standards, accessed December 8, 2025, [https://standards.iteh.ai/catalog/standards/clc/db257ea9-8ba0-4f4c-a791-df34a6030541/clc-ts-50701-2023](https://standards.iteh.ai/catalog/standards/clc/db257ea9-8ba0-4f4c-a791-df34a6030541/clc-ts-50701-2023)  
24. SIST-TS CLC/TS 50701:2024 \- iTeh Standards, accessed December 8, 2025, [https://cdn.standards.iteh.ai/samples/74651/a9c8ddd211c3488dad4994676afa70c5/SIST-TS-CLC-TS-50701-2024.pdf](https://cdn.standards.iteh.ai/samples/74651/a9c8ddd211c3488dad4994676afa70c5/SIST-TS-CLC-TS-50701-2024.pdf)  
25. Examples of cyber-attacks scenarios in railway operation and... \- ResearchGate, accessed December 8, 2025, [https://www.researchgate.net/figure/Examples-of-cyber-attacks-scenarios-in-railway-operation-and-maintenance-and-defensive\_tbl3\_338502122](https://www.researchgate.net/figure/Examples-of-cyber-attacks-scenarios-in-railway-operation-and-maintenance-and-defensive_tbl3_338502122)  
26. Reaching IEC 62443 compliance \- Bureau Veritas Cybersecurity, accessed December 8, 2025, [https://cybersecurity.bureauveritas.com/services/operational-technology/iec-62443-compliance](https://cybersecurity.bureauveritas.com/services/operational-technology/iec-62443-compliance)  
27. Cybersecurity standards and supply chain management for rail ..., accessed December 8, 2025, [https://www.mobility.siemens.com/global/en/portfolio/digital-solutions-software/cybersecurity/certification-standards.html](https://www.mobility.siemens.com/global/en/portfolio/digital-solutions-software/cybersecurity/certification-standards.html)  
28. 10 Questions to ask Your Systems Integrator for Project Success \- Prime Secured, accessed December 8, 2025, [https://blog.primesecured.com/security/10-questions-to-ask-to-your-systems-integrator](https://blog.primesecured.com/security/10-questions-to-ask-to-your-systems-integrator)  
29. Daily Safety Checklist Form for Railroad Operations | Free Template, accessed December 8, 2025, [https://safetyculture.com/library/transport-and-logistics/daily-safety-checklist-form-railroad-binq5jzuqbvb8ez1](https://safetyculture.com/library/transport-and-logistics/daily-safety-checklist-form-railroad-binq5jzuqbvb8ez1)  
30. Free cybersecurity maturity assessment questionnaire for evaluating your security posture \- Copla, accessed December 8, 2025, [https://copla.com/blog/cybersecurity/free-cybersecurity-maturity-assessment-questionnaire-for-evaluating-your-security-posture/](https://copla.com/blog/cybersecurity/free-cybersecurity-maturity-assessment-questionnaire-for-evaluating-your-security-posture/)