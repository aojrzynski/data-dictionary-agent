"""Dataset intake utilities for local CSV/XLSX/XLSM files.

This module validates file paths and loads tabular data into pandas plus basic
source metadata. It does not profile values, infer semantics, or apply config.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

SUPPORTED_EXTENSIONS = {".csv", ".xlsx", ".xlsm"}


def load_dataset(input_path: str | Path, sheet: str | None = None) -> tuple[pd.DataFrame, dict]:
    """Load a supported tabular file and return (dataframe, source metadata)."""
    path = Path(input_path)

    if not path.exists():
        raise FileNotFoundError(f"Input file does not exist: {path}")
    if not path.is_file():
        raise ValueError(f"Input path is not a file: {path}")

    suffix = path.suffix.lower()
    if suffix not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file type '{suffix}'. Supported types: .csv, .xlsx, .xlsm"
        )

    if suffix == ".csv":
        df = pd.read_csv(path)
        active_sheet = None
    else:
        excel_file = pd.ExcelFile(path)
        active_sheet = sheet if sheet else excel_file.sheet_names[0]
        df = pd.read_excel(excel_file, sheet_name=active_sheet)

    metadata = {
        "input_path": str(path),
        "file_name": path.name,
        "file_type": suffix.lstrip("."),
        "sheet_name": active_sheet,
    }
    return df, metadata
