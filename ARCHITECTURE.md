# EMO‑Core v1.0 Architecture

This file gives a **developer‑facing overview** of the EMO‑Core architecture.  
For the full conceptual and scientific description, see:

- *EMO v1.0 – Architecture Document* (Draft v2.0, Nov 2025) :contentReference[oaicite:21]{index=21}  
- *The Emergent Mind Observatory* and *Universal Interface Action (UIA) v2.0* preprints.   

---

## 1. Layers

1. **Interface Registry (IR)**  
   Postgres‑backed (later) registry of all interfaces Σᵢ:
   - Earth‑system (DestinE, CMIP, ECMWF)
   - Media / events (GDELT)
   - Knowledge graphs (OpenAlex)
   - Governance & early warnings (UNDRR/WMO, EW4All)
   - Economics, trade, finance

2. **Data Ingestion & Harmonisation (DIH)**  
   Orchestrated by Airflow/Prefect (future). Tasks:

   - Pull snapshots and time series from APIs and files.
   - Normalise timestamps and resample to EMO reference grids.
   - Align ontologies (topics, regions, hazards).
   - Produce per‑metric feature tables.

3. **Reciprocity & UIA Engine (RUE)**  

   Computes UIA‑related quantities for the human–Earth interface:

   - Informational curvature `𝓡[g_I]` (from climate/risk/health model manifolds).
   - Focusing bracket ℬ (from circulation‑style balances).
   - Coherence `C(t)` (from GWI and cross‑stream phase locking).
   - Entropy `S(t)` (planetary‑health / risk indicators).
   - Information `I(t)` (forecast skill & knowledge‑graph growth).
   - Semantic efficiency `M_E` (risk reduction per Joule).

   Then:

   - Computes `a_UIA` locally.
   - Aggregates to coarse‑grained `Ȧ_UIA` time series.
   - Defines **UIA bands** (healthy, unstable, pathological).

4. **Species‑Mind & Planetary Health Layer (SCL)**  

   Metric stack:

   - **OI** v1.0 — Organismality (treaties, compliance, conflict, alliances).
   - **SΦ / Ω** v1.0 — Synergy across multi‑stream attention/decision/memory.
   - **GWI** v1.0 — Global workspace ignition map.
   - **SMF** v1.0 — Self‑Model Fidelity across climate/health/biodiversity models.
   - **τᵢ** v1.0 — Information‑time across domains.
   - **Reciprocity fluxes** — R, J_B, B (exosomatic buffering vs selection).
   - **Planetary‑health indicators** — boundary transgression, EW coverage.

5. **Interface & Governance Layer (IDL)**  

   - REST API (`/metrics/*`, `/uia/summary`, `/interfaces`).
   - Future dashboard (React/Next.js).
   - Governance hooks (partner tier, ethics panel, observatory reports).

---

## 2. Codebase layout

```text
emo-core-v1/
  README.md
  ARCHITECTURE.md
  requirements.txt
  Dockerfile
  docker-compose.yml

  emo/
    __init__.py
    config.py
    data_sources.py
    organismality.py
    synergy.py
    gwi.py
    smf.py
    info_time.py
    reciprocity.py
    uia_engine/
      __init__.py
      models.py
      geometry.py
      focusing.py
      coherence_entropy_info.py
      semantic_efficiency.py
      aggregate.py
    twin_hooks/
      __init__.py
      destine.py
      climate_ensembles.py
    ew_hooks/
      __init__.py
      undrr_wmo.py

  api/
    __init__.py
    main.py
    routers/
      __init__.py
      metrics.py
      uia.py
      interfaces.py

  data/
    ecmwf_headline_scores.csv

  notebooks/
    emo_v10_demos.ipynb
