from typing import Optional


def normalize_jurisdiction(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None

    return value.strip().upper()
