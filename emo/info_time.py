from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

import numpy as np
import pandas as pd


@dataclass
class InfoTimeResult:
    """
    Information-time τ_I result.

    tau_i:
        Scalar clock in "information-time units".
    total_positive_increments:
        Sum of positive skill improvements.
    """

    tau_i: float
    total_positive_increments: float
    metadata: Dict[str, str]


def compute_information_time(skill_series: pd.Series) -> InfoTimeResult:
    """
    Compute a simple information-time τ_I from a forecast skill series.

    Parameters
    ----------
    skill_series:
        Time series of forecast skill (e.g., anomaly correlation),
        where higher is better.

    Returns
    -------
    InfoTimeResult

    Notes
    -----
    EMO v0.1 defines τ_I as the cumulative sum of positive skill
    improvements over time; we follow the same idea, normalising
    by the time span. 
    """
    s = skill_series.dropna().astype(float)
    if s.empty:
        return InfoTimeResult(0.0, 0.0, {"definition": "empty"})

    diffs = s.diff().fillna(0.0)
    pos_increments = diffs.clip(lower=0.0)
    total_pos = float(pos_increments.sum())

    # Normalise by number of steps for a crude τ_I
    tau_i = total_pos / max(len(s) - 1, 1)

    return InfoTimeResult(
        tau_i=tau_i,
        total_positive_increments=total_pos,
        metadata={"definition": "cum_positive_skill_v1.0"},
    )
