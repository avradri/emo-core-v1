# emo/ingestion/pipelines.py
from __future__ import annotations

import logging
from typing import List, Optional

from .base import DataLakeLayout, PipelineRun
from .gdelt import GDELTTopicConfig, run_gdelt_timeline_pipeline
from .wikipedia import WikipediaArticleConfig, run_wikipedia_pageviews_pipeline
from .owid import OWIDChartConfig, run_owid_pipeline
from .openalex import OpenAlexConceptConfig, run_openalex_pipeline
from .forecast_skill import ForecastSkillConfig, run_forecast_skill_pipeline

LOG = logging.getLogger(__name__)


def emo_daily_attention(
    layout: Optional[DataLakeLayout] = None,
) -> List[PipelineRun]:
    """
    Daily pipeline:

    - GDELT timelines for a small topic set
    - Wikipedia pageviews for matching articles
    """
    layout = layout or DataLakeLayout.from_env()

    topics = [
        GDELTTopicConfig(keyword="climate change", label="climate_change", timespan="3m"),
        GDELTTopicConfig(keyword="extreme heat", label="extreme_heat", timespan="3m"),
        GDELTTopicConfig(keyword="floods OR flooding", label="floods", timespan="3m"),
        GDELTTopicConfig(keyword="pandemic", label="pandemic", timespan="3m"),
        GDELTTopicConfig(keyword='"artificial intelligence" AND safety', label="ai_safety", timespan="3m"),
    ]
    wiki_articles = [
        WikipediaArticleConfig(
            project="en.wikipedia.org",
            article="Climate_change",
            start="20150101",
            end="20251231",
        ),
        WikipediaArticleConfig(
            project="en.wikipedia.org",
            article="Intergovernmental_Panel_on_Climate_Change",
            start="20150101",
            end="20251231",
        ),
        WikipediaArticleConfig(
            project="en.wikipedia.org",
            article="COVID-19_pandemic",
            start="20191201",
            end="20251231",
        ),
    ]

    runs: List[PipelineRun] = []
    runs.append(run_gdelt_timeline_pipeline(topics, layout=layout))
    runs.append(run_wikipedia_pageviews_pipeline(wiki_articles, layout=layout))
    return runs


def emo_weekly_synergy(
    layout: Optional[DataLakeLayout] = None,
) -> List[PipelineRun]:
    """
    Weekly pipeline:

    - OpenAlex topic timelines for a core set of concepts / topics.
    - OWID charts for complementary macro indicators (planetary boundaries,
      emissions, etc.).
    """
    layout = layout or DataLakeLayout.from_env()

    concepts = [
        OpenAlexConceptConfig(
            label="climate_change",
            display_name_search="climate change",
            year_from=1990,
            year_to=2025,
        ),
        OpenAlexConceptConfig(
            label="pandemics",
            display_name_search="pandemic",
            year_from=1990,
            year_to=2025,
        ),
        OpenAlexConceptConfig(
            label="ai_safety",
            display_name_search="artificial intelligence safety",
            year_from=1990,
            year_to=2025,
        ),
    ]
    # You can add specific OWID charts here as needed
    owid_charts = [
        OWIDChartConfig(chart_id="co2"),
        OWIDChartConfig(chart_id="ghg-emissions-by-sector"),  # adjust to real IDs
    ]

    runs: List[PipelineRun] = []
    runs.append(run_openalex_pipeline(concepts, layout=layout))
    runs.append(run_owid_pipeline(owid_charts, layout=layout))
    return runs


def emo_monthly_oi_smf(
    layout: Optional[DataLakeLayout] = None,
) -> List[PipelineRun]:
    """
    Monthly pipeline:

    - OWID charts for OI & SMF inputs (treaties, emissions, planetary boundaries).
    - You can extend this to run the metric engines directly (OI, SMF) once
      your metric modules are wired to read from the feature tables.

    For now, we focus on ingestion; metric computation can be called from
    a higher-level orchestration layer if desired.
    """
    layout = layout or DataLakeLayout.from_env()

    owid_charts = [
        OWIDChartConfig(chart_id="co2"),
        OWIDChartConfig(chart_id="co2-per-capita"),
        OWIDChartConfig(chart_id="cumulative-co2"),
        # Add treaty/boundary charts as needed
    ]

    runs: List[PipelineRun] = []
    runs.append(run_owid_pipeline(owid_charts, layout=layout))
    return runs


def emo_yearly_tau(
    skill_config: ForecastSkillConfig,
    layout: Optional[DataLakeLayout] = None,
) -> List[PipelineRun]:
    """
    Yearly pipeline:

    - Mirror forecast-skill CSVs for τ_I (information-time) computation.
    """
    layout = layout or DataLakeLayout.from_env()
    runs: List[PipelineRun] = []
    runs.append(run_forecast_skill_pipeline(skill_config, layout=layout))
    return runs
