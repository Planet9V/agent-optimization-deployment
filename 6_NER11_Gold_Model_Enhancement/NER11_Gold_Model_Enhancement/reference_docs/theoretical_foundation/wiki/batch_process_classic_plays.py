#!/usr/bin/env python3
"""
McKenney-Lacan Calculus: Batch Processor for Classic Plays
Processes 10 public domain plays from Project Gutenberg
Generates comprehensive symphonicCalculus CSV scores
"""

import urllib.request
import re
import csv
import math
from pathlib import Path

# The 10 Plays to Process
PLAYS = {
    "hamlet": {
        "title": "Hamlet",
        "author": "William Shakespeare",
        "gutenberg_id": 1524,
        "url": "https://www.gutenberg.org/files/1524/1524-0.txt"
    },
    "king_lear": {
        "title": "King Lear",
        "author": "William Shakespeare", 
        "gutenberg_id": 1128,
        "url": "https://www.gutenberg.org/files/1128/1128-0.txt"
    },
    "macbeth": {
        "title": "Macbeth",
        "author": "William Shakespeare",
        "gutenberg_id": 1533,
        "url": "https://www.gutenberg.org/files/1533/1533-0.txt"
    },
    "oedipus_rex": {
        "title": "Oedipus Rex",
        "author": "Sophocles",
        "gutenberg_id": 31,
        "url": "https://www.gutenberg.org/files/31/31-0.txt"
    },
    "medea": {
        "title": "Medea",
        "author": "Euripides",
        "gutenberg_id": 35451,
        "url": "https://www.gutenberg.org/files/35451/35451-0.txt"
    },
    "a_dolls_house": {
        "title": "A Doll's House",
        "author": "Henrik Ibsen",
        "gutenberg_id": 2542,
        "url": "https://www.gutenberg.org/files/2542/2542-0.txt"
    },
    "hedda_gabler": {
        "title": "Hedda Gabler",
        "author": "Henrik Ibsen",
        "gutenberg_id": 4093,
        "url": "https://www.gutenberg.org/files/4093/4093-0.txt"
    },
    "cherry_orchard": {
        "title": "The Cherry Orchard",
        "author": "Anton Chekhov",
        "gutenberg_id": 7986,
        "url": "https://www.gutenberg.org/files/7986/7986-0.txt"
    },
    "miss_julie": {
        "title": "Miss Julie",
        "author": "August Strindberg",
        "gutenberg_id": 14347,
        "url": "https://www.gutenberg.org/files/14347/14347-0.txt"
    },
    "duchess_of_malfi": {
        "title": "The Duchess of Malfi",
        "author": "John Webster",
        "gutenberg_id": 2232,
        "url": "https://www.gutenberg.org/files/2232/2232-0.txt"
    }
}

class McKenneyLacanCalculus:
    """Calculate McKenney-Lacan metrics for dramatic dialogue"""
    
    @staticmethod
    def calculate_trauma_R(beat, total_beats, speaker, text):
        """Riemann Curvature - Trauma accumulation"""
        # Progress through play
        progress = beat / total_beats
        
        # Detect trauma keywords
        trauma_words = ['death', 'kill', 'murder', 'blood', 'revenge', 'mad', 'cursed', 'despair']
        trauma_count = sum(1 for word in trauma_words if word in text.lower())
        
        # Baseline trauma increase
        R = progress * 0.8 + trauma_count * 0.1
        return min(1.0, max(0.0, R))
    
    @staticmethod
    def calculate_entropy_H(text):
        """Entropy - Disorder/Chaos in communication"""
        # Questions indicate uncertainty
        question_count = text.count('?')
        # Exclamations indicate agitation
        exclamation_count = text.count('!')
        # Interruptions (dashes, ellipses)
        interruption_count = text.count('--') + text.count('...')
        
        H = (question_count * 0.2 + exclamation_count * 0.15 + interruption_count * 0.1)
        return min(1.0, max(0.0, H + 0.3))  # Baseline 0.3
    
    @staticmethod
    def calculate_baseline_B(beat, total_beats):
        """Baseline degradation - Order collapse"""
        # Degrades over the course of the play
        return max(0.0, 1.0 - (beat / total_beats))
    
    @staticmethod
    def calculate_arrhythmia_alpha(speaker, prev_speaker):
        """Arrhythmia - Dialogue rhythm disruption"""
        # Same speaker continuing = smooth (low α)
        # Speaker switch = rhythm change (high α)
        if speaker == prev_speaker:
            return 0.2
        else:
            return 0.7
    
    @staticmethod
    def neo_riemannian_operation(R):
        """Determine Neo-Riemannian transformation based on Trauma"""
        if R < 0.3:
            return "R"  # Relative - smooth
        elif R < 0.6:
            return "L"  # Leading-tone - emotional
        elif R < 0.8:
            return "P"  # Parallel - dark
        else:
            return "PLP"  # Crisis modulation

def download_play(url, filename):
    """Download play from Project Gutenberg"""
    print(f"Downloading {filename}...")
    try:
        with urllib.request.urlopen(url) as response:
            content = response.read().decode('utf-8')
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
        print(f"  ✓ Downloaded {filename}")
        return True
    except Exception as e:
        print(f"  ✗ Error downloading {filename}: {e}")
        return False

def parse_dialogue(text, play_title):
    """Parse play text into dialogue beats"""
    lines = text.split('\n')
    dialogue = []
    current_speaker = "STAGE"
    
    # Simple parser - looks for ALL CAPS speaker names followed by period or colon
    speaker_pattern = re.compile(r'^([A-Z][A-Z\s]+)[\.\:]')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check for speaker
        match = speaker_pattern.match(line)
        if match:
            current_speaker = match.group(1).strip()
            # Get the text after the speaker name
            text = line[match.end():].strip()
            if text:
                dialogue.append((current_speaker, text))
        elif line and not line.startswith('[') and not line.startswith('('):
            # Continuation of dialogue
            dialogue.append((current_speaker, line))
    
    return dialogue

def generate_csv_score(play_key, play_info):
    """Generate McKenney-Lacan CSV score for a play"""
    filename = f"{play_key}.txt"
    output_csv = f"MCKENNEY_LACAN_SCORE_{play_key.upper()}.csv"
    
    # Download if needed
    if not Path(filename).exists():
        if not download_play(play_info['url'], filename):
            return None
    
    # Read and parse
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()
    
    dialogue = parse_dialogue(text, play_info['title'])
    
    if not dialogue:
        print(f"  ✗ No dialogue found in {play_info['title']}")
        return None
    
    print(f"  Processing {len(dialogue)} beats...")
    
    # Generate CSV
    calc = McKenneyLacanCalculus()
    total_beats = len(dialogue)
    
    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Header
        writer.writerow([
            'BEAT', 'SPEAKER', 'TEXT',
            'TRAUMA_R', 'ENTROPY_H', 'BASELINE_B', 'ARRHYTHMIA_α',
            'NEO_RIEMANNIAN_OP', 'CLINICAL_HEALTH_SCORE'
        ])
        
        prev_speaker = ""
        
        for beat, (speaker, text) in enumerate(dialogue, 1):
            # Calculate metrics
            R = calc.calculate_trauma_R(beat, total_beats, speaker, text)
            H = calc.calculate_entropy_H(text)
            B = calc.calculate_baseline_B(beat, total_beats)
            α = calc.calculate_arrhythmia_alpha(speaker, prev_speaker)
            
            neo_op = calc.neo_riemannian_operation(R)
            
            # Clinical health score (inverse of trauma)
            health = int((1.0 - R) * 10)
            
            writer.writerow([
                beat,
                speaker,
                text[:200],  # Truncate long lines
                round(R, 2),
                round(H, 2),
                round(B, 2),
                round(α, 2),
                neo_op,
                f"{health}/10"
            ])
            
            prev_speaker = speaker
    
    print(f"  ✓ Generated {output_csv} ({total_beats} beats)")
    return output_csv

def main():
    """Process all 10 plays"""
    print("="*70)
    print("McKenney-Lacan Calculus: Batch Processor")
    print("Processing 10 Classic Plays from Project Gutenberg")
    print("="*70)
    
    output_dir = Path("classic_plays_scored")
    output_dir.mkdir(exist_ok=True)
    
    results = {}
    
    for play_key, play_info in PLAYS.items():
        print(f"\n[{list(PLAYS.keys()).index(play_key)+1}/10] {play_info['title']} by {play_info['author']}")
        try:
            csv_file = generate_csv_score(play_key, play_info)
            results[play_key] = csv_file if csv_file else "FAILED"
        except Exception as e:
            print(f"  ✗ Error: {e}")
            results[play_key] = "ERROR"
    
    # Summary
    print("\n" + "="*70)
    print("BATCH PROCESSING COMPLETE")
    print("="*70)
    successful = sum(1 for v in results.values() if v not in ["FAILED", "ERROR"])
    print(f"Successfully scored: {successful}/10 plays")
    
    for play_key, result in results.items():
        status = "✓" if result not in ["FAILED", "ERROR"] else "✗"
        print(f"  {status} {PLAYS[play_key]['title']}: {result}")

if __name__ == "__main__":
    main()
