# AEON Nexus: Website Content Strategy

**Document ID**: WEBSITE_CONTENT_STRATEGY
**Parent Doc**: AEON_NEXUS_VISIONARY_PRD_v2
**Date**: 2025-11-29
**Author**: AEON Design Bureau (Swarm Iota)

---

## 1. The Challenge: Density vs. Beauty

We have a conflict:
1.  **The Requirement**: "ALL the content is available... well over 1000 lines long."
2.  **The Goal**: "Amazing interactions... groundbreaking UI."

**The Solution**: We treat the Content as **Texture**.
Just as a video game has "Lore" hidden in books, the AEON Nexus has "Theory" hidden in the Manifold.

---

## 2. The Dual-Mode Architecture

### 2.1 Conductor Mode (The Default)
*   **Experience**: Immersive, 3D, Symphonic.
*   **Content Visibility**: Low.
*   **Interaction**: When the user clicks a "Knot" in the 3D view, a **Glass Card** appears with a *Summary* (3-4 lines) and a button: **"Enter Scholar Mode"**.

### 2.2 Scholar Mode (The Deep Dive)
*   **Experience**: Clean, typographic, focused.
*   **Layout**:
    *   **Left Column (20%)**: The 3D Manifold (minimized but active).
    *   **Center Column (60%)**: The Text (The 65 Volumes).
    *   **Right Column (20%)**: The Zettelkasten (Citation Graph).
*   **Interaction**: As the user scrolls the text, the 3D Manifold *rotates* to show the relevant concept.
    *   *Example*: Scrolling to "Riemannian Curvature" causes the 3D mesh to spike.

---

## 3. The Structure of the Codex

We organize the 65 volumes not as a list, but as a **Knowledge Graph**.

### 3.1 The Node Types
*   **Theorems**: The core math (e.g., `Predictive_04`).
*   **Primers**: The playgrounds (e.g., `Primer_02`).
*   **Applications**: The use cases (e.g., `UNIVERSAL_APPLICATION_LAYER`).
*   **Symphonies**: The tone poems (e.g., `Movement_I`).

### 3.2 The "Deep Link" Protocol
Every paragraph in the corpus is indexed with a UUID.
*   `[#UUID-1234]`: "The Borromean Knot consists of three rings..."
*   **Action**: Clicking this link triggers `manifold.animateToState("BORROMEAN_LOCK")`.

---

## 4. The Librarian (AI Assistant)

To help users navigate 1000+ lines, we embed a local LLM (or vector search).
*   **User Query**: "How does this apply to hiring?"
*   **Librarian**: "See **Universal Application Layer**, Section 2.1: The Resonance Engine." (Links directly to the paragraph).

---

## 5. Conclusion

We do not compromise.
We give the user the **Video Game** AND the **Textbook**.
But we never force them to choose. They flow between them.
