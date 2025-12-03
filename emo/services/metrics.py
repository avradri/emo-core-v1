# emo/services/metrics.py
from __future__ import annotations

from dataclasses import asdict, dataclass, is_dataclass
from typing import Any, Dict, List, Optional

import pandas as pd

from emo.organismality import compute_organismality_index
from emo.smf import compute_smf
from emo.uia_engine import UIACoefficients, UIASnapshot, compute_a_uia


def _result_to_dict(result: Any) -> Any:
    """
    Best-effort conversion of metric results into JSON-friendly structures.

    This function handles dataclasses, lists, dictionaries, and simple types,
    and is intended to be used by the service layer before returning data
    through the FastAPI routes.

    It does *not* attempt to be fully general; it just supports the result
    types used in the current EMO metrics modules (organismality, UIA, SMF,
    etc.).
    """
    if is_dataclass(result):
        return asdict(result)

    if isinstance(result, dict):
        return {k: _result_to_dict(v) for k, v in result.items()}

    if isinstance(result, (list, tuple)):
        return [_result_to_dict(v) for v in result]

    # Fallback: assume it is already JSON-serializable (int, float, str, etc.)
    return result


# ---------------------------------------------------------------------------
# UIA summary result type
# ---------------------------------------------------------------------------


@dataclass
class UIASummary:
    """
    Lightweight summary container for UIA time-series.

    This is a simplified, JSON-friendly view of the more detailed
    `UIASnapshot` objects produced by `emo.uia_engine.compute_a_uia`.
    """

    interface_id: str
    A_uia_bar: float
    a_uia: List[float]
    timestamps: List[str]
    metadata: Dict[str, Any]

    @classmethod
    def from_snapshot(cls, snapshot: UIASnapshot) -> "UIASummary":
        """
        Build a UIASummary from a UIASnapshot.

        Parameters
        ----------
        snapshot:
            A `UIASnapshot` instance returned by `compute_a_uia`.
        """
        # For now we expose only a subset of the snapshot fields, in a
        # JSON- and Pydantic-friendly format.
        return cls(
            interface_id=snapshot.interface_id,
            A_uia_bar=float(snapshot.A_uia_bar),
            a_uia=[float(x) for x in snapshot.a_uia],
            timestamps=[str(ts) for ts in snapshot.timestamps],
            metadata=dict(snapshot.metadata or {}),
        )


# ---------------------------------------------------------------------------
# Metric engine
# ---------------------------------------------------------------------------


class MetricEngine:
    """
    High-level service layer for EMO metrics.

    This class groups together the main metrics that are currently used
    in EMO Core and exposes them via stable, JSON-friendly methods that
    the FastAPI routes can call.

    The aim is to isolate the rest of the codebase from changes in the
    underlying algorithm implementations: we can refactor `emo.organismality`,
    `emo.smf`, `emo.uia_engine`, etc. without breaking the public API, as
    long as `MetricEngine`'s interface remains stable.
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
            treaties=treaties_df,
            conflicts=conflicts_df,
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

        Best-effort wrapper around `emo.synergy`. We perform a local import
        so that EMO-Core remains importable even if the synergy tools are
        absent or under active development.

        If the module or expected functions are missing, this will raise a
        RuntimeError *when called*, but will not break `import emo` or
        `import emo.services.metrics`.
        """
        try:
            from emo import synergy as synergy_mod  # type: ignore[attr-defined]
        except ImportError as exc:  # pragma: no cover - defensive
            raise RuntimeError(
                "Synergy tools are not available (emo.synergy could not be imported)."
            ) from exc

        if not hasattr(synergy_mod, "compute_synergy_for_dataframe"):
            raise RuntimeError(
                "Synergy module does not expose the expected "
                "`compute_synergy_for_dataframe` function."
            )

        result = synergy_mod.compute_synergy_for_dataframe(df, *args, **kwargs)
        return _result_to_dict(result)

    def reciprocity_flux(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Compute reciprocity flux metrics.

        This is a thin wrapper around `emo.reciprocity`. To keep the core
        service layer import-safe, we *lazily* import `emo.reciprocity` here.

        If the module or expected function is missing, we raise a RuntimeError
        when this method is called, but we do not break `import emo` or
        `import emo.services.metrics`.

        Notes
        -----
        The concrete reciprocity implementation in `emo.reciprocity` is still
        evolving. We therefore avoid pinning to any particular function name
        at import time and instead check for it at call time. This keeps the
        service layer import-safe. If a concrete `compute_reciprocity_flux`
        function is not available, a clear RuntimeError is raised.
        """
        try:
            from emo import reciprocity as rec_mod  # type: ignore[attr-defined]
        except ImportError as exc:  # pragma: no cover - defensive
            raise RuntimeError(
                "Reciprocity tools are not available (emo.reciprocity could not be "
                "imported)."
            ) from exc

        # Preferred modern API: compute_reciprocity_fluxes (plural)
        if rec_mod is not None and hasattr(rec_mod, "compute_reciprocity_fluxes"):
            result = rec_mod.compute_reciprocity_fluxes(*args, **kwargs)
            return _result_to_dict(result)

        # Backwards-compatibility shim for older code paths that used
        # a singular `compute_reciprocity_flux` function.
        if rec_mod is not None and hasattr(rec_mod, "compute_reciprocity_flux"):
            result = rec_mod.compute_reciprocity_flux(*args, **kwargs)
            return _result_to_dict(result)

        raise RuntimeError(
            "Reciprocity module does not expose an expected "
            "`compute_reciprocity_fluxes` or `compute_reciprocity_flux` function."
        )

    # ------------------------------------------------------------------
    # Sentience-mindfield (SMF) metrics
    # ------------------------------------------------------------------

    def smf_from_dataframe(
        self,
        df: pd.DataFrame,
        *args: Any,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Compute Sentience MindField (SMF) metrics from a dataframe.

        This is a direct wrapper around `emo.smf.compute_smf`, with results
        converted into JSON-friendly structures.
        """
        result = compute_smf(df, *args, **kwargs)
        return _result_to_dict(result)

    # ------------------------------------------------------------------
    # UIA metrics
    # ------------------------------------------------------------------

    def uia_from_dataframe(
        self,
        df: pd.DataFrame,
        interface_id: str,
        *args: Any,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Compute UIA metrics from a dataframe.

        This is a direct wrapper around `emo.uia_engine.compute_a_uia`, which
        returns a `UIASnapshot`. We convert that snapshot to a dictionary via
        `UIASummary`, yielding a JSON-friendly summary suitable for API
        responses.
        """
        snapshot = compute_a_uia(
            df=df,
            interface_id=interface_id,
            coeffs=self._uia_coeffs,
            *args,
            **kwargs,
        )
        summary = UIASummary.from_snapshot(snapshot)
        return _result_to_dict(summary)

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
        metadata: Optional[Dict[str, Any]] = None,
    ) -> UIASummary:
        """
        Construct a UIA summary directly from series inputs.

        This helper is used by tests and provides a slightly higher-level API
        for wrapping `compute_a_uia`. It expects time-indexed series for the
        main UIA inputs and returns a `UIASummary` instance.
        """
        df = pd.DataFrame(
            {
                "A": A_series,
                "C": C_series,
                "S": S_series,
                "I": I_series,
            },
            index=index,
        )

        snapshot = compute_a_uia(
            df=df,
            interface_id=interface_id,
            coeffs=self._uia_coeffs,
            B=B_scalar,
            M_E=M_E,
            metadata=metadata or {},
        )
        return UIASummary.from_snapshot(snapshot)
