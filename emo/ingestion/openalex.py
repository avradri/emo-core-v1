from __future__ import annotations

import logging
from collections.abc import Iterable
from dataclasses import dataclass

import pandas as pd
import requests

from .base import DataLakeLayout, PipelineRun, ensure_parent, now_utc, save_dataframe

LOG = logging.getLogger(__name__)
OPENALEX_BASE = "https://api.openalex.org/works"


@dataclass
class OpenAlexConceptConfig:
    """
    Configuration for a yearly OpenAlex concept/publication pull.
    """

    label: str
    concept_id: str | None = None
    display_name_search: str | None = None
    filter_extra: str | None = None
    year_from: int = 1990
    year_to: int = 2025


def _build_filter(cfg: OpenAlexConceptConfig, year: int) -> str:
    parts = [f"from_publication_date:{year}-01-01", f"to_publication_date:{year}-12-31"]

    if cfg.concept_id:
        parts.append(f"concepts.id:{cfg.concept_id}")

    if cfg.filter_extra:
        parts.append(cfg.filter_extra)

    return ",".join(parts)


def _fetch_openalex_count(cfg: OpenAlexConceptConfig, year: int) -> int:
    params = {
        "filter": _build_filter(cfg, year),
        "per-page": 1,
        "mailto": "contact@example.org",
    }

    if cfg.display_name_search:
        params["search"] = cfg.display_name_search

    response = requests.get(OPENALEX_BASE, params=params, timeout=60)
    response.raise_for_status()
    payload = response.json()
    meta = payload.get("meta", {})
    return int(meta.get("count", 0))


def run_openalex_pipeline(
    configs: Iterable[OpenAlexConceptConfig],
    layout: DataLakeLayout | None = None,
) -> PipelineRun:
    """
    Pull yearly publication counts from OpenAlex for one or more concept configs.
    """
    layout = layout or DataLakeLayout.from_env()
    started = now_utc()
    records = 0
    artifacts: list[str] = []

    try:
        rows: list[dict[str, object]] = []

        for cfg in configs:
            LOG.info("Fetching OpenAlex counts for %s", cfg.label)
            for year in range(cfg.year_from, cfg.year_to + 1):
                count = _fetch_openalex_count(cfg, year)
                rows.append(
                    {
                        "label": cfg.label,
                        "year": year,
                        "count": count,
                        "concept_id": cfg.concept_id,
                        "display_name_search": cfg.display_name_search,
                    }
                )

        df = pd.DataFrame(rows)
        records = int(len(df))

        raw_path = layout.subpath("raw", "openalex", "openalex_counts_raw.csv")
        clean_path = layout.subpath("clean", "openalex", "openalex_counts.csv")

        ensure_parent(raw_path)
        df.to_csv(raw_path, index=False)
        save_dataframe(df, clean_path)

        artifacts = [str(raw_path), str(clean_path)]
        status = "success"
        detail = None
    except Exception as exc:  # pragma: no cover
        LOG.exception("OpenAlex pipeline failed: %s", exc)
        status = "failed"
        detail = str(exc)

    finished = now_utc()
    run = PipelineRun(
        name="openalex_counts",
        started_at=started,
        finished_at=finished,
        status=status,
        records=records,
        detail=detail,
        artifacts={"files": ",".join(artifacts)} if artifacts else None,
    )

    from .base import log_pipeline_run

    log_pipeline_run(run, layout=layout)
    return run
