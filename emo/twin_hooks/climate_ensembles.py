from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional

import xarray as xr


@dataclass
class EnsembleSummary:
    """
    Summary of a climate-model ensemble run.
    """

    name: str
    n_members: int
    variables: list[str]
    metadata: Dict[str, str]


def load_ensemble_dataset(path: str | Path) -> xr.Dataset:
    """
    Load a NetCDF ensemble dataset from disk.

    This is a convenience helper for using CMIP/ECMWF/NOAA ensembles
    as inputs to the UIA geometry and focusing computations. :contentReference[oaicite:32]{index=32}
    """
    ds = xr.open_dataset(path)
    return ds


def summarise_ensemble(ds: xr.Dataset) -> EnsembleSummary:
    n_members = int(ds.dims.get("member", 1))
    variables = list(ds.data_vars)
    return EnsembleSummary(
        name=ds.attrs.get("title", "ensemble"),
        n_members=n_members,
        variables=variables,
        metadata={},
    )
