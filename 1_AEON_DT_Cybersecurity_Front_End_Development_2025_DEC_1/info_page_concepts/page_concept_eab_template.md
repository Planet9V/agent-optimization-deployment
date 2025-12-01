# Page Concept: Express Attack Brief (EAB) Standard Template
**"The Living Intelligence Report"**

## 1. Core Concept
A standardized, repeatable template designed to transform dense, text-heavy "Express Attack Briefs" (EABs) into immersive, interactive intelligence experiences. It uses an "Endless Scroll" format where each section of the brief is a distinct, highly visual "Block". The goal is to make "EVERY SINGLE WORD" visible and readable while augmenting it with dynamic data visualizations.

## 2. Visual Design (The "Black Box" Recorder)
*   **Style**: High-contrast, "Dark Mode" by default. Monospace fonts for technical data, serif for narrative.
*   **Layout**: Single-column, infinite scroll.
*   **Metaphor**: Decoding a flight recorder or a classified transmission.

## 3. The Template Blocks (Standardized)

### Block 1: The Header (The Signal)
*   **Content**: Title (e.g., "VOLTZITE"), Date, TLP Level, Confidence Score.
*   **Visual**: A large, glitching title card. Background features a subtle, rotating 3D model of the target sector (e.g., Energy Grid).
*   **Data**: "Threat Level: CRITICAL" (Pulsing Red).

### Block 2: Executive Summary (The Brief)
*   **Content**: High-level overview.
*   **Visual**: Large, readable typography.
*   **Interaction**: As you scroll, key phrases ("Espionage", "Pre-positioning") highlight in neon colors.

### Block 3: Threat Actor Profile (The Identity)
*   **Content**: Who is behind it? (e.g., VOLT TYPHOON).
*   **Visual**: A "Player Card" or "Wanted Poster" style.
*   **Visualization**: A Radar Chart showing the actor's capabilities (Stealth, Destructive Potential, Resource Level).

### Block 4: Technical Analysis (The Blueprint)
*   **Content**: Deep dive into TTPs (Tactics, Techniques, Procedures).
*   **Visual**: Split screen. Text on the left, interactive "Attack Path" graph on the right.
*   **Interaction**: Hovering over a technique in the text (e.g., "Living off the Land") highlights the corresponding node in the graph.

### Block 5: Impact Assessment (The Blast Radius)
*   **Content**: What is the damage?
*   **Visual**: A "Heatmap" of the organization or sector.
*   **Visualization**: Red zones indicate affected areas (e.g., "OT Network", "Safety Systems").

### Block 6: Recommendations (The Shield)
*   **Content**: Mitigation strategies.
*   **Visual**: A checklist style.
*   **Interaction**: Users can "check off" items to see the estimated risk reduction (e.g., "Patching reduces risk by 40%").

## 4. Technical Implementation
*   **Repeatability**: The template is a React component that takes the EAB Markdown/JSON as input and renders the blocks automatically.
*   **Data Density**: Uses "Collapsible Sections" (Accordions) for extremely long technical logs, keeping the page clean but ensuring all data is accessible.

## 5. Innovation Factor
*   **"Readability"**: Transforms a wall of text into a structured narrative.
*   **"Scalability"**: Can be applied instantly to all 40+ EABs.
*   **"Engagement"**: Turns a passive reading experience into an active investigation.
