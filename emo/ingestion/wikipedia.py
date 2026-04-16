from __future__ import annotations

import logging
from collections.abc import Iterable
from dataclasses import dataclass

import pandas as pd
import requests

from .base import DataLakeLayout, PipelineRun, ensure_parent, now_utc, save_dataframe

LOG = logging.getLogger(__name__)

WIKIPEDIA_PAGEVIEWS_BASE = (
    "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article"
)


@dataclass
class WikipediaArticleConfig:
    """
    Configuration for one Wikimedia pageviews pull.
    """

    project: str
    article: str
    start: str
    end: str
    access: str = "all-access"
    agent: str = "user"
    granularity: str = "monthly"


def _fetch_pageviews(article: WikipediaArticleConfig) -> pd.DataFrame:
    url = (
        f"{WIKIPEDIA_PAGEVIEWS_BASE}/"
        f"{article.project}/{article.access}/{article.agent}/"
        f"{article.article}/{article.granularity}/{article.start}/{article.end}"
    )

    LOG.info("Fetching Wikipedia pageviews for %s", article.article)
    resp = requests.get(url, timeout=60)
    resp.raise_for_status()

    payload = resp.json()
    items = payload.get("items", [])

    dates: list[str] = []
    views: list[int] = []

    for item in items:
        dates.append(str(item["timestamp"])[:8])
        views.append(int(item["views"]))

    return pd.DataFrame(
        {
            "date": dates,
            "views": views,
            "project": article.project,
            "article": article.article,
            "granularity": article.granularity,
        }
    )


def run_wikipedia_pageviews_pipeline(
    articles: Iterable[WikipediaArticleConfig],
    layout: DataLakeLayout | None = None,
) -> PipelineRun:
    """
    Fetch pageviews for one or more articles and persist them to the data lake.
    """
    layout = layout or DataLakeLayout.from_env()
    started = now_utc()
    records = 0
    artifacts: list[str] = []

    try:
        frames: list[pd.DataFrame] = []

        for article in articles:
            frame = _fetch_pageviews(article)
            frames.append(frame)

        combined = (
            pd.concat(frames, ignore_index=True)
            if frames
            else pd.DataFrame(columns=["date", "views", "project", "article", "granularity"])
        )
        records = int(len(combined))

        raw_path = layout.subpath("raw", "wikipedia", "pageviews_raw.csv")
        clean_path = layout.subpath("clean", "wikipedia", "pageviews.csv")

        ensure_parent(raw_path)
        combined.to_csv(raw_path, index=False)
        save_dataframe(combined, clean_path)

        artifacts = [str(raw_path), str(clean_path)]
        status = "success"
        detail = None
    except Exception as exc:  # pragma: no cover
        LOG.exception("Wikipedia pipeline failed: %s", exc)
        status = "failed"
        detail = str(exc)

    finished = now_utc()
    run = PipelineRun(
        name="wikipedia_pageviews",
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
