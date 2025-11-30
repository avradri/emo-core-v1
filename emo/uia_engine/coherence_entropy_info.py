from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass
class CoherenceEntropyInfo:
    """
    Bundle of coherence C(t), entropy S(t), and information I(t) series.
    """

    C: pd.Series
    S: pd.Series
    I: pd.Series
    metadata: dict


def coherence_from_gwi(gwi_series: pd.Series, smoothing_window: int = 7) -> pd.Series:
    """
    Map a GWI series in [0,1] to a smoothed coherence C(t) in [0,1].
    """
    if gwi_series.empty:
        return gwi_series
    c = gwi_series.rolling(smoothing_window, min_periods=1).mean()
    return c.clip(0.0, 1.0)


def effective_entropy(boundary_indicators: pd.DataFrame) -> pd.Series:
    """
    Compute a crude "effective entropy" over planetary boundary indicators.

    We treat each column as a normalised indicator in [0,1] and compute:

        S(t) = - sum_i p_i log p_i

    with p_i proportional to the indicator value + epsilon.
    """
    if boundary_indicators.empty:
        return pd.Series(dtype=float)

    eps = 1e-9
    x = boundary_indicators.fillna(0.0).clip(lower=0.0)
    sums = x.sum(axis=1) + eps
    p = x.divide(sums, axis=0) + eps
    s_values = -np.sum(p * np.log(p), axis=1)
    return pd.Series(s_values, index=boundary_indicators.index, name="entropy")


def information_rate_from_skill(skill_series: pd.Series) -> pd.Series:
    """
    Convert a forecast skill series into an information-rate proxy dI/dt.

    We simply take the positive differences as "informational gains".
    """
    s = skill_series.dropna().astype(float)
    if s.empty:
        return pd.Series(dtype=float)
    diffs = s.diff().fillna(0.0)
    pos = diffs.clip(lower=0.0)
    return pd.Series(pos, index=s.index, name="dI_dt")


def bundle_coherence_entropy_info(
    gwi_series: pd.Series,
    boundary_indicators: pd.DataFrame,
    skill_series: pd.Series,
) -> CoherenceEntropyInfo:
    C = coherence_from_gwi(gwi_series)
    S = effective_entropy(boundary_indicators)
    I = information_rate_from_skill(skill_series)

    return CoherenceEntropyInfo(
        C=C,
        S=S,
        I=I,
        metadata={"definition": "emo_uia_bundle_v1.0"},
    )
