from emo.models.domain_profile import DomainProfile


DISASTER_DOMAIN_PROFILE = DomainProfile(
    domain="disaster",
    diagnostic_types=[
        "flood_warning",
        "storm_warning",
        "heat_alert",
        "wildfire_alert",
    ],
    policy_types=[
        "emergency_order",
        "preparedness_directive",
        "evacuation_order",
    ],
    budget_types=[
        "emergency_funding",
        "preparedness_funding",
        "recovery_funding",
    ],
    delivery_types=[
        "equipment_deployment",
        "staff_mobilization",
        "shelter_activation",
        "aid_delivery",
    ],
    validation_metrics=[
        "affected_population_reduced",
        "response_time_improved",
        "coverage_rate",
    ],
    weighting_scheme={
        "lag": 0.3,
        "conversion": 0.2,
        "persistence": 0.2,
        "alignment": 0.15,
        "contradiction": 0.15,
    },
    lag_targets={
        "warning_to_policy_lag_days": 2.0,
        "warning_to_delivery_lag_days": 3.0,
    },
    coverage_rules=[
        "priority_to_high_risk_zones",
        "minimum_national_coverage",
    ],
    contradiction_rules=[
        "declared_but_unfunded_response",
