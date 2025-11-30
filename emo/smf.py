from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

import numpy as np
import pandas as pd


@dataclass
class SMFResult:
    """
    Self-Model Fidelity (SMF) result.

    smf_score:
        Global alignment between self-model trajectories and realised
        trajectories, in [0, 1].
    lag_days:
        Lag (in days) at which alignment is maximal.
    """

    smf_score: float
    lag_days: int
    metadata: Dict[str, str]


def compute_smf(
    model: pd.Series,
    realised: pd.Series,
    max_lag_days: int = 365,
) -> SMFResult:
    """
    Compute a simple Self-Model Fidelity (SMF) score.

    Parameters
    ----------
    model:
        Time series representing the self-model output (e.g., a 1.5°C pathway).
    realised:
        Time series of realised values (e.g., actual emissions).
    max_lag_days:
        Max lag (both positive and negative) to consider.

    Returns
    -------
    SMFResult
    """
    if model.empty or realised.empty:
        return SMFResult(0.0, 0, {"definition": "empty"})

    # Align on common index
    df = (
        pd.concat({"model": model, "realised": realised}, axis=1)
        .dropna()
        .sort_index()
    )
    if df.empty:
        return SMFResult(0.0, 0, {"definition": "no_overlap"})

    model_vals = df["model"].to_numpy(dtype=float)
    real_vals = df["realised"].to_numpy(dtype=float)

    # Map lag in days to integer steps assuming regular spacing
    n = len(df)
    max_lag = min(max_lag_days, n - 1)
    best_corr = -1.0
    best_lag = 0

    for lag in range(-max_lag, max_lag + 1):
        if lag < 0:
            m = model_vals[-lag:]
            r = real_vals[: len(m)]
        elif lag > 0:
            m = model_vals[: n - lag]
            r = real_vals[lag:]
        else:
            m = model_vals
            r = real_vals
        if len(m) < 2:
            continue
        corr = float(np.corrcoef(m, r)[0, 1])
        if corr > best_corr:
            best_corr = corr
            best_lag = lag

    smf_score = (best_corr + 1.0) / 2.0 if best_corr > -1 else 0.0

    return SMFResult(
        smf_score=smf_score,
        lag_days=best_lag,
        metadata={"definition": "max_lagged_corr_v1.0"},
    )
