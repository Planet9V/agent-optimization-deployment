# AEON Nexus: The McKenney-Lacan Visualization Platform
**Architecture Specification & Design Document**

**Document ID**: AEON_NEXUS_WEB_SPEC
**Version**: 1.0 (Blueprint)
**Date**: 2025-11-29
**Author**: AEON Design Bureau (Swarm Iota)
**Classification**: UNCLASSIFIED // TECHNICAL SPECIFICATION

---

## 1. The Vision: "Beyond the Screen"

The AEON Nexus is not a "website." It is a **Cognitive Interface**.
It does not display data; it **renders the unconscious**.
It combines the spatial depth of a video game, the temporal precision of a DAW (Digital Audio Workstation), and the relational complexity of a Knowledge Graph.

**The Core Metaphor**: The user is the **Conductor** standing on the podium of the **Digital Twin**.

---

## 2. The Tech Stack (The Engine)

To achieve "Groundbreaking" fidelity, we use the bleeding edge of the JavaScript ecosystem.

### 2.1 Core Framework
*   **Next.js 15 (App Router)**: For server-side rendering of the initial state and SEO of the academic papers.
*   **React 19 (Concurrent Mode)**: Essential for handling high-frequency updates (60fps) from the audio/visual engine without blocking the UI.
*   **TypeScript**: Strict typing for the complex calculus interfaces.

### 2.2 The Visual Engine (3D & 4D)
*   **React Three Fiber (R3F)**: The React renderer for Three.js. Allows us to compose 3D scenes as components.
*   **Drei**: High-level helpers (Cameras, Controls, Environment).
*   **React Three Postprocessing**: For "Bloom" (Neon aesthetics), "Depth of Field" (Cinematic focus), and "Glitch" effects (Trauma simulation).
*   **Maath**: Mathematics helpers for smooth interpolation of 3D vectors.

### 2.3 The Data Engine (Graph & Calculus)
*   **Neo4j Driver**: Direct connection to the Graph Database to visualize the "Topology" (Betti Numbers).
*   **React Force Graph**: For 2D/3D visualization of the Zettelkasten Library.
*   **Zustand**: Transient state management. We need to update the "Current Beat" state 60 times a second. Redux is too slow. Zustand is bare-metal.

### 2.4 The Audio Engine (Sonification)
*   **Tone.js**: Web Audio framework. We do not play MP3s. We **synthesize** the sound in real-time based on the CSV data.
    *   *Example*: The "Heartbeat" is a `MembraneSynth` triggered by the $H(t)$ column.
    *   *Example*: The "Mischief" is a `FM_Synth` modulated by the $M(t)$ column.

### 2.5 The UI/UX Layer
*   **Tailwind CSS**: For rapid, utility-first styling.
*   **Framer Motion**: For complex layout transitions (e.g., morphing from "Score" to "Manifold").
*   **Radix UI**: Accessible, unstyled primitives for Dialogs, Popovers, and Sliders.
*   **Glassmorphism**: Heavy use of `backdrop-filter: blur(20px)` to create the "Holographic" feel.

---

## 3. The Architecture Diagram

```mermaid
graph TD
    User[User / Conductor] -->|Interacts| UI[React 19 Frontend]
    
    subgraph "The AEON Nexus (Browser)"
        UI -->|Render| Canvas[Three.js Canvas (WebGL)]
        UI -->|Synthesize| Audio[Tone.js Context]
        UI -->|Query| State[Zustand Store]
        
        Canvas -->|Visualizes| Manifold[Psychometric Manifold]
        Canvas -->|Visualizes| Score[Symphonic Timeline]
        Canvas -->|Visualizes| Twin[Holographic Dashboard]
    end
    
    subgraph "The Backend (The Chef)"
        API[FastAPI (Python)] -->|Serves| CSV[Grand Unified Score]
        API -->|Computes| Calc[Calculus Engine (PyTorch)]
        API -->|Queries| Graph[Neo4j Database]
    end
    
    UI -->|Fetch Data| API
```

---

## 4. The Site Tree & Component Breakdown

### 4.1 `/` (The Landing: The Omega Point)
*   **Visual**: A single, pulsing singularity point in the center of a void.
*   **Audio**: A low, resonant "Om" (Deep C).
*   **Interaction**: "Enter the Nexus." The point explodes (Big Bang) into the 3D interface.

### 4.2 `/score` (The Symphonic Timeline)
*   **Concept**: "Guitar Hero" for Psychohistory.
*   **Layout**:
    *   **Center**: The "Highway." Lines of dialogue flow towards the user.
    *   **Left Rail**: The "Unconscious." Colored waveforms representing $H(t)$ (Red) and $M(t)$ (Green).
    *   **Right Rail**: The "Theory." Floating bubbles representing Lacanian concepts ($a$, $, S1).
*   **Components**:
    *   `<TimelineTrack />`: Renders the scrolling lanes.
    *   `<BeatMarker />`: Visualizes the "Bar Lines" of the play.
    *   `<SonificationEngine />`: Triggers Tone.js synths when data crosses the "Now" line.

### 4.3 `/manifold` (The 3D Exploration)
*   **Concept**: "Inside the Mind."
*   **Layout**: Full-screen WebGL canvas.
*   **Visual**: A 12-dimensional hyper-shape (Calabi-Yau manifold style).
    *   **The Knot**: The Borromean Rings (Real, Symbolic, Imaginary) float in the center.
    *   **The Path**: A glowing golden line traces Willy's trajectory through the space.
*   **Interaction**:
    *   **OrbitControls**: User can rotate and zoom.
    *   **Click**: Clicking a point on the path opens the "Beat Details" panel.

### 4.4 `/twin` (The Operational Dashboard)
*   **Concept**: "The Chef's Cockpit."
*   **Layout**: HUD (Heads-Up Display) style.
*   **Components**:
    *   `<HealthGauge />`: A circular gauge showing the Health Score (0-10). Glitches when score drops.
    *   `<TopologyMap />`: A force-directed graph of the "Town" (Nodes = Characters).
    *   `<AlertBanner />`: Flashes "CRITICAL SLOWING" when $\rho > 0.9$.
    *   `<ModulationSlider />`: Allows the user to "Remix" the play (e.g., reduce Trauma).

### 4.5 `/library` (The Zettelkasten)
*   **Concept**: "The Neural Network of Knowledge."
*   **Layout**: Not a list. A 3D Galaxy of Stars.
*   **Visual**: Each "Star" is a paper (e.g., `Predictive_04`). Lines connect related concepts.
*   **Interaction**: Clicking a star opens the PDF in a "Glass Pane" overlay.

---

## 5. The "Groundbreaking" Features

### 5.1 The 4D Time-Scrub
The user can drag a slider to move back and forth in time.
*   **Effect**: The entire application syncs.
    *   The **Score** scrolls.
    *   The **Manifold** trajectory rewinds/advances.
    *   The **Audio** scrubs (using granular synthesis to preserve pitch).
    *   The **Dashboard** updates its gauges instantly.

### 5.2 The "Trauma Filter" (Shader)
We use a custom GLSL shader to visualize "Trauma" ($R > 0$).
*   **Normal**: Clean, sharp lines.
*   **Trauma**: The screen distorts (Chromatic Aberration), the colors shift to red/black, and the audio gets bit-crushed. The user *feels* the stress of the system.

### 5.3 The "Live Code" Link
Every visualization is linked to the actual Python code.
*   **Feature**: "View Source" on a graph doesn't show HTML; it shows the **PyTorch Tensor** that generated it. The user can edit the weight, and the 3D visualization updates in real-time.

---

## 6. Conclusion

This architecture transforms the McKenney-Lacan Calculus from a "Theory" into a **Place**.
It is a place where the user can go to *watch* the unconscious mind unfold, *hear* the rhythm of the cyber-social organism, and *touch* the mathematics of the soul.
