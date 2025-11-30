from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass
class FocusingResult:
    """
    Result of a coarse-grained focusing / circulation computation.
    """

    B: float  # bracket
    B_tilde: float  # dimensionless normalised bracket
    metadata: dict


def compute_focusing_bracket(
    expansion: pd.Series,
    shear: pd.Series | None = None,
    vorticity: pd.Series | None = None,
) -> FocusingResult:
    """
    Compute a highly simplified focusing bracket ℬ and its normalised
    version ~ℬ from time series of effective expansion, shear and vorticity.

    In cosmological FLRW models, ~ℬ = 3(1+q). :contentReference[oaicite:29]{index=29}
    Here we treat expansion as a proxy H, with:

        ℬ ~ 3 H^2

    and ~ℬ normalised by H^2.
    """
    H = expansion.dropna().astype(float)
    if H.empty:
        return FocusingResult(0.0, 0.0, {"definition": "empty"})

    H_mean = float(H.mean())
    B = 3.0 * H_mean**2
    B_tilde = 3.0  # B / H^2

    return FocusingResult(
        B=B,
        B_tilde=B_tilde,
        metadata={"definition": "flrw_proxy_v1.0"},
    )
