

# **A Comprehensive Cybersecurity Framework for Rail Transit Projects: An Integrated Security Case and Handover Plan Based on IEC 62443 and CLC/TS 50701**

## **Part I: The Strategic Cybersecurity Framework for Rail Infrastructure**

### **1.0 Introduction: Securing Modern Rail Transit as Critical Infrastructure**

#### **1.1 The Imperative for a Structured Framework**

The global rail sector is undergoing a profound digital transformation. Automated signaling, interconnected rolling stock, smart maintenance systems, and integrated passenger information networks are revolutionizing how railways operate, delivering unprecedented efficiency and service quality.1 However, this increasing reliance on digital technologies and the convergence of traditional, isolated Operational Technology (OT) with corporate Information Technology (IT) networks create a vast and complex cyber-attack surface.2 Rail systems are no longer merely mechanical and electrical; they are complex cyber-physical systems.

This evolution carries significant risk. Governments worldwide designate rail networks as critical national infrastructure, recognizing that their disruption can have severe consequences for public safety, economic stability, and national security.4 Unlike cyber-attacks on purely IT systems, which typically have economic consequences, a successful attack on rail OT can lead to physical events, threatening passenger lives and causing catastrophic environmental damage.4 The introduction of malware like Stuxnet demonstrated that code can cause physical destruction, and this threat has only grown as critical infrastructure has become more interconnected.5 The unique characteristics of rail systems—their vast geographic distribution, long asset lifecycles often measured in decades, and the deep integration of legacy and modern technologies—present unique cybersecurity challenges that generic IT security frameworks fail to address adequately.2

Therefore, an ad-hoc or reactive approach to cybersecurity is no longer tenable. A structured, comprehensive, and defensible framework is required to manage cyber risk throughout the entire lifecycle of a rail project, from initial concept through design, implementation, operation, and eventual decommissioning. This document provides such a framework, presenting an actionable template for two of the most critical cybersecurity artifacts for any rail project: the **Cybersecurity Case** and the **Cybersecurity Handover Plan**.

#### **1.2 Foundational Standards: IEC 62443 and CLC/TS 50701**

This framework is not built on abstract principles but is rigorously grounded in the consensus-based best practices codified in international and industry-specific standards. The two pillars of this template are the IEC 62443 series and the CENELEC CLC/TS 50701 technical specification.

* **IEC 62443: The Foundation for Industrial Cybersecurity:** The International Electrotechnical Commission (IEC) 62443 is a series of international standards that provide a comprehensive framework for securing Industrial Automation and Control Systems (IACS).7 It is recognized by the IEC as a "horizontal standard," meaning its principles are foundational and applicable across a wide range of industries, including power generation, manufacturing, and transportation.9 IEC 62443 addresses the entire IACS lifecycle, defining requirements not just for technology but also for the people, processes, and countermeasures necessary for robust security.4 It establishes the core vocabulary, concepts, and methodologies—such as risk assessment, defense-in-depth, and security levels—that form the bedrock of modern OT cybersecurity.  
* **CLC/TS 50701:2023: The Rail-Specific Application:** While IEC 62443 provides the essential foundation, the unique context of the railway sector requires specific guidance. The European Committee for Electrotechnical Standardization (CENELEC) developed CLC/TS 50701, "Railway applications – Cybersecurity," to adapt and apply the principles of IEC 62443 directly to the rail ecosystem.1 First published in 2021 and updated in 2023, TS 50701 is the world's first comprehensive cybersecurity specification tailored for rail.1 It addresses the specific challenges that IEC 62443 does not fully cover, such as the security of mixed, highly distributed systems that are characteristic of rail networks (e.g., trackside equipment, rolling stock, and central control centers).14 It provides rail-specific asset models, architectural examples, and crucially, integrates the cybersecurity lifecycle with the established rail safety lifecycle defined in EN 50126\.6  
* **The Path to IEC 63452: A Future-Proof Framework:** The global importance of TS 50701 is underscored by its role as the foundation for the forthcoming international standard, IEC 63452\.14 CENELEC has submitted TS 50701 to the IEC to be developed into a global standard, unifying cybersecurity management for railways worldwide.14 By adopting the framework presented in this document, which is based on the latest revision of TS 50701, rail projects are not only adhering to current best practices but are also "future-proofing" their cybersecurity programs against emerging international standards and regulations.

### **2.0 Core Principles of Rail Cybersecurity**

The template is built upon several core principles derived from the foundational standards. A deep understanding of these concepts is essential for the successful application of the framework.

#### **2.1 The Risk-Based Approach**

The central philosophy of both IEC 62443 and TS 50701 is the risk-based approach.4 This principle acknowledges that it is neither economically feasible nor operationally effective to attempt to protect all assets equally.4 Instead, security efforts and investments must be prioritized based on a systematic process of identifying, assessing, and treating risks to reduce them to a tolerable level.17 The framework mandates a formal risk assessment process to identify the most valuable and critical systems, understand the threats they face, and analyze their vulnerabilities. The outcome of this assessment directly drives the selection and strength of the security countermeasures, ensuring that resources are focused where they are needed most.

#### **2.2 Defense-in-Depth**

No single security control is infallible. The defense-in-depth strategy, a core tenet of IEC 62443, mandates the implementation of multiple, overlapping layers of security controls.3 This layered approach combines physical, technical, and procedural measures to protect critical assets from both external and internal threats.7 The objective is to ensure that the failure or circumvention of one layer of defense does not lead to a complete system compromise. In the rail context, this could mean combining a network firewall (technical), with locked equipment cabinets (physical), and a strict access control policy for maintenance personnel (procedural). TS 50701 provides a specific model (Figure 5\) that illustrates how these layers—from the component level up to the organizational policy level—work together to protect the rail system.19

#### **2.3 Zones and Conduits: The Cornerstone of IACS Architecture**

To effectively apply defense-in-depth and a risk-based approach to a complex system like a railway, the system must first be logically deconstructed. The Zones and Conduits model from IEC 62443 is the primary tool for this architectural segmentation.17

* A **Security Zone** is a logical or physical grouping of assets (e.g., devices, applications, servers) that share common security requirements.17 All assets within a zone are assumed to have the same level of security criticality.  
* A **Conduit** is the logical grouping of communication channels that connect two or more zones.17 Conduits must also have security requirements to protect the data flowing between zones.

By partitioning the entire rail system into zones and conduits, the security problem becomes manageable. Instead of securing hundreds or thousands of individual devices, the focus shifts to securing a smaller number of zones and the communication paths between them. This segmentation is critical for containing the impact of a cyber-attack; a breach in a lower-security zone (like a public-facing passenger information system) can be prevented from spreading to a high-security, safety-critical zone (like the signaling interlocking system).3

TS 50701 provides specific guidance and examples for applying this model to rail architecture.6 A typical rail transit project might be segmented as follows:

* **Zone 1: Signaling & Interlocking Zone:** Contains the safety-critical systems that control train movements, including interlocking controllers, track circuits, and point machines. This zone demands the highest level of integrity and availability.  
* **Zone 2: Rolling Stock Onboard Zone:** Encompasses all systems on the trains themselves, such as the Train Control and Management System (TCMS), onboard signaling equipment, passenger information displays, and CCTV. These assets are mobile and physically dispersed.  
* **Zone 3: Station Management Zone:** Includes systems within stations and buildings, such as SCADA for environmental controls, public address systems, digital signage, ticketing and fare collection systems, and physical access control.  
* **Zone 4: Operations Control Center (OCC) / Back Office Zone:** The central nervous system of the railway, containing the Automatic Train Supervision (ATS) systems, SCADA master stations, maintenance planning systems, and data historians.  
* **Conduits:** These are the communication networks that link the zones, for example:  
  * The trackside communications network (e.g., GSM-R, LTE-R) connecting the OCC to the rolling stock and signaling zones.  
  * The station Local Area Network (LAN) and Wide Area Network (WAN) connecting the Station Management Zone to the OCC Zone.  
  * The interface to the corporate IT network, which must be a highly controlled conduit.

#### **2.4 Security Levels (SLs): Quantifying Security Targets**

To make security requirements tangible and measurable, IEC 62443 introduces the concept of Security Levels (SLs). An SL defines the required resilience of a system, zone, or component against a specific class of threat.7 There are four defined levels:

* **SL 1: Protection against casual or coincidental violation.** This level protects against unintentional errors or non-malicious actions.7  
* **SL 2: Protection against intentional violation using simple means.** This level defends against attackers with low motivation and resources, using basic tools and techniques.7  
* **SL 3: Protection against intentional violation using sophisticated means.** This level protects against motivated adversaries with moderate resources and specific IACS skills, using advanced tools.8  
* **SL 4: Protection against intentional violation using advanced means with extended resources.** This level is designed to defend against nation-state-level attackers with extensive resources, who could cause a destructive impact.8

The process of securing a system involves determining a **Target Security Level (SL-T)** for each zone and conduit.17 This SL-T is not an arbitrary choice. The validity, cost, and effectiveness of the entire security design hinge on the fact that the SL-T is a direct and causal output of the risk assessment process. A project team cannot simply decide "we want SL3" without a defensible rationale. The formal risk assessment methodology, as defined in IEC 62443-3-2 and TS 50701 Clause 7, analyzes the threats, vulnerabilities, and potential impacts (including safety, operational, and financial consequences) for a given zone.17 The output of this analysis is a determination of the tolerable level of risk that the Asset Owner is willing to accept for that zone. This tolerable risk level is then mapped to a specific SL-T. For instance, a zone where a compromise could lead to catastrophic safety consequences, such as the Signaling & Interlocking Zone, will naturally require a high SL-T (e.g., SL3 or SL4) to reduce the inherent risk to a tolerable level. This direct linkage ensures that the security controls implemented are commensurate with the actual risk, preventing both over-engineering and under-protection.

### **3.0 The Rail Cybersecurity Lifecycle (The V-Model Adaptation)**

To provide a logical and auditable structure, this template is organized according to the systems engineering "V-model." This model is a well-established standard in the rail industry for managing the safety lifecycle, as defined in EN 50126\.16 CLC/TS 50701 explicitly adapts this familiar model for cybersecurity, creating a parallel and synchronized process that ensures security is considered at every stage of the project, not as an afterthought.6

The V-model illustrates the progression of the project lifecycle:

* The **left side of the V** represents the decomposition of requirements, moving from high-level concepts down to detailed design and specification. This corresponds to the Concept, Risk Assessment, and Design phases of the template.  
* The **bottom of the V** represents the implementation and building of the system.  
* The **right side of the V** represents the integration, testing, and validation of the system, moving from individual components back up to the fully integrated system. This corresponds to the Verification, Validation, and Handover phases.

Each step on the right side of the V verifies or validates the corresponding step on the left side. For example, the System Validation phase (right side) tests against the overall System Requirements defined in the Concept phase (left side). This structure ensures traceability and provides a clear, logical flow for building the evidence required for the final Cybersecurity Case.

## **Part II: The Project Ecosystem: Roles, Responsibilities, and Interactions**

### **4.0 Defining Stakeholder Roles in Accordance with IEC 62443**

A successful cybersecurity program requires clear definitions of roles and responsibilities among all parties involved. IEC 62443 defines several principal roles that are critical to the security lifecycle of an IACS.9 This framework adopts these definitions to ensure a common understanding and clear lines of accountability.

* **Asset Owner:** The organization that is ultimately accountable for and legally owns the rail system (IACS). This is typically the government transit authority or private rail company. The Asset Owner is responsible for establishing the organization's overall risk tolerance, approving the target security levels, and formally accepting the final system at handover.25  
* **Operator:** The organization responsible for the day-to-day operation and maintenance of the rail system. While often the same entity as the Asset Owner, this can be a separate contractor. The Operator is responsible for executing the operational security procedures (e.g., patch management, incident response) and maintaining the system's security posture throughout its operational life.27  
* **System Integrator (Integration Service Provider):** The primary contractor or organization responsible for the integration activities of the automation solution. This includes the design, installation, configuration, testing, commissioning, and handover of the complete system to the Asset Owner.25 The System Integrator is the primary party responsible for developing and delivering the Cybersecurity Case and executing the Handover Plan. Their capabilities and processes are governed by standards like IEC 62443-2-4.30  
* **Product Supplier:** The organization that manufactures and supports the individual hardware and/or software products that are integrated into the overall system. This includes vendors of PLCs, network switches, SCADA software, HMIs, and other IACS components.25 Product Suppliers are responsible for following a secure development lifecycle (as defined in IEC 62443-4-1) and building components with the technical security capabilities required by IEC 62443-4-2.25

### **5.0 The Rail Cybersecurity RACI Matrix**

Defining roles is the first step; assigning specific responsibilities for every critical activity is the second, and arguably more important, step. The RACI (Responsible, Accountable, Consulted, Informed) matrix is the tool used to achieve this clarity. Within this framework, the RACI matrix is elevated from a simple project management chart to a core governance and liability management document.

A cybersecurity incident is frequently the result of a process failure. For example, a known vulnerability in a signaling controller is exploited because a security patch was never applied. In the subsequent investigation, the crucial question will be: who was responsible for this failure? A vague project charter stating "the project will manage patches" is insufficient and creates ambiguity that leads to inaction. A detailed RACI matrix, established and agreed upon at the project's outset, eliminates this ambiguity. It would specify, for instance, that the Product Supplier is **Responsible** for developing and providing the patch, the System Integrator is **Responsible** for testing the patch within the integrated rail environment to ensure it does not negatively impact safety or operations, and the Operator is **Accountable** for the final decision to deploy the patch and **Responsible** for its physical deployment. This level of granularity transforms the RACI into a contractually and legally binding definition of responsibility, providing a clear framework for managing liability and ensuring that critical security tasks do not fall through the cracks.

The following table provides a template for a detailed RACI matrix covering the key activities and deliverables described in this framework. This matrix should be reviewed, customized, and formally agreed upon by all stakeholders during the project's initiation phase.

**Table 1: Rail Project Cybersecurity RACI Matrix**

| Activity / Deliverable | Asset Owner | Operator | System Integrator | Product Supplier |
| :---- | :---- | :---- | :---- | :---- |
| **Phase 1: Concept & System Definition** |  |  |  |  |
| Define and Approve Cybersecurity Management Plan (CSMP) | A | C | R | I |
| Define and Approve System under Consideration (SuC) Scope | A | C | R | I |
| Identify and Approve Essential Functions | A | R | C | I |
| **Phase 2: Risk Assessment & SL Targeting** |  |  |  |  |
| Develop and Maintain System Asset Inventory | C | I | R | C |
| Define and Approve System Zoning & Conduit Architecture | A | C | R | I |
| Conduct Detailed Risk Assessment | C | C | R | C |
| Define and Approve Organizational Risk Tolerance | A | R | C | I |
| Determine and Approve Target Security Levels (SL-T) | A | C | R | I |
| **Phase 3: Cybersecurity Design & Requirements** |  |  |  |  |
| Develop Cybersecurity Requirements Specification (CSRS) | A | C | R | C |
| Apportion Requirements to Subsystems/Components | I | I | R | C |
| Develop and Approve Compensating Countermeasures | A | C | R | C |
| Maintain Cybersecurity Requirements Traceability Matrix (CRTM) | I | I | R | I |
| **Phase 4 & 5: Implementation, V\&V, and Acceptance** |  |  |  |  |
| Develop Products Meeting SL-Capabilities (per IEC 62443-4-2) | I | I | C | R |
| Implement and Configure Security Controls | I | C | R | C |
| Develop and Execute Cybersecurity Verification Plan | I | C | R | C |
| Develop and Execute Cybersecurity Validation Plan | C | C | R | I |
| Develop and Submit Final Cybersecurity Case | C | C | R | I |
| Review and Formally Accept Cybersecurity Case | A | R | I | I |
| **Phase 5: Handover** |  |  |  |  |
| Develop Cybersecurity Handover Plan | C | A | R | I |
| Execute Operator Training on Security Procedures | I | R | A | I |
| Transfer Final As-Built Documentation | C | R | A | I |
| Transfer Security Tools, Credentials, and Keys | I | R | A | I |
| Formally Accept Security-related Application Conditions (SecRACs) | I | A | R | I |
| Execute Final System Acceptance Sign-off | A | R | I | I |
| **Phase 6: Operations & Maintenance (Post-Handover)** |  |  |  |  |
| Execute Vulnerability Management Process | I | R | C | C |
| Execute Security Patch Management Process | I | A | C | R |
| Execute Incident Response Plan | C | R | C | C |
| Execute Backup and Recovery Procedures | I | R | C | I |
| Perform Continuous Security Monitoring | I | R | C | I |
| Conduct Periodic Cybersecurity Audits | A | R | I | I |

*Legend: R \= Responsible, A \= Accountable, C \= Consulted, I \= Informed*

## **Part III: The Integrated Cybersecurity Case & Handover Template**

This part constitutes the core, actionable template. It is designed to be a living document, progressively completed by the project team as it moves through the cybersecurity lifecycle. Each section represents a key phase and requires the generation of specific deliverables and evidence. The culmination of this process is the assembly of the formal Cybersecurity Case and the execution of the Cybersecurity Handover Plan.

### **6.0 Phase 1: Concept & System Definition (Template Section)**

*This phase establishes the foundational scope and strategy for the project's cybersecurity program.*

#### **6.1 Cybersecurity Management Plan (CSMP)**

* **Actionable Task:** Develop the CSMP, which serves as the master plan for cybersecurity throughout the project. This document formalizes the organization's commitment to security and outlines the governance, policies, procedures, and resources that will be applied. It is a key requirement of IEC 62443-2-1 for establishing a security program.4  
* **Content to Include:**  
  * **Project Cybersecurity Policy:** A high-level statement of intent and commitment from senior management.  
  * **Scope and Objectives:** A clear definition of what the CSMP covers and the security goals it aims to achieve.  
  * **Roles and Responsibilities:** Reference the project's detailed RACI matrix.  
  * **Risk Management Strategy:** The methodology for performing risk assessments (aligned with IEC 62443-3-2) and the organization's risk acceptance criteria.  
  * **Applicable Standards and Regulations:** A list of all legal, regulatory, and standards-based requirements the project must adhere to.  
  * **Lifecycle Management:** A description of how cybersecurity will be managed through each phase of the project, from concept to decommissioning.  
  * **Resource Allocation:** An outline of the budget, staffing, and tools dedicated to cybersecurity activities.

#### **6.2 System under Consideration (SuC) Definition**

* **Actionable Task:** Provide a clear and unambiguous definition of the boundaries of the system to be secured. This is the foundational first step of the risk assessment process as mandated by CLC/TS 50701, Clause 6.2.21  
* **Content to Include:**  
  * **Scope Statement:** A narrative description defining what is in scope (e.g., "The complete signaling system for the new line, including trackside equipment, onboard controllers, and the central interlocking at the OCC") and what is explicitly out of scope (e.g., "The corporate IT network and existing legacy lines").  
  * **High-Level Architecture Diagrams:** Include both physical and logical diagrams that illustrate the major components of the SuC and their interconnections. These should reference the railway architecture models provided in TS 50701\.19  
  * **Key Interfaces:** Identify and describe all major data interfaces between the SuC and external systems (e.g., interface to the power utility SCADA, connection to the public internet for remote maintenance).

#### **6.3 Identification of Essential Functions**

* **Actionable Task:** List and describe the critical functions that the SuC must perform to meet its fundamental operational and safety objectives. This list is a primary input for the risk assessment, as the impact of a cyber-attack is measured by its effect on these functions.21  
* **Content to Include:** A table listing each essential function, its description, and its criticality (e.g., Safety-Critical, Mission-Critical, Business-Supporting).  
  * *Example Essential Functions:*  
    * "Ensure safe train separation and routing via the interlocking system." (Safety-Critical)  
    * "Provide continuous and reliable traction power to all trains." (Mission-Critical)  
    * "Display accurate and timely train arrival information to passengers." (Business-Supporting)  
    * "Securely process and record all fare collection transactions." (Business-Supporting)

### **7.0 Phase 2: Risk Assessment & Security Level Targeting (Template Section)**

*This phase systematically analyzes risks to the SuC and determines the required level of security for its various parts.*

#### **7.1 High-Level Risk Assessment**

* **Actionable Task:** Conduct an initial, high-level risk assessment to identify the most significant threats and potential high-impact scenarios. This is a preliminary step that helps to focus and prioritize the more resource-intensive detailed risk assessment.23  
* **Content to Include:** A summary of major threat scenarios (e.g., ransomware attack on the OCC, denial-of-service against the communication network, unauthorized access to signaling equipment) and a qualitative assessment of their potential impact on the essential functions identified in the previous phase.

#### **7.2 Asset Inventory and Partitioning into Zones & Conduits**

* **Actionable Task:** Create a comprehensive inventory of all cyber-relevant assets within the SuC and group them into logical Security Zones. This is a prerequisite for a detailed risk assessment; it is impossible to protect assets that are not known to exist. The grouping into zones simplifies the application of consistent security policies and controls.17  
* **Deliverable:** A formal System Asset and Zoning Register. This register serves as the definitive, centralized repository of all assets and their architectural context.

**Table 2: System Asset and Zoning Register (Example)**

| Asset ID | Asset Type | Vendor / Model | Location / Train ID | Function | Assigned Security Zone |
| :---- | :---- | :---- | :---- | :---- | :---- |
| PLC-IXL-01 | PLC | Siemens S7-400 | OCC Room 1 | Central Interlocking Processor | Signaling & Interlocking Zone |
| NWS-TS-23 | Switch | Cisco IE-3000 | Trackside Cabinet @ MP 5.3 | Signaling Network Switch | Signaling & Interlocking Zone |
| HMI-TCMS-C1-01 | HMI | Wabtec | Car 1, Train 05 | Driver's TCMS Display | Rolling Stock Onboard Zone |
| SVR-PIS-STN-A | Server | Dell PowerEdge | Station A Comms Room | Passenger Information Server | Station Management Zone |
| FGT-OCC-01 | Firewall | Fortinet FG-200F | OCC Room 2 | OCC Perimeter Firewall | Operations Control Center Zone |

* **Actionable Task:** Following the asset grouping, create architecture diagrams that explicitly show the defined zones and the conduits that connect them. For each conduit, describe the type of data that flows through it and its purpose.

#### **7.3 Detailed Risk Assessment (per IEC 62443-3-2 & TS 50701 Clause 7\)**

* **Actionable Task:** For each Zone and Conduit defined in the previous step, conduct a formal, detailed risk assessment. This process must be systematic and documented.  
* **Process Steps to Document for Each Zone/Conduit:**  
  1. **Threat Identification:** List credible threats applicable to the zone. Utilize standard threat catalogues (e.g., from ENISA, NIST) and rail-specific threat intelligence.24 Threats should consider various actors, from insiders to sophisticated external attackers.  
  2. **Vulnerability Identification:** Identify potential weaknesses in the systems, components, configurations, and processes within the zone that could be exploited by the identified threats.21  
  3. **Impact Assessment:** Evaluate and rate the potential consequences if a threat successfully exploits a vulnerability. The impact analysis must cover safety, operational availability, financial loss, and regulatory compliance.  
  4. **Likelihood Assessment:** Estimate and rate the probability of a specific threat successfully exploiting a vulnerability.  
  5. **Risk Determination:** Combine the impact and likelihood ratings (e.g., using a risk matrix as described in TS 50701 Annex E) to determine the overall level of risk for each threat/vulnerability pair.19

#### **7.4 Determination of Target Security Levels (SL-T)**

* **Actionable Task:** Based on the results of the detailed risk assessment, determine the Target Security Level (SL-T) required for each zone and conduit. The SL-T is the level of security (SL 1-4) necessary to mitigate the identified risks to a level that is considered acceptable by the Asset Owner.21  
* **Content to Include:** A summary table listing each Zone and Conduit, its highest identified risk level (from the risk assessment), and the assigned SL-T. A justification must be provided for each SL-T, linking it directly back to the risk it is intended to mitigate.

### **8.0 Phase 3: Cybersecurity Design & Requirements Specification (Template Section)**

*This phase translates the abstract SL-T into a concrete set of technical and procedural security requirements that will guide the system's design and implementation.*

#### **8.1 Cybersecurity Requirements Specification (CSRS)**

* **Actionable Task:** Develop the CSRS document. This involves selecting the specific security requirements (SRs) and requirement enhancements (REs) from the comprehensive catalogues provided in IEC 62443-3-3 that correspond to the SL-T assigned to each zone and conduit.21  
* **Content to Include:** A detailed list of security requirements for each zone and conduit, organized by the seven Foundational Requirements (FRs) of IEC 62443:  
  * FR1: Identification and Authentication Control (IAC)  
  * FR2: Use Control (UC)  
  * FR3: System Integrity (SI)  
  * FR4: Data Confidentiality (DC)  
  * FR5: Restricted Data Flow (RDF)  
  * FR6: Timely Response to Events (TRE)  
  * FR7: Resource Availability (RA)

#### **8.2 Apportionment of Requirements**

* **Actionable Task:** Allocate the system-level requirements defined in the CSRS down to the specific subsystems and components that will implement them. This critical step ensures that every requirement has a clear owner and can be traced through the design and testing phases.  
* **Deliverable:** A Cybersecurity Requirements Traceability Matrix (CRTM). This matrix is the central backbone of the entire assurance process. It creates an auditable link from the initial risks all the way through to the final test results, providing the core evidence for the Cybersecurity Case.

**Table 3: Cybersecurity Requirements Traceability Matrix (CRTM) (Example)**

| Risk ID | Zone / Conduit | SL-T | Requirement ID (IEC 62443-3-3) | Requirement Description | Allocated Subsystem / Component | Verification Method | Verification Result |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| R-012 | Signaling Zone | SL3 | SR 1.1 \- Human User Identification and Authentication | The system shall uniquely identify and authenticate all human users. | Central Interlocking (PLC-IXL-01), Maintenance Laptop | Test Case V-1.1.1: Attempt login with valid/invalid credentials. | Pass |
| R-025 | Rolling Stock Zone | SL2 | SR 3.1 \- Communication Integrity | The system shall ensure the integrity of transmitted information. | Onboard TCMS, Trackside Radio Block Centre | Test Case V-3.1.2: Packet integrity check during simulated data transmission. | Pass |
| R-031 | Conduit: Station to OCC | SL2 | SR 5.1 \- Network Segmentation | The conduit shall be logically and/or physically separated from other networks. | OCC Firewall (FGT-OCC-01), Station Switch Config | Design Review DR-5.1.1: Verify firewall rule base. | Pass |

#### **8.3 Compensating Countermeasures**

* **Actionable Task:** For any security requirement that cannot be met directly by a component, document a compensating countermeasure. This is particularly important for projects involving legacy systems, which may not support modern security features like encryption or strong authentication. TS 50701 Annex B provides specific guidance on handling legacy systems.6  
* **Content to Include:** For each instance, document:  
  * The specific requirement that cannot be met.  
  * The reason for non-compliance (e.g., "Legacy PLC does not support role-based access control").  
  * The detailed description of the compensating countermeasure(s) being implemented (e.g., "PLC is placed in a highly restricted network segment, all access is proxied through a jump host with multi-factor authentication, and all network traffic to the PLC is monitored by an IDS").  
  * A risk analysis demonstrating that the compensating control reduces the associated risk to an acceptable level.

### **9.0 Phase 4: Implementation, Integration, and Verification (Template Section)**

*This phase involves building the system according to the design and then systematically testing to ensure that each individual security requirement has been implemented correctly.*

#### **9.1 Implementation Evidence**

* **Actionable Task:** As the system is built and configured, collect and archive evidence of implementation for each requirement listed in the CRTM.  
* **Types of Evidence:** Configuration files from firewalls and switches, screenshots of user access control settings, software development lifecycle documents from suppliers (demonstrating compliance with IEC 62443-4-1), hardware datasheets, and physical security design drawings.

#### **9.2 Cybersecurity Verification Plan & Report**

* **Actionable Task:** Develop a formal Cybersecurity Verification Plan that details the methodology for testing each security requirement. Verification is the process of confirming that the system was "built right."  
* **Content of Plan:** For each requirement in the CRTM, specify the verification method (e.g., Design Review, Code Inspection, Functional Test, Penetration Test) and the detailed test procedure.  
* **Actionable Task:** Execute the Verification Plan and produce a Cybersecurity Verification Report. This report documents the results of all tests. The "Verification Result" column in the CRTM must be updated with the outcome (e.g., Pass, Fail, Pass with Deviations). Any failures must be tracked and remediated.

### **10.0 Phase 5: System Validation, Acceptance, and Handover (Template Section)**

*This phase focuses on testing the fully integrated system to ensure it meets the overall security objectives in its intended operational context, culminating in the formal acceptance and handover to the Operator.*

#### **10.1 Cybersecurity Validation Plan & Report**

* **Actionable Task:** Develop a Cybersecurity Validation Plan. Validation is the process of confirming that the "right system was built"—that is, the system as a whole is secure and effective in its operational environment.  
* **Content of Plan:** The plan should focus on holistic, scenario-based testing rather than individual requirement checks. This typically includes:  
  * **Penetration Testing:** Simulating attacks by ethical hackers to identify exploitable vulnerabilities in the integrated system.  
  * **Operational Scenario Testing:** Testing the system's response to simulated security incidents (e.g., loss of communication, malware detection) to ensure it fails in a safe and predictable manner.  
  * **Use Case Testing:** Verifying that security controls do not unduly impede normal operational and maintenance tasks.  
* **Actionable Task:** Execute the Validation Plan and produce a Cybersecurity Validation Report documenting the findings, vulnerabilities discovered, and remediation actions taken.

#### **10.2 The Cybersecurity Case (Summary Deliverable)**

The Cybersecurity Case is the single most important deliverable of the project's cybersecurity lifecycle. It is not simply a collection of documents; it is a structured, coherent, and defensible *argument*, supported by evidence, that the cybersecurity risks to the rail system have been identified, assessed, and mitigated to a level acceptable to the Asset Owner.6 This concept is directly inspired by the well-understood Safety Case from the rail safety domain, providing a familiar structure for senior stakeholders and regulators.

The argument is built progressively throughout the project, and this section of the template serves to synthesize and summarize that evidence into a final, compelling narrative.

* **Actionable Task:** Assemble the Cybersecurity Case document. This document does not generate new content but rather references and summarizes the evidence from all preceding phases to make the final argument for system acceptance.  
* **Structure of the Cybersecurity Case:**  
  1. **Introduction:** State the purpose of the case, the scope of the SuC it covers, and the overall claim (e.g., "The SuC for the new line is adequately secure for operational service, having met its defined SL-Ts").  
  2. **System Definition Summary:** Reference the full SuC Definition document (Section 6.2).  
  3. **Risk Management Summary:** Summarize the risk assessment process and its key findings. Reference the full Detailed Risk Assessment report (Section 7.3) and the SL-T determination (Section 7.4).  
  4. **Security Requirements Summary:** Summarize the key security requirements derived from the risk assessment. Reference the full CSRS (Section 8.1) and the CRTM (Section 8.2).  
  5. **Assurance Evidence Summary:** This is the core of the argument. Summarize the results of the verification and validation activities. Reference the Verification Report (Section 9.2) and Validation Report (Section 10.1) as the primary evidence. The CRTM is the key exhibit showing full traceability.  
  6. **Residual Risk Statement:** Explicitly list and describe any risks that were not fully mitigated and have been accepted by the Asset Owner.  
  7. **Security-related Application Conditions (SecRACs):** List all the conditions and assumptions upon which the Cybersecurity Case depends. These are the critical operational and maintenance tasks that the Operator *must* perform for the security case to remain valid.6  
  8. **Conclusion:** Reiterate the claim and make a formal recommendation for system acceptance.

#### **10.3 The Cybersecurity Handover Plan (Detailed Sub-Section)**

A system can be designed and built to be perfectly secure, only to be rendered vulnerable on the first day of operation due to an incomplete or poorly executed handover. The handover process is not merely a contractual milestone; it is a critical security control designed to mitigate the risk of knowledge gaps between the System Integrator who built the system and the Operator who must maintain its security for decades.35 The requirements for the System Integrator (as a service provider) during this phase are guided by standards like IEC 62443-2-4.26 This section of the template provides a structured plan for a comprehensive handover.

* **Actionable Task:** Develop and execute the Cybersecurity Handover Plan, which consists of several key sub-deliverables requiring formal sign-off.  
* **Handover Sub-Deliverables (Fillable Sub-Templates):**  
  * **10.3.1 Final Documentation Transfer:** A checklist of all required documentation to be transferred to the Operator. Each item must be formally acknowledged as received.  
    * *Checklist Items:* Final as-built physical and logical network diagrams; all device configuration guides; final Risk Assessment Report; final CSRS and CRTM; all Verification and Validation Reports; the final signed-off Cybersecurity Case; all operational plans from Section 11\.  
  * **10.3.2 Transfer of Security Tools & Credentials:** A formal, secure process for transferring all administrative accounts, passwords, private encryption keys, and software licenses for security tools (e.g., IDS, SIEM). This must include a documented plan for changing all default passwords and removing or disabling all temporary accounts used by the System Integrator and Product Suppliers during commissioning.35  
  * **10.3.3 Operational Readiness Training Plan:** A detailed training plan and schedule for the Operator's technical and operational staff.  
    * *Content:* Curriculum covering the system architecture, security controls, and all operational security procedures (incident response, patch management, backup/recovery).  
    * *Deliverable:* A training register signed by all attendees to provide an audit trail of completed training.  
  * **10.3.4 Formal Acceptance of SecRACs:** A table listing every SecRAC from the Cybersecurity Case. The designated representative from the Operator must formally sign against each one, acknowledging their understanding of the condition and accepting responsibility for its ongoing implementation.  
  * **10.3.5 Formal System Acceptance:** The final deliverable of the project phase. A formal sign-off sheet where the authorized representative of the Asset Owner, based on their review and acceptance of the Cybersecurity Case and the successful completion of the handover activities, formally accepts the system for operational service. This act officially transfers primary responsibility for the system's security to the Operator.

### **11.0 Phase 6: Operations, Maintenance, and Continuous Improvement (Template Section)**

*This section contains the operational plans and procedures developed by the System Integrator during the project. These documents are a key part of the handover package and provide the Operator with the necessary guidance to maintain the system's security posture over its lifecycle.*

#### **11.1 Vulnerability Management Plan**

* **Actionable Task:** Provide a detailed plan defining the process for proactively identifying, assessing, and tracking new vulnerabilities that may affect the operational system. This is a requirement of TS 50701, Clause 10.2.21  
* **Content to Include:** Procedures for subscribing to vendor security advisories, conducting periodic vulnerability scans (where operationally safe), and using a formal system to track the status of all identified vulnerabilities.

#### **11.2 Security Patch Management Plan**

* **Actionable Task:** Detail the end-to-end process for managing security patches. This is a critical and complex process in an OT environment where availability and safety are paramount. The plan must align with TS 50701, Clause 10.3.21  
* **Content to Include:**  
  * **Patch Reception and Evaluation:** How patches are received from suppliers and assessed for applicability and criticality.  
  * **Testing Procedures:** A mandatory process for testing every patch in a non-production environment (e.g., a lab or simulator) to ensure it does not adversely affect system functionality or safety before deployment.  
  * **Deployment Procedures:** Step-by-step instructions for deploying approved patches, including rollback plans in case of failure.  
  * **Scheduling and Coordination:** Rules for scheduling patching activities to minimize disruption to rail operations.

#### **11.3 Incident Response Plan**

* **Actionable Task:** Provide a comprehensive, step-by-step plan for responding to cybersecurity incidents. The plan should enable the Operator to effectively detect, analyze, contain, eradicate, and recover from an attack.12  
* **Content to Include:**  
  * **Roles and Responsibilities:** A clear definition of the Cyber Incident Response Team (CIRT).  
  * **Incident Classification:** A methodology for categorizing incidents based on severity.  
  * **Response Playbooks:** Specific checklists and procedures for common incident types (e.g., malware infection, unauthorized access, denial-of-service).  
  * **Communication Plan:** Procedures for notifying internal stakeholders, regulators, and potentially law enforcement.

#### **11.4 Backup and Recovery Plan**

* **Actionable Task:** Document the procedures for performing regular backups of all critical systems and for restoring service from those backups in the event of a system failure or destructive cyber-attack.  
* **Content to Include:** Backup schedules, storage locations (including off-site), data retention policies, and detailed, step-by-step procedures for system restoration. The plan must also include a schedule for periodically testing the recovery procedures to ensure the backups are viable.

#### **11.5 Continuous Monitoring Strategy**

* **Actionable Task:** Outline the strategy and tools for the ongoing monitoring of the rail system's security posture. This is essential for detecting anomalies, identifying potential threats, and ensuring that security controls remain effective over time. The maturity of this strategy should align with the Operator's target Cybersecurity Maturity Level.7  
* **Content to Include:** A description of the security monitoring tools to be used (e.g., Security Information and Event Management \- SIEM, Intrusion Detection Systems \- IDS), the key events and logs to be collected and analyzed, and the procedures for reviewing alerts and reports.

### **Conclusions**

The increasing digitalization of rail transit systems offers immense benefits but also introduces significant cybersecurity risks that threaten public safety and national security. Addressing these risks requires a departure from ad-hoc security measures and the adoption of a structured, lifecycle-based framework grounded in internationally recognized standards.

This report has provided a comprehensive and actionable template for developing a project's Cybersecurity Case and executing its Handover Plan, based on the foundational principles of IEC 62443 and the rail-specific guidance of CLC/TS 50701\. By adhering to this framework, rail projects can ensure that:

1. **Cybersecurity is Risk-Driven:** Security investments and controls are directly and justifiably linked to a systematic assessment of risk, ensuring resources are applied effectively and efficiently.  
2. **Accountability is Unambiguous:** The use of clearly defined roles and a detailed RACI matrix transforms responsibility from a vague concept into a contractually enforceable reality, closing the gaps where security failures often occur.  
3. **Security is Verifiable and Defensible:** The V-model lifecycle and the development of the Cybersecurity Case create a structured, evidence-based argument that the system is secure for its intended purpose, providing assurance to Asset Owners, operators, and regulators.  
4. **Operational Resilience is Maintained:** The detailed Handover Plan acts as a critical control, ensuring that the knowledge, tools, and responsibilities required to maintain the system's security posture are effectively transferred from the System Integrator to the Operator.

Ultimately, the adoption of this framework is not merely a compliance exercise. It is a strategic imperative for any rail organization committed to delivering safe, reliable, and secure transportation in an increasingly interconnected world. By embedding cybersecurity into the very fabric of the project lifecycle, from concept to operations, rail stakeholders can build the resilient systems necessary to meet the challenges of tomorrow.

#### **Works cited**

1. A deep dive into CENELEC TS 50701 for railway cybersecurity \- Shieldworkz, accessed October 28, 2025, [https://shieldworkz.com/blogs/a-deep-dive-into-cenelec-ts-50701-for-railway-cybersecurity](https://shieldworkz.com/blogs/a-deep-dive-into-cenelec-ts-50701-for-railway-cybersecurity)  
2. Adapting railway sector to repel cyber threats: a critical analysis, accessed October 28, 2025, [https://wlv.openrepository.com/server/api/core/bitstreams/4d3848a2-f293-47fd-b03f-4521225d2753/content](https://wlv.openrepository.com/server/api/core/bitstreams/4d3848a2-f293-47fd-b03f-4521225d2753/content)  
3. Case Studies: IEC 62443 Implementation in Industrial Plants \- InstruNexus, accessed October 28, 2025, [https://instrunexus.com/case-studies-iec-62443-implementation-in-industrial-plants/](https://instrunexus.com/case-studies-iec-62443-implementation-in-industrial-plants/)  
4. Understanding IEC 62443, accessed October 28, 2025, [https://www.iec.ch/blog/understanding-iec-62443](https://www.iec.ch/blog/understanding-iec-62443)  
5. CYBERSECURITY IN RAIL: IMPLICATIONS FOR OPERATIONAL SAFETY \- Scientific and practical cyber security journal, accessed October 28, 2025, [https://journal.scsa.ge/wp-content/uploads/2025/07/0084\_cybersecurity-in-rail-implications-for-operational-safety.pdf](https://journal.scsa.ge/wp-content/uploads/2025/07/0084_cybersecurity-in-rail-implications-for-operational-safety.pdf)  
6. Navigating TS 50701: Unpacking the Impact of the Cybersecurity Standard for Rail \- Cylus, accessed October 28, 2025, [https://www.cylus.com/post/navigating-ts-50701-unpacking-the-impact-of-the-cybersecurity-standard-for-rail](https://www.cylus.com/post/navigating-ts-50701-unpacking-the-impact-of-the-cybersecurity-standard-for-rail)  
7. What Is IEC 62443? Definition, Breakdown & Methodology \- Zscaler, accessed October 28, 2025, [https://www.zscaler.com/zpedia/what-is-iec-62443](https://www.zscaler.com/zpedia/what-is-iec-62443)  
8. IEC 62443 Standard: Enhancing Cybersecurity for Industrial Automation and Control Systems | Fortinet, accessed October 28, 2025, [https://www.fortinet.com/resources/cyberglossary/iec-62443](https://www.fortinet.com/resources/cyberglossary/iec-62443)  
9. IEC 62443 \- Wikipedia, accessed October 28, 2025, [https://en.wikipedia.org/wiki/IEC\_62443](https://en.wikipedia.org/wiki/IEC_62443)  
10. ANSI Standards Boost Business Case Study: Cybersecurity and Automation, accessed October 28, 2025, [https://www.ansi.org/impact-of-standards/standards-boost-business/cybersecurity-industrial-automation](https://www.ansi.org/impact-of-standards/standards-boost-business/cybersecurity-industrial-automation)  
11. ISA/IEC 62443 Series of Standards | ISAGCA, accessed October 28, 2025, [https://isagca.org/isa-iec-62443-standards](https://isagca.org/isa-iec-62443-standards)  
12. Helping Rolling Stock Manufacturers & Train Operators Align with TS 50701 \- RazorSecure, accessed October 28, 2025, [https://www.razorsecure.com/post/rail-cybersecurity-ts50701](https://www.razorsecure.com/post/rail-cybersecurity-ts50701)  
13. Railway Infrastructure Cybersecurity: An Overview \- Academic Conferences International, accessed October 28, 2025, [https://papers.academic-conferences.org/index.php/eccws/article/download/2296/2191/8601](https://papers.academic-conferences.org/index.php/eccws/article/download/2296/2191/8601)  
14. Towards the first railway cybersecurity international standard \- why standards are important for secure railways | Alstom, accessed October 28, 2025, [https://www.alstom.com/press-releases-news/2024/3/towards-first-railway-cybersecurity-international-standard-why-standards-are-important-secure-railways](https://www.alstom.com/press-releases-news/2024/3/towards-first-railway-cybersecurity-international-standard-why-standards-are-important-secure-railways)  
15. A major step for railways cybersecurity: the new CLC/TS 50701 \- CEN-CENELEC, accessed October 28, 2025, [https://www.cencenelec.eu/news-events/news/2021/eninthespotlight/2021-06-10-new-clc-ts-50701-railways-cybersecurity/](https://www.cencenelec.eu/news-events/news/2021/eninthespotlight/2021-06-10-new-clc-ts-50701-railways-cybersecurity/)  
16. CENELEC Christian Schlehuber \- TS 50701 Introduction | PDF | Risk Management \- Scribd, accessed October 28, 2025, [https://www.scribd.com/document/829947298/CENELEC-Christian-Schlehuber-TS-50701-Introduction](https://www.scribd.com/document/829947298/CENELEC-Christian-Schlehuber-TS-50701-Introduction)  
17. Understanding ISA/IEC 62443: A Guide for OT Security Teams \- Dragos, accessed October 28, 2025, [https://www.dragos.com/blog/isa-iec-62443-concepts](https://www.dragos.com/blog/isa-iec-62443-concepts)  
18. Rail Cybersecurity Compliance & Regulations \- Cervello.Security, accessed October 28, 2025, [https://cervello.security/compliance/](https://cervello.security/compliance/)  
19. SIST-TS CLC/TS 50701:2024 \- iTeh Standards, accessed October 28, 2025, [https://cdn.standards.iteh.ai/samples/74651/a9c8ddd211c3488dad4994676afa70c5/SIST-TS-CLC-TS-50701-2024.pdf](https://cdn.standards.iteh.ai/samples/74651/a9c8ddd211c3488dad4994676afa70c5/SIST-TS-CLC-TS-50701-2024.pdf)  
20. Using IEC 62443 to Secure OT Systems: The Ultimate Guide \- Verve Industrial, accessed October 28, 2025, [https://verveindustrial.com/resources/blog/the-ultimate-guide-to-protecting-ot-systems-with-iec-62443](https://verveindustrial.com/resources/blog/the-ultimate-guide-to-protecting-ot-systems-with-iec-62443)  
21. CLC/TS 50701:2023 \- Railway applications \- Cybersecurity \- iTeh Standards, accessed October 28, 2025, [https://standards.iteh.ai/catalog/standards/clc/db257ea9-8ba0-4f4c-a791-df34a6030541/clc-ts-50701-2023](https://standards.iteh.ai/catalog/standards/clc/db257ea9-8ba0-4f4c-a791-df34a6030541/clc-ts-50701-2023)  
22. IEC 62443: Ultimate OT Security Guide | Rockwell Automation | US, accessed October 28, 2025, [https://www.rockwellautomation.com/en-us/company/news/blogs/iec-62443-security-guide.html](https://www.rockwellautomation.com/en-us/company/news/blogs/iec-62443-security-guide.html)  
23. Effective ICS Cybersecurity Using the IEC 62443 Standard \- Fortinet, accessed October 28, 2025, [https://www.fortinet.com/content/dam/fortinet/assets/analyst-reports/report-sans-cybersecurity-iec-62443.pdf](https://www.fortinet.com/content/dam/fortinet/assets/analyst-reports/report-sans-cybersecurity-iec-62443.pdf)  
24. Hands-On CLC/TS 50701 (Railway applications – CyberSecurity), accessed October 28, 2025, [https://www.era.europa.eu/system/files/2023-12/05%20Standards%20-%2002%20CENELEC%20Christian%20Schlehuber.pdf?t=1720627291](https://www.era.europa.eu/system/files/2023-12/05%20Standards%20-%2002%20CENELEC%20Christian%20Schlehuber.pdf?t=1720627291)  
25. Structure of IEC 62443 \- BYHON, accessed October 28, 2025, [https://www.byhon.it/structure-of-iec-62443/](https://www.byhon.it/structure-of-iec-62443/)  
26. Industrial Automation and Control System: Principal Roles and Responsibilities \- ISA Global Cybersecurity Alliance, accessed October 28, 2025, [https://gca.isa.org/hubfs/21-29%20-%20ISAGCA/ISAGCA-IACS%20Roles%20and%20Responsibilities.pdf](https://gca.isa.org/hubfs/21-29%20-%20ISAGCA/ISAGCA-IACS%20Roles%20and%20Responsibilities.pdf)  
27. Railway Organizational Chart Template \- How to Create One \- Organimi, accessed October 28, 2025, [https://www.organimi.com/railway-organizational-structure/](https://www.organimi.com/railway-organizational-structure/)  
28. Organizational Chart \- Light Rail Transit Authority, accessed October 28, 2025, [https://www.lrta.gov.ph/organizational-chart/](https://www.lrta.gov.ph/organizational-chart/)  
29. What is IEC 62443? IEC 62443 Standard Explained | Thales Cyber Services ANZ, accessed October 28, 2025, [https://tesserent.com/resources/what-is-iec-62443](https://tesserent.com/resources/what-is-iec-62443)  
30. IEC 62443 Certification for Cybersecurity Compliance \- TÜV SÜD, accessed October 28, 2025, [https://www.tuvsud.com/en/services/testing/industrial-security-iec-62443-training](https://www.tuvsud.com/en/services/testing/industrial-security-iec-62443-training)  
31. How can IEC 62443 certification help an asset owner? \- exida Asia Pacific, accessed October 28, 2025, [https://www.exida.com.sg/how-can-iec-62443-certification-help-an-asset-owner/](https://www.exida.com.sg/how-can-iec-62443-certification-help-an-asset-owner/)  
32. IEC 62443 4-2: Technical Security Requirements for IACS Components | Keyfactor, accessed October 28, 2025, [https://www.keyfactor.com/blog/iec-62443-4-2-technical-security-requirements-for-iacs-components/](https://www.keyfactor.com/blog/iec-62443-4-2-technical-security-requirements-for-iacs-components/)  
33. Cyber security Case (adapt. from CLC/FprTS 50701\) \- ResearchGate, accessed October 28, 2025, [https://www.researchgate.net/figure/Cyber-security-Case-adapt-from-CLC-FprTS-50701\_fig3\_354891803](https://www.researchgate.net/figure/Cyber-security-Case-adapt-from-CLC-FprTS-50701_fig3_354891803)  
34. IEC 62443 \- SSA Certification \- ISASecure, accessed October 28, 2025, [https://isasecure.org/certification/iec-62443-ssa-certification](https://isasecure.org/certification/iec-62443-ssa-certification)  
35. Excerpt \#3: Industrial Cybersecurity Case Studies and Best Practices, accessed October 28, 2025, [https://gca.isa.org/blog/excerpt-3-industrial-cybersecurity-case-studies-and-best-practices](https://gca.isa.org/blog/excerpt-3-industrial-cybersecurity-case-studies-and-best-practices)  
36. IEC 62443-2-4 \- Cyber Laws, accessed October 28, 2025, [https://cyber-laws.com/2023/12/30/iec-62443-2-4-draft-whats-new/](https://cyber-laws.com/2023/12/30/iec-62443-2-4-draft-whats-new/)