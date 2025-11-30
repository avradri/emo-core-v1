from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

import numpy as np
import pandas as pd


@dataclass
class OrganismalityResult:
    """
    Result container for the Organismality Index (OI).

    The current implementation is intentionally simple: it combines
    cooperative signals (e.g., treaty density) and conflict signals
    (e.g., battle deaths) into a bounded index in [0, 1].
    """

    global_oi: float
    regional_oi: Dict[str, float]
    metadata: Dict[str, str]


def _safe_norm(series: pd.Series) -> pd.Series:
    s = series.astype(float).fillna(0.0)
    if s.max() == s.min():
        return pd.Series(0.0, index=s.index)
    return (s - s.min()) / (s.max() - s.min())


def compute_organismality_index(
    treaties: pd.DataFrame,
    conflicts: pd.DataFrame,
    region_col: str = "region",
    treaties_col: str = "treaty_count",
    conflicts_col: str = "conflict_deaths",
) -> OrganismalityResult:
    """
    Compute a simple Organismality Index (OI).

    Parameters
    ----------
    treaties:
        DataFrame with columns [region_col, treaties_col].
    conflicts:
        DataFrame with columns [region_col, conflicts_col].
    region_col:
        Column used to join regions.
    treaties_col, conflicts_col:
        Column names for cooperative / destructive activity.

    Returns
    -------
    OrganismalityResult

    Notes
    -----
    This is a *toy* OI for v1.0:

    - Treaties are assumed to be pro-organismal (cooperation).
    - Conflict deaths are anti-organismal (fragmentation).
    - We normalise both, then define:

        OI_region = treaties_norm * (1 - conflicts_norm)

    More sophisticated versions can include sanction effectiveness,
    alliance stability, disinformation shocks, etc. 
    """

    df = (
        treaties[[region_col, treaties_col]]
        .merge(conflicts[[region_col, conflicts_col]], on=region_col, how="outer")
        .fillna(0.0)
    )

    t_norm = _safe_norm(df[treaties_col])
    c_norm = _safe_norm(df[conflicts_col])

    oi_region = (t_norm * (1.0 - c_norm)).clip(0.0, 1.0)
    df["oi"] = oi_region

    regional = {r: float(v) for r, v in zip(df[region_col], df["oi"])}

    # Global OI: mean of regional scores
    global_oi = float(oi_region.mean()) if len(oi_region) else 0.0

    return OrganismalityResult(
        global_oi=global_oi,
        regional_oi=regional,
        metadata={
            "definition": "toy_v1.0",
            "description": "Treaties vs conflict deaths, normalised by region.",
        },
    )
