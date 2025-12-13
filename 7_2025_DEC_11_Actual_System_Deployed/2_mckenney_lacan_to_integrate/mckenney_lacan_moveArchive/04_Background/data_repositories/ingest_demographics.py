#!/usr/bin/env python3
"""
ingest_demographics.py

Implements the 'Unified Cultural Calculus' for ingesting and processing
demographic data into Psychohistory mathematical objects.

Frameworks implemented:
1. Monad (Friston's Markov Blanket / Free Energy)
2. Dyad (Gottman's Differential Equations)
3. Population (Galam's Sociophysics / Ising Models)
"""

import math
import json
import os
import random
from typing import List, Dict, Optional
from dataclasses import dataclass

# --- 1. Monad Level (The Individual) ---

@dataclass
class Monad:
    """
    Represents an atomic individual unit in the Psychohistory graph.
    Mathematically defined by a Markov Blanket.
    """
    id: str
    internal_states: Dict[str, float]  # e.g., {'anxiety': 0.5, 'bias_susceptibility': 0.2}
    sensory_states: Dict[str, float]   # Inputs from the world
    active_states: Dict[str, float]    # Actions upon the world
    
    def calculate_free_energy(self) -> float:
        """
        Calculates Variational Free Energy (F).
        Simplified proxy: F = (Prediction - Sensation)^2
        Minimizing F means the Monad is effectively adapting to or predicting its environment.
        """
        # Simplified "surprise" calculation
        total_prediction_error = 0.0
        for key, sensory_val in self.sensory_states.items():
            # Assume internal state is the 'prediction' for the corresponding sensory key
            # If key not in internal states, prediction is 0 (high surprise)
            prediction = self.internal_states.get(key, 0.0)
            total_prediction_error += (prediction - sensory_val) ** 2
            
        return total_prediction_error

    def update_internal_state(self, learning_rate: float = 0.1):
        """
        Active Inference: Update internal beliefs to minimize free energy.
        """
        for key, sensory_val in self.sensory_states.items():
            current_belief = self.internal_states.get(key, 0.0)
            # Simple gradient descent step
            error = sensory_val - current_belief
            self.internal_states[key] = current_belief + (learning_rate * error)


# --- 2. Dyad Level (Relationships) ---

class DyadCalculator:
    """
    Calculates dynamics between two Monads using Differential Equations.
    Based on Gottman's Love Equations.
    """
    @staticmethod
    def calculate_influence(monad_a: Monad, monad_b: Monad) -> float:
        """
        Calculates the influence of Monad B on Monad A.
        dW/dt = I + rW + A(H)
        I = Natural disposition (Internal State)
        rW = Inertia
        A(H) = Influence function
        """
        # Simplified influence metric based on 'anxiety' resonance
        state_a = monad_a.internal_states.get('anxiety', 0.0)
        state_b = monad_b.internal_states.get('anxiety', 0.0)
        
        influence = 0.5 * state_b  # B's state directly adds to A's state (linear coupling)
        return state_a + influence


# --- 3. Population Level (Sociophysics) ---

class SociophysicsCalculator:
    """
    Calculates macro-level properties of a group of Monads.
    Based on Statistical Physics (Ising Model / Galam).
    """
    @staticmethod
    def calculate_social_temperature(population: List[Monad], trait_key: str = 'anxiety') -> float:
        """
        Social Temperature (T) represents volatility or variance in the population.
        High T = Chaotic, disordered processing.
        Low T = Rigid, frozen order.
        """
        values = [m.internal_states.get(trait_key, 0.0) for m in population]
        if not values:
            return 0.0
        
        mean_val = sum(values) / len(values)
        variance = sum((x - mean_val) ** 2 for x in values) / len(values)
        
        # In this metaphor, Variance is analogous to Temperature (Kinetic Energy spread)
        return variance

    @staticmethod
    def calculate_magnetization(population: List[Monad], opinion_key: str = 'support_patching') -> float:
        """
        Magnetization (M) represents the degree of consensus or polarization.
        Range [-1, 1].
        """
        # opinions assumed to be -1 (against) or 1 (for)
        # mapped from 'support_patching' 0.0 (against) to 1.0 (for)
        mag_sum = 0.0
        for m in population:
            val = m.internal_states.get(opinion_key, 0.5)
            spin = 1 if val > 0.5 else -1
            mag_sum += spin
            
        return mag_sum / len(population) if population else 0.0


# --- Data Ingestion Simulation ---

def load_world_bank_data(json_path: str) -> List[Monad]:
    """Load World Bank demographic JSON and create a Monad per region.
    Each region's attributes are mapped to internal_states for analysis.
    """
    if not os.path.isfile(json_path):
        raise FileNotFoundError(f"World Bank data file not found: {json_path}")
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    monads: List[Monad] = []
    for entry in data:
        region_id = entry.get('id', 'unknown')
        name = entry.get('name', 'unknown')
        attrs = entry.get('attributes', [])
        # Build a dict of metric -> value
        metrics = {attr.get('metric'): attr.get('value') for attr in attrs}
        internal = {
            'population': metrics.get('population_total', 0),
            'gdp_per_capita': metrics.get('gdp_per_capita', 0),
            'internet_usage': metrics.get('internet_usage_percent', 0),
            'literacy_rate': metrics.get('literacy_rate_adult_total', 0),
            'life_expectancy': metrics.get('life_expectancy_total', 0),
            'unemployment': metrics.get('unemployment_total', 0)
        }
        # Use unemployment as a proxy for anxiety, and literacy as support_patching
        internal_states = {
            'anxiety': internal['unemployment'] / 100.0,
            'support_patching': internal['literacy_rate'] / 100.0
        }
        monad = Monad(
            id=region_id,
            internal_states=internal_states,
            sensory_states={},
            active_states={}
        )
        monads.append(monad)
    return monads

def ingest_world_bank_data():
    """High‑level entry point to ingest real World Bank data.
    Returns a list of Monads representing each geographic region.
    """
    json_path = os.path.join(os.path.dirname(__file__), 'world_bank', 'data', 'demographic_knowledge_graph_data.json')
    return load_world_bank_data(json_path)

# Preserve original mock function for fallback

    """
    Simulates ingesting demographic data and creating Monads.
    """
    print("Simulating ingestion of Census Data...")
    
    # Mock data generation
    population_list = []
    behavior_types = ['Risk_Averse', 'Risk_Seeker', 'Complacent']
    
    for i in range(50):
        b_type = random.choice(behavior_types)
        
        # Initial states based on "Persona"
        if b_type == 'Risk_Averse':
            initial_anxiety = random.uniform(0.6, 0.9)
            support = random.uniform(0.7, 1.0)
        elif b_type == 'Risk_Seeker':
            initial_anxiety = random.uniform(0.1, 0.4)
            support = random.uniform(0.0, 0.4)
        else:
            initial_anxiety = random.uniform(0.3, 0.6)
            support = random.uniform(0.4, 0.6)
            
        m = Monad(
            id=f"census_id_{i}",
            internal_states={'anxiety': initial_anxiety, 'support_patching': support},
            sensory_states={'news_threat_level': 0.8}, # Global shared input
            active_states={}
        )
        population_list.append(m)
        
    return population_list


if __name__ == "__main__":
    # Prefer real data if available, otherwise fall back to mock
    try:
        pop = ingest_world_bank_data()
        print(f"Loaded {len(pop)} regions from World Bank data.")
    except Exception as e:
        print(f"World Bank data load failed ({e}), using mock data.")
        pop = ingest_census_data_mock()
        print(f"Created mock population of {len(pop)} Monads.")
    # Population already loaded above (real or mock data)

    
    # 2. Monad Calculus (Free Energy)
    sample_monad = pop[0]
    initial_fe = sample_monad.calculate_free_energy()
    print(f"\n[Monad] Sample ({sample_monad.id}) Initial Free Energy (Surprise): {initial_fe:.4f}")
    
    # Active Inference Learning Step
    sample_monad.update_internal_state(learning_rate=0.5)
    updated_fe = sample_monad.calculate_free_energy()
    print(f"[Monad] Sample Updated Free Energy (after learning): {updated_fe:.4f}")
    
    # 3. Sociophysics Calculus (Temperature & Magnetization)
    temp = SociophysicsCalculator.calculate_social_temperature(pop, 'anxiety')
    mag = SociophysicsCalculator.calculate_magnetization(pop, 'support_patching')
    
    print(f"\n[Population] Social Temperature (Anxiety Variance): {temp:.4f}")
    print(f"[Population] Magnetization (Consensus on Patching): {mag:.4f} (-1.0 to 1.0)")
    
    if abs(mag) > 0.3:
        print("=> High Polarization detected (Ferromagnetic phase)")
    else:
        print("=> Disordered opinion state (Paramagnetic phase)")
