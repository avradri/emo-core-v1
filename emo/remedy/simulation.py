from __future__ import annotations

from emo.models.portfolio_score import PortfolioScore
from emo.models.remedy_portfolio import RemedyPortfolio
from emo.models.remedy_simulation import RemedySimulationResult


def simulate_remedy_pathways(
    portfolio: RemedyPortfolio,
    score: PortfolioScore,
) -> list[RemedySimulationResult]:
    """
    v0.1 rule-based simulation.

    Compare:
    - do_nothing
    - selected_portfolio
    - high_friction

    This is intentionally modest and transparent.
    """
    do_nothing = RemedySimulationResult(
        scenario="do_nothing",
        expected_dac_improvement=0.05,
        persistence_outlook=0.20,
        contradiction_warning="High likelihood of unresolved bottlenecks.",
        narrative=(
            "Without intervention, dominant bottlenecks are expected to persist "
            "and DAC improvement remains minimal."
        ),
        assumptions=[
            "No new remedy portfolio is activated.",
            "Existing bottlenecks continue to shape response performance.",
        ],
    )

    selected_portfolio = RemedySimulationResult(
        scenario="selected_portfolio",
        expected_dac_improvement=round(score.expected_dac_gain, 3),
        persistence_outlook=round(score.persistence_likelihood, 3),
        contradiction_warning=(
            "Moderate contradiction risk remains."
            if score.contradiction_risk >= 0.5
            else "Contradiction risk appears manageable."
        ),
        narrative=(
            f"The selected portfolio ({', '.join(portfolio.sequence) or 'no sequence'}) "
            "is expected to improve DAC relative to baseline under current assumptions."
        ),
        assumptions=[
            "The selected portfolio is implemented as designed.",
            "Feasibility and persistence remain close to current score assumptions.",
        ],
    )

    high_friction = RemedySimulationResult(
        scenario="high_friction",
        expected_dac_improvement=round(max(0.0, score.expected_dac_gain - 0.25), 3),
        persistence_outlook=round(max(0.0, score.persistence_likelihood - 0.20), 3),
        contradiction_warning="High friction amplifies implementation and coordination risk.",
        narrative=(
            "Under high-friction conditions, the portfolio still helps, but gains are "
            "reduced by coordination stress, resistance, or implementation drag."
        ),
        assumptions=[
            "Coordination burden rises above the current baseline.",
            "Persistence decays faster than expected.",
        ],
    )

    return [do_nothing, selected_portfolio, high_friction]
