import pandas as pd

from data_dictionary_agent.profiling import build_profile


def test_profile_dataset_counts():
    df = pd.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})
    metadata = {
        "input_path": "dummy.csv",
        "file_name": "dummy.csv",
        "file_type": "csv",
        "sheet_name": None,
    }
    profile = build_profile(df, metadata)
    assert profile["row_count"] == 3
    assert profile["column_count"] == 2
    assert profile["column_names"] == ["a", "b"]


def test_column_profile_fields_and_type_detection():
    df = pd.DataFrame(
        {
            "int_col": [1, 2, None],
            "dec_col": [1.1, 2.2, None],
            "bool_col": ["yes", "no", "yes"],
            "date_col": ["2024-01-01", "2024-01-02", None],
            "text_col": ["alpha", "beta", "alpha"],
            "empty_col": [" ", "", None],
        }
    )
    metadata = {
        "input_path": "dummy.csv",
        "file_name": "dummy.csv",
        "file_type": "csv",
        "sheet_name": None,
    }
    profile = build_profile(df, metadata, sample_size=2, top_values_limit=2)
    by_name = {col["column_name"]: col for col in profile["columns"]}

    assert by_name["int_col"]["inferred_physical_type"] == "integer"
    assert by_name["dec_col"]["inferred_physical_type"] == "decimal"
    assert by_name["bool_col"]["inferred_physical_type"] == "boolean"
    assert by_name["date_col"]["inferred_physical_type"] == "date_or_datetime"
    assert by_name["text_col"]["inferred_physical_type"] == "text"
    assert by_name["empty_col"]["inferred_physical_type"] == "empty"

    assert by_name["text_col"]["null_count"] == 0
    assert by_name["text_col"]["distinct_count"] == 2
    assert len(by_name["text_col"]["sample_values"]) == 2
