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
        if fn is None:
            def wrapper(f):
                return f
            return wrapper
        return fn

    flow = _identity_decorator
    task = _identity_decorator

from emo.ingestion import (
    DataLakeLayout,
    PipelineRun,
    emo_daily_attention,
    emo_weekly_synergy,
    emo_monthly_oi_smf,
    emo_yearly_tau,
    ForecastSkillConfig,
)

LOG = logging.getLogger(__name__)


@task
def _log_runs(name: str, runs: List[PipelineRun]) -> None:
    total = sum((r.records or 0) for r in runs)
    LOG.info("Flow %s completed %d runs, total records=%s", name, len(runs), total)


@flow(name="EMO Daily Attention")
def emo_daily_attention_flow() -> None:
    """
    Daily Prefect flow:

    - Ingest daily attention data (e.g., IATI / WFP / other feeds).
    """
    layout = DataLakeLayout.from_env()
    runs = emo_daily_attention(layout=layout)
    _log_runs.submit("emo_daily_attention", runs)


@flow(name="EMO Weekly Synergy")
def emo_weekly_synergy_flow() -> None:
    """
    Weekly Prefect flow:

    - Run weekly synergy / O-information analyses.
    """
    layout = DataLakeLayout.from_env()
    runs = emo_weekly_synergy(layout=layout)
    _log_runs.submit("emo_weekly_synergy", runs)


@flow(name="EMO Monthly OI & SMF")
def emo_monthly_oi_smf_flow() -> None:
    """
    Monthly Prefect flow:

    - Compute organismality index and SMF metrics.
    """
    layout = DataLakeLayout.from_env()
    runs = emo_monthly_oi_smf(layout=layout)
    _log_runs.submit("emo_monthly_oi_smf", runs)


@flow(name="EMO Yearly TauI")
def emo_yearly_tau_flow(
    forecast_skill_url: str = "https://example.org/ecmwf_headline_scores.csv",
) -> None:
    """
    Yearly Prefect flow:

    - Forecast-skill CSV mirroring for τ_I.

    Replace the default URL with the real source from ECMWF / C3S or
    similar forecast-skill provider.
    """
    layout = DataLakeLayout.from_env()
    cfg = ForecastSkillConfig(
        url=forecast_skill_url,
        canonical_name="ecmwf_headline_scores",
    )
    runs = emo_yearly_tau(skill_config=cfg, layout=layout)
    _log_runs.submit("emo_yearly_tau", runs)
