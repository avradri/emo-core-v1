# EMO‑Core v1.0 — Emergent Mind Observatory

> A continuous cognitive layer for the planet, built on the Emergent Mind Observatory (EMO) and the Universal Interface Action (UIA). 

EMO‑Core v1.0 is the backend engine for the **Emergent Mind Observatory (EMO)**:

- Ingests multi‑stream global data (planetary boundaries, climate models, digital twins, early‑warning systems, media, knowledge graphs, trade and finance). :contentReference[oaicite:9]{index=9}  
- Computes species‑level cognition metrics:
  - **OI** – Organismality Index (cooperation vs conflict)
  - **SΦ / Ω** – Synergy / O‑information across media, science, policy
  - **GWI** – Global Workspace Ignition
  - **SMF** – Self‑Model Fidelity
  - **τᵢ** – Information‑time (validated predictive capacity)
  - **Reciprocity fluxes** – R, J_B, B (exosomatic buffering and environmental selection)
- Maps them into **UIA** density `a_UIA` and its coarse‑grained counterpart `Ȧ_UIA` for the human–Earth interface. :contentReference[oaicite:10]{index=10}  
- Exposes APIs and dashboards that act as a **“vital signs monitor” for the species‑mind**.

Think of DestinE and climate models as the *physical twin* of Earth, and EMO‑Core as part of a *cognitive twin* for humanity’s emergent mind.   

---

## What this repo gives you

- A **Python package** `emo` implementing:
  - Core EMO metrics (OI, SΦ, GWI, SMF, τᵢ, reciprocity fluxes)
  - A first‑cut **UIA engine** that aggregates curvature, focusing, coherence, entropy, information, and semantic efficiency into `a_UIA`
- A **FastAPI** service exposing:
  - `/metrics/oi`, `/metrics/synergy`, `/metrics/gwi`, `/metrics/smf`, `/metrics/tau_i`
  - `/uia/summary` — coarse‑grained UIA vital signs
  - `/interfaces` — a simple in‑memory Interface Registry
- Integration hooks for:
  - **GDELT** (global news graph) :contentReference[oaicite:12]{index=12}  
  - **OpenAlex** (scholarly knowledge graph) :contentReference[oaicite:13]{index=13}  
  - **Destination Earth (DestinE) digital twins** :contentReference[oaicite:14]{index=14}  
  - **UNDRR / WMO “Early Warnings for All”** coverage and status reports :contentReference[oaicite:15]{index=15}  

This is **v1.0 of the core engine**: enough structure to be credible with labs, agencies, and funders, while staying runnable on a single VM.

---

## High‑level architecture

The design follows the EMO v1.0 architecture document: :contentReference[oaicite:16]{index=16}  

1. **Interface Registry (IR)** — catalog of interfaces Σᵢ:
   - Earth‑system (DestinE, CMIP, ECMWF)
   - Media & events (GDELT)
   - Knowledge graphs (OpenAlex)
   - Governance & early‑warning (UNDRR/WMO, EW4All)
2. **Data Ingestion & Harmonisation (DIH)** — ETL/ELT into an EMO data lake/warehouse.
3. **Reciprocity & UIA Engine (RUE)** — computes `𝓡[g_I]`, ℬ, C(t), S(t), I(t), M_E and aggregates to `a_UIA`, `Ȧ_UIA`. :contentReference[oaicite:17]{index=17}  
4. **Species‑Mind & Planetary Health Layer (SCL)** — OI, SΦ, GWI, SMF, τᵢ, reciprocity fluxes, planetary‑health indicators.
5. **Interface & Governance Layer (IDL)** — APIs, dashboards, reporting, and governance hooks.

In this repo we implement a **thin, testable slice** of each layer.

---

## Quick start

### 0. Requirements

- Python **3.11+**
- `git`
- Optional but recommended: Docker & Docker Compose

### 1. Clone and install

```bash
git clone https://github.com/YOUR-ORG/emo-core-v1.git
cd emo-core-v1

python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

pip install -r requirements.txt
