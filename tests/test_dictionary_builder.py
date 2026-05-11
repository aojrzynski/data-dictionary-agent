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


def test_config_overrides_apply_without_overwriting_observed_facts():
    profile = {
        "file_name": "demo.csv",
        "input_path": "demo.csv",
        "file_type": "csv",
        "sheet_name": None,
        "row_count": 1,
        "column_count": 1,
        "generated_at_utc": "2026-01-01T00:00:00+00:00",
        "columns": [{
            "column_name": "amount",
            "inferred_physical_type": "numeric",
            "semantic_role": "numeric_measure",
            "semantic_role_confidence": "medium",
            "null_count": 3,
            "null_ratio": 0.3,
            "distinct_count": 7,
            "uniqueness_ratio": 0.7,
            "sample_values": [1],
            "top_values": [],
            "min_value": 1,
            "max_value": 9,
            "review_required": False,
            "review_notes": [],
            "notes": [],
        }],
    }
    config = {"dataset": {}, "columns": {"amount": {"description": "Business amount", "display_name": "Amount USD", "semantic_role": "categorical", "review_notes": ["x"], "caveats": ["c"], "allowed_values": ["A"], "business_rules": ["rule"]}}}
    entry = build_data_dictionary(profile, config=config)["columns"][0]
    assert entry["description"] == "Business amount"
    assert entry["description_source"] == "config_override"
    assert entry["display_name_source"] == "config_override"
    assert entry["semantic_role_source"] == "config_override"
    assert entry["null_count"] == 3 and entry["distinct_count"] == 7
    assert "x" in entry["review_notes"] and "c" in entry["caveats"]
    assert entry["allowed_values"] == ["A"] and entry["business_rules"] == ["rule"]


def test_config_semantic_role_override_sets_default_confidence_and_caveat():
    profile = {"file_name":"d.csv","input_path":"d.csv","file_type":"csv","sheet_name":None,"row_count":1,"column_count":1,"generated_at_utc":"2026-01-01T00:00:00+00:00","columns":[{"column_name":"x","inferred_physical_type":"text","semantic_role":"unknown","semantic_role_confidence":"low","null_count":0,"null_ratio":0,"distinct_count":1,"uniqueness_ratio":1,"sample_values":["a"],"top_values":[],"min_value":"a","max_value":"a","review_required":True,"review_notes":[],"notes":[]}]}
    config = {"dataset": {}, "columns": {"x": {"semantic_role": "categorical", "description": "X desc"}}}
    entry = build_data_dictionary(profile, config=config)["columns"][0]
    assert entry["semantic_role_confidence"] == "medium"
    assert entry["semantic_role_source"] == "config_override"
    assert any("Semantic role was provided by config" in c for c in entry["caveats"])


def test_review_required_not_cleared_by_description_override():
    profile = {"file_name":"d.csv","input_path":"d.csv","file_type":"csv","sheet_name":None,"row_count":1,"column_count":1,"generated_at_utc":"2026-01-01T00:00:00+00:00","columns":[{"column_name":"x","inferred_physical_type":"text","semantic_role":"unknown","semantic_role_confidence":"low","null_count":0,"null_ratio":0,"distinct_count":1,"uniqueness_ratio":1,"sample_values":["a"],"top_values":[],"min_value":"a","max_value":"a","review_required":True,"review_notes":[],"notes":[]}]}
    config = {"dataset": {}, "columns": {"x": {"description": "X desc"}}}
    assert build_data_dictionary(profile, config=config)["columns"][0]["review_required"] is True


def test_explicit_review_required_false_respected():
    profile = {"file_name":"d.csv","input_path":"d.csv","file_type":"csv","sheet_name":None,"row_count":1,"column_count":1,"generated_at_utc":"2026-01-01T00:00:00+00:00","columns":[{"column_name":"x","inferred_physical_type":"text","semantic_role":"unknown","semantic_role_confidence":"low","null_count":0,"null_ratio":0,"distinct_count":1,"uniqueness_ratio":1,"sample_values":["a"],"top_values":[],"min_value":"a","max_value":"a","review_required":True,"review_notes":[],"notes":[]}]}
    config = {"dataset": {}, "columns": {"x": {"description": "X desc", "review_required": False}}}
    assert build_data_dictionary(profile, config=config)["columns"][0]["review_required"] is False
