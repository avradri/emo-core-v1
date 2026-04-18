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
    "climate_mitigation": [
        InterventionOption(
            option_id="climate_budget_alignment",
            family="fiscal",
            name="Climate budget alignment rule",
            description=(
                "Tie medium-term public expenditure and budget screening to "
                "validated climate targets and carbon constraints."
            ),
            target_bottlenecks=["budget", "contradiction"],
            required_capacity="medium",
            time_to_effect="medium",
            evidence_level="moderate",
            rights_risk="low",
            coordination_cost="medium",
            domains=["climate_mitigation"],
        ),
        InterventionOption(
            option_id="climate_subsidy_phaseout",
            family="regulatory",
            name="Contradictory subsidy phaseout",
            description=(
                "Identify and phase out high-emissions subsidies that undermine "
                "declared mitigation targets."
            ),
            target_bottlenecks=["contradiction", "budget"],
            required_capacity="high",
            time_to_effect="medium",
            evidence_level="strong",
            rights_risk="medium",
            coordination_cost="high",
            domains=["climate_mitigation"],
        ),
        InterventionOption(
            option_id="climate_grid_permitting",
            family="infrastructure_capacity",
            name="Grid and permitting acceleration",
            description=(
                "Accelerate permitting, transmission expansion, and interconnection "
                "capacity for low-carbon deployment."
            ),
            target_bottlenecks=["deployment", "persistence"],
            required_capacity="high",
            time_to_effect="medium",
            evidence_level="strong",
            rights_risk="low",
            coordination_cost="high",
            domains=["climate_mitigation"],
        ),
        InterventionOption(
            option_id="climate_procurement_standard",
            family="procurement_logistics",
            name="Low-carbon public procurement standard",
            description=(
                "Use public procurement rules to shift demand toward low-carbon "
                "materials, energy, and infrastructure."
            ),
            target_bottlenecks=["translation", "deployment"],
            required_capacity="medium",
            time_to_effect="medium",
            evidence_level="moderate",
            rights_risk="low",
            coordination_cost="medium",
            domains=["climate_mitigation"],
        ),
        InterventionOption(
            option_id="climate_just_transition_support",
            family="social_protection_legitimacy",
            name="Just transition support package",
            description=(
                "Pair mitigation policy with income support, retraining, and local "
                "transition assistance to improve durability and legitimacy."
            ),
            target_bottlenecks=["persistence", "contradiction"],
            required_capacity="medium",
            time_to_effect="medium",
            evidence_level="moderate",
            rights_risk="low",
            coordination_cost="medium",
            domains=["climate_mitigation"],
        ),
        InterventionOption(
            option_id="climate_cross_border_coordination",
            family="treaty_cross_border_cooperation",
            name="Cross-border mitigation coordination",
            description=(
                "Coordinate standards, grids, industrial transition, and carbon "
                "accountability across jurisdictions."
            ),
            target_bottlenecks=["translation", "persistence"],
            required_capacity="high",
            time_to_effect="long",
            evidence_level="moderate",
            rights_risk="low",
            coordination_cost="high",
            domains=["climate_mitigation"],
        ),
    ],
"food_security": [
        InterventionOption(
            option_id="food_buffer_stock_protocol",
            family="procurement_logistics",
            name="Buffer stock release protocol",
            description=(
                "Predefine trigger rules for strategic food reserve release under "
                "validated supply and price stress conditions."
            ),
            target_bottlenecks=["deployment", "translation"],
            required_capacity="medium",
            time_to_effect="short",
            evidence_level="moderate",
            rights_risk="low",
            coordination_cost="medium",
            domains=["food_security"],
        ),
        InterventionOption(
            option_id="food_income_support_targeting",
            family="social_protection_legitimacy",
            name="Targeted food income support",
            description=(
                "Deliver temporary income support or food vouchers to vulnerable "
                "households during acute food-price shocks."
            ),
            target_bottlenecks=["persistence", "contradiction"],
            required_capacity="medium",
            time_to_effect="short",
            evidence_level="strong",
            rights_risk="low",
            coordination_cost="medium",
            domains=["food_security"],
        ),
        InterventionOption(
            option_id="food_import_coordination_cell",
            family="coordination_institutional",
            name="Import coordination cell",
            description=(
                "Coordinate customs, ports, wholesalers, and emergency sourcing to "
                "reduce friction during supply disruption."
            ),
            target_bottlenecks=["deployment", "translation"],
            required_capacity="high",
            time_to_effect="short",
            evidence_level="moderate",
            rights_risk="low",
            coordination_cost="high",
            domains=["food_security"],
        ),
        InterventionOption(
            option_id="food_school_meal_protection",
            family="social_protection_legitimacy",
            name="School meal continuity protection",
            description=(
                "Protect school feeding and child nutrition programs during fiscal "
                "or supply-chain stress."
            ),
            target_bottlenecks=["persistence", "budget"],
            required_capacity="medium",
            time_to_effect="short",
            evidence_level="strong",
            rights_risk="low",
            coordination_cost="medium",
            domains=["food_security"],
        ),
        InterventionOption(
            option_id="food_agri_input_stabilization",
            family="fiscal",
            name="Agricultural input stabilization",
            description=(
                "Stabilize access to seeds, fertilizer, irrigation inputs, and fuel "
                "for high-risk production regions."
            ),
            target_bottlenecks=["budget", "persistence"],
            required_capacity="high",
            time_to_effect="medium",
            evidence_level="moderate",
            rights_risk="low",
            coordination_cost="high",
            domains=["food_security"],
        ),
        InterventionOption(
            option_id="food_export_restriction_review",
            family="regulatory",
            name="Export restriction review rule",
            description=(
                "Review and constrain emergency export restrictions that intensify "
                "regional food insecurity and policy contradiction."
            ),
            target_bottlenecks=["contradiction", "translation"],
            required_capacity="medium",
            time_to_effect="medium",
            evidence_level="moderate",
            rights_risk="medium",
            coordination_cost="high",
            domains=["food_security"],
        ),
    ],
"migration_stress": [
        InterventionOption(
            option_id="migration_reception_scaling_protocol",
            family="infrastructure_capacity",
            name="Reception scaling protocol",
            description=(
                "Predefine surge capacity rules for reception, shelter, registration, "
                "and essential service access during rapid inflow events."
            ),
            target_bottlenecks=["deployment", "translation"],
            required_capacity="high",
            time_to_effect="short",
            evidence_level="moderate",
            rights_risk="low",
            coordination_cost="high",
            domains=["migration_stress"],
        ),
        InterventionOption(
            option_id="migration_local_fiscal_support",
            family="fiscal",
            name="Local fiscal support trigger",
            description=(
                "Trigger temporary fiscal transfers to high-pressure municipalities "
                "facing sudden service and housing strain."
            ),
            target_bottlenecks=["budget", "persistence"],
            required_capacity="medium",
            time_to_effect="short",
            evidence_level="moderate",
            rights_risk="low",
            coordination_cost="medium",
            domains=["migration_stress"],
        ),
        InterventionOption(
            option_id="migration_case_coordination_cell",
            family="coordination_institutional",
            name="Cross-agency case coordination cell",
            description=(
                "Coordinate border, asylum, welfare, housing, health, and education "
                "interfaces through a shared operational cell."
            ),
            target_bottlenecks=["translation", "contradiction"],
            required_capacity="high",
            time_to_effect="medium",
            evidence_level="moderate",
            rights_risk="low",
            coordination_cost="high",
            domains=["migration_stress"],
        ),
        InterventionOption(
            option_id="migration_legal_orientation_standard",
            family="communication_attention",
            name="Legal orientation and information standard",
            description=(
                "Provide standardized multilingual information on legal pathways, "
                "rights, obligations, and available services."
            ),
            target_bottlenecks=["translation", "deployment"],
            required_capacity="low",
            time_to_effect="short",
            evidence_level="strong",
            rights_risk="low",
            coordination_cost="medium",
            domains=["migration_stress"],
        ),
        InterventionOption(
            option_id="migration_host_community_support",
            family="social_protection_legitimacy",
            name="Host-community support package",
            description=(
                "Pair migrant support measures with visible support for host "
                "communities to reduce backlash and policy contradiction."
            ),
            target_bottlenecks=["persistence", "contradiction"],
            required_capacity="medium",
            time_to_effect="medium",
            evidence_level="moderate",
            rights_risk="low",
            coordination_cost="medium",
            domains=["migration_stress"],
        ),
        InterventionOption(
            option_id="migration_cross_border_referral_protocol",
            family="treaty_cross_border_cooperation",
            name="Cross-border referral protocol",
            description=(
                "Establish coordinated referral, data-sharing, and burden-management "
                "protocols across neighboring jurisdictions."
            ),
            target_bottlenecks=["translation", "persistence"],
            required_capacity="high",
            time_to_effect="medium",
            evidence_level="moderate",
            rights_risk="medium",
            coordination_cost="high",
            domains=["migration_stress"],
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
