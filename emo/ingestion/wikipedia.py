# emo/ingestion/wikipedia.py
from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import date
from typing import Iterable, List, Optional

import pandas as pd
import requests

from .base import DataLakeLayout, PipelineRun, now_utc, save_dataframe

LOG = logging.getLogger(__name__)

PAGEVIEWS_BASE = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article"
USER_AGENT = "EMO-Core/1.0 (research; contact@example.org)"


@dataclass
class WikipediaArticleConfig:
    """
    Configuration for fetching pageviews for a specific Wikipedia article.

    Attributes
    ----------
    project:
        Wiki project (e.g. 'en.wikipedia.org').
    article:
        Article title with spaces replaced by underscores (e.g. 'Climate_change').
    access:
        'all-access', 'desktop', or 'mobile-web'.
    agent:
        'user' (recommended), 'spider', or 'all-agents'.
    granularity:
        'daily' (most useful for EMO) or 'monthly'.
    start:
        Start date (YYYYMMDD) inclusive.
    end:
        End date (YYYYMMDD) inclusive.
    """

    project: str
    article: str
    access: str = "all-access"
    agent: str = "user"
    granularity: str = "daily"
    start: str = "20150101"
    end: str = "20251231"


def fetch_pageviews(cfg: WikipediaArticleConfig, timeout: int = 60) -> pd.DataFrame:
    """
    Fetch pageviews for a single article using the Wikimedia Pageviews API. :contentReference[oaicite:23]{index=23}
    """
    headers = {"User-Agent": USER_AGENT}
    url = (
        f"{PAGEVIEWS_BASE}/{cfg.project}/{cfg.access}/{cfg.agent}"
        f"/{cfg.article}/{cfg.granularity}/{cfg.start}/{cfg.end}"
    )
    LOG.info("Fetching Wikipedia pageviews: %s", url)
    resp = requests.get(url, headers=headers, timeout=timeout)
    resp.raise_for_status()
    payload = resp.json()
    items = payload.get("items", [])
    dates: List[str] = []
    views: List[int] = []
    for item in items:
        dates.append(item["timestamp"][:8])
        views.append(int(item.get("views", 0)))

    df = pd.DataFrame(
        {
            "date": pd.to_datetime(dates, format="%Y%m%d"),
            "views": views,
            "project": cfg.project,
            "article": cfg.article,
            "access": cfg.access,
            "agent": cfg.agent,
        }
    )
    df.sort_values("date", inplace=True)
    return df


def run_wikipedia_pageviews_pipeline(
    articles: Iterable[WikipediaArticleConfig],
    layout: Optional[DataLakeLayout] = None,
) -> PipelineRun:
    """
    Fetch pageviews for a list of articles and write feature tables.

    Intended cadence: **daily** (same as GDELT).
    """
    layout = layout or DataLakeLayout.from_env()
    started = now_utc()
    records = 0
    artifacts: List[str] = []

    try:
        for cfg in articles:
            df = fetch_pageviews(cfg)
            records += len(df)
            safe_article = cfg.article.replace("/", "_")
            path = layout.subpath(
                "feature", "wikipedia", f"pageviews_{safe_article}.parquet"
            )
            save_dataframe(df, path)
            artifacts.append(str(path))
        status = "success"
        detail = None
    except Exception as exc:  # pragma: no cover - defensive
        LOG.exception("Wikipedia pageviews pipeline failed: %s", exc)
        status = "failed"
        detail = str(exc)

    finished = now_utc()
    run = PipelineRun(
        name="wikipedia_daily",
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
