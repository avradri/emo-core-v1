# emo/ingestion/gdelt.py
from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import date
from typing import Iterable, List, Optional

import pandas as pd

from .base import DataLakeLayout, PipelineRun, now_utc, save_dataframe

LOG = logging.getLogger(__name__)

try:
    from gdeltdoc import GdeltDoc, Filters  # type: ignore[import]
except ImportError:  # pragma: no cover - optional dependency
    GdeltDoc = None
    Filters = None


@dataclass
class GDELTTopicConfig:
    """
    Configuration for a GDELT DOC 2.0 topic timeline.

    Attributes
    ----------
    keyword:
        Query string (e.g. "climate change").
    label:
        Short label used in filenames (e.g. "climate_change").
    timespan:
        GDELT timespan string (e.g. "3m", "6m", "12m").
    """

    keyword: str
    label: str
    timespan: str = "3m"


def _require_gdelt_client() -> GdeltDoc:
    if GdeltDoc is None or Filters is None:
        raise ImportError(
            "gdeltdoc is not installed. Install it with `pip install gdeltdoc` "
            "or remove GDELT ingestion from your pipelines."
        )
    return GdeltDoc()


def fetch_timeline_for_topic(cfg: GDELTTopicConfig) -> pd.DataFrame:
    """
    Fetch a TimelineVolRaw timeline for a topic using gdeltdoc.

    We rely on the official-style client `gdeltdoc`, which wraps the
    GDELT DOC 2.0 API `timelinevol` / `timelinevolraw` modes in a DataFrame. :contentReference[oaicite:21]{index=21}
    """
    gd = _require_gdelt_client()
    f = Filters(
        keyword=cfg.keyword,
        timespan=cfg.timespan,
    )
    # 'timelinevolraw' returns absolute article counts over time
    timeline = gd.timeline_search("timelinevolraw", f)
    if not isinstance(timeline, pd.DataFrame):
        raise RuntimeError("gdeltdoc.timeline_search did not return a DataFrame")
    # Normalise column names: 'datetime' and 'value'
    cols = {c.lower(): c for c in timeline.columns}
    # Try to sniff time / count columns
    if "datetime" in cols:
        time_col = cols["datetime"]
    elif "date" in cols:
        time_col = cols["date"]
    else:
        time_col = timeline.columns[0]
    if "value" in cols:
        val_col = cols["value"]
    elif "count" in cols:
        val_col = cols["count"]
    else:
        val_col = timeline.columns[1]

    df = pd.DataFrame(
        {
            "datetime": pd.to_datetime(timeline[time_col]),
            "count": timeline[val_col].astype("int64"),
            "topic_label": cfg.label,
            "keyword": cfg.keyword,
        }
    )
    df.sort_values("datetime", inplace=True)
    return df


def run_gdelt_timeline_pipeline(
    topics: Iterable[GDELTTopicConfig],
    layout: Optional[DataLakeLayout] = None,
) -> PipelineRun:
    """
    Fetch GDELT DOC 2.0 timelines for a list of topics and save them as
    feature tables.

    Intended cadence: **daily** (for GWI and daily attention maps).
    """
    layout = layout or DataLakeLayout.from_env()
    started = now_utc()
    records = 0
    artifacts: List[str] = []

    try:
        for cfg in topics:
            df = fetch_timeline_for_topic(cfg)
            records += len(df)
            path = layout.subpath(
                "feature", "gdelt", f"timeline_{cfg.label}.parquet"
            )
            save_dataframe(df, path)
            artifacts.append(str(path))
        status = "success"
        detail = None
    except Exception as exc:  # pragma: no cover - defensive
        LOG.exception("GDELT pipeline failed: %s", exc)
        status = "failed"
        detail = str(exc)

    finished = now_utc()
    run = PipelineRun(
        name="gdelt_daily",
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
