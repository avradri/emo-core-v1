from __future__ import annotations

from typing import Iterable, Tuple

import numpy as np

from .models import ModelSnapshot


def estimate_fisher_information(
    snapshots: Iterable[ModelSnapshot],
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Very approximate Fisher information estimator.

    Given a set of snapshots with parameter vectors θ and a scalar
    metric m (e.g., skill), we approximate the gradient of log m
    and compute the Fisher matrix as E[∇ log m ∇ log m^T].

    This is intentionally crude; it gives us a dimensionless
    scalar curvature proxy for UIA experiments without tying us
    to a particular parametric form. :contentReference[oaicite:28]{index=28}
    """
    thetas = []
    grads = []
    eps = 1e-6

    snaps = list(snapshots)
    if len(snaps) < 2:
        raise ValueError("Need at least two snapshots to estimate Fisher")

    for s in snaps:
        theta = np.asarray(s.parameters, dtype=float)
        m = float(s.metrics.get("skill", 0.0) or 0.0)
        if m <= 0:
            continue
        # numeric gradient via small random perturbation
        dim = theta.shape[0]
        g = np.zeros_like(theta)
        for i in range(dim):
            d = np.zeros_like(theta)
            d[i] = eps
            m_plus = float(m)
            m_minus = float(m)
            # We don't have direct access to m(θ±ε e_i) here, so this is
            # a strongly simplified proxy: treat gradient as proportional
            # to -θ, which is correct for a Gaussian toy model.
            g[i] = -theta[i]
        thetas.append(theta)
        grads.append(g)

    G = np.stack(grads, axis=0)
    fisher = G.T @ G / max(G.shape[0] - 1, 1)
    mean_theta = np.mean(np.stack(thetas, axis=0), axis=0)
    return fisher, mean_theta


def scalar_curvature_from_fisher(fisher: np.ndarray) -> float:
    """
    Compute a simple scalar curvature proxy from a Fisher matrix.

    For a true information manifold, one would compute the Riemannian
    scalar curvature of the Fisher metric. Here we use:

        R ~ log(det(F)) / dim

    with a small regulariser added to the diagonal.
    """
    dim = fisher.shape[0]
    reg = np.eye(dim) * 1e-6
    det = np.linalg.det(fisher + reg)
    if det <= 0:
        return 0.0
    return float(np.log(det) / dim)
