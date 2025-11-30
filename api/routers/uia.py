from __future__ import annotations

from typing import Dict

import pandas as pd
from fastapi import APIRouter

from emo.uia_engine.aggregate import compute_a_uia
from emo.uia_engine.coherence_entropy_info import (
    bundle_coherence_entropy_info,
)
from emo.uia_engine.focusing import compute_focusing_bracket
from emo.uia_engine.semantic_efficiency import compute_semantic_efficiency
from emo.reciprocity import compute_reciprocity_fluxes

router = APIRouter()


@router.get("/summary")
async def get_uia_summary_demo() -> Dict:
    """
    Demo endpoint computing a synthetic UIA snapshot over toy data.

    This ties together:
    - reciprocity fluxes (R, J_B, B)
    - focusing bracket ℬ
    - coherence C(t), entropy S(t), and information-flow dI/dt
    - semantic efficiency M_E
    - aggregated a_UIA and Ȧ_UIA
    """
    idx = pd.date_range("2020-01-01", periods=30, freq="D")

    buffering = pd.Series([1 + i * 0.01 for i in range(30)], index=idx)
    selection = pd.Series([1.5 - i * 0.01 for i in range(30)], index=idx)
    reciprocity = compute_reciprocity_fluxes(buffering, selection)

    expansion = pd.Series([0.01] * 30, index=idx)
    focusing = compute_focusing_bracket(expansion)

    boundary_indicators = pd.DataFrame(
        {
            "climate": [0.8] * 30,
            "biosphere": [0.7] * 30,
        },
        index=idx,
    )
    skill_series = pd.Series(
        [0.5 + i * 0.005 for i in range(30)],
        index=idx,
    )
    # Use a simple GWI proxy here
    gwi_series = pd.Series(
        [0.2] * 10 + [0.8] * 10 + [0.3] * 10,
        index=idx,
        name="gwi",
    )

    cei = bundle_coherence_entropy_info(gwi_series, boundary_indicators, skill_series)
    sem_eff = compute_semantic_efficiency(
        risk_reduction=pd.Series([0.1] * 30, index=idx),
        energy_use=pd.Series([1.0] * 30, index=idx),
    )

    snapshot = compute_a_uia(
        R_scalar=reciprocity.R,
        B_scalar=focusing.B,
        C_series=cei.C,
        S_series=cei.S,
        I_series=cei.I,
        M_E_scalar=sem_eff.M_E,
    )

    return {
        "a_UIA": snapshot.a_uia_series.to_dict(),
        "A_UIA_bar": snapshot.A_uia_bar,
        "components": {
            "R": reciprocity.R,
            "B": focusing.B,
            "M_E": sem_eff.M_E,
        },
        "metadata": snapshot.metadata,
    }
