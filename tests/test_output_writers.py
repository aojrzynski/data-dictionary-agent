import csv
import json

from data_dictionary_agent.output_writers import write_dictionary_outputs


def test_output_writers_create_artifacts(tmp_path):
    dictionary = {
        "dataset": {"source_file": "demo.csv", "file_type": "csv", "sheet": None, "rows": 2, "columns": 1, "generated_at": "x"},
        "summary_counts": {"columns_needing_review": 1, "possible_sensitive_fields": 0, "identifier_like_fields": 1, "date_datetime_fields": 0, "numeric_measures": 0, "categorical_fields": 0},
        "columns": [
            {
                "column_name": "contact_id",
                "display_name": "Contact ID",
                "description": "Likely identifier field",
                "description_source": "deterministic_template",
                "physical_type": "text",
                "semantic_role": "identifier",
                "semantic_role_confidence": "high",
                "nullable": False,
                "null_count": 0,
                "null_ratio": 0,
                "distinct_count": 2,
                "uniqueness_ratio": 1.0,
                "sample_values": ["C1", "C2"],
                "top_values": [{"value": "C1", "count": 1}],
                "min_value": "C1",
                "max_value": "C2",
                "review_required": True,
                "review_notes": ["check"],
                "caveats": ["note"],
            }
        ],
    }
    paths = write_dictionary_outputs(dictionary, tmp_path)
    assert paths["data_dictionary_md"].exists()
    assert paths["data_dictionary_csv"].exists()
    assert paths["data_dictionary_json"].exists()

    with paths["data_dictionary_csv"].open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
    assert "column_name" in headers
    assert "display_name" in headers

    loaded = json.loads(paths["data_dictionary_json"].read_text(encoding="utf-8"))
    assert loaded["columns"][0]["column_name"] == "contact_id"

    md = paths["data_dictionary_md"].read_text(encoding="utf-8")
    assert "## Dataset summary" in md
    assert "## Fields needing review" in md
