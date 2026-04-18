from __future__ import annotations

from emo.models.bottleneck_profile import BottleneckProfile
from emo.models.intervention_option import InterventionOption
from emo.models.remedy_portfolio import RemedyPortfolio


def _priority_order_for_bottlenecks(
    dominant_bottlenecks: list[str],
) -> list[str]:
    """
    v0.1 ordering rule:
    repair upstream conversion bottlenecks first, then downstream persistence,
    while contradiction can appear throughout the sequence.
    """
    canonical_order = [
        "validation",
        "translation",
        "budget",
        "deployment",
        "persistence",
        "contradiction",
    ]
    return [name for name in canonical_order if name in dominant_bottlenecks]


def _sort_options_by_bottleneck_priority(
    options: list[InterventionOption],
    priority_order: list[str],
) -> list[InterventionOption]:
    def option_rank(option: InterventionOption) -> tuple[int, str]:
        for index, bottleneck in enumerate(priority_order):
            if bottleneck in option.target_bottlenecks:
                return (index, option.name)
        return (len(priority_order), option.name)

    return sorted(options, key=option_rank)


def _build_sequence_labels(options: list[InterventionOption]) -> list[str]:
    return [option.name for option in options]


def build_remedy_portfolio(
    *,
    profile: BottleneckProfile,
    options: list[InterventionOption],
) -> RemedyPortfolio:
    """
    Build a simple v0.1 remedy portfolio.

    Rules:
    - prioritize options that target dominant bottlenecks
    - preserve transparent ordering rules
    - keep the portfolio compact and readable
    """
    priority_order = _priority_order_for_bottlenecks(profile.dominant_bottlenecks)
    ranked_options = _sort_options_by_bottleneck_priority(options, priority_order)

    selected_options = ranked_options[:3]
    sequence = _build_sequence_labels(selected_options)

    rationale_parts: list[str] = []
    if profile.dominant_bottlenecks:
        rationale_parts.append(
            "Dominant bottlenecks identified: "
            + ", ".join(profile.dominant_bottlenecks)
            + "."
        )
    else:
        rationale_parts.append("No dominant bottleneck was isolated with confidence.")

    if selected_options:
        rationale_parts.append(
            "Portfolio prioritizes: "
            + ", ".join(option.name for option in selected_options)
            + "."
        )
    else:
        rationale_parts.append("No intervention options were available for selection.")

    assumptions = [
        f"Domain context is {profile.domain}.",
        f"Jurisdiction context is {profile.jurisdiction}.",
        "Portfolio is rule-based and exploratory, not prescriptive.",
        "Sequencing follows upstream-to-downstream bottleneck priority.",
    ]

    portfolio_id = (
        f"{profile.domain}_{profile.jurisdiction}_"
        f"{'_'.join(profile.dominant_bottlenecks or ['baseline'])}"
    )

    return RemedyPortfolio(
        portfolio_id=portfolio_id,
        domain=profile.domain,
        jurisdiction=profile.jurisdiction,
        options=selected_options,
        sequence=sequence,
        rationale=" ".join(rationale_parts),
        assumptions=assumptions,
    )

