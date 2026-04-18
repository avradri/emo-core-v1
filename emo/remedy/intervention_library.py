from __future__ import annotations

from emo.models.intervention_option import InterventionOption


DOMAIN_REMEDY_LIBRARY: dict[str, list[InterventionOption]] = {
    "pandemic": [
        InterventionOption(
            option_id="pandemic_procurement_authority",
            family="procurement_logistics",
            name="Emergency procurement authority",
            description=(
                "Create or pre-authorize rapid procurement channels for medical "
                "supplies, reserve stock access, and emergency contracting."
            ),
            target_bottlenecks=["budget", "deployment"],
            required_capacity="medium",
            time_to_effect="short",
            evidence_level="strong",
            rights_risk="low",
            coordination_cost="medium",
            domains=["pandemic"],
        ),
        InterventionOption(
            option_id="pandemic_continuity_funding",
            family="fiscal",
            name="Protected continuity funding",
            description=(
                "Ring-fence surge financing so validated alerts can trigger "
                "immediate operational spending without waiting for ad hoc approvals."
            ),
            target_bottlenecks=["budget", "persistence"],
            required_capacity="medium",
            time_to_effect="short",
            evidence_level="moderate",
            rights_risk="low",
            coordination_cost="low",
            domains=["pandemic"],
        ),
        InterventionOption(
            option_id="pandemic_message_unification",
            family="communication_attention",
            name="Unified public guidance protocol",
            description=(
                "Align central and local risk messaging through pre-agreed guidance "
                "templates, escalation thresholds, and update cadence."
            ),
            target_bottlenecks=["translation", "contradiction"],
            required_capacity="low",
            time_to_effect="short",
            evidence_level="moderate",
            rights_risk="low",
            coordination_cost="medium",
            domains=["pandemic"],
        ),
        InterventionOption(
            option_id="pandemic_staffing_reserve",
            family="infrastructure_capacity",
            name="Reserve staffing and continuity corps",
            description=(
                "Maintain trained reserve staffing mechanisms for surge activation "
                "and continuity of care during prolonged stress."
            ),
            target_bottlenecks=["deployment", "persistence"],
            required_capacity="high",
            time_to_effect="medium",
            evidence_level="moderate",
            rights_risk="low",
            coordination_cost="high",
            domains=["pandemic"],
        ),
    ],
    "disaster": [
        InterventionOption(
            option_id="disaster_mutual_aid_triggers",
            family="coordination_institutional",
            name="Automatic mutual-aid triggers",
            description=(
                "Pre-define cross-jurisdictional support triggers tied to validated "
                "alerts and threshold events."
            ),
            target_bottlenecks=["translation", "deployment"],
            required_capacity="medium",
            time_to_effect="short",
            evidence_level="moderate",
            rights_risk="low",
            coordination_cost="medium",
            domains=["disaster"],
        ),
        InterventionOption(
            option_id="disaster_protected_response_budget",
            family="fiscal",
            name="Protected response budget line",
            description=(
                "Maintain dedicated rapid-release funding for forecast-based early "
                "action and continuity operations."
            ),
            target_bottlenecks=["budget", "persistence"],
            required_capacity="medium",
            time_to_effect="short",
            evidence_level="strong",
            rights_risk="low",
            coordination_cost="low",
            domains=["disaster"],
        ),
        InterventionOption(
            option_id="disaster_local_logistics_cells",
            family="procurement_logistics",
            name="Local logistics activation cells",
            description=(
                "Pre-position logistics coordination capacity, suppliers, transport "
                "fallbacks, and distribution playbooks."
            ),
            target_bottlenecks=["deployment"],
            required_capacity="medium",
            time_to_effect="medium",
            evidence_level="moderate",
            rights_risk="low",
            coordination_cost="medium",
            domains=["disaster"],
        ),
        InterventionOption(
            option_id="disaster_public_warning_protocol",
            family="communication_attention",
            name="Public warning protocol harmonization",
            description=(
                "Standardize warning language, escalation thresholds, and local "
                "instruction formats across institutions."
            ),
            target_bottlenecks=["translation", "contradiction"],
            required_capacity="low",
            time_to_effect="short",
            evidence_level="moderate",
            rights_risk="low",
            coordination_cost="medium",
            domains=["disaster"],
        ),
    ],
}


def get_intervention_options(
    domain: str,
    dominant_bottlenecks: list[str],
) -> list[InterventionOption]:
    """
    Return intervention options relevant to the domain and current bottlenecks.

    v0.1 uses explicit mappings, not ML.
    """
    options = DOMAIN_REMEDY_LIBRARY.get(domain, [])
    if not dominant_bottlenecks:
        return options

    ranked: list[InterventionOption] = []
    for option in options:
        if any(
            bottleneck in option.target_bottlenecks
            for bottleneck in dominant_bottlenecks
        ):
            ranked.append(option)

    return ranked if ranked else options

def get_remedy_library(domain: str | None = None) -> dict[str, list[InterventionOption]]:
    """
    Return the whole remedy library or one domain-specific slice.
    """
    if domain is None:
        return DOMAIN_REMEDY_LIBRARY

    return {domain: DOMAIN_REMEDY_LIBRARY.get(domain, [])}
