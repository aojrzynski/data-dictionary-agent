import json

from data_dictionary_agent.llm_descriptions import build_llm_safe_summary, generate_llm_description_suggestions


def _dictionary():
    return {
        "dataset": {"source_file": "contacts_clean.csv"},
        "columns": [
            {"column_name": "email", "display_name": "Email", "physical_type": "string", "semantic_role": "possible_sensitive", "semantic_role_confidence": "medium", "null_ratio": 0.1, "distinct_count": 10, "uniqueness_ratio": 1.0, "description": "", "description_source": "blank_review_required", "review_required": True, "review_notes": [], "caveats": [], "sample_values": ["a@b.com"], "top_values": [{"value": "x", "count": 1}]},
            {"column_name": "status", "display_name": "Status", "physical_type": "string", "semantic_role": "categorical", "semantic_role_confidence": "high", "null_ratio": 0.0, "distinct_count": 3, "uniqueness_ratio": 0.1, "description": "Current status", "description_source": "config_override", "review_required": False, "review_notes": [], "caveats": [], "sample_values": ["active", "inactive", "pending", "other"], "top_values": [{"value": "active" ,"count": 9},{"value":"inactive","count":2},{"value":"pending","count":1},{"value":"other","count":1}]},
        ],
    }


def test_safe_summary_redacts_sensitive_and_caps_non_sensitive():
    safe = build_llm_safe_summary(_dictionary())
    assert next(c for c in safe["columns"] if c["column_name"] == "email")["sample_values"] == ["[REDACTED_POSSIBLE_SENSITIVE]"]
    status = next(c for c in safe["columns"] if c["column_name"] == "status")
    assert len(status["sample_values"]) == 3
    assert len(status["top_values"]) == 3


def test_full_fallback_when_no_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    _, suggestions = generate_llm_description_suggestions(_dictionary())
    assert suggestions["llm_requested"] is True
    assert suggestions["llm_used"] is False
    assert suggestions["source"] == "deterministic_fallback"


def test_invalid_json_is_explicit_fallback():
    class FakeResp: output_text = "not-json"
    class FakeClient:
        class responses:
            @staticmethod
            def create(**kwargs): return FakeResp()

    _, suggestions = generate_llm_description_suggestions(_dictionary(), client=FakeClient())
    assert suggestions["llm_call_succeeded"] is True
    assert suggestions["llm_used"] is False
    assert suggestions["source"] == "deterministic_fallback"
    assert any("could not be parsed as valid JSON" in w for w in suggestions["warnings"])


def test_raw_valid_json_is_used():
    payload = {"columns": [{"column_name": "status", "suggested_description": "Status of contact.", "confidence": "medium", "notes": []}]}
    client = type("C", (), {"responses": type("R", (), {"create": staticmethod(lambda **kwargs: type("X", (), {"output_text": json.dumps(payload)})())})})()
    _, suggestions = generate_llm_description_suggestions(_dictionary(), client=client)
    assert suggestions["source"] == "llm_suggested"
    assert suggestions["llm_used"] is True
    assert all(c["review_required"] is True for c in suggestions["columns"])


def test_fenced_json_is_used():
    payload = {"columns": [{"column_name": "status", "suggested_description": "Status of contact.", "confidence": "medium", "notes": []}]}
    wrapped = f"```json\n{json.dumps(payload)}\n```"
    client = type("C", (), {"responses": type("R", (), {"create": staticmethod(lambda **kwargs: type("X", (), {"output_text": wrapped})())})})()
    _, suggestions = generate_llm_description_suggestions(_dictionary(), client=client)
    assert suggestions["source"] == "llm_suggested"
    assert suggestions["llm_used"] is True
    assert all(c["review_required"] is True for c in suggestions["columns"])


def test_text_wrapped_json_is_used():
    payload = {"columns": [{"column_name": "status", "suggested_description": "Status of contact.", "confidence": "medium", "notes": []}]}
    wrapped = f"Here is the JSON:\n{json.dumps(payload)}\nThanks."
    client = type("C", (), {"responses": type("R", (), {"create": staticmethod(lambda **kwargs: type("X", (), {"output_text": wrapped})())})})()
    _, suggestions = generate_llm_description_suggestions(_dictionary(), client=client)
    assert suggestions["source"] == "llm_suggested"
    assert suggestions["llm_used"] is True
    assert all(c["review_required"] is True for c in suggestions["columns"])
