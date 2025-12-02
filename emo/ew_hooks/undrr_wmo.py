from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

import httpx

from emo.config import get_settings


@dataclass
class EarlyWarningCoverage:
    """
    Minimal coverage summary for EW4All-style indicators.

    Parameters
    ----------
    region:
        Human-readable region name (country, basin, or aggregate region).
    coverage:
        Fraction in [0, 1] of population or territory covered by
        multi-hazard early-warning systems in that region.
    metadata:
        Optional free-form metadata (e.g. source, year, notes).
    """

    region: str
    coverage: float
    metadata: Dict[str, str]


class EarlyWarningClient:
    """
    Thin async HTTP client for UNDRR / WMO early-warning coverage endpoints.

    The actual EW4All / Global Status of MHEWS APIs are still evolving.
    This helper assumes only a small JSON schema and is intended as a
    stable adapter that infra teams can replace or extend.

    By default, the base URL is taken from `EMO_UNDRR_BASE` via
    `emo.config.Settings.undrr_base`.
    """

    def __init__(self, base_url: Optional[str] = None, timeout: float = 10.0) -> None:
        settings = get_settings()
        self.base_url = base_url or settings.undrr_base
        self._timeout = timeout

    async def fetch_coverage(
        self,
        client: Optional[httpx.AsyncClient] = None,
        path: str = "/emo/coverage",
    ) -> List[EarlyWarningCoverage]:
        """
        Fetch a best-effort coverage distribution from a remote endpoint.

        Parameters
        ----------
        client:
            Optional existing httpx.AsyncClient to reuse. If omitted,
            a temporary client is created and closed for this call.
        path:
            Path component to append to `base_url`. Defaults to `/emo/coverage`.

        Returns
        -------
        coverages:
            List of EarlyWarningCoverage entries.
        """
        close_client = False
        if client is None:
            client = httpx.AsyncClient(timeout=self._timeout)
            close_client = True

        try:
            url = f"{self.base_url.rstrip('/')}{path}"
            resp = await client.get(url)
            resp.raise_for_status()
            payload = resp.json()
        finally:
            if close_client:
                await client.aclose()

        coverages: List[EarlyWarningCoverage] = []
        for item in payload:
            region = str(item.get("region", "Unknown"))
            coverage = float(item.get("coverage", 0.0))
            meta = {
                k: str(v)
                for k, v in item.items()
                if k not in {"region", "coverage"}
            }
            coverages.append(
                EarlyWarningCoverage(
                    region=region,
                    coverage=coverage,
                    metadata=meta,
                )
            )

        return coverages

    async def fetch_demo_coverage(self) -> List[EarlyWarningCoverage]:
        """
        Return a tiny synthetic coverage distribution for local demos.

        This avoids depending on remote availability when running EMO-Core
        in development mode or in unit tests.
        """
        return [
            EarlyWarningCoverage(
                region="Global",
                coverage=0.6,
                metadata={"source": "synthetic_demo"},
            )
        ]
