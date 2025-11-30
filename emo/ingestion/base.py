# emo/ingestion/base.py
from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Optional

import pandas as pd

LOG = logging.getLogger(__name__)


@dataclass
class DataLakeLayout:
    """
    Simple on-disk data-lake layout for EMO.

    root/
      raw/      - source snapshots, as downloaded
      clean/    - schema-normalised & type-checked tables
      feature/  - metric-ready feature tables
      metric/   - metric & UIA outputs
    """

    root: Path
    raw_dir: Path
    clean_dir: Path
    feature_dir: Path
    metric_dir: Path

    @classmethod
    def from_env(cls) -> "DataLakeLayout":
        root_str = os.getenv("EMO_DATA_ROOT", "data")
        root = Path(root_str).resolve()
        instance = cls(
            root=root,
            raw_dir=root / "raw",
            clean_dir=root / "clean",
            feature_dir=root / "feature",
            metric_dir=root / "metric",
        )
        instance._ensure_dirs()
        return instance

    def _ensure_dirs(self) -> None:
        for p in (self.raw_dir, self.clean_dir, self.feature_dir, self.metric_dir):
            p.mkdir(parents=True, exist_ok=True)

    def subpath(self, zone: str, *parts: str) -> Path:
        """
        Build a path in a given zone ('raw', 'clean', 'feature', 'metric').
        """
        if zone == "raw":
            base = self.raw_dir
        elif zone == "clean":
            base = self.clean_dir
        elif zone == "feature":
            base = self.feature_dir
        elif zone == "metric":
            base = self.metric_dir
        else:
            raise ValueError(f"Unknown data-lake zone: {zone}")
        return base.joinpath(*parts)


@dataclass
class PipelineRun:
    """
    Lightweight record of a single pipeline run.

    This is intentionally minimal; you can persist it to JSON for
    ops dashboards or attach it to logging.
    """

    name: str
    started_at: datetime
    finished_at: datetime
    status: str  # "success", "partial", "failed"
    records: Optional[int] = None
    detail: Optional[str] = None
    artifacts: Optional[Dict[str, str]] = None  # logical_name -> path

    @property
    def duration_seconds(self) -> float:
        return (self.finished_at - self.started_at).total_seconds()

    def to_dict(self) -> Dict[str, object]:
        d = asdict(self)
        d["started_at"] = self.started_at.isoformat()
        d["finished_at"] = self.finished_at.isoformat()
        return d


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def save_dataframe(df: pd.DataFrame, path: Path) -> Path:
    """
    Save a DataFrame to CSV or Parquet depending on the file extension.
    """
    ensure_parent(path)
    suffix = path.suffix.lower()
    if suffix == ".csv":
        df.to_csv(path, index=False)
    elif suffix in (".parquet", ".pq"):
        df.to_parquet(path, index=False)
    else:
        raise ValueError(f"Unsupported extension for DataFrame save: {suffix}")
    LOG.info("Saved %d rows to %s", len(df), path)
    return path


def log_pipeline_run(run: PipelineRun, layout: Optional[DataLakeLayout] = None) -> None:
    """
    Append a JSON line describing the pipeline run into metric/ops/ directory.
    """
    layout = layout or DataLakeLayout.from_env()
    ops_dir = layout.metric_dir / "ops"
    ops_dir.mkdir(parents=True, exist_ok=True)
    log_path = ops_dir / f"pipeline_runs_{run.name}.jsonl"
    with log_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(run.to_dict()) + "\n")
    LOG.info(
        "Pipeline %s finished with status=%s, records=%s, duration=%.2fs",
        run.name,
        run.status,
        run.records,
        run.duration_seconds,
    )
