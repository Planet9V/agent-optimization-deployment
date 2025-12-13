# Presentation Deck: Operationalizing Railway Cybersecurity

Here is the comprehensive  **Stakeholder Workshop Presentation Deck** . This content is structured to be copied directly into PowerPoint or a similar tool. It is designed to guide the conversation phase-by-phase, ensuring the "Nexus Points" (safety-security alignment) are addressed and the necessary data is "uploaded" from the engineering teams.


## **Slide 1: Title Slide**

**Title:** Operationalizing Railway Cybersecurity: A Lifecycle Approach
**Subtitle:** Integrating IEC 62443, TS 50701, and EN 50126 for Critical Infrastructure
**Purpose:** To define the "Nexus Points" where Safety and Security must converge.

**Speaker Notes:**
"Welcome. We are here to move beyond treating cybersecurity as just an IT compliance exercise. In railway, security is a reliability issue. If the system is not secure, it cannot be considered safe. Today, we will walk through the project lifecycle, identifying exactly when and how we 'upload' existing safety data to build our cybersecurity case."

---

## **Slide 2: The Strategy – The "Standards Nexus"**

**Visual:** A V-Cycle diagram showing **EN 50126 (Safety)** on the left and **IEC 62443 (Security)** on the right. Connect them with arrows at specific "Nexus Points."

**Key Bullet Points:**

* **The Problem:** Safety lasts 30 years; Cyber threats change monthly.
* **The Solution:** CLC/TS 50701 acts as the "Rosetta Stone" translating IEC 62443 into Rail language.^^
* **The Methodology:** We do not invent new assets. We "ingest" the Safety Hazard Log.
* **The Goal:** A **Cybersecurity Case** that supports the Safety Case.^^

**Facilitator Question (To Project Manager):**

* "Are the Safety and Security teams currently sharing the same asset register, or do we have two different versions of the 'truth' regarding the system architecture?"

---

## **Slide 3: Phase I – The "Upload" (Nexus Point 1)**

**Visual:** A funnel graphic. *Inputs:* "System Architecture," "Asset List." *Output:* "System Under Consideration (SuC)."

**Key Bullet Points:**

* **Objective:** Define the boundaries. What are we protecting?
* **Action:** Ingest the **System Definition** from EN 50126 Phase 2.^^
* **The Rule:** If it connects (physically or logically) to a safety function, it is in scope.
* **Deliverable:** A unified Asset Inventory tagged with Safety Integrity Levels (SIL).^^

**Facilitator Question (To Systems Engineer):**

* "We need to define the 'System Under Consideration' (SuC). Does the current architecture diagram include *all* maintenance laptops, remote diagnostic gateways, and passenger Wi-Fi bridges? These are our primary attack vectors."

---

## **Slide 4: Phase II – The "Worst Case" Disaster (Nexus Point 2)**

**Visual:** A Risk Matrix (Severity vs. Likelihood). The "Catastrophic" row is highlighted red.

**Key Bullet Points:**

* **The Upload:** We map the **Preliminary Hazard Analysis (PHA)** to Cyber Threats.
* **The Logic:**
  * *Hazard:* Train Collision (Catastrophic).
  * *Cyber Cause:* Malware spoofs "Track Clear" signal.
  * *Result:* Cyber Risk = Catastrophic.^^
* **Assumption:** For this workshop, we assume the attacker *is* in the network (Likelihood = 1).
* **Outcome:** Identification of "High Consequence" assets that need the strongest protection (SL-T 4).^^

**Facilitator Question (To Safety Manager):**

* "Looking at your top 3 catastrophic hazards (e.g., Collision, Derailment): Is there a hardware backstop (like a relay) that prevents this, or are we relying entirely on the software logic of the interlocking? If I own the software, do I own the hazard?"

---

## **Slide 5: Phase III – Zoning & Architecture (Nexus Point 3)**

**Visual:** A Network Diagram showing colored "Zones" separated by "Conduits" (Firewalls/Gateways).

**Key Bullet Points:**

* **Segmentation Strategy:** Group assets by **Criticality** (SIL) and  **Exposure** .^^

  * *Zone A (Vital):* Signalling, Interlocking (SIL 4) ->  **Target: SL 4** .
  * *Zone B (Ops):* Traffic Management, SCADA (SIL 2) ->  **Target: SL 3** .
  * *Zone C (Public):* Wi-Fi, Ticketing ->  **Target: SL 1** .
* **The Conduit Rule:** All traffic moving between zones must be inspected.^^

**Facilitator Question (To Network Architect):**

* "We have a conduit connecting the 'Vital Zone' to the 'Operations Zone'. If we place a firewall here, will the latency introduced by packet inspection break the safety heartbeat of the signaling protocol? Have we tested the timing?"

---

## **Slide 6: Phase IV – Supplier Interrogation (Nexus Points 4-6)**

**Visual:** A Checklist labeled "IEC 62443-4-1/4-2 Compliance."

**Key Bullet Points:**

* **The Gap:** Designing a secure network is useless if the devices (PLCs, OBCs) are vulnerable.
* **Requirement:** Suppliers must prove  **Security Level Capability (SL-C)** .^^
* **Key Checks:**
  * No hardcoded passwords.
  * Signed firmware updates.
  * Defined vulnerability disclosure time (SLA).

**Facilitator Question (To Suppliers):**

* "For the Interlocking/OBC you are supplying: Do you have an IEC 62443-4-1 certificate for your development process? If a new vulnerability is found next year, do you contractually guarantee a patch within 30 days? If not, we cannot accept this product in a Critical Zone without extra firewalls."

---

## **Slide 7: Phase V – Consensus & Mitigation (Nexus Point 7)**

**Visual:** A Balance Scale weighing "Security" vs. "Availability/Performance."

**Key Bullet Points:**

* **The Conflict:** Encryption slows down data; Patching requires downtime.
* **Compensating Countermeasures:**
  * *Issue:* Cannot patch the legacy interlocking.
  * *Fix:* "Virtual Patching" via an industrial IPS firewall at the zone boundary.^^
* **Risk Acceptance:** The Asset Owner must sign off on the "Residual Risk."

**Facilitator Question (To Operations Director):**

* "We cannot patch the Traffic Management System without a reboot. Can we agree to a maintenance window every 6 months? If not, we must accept the risk that a vulnerability could remain exposed for a year. Is that acceptable to the Board?"

---

## **Slide 8: Phase VI – The Handover (Nexus Point 8)**

**Visual:** A document stack. Bottom: "Safety Case." Top: "Cybersecurity Case."

**Key Bullet Points:**

* **The Deliverable:** The **Cybersecurity Case** (TS 50701 Clause 9).^^

  * Evidence of Risk Assessment (IRA/DRA).
  * Evidence of Testing (Penetration Test Reports).
  * **SecRAC (Security Related Application Conditions):** The manual for the operator.
* **The Shift:** From "Design/Build" (CAPEX) to "Monitor/Maintain" (OPEX).

**Facilitator Question (To Maintenance/Asset Owner):**

* "We are handing over the 'Key Management Plan' for the encryption keys. Who, by name or role, is responsible for rotating these keys next year? If they lose the keys, the trains stop. Do we have a procedure for this?"

---

## **Slide 9: Conclusion & Next Steps**

**Visual:** A Roadmap Timeline showing the upcoming workshop dates.

**Key Bullet Points:**

* **Immediate Action:** Schedule Workshop 1 (The Hazard Log "Upload").
* **Data Request:** Please provide the latest PHA, Network Topology, and Asset Register by.
* **Goal:** A signed-off Initial Risk Assessment (IRA) by.

**Closing Statement:**
"By following this sequence, we ensure that cybersecurity is not a blocker, but an enabler of safety. We will use the data you already have to build the defense you need."
