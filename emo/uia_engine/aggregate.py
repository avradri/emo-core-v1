cat > emo/uia_engine/aggregate.py <<'PY'
"""
UIA aggregation engine for EMO-Core.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass
class UIACoefficients:
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
    R_scalar: float
    B_scalar: float
    C_series: pd.Series
    S_series: pd.Series
    I_series: pd.Series
    M_E_series: pd.Series


@dataclass
class UIASnapshot:
    a_uia_series: pd.Series
    A_uia_bar: float
    terms: UIATerms
    coeffs: UIACoefficients


def default_uia_coefficients() -> UIACoefficients:
    return UIACoefficients()


def _ensure_series_like(x: float | pd.Series, index: pd.Index) -> pd.Series:
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
    if coeffs is None:
        coeffs = default_uia_coefficients()

    index = C_series.index
    if not S_series.index.equals(index) or not I_series.index.equals(index):
        raise ValueError(
            "C, S, and I series must share the same index for compute_a_uia()."
        )

    m_e_series = _ensure_series_like(M_E_scalar, index=index)

    dC = C_series.diff().fillna(0.0)
    dS = S_series.diff().fillna(0.0)
    dI = I_series.diff().fillna(0.0)

    dC_term = coeffs.gamma * coeffs.tau_c * dC
    dS_term = coeffs.delta * (dS / coeffs.S0)
    dI_term = coeffs.epsilon * (dI / coeffs.I0)

    R_term = coeffs.alpha * float(R_scalar)
    B_term = coeffs.beta * (coeffs.ell**2) * float(B_scalar)
    M_term = coeffs.eta * (m_e_series / coeffs.M0)

    a_uia_values = (
        R_term
        + B_term
        + dC_term.to_numpy()
        + dS_term.to_numpy()
        + dI_term.to_numpy()
        + M_term.to_numpy()
    )
    a_uia_series = pd.Series(a_uia_values, index=index, name="a_uia")

    A_uia_bar = float(np.nanmean(a_uia_series.to_numpy()))

    terms = UIATerms(
        R_scalar=float(R_scalar),
        B_scalar=float(B_scalar),
        C_series=C_series,
        S_series=S_series,
        I_series=I_series,
        M_E_series=m_e_series,
    )

    return UIASnapshot(
        a_uia_series=a_uia_series,
        A_uia_bar=A_uia_bar,
        terms=terms,
        coeffs=coeffs,
    )


__all__ = [
    "UIACoefficients",
    "UIATerms",
    "UIASnapshot",
    "compute_a_uia",
    "default_uia_coefficients",
]
PY
