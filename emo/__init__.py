"""
Top-level package for EMO-Core.

This module exposes a stable public API for the core EMO metric
functions so that other packages (API, dashboards, labs) can simply do:

    from emo import compute_organismality_index, compute_smf, ...

Without having to know the internal file layout.

The intent is that EMO-Core behaves like a proper, versioned library
that a lab or funder tech contact can depend on.
"""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

from .organismality import compute_organismality_index
from .synergy import build_synergy_dataset, compute_synergy_o_information
from .gwi import compute_gwi_for_topic
from .smf import compute_smf
from .info_time import compute_information_time_from_skill
from .reciprocity import compute_reciprocity_flux

try:
    # When installed as a package, this will be managed by pyproject.toml
    __version__ = version("emo-core")
except PackageNotFoundError:  # pragma: no cover - development / editable installs
    # Fallback for local development without an installed distribution
    __version__ = "0.1.0"

__all__ = [
    "__version__",
    "compute_organismality_index",
    "build_synergy_dataset",
    "compute_synergy_o_information",
    "compute_gwi_for_topic",
    "compute_smf",
    "compute_information_time_from_skill",
    "compute_reciprocity_flux",
]
