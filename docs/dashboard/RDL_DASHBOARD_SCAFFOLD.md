# RDL Dashboard Scaffold v0.1

## Purpose

This dashboard scaffold defines the first visual interface for the Remedy Design Layer (RDL) inside `emo-core-v1`.

The goal is not a polished production dashboard yet. The goal is to expose the current RDL backend in a clear governance-facing layout.

## Core panels

The first scaffold should include seven panels:

1. **Dominant Bottlenecks**
   - Domain
   - Jurisdiction
   - Dominant bottlenecks
   - Confidence

2. **Recommended Portfolio**
   - Portfolio ID
   - Selected options
   - Sequence
   - Rationale

3. **Score Summary**
   - Overall score
   - Feasibility
   - Expected DAC gain
   - Persistence likelihood
   - Contradiction risk
   - Justice risk
   - Legitimacy penalty
   - Semantic efficiency

4. **Tradeoff Report**
   - Tradeoff summary
   - Tradeoff dimensions and values

5. **Legitimacy Review**
   - Summary
   - Rights risk
   - Transparency
   - Contestability
   - Coercion-risk watch

6. **Portfolio Comparison**
   - Baseline
   - Compact
   - Full
   - Score comparison

7. **Adaptive Learning**
   - Expected DAC gain
   - Observed DAC gain
   - Learning gap
   - Persistence gap
   - Adjustment signal

## Suggested interaction flow

User enters or selects:

- domain
- jurisdiction
- DAC-style sub-scores
- optional observed outcome values

Then the interface requests:

- `/remedy/bottlenecks`
- `/remedy/portfolio`
- `/remedy/score`
- `/remedy/tradeoffs`
- `/remedy/legitimacy`
- `/remedy/compare`
- `/remedy/learn` (if observed data is available)

## Minimal layout

Top row:
- Input form
- Bottlenecks card
- Score card

Middle row:
- Portfolio card
- Tradeoff card
- Legitimacy card

Bottom row:
- Comparison card
- Learning card

## v0.1 constraints

This scaffold is intentionally simple:

- no authentication logic
- no persistence layer
- no charting requirements yet
- no historical state browser yet
- no governance memo export yet

## Next UI steps

After the scaffold exists, the next iterations can add:

- comparison charts
- domain selector
- jurisdiction snapshots
- learning-history timeline
- legitimacy warnings with visual severity
- downloadable policy memo export
