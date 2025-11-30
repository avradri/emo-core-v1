from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

import numpy as np
import pandas as pd


@dataclass
class SynergyResult:
    """
    Result container for approximate synergy / O-information.

    For v1.0 we implement a simple, Gaussian-inspired synergy proxy:
    we look at how much variance is explained jointly vs individually.
    """

    synergy_index: float
    per_stream_contribution: Dict[str, float]
    metadata: Dict[str, str]


def compute_gaussian_synergy(df: pd.DataFrame) -> SynergyResult:
    """
    Compute a crude synergy proxy from a multivariate time series.

    Parameters
    ----------
    df:
        DataFrame with columns representing streams, e.g.
        ["news", "papers", "policy", "ew_alerts"].

    Returns
    -------
    SynergyResult

    Notes
    -----
    True O-information requires higher-order information decompositions.
    Here we use a tractable approximation:

    - Fit a covariance matrix Σ.
    - Compute total variance V_total = trace(Σ).
    - Compute sum of individual variances V_diag = sum(diag(Σ)).
    - Define synergy_index = (V_diag - V_total) / max(V_diag, eps).

    Intuition:

    - If variables are independent, Σ is diagonal → V_diag ≈ V_total → index ≈ 0.
    - If there is strong shared structure, Σ has off-diagonals;
      V_total < V_diag, and the index becomes positive.

    This is not a full O-information, but provides a consistent scalar
    for early versions of EMO. :contentReference[oaicite:25]{index=25}
    """
    if df.empty or df.shape[1] < 2:
        return SynergyResult(0.0, {}, {"definition": "degenerate"})

    x = df.dropna().to_numpy(dtype=float)
    if x.shape[0] < 2:
        return SynergyResult(0.0, {}, {"definition": "degenerate"})

    cov = np.cov(x, rowvar=False)
    v_diag = float(np.trace(np.diag(np.diag(cov))))
    v_total = float(np.trace(cov))
    eps = 1e-9
    synergy_index = (v_diag - v_total) / max(v_diag, eps)

    # Simple contribution: variance share
    variances = np.diag(cov)
    total_var = float(variances.sum()) or 1.0
    per_stream = {
        col: float(v / total_var) for col, v in zip(df.columns, variances)
    }

    return SynergyResult(
        synergy_index=synergy_index,
        per_stream_contribution=per_stream,
        metadata={"definition": "gaussian_proxy_v1.0"},
    )
