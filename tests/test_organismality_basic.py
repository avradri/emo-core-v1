from __future__ import annotations

import pandas as pd

from emo.organismality import compute_organismality_index


def test_compute_organismality_index_basic() -> None:
    """
    Simple numerical sanity check for the Organismality Index (OI).

    We build tiny toy dataframes with obvious structure and assert that:
    - the result is in [0, 1]
    - regions appear in the regional index
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

    result = compute_organismality_index(treaties, conflicts)

    assert 0.0 <= result.global_oi <= 1.0
    assert set(result.regional_oi.keys()) == {"A", "B", "C"}
