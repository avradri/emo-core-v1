from __future__ import annotations


def alert_to_policy_conversion_rate(
    total_alerts: int,
    alerts_with_policy: int,
) -> float | None:
    if total_alerts <= 0:
        return None

    return alerts_with_policy / total_alerts


def alert_to_delivery_conversion_rate(
    total_alerts: int,
    alerts_with_delivery: int,
) -> float | None:
    if total_alerts <= 0:
        return None

    return alerts_with_delivery / total_alerts
