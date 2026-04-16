from __future__ import annotations

from .forecast_skill import ForecastSkillConfig, run_forecast_skill_pipeline
from .gdelt import GDELTTopicConfig, run_gdelt_timeline_pipeline
from .openalex import OpenAlexConceptConfig, run_openalex_pipeline
from .owid import OWIDChartConfig, run_owid_pipeline


def emo_daily_attention() -> None:
    run_gdelt_timeline_pipeline(
        [
            GDELTTopicConfig(
                keyword="climate change",
                start_date="2025-01-01",
                end_date="2025-12-31",
                label="climate_change",
            ),
            GDELTTopicConfig(
                keyword="biodiversity loss",
                start_date="2025-01-01",
                end_date="2025-12-31",
                label="biodiversity_loss",
            ),
            GDELTTopicConfig(
                keyword="pandemic preparedness",
                start_date="2025-01-01",
                end_date="2025-12-31",
                label="pandemic_preparedness",
            ),
            GDELTTopicConfig(
                keyword="nuclear risk",
                start_date="2025-01-01",
                end_date="2025-12-31",
                label="nuclear_risk",
            ),
            GDELTTopicConfig(
                keyword="artificial intelligence safety",
                start_date="2025-01-01",
                end_date="2025-12-31",
                label="ai_safety",
            ),
        ]
    )


def emo_weekly_synergy() -> None:
    run_openalex_pipeline(
        [
            OpenAlexConceptConfig(
                label="climate_change",
                display_name_search="climate change",
                year_from=2020,
                year_to=2025,
            ),
            OpenAlexConceptConfig(
                label="pandemic_preparedness",
                display_name_search="pandemic preparedness",
                year_from=2020,
                year_to=2025,
            ),
        ]
    )


def emo_monthly_oi_smf() -> None:
    run_owid_pipeline(
        OWIDChartConfig(
            chart_id="co2-emissions",
            label="co2_emissions",
        )
    )


def emo_yearly_tau() -> None:
    run_forecast_skill_pipeline(
        ForecastSkillConfig(
            url="https://example.org/forecast_skill.csv",
            canonical_name="forecast_skill",
        )
    )
