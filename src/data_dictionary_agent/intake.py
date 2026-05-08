from __future__ import annotations

from pathlib import Path

import pandas as pd

SUPPORTED_EXTENSIONS = {".csv", ".xlsx", ".xlsm"}


def load_dataset(input_path: str | Path, sheet: str | None = None) -> tuple[pd.DataFrame, dict]:
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
        df = pd.read_excel(path, sheet_name=sheet if sheet else 0)
        active_sheet = sheet if sheet else "first_sheet"

    metadata = {
        "input_path": str(path),
        "file_name": path.name,
        "file_type": suffix.lstrip("."),
        "sheet_name": active_sheet,
    }
    return df, metadata
