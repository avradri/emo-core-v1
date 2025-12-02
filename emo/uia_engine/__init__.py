"""
UIA engine subpackage for EMO-Core.

This package currently exposes a single high-level aggregation entry
point, compute_a_uia, and the associated dataclasses used to represent
UIA coefficients and snapshots.

The intent is that higher layers (API, dashboards, labs) can simply do:

    from emo.uia_engine import compute_a_uia, UIASnapshot

without worrying about the underlying module structure.
"""

from __future__ import annotations

from .aggregate import (
    UIACoefficients,
    UIASnapshot,
    UIATerms,
    compute_a_uia,
    default_uia_coefficients,
)

__all__ = [
    "UIACoefficients",
    "UIATerms",
    "UIASnapshot",
    "compute_a_uia",
    "default_uia_coefficients",
]
