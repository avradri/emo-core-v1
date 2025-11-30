# emo/twin_hooks/destine.py
from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

import pandas as pd
import requests
import xarray as xr

from emo.config import USER_AGENT

LOG = logging.getLogger(__name__)

# DestinE Harmonised Data Access (HDA) + STAC endpoints
# See DestinE Data Lake documentation. :contentReference[oaicite:9]{index=9}
DESTINE_HDA_DEFAULT = "https://hda.data.destination-earth.eu"
DESTINE_STAC_DEFAULT = "https://hda.data.destination-earth.eu/stac/v2"

# Digital Twin collections in the DestinE Data Lake portfolio. :contentReference[oaicite:10]{index=10}
CLIMATE_DT_COLLECTION_ID = "EO.ECMWF.DAT.DT_CLIMATE_ADAPTATION"
EXTREMES_DT_COLLECTION_ID = "EO.ECMWF.DAT.DT_EXTREMES"


@dataclass
class DestineConfig:
    """
    Configuration for connecting EMO to DestinE Harmonised Data Access (HDA).

    - hda_base_url: root of the HDA service
    - stac_base_url: root of the STAC v2 API
    - token: OAuth2 bearer token obtained via DestinE Core Service Platform (DESP)
    - timeout: HTTP timeout in seconds

    Environment variables (optional):

    - DESTINE_HDA_BASE_URL
    - DESTINE_STAC_BASE_URL
    - DESTINE_TOKEN
    - DESTINE_TIMEOUT
    """

    hda_base_url: str = DESTINE_HDA_DEFAULT
    stac_base_url: str = DESTINE_STAC_DEFAULT
    token: Optional[str] = None
    timeout: int = 30

    @classmethod
    def from_env(cls) -> "DestineConfig":
        return cls(
            hda_base_url=os.getenv("DESTINE_HDA_BASE_URL", DESTINE_HDA_DEFAULT),
            stac_base_url=os.getenv("DESTINE_STAC_BASE_URL", DESTINE_STAC_DEFAULT),
            token=os.getenv("DESTINE_TOKEN"),
            timeout=int(os.getenv("DESTINE_TIMEOUT", "30")),
        )


@dataclass
class DestineCollectionSummary:
    """
    Minimal description of a DestinE STAC collection.
    """

    id: str
    title: Optional[str]
    description: Optional[str]
    keywords: List[str]
    href: Optional[str]


@dataclass
class DestineItemSummary:
    """
    Minimal description of a DestinE STAC item (a single DT product).
    """

    id: str
    collection_id: str
    start_datetime: Optional[datetime]
    end_datetime: Optional[datetime]
    geometry: Optional[Dict[str, Any]]
    assets: Dict[str, str]  # asset key -> href


class DestineClient:
    """
    Thin client for the DestinE Harmonised Data Access (HDA) and STAC API.

    This is *not* a full SDK – it is a focused, UIA/EMO-aligned adapter that:

    - Discovers Digital Twin collections (Climate Adaptation DT, Extremes DT).
    - Queries STAC items within time windows and bounding boxes.
    - Opens DT assets with xarray for light post-processing.
    - Produces EMO-ready hazard fingerprints for overlay with OI, SMF, GWI, etc. :contentReference[oaicite:11]{index=11}

    The heavy-duty “near-data” workflows (Islet/Stack/Hook, Polytope) remain on
    the DestinE side. :contentReference[oaicite:12]{index=12}
    """

    def __init__(
        self,
        config: Optional[DestineConfig] = None,
        session: Optional[requests.Session] = None,
    ) -> None:
        self.config = config or DestineConfig.from_env()
        self.session = session or requests.Session()

        headers = {"User-Agent": USER_AGENT}
        if self.config.token:
            headers["Authorization"] = f"Bearer {self.config.token}"
        self.session.headers.update(headers)

    # ------------------------------------------------------------------
    # STAC helpers
    # ------------------------------------------------------------------

    def _stac_url(self, path: str) -> str:
        base = self.config.stac_base_url.rstrip("/")
        return f"{base}/{path.lstrip('/')}"

    def list_collections(self) -> List[DestineCollectionSummary]:
        """
        List all STAC collections visible through HDA and return a simplified summary.

        Notes
        -----
        - The STAC endpoint is documented at https://hda.data.destination-earth.eu/docs/.
        - Digital Twin collections (Climate DT, Extremes DT) require appropriate permissions
          managed via the DestinE Core Service Platform. :contentReference[oaicite:13]{index=13}
        """
        url = self._stac_url("collections")
        LOG.info("Requesting DestinE STAC collections from %s", url)
        resp = self.session.get(url, timeout=self.config.timeout)
        resp.raise_for_status()
        payload = resp.json()

        collections: List[DestineCollectionSummary] = []
        for raw in payload.get("collections", []):
            keywords = raw.get("keywords") or []
            href = None
            for link in raw.get("links") or []:
                if link.get("rel") == "self":
                    href = link.get("href")
                    break
            collections.append(
                DestineCollectionSummary(
                    id=raw.get("id"),
                    title=raw.get("title"),
                    description=raw.get("description"),
                    keywords=list(keywords),
                    href=href,
                )
            )
        return collections

    def list_dt_collections(self) -> List[DestineCollectionSummary]:
        """
        Return the subset of collections corresponding to DestinE digital twins
        that EMO cares about (Climate Adaptation DT and Weather-Induced Extremes DT). :contentReference[oaicite:14]{index=14}
        """
        all_cols = self.list_collections()
        wanted_ids = {CLIMATE_DT_COLLECTION_ID, EXTREMES_DT_COLLECTION_ID}
        filtered: List[DestineCollectionSummary] = []
        for c in all_cols:
            if c.id in wanted_ids:
                filtered.append(c)
                continue
            if any(kw in ("DT_CLIMATE_ADAPTATION", "DT_EXTREMES") for kw in c.keywords):
                filtered.append(c)
        return filtered

    def search_items(
        self,
        collection_id: str,
        datetime_range: Optional[Tuple[datetime, datetime]] = None,
        bbox: Optional[Tuple[float, float, float, float]] = None,
        limit: int = 100,
        query: Optional[Dict[str, Any]] = None,
    ) -> List[DestineItemSummary]:
        """
        Search STAC items for a given collection using POST /stac/v2/search.

        Parameters
        ----------
        collection_id:
            STAC collection ID (e.g. EO.ECMWF.DAT.DT_CLIMATE_ADAPTATION).
        datetime_range:
            Optional (start, end) datetime interval for filtering items.
        bbox:
            Optional bounding box [west, south, east, north] in WGS84.
        limit:
            Maximum number of features to return.
        query:
            Optional STAC "query" section for provider-specific filters.
        """
        url = self._stac_url("search")
        body: Dict[str, Any] = {"collections": [collection_id], "limit": limit}

        if datetime_range is not None:
            start, end = datetime_range
            # RFC3339 interval; HDA expects proper datetime strings. :contentReference[oaicite:15]{index=15}
            body["datetime"] = f"{start.isoformat()}Z/{end.isoformat()}Z"
        if bbox is not None:
            body["bbox"] = list(bbox)
        if query:
            body["query"] = query

        LOG.info("STAC search on %s for collection=%s", url, collection_id)
        resp = self.session.post(url, json=body, timeout=self.config.timeout)
        resp.raise_for_status()
        payload = resp.json()

        items: List[DestineItemSummary] = []
        for feat in payload.get("features", []):
            props = feat.get("properties", {}) or {}
            start_dt = _parse_rfc3339(props.get("start_datetime") or props.get("datetime"))
            end_dt = _parse_rfc3339(props.get("end_datetime") or props.get("datetime"))
            raw_assets = feat.get("assets", {}) or {}
            assets: Dict[str, str] = {
                key: value.get("href")
                for key, value in raw_assets.items()
                if isinstance(value, dict) and value.get("href")
            }
            items.append(
                DestineItemSummary(
                    id=feat.get("id"),
                    collection_id=feat.get("collection", collection_id),
                    start_datetime=start_dt,
                    end_datetime=end_dt,
                    geometry=feat.get("geometry"),
                    assets=assets,
                )
            )

        return items

    # ------------------------------------------------------------------
    # Digital Twin convenience wrappers
    # ------------------------------------------------------------------

    def fetch_climate_dt_items(
        self,
        datetime_range: Optional[Tuple[datetime, datetime]] = None,
        bbox: Optional[Tuple[float, float, float, float]] = None,
        limit: int = 50,
    ) -> List[DestineItemSummary]:
        """
        Convenience wrapper for Climate Change Adaptation Digital Twin STAC items.

        Corresponds to the data portfolio entry `EO.ECMWF.DAT.DT_CLIMATE_ADAPTATION`. :contentReference[oaicite:16]{index=16}
        """
        return self.search_items(
            collection_id=CLIMATE_DT_COLLECTION_ID,
            datetime_range=datetime_range,
            bbox=bbox,
            limit=limit,
        )

    def fetch_extremes_dt_items(
        self,
        datetime_range: Optional[Tuple[datetime, datetime]] = None,
        bbox: Optional[Tuple[float, float, float, float]] = None,
        limit: int = 50,
    ) -> List[DestineItemSummary]:
        """
        Convenience wrapper for Weather-Induced and Geophysical Extremes Digital Twin STAC items.

        Corresponds to the data portfolio entry `EO.ECMWF.DAT.DT_EXTREMES`. :contentReference[oaicite:17]{index=17}
        """
        return self.search_items(
            collection_id=EXTREMES_DT_COLLECTION_ID,
            datetime_range=datetime_range,
            bbox=bbox,
            limit=limit,
        )

    # ------------------------------------------------------------------
    # Asset access helpers
    # ------------------------------------------------------------------

    def download_asset(
        self,
        href: str,
        target: Path,
        overwrite: bool = False,
        chunk_size: int = 1024 * 1024,
    ) -> Path:
        """
        Stream a single asset from HDA or a federated endpoint into a local file.

        For large DT outputs it is generally better to work via edge services (Stack/Islet)
        or Polytope, but for EMO diagnostics and lightweight overlays this direct mode is
        sufficient. :contentReference[oaicite:18]{index=18}
        """
        target = Path(target)
        if target.exists() and not overwrite:
            LOG.info("File %s already exists; skipping download", target)
            return target

        LOG.info("Downloading DestinE asset %s -> %s", href, target)
        with self.session.get(href, stream=True, timeout=self.config.timeout) as resp:
            resp.raise_for_status()
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open("wb") as f:
                for chunk in resp.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
        return target

    def open_xarray_from_asset(
        self,
        href: str,
        chunks: Optional[Dict[str, int]] = None,
        engine: Optional[str] = None,
    ) -> xr.Dataset:
        """
        Open an asset (e.g. NetCDF / Zarr / GRIB2) as an xarray.Dataset.

        Notes
        -----
        - For very large DT products, prefer near-data processing inside DestinE’s
          Stack/Islet or Polytope services and only export reduced diagnostics to EMO. :contentReference[oaicite:19]{index=19}
        - For quick experiments and overlays, this helper is fine.
        """
        LOG.info("Opening DestinE asset via xarray: %s", href)
        open_kwargs: Dict[str, Any] = {}
        if chunks is not None:
            open_kwargs["chunks"] = chunks
        if engine is not None:
            open_kwargs["engine"] = engine
        return xr.open_dataset(href, **open_kwargs)  # type: ignore[arg-type]

    # ------------------------------------------------------------------
    # Hazard summarisation for EMO overlays
    # ------------------------------------------------------------------

    def summarise_hazard_for_items(
        self,
        items: List[DestineItemSummary],
        variable: str,
        asset_key: Optional[str] = None,
        quantiles: Iterable[float] = (0.5, 0.9, 0.99),
        max_items: Optional[int] = None,
        xarray_open_kwargs: Optional[Dict[str, Any]] = None,
    ) -> pd.DataFrame:
        """
        For each item, open a chosen asset, extract a variable, and compute basic statistics.

        This turns high-resolution DT output into compact feature vectors that EMO can
        join with OI, SMF, τ_I and UIA metrics in the SCL layer. :contentReference[oaicite:20]{index=20}

        Parameters
        ----------
        items:
            List of STAC item summaries (typically from fetch_climate_dt_items()).
        variable:
            Name of the variable inside the dataset (e.g. 'tasmax', 'pr', 'wind_speed').
        asset_key:
            Optional asset key to prefer (e.g. 'data'); if None, heuristics are used.
        quantiles:
            Iterable of quantiles in [0,1] to compute (e.g. 0.5, 0.9, 0.99).
        max_items:
            Optional hard cap on the number of items to process (for safety).
        xarray_open_kwargs:
            Extra kwargs passed to xarray.open_dataset (e.g. {'engine': 'cfgrib'}).

        Returns
        -------
        pandas.DataFrame
            Columns: item_id, collection_id, variable, stat, value, units,
                     start_datetime, end_datetime
        """
        rows: List[Dict[str, Any]] = []
        if xarray_open_kwargs is None:
            xarray_open_kwargs = {}

        iterator = items
        if max_items is not None:
            iterator = items[:max_items]

        for item in iterator:
            href = _select_asset_href(item.assets, asset_key)
            if not href:
                LOG.warning("No asset href found for item %s", item.id)
                continue

            try:
                ds = self.open_xarray_from_asset(href, **xarray_open_kwargs)
            except Exception as exc:  # pragma: no cover - defensive
                LOG.exception("Failed to open asset for item %s: %s", item.id, exc)
                continue

            if variable not in ds:
                LOG.warning(
                    "Variable %s not found in dataset for item %s; available=%s",
                    variable,
                    item.id,
                    list(ds.data_vars),
                )
                continue

            try:
                stats = summarise_variable_statistics(ds, variable, quantiles)
            except Exception as exc:  # pragma: no cover - defensive
                LOG.exception(
                    "Failed to summarise variable %s for item %s: %s",
                    variable,
                    item.id,
                    exc,
                )
                continue

            units = ds[variable].attrs.get("units")

            for stat_name, value in stats.items():
                rows.append(
                    {
                        "item_id": item.id,
                        "collection_id": item.collection_id,
                        "variable": variable,
                        "stat": stat_name,
                        "value": float(value),
                        "units": units,
                        "start_datetime": item.start_datetime,
                        "end_datetime": item.end_datetime,
                    }
                )

        return pd.DataFrame(rows)

    def build_climate_dt_hazard_table(
        self,
        variable: str,
        datetime_range: Optional[Tuple[datetime, datetime]] = None,
        bbox: Optional[Tuple[float, float, float, float]] = None,
        quantiles: Iterable[float] = (0.5, 0.9, 0.99),
        limit: int = 20,
        asset_key: Optional[str] = None,
        xarray_open_kwargs: Optional[Dict[str, Any]] = None,
    ) -> pd.DataFrame:
        """
        One-shot helper for EMO pipelines:

        1. Fetch Climate DT items in a spatio-temporal window.
        2. Summarise the chosen variable into hazard fingerprints.

        This is designed to be called from the EMO DIH / RUE layers when computing
        𝓡[g_I], ℬ or when building scenario overlays for SMF and GWI. 
        """
        items = self.fetch_climate_dt_items(datetime_range=datetime_range, bbox=bbox, limit=limit)
        return self.summarise_hazard_for_items(
            items=items,
            variable=variable,
            asset_key=asset_key,
            quantiles=quantiles,
            xarray_open_kwargs=xarray_open_kwargs,
        )


# ----------------------------------------------------------------------
# Standalone helpers
# ----------------------------------------------------------------------


def _parse_rfc3339(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    try:
        # keep in UTC but drop tz info for simplicity
        if value.endswith("Z"):
            value = value[:-1] + "+00:00"
        return datetime.fromisoformat(value)
    except Exception:
        return None


def _select_asset_href(assets: Dict[str, str], preferred_key: Optional[str]) -> Optional[str]:
    """
    Pick an asset href from the STAC "assets" map using light heuristics.
    """
    if not assets:
        return None
    if preferred_key and preferred_key in assets:
        return assets[preferred_key]
    # Prefer commonly used keys
    for key in ("data", "default", "asset"):
        if key in assets:
            return assets[key]
    # Fallback: first asset
    for _, href in assets.items():
        return href
    return None


def summarise_variable_statistics(
    ds: xr.Dataset,
    variable: str,
    quantiles: Iterable[float] = (0.5, 0.9, 0.99),
) -> Dict[str, float]:
    """
    Summarise a DT variable into a small set of statistics.

    The goal is not to replace impact modelling, but to provide:

    - A robust mean over space and time,
    - Selected quantiles (e.g. 90th / 99th percentiles),
    - A simple temporal delta for trend-like signals.

    This gives EMO a compact "hazard fingerprint" for each DT product that can
    be aligned with species-mind metrics (OI, SMF, GWI, τ_I) and then mapped
    into UIA terms (𝓡[g_I], ℬ, dS/dt, dI/dt). 
    """
    da = ds[variable]
    dims = list(da.dims)

    time_dim_candidates = ["time", "valid_time", "forecast_reference_time", "t"]
    time_dim = next((d for d in time_dim_candidates if d in dims), None)

    spatial_dims = [d for d in dims if d != time_dim]

    reduced = da
    if spatial_dims:
        reduced = reduced.mean(dim=spatial_dims, skipna=True)

    stats: Dict[str, float] = {}

    # Global mean
    stats["mean"] = float(reduced.mean(skipna=True).values)

    # Quantiles
    q_list = list(quantiles)
    if q_list:
        if time_dim:
            q_da = reduced.quantile(q_list, dim=time_dim, skipna=True)
        else:
            q_da = reduced.quantile(q_list, skipna=True)

        # xarray returns a DataArray with quantile dimension = 'quantile'
        # We assume 1D here.
        q_values = q_da.values
        for q, value in zip(q_list, q_values):
            stats[f"q{int(100 * q):02d}"] = float(value)

    # Simple temporal delta (last - first) as a crude trend signal
    if time_dim and time_dim in reduced.dims and reduced.sizes.get(time_dim, 0) >= 2:
        first = reduced.isel({time_dim: 0}).values
        last = reduced.isel({time_dim: -1}).values
        stats["delta"] = float(last - first)

    return stats


def build_emo_destine_overlay(
    hazard_df: pd.DataFrame,
    emo_metric_df: pd.DataFrame,
    hazard_time_col: str = "start_datetime",
    emo_time_col: str = "year",
) -> pd.DataFrame:
    """
    Join DestinE hazard fingerprints with EMO metrics for dual-twin overlays.

    Typical usage:

    - hazard_df: output of build_climate_dt_hazard_table()
      (item_id, variable, stat, value, start_datetime, ...).
    - emo_metric_df: EMO metric per year/period (e.g. SMF, OI, GWI burst counts).

    The overlay will have:

    - DT hazard statistics per item,
    - corresponding EMO metrics for the matching year,
    - ready to be served via the EMO API for map overlays (e.g. in DestinE frontends). :contentReference[oaicite:23]{index=23}
    """
    if hazard_time_col not in hazard_df.columns:
        raise ValueError(f"hazard_df has no '{hazard_time_col}' column")

    overlay = hazard_df.copy()
    overlay["_hazard_time"] = pd.to_datetime(overlay[hazard_time_col])
    overlay["year"] = overlay["_hazard_time"].dt.year

    joined = overlay.merge(
        emo_metric_df,
        left_on="year",
        right_on=emo_time_col,
        how="left",
        suffixes=("", "_emo"),
    )
    return joined


__all__ = [
    "DestineConfig",
    "DestineClient",
    "DestineCollectionSummary",
    "DestineItemSummary",
    "summarise_variable_statistics",
    "build_emo_destine_overlay",
]
