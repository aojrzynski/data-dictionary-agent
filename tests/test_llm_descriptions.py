import json

from data_dictionary_agent.llm_descriptions import build_llm_safe_summary, generate_llm_description_suggestions


def _dictionary():
    return {
        "dataset": {"source_file": "x.csv"},
        "columns": [
            {"column_name": "email", "display_name": "Email", "physical_type": "string", "semantic_role": "possible_sensitive", "semantic_role_confidence": "medium", "null_ratio": 0.1, "distinct_count": 10, "uniqueness_ratio": 1.0, "description": "", "description_source": "blank_review_required", "review_required": True, "review_notes": [], "caveats": [], "sample_values": ["a@b.com"], "top_values": [{"value": "x", "count": 1}]},
            {"column_name": "status", "display_name": "Status", "physical_type": "string", "semantic_role": "category", "semantic_role_confidence": "high", "null_ratio": 0.0, "distinct_count": 3, "uniqueness_ratio": 0.1, "description": "Current status", "description_source": "config_override", "review_required": False, "review_notes": [], "caveats": [], "sample_values": ["active", "inactive", "pending", "other"], "top_values": [{"value": "active" ,"count": 9},{"value":"inactive","count":2},{"value":"pending","count":1},{"value":"other","count":1}]},
        ],
    }


def test_safe_summary_redacts_sensitive_and_caps_non_sensitive():
    safe = build_llm_safe_summary(_dictionary())
    email = next(c for c in safe["columns"] if c["column_name"] == "email")
    assert email["sample_values"] == ["[REDACTED_POSSIBLE_SENSITIVE]"]
    assert email["top_values"] == []
    status = next(c for c in safe["columns"] if c["column_name"] == "status")
    assert len(status["sample_values"]) == 3
    assert len(status["top_values"]) == 3


def test_fallback_when_no_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    _, suggestions = generate_llm_description_suggestions(_dictionary())
    assert suggestions["llm_used"] is False
    assert suggestions["source"] == "deterministic_fallback"
    assert suggestions["columns"][0]["review_required"] is True


def test_invalid_json_from_client_falls_back():
    class FakeResp:
        output_text = "not-json"

    class FakeClient:
        class responses:
            @staticmethod
            def create(**kwargs):
                return FakeResp()

    _, suggestions = generate_llm_description_suggestions(_dictionary(), client=FakeClient())
    assert suggestions["source"] == "llm_suggested" or suggestions["source"] == "deterministic_fallback"
    assert any("valid JSON" in w for w in suggestions["warnings"])


def test_structure_valid():
    _, suggestions = generate_llm_description_suggestions(_dictionary(), client=type("C", (), {"responses": type("R", (), {"create": staticmethod(lambda **kwargs: type("X", (), {"output_text": json.dumps({"columns": [{"column_name": "status", "suggested_description": "Status of contact", "confidence": "medium", "notes": []}]})})() )})})())
    assert "columns" in suggestions
    assert all("current_description" in c for c in suggestions["columns"])
