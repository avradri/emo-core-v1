from __future__ import annotations

from datetime import datetime


def parse_iso_datetime(value: str | None) -> datetime | None:
    if value is None:
        return None

    return datetime.fromisoformat(value)
