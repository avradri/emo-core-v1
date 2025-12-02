# EMO-Core v1.0 — Technical Contact Overview

This document is for lab tech leads, digital-twin teams, and funder
due diligence engineers who need to understand what EMO-Core is, what
it does today, and how to integrate it.

---

## 1. What is EMO-Core?

EMO-Core is a Python library and API that implements the core metric
stack of the Emergent Mind Observatory (EMO):

- **Organismality Index (OI)** — cooperation vs. conflict.
- **Synergy / O-information (SΦ)** — integrative information processing.
- **Global Workspace Ignition (GWI)** — species-level "ignition" events.
- **Self-Model Fidelity (SMF)** — coupling between self-model outputs
  (forecasts, risk assessments) and actuation (budgets, regulations).
- **Information-Time (τ_I)** — effective learning speed.
- **Reciprocity fluxes (R, J_B, B)** — exosomatic buffering, environmental
  selection, and endosomatic adaptation.
- **UIA aggregation (a_UIA, Ȧ_UIA)** — a single scalar density combining
  curvature, focusing, coherence, entropy, information, and semantic
  efficiency for the human–Earth interface.

In EMO-Core v1.0 these are implemented as **pure Python metric engines**
with a thin service layer (`MetricEngine`) and a FastAPI service for
HTTP integration.

---

## 2. Repository structure (high level)

Relevant pieces for integration:

- `emo/` — core metric library (pure Python)
  - `organismality.py` — Organismality Index (OI)
  - `synergy.py` — synergy / O-information
  - `gwi.py` — global workspace ignition
  - `smf.py` — self-model fidelity
  - `info_time.py` — information-time τ_I
  - `reciprocity.py` — reciprocity fluxes R, J_B, B
  - `uia_engine/` — UIA aggregation (`compute_a_uia`, `UIASnapshot`)
  - `services/metrics.py` — `MetricEngine` + `UIASummary`

- `api/` — FastAPI service
  - `main.py` — FastAPI app (`uvicorn api.main:app`)
  - `routers/metrics.py` — `/metrics/*` endpoints (OI, etc.)
  - `routers/uia.py` — `/uia/*` endpoints (UIA summaries)

- `orchestration/` — Airflow/Prefect flows for ingestion (optional, can be ignored if you only need metrics).

- `docs/` — architecture docs and this file.

---

## 3. How do I run it?

### 3.1 Install

From a checkout of the repo:

```bash
pip install -e ".[dev]"
