# Remedy Design Layer (RDL) v0.1

## Overview

The Remedy Design Layer (RDL) is the intervention layer that extends the EMO + DAC stack beyond diagnosis and actuation audit into structured remedy design.

In the current architecture:

- UIA measures the ledger
- EMO measures the condition
- DAC measures conversion
- RDL designs repair

RDL v0.1 is intentionally modest, explicit, and rule-based. It does not attempt to act as a policy oracle. Instead, it provides a transparent first-pass framework for:

- bottleneck attribution
- intervention mapping
- portfolio construction
- portfolio scoring
- trade-off reporting
- legitimacy review
- simple simulation
- narrative explanation

## Current implementation

RDL is implemented inside `emo-core-v1` as a first-class subsystem.

### Core modules

Located under:

- `emo/remedy/`

Current modules:

- `bottlenecks.py`
- `intervention_library.py`
- `portfolio_builder.py`
- `scoring.py`
- `simulation.py`
- `tradeoffs.py`
- `legitimacy.py`

### Data models

Located under:

- `emo/models/`

Current RDL-related models:

- `bottleneck_profile.py`
- `intervention_option.py`
- `remedy_portfolio.py`
- `portfolio_score.py`
- `remedy_simulation.py`
- `remedy_tradeoff.py`
- `legitimacy_report.py`

### API layer

Located under:

- `api/routers/remedy.py`
- `api/services/remedy_service.py`
- `api/schemas/remedy_request.py`
- `api/schemas/remedy_response.py`

## Current endpoints

RDL v0.1 currently exposes the following endpoints:

- `POST /remedy/bottlenecks`
- `POST /remedy/options`
- `POST /remedy/portfolio`
- `POST /remedy/score`
- `GET /remedy/library`
- `POST /remedy/explain`
- `POST /remedy/simulate`
- `POST /remedy/tradeoffs`
- `POST /remedy/legitimacy`

## Endpoint roles

### `POST /remedy/bottlenecks`

Builds a first-pass bottleneck profile from DAC-style sub-scores.

Inputs include:

- `validation_score`
- `translation_score`
- `budget_score`
- `deployment_score`
- `persistence_score`
- `contradiction_score`

Outputs include:

- dominant bottlenecks
- confidence score

### `POST /remedy/options`

Maps dominant bottlenecks to intervention options from the current remedy library.

### `POST /remedy/portfolio`

Builds a compact remedy portfolio from available options using transparent ordering rules.

### `POST /remedy/score`

Scores the selected portfolio across a small v0.1 metric set:

- feasibility
- expected DAC gain
- persistence likelihood
- contradiction risk
- justice risk
- semantic efficiency
- overall score

### `GET /remedy/library`

Returns either:

- the full remedy library
- or one domain-specific slice using `?domain=...`

### `POST /remedy/explain`

Returns a readable rule-based explanation that summarizes:

- dominant bottlenecks
- recommended portfolio
- score interpretation

### `POST /remedy/simulate`

Returns a simple rule-based comparison of three scenarios:

- `do_nothing`
- `selected_portfolio`
- `high_friction`

### `POST /remedy/tradeoffs`

Returns a structured trade-off report derived from the portfolio score.

### `POST /remedy/legitimacy`

Returns a first-pass legitimacy review with flags such as:

- rights risk
- transparency
- contestability
- coercion-risk watch

## Current domains

RDL v0.1 currently includes these intervention-library domains:

- `pandemic`
- `disaster`
- `climate_mitigation`

## Design principles

RDL v0.1 follows five principles:

1. Explicit mappings instead of hidden inference
2. Rule-based logic instead of overclaiming prediction
3. Compact portfolios rather than inflated policy catalogs
4. Contestable outputs rather than technocratic closure
5. Clear separation between diagnosis, remedy generation, and evaluation

## Status

RDL v0.1 is operational inside the repo and exposed through FastAPI.

At the time of this documentation update, the subsystem includes API test coverage for:

- score
- portfolio
- bottlenecks
- options
- library
- explain
- simulate
- tradeoffs
- legitimacy
- climate mitigation library access

## Known limitations

RDL v0.1 remains deliberately constrained.

Current limitations include:

- rule-based scoring only
- no empirical learning loop yet
- no multi-portfolio comparison endpoint yet
- no domain-specific weighting profiles yet
- no full legitimacy-constrained optimization yet
- no persistence calibration from observed outcomes yet

## Next candidate steps

Possible next directions include:

- portfolio comparison endpoint
- domain expansion (`food_security`, `migration_stress`, `pandemic preparedness+`, etc.)
- stronger explanation generation
- legitimacy-aware scoring
- observed-outcome learning loop
- domain-specific simulation profiles
- dashboard integration

## Suggested example request

Example `POST /remedy/score` payload:

```json
{
  "domain": "disaster",
  "jurisdiction": "RO",
  "validation_score": 0.8,
  "translation_score": 0.4,
  "budget_score": 0.5,
  "deployment_score": 0.6,
  "persistence_score": 0.45,
  "contradiction_score": 0.7
}
