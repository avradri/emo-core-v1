from __future__ import annotations

from typing import Any


def build_dac_snapshot(
    domain: str,
    jurisdiction: str,
    metrics: dict[str, Any],
    mode: str,
) -> dict[str, Any]:
    return {
        "domain": domain,
        "jurisdiction": jurisdiction,
        "metrics": metrics,
        "mode": mode,
    }
