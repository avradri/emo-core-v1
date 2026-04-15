from emo.metrics.dac.conversion import (
    alert_to_delivery_conversion_rate,
    alert_to_policy_conversion_rate,
)


def test_alert_to_policy_conversion_rate():
    assert alert_to_policy_conversion_rate(10, 4) == 0.4


def test_alert_to_delivery_conversion_rate():
    assert alert_to_delivery_conversion_rate(8, 2) == 0.25


def test_conversion_rate_with_zero_alerts():
    assert alert_to_policy_conversion_rate(0, 0) is None
    assert alert_to_delivery_conversion_rate(0, 0) is None
