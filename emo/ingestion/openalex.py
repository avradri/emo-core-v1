# emo/ingestion/openalex.py
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Iterable, List, Optional

import pandas as pd
import requests

from .base import DataLakeLayout, PipelineRun, now_utc, save_dataframe

LOG = logging.getLogger(__name__)

OPENALEX_BASE = "https://api.openalex.org"
OPENALEX_MAILTO = "mailto=contact@example.org"  # replace with real email for polite use


@dataclass
class OpenAlexConceptConfig:
    """
    Configuration for tracking works associated with an OpenAlex concept or topic.

    You can either:
    - Provide a full concepts.id like 'https://openalex.org/C1234567890', OR
    - Provide a `display_name` search string (slower, but convenient).

    For more complex use cases, you can pass a raw filter string.
    """

    label: str                # short label for filenames, e.g. "climate_change"
    concept_id: Optional[str] = None
    display_name_search: Optional[str] = None
    filter_extra: Optional[str] = None
    year_from: int = 1990
    year_to: int = 2025


def _build_works_filter(cfg: OpenAlexConceptConfig, year_from: int, year_to: int) -> str:
    filters: List[str] = []
    # Restrict by concept/topic if possible
    if cfg.concept_id:
        filters.append(f"concepts.id:{cfg.concept_id}")
    elif cfg.display_name_search:
        filters.append(f"default.search:{cfg.display_name_search}")
    if cfg.filter_extra:
        filters.append(cfg.filter_extra)
    # Publication year window
    filters.append(f"publication_year:{year_from}-{year_to}")
    return ",".join(filters)


def fetch_works_by_year(cfg: OpenAlexConceptConfig) -> pd.DataFrame:
    """
    Use OpenAlex /works with group_by=publication_year to get counts per year. :contentReference[oaicite:25]{index=25}
    """
    params: dict[str, str | int] = {
        "group_by": "publication_year",
        "per-page": 200,  # group_by results, not individual works
        "mailto": OPENALEX_MAILTO,
    }
    filters = _build_works_filter(cfg, cfg.year_from, cfg.year_to)
    params["filter"] = filters

    url = f"{OPENALEX_BASE}/works"
    LOG.info("Fetching OpenAlex works grouped by year for %s", cfg.label)
    resp = requests.get(url, params=params, timeout=60)
    resp.raise_for_status()
    payload = resp.json()

    groups = payload.get("group_by", []) or payload.get("results", [])
    years: List[int] = []
    counts: List[int] = []

    for g in groups:
        year = g.get("key") or g.get("publication_year")
        count = g.get("count", 0)
        try:
            year_int = int(year)
        except Exception:
            continue
        years.append(year_int)
        counts.append(int(count))

    df = pd.DataFrame(
        {
            "year": years,
            "works_count": counts,
            "label": cfg.label,
            "concept_id": cfg.concept_id,
            "display_name_search": cfg.display_name_search,
            "filter_extra": cfg.filter_extra,
        }
    ).sort_values("year")

    return df.reset_index(drop=True)


def openalex_weekly_ingestion(
    concepts: Iterable[OpenAlexConceptConfig],
    layout: Optional[DataLakeLayout] = None,
) -> PipelineRun:
    """
    Weekly pipeline:

    - For each configured concept/topic, query OpenAlex /works grouped by year
      and store a small feature table in the data lake.

    This is intended to be light-weight, cheap to run, and primarily used for
    high-level trend visualisation.
    """
    layout = layout or DataLakeLayout.from_env()
    started = now_utc()
    records = 0
    artifacts: List[str] = []
    status = "success"
    detail = ""

    try:
        for cfg in concepts:
            df = fetch_works_by_year(cfg)
            records += len(df)
            path = layout.subpath(
                "feature",
                "openalex",
                f"works_by_year_{cfg.label}.parquet",
            )
            save_dataframe(df, path)
            artifacts.append(str(path))
    except Exception as exc:  # pragma: no cover - defensive
        LOG.exception("OpenAlex weekly ingestion failed")
        status = "error"
        detail = str(exc)

    finished = now_utc()
    run = PipelineRun(
        name="openalex_weekly",
        started_at=started,
        finished_at=finished,
        status=status,
        records=records,
        detail=detail,
        artifacts={"feature_paths": ",".join(artifacts)} if artifacts else None,
    )
    from .base import log_pipeline_run

    log_pipeline_run(run, layout=layout)
    return run
