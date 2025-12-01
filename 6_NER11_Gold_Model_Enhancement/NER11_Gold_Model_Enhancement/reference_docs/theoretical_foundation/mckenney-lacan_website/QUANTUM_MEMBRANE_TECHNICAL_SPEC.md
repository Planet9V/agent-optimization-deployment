# Quantum Membrane: Technical Specification & Architecture

**Document ID**: QUANTUM_MEMBRANE_SPEC_v1
**Classification**: DEEP ENGINEERING // HARD REASONING
**Target**: Option 5 (Evolved Species)
**Date**: 2025-11-29

---

## 1. The Core Concept: Probabilistic UI

Traditional UIs are **Deterministic**: If I click X, Y happens.
The Quantum Membrane is **Probabilistic**: If I click X, Y happens with probability $P(Y|X, \text{Context})$.

### 1.1 The Mathematics of Collapse
We model the UI as a **Wave Function** $\Psi$.
*   **Superposition**: All potential UI elements (Search, Graph, Text, Settings) exist simultaneously in a hidden state.
*   **Observation**: The user's cursor position ($u, v$) and gaze (if available) act as the "Observer."
*   **Collapse**: The probability of an element $E_i$ rendering is given by:
    $$ P(E_i) = \frac{1}{1 + e^{-k(I_i - T)}} $$
    Where:
    *   $I_i$ is the **Relevance Score** (computed by the GNN).
    *   $T$ is the **Entropy Threshold** (Global State).
    *   $k$ is the **Steepness** (Sensitivity).

---

## 2. The Tech Stack (Verified Compatibility)

To implement this, we need a specific stack that supports **Concurrent Rendering** (React 19) and **High-Performance Physics** (WebWorkers).

### 2.1 Dependency Matrix
*   **Framework**: `next@15.0.0-rc.0` (App Router, Server Actions)
*   **Core**: `react@19.0.0-rc.0`, `react-dom@19.0.0-rc.0`
*   **3D Engine**: `@react-three/fiber@9.0.0-alpha` (React 19 compatible)
*   **Physics**: `@react-three/cannon` (Worker-based)
*   **Animation**: `@react-spring/three` (Spring physics for UI)
*   **State**: `zustand@4.5.0` (Transient updates, no re-renders)
*   **Math**: `mathjs` (Matrix operations for GNN)

---

## 3. The Architecture: "The Living Graph"

### 3.1 The GNN Worker (`workers/gnn.worker.ts`)
We cannot run the Relevance Score calculation on the main thread. It runs in a WebWorker.
*   **Input**: User Interaction History (Clicks, Hovers, Time).
*   **Model**: A simple Bayesian Network (or lightweight TensorFlow.js model).
*   **Output**: A Float32Array of probabilities for every node in the graph.

### 3.2 The Membrane Component (`components/membrane/QuantumCanvas.tsx`)
This is the main entry point. It renders the 3D scene.

```tsx
// Pseudo-code for Architecture
function QuantumCanvas() {
  const entropy = useStore(state => state.entropy)
  const probabilities = useGNN() // Custom hook consuming Worker data
  
  return (
    <Canvas concurrent>
      <Physics gravity={[0, 0, 0]}>
        <Swarm 
          count={1000} 
          probabilities={probabilities} 
          entropy={entropy} 
        />
      </Physics>
      <PostProcessing>
         <Glitch active={entropy > 0.8} />
      </PostProcessing>
    </Canvas>
  )
}
```

### 3.3 The Node Shader (`shaders/MembraneNode.glsl`)
We do not fade nodes out (opacity). We **dissolve** them using noise.
*   **Uniforms**: `uProbability`, `uTime`, `uEntropy`.
*   **Logic**: If `noise(uv + time) > uProbability`, discard the pixel.

---

## 4. Implementation Strategy

### Phase 1: The Skeleton
1.  Initialize Next.js 15 project with TypeScript.
2.  Configure `next.config.js` for GLSL support (`glslify-loader`).
3.  Set up the Zustand store for "System Entropy."

### Phase 2: The Physics
1.  Implement the `ForceGraph` using `d3-force-3d` inside a WebWorker.
2.  Map the 3D coordinates to `InstancedMesh` for performance (1 draw call for 10k nodes).

### Phase 3: The Intelligence
1.  Implement the `GNN` worker.
2.  Connect the `Relevance Score` to the `InstanceColor` and `InstanceScale`.

---

## 5. Risk Assessment (Hard Reasoning)

*   **Risk**: React 19 RC is unstable.
    *   *Mitigation*: Pin versions exactly. Use `useSyncExternalStore` for Zustand compatibility.
*   **Risk**: WebGL Context Loss on mobile.
    *   *Mitigation*: Fallback to "2D Dashboard" (Option 2) if `gl.capabilities.isWebGL2` is false.
*   **Risk**: User Confusion ("Where is the menu?").
    *   *Mitigation*: The "Observer Effect" must be subtle. Key navigation elements (Home, Search) must have $P(E) = 1.0$ always.

---

## 6. Conclusion

This is not a website. It is a **Simulation**.
It requires treating the DOM and the Canvas as a single, fluid medium.
We are building a **Cybernetic Organism** where the user is the brain and the website is the body.
