# AEON Nexus: Tech Stack Deep Dive

**Document ID**: AEON_NEXUS_TECH_STACK_DEEP_DIVE
**Parent Doc**: AEON_NEXUS_VISIONARY_PRD_v2
**Date**: 2025-11-29
**Author**: AEON Design Bureau (Swarm Iota)

---

## 1. The Core Engine: Next.js 15 + React 19

To achieve "Groundbreaking" performance, we use the latest React features.
*   **Concurrent Mode**: Essential for keeping the UI responsive (60fps) while the 3D engine and Audio engine are crunching data.
*   **Server Components (RSC)**: We render the "Scholar Mode" text on the server for SEO and speed.
*   **Suspense**: We stream the 3D assets and the Graph data independently.

---

## 2. The 3D Engine: React Three Fiber (R3F)

We do not use standard materials. We write **Custom Shaders**.

### 2.1 The Trauma Shader (GLSL)
*   **Vertex Shader**: Displaces the mesh based on the $R$ value (Riemann Curvature).
*   **Fragment Shader**: Uses `dFdx` and `dFdy` to calculate face normals dynamically for a "Crystal" look.
*   **Optimization**: We use `InstancedMesh` for the "Note Blocks" in the Score view (1000+ objects with 1 draw call).

### 2.2 The Flow Shader
*   **Concept**: Visualizing the "Geodesic" path.
*   **Technique**: A scrolling UV texture on a `TubeGeometry` that glows based on the "Energy" ($H$) of the system.

---

## 3. The Audio Engine: Tone.js

We do not play MP3s. We **synthesize** the soul of the machine.

### 3.1 Generative Synthesis
*   **Heartbeat**: `MembraneSynth`. Pitch decays with "Exhaustion".
*   **Mischief**: `FMSynth`. Modulation Index increases with "Chaos".
*   **Harmony**: `PolySynth`. Plays the chords derived from the `GTTM` analysis.

### 3.2 Spatial Audio
*   **Panner3D**: We attach a Panner node to each "Actor" in the 3D graph.
*   **Effect**: As you fly through the graph, you hear the voices (Instruments) spatialized around you.

---

## 4. The Data Engine: Neo4j + FastAPI

### 4.1 The Graph (Neo4j)
*   **Nodes**: `Theorem`, `Primer`, `Application`, `Symphony`.
*   **Edges**: `CITES`, `EXPLAINS`, `VISUALIZES`.
*   **Query**: `MATCH (t:Theorem)-[:VISUALIZES]->(p:Primer) RETURN p`

### 4.2 The Calculus (FastAPI)
*   **PyTorch**: We run the `PsychometricTensor` calculations on the backend.
*   **WebSocket**: We stream the "Future Cone" simulation data to the frontend in real-time.

---

## 5. Performance Strategy

*   **WebGPU**: We target the WebGPU renderer for Three.js (if available) for massive particle counts.
*   **WebWorkers**: We run the "Force Directed Graph" physics in a separate thread to avoid blocking the main thread.
*   **LOD (Level of Detail)**: We simplify the 3D meshes when the camera is far away.
