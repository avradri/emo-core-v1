from typing import Dict


def infer_behavioral_mode(metrics: Dict[str, float]) -> str:
    warning_to_policy_lag = metrics.get("warning_to_policy_lag_days", 0)
    persistence_30d = metrics.get("implementation_persistence_30d", 1.0)
    contradiction = metrics.get("declared_vs_funded_gap", 0.0)

    if contradiction > 0.5:
        return "contradictory_action"

    if warning_to_policy_lag > 7:
        return "delayed_coordination"

    if persistence_30d < 0.5:
        return "fragmentation_relapse"

    return "selective_stabilization"
