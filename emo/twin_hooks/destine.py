from __future__ import annotations

import logging
import os
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd
import requests
import xarray as xr

from emo.config import USER_AGENT

LOG = logging.getLogger(__name__)

DESTINE_HDA_DEFAULT = "https://hda-01.destine.eu"
DESTINE_STAC_DEFAULT = "https://hda-01.destine.eu/stac"

CLIMATE_DT_COLLECTION_ID = "EO.ECMWF.DAT.DESTINE.CLIMATE_ADAPTATION"
EXTREMES_DT_COLLECTION_ID = "EO.ECMWF.DAT.DESTINE.EXTREMES"


@dataclass
class DestineConfig:
    """
    Configuration for connecting EMO to DestinE Harmonised Data Access (HDA).
    """

    hda_base_url: str = DESTINE_HDA_DEFAULT
    stac_base_url: str = DESTINE_STAC_DEFAULT
    token: str | None = None
    timeout: int = 30

    @classmethod
    def from_env(cls) -> DestineConfig:
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
    title: str | None
    description: str | None
    keywords: list[str]
    href: str | None


@dataclass
class DestineItemSummary:
    """
    Minimal description of a DestinE STAC item.
    """

    id: str
    collection_id: str
    start_datetime: datetime | None
    end_datetime: datetime | None
    geometry: dict[str, Any] | None
    assets: dict[str, str]


class DestineClient:
    """
    Thin client for the DestinE Harmonised Data Access (HDA) and STAC API.
    """

    def __init__(
        self,
        config: DestineConfig | None = None,
        session: requests.Session | None = None,
    ) -> None:
        self.config = config or DestineConfig.from_env()
        self.session = session or requests.Session()

        headers = {"User-Agent": USER_AGENT}
        if self.config.token:
            headers["Authorization"] = f"Bearer {self.config.token}"
        self.session.headers.update(headers)

    def _stac_url(self, path: str) -> str:
        base = self.config.stac_base_url.rstrip("/")
        return f"{base}/{path.lstrip('/')}"

    def list_collections(self) -> list[DestineCollectionSummary]:
        """
        List all STAC collections visible through HDA and return a simplified summary.
        """
        url = self._stac_url("collections")
        LOG.info("Requesting DestinE STAC collections from %s", url)
        resp = self.session.get(url, timeout=self.config.timeout)
        resp.raise_for_status()
        payload = resp.json()

        collections: list[DestineCollectionSummary] = []
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
        datetime_range: tuple[datetime, datetime] | None = None,
        bbox: tuple[float, float, float, float] | None = None,
        limit: int = 50,
        query: dict[str, Any] | None = None,
    ) -> list[DestineItemSummary]:
        """
        Generic STAC search.
        """
        url = self._stac_url("search")
        body: dict[str, Any] = {"collections": [collection_id], "limit": limit}

        if datetime_range is not None:
            start, end = datetime_range
            body["datetime"] = f"{start.isoformat()}Z/{end.isoformat()}Z"

        if bbox is not None:
            body["bbox"] = list(bbox)

        if query:
            body["query"] = query

        LOG.info("STAC search on %s for collection=%s", url, collection_id)
        resp = self.session.post(url, json=body, timeout=self.config.timeout)
        resp.raise_for_status()
        payload = resp.json()

        items: list[DestineItemSummary] = []
        for feat in payload.get("features", []):
            props = feat.get("properties", {}) or {}
            start_dt = _parse_rfc3339(
                props.get("start_datetime") or props.get("datetime")
            )
            end_dt = _parse_rfc3339(
                props.get("end_datetime") or props.get("datetime")
            )

            raw_assets = feat.get("assets", {}) or {}
            assets: dict[str, str] = {}
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

    def fetch_climate_dt_items(
        self,
        datetime_range: tuple[datetime, datetime] | None = None,
        bbox: tuple[float, float, float, float] | None = None,
        limit: int = 50,
    ) -> list[DestineItemSummary]:
        """
        Convenience wrapper for Climate Change Adaptation Digital Twin STAC items.
        """
        return self.search_items(
            collection_id=CLIMATE_DT_COLLECTION_ID,
            datetime_range=datetime_range,
            bbox=bbox,
            limit=limit,
        )

    def fetch_extremes_dt_items(
        self,
        datetime_range: tuple[datetime, datetime] | None = None,
        bbox: tuple[float, float, float, float] | None = None,
        limit: int = 50,
    ) -> list[DestineItemSummary]:
        """
        Convenience wrapper for Extremes Digital Twin STAC items.
        """
        return self.search_items(
            collection_id=EXTREMES_DT_COLLECTION_ID,
            datetime_range=datetime_range,
            bbox=bbox,
            limit=limit,
        )

    def open_asset_as_xarray(self, href: str) -> xr.Dataset:
        """
        Open a DestinE asset as an xarray Dataset.
        """
        LOG.info("Opening DestinE asset %s with xarray", href)
        return xr.open_dataset(href)

    def download_asset(
        self,
        href: str,
        target_path: Path,
        chunk_size: int = 1024 * 1024,
    ) -> Path:
        """
        Stream a DT asset to local disk.
        """
        LOG.info("Downloading DestinE asset %s to %s", href, target_path)
        resp = self.session.get(href, stream=True, timeout=self.config.timeout)
        resp.raise_for_status()

        target_path.parent.mkdir(parents=True, exist_ok=True)
        with target_path.open("wb") as file_obj:
            for chunk in resp.iter_content(chunk_size=chunk_size):
                if chunk:
                    file_obj.write(chunk)
        return target_path


def _parse_rfc3339(value: Any) -> datetime | None:
    """
    Parse a RFC3339 datetime string, returning None if parsing fails.
    """
    if not value or not isinstance(value, str):
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except Exception:
        return None


def destine_items_to_dataframe(items: Iterable[DestineItemSummary]) -> pd.DataFrame:
    """
    Convert a list of DestineItemSummary objects into a tabular dataframe.
    """
    rows: list[dict[str, Any]] = []
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
    variables: Iterable[str] | None = None,
    dims: Iterable[str] | None = None,
) -> pd.DataFrame:
    """
    Compute simple summary statistics for variables in a DestinE dataset.
    """
    if isinstance(ds, xr.DataArray):
        name = ds.name or "value"
        ds = ds.to_dataset(name=name)

    if variables is None:
        var_names: list[str] = [
            str(name)
            for name, data_array in ds.data_vars.items()
            if getattr(getattr(data_array, "dtype", None), "kind", "") in {"i", "u", "f"}
        ]
    else:
        var_names = list(variables)

    dims_list: list[str] | None = list(dims) if dims is not None else None
    rows: list[dict[str, Any]] = []

    for name in var_names:
        if name not in ds.data_vars:
            continue

        data_array = ds.data_vars[name]

        if dims_list is None:
            reduce_dims = None
        else:
            reduce_dims = [dim for dim in dims_list if dim in data_array.dims] or None

        mean_da = data_array.mean(dim=reduce_dims, skipna=True)
        std_da = data_array.std(dim=reduce_dims, skipna=True)
        min_da = data_array.min(dim=reduce_dims, skipna=True)
        max_da = data_array.max(dim=reduce_dims, skipna=True)
        count_da = data_array.count(dim=reduce_dims)

        rows.append(
            {
                "variable": name,
                "mean": float(mean_da.values.item()),
                "std": float(std_da.values.item()) if std_da.size else float("nan"),
                "min": float(min_da.values.item()),
                "max": float(max_da.values.item()),
                "count": int(count_da.values.item()),
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
    """
    Align DestinE hazards with EMO metrics on a common time axis.
    """

    def _is_datetime_like(series: pd.Series) -> bool:
        return pd.api.types.is_datetime64_any_dtype(
            series
        ) or pd.api.types.is_datetime64tz_dtype(series)

    def _coerce_datetime(series: pd.Series) -> pd.Series:
        if _is_datetime_like(series):
            return series
        if pd.api.types.is_numeric_dtype(series):
            return series
        coerced = pd.to_datetime(series, errors="ignore", utc=False)
        return coerced if _is_datetime_like(coerced) else series

    hazards = hazard_df.copy()
    metrics = emo_metric_df.copy()

    h_time = _coerce_datetime(hazards[hazard_time_col])
    e_time = _coerce_datetime(metrics[emo_time_col])

    h_is_dt = _is_datetime_like(h_time)
    e_is_dt = _is_datetime_like(e_time)

    if h_is_dt and not e_is_dt:
        hazards_key = h_time.dt.year
        metrics_key = metrics[emo_time_col]
    elif not h_is_dt and e_is_dt:
        hazards_key = hazards[hazard_time_col]
        metrics_key = e_time.dt.year
    elif h_is_dt and e_is_dt:
        hazards_key = h_time.dt.normalize()
        metrics_key = e_time.dt.normalize()
    else:
        hazards_key = hazards[hazard_time_col]
        metrics_key = metrics[emo_time_col]

    overlay_col = "_emo_destine_overlay_time"
    while overlay_col in hazards.columns or overlay_col in metrics.columns:
        overlay_col = "_" + overlay_col

    hazards[overlay_col] = hazards_key
    metrics[overlay_col] = metrics_key

    merged = hazards.merge(
        metrics,
        on=overlay_col,
        how=how,
        suffixes=("_hazard", "_emo"),
    )
    return merged.rename(columns={overlay_col: "overlay_time"})
