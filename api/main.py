# api/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers import metrics, uia


DESCRIPTION = """
Emergent Mind Observatory (EMO) v1.0 API

This API exposes:

- Species-mind metrics (OI, synergy, GWI, SMF, τ_I) built from open data. :contentReference[oaicite:5]{index=5}
- Prototype DestinE × EMO overlays so digital twin scenarios can be viewed
  together with cognitive metrics. 
- Early UIA-style summaries for the human–Earth interface. 
"""

app = FastAPI(
    title="Emergent Mind Observatory API",
    version="1.0.0",
    description=DESCRIPTION,
    contact={"name": "EMO team", "email": "contact@example.org"},
)


# Allow the dashboard / notebooks / DestinE frontends to call us easily
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten later if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["ops"])
def health() -> dict:
    """
    Lightweight health check for ops and uptime monitoring.
    """
    return {"status": "ok"}


# Mount routers under /v1
app.include_router(metrics.router, prefix="/v1")
app.include_router(uia.router, prefix="/v1")
