from typing import Optional


def implementation_persistence_30d(
    started_implementations: int,
    active_after_30d: int,
) -> Optional[float]:
    if started_implementations <= 0:
        return None

    return active_after_30d / started_implementations


def implementation_persistence_90d(
    started_implementations: int,
    active_after_90d: int,
) -> Optional[float]:
    if started_implementations <= 0:
        return None

    return active_after_90d / started_implementations
