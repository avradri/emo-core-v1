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

    Parameters
    ----------
    parameters:
        Dictionary of scalar run parameters (e.g. forcings, scenario IDs,
        configuration flags). Keys should be strings; values will be cast
        to float where appropriate.
    score:
        Scalar figure of merit for the run (e.g. skill score, loss, error).
    metadata:
        Optional free-form metadata (e.g. collection ID, member ID, notes).
    """

    parameters: Dict[str, float]
    score: float
    metadata: Dict[str, str]


def ensemble_from_dataframe(
    df: pd.DataFrame,
    parameter_cols: Sequence[str],
    score_col: str,
    metadata_cols: Optional[Sequence[str]] = None,
) -> List[ClimateEnsembleMember]:
    """
    Build an ensemble from a tabular collection of runs.

    Each row in `df` corresponds to a single ensemble member.

    Parameters
    ----------
    df:
        Dataframe with one row per ensemble member.
    parameter_cols:
        Columns containing scalar parameters to be fed into information
        geometry / UIA curvature tools.
    score_col:
        Column containing a scalar score per run (e.g. skill).
    metadata_cols:
        Optional columns to copy directly into the metadata dict.

    Returns
    -------
    members:
        List of ClimateEnsembleMember instances.
    """
    if metadata_cols is None:
        metadata_cols = []

    members: List[ClimateEnsembleMember] = []

    for _, row in df.iterrows():
        parameters = {name: float(row[name]) for name in parameter_cols}
        score = float(row[score_col])
        metadata = {name: str(row[name]) for name in metadata_cols}
        members.append(
            ClimateEnsembleMember(
                parameters=parameters,
                score=score,
                metadata=metadata,
            )
        )

    return members


def prepare_ensemble_for_information_geometry(
    members: Iterable[ClimateEnsembleMember],
    parameter_order: Optional[Sequence[str]] = None,
) -> Tuple[np.ndarray, np.ndarray, List[str]]:
    """
    Convert an ensemble into arrays suitable for information-geometry tools.

    Parameters
    ----------
    members:
        Iterable of ClimateEnsembleMember.
    parameter_order:
        Optional explicit order of parameter names. If omitted, the union
        of all parameter keys is used in sorted order.

    Returns
    -------
    theta:
        Array of shape (n_members, n_parameters) with parameter values.
        Missing parameters are filled with NaN.
    scores:
        Array of shape (n_members,) with scalar scores.
    parameter_names:
        List of parameter names corresponding to the columns of `theta`.
    """
    members_list = list(members)
    if not members_list:
        raise ValueError(
            "prepare_ensemble_for_information_geometry() "
            "received an empty ensemble."
        )

    if parameter_order is None:
        keys: List[str] = []
        for m in members_list:
            keys.extend(list(m.parameters.keys()))
        parameter_order = sorted(set(keys))

    n_members = len(members_list)
    n_params = len(parameter_order)

    theta = np.full((n_members, n_params), np.nan, dtype=float)
    scores = np.zeros(n_members, dtype=float)

    for i, m in enumerate(members_list):
        for j, name in enumerate(parameter_order):
            if name in m.parameters:
                theta[i, j] = float(m.parameters[name])
        scores[i] = float(m.score)

    return theta, scores, list(parameter_order)


__all__ = [
    "ClimateEnsembleMember",
    "ensemble_from_dataframe",
    "prepare_ensemble_for_information_geometry",
]
