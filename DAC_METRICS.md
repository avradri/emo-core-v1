# DAC Metrics

DAC metrics are organized as metric families rather than a single raw scalar.

## 1. Lag metrics

These measure how long it takes for validated diagnostics to become action.

Examples:

- warning_to_policy_lag_days
- warning_to_budget_lag_days
- warning_to_delivery_lag_days
- model_to_action_lag_days

## 2. Conversion metrics

These measure whether warnings become action at all.

Examples:

- alert_to_policy_conversion_rate
- alert_to_budget_conversion_rate
- alert_to_delivery_conversion_rate
- diagnostic_coverage_to_actuation_ratio

## 3. Persistence metrics

These measure whether implementation lasts.

Examples:

- implementation_persistence_30d
- implementation_persistence_90d
- budget_execution_ratio
- delivery_continuity_after_attention_spike

## 4. Alignment metrics

These measure whether action matches goals and models.

Examples:

- forecast_to_budget_alignment
- model_informed_spending_ratio
- target_investment_consistency
- goal_delivery_match_score

## 5. Contradiction metrics

These measure whether systems cancel themselves out.

Examples:

- actuation_contradiction_score
- declared_vs_funded_gap
- funded_vs_delivered_gap
- policy_signal_conflict_index

## Composite score rule

A domain-level DAC summary may later be computed, but only as a transparent composite built from declared metric families and declared weights.
