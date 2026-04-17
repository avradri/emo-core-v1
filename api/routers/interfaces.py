from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from emo.data_sources import InterfaceRegistry

router = APIRouter()
_registry = InterfaceRegistry()


@router.get("/")
async def list_interfaces() -> dict[str, dict[str, Any]]:
    """Return a list of interfaces Σ_i known to the in-memory registry."""
    data: dict[str, dict[str, Any]] = {}

    for interface_id, interface in _registry.list().items():
        data[interface_id] = {
            "id": interface.id,
            "name": interface.name,
            "class": interface.klass.value,
            "provider": interface.provider,
            "description": interface.description,
            "base_url": interface.base_url,
            "uia_roles": interface.uia_roles,
        }

    return data
