"""
Hooks for UNDRR / WMO Early Warnings for All (EW4All) and related
multi-hazard early-warning system status data.

This subpackage currently provides a light-weight HTTP client for early
warning coverage summaries, designed so that labs and infrastructure
teams can plug EMO-Core into their own EW4All-compatible data sources.
"""

from .undrr_wmo import EarlyWarningClient, EarlyWarningCoverage

__all__ = [
    "EarlyWarningCoverage",
    "EarlyWarningClient",
]
