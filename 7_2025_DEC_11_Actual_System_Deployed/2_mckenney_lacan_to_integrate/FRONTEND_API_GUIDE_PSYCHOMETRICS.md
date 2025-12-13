# Frontend API Guide: Psychometrics

This guide details how to use the new **Psychometrics APIs** to visualize McKenney-Lacan dynamics in the frontend.

## Base URL
All endpoints are relative to `/api/psychometrics`.

## 1. Dissonance (Friction)
Calculates the interpersonal friction between two actors. Use this for **Relationship Graphs** or **Conflict Alerts**.

*   **Endpoint**: `GET /api/psychometrics/dissonance`
*   **Parameters**:
    *   `actor_a`: ID of the first actor (e.g., "APT29")
    *   `actor_b`: ID of the second actor (e.g., "Firewall_X")
*   **Example Request**:
    ```javascript
    const res = await fetch('/api/psychometrics/dissonance?actor_a=APT29&actor_b=CISO_Jim');
    const data = await res.json();
    ```
*   **Example Response**:
    ```json
    {
      "actor_a": "APT29",
      "actor_b": "CISO_Jim",
      "dissonance_score": 1.25,
      "interpretation": "High Friction"
    }
    ```

## 2. Group Hamiltonian (Energy)
Calculates the total energy of a group or incident. Use this for **Stability Gauges** or **Incident Severity**.

*   **Endpoint**: `POST /api/psychometrics/hamiltonian`
*   **Body**:
    ```json
    {
      "actorIds": ["APT29", "CISO_Jim", "Analyst_Alice"]
    }
    ```
*   **Example Response**:
    ```json
    {
      "group_size": 3,
      "energy": {
        "total": 5.4,
        "kinetic": 2.1,
        "potential": 3.3
      }
    }
    ```

## 3. Reflectivity Matrix (Influence)
Calculates the influence map of a group. Use this for **Heatmaps** or **Influence Network Visualizations**.

*   **Endpoint**: `POST /api/psychometrics/reflectivity`
*   **Body**:
    ```json
    {
      "actorIds": ["Alice", "Bob"]
    }
    ```
*   **Example Response**:
    ```json
    {
      "actors": ["Alice", "Bob"],
      "matrix": [
        [1.0, 0.2],
        [0.8, 1.0]
      ]
    }
    ```
    *   `matrix[i][j]` represents the influence of Actor J on Actor I.

## Error Handling
All endpoints return standard error objects:
```json
{
  "error": "Error message description",
  "details": "Stack trace or specific error info"
}
```
