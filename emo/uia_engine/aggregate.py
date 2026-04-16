"""
UIA aggregation engine for EMO-Core.

This module implements a concrete, readable version of the UIA density

    a_UIA = α 𝓡[g_I] + β ℓ² ℬ
          + γ τ_C dC/dt
          + δ (1/S₀) dS/dt
          + ε (1/I₀) dI/dt
          + η (M_E / M₀),

and its coarse-grained counterpart Ȧ_UIA, as described in the UIA v2.0
and EMO v2.0 drafts.

For EMO-Core v1.0 we adopt the following pragmatic approximation:

- 𝓡[g_I] (informational curvature) is summarized as a scalar R_scalar
  for the time window of interest.
- ℬ (focusing bracket) is summarized as a scalar B_scalar.
- C, S, and I are pandas.Series indexed by time.
- M_E is treated as a scalar or a series aligned with C's index.

This is sufficient to produce a time series a_uia(t) and a coarse-
grained Ȧ_UIA for the window.

The design goal is clarity and faithfulness to the equation in the
paper rather than squeezing out every last bit of performance.
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass
class UIACoefficients:
    """
    Dimensionless coefficients and scales for the UIA density.

    The default values are deliberately simple and neutral; in practice,
    different interface classes (bench-top optics, biological systems,
    planetary cognition via EMO, etc.) will use different calibrated
    values. For EMO-Core v1.0 we just expose them explicitly.

    Parameters
    ----------
    alpha, beta, gamma, delta, epsilon, eta:
        Dimensionless weights for each term in a_UIA.
    ell:
        Characteristic length scale ℓ entering ℓ² ℬ.
    tau_c:
        Coherence time τ_C ≈ 1 / γ_dephase scaling dC/dt.
    S0, I0, M0:
        Reference scales for entropy, information, and semantic efficiency.
    """

    alpha: float = 1.0
    beta: float = 1.0
    gamma: float = 1.0
    delta: float = 1.0
    epsilon: float = 1.0
    eta: float = 1.0

    ell: float = 1.0
    tau_c: float = 1.0

    S0: float = 1.0
    I0: float = 1.0
    M0: float = 1.0


@dataclass
class UIATerms:
    """
    Container for the terms entering the UIA density.

    Parameters
    ----------
    R_scalar:
        Scalar summary of informational curvature 𝓡[g_I] over the window.
    B_scalar:
        Scalar summary of the focusing bracket ℬ over the window.
    C_series:
        Coherence time series C(t) indexed by time.
    S_series:
        Entropy-like time series S(t) indexed by time.
    I_series:
        Information-like time series I(t) indexed by time.
    M_E_series:
        Semantic efficiency M_E(t) aligned with C_series.index.
        For many applications this will be constant over the window.
    """

    R_scalar: float
    B_scalar: float
    C_series: pd.Series
    S_series: pd.Series
    I_series: pd.Series
    M_E_series: pd.Series


@dataclass
class UIASnapshot:
    """
    Result of a UIA aggregation over a time window.

    Parameters
    ----------
    a_uia_series:
        Time series of the local UIA density a_UIA(t).
    A_uia_bar:
        Coarse-grained Ȧ_UIA over the window (simple time average).
    terms:
        Underlying UIATerms instance used in the computation.
    coeffs:
        UIACoefficients used in the computation.
    """

    a_uia_series: pd.Series
    A_uia_bar: float
    terms: UIATerms
    coeffs: UIACoefficients


def default_uia_coefficients() -> UIACoefficients:
    """
    Return a default set of UIA coefficients.

    For EMO-Core v1.0 this is a simple all-ones configuration for the
    weights and scales, which keeps the implementation transparent.
    """
    return UIACoefficients()


def _ensure_series_like(x: float | pd.Series, index: pd.Index) -> pd.Series:
    """
    Utility: promote a scalar or Series to a Series aligned with `index`.
    """
    if isinstance(x, pd.Series):
        if not x.index.equals(index):
            return x.reindex(index).ffill().bfill()
        return x
    return pd.Series(float(x), index=index)


def compute_a_uia(
    R_scalar: float,
    B_scalar: float,
    C_series: pd.Series,
    S_series: pd.Series,
    I_series: pd.Series,
    M_E_scalar: float | pd.Series,
    coeffs: UIACoefficients | None = None,
) -> UIASnapshot:
    """
    Compute a_UIA(t) and Ȧ_UIA over a given time window.

    This is the main entry point for EMO-Core v1.0 and is used by tests
    and by the API layer.

    Parameters
    ----------
    R_scalar:
        Scalar informational curvature 𝓡[g_I] for the window.
    B_scalar:
        Scalar focusing bracket ℬ for the window.
