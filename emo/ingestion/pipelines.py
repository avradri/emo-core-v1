from __future__ import annotations

import logging

from .base import DataLakeLayout, PipelineRun
from .forecast_skill import ForecastSkillConfig, run_forecast_skill_pipeline
from .gdelt import GDELTTopicConfig, run_gdelt_timeline_pipeline
from .openalex import OpenAlexConceptConfig, run_openalex_pipeline
from .owid import OWIDChartConfig, run_owid_pipeline
from .wikipedia import WikipediaArticleConfig, run_wikipedia_pageviews_pipeline

LOG = logging.getLogger(__name__)


def emo_daily_attention(
    layout: DataLakeLayout | None = None,
) -> list[PipelineRun]:
    """
    Daily pipeline:

    - GDELT timelines for a small topic set
    - Wikipedia pageviews for matching articles
    """
    layout = layout or DataLakeLayout.from_env()

    topics = [
        GDELTTopicConfig(
            keyword="climate change",
            start_date="2025-01-01",
            end_date="2025-12-31",
            label="climate_change",
        ),
        GDELTTopicConfig(
            keyword="extreme heat",
            start_date="2025-01-01",
            end_date="2025-12-31",
            label="extreme_heat",
        ),
        GDELTTopicConfig(
            keyword="floods OR flooding",
            start_date="2025-01-01",
            end_date="2025-12-31",
            label="floods",
        ),
        GDELTTopicConfig(
            keyword="pandemic",
            start_date="2025-01-01",
            end_date="2025-12-31",
            label="pandemic",
        ),
        GDELTTopicConfig(
            keyword='"artificial intelligence" AND safety',
            start_date="2025-01-01",
            end_date="2025-12-31",
            label="ai_safety",
        ),
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

    runs: list[PipelineRun] = []
    runs.append(run_gdelt_timeline_pipeline(topics, layout=layout))
    runs.append(run_wikipedia_pageviews_pipeline(wiki_articles, layout=layout))
    return runs


def emo_weekly_synergy(
    layout: DataLakeLayout | None = None,
) -> list[PipelineRun]:
    """
    Weekly pipeline:

    - OpenAlex topic timelines for a core set of concepts / topics.
    - OWID charts for complementary macro indicators.
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

    owid_charts = [
        OWIDChartConfig(chart_id="co2"),
        OWIDChartConfig(chart_id="ghg-emissions-by-sector"),
    ]

    runs: list[PipelineRun] = []
    runs.append(run_openalex_pipeline(concepts, layout=layout))
    runs.append(run_owid_pipeline(owid_charts, layout=layout))
    return runs


def emo_monthly_oi_smf(
    layout: DataLakeLayout | None = None,
) -> list[PipelineRun]:
    """
    Monthly pipeline:

    - OWID charts for OI & SMF inputs.
    """
    layout = layout or DataLakeLayout.from_env()

    owid_charts = [
        OWIDChartConfig(chart_id="co2"),
        OWIDChartConfig(chart_id="co2-per-capita"),
        OWIDChartConfig(chart_id="cumulative-co2"),
    ]

    runs: list[PipelineRun] = []
    runs.append(run_owid_pipeline(owid_charts, layout=layout))
    return runs


def emo_yearly_tau(
    skill_config: ForecastSkillConfig,
    layout: DataLakeLayout | None = None,
) -> list[PipelineRun]:
    """
    Yearly pipeline:

    - Mirror forecast-skill CSVs for τ_I computation.
    """
    layout = layout or DataLakeLayout.from_env()

    runs: list[PipelineRun] = []
    runs.append(run_forecast_skill_pipeline(skill_config, layout=layout))
    return runs
