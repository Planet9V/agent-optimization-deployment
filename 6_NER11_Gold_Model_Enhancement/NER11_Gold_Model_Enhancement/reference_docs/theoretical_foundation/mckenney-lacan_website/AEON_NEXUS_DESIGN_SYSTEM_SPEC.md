# AEON Nexus: Design System Specification
**The Visual Language of the Digital Twin**

**Document ID**: AEON_NEXUS_DESIGN_SYSTEM_SPEC
**Parent Doc**: AEON_NEXUS_PRD_EXHAUSTIVE
**Date**: 2025-11-29
**Author**: AEON Design Bureau (Swarm Iota)

---

## 1. The Aesthetic: "Neon Noir"

The interface must feel like it exists **inside a computer**.
It is not "Paper" (Material Design). It is **Light** (Holography).
*   **Keywords**: Translucent, Luminescent, Volumetric, Glitch, Mathematical.

---

## 2. Typography

We use a tri-font stack to separate the "Registers".

### 2.1 The Symbolic (Headings)
*   **Font**: **Orbitron** (Google Fonts).
*   **Weight**: 900 (Black).
*   **Usage**: Page Titles, "CRITICAL SLOWING" Alerts.
*   **Effect**: `text-shadow: 0 0 20px rgba(0, 240, 255, 0.8)`.

### 2.2 The Imaginary (UI Elements)
*   **Font**: **Inter** (Google Fonts).
*   **Weight**: 400/600.
*   **Usage**: Buttons, Tooltips, Dashboard Labels.
*   **Tracking**: `-0.02em` (Tight and modern).

### 2.3 The Real (Data/Code)
*   **Font**: **JetBrains Mono**.
*   **Usage**: The CSV Data, The Python Code, The Math Equations.
*   **Feature**: Ligatures enabled (`=>`, `!=`).

---

## 3. The Color Palette (The Spectrum)

We define the colors semantically based on the Lacanian Registers.

| Token | Hex | Usage | Meaning |
| :--- | :--- | :--- | :--- |
| **`color-void`** | `#050505` | Background | The Empty Set ($\emptyset$). |
| **`color-hologram`** | `#00F0FF` | Primary UI | The Digital Twin (Ideal). |
| **`color-trauma`** | `#FF0055` | Alerts / $R$ | The Real (Pain/Error). |
| **`color-symbolic`** | `#FFD700` | The Path | The Law / Gold Standard. |
| **`color-imaginary`** | `#BD00FF` | Mischief | Illusion / Chaos. |
| **`color-glass`** | `rgba(255,255,255,0.05)` | Panels | The Medium. |

---

## 4. Glassmorphism (The Material)

The UI panels are not solid; they are **Frosted Glass**.

### 4.1 The CSS Class (`.glass-panel`)
```css
.glass-panel {
  background: rgba(10, 10, 10, 0.4);
  backdrop-filter: blur(24px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 
    0 8px 32px 0 rgba(0, 0, 0, 0.37),
    inset 0 0 0 1px rgba(255, 255, 255, 0.05);
}
```

---

## 5. Motion Physics (Framer Motion)

Nothing moves linearly. Everything has **Mass**.

### 5.1 The Standard Transition
```javascript
const spring = {
  type: "spring",
  stiffness: 200,
  damping: 20,
  mass: 1
};
```

### 5.2 The "Glitch" Animation
Used when Trauma > 0.8.
```javascript
const glitch = {
  x: [0, -2, 2, -1, 1, 0],
  y: [0, 1, -1, 0],
  transition: { duration: 0.2, repeat: Infinity }
};
```

---

## 6. UI Component Specs

### 6.1 `<NeonButton />`
*   **State**: Hover.
*   **Effect**: The border glows brighter (`box-shadow: 0 0 15px color-hologram`).
*   **Sound**: Triggers a short, high-pitched "Chirp" (Tone.js) on hover.

### 6.2 `<HealthRing />`
*   **Visual**: A 3D Torus rendered in Three.js.
*   **Behavior**: Rotates slowly.
*   **Data Binding**:
    *   **Color**: Interpolates from Blue (10) to Red (0).
    *   **Radius**: Pulses with the Heartbeat ($H(t)$).

### 6.3 `<TerminalBlock />`
*   **Visual**: A dark, monospaced code block with line numbers.
*   **Feature**: "Live Edit". The user can type into it, and the system re-calculates.
*   **Cursor**: A blinking block cursor (`_`).

---

## 7. Conclusion

This Design System ensures that the AEON Nexus is not just a "Tool"; it is an **Artifact**. It feels like it was retrieved from the year 2050.
