from __future__ import annotations

import logging
from collections.abc import Iterable
from dataclasses import dataclass

import pandas as pd

from .base import DataLakeLayout, PipelineRun, ensure_parent, now_utc, save_dataframe

LOG = logging.getLogger(__name__)

try:
    from gdeltdoc import Filters, GdeltDoc  # type: ignore[import]
except ImportError:  # pragma: no cover
    Filters = None
    GdeltDoc = None


@dataclass
class GDELTTopicConfig:
    """
    Configuration for a GDELT topic timeline pull.
    """

    keyword: str
    start_date: str
    end_date: str
    label: str


def _fetch_gdelt_timeline(cfg: GDELTTopicConfig) -> pd.DataFrame:
    """
    Fetch a timeline for a single keyword/topic from GDELT Doc 2.0.

    Returns a DataFrame with at least:
    - date
    - value
    - keyword
    - label
    """
    if GdeltDoc is None or Filters is None:
        raise ImportError(
            "gdeltdoc is not installed. Install optional ingestion dependencies "
            "to use the GDELT pipeline."
        )

    gdelt = GdeltDoc()
    filters = Filters(
        keyword=cfg.keyword,
        start_date=cfg.start_date,
        end_date=cfg.end_date,
    )

    timeline = gdelt.timeline_search("timelinevol", filters=filters)
    df = pd.DataFrame(timeline)

    if df.empty:
        return pd.DataFrame(columns=["date", "value", "keyword", "label"])

    if "date" not in df.columns:
        first_col = df.columns[0]
        df = df.rename(columns={first_col: "date"})

    value_col = None
    for candidate in ("value", "count", "Volume Intensity", "norm"):
        if candidate in df.columns:
            value_col = candidate
            break

    if value_col is None:
        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        if not numeric_cols:
            raise ValueError("Could not infer timeline value column from GDELT output.")
        value_col = numeric_cols[0]

    out = df[["date", value_col]].copy()
    out = out.rename(columns={value_col: "value"})
    out["keyword"] = cfg.keyword
    out["label"] = cfg.label
    return out


def run_gdelt_timeline_pipeline(
    topics: Iterable[GDELTTopicConfig],
    layout: DataLakeLayout | None = None,
) -> PipelineRun:
    """
    Fetch GDELT timelines for one or more topics and persist them to the data lake.
    """
    layout = layout or DataLakeLayout.from_env()
    started = now_utc()
    records = 0
    artifacts: list[str] = []

    try:
        frames: list[pd.DataFrame] = []

        for topic in topics:
            LOG.info("Fetching GDELT timeline for %s", topic.label)
            frame = _fetch_gdelt_timeline(topic)
            frames.append(frame)

        combined = (
            pd.concat(frames, ignore_index=True)
            if frames
            else pd.DataFrame(columns=["date", "value", "keyword", "label"])
        )
        records = int(len(combined))

        raw_path = layout.subpath("raw", "gdelt", "gdelt_timeline_raw.csv")
        clean_path = layout.subpath("clean", "gdelt", "gdelt_timeline.csv")

        ensure_parent(raw_path)
        combined.to_csv(raw_path, index=False)
        save_dataframe(combined, clean_path)

        artifacts = [str(raw_path), str(clean_path)]
        status = "success"
        detail = None
    except Exception as exc:  # pragma: no cover
        LOG.exception("GDELT timeline pipeline failed: %s", exc)
        status = "failed"
        detail = str(exc)

    finished = now_utc()
    run = PipelineRun(
        name="gdelt_timeline",
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
