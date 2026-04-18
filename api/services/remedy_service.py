from __future__ import annotations

from dataclasses import asdict
from typing import Any

from emo.remedy.legitimacy import build_legitimacy_report
from emo.remedy.tradeoffs import build_tradeoff_report
from emo.remedy.simulation import simulate_remedy_pathways
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
def build_remedy_explain_result(payload: RemedyRequest) -> dict:
    pipeline = _build_remedy_pipeline(payload)

    profile = pipeline["profile"]
    portfolio = pipeline["portfolio"]
    score = pipeline["score"]

    bottlenecks = profile.dominant_bottlenecks or ["none clearly isolated"]
    option_names = [option.name for option in portfolio.options] or ["no options selected"]

    explanation = (
        f"Dominant bottlenecks: {', '.join(bottlenecks)}. "
        f"Recommended portfolio: {', '.join(option_names)}. "
        f"Overall score: {score.overall_score:.3f}. "
        f"Feasibility: {score.feasibility:.3f}. "
        f"Expected DAC gain: {score.expected_dac_gain:.3f}. "
        f"Persistence likelihood: {score.persistence_likelihood:.3f}. "
        f"Contradiction risk: {score.contradiction_risk:.3f}. "
        f"Justice risk: {score.justice_risk:.3f}. "
        "This explanation is rule-based and provisional."
    )

    return {
        "explanation": explanation,
        "profile": asdict(profile),
        "portfolio": asdict(portfolio),
        "score": asdict(score),
    }
def build_remedy_simulation_result(payload: RemedyRequest) -> dict:
    pipeline = _build_remedy_pipeline(payload)

    simulations = simulate_remedy_pathways(
        portfolio=pipeline["portfolio"],
        score=pipeline["score"],
    )

    return {
        "profile": asdict(pipeline["profile"]),
        "portfolio": asdict(pipeline["portfolio"]),
        "score": asdict(pipeline["score"]),
        "simulations": [asdict(simulation) for simulation in simulations],
    }
def build_remedy_tradeoff_result(payload: RemedyRequest) -> dict:
    pipeline = _build_remedy_pipeline(payload)

    tradeoff_report = build_tradeoff_report(pipeline["score"])

    return {
        "profile": asdict(pipeline["profile"]),
        "portfolio": asdict(pipeline["portfolio"]),
        "score": asdict(pipeline["score"]),
        "tradeoff_report": asdict(tradeoff_report),
    }
def build_remedy_legitimacy_result(payload: RemedyRequest) -> dict:
    pipeline = _build_remedy_pipeline(payload)

    legitimacy_report = build_legitimacy_report(pipeline["options"])

    return {
        "profile": asdict(pipeline["profile"]),
        "portfolio": asdict(pipeline["portfolio"]),
        "legitimacy_report": asdict(legitimacy_report),
    }
