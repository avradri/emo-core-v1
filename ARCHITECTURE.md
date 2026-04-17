cat > ARCHITECTURE.md <<'EOF'
# EMO-Core Architecture

This file gives a **developer-facing overview** of the EMO-Core architecture.

For the full conceptual and scientific description, see:

- `WHITEPAPER_EMO_v1_1_funders.md`
- `README.md`
- `README_DAC.md`
- `docs/DAC_ARCHITECTURE.md`
- `docs/DAC_METRICS.md`

---

## 1. Layers

1. **Interface Registry (IR)**  
   Registry of interfaces `Σᵢ` across the human–Earth system, including:

   - Earth-system and forecasting infrastructures
   - Media and event streams
   - Knowledge systems
   - Governance and early-warning systems
   - Economic, trade, and finance interfaces

2. **Data Ingestion & Harmonization (DIH)**  
   Ingestion and preprocessing layer for upstream signals, snapshots, and time series.

   Responsibilities:

   - Pull data from APIs, files, and demo fixtures
   - Normalize timestamps and temporal resolution
   - Align domains, jurisdictions, hazards, and topics
   - Produce clean feature tables for metric computation
   - Maintain quality flags and event-linking logic

3. **Reciprocity & UIA Engine (RUE)**  
   Computes UIA-related quantities for the human–Earth interface.

   Core functions:

   - Informational curvature
   - Focusing bracket dynamics
   - Coherence, entropy, and information aggregation
   - Semantic efficiency
   - Local `a_UIA` estimation
   - Coarse-grained `Ā_UIA` aggregation
   - UIA band assignment

4. **Species-Mind & Planetary Health Layer (SCL)**  
   Computes species-level cognition and planetary-response metrics.

   Metric stack:

   - **OI** v1.0 — Organismality (treaties, compliance, conflict, alliances)
   - **SΦ / Ω** v1.0 — Synergy across multi-stream attention, decision, and memory
   - **GWI** v1.0 — Global workspace ignition map
   - **SMF** v1.0 — Self-Model Fidelity across climate, health, and biodiversity models
   - **τᵢ** v1.0 — Information-time across domains
   - **Reciprocity fluxes** — `R`, `J_B`, `B` (exosomatic buffering vs selection)
   - **Planetary-health indicators** — boundary transgression, early-warning coverage, related system stress signals

5. **DAC Layer (Diagnostic-to-Actuation Coupling)**  
   DAC is a first-class subsystem inside EMO. It measures whether validated diagnosis is converted into organized response.

   Conceptually, DAC sits between recognized risk and downstream implementation.  
   Operationally, it extends EMO from a cognitive observatory into a response-aware observatory.

   DAC includes metrics for:

   - **lag** — how long it takes to move from diagnosis to response
   - **conversion** — whether warnings and assessments become commitments, budgets, or interventions
   - **persistence** — whether response is sustained over time
   - **contradiction** — whether systems acknowledge a risk while materially reinforcing it
   - **shared/comparative metrics** — cross-domain and cross-jurisdiction benchmarking
   - **behavioral mode inference** — response pattern classification from DAC metric bundles
   - **snapshot/report generation** — state-of-response views for domains and scenarios

   Within the broader architecture:

   - **EMO** observes collective cognition
   - **UIA** formalizes interface structure and organismality
   - **DAC** measures the bridge from diagnosis to organized response

6. **Interface & Governance Layer (IDL)**  
   Delivery layer for APIs, demos, dashboards, and governance-facing outputs.

   Includes:

   - REST API routers
   - Schema validation and query models
   - Demo flows and scenario services
   - Dashboard integration
   - Reporting hooks
   - Governance and observatory-facing outputs

---

## 2. Codebase layout

```text
emo-core-v1/
  README.md
  README_DAC.md
  ARCHITECTURE.md
  DESTINE_INTEGRATION.md
  LIVE_PIPELINES.md
  Dockerfile
  docker-compose.yml
  pyproject.toml
  requirements.txt

  api/
    __init__.py
    main.py
    demo/
      __init__.py
      bulgaria_disaster_demo.py
      romania_disaster_demo.py
    routers/
      __init__.py
      dac.py
      interfaces.py
      metrics.py
      uia.py
    schemas/
      __init__.py
      dac.py
      dac_compare.py
      dac_compare_query.py
      dac_event_query.py
      dac_events.py
      dac_metrics.py
      dac_metrics_query.py
      dac_mode.py
      dac_mode_query.py
      dac_snapshot.py
      dac_snapshot_query.py
    services/
      __init__.py
      dac_compare_demo_flow_service.py
      dac_compare_service.py
      dac_compare_shared_metrics_service.py
      dac_demo_flow_service.py
      dac_events_service.py
      dac_metrics_service.py
      dac_mode_service.py
      dac_service.py
      dac_shared_metrics_service.py
      dac_snapshot_service.py

  emo/
    __init__.py
    config.py
    data_sources.py
    gwi.py
    info_time.py
    organismality.py
    reciprocity.py
    smf.py
    synergy.py

    ew_hooks/
      __init__.py
      undrr_wmo.py

    harmonize/
      __init__.py
      event_linking.py
      jurisdiction_mapping.py
      quality_flags.py
      time_alignment.py

    inference/
      __init__.py
      behavioral_modes.py

    ingestion/
      __init__.py
      base.py
      forecast_skill.py
      gdelt.py
      openalex.py
      owid.py
      pipelines.py
      wikipedia.py

    metrics/
      __init__.py
      dac/
        __init__.py
        contradiction.py
        conversion.py
        lag.py
        persistence.py

    models/
      __init__.py
      budget_commitment.py
      delivery_trace.py
      diagnostic_event.py
      domain_profile.py
      policy_instrument.py
      validation_outcome.py

    reporting/
      __init__.py
      snapshots.py

    services/
      metrics.py

    twin_hooks/
      __init__.py
      climate_ensembles.py
      destine.py

    uia_engine/
      __init__.py
      aggregate.py
      coherence_entropy_info.py
      focusing.py
      geometry.py
      models.py
      semantic_efficiency.py

    unit/
      test_dac_conversion.py
      test_dac_lag.py
      test_dac_persistence.py

  dashboard/
    app/
      components/
        ScenarioTable.tsx
        UIAGauge.tsx
      globals.css
      layout.tsx
      page.tsx
    next.config.js
    package.json
    tsconfig.json

  docs/
    DAC_ARCHITECTURE.md
    DAC_METRICS.md
    DAC_V0_1_ISSUES.md
    DAC_V0_1_ROADMAP.md
    TECH_CONTACT.md

  data/
    ecmwf_headline_scores.csv

  deck/
    EMO_v1_Founder_Pitch_Deck.md

  grants/
    GRANT_HorizonEurope_EMO_v1.md

  notebooks/
    emo_v10_demos.ipynb

  orchestration/
    airflow_dag_emo.py
    prefect_flows.py

  tests/
    __init__.py
    fixtures/
      bulgaria_disaster_demo.py
      disaster_domain_profile.py
      pandemic_domain_profile.py
      romania_disaster_demo.py
    integration/
      test_dac_compare_router.py
      test_dac_events_router.py
      test_dac_metrics_router.py
      test_dac_mode_router.py
      test_dac_router.py
      test_dac_snapshot_router.py
    unit/
      test_behavioral_modes.py
      test_dac_contradiction.py
      test_domain_profiles.py
      test_event_linking.py
      test_jurisdiction_mapping.py
      test_quality_flags.py
      test_snapshots.py
      test_time_alignment.py
    test_api_uia_and_meta.py
    test_imports.py
    test_metrics_service.py
    test_organismality_basic.py
    test_uia_engine_smoke.py
