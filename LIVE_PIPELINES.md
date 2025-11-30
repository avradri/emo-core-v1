# EMO v1.0 Live Pipelines

_The Emergent Mind Observatory – live cognitive layer for the planet_

This document describes how EMO-Core v1.0 runs as a **continuous observatory**, not a one‑off script. It turns the architecture in `ARCHITECTURE.md` and the EMO/UIA papers into a concrete pipeline design.   

At a high level, EMO operates four cadence bands:

- **Daily** – attention & ignition (GWI), near‑real‑time climate/ risk news.
- **Weekly** – synergy Ω across media / science / conflict.
- **Monthly** – organismality (OI), self‑model fidelity (SMF), UIA aggregates.
- **Yearly** – information‑time τ_I and deep UIA recalibration.

All pipelines share the same structure:

```text
External sources  -->  Ingestion & Harmonisation  -->  Metric engines  -->  UIA engine  -->  API + Dashboard
(GDELT, OWID,     (emo.ingestion.* modules,      (emo.organismality,   (emo.uia_engine.   (FastAPI + Next.js)
Wikipedia,        data lake on disk or S3)        emo.smf, emo.gwi,…)    aggregate)        + partner hooks)
OpenAlex, DTs)
