from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass
class ClimateEnsembleMember:
    """
    Minimal representation of a single climate ensemble member.
    """

    parameters: dict[str, float]
    score: float
    metadata: dict[str, str]


def ensemble_from_dataframe(
    df: pd.DataFrame,
    parameter_cols: Sequence[str],
    score_col: str,
    metadata_cols: Sequence[str] | None = None,
) -> list[ClimateEnsembleMember]:
    """
    Build an ensemble from a tabular collection of runs.
    """
    if metadata_cols is None:
        metadata_cols = []

    members: list[ClimateEnsembleMember] = []

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
    parameter_order: Sequence[str] | None = None,
) -> tuple[np.ndarray, np.ndarray, list[str]]:
    """
    Convert an ensemble into arrays suitable for information-geometry tools.
    """
    members_list = list(members)
    if not members_list:
        raise ValueError(
            "prepare_ensemble_for_information_geometry() received an empty ensemble."
        )

    if parameter_order is None:
        keys: list[str] = []
        for member in members_list:
            keys.extend(list(member.parameters.keys()))
        parameter_order = sorted(set(keys))

    n_members = len(members_list)
    n_params = len(parameter_order)

    theta = np.full((n_members, n_params), np.nan, dtype=float)
    scores = np.zeros(n_members, dtype=float)

    for i, member in enumerate(members_list):
        for j, name in enumerate(parameter_order):
            if name in member.parameters:
                theta[i, j] = float(member.parameters[name])
        scores[i] = float(member.score)

    return theta, scores, list(parameter_order)


__all__ = [
    "ClimateEnsembleMember",
    "ensemble_from_dataframe",
    "prepare_ensemble_for_information_geometry",
                                  ]
