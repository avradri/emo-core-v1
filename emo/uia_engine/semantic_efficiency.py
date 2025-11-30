from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass
class SemanticEfficiencyResult:
    """
    Semantic efficiency M_E result.
    """

    M_E: float
    metadata: dict


def compute_semantic_efficiency(
    risk_reduction: pd.Series,
    energy_use: pd.Series,
) -> SemanticEfficiencyResult:
    """
    Estimate semantic efficiency M_E = risk_reduction per Joule.

    Parameters
    ----------
    risk_reduction:
        Time series of reductions in risk / impact (e.g., disaster losses
        avoided, reductions in boundary transgression).
    energy_use:
        Time series of exosomatic energy used in mitigation/adaptation/
        governance actions.

    Returns
    -------
    SemanticEfficiencyResult
    """
    r = risk_reduction.dropna().astype(float)
    e = energy_use.dropna().astype(float)

    if r.empty or e.empty:
        return SemanticEfficiencyResult(0.0, {"definition": "empty"})

    # Align on common index
    df = (
        pd.concat({"risk": r, "energy": e}, axis=1)
        .dropna()
        .sort_index()
    )
    if df.empty:
        return SemanticEfficiencyResult(0.0, {"definition": "no_overlap"})

    total_risk_reduction = float(df["risk"].sum())
    total_energy = float(df["energy"].sum())
    if total_energy <= 0:
        return SemanticEfficiencyResult(0.0, {"definition": "zero_energy"})

    M_E = total_risk_reduction / total_energy
    return SemanticEfficiencyResult(
        M_E=M_E,
        metadata={"definition": "sum_risk_over_energy_v1.0"},
    )
