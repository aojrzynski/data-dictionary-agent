from data_dictionary_agent.semantic_inference import infer_semantic_metadata


def _cp(name: str, inferred_type: str, uniqueness: float, distinct: int = 10, non_null: int = 10, samples=None):
    return {
        "column_name": name,
        "normalised_column_name": name,
        "inferred_physical_type": inferred_type,
        "uniqueness_ratio": uniqueness,
        "distinct_count": distinct,
        "non_null_count": non_null,
        "sample_values": samples or [],
    }


def test_identifier_high_confidence_contact_id():
    r = infer_semantic_metadata(_cp("contact_id", "text", 1.0, samples=["C1001", "C1002"]))
    assert r["semantic_role"] == "identifier"
    assert r["semantic_role_confidence"] == "high"
    assert r["review_required"] is False


def test_identifier_review_for_non_unique_account_id():
    r = infer_semantic_metadata(_cp("account_id", "text", 0.4, distinct=4, non_null=10))
    assert r["semantic_role"] == "identifier"
    assert r["review_required"] is True


def test_date_roles_and_numeric_measure_and_category_and_free_text():
    assert infer_semantic_metadata(_cp("created_date", "date_or_datetime", 0.2))["semantic_role"] == "date"
    assert infer_semantic_metadata(_cp("last_modified_date", "date_or_datetime", 0.3))["semantic_role"] == "date"
    assert infer_semantic_metadata(_cp("quantity", "integer", 0.2))["semantic_role"] == "numeric_measure"
    assert infer_semantic_metadata(_cp("total_amount", "decimal", 0.8))["semantic_role"] == "numeric_measure"
    assert infer_semantic_metadata(_cp("status", "text", 0.1, distinct=2, non_null=20))["semantic_role"] == "categorical"
    assert infer_semantic_metadata(_cp("lead_source", "text", 0.2, distinct=3, non_null=20))["semantic_role"] == "categorical"
    assert infer_semantic_metadata(_cp("notes", "text", 0.9, distinct=18, non_null=20))["semantic_role"] == "free_text"


def test_sensitive_and_ambiguous_paths():
    email = infer_semantic_metadata(_cp("email", "text", 1.0))
    phone = infer_semantic_metadata(_cp("phone", "text", 1.0))
    assert email["semantic_role"] == "possible_sensitive"
    assert email["review_required"] is True
    assert phone["semantic_role"] == "possible_sensitive"
    assert phone["review_required"] is True

    generic = infer_semantic_metadata(_cp("value", "text", 0.3, distinct=6, non_null=10))
    assert generic["review_required"] is True

    mixed = infer_semantic_metadata(_cp("mystery", "mixed_or_unknown", 0.3, distinct=6, non_null=10))
    assert mixed["review_required"] is True
