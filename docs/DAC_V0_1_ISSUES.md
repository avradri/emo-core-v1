# DAC v0.1 Issue List

## Phase 1 - Replace demo data with real internal records
- connect `/dac/events` to real `DiagnosticEvent` and `PolicyInstrument` objects
- return structured event records from model-backed data instead of hard-coded demo values
- define the first in-repo demo dataset for Romania disaster response
- define the first in-repo demo dataset for pandemic response

## Phase 2 - Compute real metrics
- make `/dac/metrics/summary` compute values from `lag.py`
- connect conversion metrics from `conversion.py`
- connect persistence metrics from `persistence.py`
- connect contradiction metrics from `contradiction.py`
- replace static service values with computed outputs

## Phase 3 - Connect behavioral inference to computed metrics
- feed computed metrics into `infer_behavioral_mode`
- remove hard-coded demo metrics from `/dac/modes/current`
- add richer mode rules for pulsed adaptation and contradictory action
- add uncertainty notes later

## Phase 4 - Domain-aware DAC behavior
- use `DomainProfile` fixtures to parameterize disaster and pandemic logic
- connect lag targets and weighting schemes
- define domain-specific event linking rules
- define first contradiction rules per domain

## Phase 5 - Reporting and snapshots
- make `/dac/report/snapshot` build from computed metrics and inferred mode
- connect `build_dac_snapshot` to the snapshot service
- add timestamped snapshot records later
- prepare machine-readable report exports

## Phase 6 - API expansion
- add query parameters for jurisdiction
- add query parameters for domain
- add compare parameters for left and right jurisdictions
- add event filters by type and date

## Phase 7 - Dashboard integration
- add DAC overview card
- add metrics summary card
- add current mode card
- add events timeline card
- add compare view card

## Phase 8 - Validation and test expansion
- add tests for model-backed event services
- add tests for computed metrics summary responses
- add tests for domain-aware inference behavior
- add tests for snapshot generation from live values

## First practical target
- Romania disaster demo flow
- one diagnostic event
- one policy event
- one delivery event
- computed lag
- computed mode
- snapshot output
