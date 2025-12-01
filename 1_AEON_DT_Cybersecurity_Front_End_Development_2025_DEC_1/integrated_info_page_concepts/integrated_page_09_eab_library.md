# Integrated Page Concept: The EAB Library (Express Attack Briefs)

## 1. Persona Evaluation & Strategy
*   **Evaluator**: "The Analyst" (Research/Intel Expert)
*   **Critique**: "The 'Codex' is great for documentation, but I need a dedicated feed for the EABs. There are going to be 200+ of these. I need to filter by Sector, Threat Actor, and Severity. I need to see the 'Latest Intel' instantly."
*   **Consolidation Strategy**: Expand `page_concept_eab_template.md` into a full "Library Application" design.

## 2. Core Concept: "The Daily Briefing"
This page is the "News Feed" of the AEON platform. It presents the Express Attack Briefs not as static files, but as a dynamic, searchable intelligence stream.

## 3. The "Wow" Visualization
**The Threat Radar Wall**
*   **Visual**: A "Minority Report" style grid of floating cards.
*   **Interaction**:
    *   **The Filter**: A circular "Radar" control. Dragging a handle to "Energy Sector" filters the grid to show only Energy-related EABs.
    *   **The Preview**: Hovering over a card expands it to show the "Executive Summary" and "Kill Chain" diagram.
    *   **The Deep Dive**: Clicking opens the full EAB in the "Reader Mode" (from the Codex).

## 4. Key Narrative & Copy
*   **Headline**: "Intelligence at the Speed of Attack."
*   **Sub-headline**: "A Curated Library of 200+ Express Attack Briefs."
*   **Body Copy**: "Threats evolve daily. Your intelligence should too. The EAB Library is a living repository of tactical analysis, updated in real-time. From the latest APT campaigns to emerging zero-days, every brief is standardized, actionable, and integrated with the AEON Graph."

## 5. Integrated Features
*   **The Standard Template**: (From EAB Template) Every brief follows the strict "Situation, Impact, Remediation" format.
*   **The Graph Link**: Each EAB links directly to the relevant nodes in the Neo4j graph (e.g., "Click here to see all assets affected by CVE-2025-1234").
*   **The Subscription**: Users can "Subscribe" to specific tags (e.g., "Manufacturing," "Ransomware") to get alerts.

## 6. Technical Implementation
*   **Stack**: React + Masonry Layout (for the grid) + Lunr.js (for client-side search).
*   **Scalability**: Designed to handle 1000+ briefs with pagination and lazy loading.
