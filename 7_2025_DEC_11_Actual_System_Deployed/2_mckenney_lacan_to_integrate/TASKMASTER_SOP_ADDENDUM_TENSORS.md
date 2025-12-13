# SOP Addendum: Psychometric Tensor Ingestion
**Parent SOP**: `TASKMASTER_NER11_GOLD_COMPLETE_v2.0.md`
**Enhancement**: E27-Tensor-Upgrade

## 1. Overview
This addendum defines the procedure for calculating and ingesting **Psychometric Tensors** (Axiom 1) during the Entity Extraction phase. This ensures that every `Actor` and `Group` entity in the Knowledge Graph has a corresponding personality profile.

## 2. The "Comedy" Heuristic (Tensor Generation)

Since we cannot administer personality tests to threat actors, we use a **Stereotype Heuristic** based on the Actor Type and Description.

### 2.1 Heuristic Rules

| Actor Type | Keyword Match | Stereotype | Tensor Profile (DISC + OCEAN) |
| :--- | :--- | :--- | :--- |
| **APT / State** | "APT", "State", "Ministry", "Bureau" | **The Bureaucrat** | High C, High S, Low N. Methodical, slow, persistent. |
| **Cybercrime** | "Gang", "Ransom", "Cartel" | **The Mercenary** | High D, High I, High N. Aggressive, loud, volatile. |
| **Hacktivist** | "Anonymous", "Front", "Army" | **The Zealot** | High I, High O, Low A. Ideological, expressive, disagreeable. |
| **Script Kiddie** | "Lulz", "Sec", "Team" | **The Chaos Agent** | High I, High N, Low C. Erratic, attention-seeking, sloppy. |
| **Insider** | "Employee", "Contractor" | **The Disgruntled** | High N, Low A, Low S. Resentful, stressed, unstable. |

### 2.2 Python Implementation Logic

```python
def generate_tensor(actor_name, description):
    # Default: Neutral
    tensor = [0.5] * 9 
    
    desc_lower = description.lower()
    name_lower = actor_name.lower()
    
    if "apt" in name_lower or "state" in desc_lower:
        # The Bureaucrat
        tensor = [0.6, 0.3, 0.8, 0.9,  0.4, 0.9, 0.2, 0.3, 0.2]
        
    elif "ransom" in desc_lower or "gang" in name_lower:
        # The Mercenary
        tensor = [0.9, 0.7, 0.3, 0.4,  0.5, 0.3, 0.7, 0.2, 0.6]
        
    # ... (Add other heuristics)
    
    return tensor
```

## 3. Ingestion Procedure

1.  **Extract**: Identify `Actor` or `Group` entity.
2.  **Classify**: Apply Heuristic Rules to determine Stereotype.
3.  **Generate**: Create the 9-dimensional float array.
4.  **Store**:
    *   **Neo4j**: Set `a.psychometric_tensor` property.
    *   **Qdrant**: Add to `payload.psychometric_tensor`.

## 4. Quality Assurance
*   **Check**: Ensure no tensor values exceed [0.0, 1.0].
*   **Verify**: "APT29" should *never* have Low Conscientiousness (C < 0.5).

## 5. Continuous Learning (The "Loop")

The **Neural Council** requires that these tensors are not static. They must evolve as we observe new behavior.

### 5.1 The Update Trigger
Run the update script whenever a **Significant Event** occurs:
1.  **Change in TTPs** (e.g., An APT uses a new, sloppy tool).
2.  **Public Statement** (e.g., A manifesto is released -> analyze for Openness/Neuroticism).
3.  **Failed Attack** (e.g., Panic behavior -> Increase Neuroticism).

### 5.2 Execution Procedure
Use the `scripts/logic/update_tensor.py` utility.

```bash
# Example: APT29 acts impulsively (High I, Low C)
# Event Tensor: [0.4, 0.9, 0.2, 0.1, 0.5, 0.1, 0.8, 0.4, 0.9]
# Learning Rate: 0.2 (Significant shift)

python scripts/logic/update_tensor.py "APT29" "0.4,0.9,0.2,0.1,0.5,0.1,0.8,0.4,0.9" 0.2
```

### 5.3 The Math (Bayesian Drift)
We use a weighted moving average to "drift" the personality:
$$ T_{new} = (1 - \alpha)T_{old} + \alpha T_{event} $$

This ensures that one outlier event doesn't rewrite the entire personality, but a *pattern* of events will gradually shift the profile.

