"""
Top-level package for EMO-Core.

This module exposes a stable public API for the core EMO metric
functions *when they are available*, but it is deliberately defensive:
missing optional modules (e.g. synergy tools under active development)
will not cause `import emo` to fail.

This makes EMO-Core safe to import in tests, API services, and lab
environments even if some metric submodules are still evolving.
"""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

__all__: list[str] = ["__version__"]

try:
    # When installed as a package, this will be managed by pyproject.toml
    __version__ = version("emo-core")
except PackageNotFoundError:  # pragma: no cover - development / editable installs
    # Fallback for local development without an installed distribution
    __version__ = "0.1.0"


def _export_from(module_name: str, names: list[str]) -> None:
    """
    Helper: try to import specific names from an internal submodule.

    If the submodule or the names are missing, we simply skip them
    instead of raising an ImportError. This keeps `import emo` robust.
    """
    global_vars = globals()
    module_path = f"{__name__}.{module_name}"

    try:
        module = __import__(module_path, fromlist=names)
    except Exception:
        return

    for name in names:
        if not hasattr(module, name):
            continue
        global_vars[name] = getattr(module, name)
        __all__.append(name)


# Core metric functions (expected to be present in a v1.0 checkout)
_export_from("organismality", ["compute_organismality_index"])
_export_from("gwi", ["compute_gwi_for_topic"])
_export_from("smf", ["compute_smf"])
_export_from("info_time", ["compute_information_time_from_skill"])
_export_from("reciprocity", ["compute_reciprocity_flux"])

# Synergy helpers are optional; if the module or names are missing we just skip.
_export_from("synergy", ["build_synergy_dataset", "compute_synergy_o_information"])
