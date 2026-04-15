from collections.abc import Mapping


def infer_behavioral_mode(metrics: Mapping[str, float | int | None]) -> str:
    warning_to_policy_lag_raw = metrics.get("warning_to_policy_lag_days", 0)
    persistence_30d_raw = metrics.get("implementation_persistence_30d", 1.0)
    contradiction_raw = metrics.get("declared_vs_funded_gap", 0.0)

    warning_to_policy_lag = float(warning_to_policy_lag_raw or 0)
    persistence_30d = float(persistence_30d_raw or 0.0)
    contradiction = float(contradiction_raw or 0.0)

    if contradiction > 0.5:
        return "contradictory_action"

    if warning_to_policy_lag > 7:
        return "delayed_coordination"

    if persistence_30d < 0.5:
        return "fragmentation_relapse"

    return "selective_stabilization"
