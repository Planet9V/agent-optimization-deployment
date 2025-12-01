# Protocol E21: Text-to-Personality Extraction (The NLP Pipeline)

**Document ID**: E21_PROTOCOL_TEXT_TO_PERSONALITY
**Version**: 1.0 (Application)
**Date**: 2025-11-28
**Author**: AEON Research Division (Swarm 2 - The Analysts)
**Classification**: TOP SECRET // NOFORN // AEON EYES ONLY

---

## 1. Objective

To extract a high-dimensional **Psychometric Tensor** ($\mathbf{P}$) from unstructured text (Transcripts, Emails, Slack).
$$ \text{Text} \xrightarrow{f} \mathbf{P} \in \mathbb{R}^{4 \times 5 \times 3} $$
*   **Dimensions**: DISC (4) $\times$ Big 5 (5) $\times$ Lacan (3).

---

## 2. The Extraction Pipeline

### 2.1 Layer 1: Lexical Analysis (The Bag of Words)
We use **LIWC (Linguistic Inquiry and Word Count)** dictionaries to map words to traits.

| Trait | Marker Words | Weight ($w$) |
| :--- | :--- | :--- |
| **Dominance (D)** | "Must", "Now", "Result", "Fail", "I" | $+1.5$ |
| **Influence (I)** | "We", "Exciting", "Feel", "!", "Love" | $+1.2$ |
| **Steadiness (S)** | "Process", "Steady", "Plan", "Agree", "Team" | $+1.0$ |
| **Compliance (C)** | "Data", "Verify", "Incorrect", "Logic", "Rule" | $+1.5$ |
| **Neuroticism (N)** | "Worry", "Risk", "Afraid", "Wrong", "Maybe" | $+2.0$ |

**Algorithm**:
$$ P_{trait} = \frac{\sum_{w \in \text{Text}} \mathbb{I}(w \in \text{Dict}_{trait}) \cdot \text{Weight}(w)}{\text{Total Words}} $$

### 2.2 Layer 2: Syntactic Analysis (The Structure)
We analyze the *structure* of the sentences.

*   **Sentence Length**: Short/Punchy $\to$ High D. Long/Complex $\to$ High C.
*   **Voice**: Active Voice $\to$ High D/I. Passive Voice $\to$ High S/C.
*   **Punctuation**: Exclamation (!) $\to$ High I. Question (?) $\to$ High S. Period (.) $\to$ High D.

### 2.3 Layer 3: Semantic Analysis (The Meaning)
We use **BERT Embeddings** to classify the *intent* of the text.

*   **Intent: Command** $\to$ High D.
*   **Intent: Persuade** $\to$ High I.
*   **Intent: Support** $\to$ High S.
*   **Intent: Correct** $\to$ High C.

---

## 3. Lacanian Extraction (The Unconscious)

Extracting the **Lacanian Register** (RSI) requires deeper analysis.

### 3.1 The Real (R)
*   **Markers**: Gaps, Stuttering, Trauma, "Unspeakable", "Crash", "Panic".
*   **Detection**: High perplexity in the Language Model. The model *fails* to predict the next word.

### 3.2 The Symbolic (S)
*   **Markers**: Law, Code, Protocol, "The Father", "The Boss", "Policy".
*   **Detection**: High frequency of "Deontic Modals" (Must, Shall, Ought).

### 3.3 The Imaginary (I)
*   **Markers**: Ego, Mirror, "I am", "They are", Rivalry, Jealousy.
*   **Detection**: High usage of First Person Singular ("I") and Second Person ("You") in adversarial contexts.

---

## 4. The Output: The Psychometric Tensor

The final output is a JSON object ready for Neo4j ingestion.

```json
{
  "entity_id": "user_123",
  "timestamp": "2025-11-28T12:00:00Z",
  "psychometrics": {
    "DISC": { "D": 0.8, "I": 0.2, "S": 0.1, "C": 0.4 },
    "Big5": { "O": 0.7, "C": 0.9, "E": 0.3, "A": 0.2, "N": 0.6 },
    "Lacan": { "R": 0.1, "S": 0.8, "I": 0.1 }
  },
  "derived_traits": {
    "role": "The Beckmesser (High C, High S)",
    "risk_profile": "Rigid, Risk-Averse",
    "musical_key": "C Minor"
  }
}
```

---

## 5. Conclusion

This protocol allows us to turn the "Noise" of chat logs into the "Signal" of personality. It is the first step in the **McKenney-Lacan Calculus**.
