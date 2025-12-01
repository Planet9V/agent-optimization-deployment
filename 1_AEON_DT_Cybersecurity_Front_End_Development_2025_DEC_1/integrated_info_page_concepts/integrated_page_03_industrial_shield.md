# Integrated Page Concept: The Industrial Shield (OT Security & Resilience)

## 1. Persona Evaluation & Strategy
*   **Evaluator**: "The CISO" (Risk/Compliance Expert)
*   **Critique**: "The 'Shield Generator' is cool but too sci-fi. The 'Resilience Engine' is great for engineers but needs context. The 'Ontology' is too abstract. I need a single pane of glass that shows me *Compliance*, *Reliability*, and *Inventory* in one view. Prove to me that you understand OT is different from IT."
*   **Consolidation Strategy**: Merge `page_concept_iec62443_safety.md`, `page_concept_resilience_engine.md`, `page_concept_equipment_ontology.md`, and `page_concept_deep_sbom_attack_path.md` into a comprehensive "OT Defense Citadel."

## 2. Core Concept: "The Physics of Defense"
This page treats cybersecurity as a physical engineering discipline. It visualizes the "Digital Twin" not just as data, but as a fortified structure protecting critical assets.

## 3. The "Wow" Visualization
**The Digital Twin Citadel**
*   **Visual**: A high-fidelity 3D model of a generic industrial facility (Refinery/Factory).
*   **Interaction**:
    *   **The Zones**: The facility is divided into glowing, semi-transparent "Conduits" (IEC 62443 Zones).
    *   **The Health**: Zooming in reveals individual assets (Turbines, PLCs). They pulse with "Health" (MTBF) and "Security" (Vulnerability) metrics.
    *   **The Attack**: A red "Attack Path" line snakes through the network, stopped by a "Zone Firewall."

## 4. Key Narrative & Copy
*   **Headline**: "Cybersecurity That Speaks Physics."
*   **Sub-headline**: "IEC 62443 Compliance, RAMS Resilience, and Deep SBOM Visibility."
*   **Body Copy**: "In the OT world, a reboot isn't an option; it's an outage. AEON's Industrial Shield engine integrates safety standards (IEC 62443) with engineering reality (RAMS). We map every bolt, every line of code, and every protocol to ensure that your digital defenses are as robust as your physical walls."

## 5. Integrated Features
*   **The Zone Architect**: (From IEC 62443) A drag-and-drop interface for defining security zones and conduits.
*   **The Failure Predictor**: (From Resilience Engine) A "Time Slider" that shows predicted component failures based on MTBF curves.
*   **The Supply Chain X-Ray**: (From Deep SBOM) Clicking a PLC reveals its entire software bill of materials, highlighting a hidden Log4j vulnerability deep in the firmware.

## 6. Technical Implementation
*   **Stack**: React Three Fiber (for the Facility Model) + Neo4j (Graph Data).
*   **Data Density**: High. The "Asset Detail" panel pulls real specs from the Ontology.
