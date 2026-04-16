from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass
class SMFResult:
    """
    Self-Model Fidelity (SMF) result.
    """

    smf_score: float
    lag_days: int
    metadata: dict[str, str]


def compute_smf(
    model: pd.Series,
    realised: pd.Series,
    max_lag_days: int = 365,
) -> SMFResult:
    """
    Compute a simple Self-Model Fidelity (SMF) score.
    """
    if model.empty or realised.empty:
        return SMFResult(0.0, 0, {"definition": "empty"})

    df = (
        pd.concat({"model": model, "realised": realised}, axis=1)
        .dropna()
        .sort_index()
    )
    if df.empty:
        return SMFResult(0.0, 0, {"definition": "no_overlap"})

    model_vals = df["model"].to_numpy(dtype=float)
    real_vals = df["realised"].to_numpy(dtype=float)

    n = len(df)
    max_lag = min(max_lag_days, n - 1)
    best_corr = -1.0
    best_lag = 0

    for lag in range(-max_lag, max_lag + 1):
        if lag < 0:
            model_slice = model_vals[-lag:]
            real_slice = real_vals[: len(model_slice)]
        elif lag > 0:
            model_slice = model_vals[: n - lag]
            real_slice = real_vals[lag:]
        else:
            model_slice = model_vals
            real_slice = real_vals

        if len(model_slice) < 2:
            continue

        corr = float(np.corrcoef(model_slice, real_slice)[0, 1])
        if corr > best_corr:
            best_corr = corr
            best_lag = lag

    smf_score = (best_corr + 1.0) / 2.0 if best_corr > -1 else 0.0

    return SMFResult(
        smf_score=smf_score,
        lag_days=best_lag,
        metadata={"definition": "max_lagged_corr_v1.0"},
        )
