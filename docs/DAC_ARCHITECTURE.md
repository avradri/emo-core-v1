# DAC Architecture

DAC (Diagnostic-to-Actuation Coupling) is a first-class subsystem inside EMO.

## Purpose

DAC measures how strongly validated signals of danger are translated into:

- policy action
- budget commitment
- operational delivery
- persistent implementation
- observable improvement

## Position inside EMO

- EMO = observatory layer
- UIA = formal interface ledger
- DAC = dynamic bridge from diagnosis to organized response

DAC is not a separate replacement for EMO. It extends EMO by measuring the conversion of diagnostics into actuation.

## v0.1 design principle

DAC will be built inside `emo-core-v1` with a clean package boundary so it can later be split into a dedicated repository if needed.

## Initial v0.1 domains

- disaster preparedness
- pandemic response

## Initial architecture areas

- typed domain models
- harmonization and event linking
- DAC metric engine
- behavioral mode inference
- API routes
- dashboard outputs
- snapshot reporting

## Core design rule

DAC should not begin as one magic score.

It should begin as a family of metric groups:

- lag metrics
- conversion metrics
- persistence metrics
- alignment metrics
- contradiction metrics
