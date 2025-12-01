import * as Tone from 'tone';

// --- 1. Mathematical Foundation: Neo-Riemannian Group Theory ---

type PitchClass = number; // 0-11 (C=0, C#=1, ...)
type Triad = [PitchClass, PitchClass, PitchClass];

class Tonnetz {
    // The 12 Major and 12 Minor Triads form the nodes of the Tonnetz Graph.
    // We navigate this graph using P, L, and R operations.

    static getMajorTriad(root: PitchClass): Triad {
        return [root, (root + 4) % 12, (root + 7) % 12];
    }

    static getMinorTriad(root: PitchClass): Triad {
        return [root, (root + 3) % 12, (root + 7) % 12];
    }

    // P (Parallel): C Major <-> c minor (Preserves 5th, moves 3rd by semitone)
    static transformP(triad: Triad): Triad {
        const [root, third, fifth] = triad;
        // Simplified logic for brevity: Inverts the third around the root/fifth axis
        const isMajor = (third - root + 12) % 12 === 4;
        return isMajor
            ? [root, (third - 1 + 12) % 12, fifth] // Major -> Minor
            : [root, (third + 1) % 12, fifth];     // Minor -> Major
    }

    // L (Leading-Tone): C Major <-> e minor (Preserves Minor 3rd, moves Root by semitone)
    static transformL(triad: Triad): Triad {
        const [root, third, fifth] = triad;
        const isMajor = (third - root + 12) % 12 === 4;
        return isMajor
            ? [(root - 1 + 12) % 12, third, fifth] // C Maj -> e min (C->B)
            : [(root + 1) % 12, third, fifth];     // e min -> C Maj (B->C)
    }

    // R (Relative): C Major <-> a minor (Preserves Major 3rd, moves Fifth by whole tone)
    static transformR(triad: Triad): Triad {
        const [root, third, fifth] = triad;
        const isMajor = (third - root + 12) % 12 === 4;
        return isMajor
            ? [root, third, (fifth + 2) % 12] // C Maj -> a min (G->A)
            : [root, third, (fifth - 2 + 12) % 12]; // a min -> C Maj (A->G)
    }
}

// --- 2. The Maximus Engine: Trauma-Driven Orchestration ---

interface CalculusMetrics {
    H: number; // Entropy (0-1) -> Density
    R: number; // Trauma (0-1) -> Harmonic Distance
    V: number; // Velocity (0-1) -> Dynamics
}

export class MaximusEngine {
    private currentTriad: Triad = [0, 4, 7]; // Start at C Major
    private sampler: Tone.Sampler;
    private isPlaying: boolean = false;

    constructor() {
        // High-Fidelity Sampler (Mock URLs for production structure)
        this.sampler = new Tone.Sampler({
            urls: {
                "C2": "cello_c2.mp3",
                "C4": "violin_c4.mp3",
                "C5": "celesta_c5.mp3"
            },
            baseUrl: "/samples/orchestra/",
            onload: () => console.log("Maximus Orchestral Samples Loaded")
        }).toDestination();
    }

    // The Core Logic: Mapping Calculus to Group Theory
    public update(metrics: CalculusMetrics, time: number) {
        if (!this.isPlaying) return;

        // 1. Determine Transformation based on Trauma (R)
        // Low Trauma = R (Relative, smooth)
        // Mid Trauma = L (Leading-Tone, emotional)
        // High Trauma = P (Parallel, dark) + Compound Operations (PL, PRP)

        let nextTriad = this.currentTriad;

        if (metrics.R < 0.3) {
            nextTriad = Tonnetz.transformR(this.currentTriad);
        } else if (metrics.R < 0.6) {
            nextTriad = Tonnetz.transformL(this.currentTriad);
        } else {
            // High Trauma: Rapid modulation (PLP sequence)
            nextTriad = Tonnetz.transformP(Tonnetz.transformL(this.currentTriad));
        }

        this.currentTriad = nextTriad;

        // 2. Orchestrate based on Entropy (H)
        // High Entropy = Polyrhythms (3 against 4)
        // Low Entropy = Unison

        const velocity = metrics.V * 0.8 + 0.2; // Min volume 0.2

        // Play the Triad
        const notes = nextTriad.map(pc => Tone.Frequency(pc + 60, "midi").toNote());

        if (metrics.H > 0.7) {
            // Polyrhythmic Arpeggio
            const now = Tone.now();
            this.sampler.triggerAttackRelease(notes[0], "8n", now, velocity);
            this.sampler.triggerAttackRelease(notes[1], "8n", now + 0.33, velocity); // Triplet feel
            this.sampler.triggerAttackRelease(notes[2], "8n", now + 0.66, velocity);
        } else {
            // Block Chord
            this.sampler.triggerAttackRelease(notes, "2n", undefined, velocity);
        }
    }

    public start() {
        Tone.start();
        Tone.Transport.start();
        this.isPlaying = true;
    }
}
