# Page Concept: The Triage Command Center
**"The War Room of Priorities"**

## 1. Core Concept
A high-stakes "Mission Control" screen that sorts the chaos of 316,000 vulnerabilities into three clear buckets: NOW, NEXT, and NEVER. It uses the visual language of emergency triage.

## 2. Visual Design (The "Defcon" Map)
*   **Style**: Dark room, glowing map tables, large countdown timers.
*   **Color Palette**:
    *   **NOW**: Pulsing Red (Alarm).
    *   **NEXT**: Steady Amber (Warning).
    *   **NEVER**: Cool Blue (Stable).

## 3. The Buckets

### The NOW Bucket (Immediate Action)
*   **Visual**: A "Hot List" on the center screen. Items are burning/smoking.
*   **Content**: "Log4Shell in Turbine Control". "EternalBlue in MRI Machine".
*   **Metric**: "Time to Impact: 4 Hours".

### The NEXT Bucket (Scheduled)
*   **Visual**: A calendar view on the right screen.
*   **Content**: "Update Windows Server 2019". "Patch Office 365".

### The NEVER Bucket (Accepted Risk)
*   **Visual**: A "Cold Storage" vault on the left.
*   **Content**: "Legacy Printer Vulnerability (Air Gapped)".

## 4. The Algorithm (The Brain)
*   **Visual**: A central visualization of the scoring logic.
    *   `Technical Score (CVSS) + Psychological Score (Bias) = Priority`.
    *   *Animation*: Watch a "High CVSS" vuln get downgraded to "NEVER" because it's on an air-gapped legacy system (Context).

## 5. Technical Implementation
*   **Data Source**: `Enhancement_12_NOW_NEXT_NEVER/README.md`.
*   **Visuals**: D3.js for dynamic sorting and filtering.

## 6. Innovation Factor
*   **"Focus"**: Solves the "Alert Fatigue" problem by visually hiding the noise (NEVER).
*   **"Psychology"**: Explicitly visualizes *why* something is prioritized (e.g., "Normalcy Bias Detected").
*   **"Actionability"**: The "NOW" list is a to-do list, not just a report.
