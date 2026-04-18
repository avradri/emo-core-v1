from __future__ import annotations

from dataclasses import asdict
from typing import Any

from api.schemas.remedy_request import RemedyLearningRequest, RemedyRequest
from emo.models.bottleneck_profile import BottleneckProfile
from emo.models.portfolio_score import PortfolioScore
from emo.models.remedy_portfolio import RemedyPortfolio
from emo.remedy.bottlenecks import classify_bottlenecks
from emo.remedy.comparison import build_portfolio_comparison_report
from emo.remedy.explain import build_explanation
from emo.remedy.intervention_library import get_intervention_options, get_remedy_library
from emo.remedy.learning import build_learning_report
from emo.remedy.legitimacy import build_legitimacy_report
from emo.remedy.portfolio_builder import build_remedy_portfolio
from emo.remedy.scoring import score_portfolio
from emo.remedy.simulation import simulate_remedy_pathways
from emo.remedy.tradeoffs import build_tradeoff_report


def _build_profile(
    payload: RemedyRequest | RemedyLearningRequest,
) -> BottleneckProfile:
    return classify_bottlenecks(
        domain=payload.domain,
        jurisdiction=payload.jurisdiction,
        validation_score=payload.validation_score,
        translation_score=payload.translation_score,
        budget_score=payload.budget_score,
        deployment_score=payload.deployment_score,
        persistence_score=payload.persistence_score,
        contradiction_score=payload.contradiction_score,
    )


def _build_remedy_pipeline(
    payload: RemedyRequest | RemedyLearningRequest,
) -> dict[str, BottleneckProfile | RemedyPortfolio | PortfolioScore]:
    profile = _build_profile(payload)
    options = get_intervention_options(profile.domain, profile.dominant_bottlenecks)
    portfolio = build_remedy_portfolio(profile, options)
    score = score_portfolio(portfolio, profile)

    return {
        "profile": profile,
        "portfolio": portfolio,
        "score": score,
    }


def build_remedy_profile(payload: RemedyRequest) -> dict[str, Any]:
    profile = _build_profile(payload)
    return asdict(profile)


def build_remedy_options(payload: RemedyRequest) -> dict[str, Any]:
    profile = _build_profile(payload)
    options = get_intervention_options(profile.domain, profile.dominant_bottlenecks)

    return {
        "profile": asdict(profile),
        "options": [asdict(option) for option in options],
    }


def build_remedy_portfolio_result(payload: RemedyRequest) -> dict[str, Any]:
    pipeline = _build_remedy_pipeline(payload)

    return {
        "profile": asdict(pipeline["profile"]),
        "portfolio": asdict(pipeline["portfolio"]),
    }


def build_remedy_score_result(payload: RemedyRequest) -> dict[str, Any]:
    pipeline = _build_remedy_pipeline(payload)

    return {
        "profile": asdict(pipeline["profile"]),
        "portfolio": asdict(pipeline["portfolio"]),
        "score": asdict(pipeline["score"]),
    }


def build_remedy_library_result(domain: str | None = None) -> dict[str, Any]:
    library = get_remedy_library(domain)

    return {
        "library": {
            name: [asdict(option) for option in options]
            for name, options in library.items()
        }
    }


def build_remedy_explain_result(payload: RemedyRequest) -> dict[str, Any]:
    pipeline = _build_remedy_pipeline(payload)

    profile = pipeline["profile"]
    portfolio = pipeline["portfolio"]
    score = pipeline["score"]

    tradeoff_report = build_tradeoff_report(score)
    comparison_report = build_portfolio_comparison_report(portfolio)

    explanation = build_explanation(
        portfolio=portfolio,
        score=score,
        tradeoff_report=tradeoff_report,
        comparison_report=comparison_report,
        dominant_bottlenecks=profile.dominant_bottlenecks,
    )

    return {
        "explanation": explanation,
        "profile": asdict(profile),
        "portfolio": asdict(portfolio),
        "score": asdict(score),
    }


def build_remedy_simulation_result(payload: RemedyRequest) -> dict[str, Any]:
    pipeline = _build_remedy_pipeline(payload)

    simulations = simulate_remedy_pathways(
        pipeline["profile"],
        pipeline["portfolio"],
        pipeline["score"],
    )

    return {
        "profile": asdict(pipeline["profile"]),
        "portfolio": asdict(pipeline["portfolio"]),
        "score": asdict(pipeline["score"]),
        "simulations": [asdict(item) for item in simulations],
    }


def build_remedy_tradeoff_result(payload: RemedyRequest) -> dict[str, Any]:
    pipeline = _build_remedy_pipeline(payload)

    tradeoff_report = build_tradeoff_report(pipeline["score"])

    return {
        "profile": asdict(pipeline["profile"]),
        "portfolio": asdict(pipeline["portfolio"]),
        "score": asdict(pipeline["score"]),
        "tradeoff_report": asdict(tradeoff_report),
    }


def build_remedy_legitimacy_result(payload: RemedyRequest) -> dict[str, Any]:
    pipeline = _build_remedy_pipeline(payload)

    legitimacy_report = build_legitimacy_report(
        pipeline["profile"],
        pipeline["portfolio"],
        pipeline["score"],
    )

    return {
        "profile": asdict(pipeline["profile"]),
        "portfolio": asdict(pipeline["portfolio"]),
        "score": asdict(pipeline["score"]),
        "legitimacy_report": asdict(legitimacy_report),
    }


def build_remedy_comparison_result(payload: RemedyRequest) -> dict[str, Any]:
    pipeline = _build_remedy_pipeline(payload)

    comparison_report = build_portfolio_comparison_report(pipeline["portfolio"])

    return {
        "profile": asdict(pipeline["profile"]),
        "portfolio": asdict(pipeline["portfolio"]),
        "comparison_report": asdict(comparison_report),
    }


def build_remedy_learning_result(payload: RemedyLearningRequest) -> dict[str, Any]:
    pipeline = _build_remedy_pipeline(payload)

    learning_report = build_learning_report(
        score=pipeline["score"],
        observed_dac_gain=payload.observed_dac_gain,
        observed_persistence=payload.observed_persistence,
    )

    return {
        "profile": asdict(pipeline["profile"]),
        "portfolio": asdict(pipeline["portfolio"]),
        "score": asdict(pipeline["score"]),
        "learning_report": asdict(learning_report),
    }
