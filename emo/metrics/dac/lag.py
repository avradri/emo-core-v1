from typing import Optional

from emo.harmonize.time_alignment import parse_iso_datetime
from emo.models.delivery_trace import DeliveryTrace
from emo.models.diagnostic_event import DiagnosticEvent
from emo.models.policy_instrument import PolicyInstrument


def warning_to_policy_lag_days(
    diagnostic: DiagnosticEvent,
    policy: PolicyInstrument,
) -> Optional[int]:
    diagnostic_time = parse_iso_datetime(diagnostic.issued_at)
    policy_time = parse_iso_datetime(policy.announced_at)

    if diagnostic_time is None or policy_time is None:
        return None

    return (policy_time - diagnostic_time).days


def warning_to_delivery_lag_days(
    diagnostic: DiagnosticEvent,
    delivery: DeliveryTrace,
) -> Optional[int]:
    diagnostic_time = parse_iso_datetime(diagnostic.issued_at)
    delivery_time = parse_iso_datetime(delivery.started_at)

    if diagnostic_time is None or delivery_time is None:
        return None

    return (delivery_time - diagnostic_time).days
