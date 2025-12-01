# AEON Nexus: Technical Specification - Audio Sonification

**Document ID**: AEON_NEXUS_TECH_SPEC_AUDIO_SONIFICATION
**Parent Doc**: AEON_NEXUS_PRD_EXHAUSTIVE
**Date**: 2025-11-29
**Author**: AEON Design Bureau (Swarm Iota)

---

## 1. The Audio Architecture (Tone.js)

We use a **Multi-Channel Generative System**.
Each "Lane" in the CSV score corresponds to a specific Synthesizer.

### 1.1 The Instrument Rack
```javascript
import * as Tone from 'tone';

// 1. The Heartbeat (Column D)
// Sound: Deep, thumping kick drum.
export const heartbeatSynth = new Tone.MembraneSynth({
    pitchDecay: 0.05,
    octaves: 10,
    oscillator: { type: "sine" },
    envelope: {
        attack: 0.001,
        decay: 0.4,
        sustain: 0.01,
        release: 1.4,
        attackCurve: "exponential"
    }
}).toDestination();

// 2. The Mischief (Column F)
// Sound: High-pitched, metallic FM synthesis.
export const mischiefSynth = new Tone.FMSynth({
    harmonicity: 3,
    modulationIndex: 10,
    oscillator: { type: "sine" },
    envelope: { attack: 0.01, decay: 0.2 },
    modulation: { type: "square" },
    modulationEnvelope: { attack: 0.5, decay: 0.01 }
}).toDestination();

// 3. The Harmony (Column I)
// Sound: Warm, analog strings (Sawtooth with LowPass Filter).
export const harmonySynth = new Tone.PolySynth(Tone.Synth, {
    oscillator: { type: "fatsawtooth", count: 3, spread: 30 },
    envelope: { attack: 0.4, decay: 0.1, sustain: 0.5, release: 1 }
}).toDestination();
```

---

## 2. The Effects Chain (The Trauma)

When the system is stressed, we don't just change the notes; we degrade the *quality* of the audio.

### 2.1 The Trauma Bus
```javascript
const distortion = new Tone.Distortion(0.8);
const bitCrusher = new Tone.BitCrusher(4);
const reverb = new Tone.Reverb(2.5);

// Connect Synths to the Bus
heartbeatSynth.connect(distortion);
mischiefSynth.connect(bitCrusher);

// Control Logic
function updateEffects(traumaValue) {
    // traumaValue is 0.0 to 1.0 (from CSV Column S)
    distortion.wet.value = traumaValue; // More distortion as trauma rises
    bitCrusher.bits.value = 8 - (traumaValue * 4); // Lower bits = More noise
}
```

---

## 3. The Mapping Logic (Data to Sound)

We parse the CSV row and trigger events.

| CSV Column | Data Value | Audio Parameter | Effect |
| :--- | :--- | :--- | :--- |
| **D (Heartbeat)** | `1.0` (Regular) | `heartbeatSynth.triggerAttackRelease("C1", "8n")` | Steady Pulse |
| **D (Heartbeat)** | `0.4` (Failing) | `heartbeatSynth.triggerAttackRelease("C1", "16n")` | Rapid/Weak Pulse |
| **F (Mischief)** | `0.8` (High) | `mischiefSynth.set({ harmonicity: 10 })` | Screeching Tone |
| **I (Harmony)** | `Tonic (I)` | `harmonySynth.triggerAttack(["D3", "F#3", "A3"])` | D Major Chord |
| **I (Harmony)** | `Dim7` | `harmonySynth.triggerAttack(["C#3", "E3", "G3", "Bb3"])` | Diminished Chord |

---

## 4. The 4D Scrub Implementation

When the user drags the timeline slider:
1.  **Tone.Transport** jumps to the new time.
2.  **Granular Synthesis**: We cannot just "seek" a synth. We must re-trigger the state.
3.  **State Reconstruction**: The engine looks at the *previous* keyframe to determine active notes and re-attacks them with a fade-in to prevent clicking.
