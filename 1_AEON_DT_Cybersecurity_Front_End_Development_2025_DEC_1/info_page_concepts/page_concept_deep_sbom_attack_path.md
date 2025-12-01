# Page Concept: Deep SBOM Attack Path
**"The Butterfly Effect of Code"**

## 1. Core Concept
A "Micro-to-Macro" visualization showing how a tiny library vulnerability (micro) triggers a catastrophic sector-wide breach (macro). It emphasizes the "Deep SBOM" capability.

## 2. Visual Design (The "Fractal Zoom")
*   **Initial View**: A single line of code in a library (e.g., `OpenSSL 1.0.2k`).
*   **The Zoom Out**:
    1.  **Library**: See the library inside a Software Package.
    2.  **Device**: See the software inside a Firewall.
    3.  **Facility**: See the firewall inside a Water Plant.
    4.  **Sector**: See the plant inside the National Grid.
*   **The Infection**: A red pulse starts at the code level and spreads outward, turning the entire grid red.

## 3. Key Features

### 3.1 The "NOW/NEXT/NEVER" Triage
*   **Visual**: A 3-lane highway.
*   **NOW Lane (Fast)**: High Criticality + High Exploitability. Cars (Patches) speeding through.
*   **NEXT Lane (Slow)**: Monitor.
*   **NEVER Lane (Parking)**: Accepted Risk.
*   **Interaction**: Drag and drop vulnerabilities to see how the "Priority Score" algorithm sorts them.

### 3.2 The Attack Path Tracer
*   **Visual**: A circuit board diagram.
*   **Flow**: Attacker (APT29) → Technique (T1190) → CVE → Library → Asset.
*   **Highlight**: "The Weakest Link." Show that 90% of the path is secure, but one library breaks the chain.

### 3.3 The Variation Engine
*   **Visual**: Two identical-looking firewalls side-by-side.
*   **Reveal**: "X-Ray" toggle shows one has 12 Critical CVEs (Old Firmware), the other has 0 (New Firmware).
*   **Message**: "Equipment Level Asset Management is a Lie. You need SBOM Level."

## 4. Technical Implementation
*   **Data Source**: `DEEP_SBOM_ATTACK_PATH_ARCHITECTURE.md`.
*   **Visuals**: D3.js Force Directed Graph for the attack paths.
*   **Data**: Real CVE and EPSS scores from the document.

## 5. Business Value
*   **"Precision"**: Demonstrates why AEON is 100x more accurate than competitors.
*   **"Efficiency"**: The NOW/NEXT/NEVER framework saves money by prioritizing only what matters.
*   **"Fear/Relief"**: Scares them with the hidden risk, then relieves them with the solution.
