from emo.models.diagnostic_event import DiagnosticEvent
from emo.models.policy_instrument import PolicyInstrument


def policy_matches_diagnostic(
    diagnostic: DiagnosticEvent,
    policy: PolicyInstrument,
) -> bool:
    if policy.diagnostic_link is None:
        return False

    return policy.diagnostic_link == diagnostic.id
