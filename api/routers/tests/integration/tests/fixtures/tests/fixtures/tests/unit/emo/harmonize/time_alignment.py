from datetime import datetime
from typing import Optional


def parse_iso_datetime(value: Optional[str]) -> Optional[datetime]:
    if value is None:
        return None

    return datetime.fromisoformat(value)
