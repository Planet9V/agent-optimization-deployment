import json
import random
import math

# 1. The Tragic Structure
SCENES = [
    {"id": "ACT_1_KITCHEN", "length": 50, "base_R": 0.2, "base_H": 0.3},
    {"id": "ACT_1_MEMORY_1", "length": 30, "base_R": 0.1, "base_H": 0.5},
    {"id": "ACT_1_OFFICE", "length": 40, "base_R": 0.4, "base_H": 0.6},
    {"id": "ACT_2_HOWARD", "length": 60, "base_R": 0.7, "base_H": 0.8},
    {"id": "ACT_2_RESTAURANT", "length": 80, "base_R": 0.9, "base_H": 0.9},
    {"id": "ACT_2_GARDEN", "length": 40, "base_R": 0.95, "base_H": 0.2},
    {"id": "REQUIEM", "length": 20, "base_R": 0.0, "base_H": 0.1}
]

CHARACTERS = ["Willy", "Linda", "Biff", "Happy", "Charley", "Bernard", "Ben"]

# 2. The Neo-Riemannian Logic
def get_transformation(R):
    if R < 0.3: return "R" # Relative (Smooth)
    if R < 0.6: return "L" # Leading-Tone (Emotional)
    if R < 0.8: return "P" # Parallel (Dark)
    return "PLP" # Crisis Modulation

def generate_beat(scene_id, beat_num, base_R, base_H):
    # Add noise to metrics
    R = min(1.0, max(0.0, base_R + random.uniform(-0.1, 0.2)))
    H = min(1.0, max(0.0, base_H + random.uniform(-0.1, 0.1)))
    V = abs(math.sin(beat_num / 10.0))
    
    speaker = random.choice(CHARACTERS)
    
    return {
        "beat": beat_num,
        "scene": scene_id,
        "speaker": speaker,
        "metrics": {"H": round(H, 2), "R": round(R, 2), "V": round(V, 2)},
        "music": {
            "operation": get_transformation(R),
            "texture": "Polyrhythm" if H > 0.7 else "Monophonic"
        }
    }

# 3. The Generator Loop
def generate_full_play():
    full_score = {
        "title": "Death of a Salesman: Complete Symphonic Score",
        "engine": "Maximus Optimus",
        "total_beats": 0,
        "data": []
    }
    
    global_beat = 1
    
    for scene in SCENES:
        print(f"Generating {scene['id']}...")
        scene_data = {
            "id": scene['id'],
            "beats": []
        }
        
        for i in range(scene['length']):
            beat = generate_beat(scene['id'], global_beat, scene['base_R'], scene['base_H'])
            scene_data['beats'].append(beat)
            global_beat += 1
            
        full_score['data'].append(scene_data)
        
    full_score['total_beats'] = global_beat - 1
    return full_score

if __name__ == "__main__":
    score = generate_full_play()
    
    with open("DEATH_OF_A_SALESMAN_COMPLETE_SCORE.json", "w") as f:
        json.dump(score, f, indent=2)
        
    print(f"\nComplete Score Generated: {score['total_beats']} Beats.")
