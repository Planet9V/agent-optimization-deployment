# Page Concept: The Cyber Epidemic Tracker
**"The Physics of Contagion"**

## 1. Core Concept
A visualization of **Cyber Epidemiology**. This page treats malware and information as "Viruses" spreading through a population. It visualizes the **$R_0$ (Basic Reproduction Number)** and the **Epidemic Threshold** of the network, showing how "Hubs" accelerate the spread.

## 2. Visual Design (The "Contagion Map")
*   **The Map**: A dark, bio-hazard themed network map.
*   **The Infection**: Infected nodes turn **Red**. Recovered nodes turn **Blue**. Susceptible nodes are **Grey**.
*   **The Spread**: A "Pulse" effect radiates from infected nodes to their neighbors.

## 3. Key Features & Interactions

### 3.1 The "$R_0$" Gauge
*   **Visual**: A prominent gauge showing the current $R_0$.
    *   **$R_0 < 1$**: Green Zone (Dying out).
    *   **$R_0 > 1$**: Red Zone (Exponential Growth).
    *   **$R_0 \to \infty$**: Flashing Warning (Scale-Free Saturation).

### 3.2 "Patient Zero" Simulation
*   **Interaction**: Click any node to designate it as "Patient Zero".
*   **Effect**: Watch the infection spread from that point.
    *   **Hub Infection**: If you click a central hub, the map turns red instantly.
    *   **Leaf Infection**: If you click a peripheral node, the spread is slow.

### 3.3 Immunization Strategy Selector
*   **Controls**: Buttons for defense strategies.
    *   **"Random Immunization"**: Randomly turns 10% of nodes Blue. (Ineffective).
    *   **"Targeted Immunization"**: Turns the top 10% of **Hubs** Blue. (Highly Effective).
*   **Visual**: Shows the "Firebreak" effect. The red wave hits the blue wall and stops.

## 4. Technical Implementation
*   **Data Source**: `02_MATHEMATICAL_PHYSICS_OF_CYBER_EPIDEMICS.md`.
*   **Backend**: SIR / SEI Model simulation.
*   **Visualization**:
    *   **WebGL**: For efficient rendering of color changes across thousands of nodes.

## 5. Business Value
*   **"Urgency"**: Visually demonstrates how fast a threat can spread ($R_0$).
*   **"Strategy"**: Proves the value of **Targeted Defense** (protecting the Hubs/Crown Jewels).
*   **"Clarity"**: Uses the familiar language of pandemics (which everyone now understands) to explain Cyber Risk.
