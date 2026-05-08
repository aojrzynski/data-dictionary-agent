from data_dictionary_agent.dictionary_builder import build_data_dictionary


def test_build_data_dictionary_structure_and_required_fields():
    profile = {
        "file_name": "demo.csv",
        "input_path": "demo.csv",
        "file_type": "csv",
        "sheet_name": None,
        "row_count": 2,
        "column_count": 2,
        "generated_at_utc": "2026-01-01T00:00:00+00:00",
        "columns": [
            {
                "column_name": "contact_id",
                "inferred_physical_type": "text",
                "semantic_role": "identifier",
                "semantic_role_confidence": "high",
                "null_count": 0,
                "null_ratio": 0,
                "distinct_count": 2,
                "uniqueness_ratio": 1.0,
                "sample_values": ["C1", "C2"],
                "top_values": [{"value": "C1", "count": 1}],
                "min_value": "C1",
                "max_value": "C2",
                "review_required": False,
                "review_notes": [],
                "notes": [],
            },
            {
                "column_name": "email",
                "inferred_physical_type": "text",
                "semantic_role": "possible_sensitive",
                "semantic_role_confidence": "medium",
                "null_count": 1,
                "null_ratio": 0.5,
                "distinct_count": 1,
                "uniqueness_ratio": 1.0,
                "sample_values": ["a@example.com"],
                "top_values": [{"value": "a@example.com", "count": 1}],
                "min_value": None,
                "max_value": None,
                "review_required": True,
                "review_notes": ["review me"],
                "notes": [],
            },
        ],
    }

    dictionary = build_data_dictionary(profile)
    assert "dataset" in dictionary
    assert len(dictionary["columns"]) == 2
    first = dictionary["columns"][0]
    required = {
        "column_name","display_name","description","description_source","physical_type","semantic_role",
        "semantic_role_confidence","nullable","null_count","null_ratio","distinct_count","uniqueness_ratio",
        "sample_values","top_values","min_value","max_value","review_required","review_notes","caveats",
    }
    assert required.issubset(first.keys())
    assert first["display_name"] == "Contact ID"
    assert first["description_source"] == "deterministic_template"


def test_sensitive_description_and_caveats_and_nullable_rule():
    profile = {
        "file_name": "demo.csv",
        "input_path": "demo.csv",
        "file_type": "csv",
        "sheet_name": None,
        "row_count": 1,
        "column_count": 1,
        "generated_at_utc": "2026-01-01T00:00:00+00:00",
        "columns": [
            {
                "column_name": "email",
                "inferred_physical_type": "mixed_or_unknown",
                "semantic_role": "possible_sensitive",
                "semantic_role_confidence": "low",
                "null_count": 1,
                "null_ratio": 1,
                "distinct_count": 0,
                "uniqueness_ratio": 0,
                "sample_values": [],
                "top_values": [],
                "min_value": None,
                "max_value": None,
                "review_required": True,
                "review_notes": ["name suggests personal data"],
                "notes": ["Column contains multiple value patterns."],
            }
        ],
    }
    entry = build_data_dictionary(profile)["columns"][0]
    assert "possible personal or contact data" in entry["description"]
    assert entry["nullable"] is True
    assert any("classification requires human review" in c for c in entry["caveats"])
    assert any("semantic confidence is low" in c for c in entry["caveats"])
