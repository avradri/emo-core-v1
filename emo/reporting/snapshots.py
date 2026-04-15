from typing import Any, Dict


def build_dac_snapshot(
    domain: str,
    jurisdiction: str,
    metrics: Dict[str, Any],
    mode: str,
) -> Dict[str, Any]:
    return {
        "domain": domain,
        "jurisdiction": jurisdiction,
        "metrics": metrics,
        "mode": mode,
    }
