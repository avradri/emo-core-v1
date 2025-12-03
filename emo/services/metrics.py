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

    - dataclasses      -> dict
    - pandas Series    -> dict
    - pandas DataFrame -> list[dict]
    - other objects    -> returned as-is
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

        if not hasattr(synergy_mod, "build_synergy_dataset") or not hasattr(
            synergy_mod, "compute_synergy_o_information"
        ):
            raise RuntimeError(
                "Synergy module does not expose the expected "
                "`build_synergy_dataset` and `compute_synergy_o_information` "
                "functions."
            )

        dataset = synergy_mod.build_synergy_dataset(df, *args, **kwargs)
        result = synergy_mod.compute_synergy_o_information(dataset)
        return _result_to_dict(result)

    def gwi_for_topic(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        """
        Compute Global Workspace Ignition (GWI) metrics for a selected topic.

        This uses a lazy import of `emo.gwi` so that the absence of a
        specific helper function does not break module import.
        """
        try:
            from emo import gwi as gwi_mod  # type: ignore[attr-defined]
        except ImportError as exc:  # pragma: no cover - defensive
            raise RuntimeError(
                "GWI tools are not available (emo.gwi could not be imported)."
            ) from exc

        if not hasattr(gwi_mod, "compute_gwi_for_topic"):
            raise RuntimeError(
                "GWI module does not expose the expected `compute_gwi_for_topic` "
                "function."
            )

        result = gwi_mod.compute_gwi_for_topic(*args, **kwargs)
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
        Compute information-time τ_I from a forecast-skill time series.

        We *do not* depend on an external compute_information_time_from_skill
        symbol here. Instead, we implement a simple, robust fallback that:

        - Accepts a skill time series (list-like or pandas Series),
        - Normalizes it to [0, 1] using min/max,
        - Interprets (1 - skill_norm) as the "remaining information gap",
        - Integrates that gap over time to produce a τ_I-like timescale.

        This keeps the service layer import-safe even if emo.info_time is
        still evolving. If you later add a dedicated emo.info_time module
        with a richer implementation, you can wire it in here.
        """
        # Extract skill series from args/kwargs in a tolerant way
        if "skill_series" in kwargs:
            skill = kwargs.pop("skill_series")
        elif args:
            skill = args[0]
            args = args[1:]
        else:
            raise ValueError(
                "information_time_from_skill requires a `skill_series` "
                "as the first positional argument or `skill_series=` keyword."
            )

        dt = float(kwargs.pop("dt", 1.0))

        series = pd.Series(skill)
        if len(series) == 0:
            return {
                "tau_I": 0.0,
                "dt": dt,
                "n_points": 0,
                "skill_min": None,
                "skill_max": None,
            }

        s_min = float(series.min())
        s_max = float(series.max())

        if s_max > s_min:
            normalized = (series - s_min) / (s_max - s_min)
        else:
            # Flat skill: treat as zero progress
            normalized = pd.Series(0.0, index=series.index)

        # Simple "information-time" proxy: integral of the remaining gap
        gap = (1.0 - normalized).clip(lower=0.0)
        tau_I = float(gap.sum() * dt)

        return {
            "tau_I": tau_I,
            "dt": dt,
            "n_points": int(len(series)),
            "skill_min": s_min,
            "skill_max": s_max,
        }

    def reciprocity_flux(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        """
        Compute reciprocity fluxes R, J_B, B for a given dataset.

        We avoid any fragile import from `emo.reciprocity` here to keep the
        service layer import-safe. If a concrete `compute_reciprocity_flux`
        implementation is available in `emo.reciprocity`, we use it; otherwise
        we fall back to a simple summary of the provided data.

        This means:

        - In fully wired deployments, you can implement your detailed
          reciprocity flux logic in emo/reciprocity.py and expose a
          `compute_reciprocity_flux` function.
        - In minimal / test deployments, the fallback still returns a
          JSON-friendly summary dict.
        """
        try:
            from emo import reciprocity as rec_mod  # type: ignore[attr-defined]
        except ImportError:
            rec_mod = None

        if rec_mod is not None and hasattr(rec_mod, "compute_reciprocity_flux"):
            result = rec_mod.compute_reciprocity_flux(*args, **kwargs)
            return _result_to_dict(result)

        # Fallback: treat the first arg or "data" kwarg as a DataFrame-like.
        data = None
        if "data" in kwargs:
            data = kwargs["data"]
        elif args:
            data = args[0]

        if data is None:
            # Nothing sensible to summarize; return an empty placeholder.
            return {
                "R": None,
                "J_B": None,
                "B": None,
                "detail": "no data provided; reciprocity_flux fallback",
            }

        df = pd.DataFrame(data)

        return {
            "R": 0.0,
            "J_B": 0.0,
            "B": 0.0,
            "n_rows": int(df.shape[0]),
            "n_cols": int(df.shape[1]),
            "columns": list(df.columns),
            "detail": "fallback reciprocity_flux summary (no emo.reciprocity implementation found)",
        }

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
