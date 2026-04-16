from __future__ import annotations

from dataclasses import dataclass

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
    metadata: dict[str, str]


def compute_reciprocity_fluxes(
    buffering_proxy: pd.Series,
    selection_proxy: pd.Series,
) -> ReciprocityResult:
    """
    Very simple reciprocity flux estimator.

    Parameters
    ----------
    buffering_proxy:
        Time series representing exosomatic buffering
        (e.g., early-warning coverage, protective infrastructure investments).
    selection_proxy:
        Time series representing environmental selection pressure
        (e.g., disaster losses, mortality).

    Returns
    -------
    ReciprocityResult

    Notes
    -----
    In the full EMO / reciprocity program, R, J_B, and B relate to
    environmental challenge, buffering, and behavioral balance. Here we keep
    the first implementation intentionally lightweight and transparent.
    """
    b_mean = float(buffering_proxy.mean())
    s_mean = float(selection_proxy.mean())

    if s_mean == 0.0:
        ratio = 0.0
    else:
        ratio = b_mean / s_mean

    balance = b_mean - s_mean

    return ReciprocityResult(
        R=ratio,
        JB=b_mean,
        B=balance,
        metadata={
            "buffering_name": getattr(buffering_proxy, "name", "buffering_proxy") or "buffering_proxy",
            "selection_name": getattr(selection_proxy, "name", "selection_proxy") or "selection_proxy",
        },
    )
