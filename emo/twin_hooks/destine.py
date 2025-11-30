from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

import httpx

from emo.config import get_settings


@dataclass
class DestineScenarioSummary:
    """
    Minimal DestinE scenario summary used by EMO.

    This is a deliberately small subset — enough to attach cognitive
    overlays (OI, SMF, ignition, UIA bands) to DestinE runs. :contentReference[oaicite:30]{index=30}
    """

    scenario_id: str
    name: str
    description: str
    start_time: str
    end_time: str
    metadata: Dict[str, Any]


class DestineClient:
    """
    Thin HTTP client for Destination Earth (DestinE) metadata.

    NOTE: DestinE endpoints and authentication are still evolving; this
    client is intentionally generic and must be wired to the actual
    operational APIs of ECMWF/ESA/EUMETSAT. :contentReference[oaicite:31]{index=31}
    """

    def __init__(self, base_url: Optional[str] = None) -> None:
        settings = get_settings()
        self.base_url = base_url or settings.destine_base

    async def list_scenarios(self) -> Dict[str, DestineScenarioSummary]:
        """
        Fetch a list of available DestinE scenarios.

        Currently returns a synthetic dictionary until wired to real APIs.
        """
        # Placeholder: replace with real HTTP calls when endpoints are public.
        return {
            "demo-scenario-1": DestineScenarioSummary(
                scenario_id="demo-scenario-1",
                name="Synthetic heatwave demo",
                description="Placeholder DestinE scenario for EMO demo.",
                start_time="2030-06-01T00:00:00Z",
                end_time="2030-08-31T00:00:00Z",
                metadata={},
            )
        }

    async def fetch_scenario_fields(
        self,
        scenario_id: str,
        variables: list[str],
    ) -> Dict[str, Any]:
        """
        Fetch selected hazard/exposure/impact fields for a scenario.

        The actual implementation will depend on DestinE API conventions.
        """
        # Placeholder; we keep the shape so code compiles.
        return {"scenario_id": scenario_id, "variables": variables, "data": None}
