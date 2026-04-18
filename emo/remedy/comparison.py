from __future__ import annotations

from emo.models.portfolio_score import PortfolioScore
from emo.models.remedy_comparison import RemedyComparisonItem, RemedyComparisonReport
from emo.models.remedy_portfolio import RemedyPortfolio
from emo.remedy.scoring import score_portfolio


def _clone_portfolio_with_subset(
    portfolio: RemedyPortfolio,
    option_count: int,
    label: str,
) -> RemedyPortfolio:
    selected_options = portfolio.options[:option_count]
    selected_sequence = [option.name for option in selected_options]

    return RemedyPortfolio(
        portfolio_id=f"{portfolio.portfolio_id}_{label}",
        domain=portfolio.domain,
        jurisdiction=portfolio.jurisdiction,
        options=selected_options,
        sequence=selected_sequence,
        rationale=portfolio.rationale,
        assumptions=portfolio.assumptions,
    )


def _item_from_score(
    label: str,
    portfolio: RemedyPortfolio,
    score: PortfolioScore,
) -> RemedyComparisonItem:
    return RemedyComparisonItem(
        portfolio_label=label,
        sequence=portfolio.sequence,
        overall_score=score.overall_score,
        feasibility=score.feasibility,
        expected_dac_gain=score.expected_dac_gain,
        persistence_likelihood=score.persistence_likelihood,
        contradiction_risk=score.contradiction_risk,
        justice_risk=score.justice_risk,
        semantic_efficiency=score.semantic_efficiency,
    )


def build_portfolio_comparison_report(portfolio: RemedyPortfolio) -> RemedyComparisonReport:
    """
    Compare three simple portfolio variants:
    - baseline: first option only
    - compact: first two options
    - full: first three options
    """
    variants: list[tuple[str, int]] = [
        ("baseline", 1),
        ("compact", 2),
        ("full", 3),
    ]

    comparisons: list[RemedyComparisonItem] = []

    for label, count in variants:
        variant_portfolio = _clone_portfolio_with_subset(portfolio, count, label)
        variant_score = score_portfolio(variant_portfolio)
        comparisons.append(_item_from_score(label, variant_portfolio, variant_score))

    best = max(comparisons, key=lambda item: item.overall_score)
    summary = (
        f"Compared {len(comparisons)} portfolio variants. "
        f"Highest overall score: {best.portfolio_label} ({best.overall_score:.3f})."
    )

    return RemedyComparisonReport(summary=summary, comparisons=comparisons)
