# Maximus Optimus: Audio Specification (Neo-Riemannian)

**Document ID**: MAXIMUS_OPTIMUS_AUDIO_SPEC
**Classification**: HIGH THEORY // 9/10 EFFORT
**Target**: Option 3 (Visionary) & Option 5 (Evolved)
**Date**: 2025-11-29

---

## 1. Theoretical Foundation: The Tonnetz

We reject simple "Major/Minor" scales. We use **Neo-Riemannian Group Theory**.
The musical space is a **Tonnetz Grid** (Tone Network), where chords are connected by parsimonious voice-leading.

### 1.1 The Operations (PLR Group)
*   **P (Parallel)**: Maps a Major triad to its Parallel Minor (C Maj $\leftrightarrow$ c min).
    *   *Effect*: Darkening / Brightening.
    *   *Calculus Mapping*: High Trauma ($R > 0.8$) triggers rapid P-shifts (Mood Swings).
*   **L (Leading-Tone)**: Maps a Major triad to its Leading-Tone Minor (C Maj $\leftrightarrow$ e min).
    *   *Effect*: Emotional, poignant shift.
    *   *Calculus Mapping*: Mid Trauma ($0.3 < R < 0.6$) triggers L-shifts (Anxiety).
*   **R (Relative)**: Maps a Major triad to its Relative Minor (C Maj $\leftrightarrow$ a min).
    *   *Effect*: Smooth, logical transition.
    *   *Calculus Mapping*: Low Trauma ($R < 0.3$) triggers R-shifts (Stability).

---

## 2. The Algorithm: Trauma-Driven Harmony

The `MaximusEngine` does not play a "Song." It navigates the Tonnetz based on the **Riemannian Curvature ($R$)** of the system.

### 2.1 The Navigation Logic
$$ \text{NextState} = f(\text{CurrentState}, R(t)) $$

*   If $R(t) \approx 0$: Stay on Current Node (Static Harmony).
*   If $R(t)$ increases: Move to Neighbor Node (Single Operation: P, L, or R).
*   If $R(t)$ spikes: Jump to Distant Node (Compound Operation: PLP, RLP).

### 2.2 The Polyrhythmic Scheduler
Entropy ($H$) controls the **Time Domain**.
*   **Low Entropy ($H < 0.3$)**: Unison (Block Chords).
*   **Mid Entropy ($0.3 < H < 0.7$)**: Arpeggios (8th notes).
*   **High Entropy ($H > 0.7$)**: Polyrhythms (3 against 4, 5 against 4).

---

## 3. Implementation Details

*   **Language**: TypeScript (Strict Typing).
*   **Library**: `Tone.js` (Web Audio API wrapper).
*   **Architecture**: Class-based `MaximusEngine` with internal state (`currentTriad`).
*   **Performance**: Uses `Tone.Sampler` for realistic orchestral sounds, scheduled via `Tone.Transport` for precise timing.

---

## 4. Conclusion

This specification elevates the audio from "Sound Effects" to **Generative Art**.
It uses advanced music theory (Group Theory) to mathematically represent the psychological state of the system.
This is the "True Honest" application of the McKenney-Lacan Calculus.
