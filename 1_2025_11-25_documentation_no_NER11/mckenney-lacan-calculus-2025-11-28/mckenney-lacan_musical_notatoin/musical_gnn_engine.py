import random
import json
import math

# 1. The RUV-Swarm Entity Matrix
ENTITIES = {
    "Chef": {"Instrument": "Cello", "Role": "Orchestrator", "Range": "Low", "Clef": "Bass"},
    "Scout": {"Instrument": "Violin", "Role": "Explorer", "Range": "High", "Clef": "Treble"},
    "Hunter": {"Instrument": "Percussion", "Role": "Enforcer", "Range": "Rhythmic", "Clef": "Neutral"},
    "Scribe": {"Instrument": "Oboe", "Role": "Recorder", "Range": "Mid", "Clef": "Alto"},
    "Jester": {"Instrument": "Synthesizer", "Role": "Disruptor", "Range": "Variable", "Clef": "Treble"}
}

# 2. The Calculus Metrics (Input Data Simulation)
def generate_metrics(cycle):
    # Simulate a "Crisis" wave (Sine wave with noise)
    t = cycle / 10.0
    entropy = 0.5 + 0.4 * math.sin(t) + random.uniform(-0.1, 0.1)
    trauma = max(0, math.sin(t * 2) * entropy)
    velocity = abs(math.cos(t))
    return {"H": entropy, "R": trauma, "V": velocity}

# 3. The GNN Mapping Logic (The "Brain")
class MusicalGNN:
    def __init__(self):
        self.weights = {e: 1.0 for e in ENTITIES} # Adaptive weights

    def map_to_score(self, cycle, metrics):
        score_slice = {"cycle": cycle, "metrics": metrics, "notes": []}
        
        for entity, config in ENTITIES.items():
            # Activation Function: Does this entity play?
            activation = metrics["H"] * self.weights[entity] + random.uniform(-0.2, 0.2)
            
            if activation > 0.6: # Threshold
                # Pitch Mapping (Trauma -> Dissonance)
                base_pitch = 60 # Middle C
                if config["Range"] == "High": base_pitch += 12
                if config["Range"] == "Low": base_pitch -= 12
                
                # Trauma adds accidentals (sharps/flats)
                pitch_offset = int(metrics["R"] * 12) 
                note = base_pitch + pitch_offset
                
                # Dynamics (Velocity -> Volume)
                volume = int(metrics["V"] * 127)
                
                score_slice["notes"].append({
                    "entity": entity,
                    "instrument": config["Instrument"],
                    "note": note,
                    "volume": volume,
                    "duration": "4n"
                })
                
                # Feedback Loop: If Jester plays during high trauma, reinforce connection
                if entity == "Jester" and metrics["R"] > 0.8:
                    self.weights["Jester"] += 0.1

        return score_slice

# 4. The Simulation Loop (100 Cycles)
def run_simulation():
    gnn = MusicalGNN()
    full_score = []
    
    print("Running 100 Cycles of Symphonic Calculus...")
    for i in range(100):
        metrics = generate_metrics(i)
        slice_data = gnn.map_to_score(i, metrics)
        full_score.append(slice_data)
        
    return full_score

# 5. SWOT Analysis Generator
def generate_swot(score_data):
    # Analyze the score for density, dissonance, and rhythm
    total_notes = sum(len(s["notes"]) for s in score_data)
    avg_dissonance = sum(s["metrics"]["R"] for s in score_data) / len(score_data)
    
    return {
        "Strengths": [
            "Direct mapping of Trauma ($R$) to Pitch Dissonance.",
            f"High dynamic range (Velocity mapped to Volume). Avg Vol: {int(total_notes/100)}",
            "Adaptive Jester role reinforces during crisis."
        ],
        "Weaknesses": [
            "Rhythmic complexity is limited to 4n (Quarter notes).",
            "Percussion mapping needs specific MIDI drum map."
        ],
        "Opportunities": [
            "Export to MusicXML for real orchestra.",
            "Real-time sonification of live cyber attacks."
        ],
        "Threats": [
            "Listener fatigue due to high dissonance (Avg R: {:.2f}).".format(avg_dissonance)
        ]
    }

if __name__ == "__main__":
    score = run_simulation()
    swot = generate_swot(score)
    
    output = {
        "score": score,
        "swot": swot
    }
    
    with open("symphonic_calculus_score.json", "w") as f:
        json.dump(output, f, indent=2)
        
    print("\nSimulation Complete.")
    print("SWOT Analysis:")
    for k, v in swot.items():
        print(f"{k}: {v}")
