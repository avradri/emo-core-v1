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

DESTINE_HDA_DEFAULT = "https://hda-01.destine.eu"  # placeholder; update when stable
DESTINE_STAC_DEFAULT = "https://hda-01.destine.eu/stac"  # placeholder

CLIMATE_DT_COLLECTION_ID = "EO.ECMWF.DAT.DESTINE.CLIMATE_ADAPTATION"
EXTREMES_DT_COLLECTION_ID = "EO.ECMWF.DAT.DESTINE.EXTREMES"


@dataclass
class DestineConfig:
    """
    Configuration for connecting EMO to DestinE Harmonised Data Access (HDA).

    - hda_base_url: root of the HDA service
    - stac_base_url: root of the STAC v2 API
    - token: OAuth2 bearer token obtained via DestinE Core Service Platform
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
    - Produces EMO-ready hazard fingerprints for overlay with OI, SMF, GWI, etc.

    The heavy-duty “near-data” workflows remain on the DestinE side.
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
        This is a convenience wrapper; advanced users should consult the official
        DestinE documentation and the STAC specification.
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

    def search_items(
        self,
        collection_id: str,
        datetime_range: Optional[Tuple[datetime, datetime]] = None,
        bbox: Optional[Tuple[float, float, float, float]] = None,
        limit: int = 50,
        query: Optional[Dict[str, Any]] = None,
    ) -> List[DestineItemSummary]:
        """
        Generic STAC search.

        Parameters
        ----------
        collection_id:
            STAC collection identifier (e.g. for Climate DT or Extremes DT).
        datetime_range:
            Optional (start, end) datetime interval.
        bbox:
            Optional spatial bounding box [minx, miny, maxx, maxy].
        limit:
            Maximum number of items to return.
        query:
            Optional STAC "query" structure for advanced filtering.
        """
        url = self._stac_url("search")
        body: Dict[str, Any] = {"collections": [collection_id], "limit": limit}

        if datetime_range is not None:
            start, end = datetime_range
            # RFC3339 interval; HDA expects proper datetime strings.
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
            assets: Dict[str, str] = {}
            for key, value in raw_assets.items():
                if not isinstance(value, dict):
                    continue
                href = value.get("href")
                if not isinstance(href, str):
                    continue
                assets[key] = href
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

        Corresponds to the data portfolio entry `EO.ECMWF.DAT....CLIMATE_ADAPTATION`.
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
        Convenience wrapper for Extremes Digital Twin STAC items.
        """
        return self.search_items(
            collection_id=EXTREMES_DT_COLLECTION_ID,
            datetime_range=datetime_range,
            bbox=bbox,
            limit=limit,
        )

    # ------------------------------------------------------------------
    # Data access helpers (xarray)
    # ------------------------------------------------------------------

    def open_asset_as_xarray(self, href: str) -> xr.Dataset:
        """
        Open a DestinE DT asset as an xarray Dataset.

        In practice this will often be a NetCDF or Zarr store mounted within
        the HDA / near-data compute environment.
        """
        LOG.info("Opening DestinE asset %s with xarray", href)
        ds = xr.open_dataset(href)
        return ds

    def download_asset(
        self,
        href: str,
        target_path: Path,
        chunk_size: int = 1024 * 1024,
    ) -> Path:
        """
        Stream a DT asset to local disk.

        This is mainly intended for small test slices rather than full production
        pipelines, which should run near-data.
        """
        LOG.info("Downloading DestinE asset %s to %s", href, target_path)
        resp = self.session.get(href, stream=True, timeout=self.config.timeout)
        resp.raise_for_status()

        target_path.parent.mkdir(parents=True, exist_ok=True)
        with target_path.open("wb") as f:
            for chunk in resp.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)

        return target_path


def _parse_rfc3339(value: Any) -> Optional[datetime]:
    """
    Parse a RFC3339 datetime string, returning None if parsing fails.
    """
    if not value or not isinstance(value, str):
        return None
    try:
        # xarray / pandas handle timezone-naive ISO8601 reasonably
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except Exception:
        return None


def destine_items_to_dataframe(items: Iterable[DestineItemSummary]) -> pd.DataFrame:
    """
    Convert a list of DestineItemSummary objects into a tabular dataframe.
    """
    rows = []
    for item in items:
        rows.append(
            {
                "id": item.id,
                "collection_id": item.collection_id,
                "start_datetime": item.start_datetime,
                "end_datetime": item.end_datetime,
                "geometry": item.geometry,
                "assets": item.assets,
            }
        )
    return pd.DataFrame(rows)


def summarise_variable_statistics(
    ds: xr.Dataset | xr.DataArray,
    variables: Optional[Iterable[str]] = None,
    dims: Optional[Iterable[str]] = None,
) -> pd.DataFrame:
    """Compute simple summary statistics for variables in a DestinE dataset.

    This helper collapses the selected dimensions (or all dimensions, if
    ``dims`` is ``None``) to produce a single row of statistics per variable.

    Parameters
    ----------
    ds:
        Input :class:`xarray.Dataset` or :class:`xarray.DataArray` coming from a
        DestinE DT asset.
    variables:
        Optional iterable of variable names to summarise. If omitted, all
        numeric data variables in ``ds`` are used.
    dims:
        Optional iterable of dimension names to reduce over. If omitted, all
        dimensions of each variable are reduced.

    Returns
    -------
    pandas.DataFrame
        One row per variable with columns: ``variable``, ``mean``, ``std``,
        ``min``, ``max``, ``count``.
    """
    # Normalise input to a Dataset
    if isinstance(ds, xr.DataArray):
        name = ds.name or "value"
        ds = ds.to_dataset(name=name)

    if variables is None:
        var_names: List[str] = [
            name
            for name, da in ds.data_vars.items()
            if getattr(getattr(da, "dtype", None), "kind", "") in {"i", "u", "f"}
        ]
    else:
        var_names = list(variables)

    dims_list: Optional[List[str]] = list(dims) if dims is not None else None

    rows: List[Dict[str, Any]] = []
    for name in var_names:
        if name not in ds.data_vars:
            # Be forgiving – callers may pass a superset of variables.
            continue
        da = ds.data_vars[name]

        if dims_list is None:
            reduce_dims = None  # xarray: reduce over all dimensions
        else:
            # Only keep dimensions that are present in this DataArray.
            reduce_dims = [d for d in dims_list if d in da.dims] or None

        mean_da = da.mean(dim=reduce_dims, skipna=True)
        std_da = da.std(dim=reduce_dims, skipna=True)
        min_da = da.min(dim=reduce_dims, skipna=True)
        max_da = da.max(dim=reduce_dims, skipna=True)
        count_da = da.count(dim=reduce_dims)

        # xarray returns 0-D arrays; .item() gives us a Python scalar.
        mean = float(mean_da.values.item())
        std = float(std_da.values.item()) if std_da.size else float("nan")
        min_ = float(min_da.values.item())
        max_ = float(max_da.values.item())
        count = int(count_da.values.item())

        rows.append(
            {
                "variable": name,
                "mean": mean,
                "std": std,
                "min": min_,
                "max": max_,
                "count": count,
            }
        )

    return pd.DataFrame(rows)


def build_emo_destine_overlay(
    hazard_df: pd.DataFrame,
    emo_metric_df: pd.DataFrame,
    hazard_time_col: str = "start_datetime",
    emo_time_col: str = "time",
    how: str = "left",
) -> pd.DataFrame:
    """Align DestinE hazards with EMO metrics on a common time axis.

    The function is deliberately simple and opinionated:

    - If the hazard time column is datetime-like and the EMO time column is
      numeric (e.g. a ``year`` field), hazards are grouped by calendar year and
      joined to the EMO metrics on that year.
    - If both columns are datetime-like, they are normalised to dates and
      joined on that date.
    - Otherwise a direct merge between the two columns is performed.

    Parameters
    ----------
    hazard_df:
        Tabular hazard indicators derived from DestinE digital twins –
        typically derived from STAC items or sliced xarray datasets.
    emo_metric_df:
        Tabular EMO metrics (e.g. annual SMF, OI) with a coarse-grained time
        column.
    hazard_time_col:
        Name of the time-like column in ``hazard_df`` (default:
        ``"start_datetime"``).
    emo_time_col:
        Name of the time-like column in ``emo_metric_df`` (default:
        ``"time"``).
    how:
        Merge mode passed to :func:`pandas.merge` (default: ``"left"``).

    Returns
    -------
    pandas.DataFrame
        Combined table with an ``overlay_time`` column plus the original
        hazard and EMO metric fields.
    """

    def _is_datetime_like(s: pd.Series) -> bool:
        return pd.api.types.is_datetime64_any_dtype(s) or pd.api.types.is_datetime64tz_dtype(s)

    def _coerce_datetime(s: pd.Series) -> pd.Series:
        if _is_datetime_like(s):
            return s
        # Avoid converting plain numeric series (e.g. a ``year`` column) into
        # timestamps; those are usually already the coarse time key.
        if pd.api.types.is_numeric_dtype(s):
            return s
        coerced = pd.to_datetime(s, errors="ignore", utc=False)
        return coerced if _is_datetime_like(coerced) else s

    # Work on copies to avoid mutating caller-owned dataframes.
    hazards = hazard_df.copy()
    metrics = emo_metric_df.copy()

    h_time = _coerce_datetime(hazards[hazard_time_col])
    e_time = _coerce_datetime(metrics[emo_time_col])

    h_is_dt = _is_datetime_like(h_time)
    e_is_dt = _is_datetime_like(e_time)

    # Decide how to build the join key.
    if h_is_dt and not e_is_dt:
        # Typical case: hazards have full timestamps; EMO metrics are by year.
        hazards_key = h_time.dt.year
        metrics_key = metrics[emo_time_col]
    elif not h_is_dt and e_is_dt:
        # Less common: EMO metric is timestamped, hazards already coarse.
        hazards_key = hazards[hazard_time_col]
        metrics_key = e_time.dt.year
    elif h_is_dt and e_is_dt:
        # Align on calendar date.
        hazards_key = h_time.dt.normalize()
        metrics_key = e_time.dt.normalize()
    else:
        # Fall back to a direct join on the provided columns.
        hazards_key = hazards[hazard_time_col]
        metrics_key = metrics[emo_time_col]

    overlay_col = "_emo_destine_overlay_time"
    # Be cautious not to overwrite an existing column.
    while overlay_col in hazards.columns or overlay_col in metrics.columns:
        overlay_col = "_" + overlay_col

    hazards[overlay_col] = hazards_key
    metrics[overlay_col] = metrics_key

    merged = hazards.merge(metrics, on=overlay_col, how=how, suffixes=("_hazard", "_emo"))
    merged = merged.rename(columns={overlay_col: "overlay_time"})
    return merged
