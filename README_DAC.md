# DAC v0.1

Diagnostic-to-Actuation Coupling (DAC) is a first-class subsystem inside EMO.

## What DAC does

DAC measures how strongly validated signals of danger are translated into:

- policy action
- budget commitment
- delivery
- persistence
- observable response structure

## Current scaffold

The current DAC scaffold includes:

- API endpoints for domains, events, comparison, metrics summary, current mode, and report snapshot
- typed schemas and services
- typed core models
- harmonization helpers
- DAC metric modules
- behavioral mode inference
- fixtures and integration tests

## Current DAC endpoints

- `/dac/domains`
- `/dac/events`
- `/dac/compare`
- `/dac/metrics/summary`
- `/dac/modes/current`
- `/dac/report/snapshot`

## Initial v0.1 domains

- disaster preparedness
- pandemic response

## Status

This is a clean v0.1 foundation branch. The current implementation uses demo data and route scaffolding, preparing the repo for real data ingestion, domain linking, metric computation, and dashboard integration.
