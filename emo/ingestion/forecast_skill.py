# emo/ingestion/forecast_skill.py
from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

import requests

from .base import DataLakeLayout, PipelineRun, now_utc, ensure_parent

LOG = logging.getLogger(__name__)


@dataclass
class ForecastSkillConfig:
    """
    Minimal config for mirroring a forecast-skill CSV into the data lake.

    Attributes
    ----------
    url:
        Remote URL to a CSV with at least [year, skill] columns.
    canonical_name:
        Logical name for the file (e.g. 'ecmwf_headline_scores').
    """

    url: str
    canonical_name: str = "forecast_skill"


def run_forecast_skill_pipeline(
    cfg: ForecastSkillConfig,
    layout: Optional[DataLakeLayout] = None,
    timeout: int = 60,
) -> PipelineRun:
    """
    Download a forecast-skill CSV and store:

    - a timestamped snapshot in raw/forecast_skill/
    - a canonical copy in clean/forecast_skill/{canonical_name}.csv

    Intended cadence: **yearly** (or when new skill series become available).
    """
    layout = layout or DataLakeLayout.from_env()
    started = now_utc()
    artifacts = {}

    try:
        LOG.info("Downloading forecast skill CSV from %s", cfg.url)
        resp = requests.get(cfg.url, timeout=timeout)
        resp.raise_for_status()
        content = resp.content

        ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        raw_path = layout.subpath(
            "raw", "forecast_skill", f"{cfg.canonical_name}_{ts}.csv"
        )
        ensure_parent(raw_path)
        raw_path.write_bytes(content)

        clean_path = layout.subpath(
            "clean", "forecast_skill", f"{cfg.canonical_name}.csv"
        )
        ensure_parent(clean_path)
        clean_path.write_bytes(content)

        artifacts = {
            "raw_csv": str(raw_path),
            "clean_csv": str(clean_path),
        }
        status = "success"
        detail = None
        records = None  # unknown here; metric layer will parse
    except Exception as exc:  # pragma: no cover - defensive
        LOG.exception("Forecast skill pipeline failed: %s", exc)
        status = "failed"
        detail = str(exc)
        records = None

    finished = now_utc()
    run = PipelineRun(
        name="forecast_skill_yearly",
        started_at=started,
        finished_at=finished,
        status=status,
        records=records,
        detail=detail,
        artifacts=artifacts or None,
    )
    from .base import log_pipeline_run

    log_pipeline_run(run, layout=layout)
    return run
