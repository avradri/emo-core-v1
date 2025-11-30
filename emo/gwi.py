from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

import numpy as np
import pandas as pd


@dataclass
class GWIResult:
    """
    Result container for Global Workspace Ignition (GWI).

    gwi_series:
        Time-indexed ignition intensity in [0, 1].
    events:
        List of timestamps where ignition crosses a configurable
        percentile threshold.
    """

    gwi_series: pd.Series
    events: List[pd.Timestamp]
    metadata: Dict[str, str]


def compute_gwi(
    streams: pd.DataFrame,
    ignition_percentile: float = 0.95,
) -> GWIResult:
    """
    Compute a simple GWI score from multiple attention streams.

    Parameters
    ----------
    streams:
        DataFrame indexed by time, columns are attention proxies
        (e.g., news volume, pageviews, search trends).
    ignition_percentile:
        Percentile above which we mark an "ignition event".

    Returns
    -------
    GWIResult
    """
    if streams.empty:
        empty = pd.Series(dtype=float)
        return GWIResult(empty, [], {"definition": "empty"})

    df = streams.sort_index().fillna(0.0)
    z = (df - df.mean()) / (df.std(ddof=0) + 1e-9)
    composite = z.mean(axis=1)

    # Squash into [0,1] via logistic
    gwi_values = 1.0 / (1.0 + np.exp(-composite.to_numpy()))
    gwi_series = pd.Series(gwi_values, index=df.index, name="gwi")

    threshold = float(np.quantile(gwi_series.to_numpy(), ignition_percentile))
    events = gwi_series[gwi_series >= threshold].index.to_list()

    return GWIResult(
        gwi_series=gwi_series,
        events=events,
        metadata={
            "definition": "logistic_zscore_v1.0",
            "ignition_percentile": f"{ignition_percentile:.2f}",
        },
    )
