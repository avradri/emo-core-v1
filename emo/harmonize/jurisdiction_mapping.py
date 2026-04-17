from __future__ import annotations


def normalize_jurisdiction(value: str | None) -> str | None:
    if value is None:
        return None

    return value.strip().upper()
