# API Specification: Psychometrics & Group Dynamics
**Version**: 1.0
**Base URL**: `/api/v1/psychometrics`

## Overview
This API exposes the mathematical models of the **McKenney-Lacan Theorem** to the frontend, allowing for real-time visualization of team dynamics, friction, and energy.

## Endpoints

### 1. Dissonance Calculation ($D_{ij}$)
Calculates the friction between two actors based on their Psychometric Tensors.

*   **GET** `/dissonance`
*   **Query Params**:
    *   `actor_a` (str): ID of first actor (e.g., "APT29")
    *   `actor_b` (str): ID of second actor (e.g., "CISO_Jim")
*   **Response**:
    ```json
    {
      "dissonance_score": 0.85,
      "components": {
        "disc_friction": 0.4,
        "ocean_friction": 0.45
      },
      "interpretation": "High Dissonance - Likely Conflict"
    }
    ```

### 2. Group Hamiltonian ($H$)
Calculates the total "Energy" of a group (Kinetic + Potential).

*   **POST** `/hamiltonian`
*   **Body**: `{"actor_ids": ["Alice", "Bob", "Charlie"]}`
*   **Response**:
    ```json
    {
      "total_energy": 12.5,
      "kinetic_energy": 5.0, // Action Rate
      "potential_energy": 7.5, // Latent Tension
      "stability_status": "Unstable"
    }
    ```

### 3. Reflectivity Matrix ($R$)
Returns the $N \times N$ matrix of influence/validation between group members (The "Hall of Mirrors").

*   **POST** `/reflectivity`
*   **Body**: `{"actor_ids": ["Alice", "Bob"]}`
*   **Response**:
    ```json
    {
      "matrix": [
        [1.0, 0.2], // Alice -> Alice, Alice -> Bob
        [-0.5, 1.0] // Bob -> Alice (Critical), Bob -> Bob
      ],
      "pathologies": ["Bob is hyper-critical of Alice"]
    }
    ```

### 4. Lacanian Topology Map
Returns the coordinates of an asset or event in the RSI (Real, Symbolic, Imaginary) space.

*   **GET** `/topology/{entity_id}`
*   **Response**:
    ```json
    {
      "entity_id": "CVE-2024-1234",
      "rsi_coordinates": {
        "real": 0.9, // Traumatic/Unsymbolizable
        "symbolic": 0.1,
        "imaginary": 0.0
      },
      "classification": "The Real (Trauma)"
    }
    ```
