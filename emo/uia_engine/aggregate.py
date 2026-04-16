from __future__ import annotations

from dataclasses import dataclass

from .models import InterfaceState


@dataclass
class UIAWeights:
    """
    Dimensionless weights for the UIA aggregation.

    Defaults are intentionally simple and can be calibrated later against
    empirical or theoretical constraints.
    """

    alpha: float = 1.0
    beta: float = 1.0
    gamma: float = 1.0
    delta: float = 1.0
    epsilon: float = 1.0
    eta: float = 1.0


def aggregate_uia(
    state: InterfaceState,
    weights: UIAWeights | None = None,
) -> float:
    """
    Compute a coarse-grained UIA score from an InterfaceState.

    The local UIA density is treated here as the weighted sum:

        a_UIA =
            alpha   * informational_curvature
          + beta    * focusing_term
          + gamma   * coherence_rate
          + delta   * entropy_rate
          + epsilon * information_rate
          + eta     * semantic_efficiency

    This function is deliberately lightweight and deterministic so it can be
    reused across demos, tests, and orchestration code.
    """
    if weights is None:
        weights = UIAWeights()

    return (
        weights.alpha * state.informational_curvature
        + weights.beta * state.focusing_term
        + weights.gamma * state.coherence_rate
        + weights.delta * state.entropy_rate
        + weights.epsilon * state.information_rate
        + weights.eta * state.semantic_efficiency
    )


__all__ = ["UIAWeights", "aggregate_uia"]
