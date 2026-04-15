from typing import Optional


def declared_vs_funded_gap(
    declared_commitments: int,
    funded_commitments: int,
) -> Optional[float]:
    if declared_commitments <= 0:
        return None

    gap = declared_commitments - funded_commitments
    return gap / declared_commitments
