from emo.models.delivery_trace import DeliveryTrace
from emo.models.diagnostic_event import DiagnosticEvent
from emo.models.policy_instrument import PolicyInstrument


ROMANIA_DISASTER_DIAGNOSTIC = DiagnosticEvent(
    id="diag-ro-001",
    domain="disaster",
    hazard_type="flood",
    source="demo",
    issued_at="2026-01-01T00:00:00",
    geo_scope="RO",
    diagnostic_class="flood_warning",
    validation_status="validated",
)

ROMANIA_DISASTER_POLICY = PolicyInstrument(
    id="policy-ro-001",
    instrument_type="emergency_order",
    jurisdiction="RO",
    announced_at="2026-01-04T00:00:00",
    diagnostic_link="diag-ro-001",
)

ROMANIA_DISASTER_DELIVERY = DeliveryTrace(
    id="delivery-ro-001",
    delivery_type="equipment_deployment",
    jurisdiction="RO",
    started_at="2026-01-06T00:00:00",
    diagnostic_link="diag-ro-001",
    instrument_link="policy-ro-001",
)
