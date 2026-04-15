from emo.metrics.dac.lag import (
    warning_to_delivery_lag_days,
    warning_to_policy_lag_days,
)
from emo.models.delivery_trace import DeliveryTrace
from emo.models.diagnostic_event import DiagnosticEvent
from emo.models.policy_instrument import PolicyInstrument


def test_warning_to_policy_lag_days():
    diagnostic = DiagnosticEvent(
        id="diag-1",
        domain="disaster",
        hazard_type="flood",
        source="demo",
        issued_at="2026-01-01T00:00:00",
    )

    policy = PolicyInstrument(
        id="policy-1",
        instrument_type="emergency_order",
        jurisdiction="RO",
        announced_at="2026-01-04T00:00:00",
    )

    assert warning_to_policy_lag_days(diagnostic, policy) == 3


def test_warning_to_delivery_lag_days():
    diagnostic = DiagnosticEvent(
        id="diag-2",
        domain="disaster",
        hazard_type="storm",
        source="demo",
        issued_at="2026-02-10T00:00:00",
    )

    delivery = DeliveryTrace(
        id="delivery-1",
        delivery_type="equipment_deployment",
        jurisdiction="RO",
        started_at="2026-02-15T00:00:00",
    )

    assert warning_to_delivery_lag_days(diagnostic, delivery) == 5
