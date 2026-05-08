from pathlib import Path

import pandas as pd
import pytest

from data_dictionary_agent.intake import load_dataset


def test_csv_intake_works():
    df, metadata = load_dataset("sample_data/crm_contacts/contacts_clean.csv")
    assert not df.empty
    assert metadata["file_type"] == "csv"


def test_excel_named_sheet_intake_works(tmp_path: Path):
    file_path = tmp_path / "workbook.xlsx"
    first_df = pd.DataFrame({"id": [1, 2], "name": ["a", "b"]})
    second_df = pd.DataFrame({"id": [10], "name": ["target"]})

    with pd.ExcelWriter(file_path) as writer:
        first_df.to_excel(writer, sheet_name="FirstSheet", index=False)
        second_df.to_excel(writer, sheet_name="TargetSheet", index=False)

    df, metadata = load_dataset(file_path, sheet="TargetSheet")
    assert df.shape == (1, 2)
    assert df.iloc[0]["name"] == "target"
    assert metadata["file_type"] == "xlsx"
    assert metadata["sheet_name"] == "TargetSheet"


def test_excel_default_loads_first_sheet_and_records_real_name(tmp_path: Path):
    file_path = tmp_path / "workbook.xlsx"
    first_df = pd.DataFrame({"id": [1, 2], "name": ["first", "sheet"]})
    second_df = pd.DataFrame({"id": [3], "name": ["second"]})

    with pd.ExcelWriter(file_path) as writer:
        first_df.to_excel(writer, sheet_name="Alpha", index=False)
        second_df.to_excel(writer, sheet_name="Beta", index=False)

    df, metadata = load_dataset(file_path)
    assert df.shape == (2, 2)
    assert df.iloc[0]["name"] == "first"
    assert metadata["file_type"] == "xlsx"
    assert metadata["sheet_name"] == "Alpha"


def test_unsupported_type_raises_clear_error(tmp_path: Path):
    file_path = tmp_path / "bad.txt"
    file_path.write_text("hello", encoding="utf-8")
    with pytest.raises(ValueError, match="Unsupported file type"):
        load_dataset(file_path)


def test_missing_file_raises_clear_error():
    with pytest.raises(FileNotFoundError, match="does not exist"):
        load_dataset("sample_data/does_not_exist.csv")
