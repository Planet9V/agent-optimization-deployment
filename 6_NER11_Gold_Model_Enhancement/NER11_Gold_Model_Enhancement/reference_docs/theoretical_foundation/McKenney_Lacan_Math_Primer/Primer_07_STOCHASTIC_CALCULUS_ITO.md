# Primer 7: Stochastic Calculus (Itô Processes & Martingales)

**Document ID**: PRIMER_07_STOCHASTIC_CALCULUS_ITO
**Version**: 1.0 (Foundation)
**Date**: 2025-11-28
**Author**: AEON Research Division (Agent 7 - The Probabilist)
**Classification**: UNCLASSIFIED // ACADEMIC REFERENCE

---

## 1. Brownian Motion (Wiener Process)

### 1.1 Definition
A continuous-time stochastic process $W_t$ such that:
1.  $W_0 = 0$.
2.  Increments $W_t - W_s$ are independent and Gaussian $\mathcal{N}(0, t-s)$.
3.  Paths are continuous but nowhere differentiable (Fractal).

### 1.2 Cyber Meaning
Brownian Motion models the "Random Walk" of a user or an attacker in the network.
*   **Drift**: The intentional movement (Goal).
*   **Diffusion**: The noise/uncertainty.

---

## 2. Itô Calculus

### 2.1 The Itô Integral
Since $dW_t \sim \sqrt{dt}$, standard calculus fails ($dW_t^2 = dt$).
We define the stochastic integral:
$$ I(t) = \int_0^t \Delta_u dW_u $$

### 2.2 Itô's Lemma
The "Chain Rule" for stochastic processes.
$$ df(t, X_t) = \left( \frac{\partial f}{\partial t} + \mu \frac{\partial f}{\partial x} + \frac{1}{2} \sigma^2 \frac{\partial^2 f}{\partial x^2} \right) dt + \sigma \frac{\partial f}{\partial x} dW_t $$
*   **Cyber Meaning**: Calculating the rate of change of "Risk" ($f$) given the volatility of the "Threat Landscape" ($X_t$).

---

## 3. Stochastic Differential Equations (SDEs)

### 3.1 Geometric Brownian Motion
$$ dS_t = \mu S_t dt + \sigma S_t dW_t $$
Used to model asset prices.
*   **Cyber Meaning**: Modeling the "Value at Risk" (VaR) of a data asset over time.

### 3.2 Ornstein-Uhlenbeck Process
Mean-reverting process.
$$ dX_t = \theta (\mu - X_t) dt + \sigma dW_t $$
*   **Cyber Meaning**: Modeling "Security Posture." If it drifts too far from the mean (Policy), the "Spring Force" ($\theta$) pulls it back (Auto-Remediation).

---

## 4. Martingales

### 4.1 Definition
A process where the expected future value equals the current value.
$$ E[M_{t+s} | \mathcal{F}_t] = M_t $$
*   **Fair Game**: No arbitrage.

### 4.2 Application: Cyber Insurance
We use Martingale Pricing Theory to price "Cyber Risk Options."
*   **Girsanov Theorem**: Changing the measure to make the discounted risk process a martingale.

---

## 5. Conclusion

Stochastic Calculus allows us to model the "Fog of War." It proves that in a volatile environment, the "Average" behavior is irrelevant; the *Volatility* (Variance) drives the risk. Itô's Lemma gives us the tool to differentiate through the noise.
