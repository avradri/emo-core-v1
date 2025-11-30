# api/routers/metrics.py

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from emo import (
    compute_organismality_index,
    build_synergy_dataset,
    compute_synergy_o_information,
    compute_gwi_for_topic,
    compute_smf,
    compute_information_time_from_skill,
)
from emo.twin_hooks import (
    DestineHDAClient,
    DestineScenarioMetadata,
    summarise_scenarios_cognitively,
    discover_climate_dt_scenarios,
)

router = APIRouter(prefix="/metrics", tags=["metrics"])


# ---------------------------------------------------------------------------
# Pydantic response models for EMO metrics
# ---------------------------------------------------------------------------


class OIResponse(BaseModel):
    start_year: int
    end_year: int
    latest_oi: float
    trend_20y: Optional[float]


class SynergyResponse(BaseModel):
    topic: str
    start_year: int
    end_year: int
    o_information: float


class GWIEvent(BaseModel):
    date: str
    ignition: float
    news_z: float
    search_z: float


class GWIResponse(BaseModel):
    topic: str
    wiki_article: str
    start_date: str
    end_date: str
    ignition_events: List[GWIEvent]


class SMFResponse(BaseModel):
    start_year: int
    end_year: int
    smf_global: float
    corr: float


class TauIResponse(BaseModel):
    start_year: int
    end_year: int
    accel_ratio: float


# ---------------------------------------------------------------------------
# Pydantic models for DestinE × EMO overlays
# ---------------------------------------------------------------------------


class DestineScenarioOut(BaseModel):
    twin_id: Optional[str]
    collection_id: str
    item_id: str
    title: Optional[str]
    time_start: Optional[str]
    time_end: Optional[str]
    bbox: Optional[List[float]]


class DestineScenarioOverlayOut(DestineScenarioOut):
    oi_mean: Optional[float]
    oi_trend_20y: Optional[float]
    omega_synergy: Optional[float]
    gwi_ignitions: Optional[int]
    smf_global: Optional[float]
    smf_corr: Optional[float]
    tau_i_accel_ratio: Optional[float]


# ---------------------------------------------------------------------------
# Core EMO metrics endpoints
# ---------------------------------------------------------------------------


@router.get(
    "/oi",
    response_model=OIResponse,
    summary="Global Organismality Index (OI)",
)
def get_oi(
    start_year: int = Query(1950, ge=1900, description="First year to include"),
    end_year: Optional[int] = Query(
        None,
        description="Last year to include (defaults to latest available)",
    ),
) -> OIResponse:
    """
    Compute the global Organismality Index (OI) over a time window.

    OI ~ sigmoid(z(cooperation) - z(violence)), using environmental-treaty
    participation and conflict deaths as in EMO v0.1. :contentReference[oaicite:12]{index=12}
    """
    result = compute_organismality_index(start_year=start_year, end_year=end_year)
    df = result.df
    start = int(df["year"].min())
    end = int(df["year"].max())

    return OIResponse(
        start_year=start,
        end_year=end,
        latest_oi=result.latest_oi,
        trend_20y=result.trend_20y,
    )


@router.get(
    "/synergy",
    response_model=SynergyResponse,
    summary="Synergy / O-information for a topic",
)
def get_synergy(
    topic: str = Query(
        "climate change",
        description="Free-text news query for GDELT and OpenAlex search term if no concept_id is given.",
    ),
    openalex_concept_id: Optional[str] = Query(
        None,
        description="Optional OpenAlex concept ID for the topic (e.g. climate-change concept).",
    ),
    start_year: int = Query(
        1990,
        ge=1900,
        description="First year for the synergy window.",
    ),
    end_year: Optional[int] = Query(
        None,
        description="Last year for the synergy window (defaults to latest available).",
    ),
) -> SynergyResponse:
    """
    Compute Gaussian O-information Ω across attention (news), memory (papers),
    and conflict streams, following EMO v0.1. 
    """
    df = build_synergy_dataset(
        topic_query=topic,
        openalex_concept_id=openalex_concept_id,
        start_year=start_year,
        end_year=end_year,
    )
    o_info = compute_synergy_o_information(df)
    return SynergyResponse(
        topic=topic,
        start_year=int(df["year"].min()),
        end_year=int(df["year"].max()),
        o_information=float(o_info),
    )


@router.get(
    "/gwi",
    response_model=GWIResponse,
    summary="Global Workspace Ignition (GWI) for a topic",
)
def get_gwi(
    topic: str = Query("IPCC", description="News query string for GDELT."),
    wiki_article: str = Query(
        "Intergovernmental_Panel_on_Climate_Change",
        description="Wikipedia article slug for the same topic.",
    ),
    start: str = Query("2015-01-01", description="Start date (YYYY-MM-DD)."),
    end: str = Query("2025-01-01", description="End date (YYYY-MM-DD)."),
    ignition_percentile: float = Query(
        0.95,
        ge=0.5,
        le=0.999,
        description="Percentile threshold for ignition events.",
    ),
) -> GWIResponse:
    """
    Compute Global Workspace Ignition (GWI) for a topic using GDELT news volumes
    and Wikipedia pageviews. 
    """
    try:
        start_dt = datetime.fromisoformat(start)
        end_dt = datetime.fromisoformat(end)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=f"Invalid date format: {exc}")

    res = compute_gwi_for_topic(
        topic_query=topic,
        wiki_article=wiki_article,
        start_date=start_dt,
        end_date=end_dt,
        ignition_percentile=ignition_percentile,
    )

    events: List[GWIEvent] = []
    for _, row in res.events.iterrows():
        date_val = row.get("date")
        if hasattr(date_val, "isoformat"):
            date_str = date_val.isoformat()
        else:
            date_str = str(date_val)
        events.append(
            GWIEvent(
                date=date_str,
                ignition=float(row["ignition"]),
                news_z=float(row["news_z"]),
                search_z=float(row["search_z"]),
            )
        )

    return GWIResponse(
        topic=topic,
        wiki_article=wiki_article,
        start_date=start_dt.date().isoformat(),
        end_date=end_dt.date().isoformat(),
        ignition_events=events,
    )


@router.get(
    "/smf",
    response_model=SMFResponse,
    summary="Self-Model Fidelity (SMF) for climate",
)
def get_smf(
    start_year: int = Query(
        1990,
        ge=1900,
        description="First year for SMF window.",
    ),
    end_year: Optional[int] = Query(
        None,
        description="Last year (defaults to latest in the data).",
    ),
) -> SMFResponse:
    """
    Compute Self-Model Fidelity (SMF) for climate:

    compares 1.5°C-consistent CO₂ pathways with realised emissions. 
    """
    res = compute_smf(start_year=start_year, end_year=end_year)
    start = int(res.df["year"].min())
    end = int(res.df["year"].max())
    return SMFResponse(
        start_year=start,
        end_year=end,
        smf_global=float(res.smf_global),
        corr=float(res.corr),
    )


@router.get(
    "/tau_i",
    response_model=TauIResponse,
    summary="Information-time τ_I from forecast skill",
)
def get_tau_i(
    skill_csv_path: str = Query(
        "data/ecmwf_headline_scores.csv",
        description="Path to forecast-skill CSV on the server.",
    ),
) -> TauIResponse:
    """
    Compute information-time τ_I(t) from a forecast-skill time series (e.g. ECMWF
    headline scores or similar). 
    """
    try:
        res = compute_information_time_from_skill(skill_csv_path)
    except FileNotFoundError:
        raise HTTPException(
            status_code=500,
            detail=(
                f"Forecast skill CSV not found at '{skill_csv_path}'. "
                "Place a file with columns [year, skill] there or point to the right path."
            ),
        )
    df = res.df
    start = int(df["year"].min())
    end = int(df["year"].max())
    return TauIResponse(
        start_year=start,
        end_year=end,
        accel_ratio=float(res.accel_ratio),
    )


# ---------------------------------------------------------------------------
# DestinE × EMO overlay endpoints
# ---------------------------------------------------------------------------


@router.get(
    "/destine/scenarios",
    response_model=List[DestineScenarioOut],
    summary="List DestinE climate scenarios that EMO can attach cognitive overlays to",
)
def list_destine_scenarios(
    q: str = Query(
        "climate",
        description="Free-text search in DestinE collections (e.g. 'climate').",
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
        20,
        ge=1,
        le=200,
        description="Maximum number of items to return.",
    ),
) -> List[DestineScenarioOut]:
    """
    Discover climate-related DestinE digital twin scenarios via the HDA/STAC
    interface and return lightweight metadata for each scenario. 
    """
    client = DestineHDAClient()

    dt_range: Optional[str] = None
    if datetime_start and datetime_end:
        dt_range = f"{datetime_start}/{datetime_end}"

    scenarios: List[DestineScenarioMetadata] = discover_climate_dt_scenarios(
        client=client,
        collection_query=q,
        datetime_range=dt_range,
        limit=limit,
    )

    out: List[DestineScenarioOut] = []
    for s in scenarios:
        d = s.to_public_dict()
        out.append(
            DestineScenarioOut(
                twin_id=d.get("twin_id"),
                collection_id=d["collection_id"],
                item_id=d["item_id"],
                title=d.get("title"),
                time_start=d.get("time_start"),
                time_end=d.get("time_end"),
                bbox=d.get("bbox"),
            )
        )
    return out


@router.get(
    "/destine/scenarios/overlays",
    response_model=List[DestineScenarioOverlayOut],
    summary="Compute EMO cognitive overlays for DestinE climate scenarios",
)
def list_destine_scenario_overlays(
    q: str = Query(
        "climate",
        description="Free-text search for DestinE climate collections.",
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
        description="Maximum number of scenarios to summarise.",
    ),
    forecast_skill_csv: Optional[str] = Query(
        "data/ecmwf_headline_scores.csv",
        description="Forecast-skill CSV path used to compute τ_I overlays (optional).",
    ),
    gwi_topic: str = Query(
        "climate change",
        description="Topic query for GWI overlays.",
    ),
    gwi_wiki_article: str = Query(
        "Climate_change",
        description="Wikipedia article slug for GWI overlays.",
    ),
) -> List[DestineScenarioOverlayOut]:
    """
    For each discovered DestinE climate scenario, compute a small "cognitive
    overlay" using EMO metrics:

    - mean OI and 20y trend
    - synergy Ω
    - number of GWI ignition events for a climate topic
    - SMF scores
    - τ_I acceleration ratio (if forecast-skill data provided)

    This creates exactly the dual-twin view described in the EMO v1.0 architecture:
    DestinE simulates the Earth, EMO simulates species-mind response. 
    """
    client = DestineHDAClient()

    dt_range: Optional[str] = None
    if datetime_start and datetime_end:
        dt_range = f"{datetime_start}/{datetime_end}"

    scenarios: List[DestineScenarioMetadata] = discover_climate_dt_scenarios(
        client=client,
        collection_query=q,
        datetime_range=dt_range,
        limit=limit,
    )
    if not scenarios:
        raise HTTPException(
            status_code=404,
            detail="No DestinE scenarios found for the given parameters.",
        )

    # Compute scenario-wise cognitive summaries
    df = summarise_scenarios_cognitively(
        scenarios,
        forecast_skill_csv=forecast_skill_csv,
        gwi_topic=gwi_topic,
        gwi_wiki_article=gwi_wiki_article,
    )

    # Map item_id -> bbox from metadata
    bbox_by_item = {s.item_id: s.bbox for s in scenarios}

    out: List[DestineScenarioOverlayOut] = []
    for _, row in df.iterrows():
        item_id = row["item_id"]
        out.append(
            DestineScenarioOverlayOut(
                twin_id=row.get("twin_id"),
                collection_id=row["collection_id"],
                item_id=item_id,
                title=row.get("title"),
                time_start=row.get("time_start"),
                time_end=row.get("time_end"),
                bbox=bbox_by_item.get(item_id),
                oi_mean=row.get("oi_mean"),
                oi_trend_20y=row.get("oi_trend_20y"),
                omega_synergy=row.get("omega_synergy"),
                gwi_ignitions=row.get("gwi_ignitions"),
                smf_global=row.get("smf_global"),
                smf_corr=row.get("smf_corr"),
                tau_i_accel_ratio=row.get("tau_i_accel_ratio"),
            )
        )

    return out
