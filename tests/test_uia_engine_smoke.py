from __future__ import annotations

import pandas as pd

from emo.uia_engine.aggregate import UIASnapshot, compute_a_uia


def test_compute_a_uia_smoke() -> None:
    """
    Smoke test for the UIA aggregation.

    Uses synthetic but dimensionally consistent series for C, S, I.
    """
    index = pd.date_range("2025-01-01", periods=5, freq="D")
    C = pd.Series([0.2, 0.3, 0.4, 0.5, 0.6], index=index)
    S = pd.Series([1.0, 0.95, 0.9, 0.85, 0.8], index=index)
    I = pd.Series([0.1, 0.2, 0.35, 0.5, 0.7], index=index)

    snapshot = compute_a_uia(
        R_scalar=1.0,
        B_scalar=1.0,
        C_series=C,
        S_series=S,
        I_series=I,
        M_E_scalar=0.5,
    )

    assert isinstance(snapshot, UIASnapshot)
    assert len(snapshot.a_uia_series) == len(index)
    assert isinstance(snapshot.A_uia_bar, float)
