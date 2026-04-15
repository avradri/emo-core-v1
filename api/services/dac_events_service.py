from api.schemas.dac_events import DACEventRecord, DACEventsResponse
from api.services.dac_demo_flow_service import get_romania_disaster_demo_flow


def get_dac_events(
    domain: str | None = None,
    jurisdiction: str | None = None,
) -> DACEventsResponse:
    flow = get_romania_disaster_demo_flow()

    diagnostic = flow["diagnostic"]
    policy = flow["policy"]

    events = [
        DACEventRecord(
            id=diagnostic.id,
            kind="diagnostic",
            domain=diagnostic.domain,
            jurisdiction=diagnostic.geo_scope or "UNKNOWN",
            timestamp=diagnostic.issued_at,
        ),
        DACEventRecord(
            id=policy.id,
            kind="policy",
            domain=diagnostic.domain,
            jurisdiction=policy.jurisdiction,
            timestamp=policy.announced_at,
        ),
    ]

    if domain is not None:
        events = [event for event in events if event.domain == domain]

    if jurisdiction is not None:
        events = [event for event in events if event.jurisdiction == jurisdiction]

    return DACEventsResponse(events=events)
