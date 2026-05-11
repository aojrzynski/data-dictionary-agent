from data_dictionary_agent.output_writers import write_suggested_overrides_yaml
from data_dictionary_agent.suggested_overrides import build_suggested_overrides


def test_unknown_and_sensitive_appear_in_suggestions(tmp_path):
    dictionary = {"dataset": {"source_file": "x.csv"}, "columns": [
        {"column_name": "a", "display_name": "A", "description": "", "description_source": "blank_review_required", "semantic_role": "unknown", "semantic_role_confidence": "low", "review_required": True, "review_notes": [], "caveats": []},
        {"column_name": "email", "display_name": "Email", "description": "d", "description_source": "deterministic_template", "semantic_role": "possible_sensitive", "semantic_role_confidence": "medium", "review_required": True, "review_notes": [], "caveats": []},
    ]}
    s = build_suggested_overrides(dictionary)
    assert "a" in s["columns"] and "email" in s["columns"]
    p = write_suggested_overrides_yaml(s, tmp_path)
    assert p.exists()


def test_clean_dictionary_produces_empty_columns():
    s = build_suggested_overrides({"dataset": {"source_file": "x.csv"}, "columns": []})
    assert s["columns"] == {}
