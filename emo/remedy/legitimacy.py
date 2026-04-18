from __future__ import annotations

from emo.models.intervention_option import InterventionOption
from emo.models.legitimacy_report import LegitimacyFlag, LegitimacyReport


def _max_rights_risk(options: list[InterventionOption]) -> str:
    if any(option.rights_risk == "high" for option in options):
        return "high"
    if any(option.rights_risk == "medium" for option in options):
        return "medium"
    return "low"


def build_legitimacy_report(options: list[InterventionOption]) -> LegitimacyReport:
    rights_level = _max_rights_risk(options)

    flags: list[LegitimacyFlag] = []

    if rights_level == "high":
        flags.append(
            LegitimacyFlag(
                category="rights_risk",
                level="high",
                message="The portfolio contains at least one high rights-risk measure.",
            )
        )
    elif rights_level == "medium":
        flags.append(
            LegitimacyFlag(
                category="rights_risk",
                level="moderate",
                message="The portfolio contains measures that may require stronger safeguards.",
            )
        )
    else:
        flags.append(
            LegitimacyFlag(
                category="rights_risk",
                level="low",
                message="No major rights-risk signal is currently visible in the portfolio.",
            )
        )

    flags.append(
        LegitimacyFlag(
            category="transparency",
            level="required",
            message="Portfolio logic should remain explainable and publicly contestable.",
        )
    )

    flags.append(
        LegitimacyFlag(
            category="contestability",
            level="required",
            message="Affected actors should be able to challenge or revise remedy choices.",
        )
    )

    flags.append(
        LegitimacyFlag(
            category="coercion_risk",
            level="watch",
            message="Implementation should be reviewed for coercive spillovers under stress.",
        )
    )

    summary = (
        f"Legitimacy review indicates rights risk is {rights_level}, while transparency "
        "and contestability remain mandatory constraints."
    )

    return LegitimacyReport(summary=summary, flags=flags)
