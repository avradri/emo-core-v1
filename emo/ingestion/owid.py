from __future__ import annotations

import logging
from collections.abc import Iterable
from dataclasses import dataclass

import requests

from .base import DataLakeLayout, PipelineRun, ensure_parent, now_utc

LOG = logging.getLogger(__name__)

OWID_GRAPHER_BASE = "https://ourworldindata.org/grapher"


@dataclass
class OWIDChartConfig:
    """
    Configuration for a single OWID chart to download.
    """

    chart_id: str


def download_chart_csv(
    chart: OWIDChartConfig,
    layout: DataLakeLayout | None = None,
    timeout: int = 60,
) -> str:
    """
    Download a single OWID chart (CSV) into the raw zone.
    """
    layout = layout or DataLakeLayout.from_env()
    url = f"{OWID_GRAPHER_BASE}/{chart.chart_id}.csv"

    LOG.info("Downloading OWID chart %s from %s", chart.chart_id, url)
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()

    out_path = layout.subpath("raw", "owid", f"{chart.chart_id}.csv")
    ensure_parent(out_path)
    out_path.write_bytes(response.content)
    return str(out_path)


def run_owid_pipeline(
    charts: Iterable[OWIDChartConfig],
    layout: DataLakeLayout | None = None,
    timeout: int = 60,
) -> PipelineRun:
    """
    Download one or more OWID charts into the data lake.
    """
    layout = layout or DataLakeLayout.from_env()
    started = now_utc()
    count = 0
    artifacts: list[str] = []

    try:
        for chart in charts:
            artifact = download_chart_csv(chart, layout=layout, timeout=timeout)
            artifacts.append(artifact)
            count += 1

        status = "success"
        detail = None
    except Exception as exc:  # pragma: no cover
        LOG.exception("OWID pipeline failed: %s", exc)
        status = "failed"
        detail = str(exc)

    finished = now_utc()
    run = PipelineRun(
        name="owid_chart_mirror",
        started_at=started,
        finished_at=finished,
        status=status,
        records=count,
        detail=detail,
        artifacts={"files": ",".join(artifacts)} if artifacts else None,
    )

    from .base import log_pipeline_run

    log_pipeline_run(run, layout=layout)
    return run
