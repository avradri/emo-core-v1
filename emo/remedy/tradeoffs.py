from __future__ import annotations

from emo.models.portfolio_score import PortfolioScore
from emo.models.remedy_tradeoff import RemedyTradeoff, RemedyTradeoffReport


def _interpret_positive(value: float) -> str:
    if value >= 0.75:
        return "strong"
    if value >= 0.5:
        return "moderate"
    return "weak"


def _interpret_risk(value: float) -> str:
    if value >= 0.75:
        return "high"
    if value >= 0.5:
        return "moderate"
    return "low"


def build_tradeoff_report(score: PortfolioScore) -> RemedyTradeoffReport:
    tradeoffs = [
        RemedyTradeoff(
            dimension="feasibility",
            value=score.feasibility,
            interpretation=_interpret_positive(score.feasibility),
        ),
        RemedyTradeoff(
            dimension="expected_dac_gain",
            value=score.expected_dac_gain,
            interpretation=_interpret_positive(score.expected_dac_gain),
        ),
        RemedyTradeoff(
            dimension="persistence_likelihood",
            value=score.persistence_likelihood,
            interpretation=_interpret_positive(score.persistence_likelihood),
        ),
        RemedyTradeoff(
            dimension="contradiction_risk",
            value=score.contradiction_risk,
            interpretation=_interpret_risk(score.contradiction_risk),
        ),
        RemedyTradeoff(
            dimension="justice_risk",
            value=score.justice_risk,
            interpretation=_interpret_risk(score.justice_risk),
        ),
        RemedyTradeoff(
            dimension="semantic_efficiency",
            value=score.semantic_efficiency,
            interpretation=_interpret_positive(score.semantic_efficiency),
        ),
        RemedyTradeoff(
            dimension="overall_score",
            value=score.overall_score,
            interpretation=_interpret_positive(score.overall_score),
        ),
    ]

    summary = (
        f"Overall score is {score.overall_score:.3f}; "
        f"feasibility is {_interpret_positive(score.feasibility)}, "
        f"expected DAC gain is {_interpret_positive(score.expected_dac_gain)}, "
        f"persistence is {_interpret_positive(score.persistence_likelihood)}, "
        f"contradiction risk is {_interpret_risk(score.contradiction_risk)}, "
        f"justice risk is {_interpret_risk(score.justice_risk)}."
    )

    return RemedyTradeoffReport(summary=summary, tradeoffs=tradeoffs)
