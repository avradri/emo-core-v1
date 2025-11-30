from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

import httpx

from emo.config import get_settings


@dataclass
class EarlyWarningCoverage:
    """
    Minimal coverage summary for EW4All-style indicators.

    coverage:
        Fraction of population covered by multi-hazard early warning
        systems in a given region.
    """

    region: str
    coverage: float
    metadata: Dict[str, str]


class EarlyWarningClient:
    """
    Thin client for UNDRR/WMO early-warning coverage data.

    In v1.0 this is a placeholder that could be wired either to the
    Global Status of MHEWS reports or the new Global Observatory for
    Early Warning Systems Investments. :contentReference[oaicite:34]{index=34}
    """

    def __init__(self, base_url: Optional[str] = None) -> None:
        settings = get_settings()
        self.base_url = base_url or settings.undrr_base

    async def fetch_demo_coverage(self) -> list[EarlyWarningCoverage]:
        """
        Return a tiny synthetic coverage distribution for demo purposes.
        """
        return [
            EarlyWarningCoverage(
                region="Global",
                coverage=0.6,
                metadata={"source": "synthetic_demo"},
            )
        ]
