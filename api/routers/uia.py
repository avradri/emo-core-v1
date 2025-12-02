# api/routers/uia.py
from __future__ import annotations

from dataclasses import asdict
from typing import Any, Dict, List, Optional

import pandas as pd
from fastapi import APIRouter
from pydantic import BaseModel

from emo.services.metrics import MetricEngine

router = APIRouter(prefix="/uia", tags=["uia"])

_engine = MetricEngine()


class UIARequest(BaseModel):
    """
    Request payload for computing a UIA summary for a given interface/time window.

    interface_id:
        Identifier for the interface Σ (e.g. "global_human_earth").
    R_scalar:
        Scalar informational curvature 𝓡[g_I] over the window.
    B_scalar:
        Scalar focusing bracket ℬ over the window.
    C:
        Coherence time series C(t).
    S:
        Entropy-like time series S(t).
    I:
        Information-like time series I(t).
    timestamps:
        Optional ISO8601 timestamps. If omitted, a simple integer index
        is used.
    M_E:
        Semantic efficiency M_E for the window (scalar). For many
        applications this is a reasonable approximation.
    metadata:
        Optional free-form metadata.
    """

    interface_id: str
    R_scalar: float
    B_scalar: float
    C: List[float]
    S: List[float]
    I: List[float]
    timestamps: Optional[List[str]] = None
    M_E: float = 0.0
    metadata: Optional[Dict[str, Any]] = None


@router.post("/summary")
async def compute_uia_summary(payload: UIARequest) -> Dict[str, Any]:
    """
    Compute a UIASummary from scalar R, B and time series C, S, I.

    This endpoint is designed to be easy to call from lab code: assemble
    your C/S/I time series on the client side, estimate R and B for the
    same window, and POST them here to obtain a coarse-grained Ȧ_UIA and
    the corresponding a_UIA(t) series.
    """
    if not (len(payload.C) == len(payload.S) == len(payload.I)):
        raise ValueError("C, S, and I must have the same length.")

    if payload.timestamps is not None:
        if len(payload.timestamps) != len(payload.C):
            raise ValueError("timestamps length must match C/S/I length.")
        index = pd.to_datetime(payload.timestamps)
    else:
        # Simple integer index is fine if timestamps are not provided.
        index = pd.RangeIndex(len(payload.C))

    C_series = pd.Series(payload.C, index=index)
    S_series = pd.Series(payload.S, index=index)
    I_series = pd.Series(payload.I, index=index)

    summary = _engine.uia_from_series(
        interface_id=payload.interface_id,
        R_scalar=payload.R_scalar,
        B_scalar=payload.B_scalar,
        C_series=C_series,
        S_series=S_series,
        I_series=I_series,
        M_E=payload.M_E,
        metadata=payload.metadata,
    )

    # Convert dataclass to dict for FastAPI/JSON.
    return asdict(summary)
