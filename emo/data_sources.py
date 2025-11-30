from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional

import httpx

from .config import get_settings


class InterfaceClass(str, Enum):
    EARTH_SYSTEM = "earth_system"
    MEDIA = "media"
    KNOWLEDGE_GRAPH = "knowledge_graph"
    EARLY_WARNING = "early_warning"
    ECONOMIC = "economic"
    GOVERNANCE = "governance"
    HEALTH = "health"
    AI_MODEL = "ai_model"


@dataclass
class Interface:
    """
    Minimal representation of an interface Σ_i in the Interface Registry.

    In v1.0 we keep this in-memory; a later version can persist it to Postgres
    following the schema in the EMO architecture document. :contentReference[oaicite:23]{index=23}
    """

    id: str
    name: str
    klass: InterfaceClass
    provider: str
    description: str
    base_url: Optional[str] = None
    uia_roles: Optional[Dict[str, bool]] = None


class InterfaceRegistry:
    """
    In-memory interface registry used by the API.

    This is deliberately minimal and can be swapped for a DB-backed
    implementation without breaking the API layer.
    """

    def __init__(self) -> None:
        self._interfaces: Dict[str, Interface] = {}
        self._bootstrap_defaults()

    def _bootstrap_defaults(self) -> None:
        settings = get_settings()

        self.register(
            Interface(
                id="gdelt-doc",
                name="GDELT Doc 2.0",
                klass=InterfaceClass.MEDIA,
                provider="GDELT Project",
                description="Global news and event graph (Doc 2.0 API).",
                base_url=settings.gdelt_doc_api_base,
                uia_roles={"C": True, "S": True, "I": True},
            )
        )
        self.register(
            Interface(
                id="openalex",
                name="OpenAlex",
                klass=InterfaceClass.KNOWLEDGE_GRAPH,
                provider="OurResearch",
                description="Open index of scholarly works, sources, and concepts.",
                base_url=settings.openalex_base,
                uia_roles={"I": True},
            )
        )
        self.register(
            Interface(
                id="destine",
                name="Destination Earth",
                klass=InterfaceClass.EARTH_SYSTEM,
                provider="ECMWF / ESA / EUMETSAT",
                description="High-resolution digital twin of the Earth system.",
                base_url=settings.destine_base,
                uia_roles={"R": True, "B": True},
            )
        )

    def register(self, interface: Interface) -> None:
        self._interfaces[interface.id] = interface

    def list(self) -> Dict[str, Interface]:
        return dict(self._interfaces)

    def get(self, interface_id: str) -> Optional[Interface]:
        return self._interfaces.get(interface_id)


# --- Tiny helper clients ----------------------------------------------------


async def fetch_json(url: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Lightweight async JSON fetcher.

    Used by ingestion hooks and demo endpoints; in a real deployment
    this should be wrapped with robust retry, rate-limit, and telemetry.
    """
    async with httpx.AsyncClient(timeout=20) as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        return resp.json()
