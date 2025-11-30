from __future__ import annotations

from typing import Dict

from fastapi import APIRouter

from emo.data_sources import InterfaceRegistry

router = APIRouter()
_registry = InterfaceRegistry()


@router.get("/")
async def list_interfaces() -> Dict[str, Dict]:
    """
    Return a list of interfaces Σ_i known to the in-memory registry.
    """
    data = {}
    for iid, iface in _registry.list().items():
        data[iid] = {
            "id": iface.id,
            "name": iface.name,
            "class": iface.klass.value,
            "provider": iface.provider,
            "description": iface.description,
            "base_url": iface.base_url,
            "uia_roles": iface.uia_roles,
        }
    return data
