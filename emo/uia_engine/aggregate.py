from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import numpy as np
import pandas as pd


@dataclass
class UIASnapshot:
    """
    Snapshot of a_UIA and Ȧ_UIA for a given time window.
    """

    a_uia_series: pd.Series
    A_uia_bar: float
    metadata: dict


def compute_a_uia(
    R_scalar: float,
    B_scalar: float,
    C_series: pd.Series,
    S_series: pd.Series,
    I_series: pd.Series,
    M_E_scalar: float,
    alpha: float = 1.0,
    beta: float = 1.0,
    gamma: float = 1.0,
    delta: float = -1.0,
    epsilon: float = 1.0,
    eta: float = 1.0,
    S0: Optional[float] = None,
    I0: Optional[float] = None,
) -> UIASnapshot:
    """
    Compute a_UIA(t) from its constituent terms.

    This is a direct implementation of the v2.0 UIA density:

        a_UIA
          = α R[g_I]
          + β ℓ^2 ℬ
          + γ τ_C dC/dt
          + δ (1/S0) dS/dt
          + ε (1/I0) dI/dt
          + η (M_E/M0)

    with several simplifications:

    - ℓ^2 is absorbed into β.
    - τ_C and M0 are absorbed into γ and η.
    - R[g_I] and ℬ are scalars aggregated over the chosen window.
    """
    # We treat R and B as scalars; C, S, I as time series.
    # Compute derivatives numerically.
    C = C_series.sort_index()
    S = S_series.sort_index()
    I = I_series.sort_index()

    if C.empty or S.empty or I.empty:
        # Degenerate case: just pack scalars
        a_val = alpha * R_scalar + beta * B_scalar + eta * M_E_scalar
        series = pd.Series([a_val], index=[pd.Timestamp.utcnow()], name="a_UIA")
        return UIASnapshot(series, float(a_val), {"definition": "degenerate"})

    def _dt(x: pd.Series) -> pd.Series:
        return x.diff().fillna(0.0)

    dC_dt = _dt(C)
    dS_dt = _dt(S)
    dI_dt = _dt(I)

    S0 = S0 if S0 is not None else float(S.abs().mean() or 1.0)
    I0 = I0 if I0 is not None else float(I.abs().mean() or 1.0)

    a_vals = (
        alpha * R_scalar
        + beta * B_scalar
        + gamma * dC_dt
        + delta * (dS_dt / S0)
        + epsilon * (dI_dt / I0)
        + eta * M_E_scalar
    )

    a_series = pd.Series(a_vals, index=C.index, name="a_UIA")

    A_bar = float(a_series.mean())

    return UIASnapshot(
        a_uia_series=a_series,
        A_uia_bar=A_bar,
        metadata={
            "definition": "uia_v2_proxy_v1.0",
            "alpha": alpha,
            "beta": beta,
            "gamma": gamma,
            "delta": delta,
            "epsilon": epsilon,
            "eta": eta,
        },
    )
