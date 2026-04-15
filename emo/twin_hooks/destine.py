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
        Input Dataset or DataArray coming from a DestinE DT asset.
    variables:
        Optional iterable of variable names to summarise. If omitted, all
        numeric data variables in ``ds`` are used.
    dims:
        Optional iterable of dimension names to reduce over. If omitted,
        all dimensions of each variable are reduced.

    Returns
    -------
    pandas.DataFrame
        One row per variable with columns:
        ``variable``, ``mean``, ``std``, ``min``, ``max``, ``count``.
    """
    if isinstance(ds, xr.DataArray):
        name = ds.name or "value"
        ds = ds.to_dataset(name=name)

    if variables is None:
        var_names: list[str] = [
            str(name)
            for name, da in ds.data_vars.items()
            if getattr(getattr(da, "dtype", None), "kind", "") in {"i", "u", "f"}
        ]
    else:
        var_names = list(variables)

    dims_list: Optional[list[str]] = list(dims) if dims is not None else None
    rows: list[dict[str, Any]] = []

    for name in var_names:
        if name not in ds.data_vars:
            continue

        da = ds.data_vars[name]

        if dims_list is None:
            reduce_dims = None
        else:
            reduce_dims = [d for d in dims_list if d in da.dims] or None

        mean_da = da.mean(dim=reduce_dims, skipna=True)
        std_da = da.std(dim=reduce_dims, skipna=True)
        min_da = da.min(dim=reduce_dims, skipna=True)
        max_da = da.max(dim=reduce_dims, skipna=True)
        count_da = da.count(dim=reduce_dims)

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
