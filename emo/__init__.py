"""
EMO-Core v1.0

Core metric engine for the Emergent Mind Observatory (EMO), implementing
species-level cognition metrics and the UIA aggregation pipeline.
"""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("emo-core")
except PackageNotFoundError:
    __version__ = "0.1.0"

__all__ = ["__version__"]
