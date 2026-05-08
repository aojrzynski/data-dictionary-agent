from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone

import pandas as pd

PROFILER_VERSION = "0.1.0"


TRUE_VALUES = {"true", "t", "yes", "y", "1"}
FALSE_VALUES = {"false", "f", "no", "n", "0"}


def _normalise_column_name(name: str) -> str:
    return "_".join(str(name).strip().lower().split())


def _clean_series_for_nulls(series: pd.Series) -> pd.Series:
    if series.dtype == object:
        s = series.apply(lambda x: x.strip() if isinstance(x, str) else x)
        s = s.replace("", pd.NA)
        return s
    return series


def _infer_physical_type(series: pd.Series) -> str:
    s = _clean_series_for_nulls(series)
    non_null = s.dropna()
    if non_null.empty:
        return "empty"

    if pd.api.types.is_integer_dtype(non_null):
        return "integer"
    if pd.api.types.is_float_dtype(non_null):
        return "decimal"
    if pd.api.types.is_bool_dtype(non_null):
        return "boolean"
    if pd.api.types.is_datetime64_any_dtype(non_null):
        return "date_or_datetime"

    if non_null.dtype == object:
        lowered = [str(v).strip().lower() for v in non_null]
        unique_vals = set(lowered)
        if unique_vals and unique_vals.issubset(TRUE_VALUES | FALSE_VALUES):
            return "boolean"

        numeric = pd.to_numeric(non_null, errors="coerce")
        if numeric.notna().all():
            if (numeric % 1 == 0).all():
                return "integer"
            return "decimal"

        parsed_dates = pd.to_datetime(non_null, errors="coerce")
        if parsed_dates.notna().mean() >= 0.8:
            return "date_or_datetime"

        kinds = Counter()
        for value in non_null:
            sval = str(value).strip()
            if not sval:
                continue
            if pd.to_numeric(pd.Series([sval]), errors="coerce").notna().all():
                kinds["numeric"] += 1
            elif pd.to_datetime(pd.Series([sval]), errors="coerce").notna().all():
                kinds["date"] += 1
            else:
                kinds["text"] += 1

        if len(kinds) > 1:
            return "mixed_or_unknown"
        return "text"

    return "mixed_or_unknown"


def build_profile(
    df: pd.DataFrame,
    metadata: dict,
    sample_size: int = 5,
    top_values_limit: int = 5,
) -> dict:
    column_profiles = []

    for column in df.columns:
        raw_series = df[column]
        s = _clean_series_for_nulls(raw_series)

        non_null_count = int(s.notna().sum())
        null_count = int(s.isna().sum())
        row_count = len(s)
        distinct_count = int(s.dropna().nunique())

        non_null_values = s.dropna().tolist()
        sample_values = [str(v) for v in non_null_values[:sample_size]]

        top_counts = s.dropna().astype(str).value_counts().head(top_values_limit)
        top_values = [{"value": idx, "count": int(cnt)} for idx, cnt in top_counts.items()]

        min_value = None
        max_value = None
        try:
            non_null = s.dropna()
            if not non_null.empty:
                min_value = non_null.min()
                max_value = non_null.max()
        except Exception:
            pass

        notes = []
        inferred = _infer_physical_type(raw_series)
        if inferred == "mixed_or_unknown":
            notes.append("Column contains multiple value patterns.")

        column_profiles.append(
            {
                "column_name": str(column),
                "normalised_column_name": _normalise_column_name(str(column)),
                "pandas_dtype": str(raw_series.dtype),
                "inferred_physical_type": inferred,
                "non_null_count": non_null_count,
                "null_count": null_count,
                "null_ratio": round(null_count / row_count, 6) if row_count else 0.0,
                "distinct_count": distinct_count,
                "uniqueness_ratio": round(distinct_count / non_null_count, 6)
                if non_null_count
                else 0.0,
                "sample_values": sample_values,
                "top_values": top_values,
                "min_value": None if min_value is None else str(min_value),
                "max_value": None if max_value is None else str(max_value),
                "notes": notes,
            }
        )

    return {
        "input_path": metadata["input_path"],
        "file_name": metadata["file_name"],
        "file_type": metadata["file_type"],
        "sheet_name": metadata["sheet_name"],
        "row_count": len(df),
        "column_count": len(df.columns),
        "column_names": [str(c) for c in df.columns],
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "profiler_version": PROFILER_VERSION,
        "columns": column_profiles,
    }
