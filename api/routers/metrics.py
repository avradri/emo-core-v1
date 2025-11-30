from __future__ import annotations

from datetime import datetime, timedelta
from typing import Dict

import pandas as pd
from fastapi import APIRouter

from emo.organismality import compute_organismality_index
from emo.synergy import compute_gaussian_synergy
from emo.gwi import compute_gwi
from emo.smf import compute_smf
from emo.info_time import compute_information_time

router = APIRouter()


@router.get("/oi")
async def get_organismality_demo() -> Dict:
    """
    Demo endpoint returning a toy OI calculation over synthetic data.
    """
    treaties = pd.DataFrame(
        {
            "region": ["World"],
            "treaty_count": [120],
        }
    )
    conflicts = pd.DataFrame(
        {
            "region": ["World"],
            "conflict_deaths": [10_000],
        }
    )
    res = compute_organismality_index(treaties, conflicts)
    return {
        "global_oi": res.global_oi,
        "regional_oi": res.regional_oi,
        "metadata": res.metadata,
    }


@router.get("/synergy")
async def get_synergy_demo() -> Dict:
    """
    Demo endpoint returning a toy synergy calculation.
    """
    idx = pd.date_range("2020-01-01", periods=100, freq="D")
    df = pd.DataFrame(
        {
            "news": range(100),
            "papers": [i * 0.8 for i in range(100)],
            "policy": [i * 0.5 for i in range(100)],
        },
        index=idx,
    )
    res = compute_gaussian_synergy(df)
    return {
        "synergy_index": res.synergy_index,
        "per_stream_contribution": res.per_stream_contribution,
        "metadata": res.metadata,
    }


@router.get("/gwi")
async def get_gwi_demo() -> Dict:
    """
    Demo endpoint returning a toy GWI timeseries and ignition events.
    """
    idx = pd.date_range("2020-01-01", periods=60, freq="D")
    streams = pd.DataFrame(
        {
            "news": [1] * 20 + [10] * 20 + [2] * 20,
            "pageviews": [2] * 20 + [8] * 20 + [3] * 20,
        },
        index=idx,
    )
    res = compute_gwi(streams)
    return {
        "gwi_series": res.gwi_series.to_dict(),
        "events": [t.isoformat() for t in res.events],
        "metadata": res.metadata,
    }


@router.get("/smf")
async def get_smf_demo() -> Dict:
    """
    Demo endpoint returning a toy Self-Model Fidelity (SMF) score.
    """
    idx = pd.date_range("2010", periods=20, freq="Y")
    model = pd.Series(range(20), index=idx)
    realised = pd.Series([v * 1.1 for v in range(20)], index=idx)
    res = compute_smf(model, realised)
    return {
        "smf_score": res.smf_score,
        "lag_days": res.lag_days,
        "metadata": res.metadata,
    }


@router.get("/tau_i")
async def get_tau_i_demo() -> Dict:
    """
    Demo endpoint returning a toy information-time τ_I.
    """
    idx = pd.date_range("2000", periods=10, freq="Y")
    skill = pd.Series([0.4, 0.41, 0.45, 0.44, 0.47, 0.5, 0.51, 0.52, 0.52, 0.53], index=idx)
    res = compute_information_time(skill)
    return {
        "tau_i": res.tau_i,
        "total_positive_increments": res.total_positive_increments,
        "metadata": res.metadata,
    }
