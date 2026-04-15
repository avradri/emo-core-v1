from emo.models.domain_profile import DomainProfile


PANDEMIC_DOMAIN_PROFILE = DomainProfile(
    domain="pandemic",
    diagnostic_types=[
        "outbreak_alert",
        "surveillance_signal",
        "who_emergency_notice",
        "hospital_capacity_warning",
    ],
    policy_types=[
        "public_health_order",
        "travel_advisory",
        "testing_directive",
        "vaccination_policy",
    ],
    budget_types=[
        "emergency_health_funding",
        "surge_capacity_funding",
        "stockpile_funding",
    ],
    delivery_types=[
        "testing_deployment",
        "vaccine_distribution",
        "staff_mobilization",
        "stockpile_release",
    ],
    validation_metrics=[
        "case_growth_reduced",
        "hospital_pressure_reduced",
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
        "warning_to_policy_lag_days": 1.0,
        "warning_to_delivery_lag_days": 2.0,
    },
    coverage_rules=[
        "priority_to_high_transmission_zones",
        "minimum_population_coverage",
    ],
    contradiction_rules=[
        "declared_but_unfunded_response",
        "funded_but_undelivered_response",
    ],
)
