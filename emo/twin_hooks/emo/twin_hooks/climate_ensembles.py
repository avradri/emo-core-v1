# emo/twin_hooks/climate_ensembles.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd


@dataclass
class ClimateEnsembleMember:
    """
    Minimal representation of a single climate ensemble member.

    Examples
    --------
    - One instance per DestinE Climate DT simulation (different models / forcings).
    - One instance per CMIP-like run (different parameterisations or scenarios).
    """

    run_id: str
    parameters: Dict[str, float]
    score: float
    meta: Dict[str, str]


def ensemble_from_dataframe(
    df: pd.DataFrame,
    run_col: str,
    parameter_cols: Sequence[str],
    score_col: str,
    meta_cols: Optional[Sequence[str]] = None,
) -> List[ClimateEnsembleMember]:
    """
    Convert a DataFrame with one row per ensemble run into ClimateEnsembleMember objects.

    Parameters
    ----------
    df:
        DataFrame where each row is a single ensemble run.
    run_col:
        Column with unique run identifiers.
    parameter_cols:
        Columns representing model parameters or knobs (e.g. ECS, aerosol scaling).
    score_col:
        Column with a scalar score per run (e.g. forecast skill, log-likelihood).
    meta_cols:
        Optional columns to carry through as string metadata.
    """
    if meta_cols is None:
        meta_cols = []

    members: List[ClimateEnsembleMember] = []
    for _, row in df.iterrows():
        params = {col: float(row[col]) for col in parameter_cols}
        meta = {col: str(row[col]) for col in meta_cols}
        members.append(
            ClimateEnsembleMember(
                run_id=str(row[run_col]),
                parameters=params,
                score=float(row[score_col]),
                meta=meta,
            )
        )
    return members


def prepare_ensemble_for_information_geometry(
    members: Iterable[ClimateEnsembleMember],
    parameter_order: Optional[Sequence[str]] = None,
) -> Tuple[np.ndarray, np.ndarray, List[str]]:
    """
    Prepare an ensemble for information-geometry-based UIA calculations.

    This function does *not* compute 𝓡[g_I] itself; instead it returns:

    - theta:   array of shape (n_runs, n_params) with parameter vectors θ_i
    - scores:  array of shape (n_runs,) with associated scalar scores s(θ_i)
    - param_names: list of parameter names, defining column order in theta

    The UIA engine can then fit statistical manifolds, estimate Fisher metrics,
    and derive informational curvature 𝓡[g_I] on top of this representation. 
    """
    members = list(members)
    if not members:
        raise ValueError("No ensemble members provided")

    # Infer parameter ordering if not explicitly given
    if parameter_order is None:
        # use parameters from the first member
        parameter_order = list(members[0].parameters.keys())

    n_runs = len(members)
    n_params = len(parameter_order)
    theta = np.zeros((n_runs, n_params), dtype=float)
    scores = np.zeros(n_runs, dtype=float)

    for i, m in enumerate(members):
        for j, name in enumerate(parameter_order):
            theta[i, j] = float(m.parameters.get(name, np.nan))
        scores[i] = float(m.score)

    return theta, scores, list(parameter_order)


__all__ = [
    "ClimateEnsembleMember",
    "ensemble_from_dataframe",
    "prepare_ensemble_for_information_geometry",
]
