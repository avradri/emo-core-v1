from __future__ import annotations

from emo.models.delivery_trace import DeliveryTrace
from emo.models.diagnostic_event import DiagnosticEvent
from emo.models.policy_instrument import PolicyInstrument

BULGARIA_DISASTER_DIAGNOSTIC = DiagnosticEvent(
    id="diag-bg-001",
    domain="disaster",
    hazard_type="flood",
    source="demo",
    issued_at="2026-01-01T00:00:00",
    geo_scope="BG",
    diagnostic_class="flood_warning",
    validation_status="validated",
)

BULGARIA_DISASTER_POLICY = PolicyInstrument(
    id="policy-bg-001",
    instrument_type="emergency_order",
    jurisdiction="BG",
    announced_at="2026-01-06T00:00:00",
    diagnostic_link="diag-bg-001",
)

BULGARIA_DISASTER_DELIVERY = DeliveryTrace(
    id="delivery-bg-001",
    delivery_type="equipment_deployment",
    jurisdiction="BG",
    started_at="2026-01-08T00:00:00",
    diagnostic_link="diag-bg-001",
    instrument_link="policy-bg-001",
)
