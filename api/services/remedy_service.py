from __future__ import annotations

from dataclasses import asdict
from typing import Any

from emo.remedy.intervention_library import get_remedy_library
from api.schemas.remedy_request import RemedyRequest
from emo.models.bottleneck_profile import BottleneckProfile
from emo.models.intervention_option import InterventionOption
from emo.models.portfolio_score import PortfolioScore
from emo.models.remedy_portfolio import RemedyPortfolio
from emo.remedy.bottlenecks import classify_bottlenecks
from emo.remedy.intervention_library import get_intervention_options
from emo.remedy.portfolio_builder import build_remedy_portfolio
from emo.remedy.scoring import score_portfolio


def _build_remedy_pipeline(payload: RemedyRequest) -> dict[str, Any]:
    profile: BottleneckProfile = classify_bottlenecks(
        domain=payload.domain,
        jurisdiction=payload.jurisdiction,
        validation_score=payload.validation_score,
        translation_score=payload.translation_score,
        budget_score=payload.budget_score,
        deployment_score=payload.deployment_score,
        persistence_score=payload.persistence_score,
        contradiction_score=payload.contradiction_score,
    )

    options: list[InterventionOption] = get_intervention_options(
        payload.domain,
        profile.dominant_bottlenecks,
    )

    portfolio: RemedyPortfolio = build_remedy_portfolio(
        profile=profile,
        options=options,
    )

    score: PortfolioScore = score_portfolio(portfolio)

    return {
        "profile": profile,
        "options": options,
        "portfolio": portfolio,
        "score": score,
    }


def build_remedy_profile(payload: RemedyRequest) -> dict:
    pipeline = _build_remedy_pipeline(payload)
    return asdict(pipeline["profile"])


def build_remedy_options(payload: RemedyRequest) -> dict:
    pipeline = _build_remedy_pipeline(payload)
    return {
        "profile": asdict(pipeline["profile"]),
        "options": [asdict(option) for option in pipeline["options"]],
    }


def build_remedy_portfolio_result(payload: RemedyRequest) -> dict:
    pipeline = _build_remedy_pipeline(payload)
    return {
        "profile": asdict(pipeline["profile"]),
        "portfolio": asdict(pipeline["portfolio"]),
    }


def build_remedy_score_result(payload: RemedyRequest) -> dict:
    pipeline = _build_remedy_pipeline(payload)
    return {
        "profile": asdict(pipeline["profile"]),
        "portfolio": asdict(pipeline["portfolio"]),
        "score": asdict(pipeline["score"]),
    }
def build_remedy_library_result(domain: str | None = None) -> dict:
    library = get_remedy_library(domain)

    return {
        "library": {
            name: [asdict(option) for option in options]
            for name, options in library.items()
        }
    }
