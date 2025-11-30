# emo/ingestion/owid.py
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Iterable, List, Optional

import requests

from .base import DataLakeLayout, PipelineRun, now_utc, ensure_parent

LOG = logging.getLogger(__name__)

OWID_GRAPHER_BASE = "https://ourworldindata.org/grapher"


@dataclass
class OWIDChartConfig:
    """
    Configuration for a single OWID chart to download.

    Example chart IDs (you can adjust to your needs):
    - 'co2'                       (global CO₂ emissions)
    - 'co2-by-sector'             (sectoral breakdowns)
    - 'climate-change-risk-index' (if available)
    - 'planetary-boundaries'      (if published as chart)
    """

    chart_id: str


def download_chart_csv(
    chart: OWIDChartConfig,
    layout: Optional[DataLakeLayout] = None,
    timeout: int = 60,
) -> str:
    """
    Download a single OWID chart (CSV) into the raw zone.

    The OWID "Chart API" serves CSV/JSON at URLs of the form
    https://ourworldindata.org/grapher/{chart_id}.csv. :contentReference[oaicite:19]{index=19}
    """
    layout = layout or DataLakeLayout.from_env()
    url = f"{OWID_GRAPHER_BASE}/{chart.chart_id}.csv"
    target = layout.subpath("raw", "owid", f"{chart.chart_id}.csv")
    ensure_parent(target)

    LOG.info("Downloading OWID chart %s from %s", chart.chart_id, url)
    resp = requests.get(url, timeout=timeout)
    resp.raise_for_status()
    target.write_bytes(resp.content)
    LOG.info("Saved OWID chart %s to %s", chart.chart_id, target)
    return str(target)


def run_owid_pipeline(
    charts: Iterable[OWIDChartConfig],
    layout: Optional[DataLakeLayout] = None,
    timeout: int = 60,
) -> PipelineRun:
    """
    Download a set of OWID charts into the data lake.

    This should run on a **monthly** cadence for OI / SMF / planetary health.
    """
    layout = layout or DataLakeLayout.from_env()
    started = now_utc()
    count = 0
    artifacts: List[str] = []

    try:
        for chart in charts:
            path = download_chart_csv(chart, layout=layout, timeout=timeout)
            artifacts.append(path)
            count += 1

        status = "success"
        detail = None
    except Exception as exc:  # pragma: no cover - defensive
        LOG.exception("OWID pipeline failed: %s", exc)
        status = "failed"
        detail = str(exc)

    finished = now_utc()
    run = PipelineRun(
        name="owid_monthly",
        started_at=started,
        finished_at=finished,
        status=status,
        records=count,
        detail=detail,
        artifacts={"csv_paths": ",".join(artifacts)} if artifacts else None,
    )
    from .base import log_pipeline_run

    log_pipeline_run(run, layout=layout)
    return run
