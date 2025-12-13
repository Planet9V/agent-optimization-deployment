# Feasibility Study: The "Speckle + R3F" Hybrid Stack
**Project:** Cyber-62443-Assure
**Objective:** Select the 3D stack that delivers "Stunning Visuals" (R3F) with "Granular Asset Intelligence" (Speckle).

---

## 1. Executive Summary

| Requirement | Best Choice | Why? |
|:---|:---|:---|
| **Visually Stunning** | **React Three Fiber (R3F)** | Access to `drei` ecosystem (Environment, Shadows, Postprocessing) makes "premium" visuals trivial. |
| **Granular Attributes** | **Speckle** | **Crucial for 62443.** Allows querying specific objects ("Show me Frame 12") and attaching metadata (Risk: High) to them. |
| **BIM File Support** | **Speckle** | Handles Revit/Rhino/IFC imports server-side and streams *objects* (not just files) to the browser. |
| **Equipment Library** | **Use External GLBs** | *Gap remains.* We still need a "Cyber-62443 Asset Kit" (GLTFs) for non-BIM cyber assets (firewalls, servers) to augment the BIM model. |
| **Diegetic UI** | **pmndrs/uikit** | Best-in-class for placing UI *inside* the 3D world (e.g., floating panels aligned to a wall). |

**Recommended Stack:** **R3F + Speckle (Data Layer) + pmndrs/uikit + Custom GLB Asset Set.**

---

## 2. Technology Comparison

### 2.1 The Core Engine: R3F vs. Babylon.js

| Feature | React Three Fiber (R3F) | Babylon.js |
|:---|:---|:---|
| **Visual Quality** | ⭐⭐⭐⭐⭐ **Superior.** The `drei` library allows "cinematic" lighting/shadows with single lines of code (`<Environment preset="city" />`). | ⭐⭐⭐⭐ Good, but requires more manual tuning. |
| **React Integration** | ⭐⭐⭐⭐⭐ **Native.** It *is* React. State handling (zustand/redux) just works. | ⭐⭐⭐ Requires a bridge. |
| **Simplicity** | ⭐⭐⭐⭐ Declarative component model. | ⭐⭐⭐ Imperative API. |

**Verdict:** **R3F** provides the "Stunning" frontend we need.

### 2.2 BIM & Data: IFC.js vs. Speckle

| Feature | IFC.js (That Open Platform) | Speckle |
|:---|:---|:---|
| **Primary Use** | **File Viewing.** Great for loading a whole `.ifc` file. | **Object Streaming.** Breaks models into atomic objects with metadata. |
| **Granularity** | ⭐⭐ Low. Hard to query "just the sensors." | ⭐⭐⭐⭐⭐ **High.** Perfect for "Select Object -> Show Risk Score." |
| **Workflow** | File-based (Drag & Drop). | Stream-based (Push from Revit -> Stream to Web). |
| **Cybersecurity Fit** | **Too Basic.** Good for visualization, bad for intelligence. | **Ideal.** We can attach "Cyber Attributes" (SL-T, Vulnerabilities) directly to the Speckle objects. |

**Verdict:** **Speckle** is the correct choice. The complexity of running a Speckle server (or using their heavy cloud API) is worth it for the **granular attribute access** required for a PRD-driven compliance tool.

### 2.3 Diegetic UI: `pmndrs/uikit`

*   **Role:** The "Minority Report" interface.
*   **Feasibility:** High. Works natively inside R3F.

---

## 3. The "Equipment Library" Solution

**Problem:** Neither Speckle nor R3F provides "Cyber Assets" (Firewalls, PLCs). Speckle provides the *Building* (Walls, HVAC).
**Solution:** We act as the "Integrator." We place our own **Custom GLB Assets** (Cyber) *inside* the Speckle **BIM Model** (Physical).

**The "Cyber-62443 Asset Kit":**
We must source these 5 key low-poly assets to make the tool useful:

| Asset Type | Source Recommendation | File Format |
|:---|:---|:---|
| **PLC (generic)** | TurboSquid / Sketchfab (Buy a low-poly indusrial pack ~ $20) | `.glb` |
| **Server Rack** | Kenney.nl "Space Kit" (Free, CC0) - Looks clean/techy | `.glb` |
| **Firewall** | Custom simple box with texture | `.glb` |
| **HMI Screen** | `pmndrs/uikit` panel (Interactive!) | `React Component` |
| **Conduits** | Procedural Tubes (R3F `TubeGeometry`) | `Three.js Mesh` |

---

## 4. Proposed Architecture: "The Speckle-Cyber Hybrid"

```mermaid
graph TD
    User[User / Browser]
    
    subgraph "Data Layer"
        Speckle[Speckle Server] --> |Streams Objects| App
        Postgres[Cyber-Assure DB] --> |Attributes (Risk/SL)| App
    end

    subgraph "The Scene (R3F Canvas)"
        DirectionLight
        Environment[Environment (City Preset)]
        
        subgraph "Layer 1: The Facility (Speckle)"
            SpeckleLoader[Speckle R3F Loader]
            SpeckleObject[Wall/Pump/HVAC]
        end
        
        subgraph "Layer 2: Cyber Overlay (Custom GLB)"
            Asset1[PLC Model (.glb)]
            Asset2[Firewall Model (.glb)]
            Conduit[Glowing Tube]
        end
        
        subgraph "Layer 3: UI (Diegetic)"
            Panel[uikit Floating Panel] --> |Read/Write| Postgres
        end
    end
    
    User --> |Select| SpeckleObject
    User --> |Drag & Drop| Asset1
```

## 5. Recommendation

**Go with:**
1.  **Frontend:** **React Three Fiber** + **Drei** (Visuals).
2.  **BIM Data:** **Speckle** (Granular Object Streaming).
3.  **UI:** **pmndrs/uikit** (Diegetic Panels).
4.  **Cyber Assets:** **Custom "Cyber Kit"** (GLTF/GLB from sketchfab/kenney).

**Next Step:**
Create the `IEC62443_Reqs` structure and begin populating the asset library manifest.
