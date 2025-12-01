# Primer 8: Quantum Mechanics (Hilbert Spaces & Operators)

**Document ID**: PRIMER_08_QUANTUM_MECHANICS_HILBERT
**Version**: 1.0 (Foundation)
**Date**: 2025-11-28
**Author**: AEON Research Division (Agent 8 - The Physicist)
**Classification**: UNCLASSIFIED // ACADEMIC REFERENCE

---

## 1. Hilbert Spaces ($\mathcal{H}$)

### 1.1 Definition
A **Hilbert Space** is a complete inner product space.
*   **State Vector**: $|\psi\rangle \in \mathcal{H}$.
*   **Superposition**: $|\psi\rangle = \alpha |0\rangle + \beta |1\rangle$.
*   **Normalization**: $\langle \psi | \psi \rangle = 1$.

### 1.2 Cyber Meaning
The state of a vulnerability is a vector in a Hilbert Space.
*   $|0\rangle$: Safe.
*   $|1\rangle$: Exploited.
*   Before measurement (audit), the state is a superposition.

---

## 2. Operators and Observables

### 2.1 Hermitian Operators ($\hat{A}$)
Observables correspond to Hermitian operators ($\hat{A} = \hat{A}^\dagger$).
*   **Eigenvalues**: The possible outcomes of a measurement.
*   **Expectation Value**: $\langle \hat{A} \rangle = \langle \psi | \hat{A} | \psi \rangle$.

### 2.2 The Hamiltonian ($\hat{H}$)
The operator corresponding to Total Energy.
$$ i\hbar \frac{\partial}{\partial t} |\psi\rangle = \hat{H} |\psi\rangle $$
*   **Cyber Meaning**: The Hamiltonian governs the time evolution of the risk.

---

## 3. Entanglement

### 3.1 Tensor Products
The state space of a composite system is $\mathcal{H}_A \otimes \mathcal{H}_B$.

### 3.2 Entangled States
A state that cannot be written as a product state $|\psi\rangle_A \otimes |\phi\rangle_B$.
*   **Bell State**: $\frac{1}{\sqrt{2}} (|00\rangle + |11\rangle)$.
*   **Cyber Meaning**: If System A and System B are entangled (share a dependency), measuring A (finding a bug) instantaneously collapses the state of B.

---

## 4. Application: Quantum Risk

We calculate the **Von Neumann Entropy** of the system.
$$ S = -\text{Tr}(\rho \ln \rho) $$
*   $\rho$: Density Matrix.
*   **Pure State**: $S = 0$ (Perfect Knowledge).
*   **Mixed State**: $S > 0$ (Uncertainty/Risk).

---

## 5. Conclusion

Quantum Mechanics is the physics of information. It teaches us that observation is not passive; it is active. It changes the state. In Cyber Security, the act of looking for a bug (Pen-Test) collapses the wavefunction of the system.
