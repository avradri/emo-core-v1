from __future__ import annotations

from emo.models.portfolio_score import PortfolioScore
from emo.models.remedy_comparison import RemedyComparisonReport
from emo.models.remedy_portfolio import RemedyPortfolio
from emo.models.remedy_tradeoff import RemedyTradeoffReport


def build_explanation(
    portfolio: RemedyPortfolio,
    score: PortfolioScore,
    tradeoff_report: RemedyTradeoffReport,
    comparison_report: RemedyComparisonReport | None = None,
    dominant_bottlenecks: list[str] | None = None,
) -> str:
    bottlenecks = dominant_bottlenecks or ["none clearly isolated"]
    option_names = [option.name for option in portfolio.options] or ["no options selected"]

    comparison_line = ""
    if comparison_report and comparison_report.comparisons:
        best = max(
            comparison_report.comparisons,
            key=lambda item: item.overall_score,
        )
        comparison_line = (
            f" Best comparison variant: {best.portfolio_label} "
            f"({best.overall_score:.3f})."
        )

    explanation = (
        f"Dominant bottlenecks: {', '.join(bottlenecks)}. "
        f"Recommended portfolio: {', '.join(option_names)}. "
        f"Overall score: {score.overall_score:.3f}. "
        f"Feasibility: {score.feasibility:.3f}. "
        f"Expected DAC gain: {score.expected_dac_gain:.3f}. "
        f"Persistence likelihood: {score.persistence_likelihood:.3f}. "
        f"Contradiction risk: {score.contradiction_risk:.3f}. "
        f"Justice risk: {score.justice_risk:.3f}. "
        f"Legitimacy penalty: {score.legitimacy_penalty:.3f}. "
        f"Tradeoff summary: {tradeoff_report.summary}."
        f"{comparison_line} "
        "This explanation is rule-based and provisional."
    )

    return explanation
