from __future__ import annotations

from dataclasses import asdict, dataclass, is_dataclass
from typing import Any

import pandas as pd

from emo.organismality import compute_organismality_index
from emo.smf import compute_smf
from emo.uia_engine import UIACoefficients, UIASnapshot, compute_a_uia


def _result_to_dict(result: Any) -> Any:
    """
    Best-effort conversion of metric results into JSON-friendly structures.

    This helper keeps the service layer and API endpoints decoupled from the
    concrete return types of the scientific core (dataclasses, pandas objects,
    etc.).
    """
    if is_dataclass(result) and not isinstance(result, type):
        return asdict(result)

    if isinstance(result, pd.DataFrame):
        return result.to_dict(orient="records")

    if isinstance(result, pd.Series):
        return result.to_dict()

    if isinstance(result, dict):
        return {k: _result_to_dict(v) for k, v in result.items()}

    if isinstance(result, (list, tuple)):
        return [_result_to_dict(v) for v in result]

    return result


@dataclass
class UIASummary:
    """
    JSON-serialisable summary of a UIA aggregation.

    This is a thin, API-facing wrapper around :class:`emo.uia_engine.UIASnapshot`.
    We keep the structure deliberately small and stable so that FastAPI can expose
    it directly.
    """

    interface_id: str
    A_uia_bar: float
    a_uia: list[float]
    timestamps: list[str]
    metadata: dict[str, Any]

    @classmethod
    def from_snapshot(
        cls,
        snapshot: UIASnapshot,
        interface_id: str,
        metadata: dict[str, Any] | None = None,
    ) -> UIASummary:
        """
        Build a :class:`UIASummary` from a :class:`UIASnapshot`.

        Parameters
        ----------
        snapshot:
            Result returned by :func:`emo.uia_engine.compute_a_uia`.
        interface_id:
            Identifier for the interface Σ (e.g. "global_human_earth").
        metadata:
            Optional extra metadata to attach to the summary.
        """
        index = snapshot.a_uia_series.index
        a_values = [float(v) for v in snapshot.a_uia_series.to_numpy()]
        timestamps = [str(ts) for ts in index]

        return cls(
            interface_id=interface_id,
            A_uia_bar=float(snapshot.A_uia_bar),
            a_uia=a_values,
            timestamps=timestamps,
            metadata=metadata or {},
        )


class MetricEngine:
    """
    High-level service layer for EMO metrics.

    This class groups together the main metrics that are currently used in
    EMO Core and exposes them via stable, JSON-friendly methods that the
    FastAPI routes can call.
    """

    def __init__(self, uia_coeffs: UIACoefficients | None = None) -> None:
        self._uia_coeffs = uia_coeffs or UIACoefficients()

    def organismality_from_frames(
        self,
        treaties_df: pd.DataFrame,
        conflicts_df: pd.DataFrame,
    ) -> dict[str, Any]:
        """
        Compute the Organismality Index (OI) from treaty and conflict data.
        """
        result = compute_organismality_index(
            treaties=treaties_df,
            conflicts=conflicts_df,
        )
        return _result_to_dict(result)

    def synergy_from_dataframe(
        self,
        df: pd.DataFrame,
        *args: Any,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Compute synergy / O-information metrics for a multivariate dataset.
        """
        try:
            from emo import synergy as synergy_mod  # type: ignore[attr-defined]
        except ImportError as exc:
            raise RuntimeError(
                "Synergy tools are not available (emo.synergy could not be imported)."
            ) from exc

        if hasattr(synergy_mod, "compute_gaussian_synergy"):
            result = synergy_mod.compute_gaussian_synergy(df, *args, **kwargs)
            return _result_to_dict(result)

        raise RuntimeError(
            "Synergy module does not expose the expected "
            "`compute_gaussian_synergy` function."
        )

    def reciprocity_flux(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Compute reciprocity flux metrics.
        """
        try:
            from emo import reciprocity as rec_mod  # type: ignore[attr-defined]
        except ImportError as exc:
            raise RuntimeError(
                "Reciprocity tools are not available (emo.reciprocity could not be imported)."
            ) from exc

        if hasattr(rec_mod, "compute_reciprocity_fluxes"):
            result = rec_mod.compute_reciprocity_fluxes(*args, **kwargs)
            return _result_to_dict(result)

        if hasattr(rec_mod, "compute_reciprocity_flux"):
            result = rec_mod.compute_reciprocity_flux(*args, **kwargs)
            return _result_to_dict(result)

        raise RuntimeError(
            "Reciprocity module does not expose an expected "
            "`compute_reciprocity_fluxes` or `compute_reciprocity_flux` function."
        )

    def smf_from_dataframe(
        self,
        df: pd.DataFrame,
        *args: Any,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Compute Self-Model Fidelity (SMF) metrics from a dataframe.
        """
        result = compute_smf(df, *args, **kwargs)
        return _result_to_dict(result)

    def uia_from_series(
        self,
        interface_id: str,
        R_scalar: float,
        B_scalar: float,
        C_series: pd.Series,
        S_series: pd.Series,
        I_series: pd.Series,
        M_E: float,
        metadata: dict[str, Any] | None = None,
    ) -> UIASummary:
        """
        Compute UIA metrics from scalar R, B and time series C, S, I.
        """
        snapshot = compute_a_uia(
            R_scalar=R_scalar,
            B_scalar=B_scalar,
            C_series=C_series,
            S_series=S_series,
            I_series=I_series,
            M_E_scalar=M_E,
            coeffs=self._uia_coeffs,
        )
        return UIASummary.from_snapshot(
            snapshot=snapshot,
            interface_id=interface_id,
            metadata=metadata,
        )

    def uia_from_dataframe(
        self,
        df: pd.DataFrame,
        interface_id: str,
        *,
        R_scalar: float,
        B_scalar: float,
        M_E: float,
        metadata: dict[str, Any] | None = None,
    ) -> UIASummary:
        """
        Convenience wrapper for UIA aggregation when C, S and I live in a dataframe.
        """
        try:
            C_series = df["C"]
            S_series = df["S"]
            I_series = df["I"]
        except KeyError as exc:
            raise KeyError("df must contain 'C', 'S' and 'I' columns") from exc

        return self.uia_from_series(
            interface_id=interface_id,
            R_scalar=R_scalar,
            B_scalar=B_scalar,
            C_series=C_series,
            S_series=S_series,
            I_series=I_series,
            M_E=M_E,
            metadata=metadata,
        )

    def uia_summary(
        self,
        interface_id: str,
        index: pd.DatetimeIndex,
        A_series: pd.Series,
        B_scalar: float,
        C_series: pd.Series,
        S_series: pd.Series,
        I_series: pd.Series,
        M_E: float,
        metadata: dict[str, Any] | None = None,
    ) -> UIASummary:
        """
        Legacy convenience wrapper for UIA aggregation.
        """
        C_series = C_series.copy()
        C_series.index = index

        S_series = S_series.copy()
        S_series.index = index

        I_series = I_series.copy()
        I_series.index = index

        return self.uia_from_series(
            interface_id=interface_id,
            R_scalar=1.0,
            B_scalar=B_scalar,
            C_series=C_series,
            S_series=S_series,
            I_series=I_series,
            M_E=M_E,
            metadata=metadata,
)
