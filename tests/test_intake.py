from pathlib import Path

import pytest

from data_dictionary_agent.intake import load_dataset


def test_csv_intake_works():
    df, metadata = load_dataset("sample_data/crm_contacts/contacts_clean.csv")
    assert not df.empty
    assert metadata["file_type"] == "csv"


def test_unsupported_type_raises_clear_error(tmp_path: Path):
    file_path = tmp_path / "bad.txt"
    file_path.write_text("hello", encoding="utf-8")
    with pytest.raises(ValueError, match="Unsupported file type"):
        load_dataset(file_path)


def test_missing_file_raises_clear_error():
    with pytest.raises(FileNotFoundError, match="does not exist"):
        load_dataset("sample_data/does_not_exist.csv")
