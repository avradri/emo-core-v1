cat > emo/uia_engine/__init__.py <<'PY'
"""
UIA engine subpackage for EMO-Core.
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
PY
