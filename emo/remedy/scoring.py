from __future__ import annotations

from emo.models.portfolio_score import PortfolioScore
from emo.models.remedy_portfolio import RemedyPortfolio

_CAPACITY_TO_FEASIBILITY = {
    "low": 0.9,
    "medium": 0.65,
    "high": 0.4,
}

_TIME_TO_EFFECT_TO_GAIN = {
    "short": 0.85,
    "medium": 0.65,
    "long": 0.45,
}

_EVIDENCE_TO_PERSISTENCE = {
    "conceptual": 0.4,
    "moderate": 0.65,
    "strong": 0.85,
}

_RISK_TO_VALUE = {
    "low": 0.2,
    "medium": 0.5,
    "high": 0.8,
}


def _average(values: list[float]) -> float:
    if not values:
        return 0.0
    return sum(values) / len(values)


def _compute_legitimacy_penalty(justice_risk: float) -> float:
    """
    v0.1 legitimacy-aware scoring:
    use justice risk as a first visible legitimacy penalty.
    """
    return round(0.12 * justice_risk, 3)


def score_portfolio(portfolio: RemedyPortfolio) -> PortfolioScore:
    """
    Transparent v0.1 scoring for remedy portfolios.
    """
    if not portfolio.options:
        return PortfolioScore(
            portfolio_id=portfolio.portfolio_id,
            feasibility=0.0,
            expected_dac_gain=0.0,
            persistence_likelihood=0.0,
            contradiction_risk=0.0,
            semantic_efficiency=0.0,
            justice_risk=0.0,
            legitimacy_penalty=0.0,
            overall_score=0.0,
            notes=["No intervention options were available in the portfolio."],
        )

    feasibility = _average(
        [
            _CAPACITY_TO_FEASIBILITY.get(option.required_capacity, 0.5)
            for option in portfolio.options
        ]
    )

    expected_dac_gain = _average(
        [
            _TIME_TO_EFFECT_TO_GAIN.get(option.time_to_effect, 0.5)
            for option in portfolio.options
        ]
    )

    persistence_likelihood = _average(
        [
            _EVIDENCE_TO_PERSISTENCE.get(option.evidence_level, 0.5)
            for option in portfolio.options
        ]
    )

    contradiction_risk = _average(
        [
            _RISK_TO_VALUE.get(option.coordination_cost, 0.5)
            for option in portfolio.options
        ]
    )

    justice_risk = _average(
        [
            _RISK_TO_VALUE.get(option.rights_risk, 0.5)
            for option in portfolio.options
        ]
    )

    semantic_efficiency = _average(
        [
            (
                _TIME_TO_EFFECT_TO_GAIN.get(option.time_to_effect, 0.5)
                + (1.0 - _RISK_TO_VALUE.get(option.coordination_cost, 0.5))
            )
            / 2.0
            for option in portfolio.options
        ]
    )

    legitimacy_penalty = _compute_legitimacy_penalty(justice_risk)

    overall_score = (
        0.24 * feasibility
        + 0.24 * expected_dac_gain
        + 0.20 * persistence_likelihood
        + 0.18 * semantic_efficiency
        - 0.08 * contradiction_risk
        - 0.06 * justice_risk
        - legitimacy_penalty
    )

    overall_score = max(0.0, min(1.0, overall_score))

    notes = [
        "Score is rule-based and provisional.",
        "Higher overall score suggests a more plausible v0.1 portfolio.",
        "Contradiction and justice risks act as penalties, not hard exclusions.",
        "Legitimacy penalty currently uses justice risk as a first-pass proxy.",
    ]

    return PortfolioScore(
        portfolio_id=portfolio.portfolio_id,
        feasibility=round(feasibility, 3),
        expected_dac_gain=round(expected_dac_gain, 3),
        persistence_likelihood=round(persistence_likelihood, 3),
        contradiction_risk=round(contradiction_risk, 3),
        semantic_efficiency=round(semantic_efficiency, 3),
        justice_risk=round(justice_risk, 3),
        legitimacy_penalty=round(legitimacy_penalty, 3),
        overall_score=round(overall_score, 3),
        notes=notes,
    )
