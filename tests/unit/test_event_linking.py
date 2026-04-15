from emo.harmonize.event_linking import policy_matches_diagnostic
from emo.models.diagnostic_event import DiagnosticEvent
from emo.models.policy_instrument import PolicyInstrument


def test_policy_matches_diagnostic_true():
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
        announced_at="2026-01-02T00:00:00",
        diagnostic_link="diag-1",
    )

    assert policy_matches_diagnostic(diagnostic, policy) is True


def test_policy_matches_diagnostic_false_when_missing_link():
    diagnostic = DiagnosticEvent(
        id="diag-2",
        domain="pandemic",
        hazard_type="outbreak",
        source="demo",
        issued_at="2026-02-01T00:00:00",
    )

    policy = PolicyInstrument(
        id="policy-2",
        instrument_type="public_health_order",
        jurisdiction="RO",
        announced_at="2026-02-02T00:00:00",
    )

    assert policy_matches_diagnostic(diagnostic, policy) is False
