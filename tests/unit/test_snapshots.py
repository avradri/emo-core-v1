from emo.reporting.snapshots import build_dac_snapshot


def test_build_dac_snapshot():
    result = build_dac_snapshot(
        domain="disaster",
        jurisdiction="RO",
        metrics={
            "warning_to_policy_lag_days": 3,
            "alert_to_policy_conversion_rate": 0.4,
        },
        mode="delayed_coordination",
    )

    assert result["domain"] == "disaster"
    assert result["jurisdiction"] == "RO"
    assert result["metrics"]["warning_to_policy_lag_days"] == 3
    assert result["mode"] == "delayed_coordination"
