from emo.inference.behavioral_modes import infer_behavioral_mode


def test_infer_behavioral_mode_contradictory_action():
    result = infer_behavioral_mode(
        {
            "warning_to_policy_lag_days": 2,
            "implementation_persistence_30d": 0.8,
            "declared_vs_funded_gap": 0.6,
        }
    )

    assert result == "contradictory_action"


def test_infer_behavioral_mode_delayed_coordination():
    result = infer_behavioral_mode(
        {
            "warning_to_policy_lag_days": 10,
            "implementation_persistence_30d": 0.8,
            "declared_vs_funded_gap": 0.1,
        }
    )

    assert result == "delayed_coordination"


def test_infer_behavioral_mode_fragmentation_relapse():
    result = infer_behavioral_mode(
        {
            "warning_to_policy_lag_days": 3,
            "implementation_persistence_30d": 0.4,
            "declared_vs_funded_gap": 0.1,
        }
    )

    assert result == "fragmentation_relapse"


def test_infer_behavioral_mode_selective_stabilization():
    result = infer_behavioral_mode(
        {
            "warning_to_policy_lag_days": 2,
            "implementation_persistence_30d": 0.8,
            "declared_vs_funded_gap": 0.1,
        }
    )

    assert result == "selective_stabilization"
