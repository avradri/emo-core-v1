from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

import pandas as pd


@dataclass
class ReciprocityResult:
    """
    Reciprocity flux result.

    R:
        Ratio of exosomatic buffering vs environmental selection.
    JB:
        Buffering current analogue (J_B).
    B:
        Coarse-grained focusing / balance term.
    """

    R: float
    JB: float
    B: float
    metadata: Dict[str, str]


def compute_reciprocity_fluxes(
    buffering_proxy: pd.Series,
    selection_proxy: pd.Series,
) -> ReciprocityResult:
    """
    Very simple reciprocity flux estimator.

    Parameters
    ----------
    buffering_proxy:
        Time series representing exosomatic buffering (e.g., early-warning
        coverage, protective infrastructure investments).
    selection_proxy:
        Time series representing environmental selection pressure
        (e.g., disaster losses, mortality).

    Returns
    -------
    ReciprocityResult

    Notes
    -----
    In the full EMO / reciprocity program, R, J_B, and B relate to
    coarse-grained balances between buffering and selection. Here we
    approximate:

        JB ~ mean(buffering_proxy)
        B  ~ mean(selection_proxy)
        R  ~ JB / max(B, eps)

    This gives a single scalar R > 1 when buffering dominates,
    R < 1 when selection dominates. 
    """
    bp = buffering_proxy.dropna().astype(float)
    sp = selection_proxy.dropna().astype(float)
    if bp.empty or sp.empty:
        return ReciprocityResult(1.0, 0.0, 0.0, {"definition": "empty"})

    JB = float(bp.mean())
    B = float(sp.mean())
    eps = 1e-9
    R = JB / max(B, eps) if B > 0 else float("inf")

    return ReciprocityResult(
        R=R,
        JB=JB,
        B=B,
        metadata={"definition": "mean_ratio_v1.0"},
    )
