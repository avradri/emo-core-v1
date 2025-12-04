# emo/twin_hooks/__init__.py
from __future__ import annotations

from .climate_ensembles import (
    ClimateEnsembleMember,
    ensemble_from_dataframe,
    prepare_ensemble_for_information_geometry,
)
from .destine import (  # type: ignore[attr-defined]
    DestineClient,
    DestineConfig,
    DestineCollectionSummary,
    DestineItemSummary,
    summarise_variable_statistics,
    build_emo_destine_overlay,
)

__all__ = [
    "DestineClient",
    "DestineConfig",
    "DestineCollectionSummary",
    "DestineItemSummary",
    "summarise_variable_statistics",
    "build_emo_destine_overlay",
    "ClimateEnsembleMember",
    "ensemble_from_dataframe",
    "prepare_ensemble_for_information_geometry",
]
