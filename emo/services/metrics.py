# emo/services/metrics.py
from __future__ import annotations

from dataclasses import asdict, dataclass, is_dataclass
from typing import Any, Dict, List, Optional

import pandas as pd

from emo import (
    build_synergy_dataset,
    compute_gwi_for_topic,
    compute_information_time_from_skill,
    compute_organismality_index,
    compute_reciprocity_flux,
    compute_smf,
    compute_synergy_o_information,
)
from emo.uia_engine import UIACoefficients, UIASnapshot, compute_a_uia


def _result_to_dict(result: Any) -> Any:
    """
    Best-effort conversion of metric results into JSON-friendly structures.

    - dataclasses  -> dict
    - pandas Series -> dict
    - pandas DataFrame -> list[dict]
    - other objects -> returned as-is
    """
    if is_dataclass(result):
        return asdict(result)

    if isinstance(result, pd.DataFrame):
        return result.to_dict(orient="records")

    if isinstance(result, pd.Series):
        return result.to_dict()

    return result


@dataclass
class UIASummary:
    """
    JSON-friendly summary for a UIA aggregation window.

    This sits one layer above UIASnapshot, and is what we expect to return
    from API endpoints and dashboards.

    Parameters
    ----------
    interface_id:
        Identifier for the interface Σ (e.g. "global_human_earth",
        "eu_energy_system", "destine_v1").
    window_start:
        Start of the time window as ISO8601 string, or None if unknown.
    window_end:
        End of the time window as ISO8601 string, or None if unknown.
    A_uia_bar:
        Coarse-grained Ȧ_UIA over the window.
    a_uia:
        Values of the local UIA density a_UIA(t).
    timestamps:
        ISO8601 timestamps corresponding to a_uia entries.
    metadata:
        Optional free-form metadata (e.g. scenario name, notes).
    """

    interface_id: str
    window_start: Optional[str]
    window_end: Optional[str]
    A_uia_bar: float
    a_uia: List[float]
    timestamps: List[str]
    metadata: Dict[str, Any]


class MetricEngine:
    """
    High-level service layer for EMO metrics.

    This class provides a clean, lab-facing API around the core metric
    functions implemented in the emo package, plus UIA aggregation.

    It is intentionally thin: it delegates all scientific logic to the
    underlying modules, and focuses on producing JSON-friendly outputs.
    """

    def __init__(self, uia_coeffs: Optional[UIACoefficients] = None) -> None:
        self._uia_coeffs = uia_coeffs or UIACoefficients()

    # ------------------------------------------------------------------
    # Species-mind metrics
    # ------------------------------------------------------------------

    def organismality_from_frames(
        self,
        treaties_df: pd.DataFrame,
        conflicts_df: pd.DataFrame,
    ) -> Dict[str, Any]:
        """
        Compute the Organismality Index (OI) from treaty and conflict data.

        This simply wraps `compute_organismality_index` and converts the
        result into a dictionary that FastAPI can serialize.
        """
        result = compute_organismality_index(
            treaties_df=treaties_df,
            conflicts_df=conflicts_df,
        )
        return _result_to_dict(result)

    def synergy_from_dataframe(
        self,
        df: pd.DataFrame,
        *args: Any,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Compute synergy / O-information metrics for a multivariate dataset.

        This is a convenience wrapper around `build_synergy_dataset` and
        `compute_synergy_o_information`. The exact arguments depend on the
        underlying implementation; we expose *args/**kwargs so that labs can
        call this directly from Python and tailor it to their needs.
        """
        dataset = build_synergy_dataset(df, *args, **kwargs)
        result = compute_synergy_o_information(dataset)
        return _result_to_dict(result)

    def gwi_for_topic(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        """
        Compute Global Workspace Ignition (GWI) metrics for a selected topic.

        Thin wrapper around `compute_gwi_for_topic`.
        """
        result = compute_gwi_for_topic(*args, **kwargs)
        return _result_to_dict(result)

    def smf(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        """
        Compute Self-Model Fidelity (SMF) metrics.

        Thin wrapper around `compute_smf`.
        """
        result = compute_smf(*args, **kwargs)
        return _result_to_dict(result)

    def information_time_from_skill(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        """
        Compute information-time τ_I from forecast skill improvements.

        Thin wrapper around `compute_information_time_from_skill`.
        """
        result = compute_information_time_from_skill(*args, **kwargs)
        return _result_to_dict(result)

    def reciprocity_flux(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        """
        Compute reciprocity fluxes R, J_B, B for a given dataset.

        Thin wrapper around `compute_reciprocity_flux`.
        """
        result = compute_reciprocity_flux(*args, **kwargs)
        return _result_to_dict(result)

    # ------------------------------------------------------------------
    # UIA aggregation
    # ------------------------------------------------------------------

    def uia_from_series(
        self,
        interface_id: str,
        R_scalar: float,
        B_scalar: float,
        C_series: pd.Series,
        S_series: pd.Series,
        I_series: pd.Series,
        M_E: float | pd.Series = 0.0,
        coeffs: Optional[UIACoefficients] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> UIASummary:
        """
        Compute a_UIA(t) and a UIASummary for a given interface and window.

        Parameters
        ----------
        interface_id:
            Identifier for the interface Σ.
        R_scalar:
            Scalar informational curvature 𝓡[g_I] over the window.
        B_scalar:
            Scalar focusing bracket ℬ over the window.
        C_series, S_series, I_series:
            Time series for coherence C(t), entropy-like S(t), and
            information-like I(t), all sharing the same index.
        M_E:
            Semantic efficiency M_E; scalar or Series aligned with C_series.
        coeffs:
            Optional custom UIACoefficients. If omitted, defaults from
            `self._uia_coeffs` are used.
        metadata:
            Optional metadata dictionary.

        Returns
        -------
        UIASummary
            JSON-friendly summary of the UIA aggregation.
        """
        coeffs = coeffs or self._uia_coeffs

        snapshot: UIASnapshot = compute_a_uia(
            R_scalar=R_scalar,
            B_scalar=B_scalar,
            C_series=C_series,
            S_series=S_series,
            I_series=I_series,
            M_E_scalar=M_E,
            coeffs=coeffs,
        )

        index = snapshot.a_uia_series.index
        if len(index) > 0:
            window_start = str(index[0])
            window_end = str(index[-1])
        else:
            window_start = None
            window_end = None

        a_uia_values = [float(v) for v in snapshot.a_uia_series.to_numpy()]
        timestamps = [str(ts) for ts in index]

        return UIASummary(
            interface_id=interface_id,
            window_start=window_start,
            window_end=window_end,
            A_uia_bar=float(snapshot.A_uia_bar),
            a_uia=a_uia_values,
            timestamps=timestamps,
            metadata=metadata or {},
        )
