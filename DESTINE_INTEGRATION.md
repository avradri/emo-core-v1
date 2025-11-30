# EMO × DestinE – Dual-Twin Integration

_EMO v1.0 | DestinE integration note_

## 1. Why this matters

Destination Earth (DestinE) is building high-resolution **digital twins of the Earth system**:
a Digital Twin Engine (DTE), thematic digital twins (Climate Adaptation DT, Extremes DT),
a Data Lake, and a Core Service Platform for users. :contentReference[oaicite:28]{index=28}  

EMO v1.0 is the **cognitive twin**: a live observatory of species-level cognition that measures
whether humanity’s emergent mind is actually learning, coordinating, and acting in time.   

The combination is a genuine **dual-twin** system:

- DestinE: “What is the Earth system doing under different scenarios?”
- EMO: “How is the species mind responding – and is that response adequate?”

## 2. Technical integration

DestinE exposes its Digital Twin outputs via the **DestinE Data Lake** and the Harmonised
Data Access (HDA) service, including a STAC v2 API:

- HDA root: `https://hda.data.destination-earth.eu`
- STAC API: `https://hda.data.destination-earth.eu/stac/v2/` :contentReference[oaicite:30]{index=30}  

The two main DT collections EMO targets first are:

- `EO.ECMWF.DAT.DT_CLIMATE_ADAPTATION` – Climate Change Adaptation Digital Twin
- `EO.ECMWF.DAT.DT_EXTREMES` – Weather-Induced and Geophysical Extremes Digital Twin :contentReference[oaicite:31]{index=31}  

On the EMO side, this repository provides:

- `emo.twin_hooks.destine.DestineClient`  
  – wraps STAC queries and asset access.
- `DestineClient.build_climate_dt_hazard_table()`  
  – turns DT output fields (e.g. tasmax, precipitation) into compact hazard fingerprints.
- `emo.twin_hooks.destine.build_emo_destine_overlay()`  
  – joins DT fingerprints with EMO metrics (OI, SMF, GWI, τ_I) for dual-twin overlays.

These tables feed into:

- The **Species-Mind & Planetary Health layer (SCL)** (e.g. climate SMF, GWI) and
- The **UIA Engine (RUE)**, which uses DT ensembles to estimate 𝓡[g_I], ℬ, dS/dt, dI/dt
  for the human–Earth interface. :contentReference[oaicite:32]{index=32}  

## 3. Minimal example (notebook / script)

```python
from datetime import datetime
import pandas as pd

from emo.twin_hooks import DestineClient, build_emo_destine_overlay
from emo.organismality import compute_organismality_index
from emo.smf import compute_smf

# 1. Connect to DestinE (token must be set via DESTINE_TOKEN environment variable)
client = DestineClient()

# 2. Pull a small sample of Climate DT output and summarise a hazard variable
start = datetime(2030, 1, 1)
end = datetime(2039, 12, 31)
hazard_df = client.build_climate_dt_hazard_table(
    variable="tasmax",
    datetime_range=(start, end),
    limit=5,  # keep it small for a demo
)

# 3. Compute an EMO metric over the same period (e.g. climate SMF per year)
smf_res = compute_smf(start_year=1990)
smf_df = smf_res.df[["year", "smf_local"]].groupby("year").mean().reset_index()

# 4. Build an overlay table for dashboards / DestinE frontends
overlay_df = build_emo_destine_overlay(
    hazard_df=hazard_df,
    emo_metric_df=smf_df,
    hazard_time_col="start_datetime",
    emo_time_col="year",
)

print(overlay_df.head())
