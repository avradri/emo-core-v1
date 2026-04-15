from datetime import datetime
from typing import Optional

from emo.models.diagnostic_event import DiagnosticEvent
from emo.models.policy_instrument import PolicyInstrument
from emo.models.delivery_trace import DeliveryTrace


def _parse_date(value: Optional[str]) -> Optional[datetime]:
    if value is None:
        return None
    return datetime.fromisoformat(value)


def warning_to_policy_lag_days(
    diagnostic: DiagnosticEvent,
    policy: PolicyInstrument,
) -> Optional[int]:
    diagnostic_time = _parse_date(diagnostic.issued_at)
    policy_time = _parse_date(policy.announced_at)

    if diagnostic_time is None or policy_time is None:
        return None

    return (policy_time - diagnostic_time).days


def warning_to_delivery_lag_days(
    diagnostic: DiagnosticEvent,
    delivery: DeliveryTrace,
) -> Optional[int]:
    diagnostic_time = _parse_date(diagnostic.issued_at)
    delivery_time = _parse_date(delivery.started_at)

    if diagnostic_time is None or delivery_time is None:
        return None

    return (delivery_time - diagnostic_time).days
