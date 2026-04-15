from api.schemas.dac_events import DACEventRecord, DACEventsResponse


def get_dac_events() -> DACEventsResponse:
    return DACEventsResponse(
        events=[
            DACEventRecord(
                id="diag-1",
                kind="diagnostic",
                domain="disaster",
                jurisdiction="RO",
                timestamp="2026-01-01T00:00:00",
            ),
            DACEventRecord(
                id="policy-1",
                kind="policy",
                domain="disaster",
                jurisdiction="RO",
                timestamp="2026-01-04T00:00:00",
            ),
        ]
    )
