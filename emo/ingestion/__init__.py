# emo/ingestion/__init__.py
from .base import DataLakeLayout, PipelineRun
from .owid import OWIDChartConfig, run_owid_pipeline
from .gdelt import GDELTTopicConfig, run_gdelt_timeline_pipeline
from .wikipedia import WikipediaArticleConfig, run_wikipedia_pageviews_pipeline
from .openalex import OpenAlexConceptConfig, run_openalex_pipeline
from .forecast_skill import ForecastSkillConfig, run_forecast_skill_pipeline
from .pipelines import (
    emo_daily_attention,
    emo_weekly_synergy,
    emo_monthly_oi_smf,
    emo_yearly_tau,
)

__all__ = [
    "DataLakeLayout",
    "PipelineRun",
    "OWIDChartConfig",
    "run_owid_pipeline",
    "GDELTTopicConfig",
    "run_gdelt_timeline_pipeline",
    "WikipediaArticleConfig",
    "run_wikipedia_pageviews_pipeline",
    "OpenAlexConceptConfig",
    "run_openalex_pipeline",
    "ForecastSkillConfig",
    "run_forecast_skill_pipeline",
    "emo_daily_attention",
    "emo_weekly_synergy",
    "emo_monthly_oi_smf",
    "emo_yearly_tau",
]
