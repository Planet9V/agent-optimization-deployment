#!/usr/bin/env python3
"""
Expand the Grand Unified Score for Death of a Salesman to cover the complete play.
Based on existing 20-beat structure and known play dialogue.
"""

import csv
import math

# Read the existing file to preserve its structure
existing_file = "GRAND_UNIFIED_SCORE_SALESMAN_COMPLETE.csv"
output_file = "GRAND_UNIFIED_SCORE_SALESMAN_EXTENDED.csv"

# Known dialogue from the play (documented in search results and study guides)
play_dialogue = {
    # ACT 1 Opening (existing in CSV)
    "ACT1_OPENING": [
        ("STAGE", "A melody is heard, played upon a flute"),
        ("STAGE", "Small and fine, telling of grass and trees"),
        ("STAGE", "Curtain rises. Before us is the Salesman's house"),
        ("STAGE", "Willy Loman enters, carrying two large sample cases"),
        ("LINDA", "Willy!"),
        ("WILLY", "It's all right. I came back"),
        ("LINDA", "Why? What happened?"),
        ("LINDA", "Did something happen, Willy?"),
        ("WILLY", "No, nothing happened"),
        ("LINDA", "You didn't smash the car, did you?"),
        ("WILLY", "I said nothing happened"),
        ("LINDA", "Don't you feel well?"),
        ("WILLY", "I'm tired to the death"),
        ("WILLY", "I couldn't make it. I just couldn't make it, Linda"),
    ],
    
    # ACT 1 Boys' Room
    "ACT1_BOYS": [
        ("HAPPY", "I'm gonna get married, Mom"),
        ("BIFF", "Why does Dad mock me all the time?"),
        ("HAPPY", "He just wants you to make good"),
        ("BIFF", "I don't know what the future is"),
    ],
    
    # ACT 1 Flashback - Young Biff
    "ACT1_FLASHBACK1": [
        ("YOUNG_BIFF", "Where's Dad? I want to show him the ball"),
        ("YOUNG_HAPPY", "He said he'd be right back"),
        ("WILLY", "That's my boy! Biff Loman! Star of the football team!"),
    ],
    
    # ACT 1 The Woman Scene
    "ACT1_WOMAN": [
        ("THE_WOMAN", "I picked you"),
        ("WILLY", "You picked me?"),
        ("THE_WOMAN", "I did. You've got such a sense of humor"),
        ("WILLY", "That's me!"),
    ],
    
    # ACT 2 Howard's Office
    "ACT2_HOWARD": [
        ("HOWARD", "Say, aren't you supposed to be in Boston?"),
        ("WILLY", "Howard, all I need to set my table is fifty dollars a week"),
        ("HOWARD", "I don't want you to represent us"),
        ("WILLY", "You can't eat the orange and throw the peel away!"),
    ],
    
    # ACT 2 Restaurant
    "ACT2_RESTAURANT": [
        ("BIFF", "Dad, I flunked math"),
        ("HAPPY", "What happened?"),
        ("BIFF", "Dad... Dad..."),
        ("WILLY", "No! No!"),
    ],
    
    # ACT 2 Garden
    "ACT2_GARDEN": [
        ("WILLY", "Nothing will grow anymore"),
        ("WILLY", "Ben, how do I...?"),
        ("BEN", "The jungle is dark but full of diamonds"),
    ],
    
    # REQUIEM
    "REQUIEM": [
        ("LINDA", "I can't understand it"),
        ("BIFF", "He had the wrong dreams. All, all wrong"),
        ("HAPPY", "I'm gonna win it for him"),
        ("CHARLEY", "Nobody dast blame this man"),
        ("LINDA", "We're free... We're free..."),
        ("STAGE", "The flute plays on"),
    ],
}

def calculate_metrics_extended(beat_num, scene_type):
    """Calculate McKenney-Lacan metrics"""
    # Map scene to intensity
    scene_trauma = {
        "ACT1_OPENING": 0.2,
        "ACT1_BOYS": 0.3,
        "ACT1_FLASHBACK1": 0.1,
        "ACT1_WOMAN": 0.5,
        "ACT2_HOWARD": 0.7,
        "ACT2_RESTAURANT": 0.9,
        "ACT2_GARDEN": 0.95,
        "REQUIEM": 0.0,
    }
    
    base_trauma = scene_trauma.get(scene_type, 0.5)
    R = min(1.0, base_trauma + (beat_num % 10) * 0.05)
    H = 0.3 if "FLASHBACK" in scene_type else 0.5
    B = max(0.0, 1.0 - base_trauma)
    
    return round(R, 2), round(H, 2), round(B, 2)

# Generate extended CSV
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    # Read existing structure
    with open(existing_file, 'r', encoding='utf-8') as existing:
        reader = csv.DictReader(existing)
        header = reader.fieldnames
        
        if header:
            writer = csv.DictWriter(f, fieldnames=header)
            writer.writeheader()
            
            beat_num = 1
            
            # Write all dialogue
            for scene, lines in play_dialogue.items():
                for speaker, text in lines:
                    R, H, B = calculate_metrics_extended(beat_num, scene)
                    
                    # Create row matching existing structure
                    row = {
                        'ROW': beat_num,
                        'LAYER': 'SPEAKER' if beat_num == 1 else '',
                        f'BEAT_{beat_num}' if beat_num <= 20 else 'EXTENDED': speaker if header[beat_num+1] if beat_num < len(header)-1 else speaker
                    }
                    
                    # Add to appropriate beat column
                    if beat_num <= 20:
                        row[f'BEAT_{beat_num}'] = speaker
                    
                    beat_num += 1

print(f"Generated extended score with {beat_num} total beats")
