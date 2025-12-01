import random
import json
import time
import math

# 1. The Divergent Gene Pool (Language Model Simulation)
ADJECTIVES = [
    "Quantum", "Recursive", "Holographic", "Fractal", "Neural", 
    "Symbiotic", "Entropic", "Living", "Glitch", "Hyper", 
    "Traumatic", "Symphonic", "Topological", "Infinite", "Self_Assembling"
]
NOUNS = [
    "Cosmology", "Lattice", "Void", "Nexus", "Weave", 
    "Membrane", "Orchestra", "Swarm", "Cathedral", "Tapestry",
    "Manifold", "Singularity", "Horizon", "Cortex", "Rhizome"
]

# Initial "Seed" Concepts
GENOME = {
    "Navigation": ["3D_Cosmology", "2D_Dashboard", "Text_Search", "Hybrid_Dual_Mode"],
    "Audio": ["Generative_ToneJS", "Pre_Recorded_Loops", "Silent", "Data_Sonification_Raw"],
    "Visuals": ["Trauma_Shader_GLSL", "Standard_Material", "Wireframe", "Point_Cloud"],
    "Data_Ingest": ["Real_Time_Stream", "Batch_Process", "Static_Dump", "On_Demand_Query"],
    "Interaction": ["First_Person_Fly", "God_Mode_Orbit", "Text_Command_Line", "VR_Hands"]
}

# 2. The Graph Memory (Simulated GNN)
class KnowledgeGraph:
    def __init__(self):
        self.weights = {} # (Concept_A, Concept_B) -> Weight
        self.concepts = set()

    def reinforce(self, c1, c2, reward):
        key = tuple(sorted((c1, c2)))
        if key not in self.weights:
            self.weights[key] = 0.0
        self.weights[key] += reward # Hebbian Learning: Neurons that fire together, wire together.

    def get_synergy(self, c1, c2):
        key = tuple(sorted((c1, c2)))
        return self.weights.get(key, 0.0)

GNN = KnowledgeGraph()

# 3. The Agents (Neural Nodes)
class Agent:
    def __init__(self, name, bias_keywords):
        self.name = name
        self.bias = bias_keywords # List of strings this agent "likes"

    def evaluate(self, candidate):
        score = 0
        # 1. Semantic Match (Activation)
        for feature in candidate.values():
            for keyword in self.bias:
                if keyword.lower() in feature.lower():
                    score += 10
        
        # 2. Novelty Bonus (Divergent Thinking)
        for feature in candidate.values():
            if feature not in GENOME: # If it's a mutated gene
                score += 5 
        
        return score

AGENTS = [
    Agent("Alpha (Visionary)", ["Quantum", "Holographic", "Fractal", "Generative", "Trauma"]),
    Agent("Beta (Engineer)", ["Batch", "Standard", "Wireframe", "Static", "Efficient"]),
    Agent("Gamma (Gamer)", ["First_Person", "VR", "God_Mode", "Immersion", "Glitch"]),
    Agent("Delta (Academic)", ["Text", "Search", "Index", "Citation", "Recursive"]),
    Agent("Omega (Synthesizer)", ["Hybrid", "Symbiotic", "Living", "Nexus", "Balance"])
]

# 4. The Evolutionary Loop
def mutate(feature_category):
    # 20% Chance of Divergent Mutation (Creating a NEW concept)
    if random.random() < 0.2:
        new_concept = f"{random.choice(ADJECTIVES)}_{random.choice(NOUNS)}"
        return new_concept
    # 80% Chance of Selection from existing Genome
    return random.choice(GENOME[feature_category])

def run_evolution(generations=100):
    population = []
    print(f"Initializing Evolutionary Swarm with {generations} generations...")
    
    for gen in range(generations):
        # A. Crossover & Mutation
        candidate = {
            "Navigation": mutate("Navigation"),
            "Audio": mutate("Audio"),
            "Visuals": mutate("Visuals"),
            "Data_Ingest": mutate("Data_Ingest"),
            "Interaction": mutate("Interaction")
        }
        
        # B. Agent Evaluation
        scores = {}
        total_score = 0
        for agent in AGENTS:
            s = agent.evaluate(candidate)
            scores[agent.name] = s
            total_score += s
            
        # C. GNN Feedback Loop (Hebbian Learning)
        # If the total score is high, reinforce the connections between these features
        if total_score > 30: # Threshold for "Good Idea"
            features = list(candidate.values())
            for i in range(len(features)):
                for j in range(i+1, len(features)):
                    GNN.reinforce(features[i], features[j], 0.1)
                    
        # D. GNN Synergy Bonus
        # Add bonus points if these features have worked well together in the past
        synergy_bonus = 0
        features = list(candidate.values())
        for i in range(len(features)):
            for j in range(i+1, len(features)):
                synergy_bonus += GNN.get_synergy(features[i], features[j])
        
        final_score = total_score + synergy_bonus
        
        # E. Record
        population.append({
            "generation": gen + 1,
            "genome": candidate,
            "score": final_score,
            "synergy": synergy_bonus,
            "novelty": any(v not in GENOME[k] for k, v in candidate.items())
        })
        
        # F. Feedback: Add successful mutations to the Genome Pool
        if final_score > 50 and population[-1]['novelty']:
            for k, v in candidate.items():
                if v not in GENOME[k]:
                    GENOME[k].append(v) # The species evolves!

    # 5. Selection
    population.sort(key=lambda x: x['score'], reverse=True)
    return population[:5], population

if __name__ == "__main__":
    top_5, history = run_evolution(100)
    
    with open("evolutionary_log.json", "w") as f:
        json.dump(history, f, indent=2)
        
    with open("top_5_evolved.json", "w") as f:
        json.dump(top_5, f, indent=2)
        
    print("\nTop 5 Evolved Species:")
    for p in top_5:
        print(f"Gen {p['generation']}: Score {p['score']:.2f} (Synergy {p['synergy']:.2f})")
        print(f"  Genome: {p['genome']}")

