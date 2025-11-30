# orchestration/prefect_flows.py
from __future__ import annotations

import logging
from typing import List

from prefect import flow, task

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

    - GDELT timelines
    - Wikipedia pageviews
    """
    layout = DataLakeLayout.from_env()
    runs = emo_daily_attention(layout=layout)
    _log_runs.submit("emo_daily_attention", runs)


@flow(name="EMO Weekly Synergy")
def emo_weekly_synergy_flow() -> None:
    """
    Weekly Prefect flow:

    - OpenAlex topic timelines
    - OWID macro indicators
    """
    layout = DataLakeLayout.from_env()
    runs = emo_weekly_synergy(layout=layout)
    _log_runs.submit("emo_weekly_synergy", runs)


@flow(name="EMO Monthly OI & SMF")
def emo_monthly_oi_smf_flow() -> None:
    """
    Monthly Prefect flow:

    - OWID charts for OI and SMF.
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
