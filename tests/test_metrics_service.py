# tests/test_metrics_service.py
from __future__ import annotations

import pandas as pd

from emo.services.metrics import MetricEngine, UIASummary


def test_metric_engine_organismality_from_frames() -> None:
    """
    Basic integration test for the MetricEngine.organismality_from_frames wrapper.

    Uses tiny synthetic treaty/conflict data and checks that the returned
    dictionary has the expected shape.
    """
    treaties = pd.DataFrame(
        {
            "region": ["A", "B", "C"],
            "treaty_count": [10, 5, 0],
        }
    )
    conflicts = pd.DataFrame(
        {
            "region": ["A", "B", "C"],
            "conflict_deaths": [0, 10, 20],
        }
    )

    engine = MetricEngine()
    result = engine.organismality_from_frames(
        treaties_df=treaties,
        conflicts_df=conflicts,
    )

    # Should be a JSON-friendly dictionary mirroring OrganismalityResult.
    assert isinstance(result, dict)
    assert set(result.keys()) == {"global_oi", "regional_oi", "metadata"}
    assert 0.0 <= float(result["global_oi"]) <= 1.0
    assert set(result["regional_oi"].keys()) == {"A", "B", "C"}
    assert isinstance(result["metadata"], dict)


def test_metric_engine_uia_from_series() -> None:
    """
    Smoke test for MetricEngine.uia_from_series.

    This exercises the UIA engine through the service layer and ensures
    we get a UIASummary instance with the right dimensions.
    """
    index = pd.date_range("2025-01-01", periods=5, freq="D")
    C = pd.Series([0.2, 0.3, 0.4, 0.5, 0.6], index=index)
    S = pd.Series([1.0, 0.95, 0.9, 0.85, 0.8], index=index)
    I = pd.Series([0.1, 0.2, 0.35, 0.5, 0.7], index=index)

    engine = MetricEngine()
    summary = engine.uia_from_series(
        interface_id="test_interface",
        R_scalar=1.0,
        B_scalar=1.0,
        C_series=C,
        S_series=S,
        I_series=I,
        M_E=0.5,
        metadata={"lab": "test"},
    )

    assert isinstance(summary, UIASummary)
    assert summary.interface_id == "test_interface"
    assert isinstance(summary.A_uia_bar, float)
    assert len(summary.a_uia) == len(index)
    assert len(summary.timestamps) == len(index)
    assert isinstance(summary.metadata, dict)
    assert summary.metadata.get("lab") == "test"
