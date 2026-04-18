from __future__ import annotations

from emo.models.portfolio_score import PortfolioScore
from emo.models.remedy_learning import RemedyLearningReport


def _classify_adjustment_signal(learning_gap: float, persistence_gap: float) -> str:
    if learning_gap < -0.2 or persistence_gap < -0.2:
        return "downweight"
    if learning_gap > 0.2 and persistence_gap > 0.1:
        return "upweight"
    return "hold"


def build_learning_report(
    score: PortfolioScore,
    observed_dac_gain: float,
    observed_persistence: float,
) -> RemedyLearningReport:
    learning_gap = round(observed_dac_gain - score.expected_dac_gain, 3)
    persistence_gap = round(observed_persistence - score.persistence_likelihood, 3)
    adjustment_signal = _classify_adjustment_signal(learning_gap, persistence_gap)

    notes = [
        "Learning is rule-based and provisional.",
        "Observed outcomes are compared against current portfolio expectations.",
        "Adjustment signals are advisory, not automatic policy updates.",
    ]

    return RemedyLearningReport(
        portfolio_id=score.portfolio_id,
        expected_dac_gain=round(score.expected_dac_gain, 3),
        observed_dac_gain=round(observed_dac_gain, 3),
        learning_gap=learning_gap,
        persistence_gap=persistence_gap,
        adjustment_signal=adjustment_signal,
        notes=notes,
    )
