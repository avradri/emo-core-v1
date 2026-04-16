from __future__ import annotations


def declared_vs_funded_gap(
    declared_commitments: int,
    funded_commitments: int,
) -> float | None:
    if declared_commitments <= 0:
        return None

    gap = declared_commitments - funded_commitments
    return gap / declared_commitments
