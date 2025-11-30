from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict

import numpy as np


@dataclass
class ModelSnapshot:
    """
    Minimal snapshot of a model state for UIA purposes.
    """

    parameters: np.ndarray  # parameter vector θ
    metrics: Dict[str, float]  # e.g., skill, loss, rmse


class UIAModel(ABC):
    """
    Abstract base class for models that can be plugged into the
    UIA geometry and curvature computations.
    """

    @abstractmethod
    def sample_snapshots(self, n: int) -> list[ModelSnapshot]:
        """
        Return a list of model snapshots for curvature estimation.
        """


class DummyModel(UIAModel):
    """
    Tiny example model for testing the UIA geometry functions.
    """

    def __init__(self, dim: int = 2) -> None:
        self.dim = dim

    def sample_snapshots(self, n: int) -> list[ModelSnapshot]:
        xs = np.random.randn(n, self.dim)
        snapshots = []
        for i in range(n):
            theta = xs[i]
            snapshots.append(
                ModelSnapshot(
                    parameters=theta,
                    metrics={"skill": float(np.exp(-np.linalg.norm(theta) ** 2))},
                )
            )
        return snapshots
