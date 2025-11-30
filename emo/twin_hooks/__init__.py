# emo/twin_hooks/__init__.py
from .destine import (
    DestineClient,
    DestineConfig,
    DestineCollectionSummary,
    DestineItemSummary,
    summarise_variable_statistics,
    build_emo_destine_overlay,
)
from .climate_ensembles import (
    ClimateEnsembleMember,
    ensemble_from_dataframe,
    prepare_ensemble_for_information_geometry,
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
