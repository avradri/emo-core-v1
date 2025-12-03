# orchestration/prefect_flows.py
from __future__ import annotations

import logging
from typing import List

try:  # Prefect is an optional dependency
    from prefect import flow, task  # type: ignore[import]
except Exception:  # pragma: no cover - graceful degradation if Prefect is missing
    def _identity_decorator(fn=None, *args, **kwargs):
        """Fallback no-op decorator used when Prefect is not installed.

        This keeps import-time behaviour simple so that
        `import orchestration.prefect_flows` works even when
        the Prefect library is not available. The wrapped
        function is returned unchanged, and any decorator
        arguments are ignored.
        """
        if fn is not None and callable(fn):
            # Used as @decorator without arguments: @task / @flow
            return fn

        def wrapper(f):
            return f

        return wrapper

    # Expose stand-ins with the same API shape as Prefect.
    flow = _identity_decorator  # type: ignore[assignment]
    task = _identity_decorator  # type: ignore[assignment]

from emo.ingestion import (
    DataLakeLayout,
    ForecastSkillConfig,
    PipelineRun,
    emo_daily_attention,
    emo_weekly_synergy,
    emo_monthly_oi_smf,
    emo_yearly_tau,
)

LOG = logging.getLogger(__name__)


@task
def _log_runs(name: str, runs: List[PipelineRun]) -> None:
    """Log a short summary of completed pipeline runs."""
    total = sum((r.records or 0) for r in runs)
    LOG.info("Flow %s completed %d runs, total records=%s", name, len(runs), total)


@flow(name="EMO Daily Attention")
def emo_daily_attention_flow() -> None:
    """
    Daily Prefect flow.

    Ingests / updates the daily attention data lake tables.
    """
    layout = DataLakeLayout.from_env()
    runs = emo_daily_attention(layout=layout)
    _log_runs.submit("emo_daily_attention", runs)


@flow(name="EMO Weekly Synergy")
def emo_weekly_synergy_flow() -> None:
    """
    Weekly Prefect flow.

    Runs the weekly synergy / O-information analysis.
    """
    layout = DataLakeLayout.from_env()
    runs = emo_weekly_synergy(layout=layout)
    _log_runs.submit("emo_weekly_synergy", runs)

@flow(name="EMO Monthly OI and SMF")
def emo_monthly_oi_smf_flow() -> None:
    """
    Monthly Prefect flow.

    Computes the organismality index (OI) and SMF metrics and stores
    the results in the data lake.
    """
    layout = DataLakeLayout.from_env()
    runs = emo_monthly_oi_smf(layout=layout)
    _log_runs.submit("emo_monthly_oi_smf", runs)


@flow(name="EMO Yearly TauI")
def emo_yearly_tau_flow(
    forecast_skill_url: str = "https://example.com/forecast_skill.csv",
) -> None:
    """
    Yearly Prefect flow.

    Mirrors forecast-skill CSV data (for τ_I) into the data lake.

    Replace the default URL with the real source from ECMWF / C3S or a
    similar forecast-skill provider in production deployments.
    """
    layout = DataLakeLayout.from_env()
    cfg = ForecastSkillConfig(
        url=forecast_skill_url,
        canonical_name="ecmwf_headline_scores",
    )
    runs = emo_yearly_tau(skill_config=cfg, layout=layout)
    _log_runs.submit("emo_yearly_tau", runs)
