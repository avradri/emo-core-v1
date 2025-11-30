# api/routers/uia.py

from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from emo.twin_hooks import (
    DestineHDAClient,
    DestineScenarioMetadata,
    summarise_scenarios_cognitively,
    discover_climate_dt_scenarios,
)

router = APIRouter(prefix="/uia", tags=["uia"])


class DestineUIASummary(BaseModel):
    """
    Prototype UIA-style summary over DestinE climate scenarios.

    This is **not** the full UIA engine – it is a v1.0-friendly summary that
    aggregates EMO metrics into a single climate cognition index that can be
    shown as a gauge on the dashboard. 
    """

    twin_id: str = "ClimateDT"
    n_scenarios: int

    oi_mean_avg: Optional[float]
    smf_global_avg: Optional[float]
    omega_synergy_avg: Optional[float]
    gwi_ignitions_total: Optional[int]
    tau_i_accel_ratio_avg: Optional[float]

    uia_proxy: Optional[float]


def _safe_mean(df, col: str) -> Optional[float]:
    if col not in df.columns:
        return None
    series = df[col].dropna()
    if series.empty:
        return None
    return float(series.mean())


@router.get(
    "/destine/summary",
    response_model=DestineUIASummary,
    summary="Prototype UIA summary for DestinE climate scenarios",
)
def destine_uia_summary(
    q: str = Query(
        "climate",
        description="Free-text search term for DestinE climate DT collections.",
    ),
    datetime_start: Optional[str] = Query(
        None,
        description="Optional start datetime (YYYY-MM-DD or full ISO8601).",
    ),
    datetime_end: Optional[str] = Query(
        None,
        description="Optional end datetime (YYYY-MM-DD or full ISO8601).",
    ),
    limit: int = Query(
        10,
        ge=1,
        le=50,
        description="Maximum number of scenarios to include.",
    ),
    forecast_skill_csv: Optional[str] = Query(
        "data/ecmwf_headline_scores.csv",
        description="Optional forecast-skill CSV for τ_I overlays.",
    ),
    gwi_topic: str = Query(
        "climate change",
        description="Topic used for GWI overlays.",
    ),
    gwi_wiki_article: str = Query(
        "Climate_change",
        description="Wikipedia article used for GWI overlays.",
    ),
) -> DestineUIASummary:
    """
    Aggregate DestinE climate scenarios into a single UIA-style climate cognition
    summary:

    - average OI and SMF across scenarios
    - mean Ω (synergy) and τ_I acceleration ratio
    - total number of global ignition events

    A provisional `uia_proxy` in [0,1] combines these into a single index:

        uia_proxy ≈ 0.4 * OI_norm + 0.4 * SMF_norm + 0.2 * τ_I_norm

    This is explicitly labelled a *proxy* until the full UIA engine is implemented. 
    """
    client = DestineHDAClient()

    dt_range: Optional[str] = None
    if datetime_start and datetime_end:
        dt_range = f"{datetime_start}/{datetime_end}"

    scenarios: list[DestineScenarioMetadata] = discover_climate_dt_scenarios(
        client=client,
        collection_query=q,
        datetime_range=dt_range,
        limit=limit,
    )
    if not scenarios:
        raise HTTPException(
            status_code=404,
            detail="No DestinE climate scenarios found for the given parameters.",
        )

    df = summarise_scenarios_cognitively(
        scenarios,
        forecast_skill_csv=forecast_skill_csv,
        gwi_topic=gwi_topic,
        gwi_wiki_article=gwi_wiki_article,
    )

    n = len(df)
    oi_mean_avg = _safe_mean(df, "oi_mean")
    smf_global_avg = _safe_mean(df, "smf_global")
    omega_synergy_avg = _safe_mean(df, "omega_synergy")
    tau_i_avg = _safe_mean(df, "tau_i_accel_ratio")

    if "gwi_ignitions" in df.columns:
        gwi_total = int(df["gwi_ignitions"].fillna(0).sum())
    else:
        gwi_total = None

    # --- heuristic UIA proxy ------------------------------------------------

    def _clip(val: Optional[float], lo: float, hi: float) -> Optional[float]:
        if val is None:
            return None
        return max(lo, min(hi, val))

    # OI and SMF are already ~[0,1], clip just in case
    oi_norm = _clip(oi_mean_avg, 0.0, 1.0)
    smf_norm = _clip(smf_global_avg, 0.0, 1.0)

    # τ_I acceleration ratio – treat 0..2 as [0,1], clip beyond
    tau_norm = None
    if tau_i_avg is not None:
        tau_norm = _clip(tau_i_avg / 2.0, 0.0, 1.0)

    uia_proxy: Optional[float] = None
    if oi_norm is not None and smf_norm is not None and tau_norm is not None:
        uia_proxy = 0.4 * oi_norm + 0.4 * smf_norm + 0.2 * tau_norm

    return DestineUIASummary(
        n_scenarios=n,
        oi_mean_avg=oi_mean_avg,
        smf_global_avg=smf_global_avg,
        omega_synergy_avg=omega_synergy_avg,
        gwi_ignitions_total=gwi_total,
        tau_i_accel_ratio_avg=tau_i_avg,
        uia_proxy=uia_proxy,
    )
