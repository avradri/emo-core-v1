from __future__ import annotations


def missing_required_fields(
    required_fields: list[str],
    present_fields: list[str],
) -> list[str]:
    present = set(present_fields)
    return [field for field in required_fields if field not in present]
