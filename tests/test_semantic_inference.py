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


def test_identifier_review_for_non_unique_account_id_and_code_review():
    r = infer_semantic_metadata(_cp("account_id", "text", 0.4, distinct=4, non_null=10))
    assert r["semantic_role"] == "identifier"
    assert r["review_required"] is True

    code = infer_semantic_metadata(_cp("product_code", "text", 0.98, distinct=98, non_null=100))
    assert code["semantic_role"] == "identifier"
    assert code["review_required"] is True


def test_identifier_false_positive_guards():
    assert infer_semantic_metadata(_cp("paid_amount", "decimal", 0.2))["semantic_role"] == "numeric_measure"
    assert infer_semantic_metadata(_cp("grid_voltage", "text", 0.6))["semantic_role"] != "identifier"
    assert infer_semantic_metadata(_cp("valid_from", "date_or_datetime", 0.2))["semantic_role"] == "date"


def test_date_roles_and_datetime():
    assert infer_semantic_metadata(_cp("created_date", "date_or_datetime", 0.2))["semantic_role"] == "date"
    assert infer_semantic_metadata(_cp("last_modified_date", "date_or_datetime", 0.3))["semantic_role"] == "date"
    assert (
        infer_semantic_metadata(
            _cp("updated_at", "date_or_datetime", 0.8, samples=["2024-01-01T10:30:00", "2024-01-01 10:30:00"])
        )["semantic_role"]
        == "datetime"
    )


def test_numeric_category_and_free_text():
    assert infer_semantic_metadata(_cp("quantity", "integer", 0.2))["semantic_role"] == "numeric_measure"
    assert infer_semantic_metadata(_cp("total_amount", "decimal", 0.8))["semantic_role"] == "numeric_measure"
    assert infer_semantic_metadata(_cp("status", "text", 0.1, distinct=2, non_null=20))["semantic_role"] == "categorical"
    assert infer_semantic_metadata(_cp("lead_source", "text", 0.2, distinct=3, non_null=20))["semantic_role"] == "categorical"
    assert infer_semantic_metadata(_cp("notes", "text", 0.9, distinct=18, non_null=20))["semantic_role"] == "free_text"


def test_sensitive_precision_and_ambiguous_paths():
    first_name = infer_semantic_metadata(_cp("first_name", "text", 0.5))
    email = infer_semantic_metadata(_cp("email", "text", 1.0))
    assert first_name["semantic_role"] == "possible_sensitive"
    assert first_name["review_required"] is True
    assert email["semantic_role"] == "possible_sensitive"
    assert email["review_required"] is True

    assert infer_semantic_metadata(_cp("asset_name", "text", 0.9))["semantic_role"] != "possible_sensitive"
    assert infer_semantic_metadata(_cp("product_name", "text", 0.9))["semantic_role"] != "possible_sensitive"
    assert infer_semantic_metadata(_cp("file_name", "text", 0.9))["semantic_role"] != "possible_sensitive"

    generic = infer_semantic_metadata(_cp("value", "text", 0.3, distinct=6, non_null=10))
    assert generic["review_required"] is True

    mixed = infer_semantic_metadata(_cp("mystery", "mixed_or_unknown", 0.3, distinct=6, non_null=10))
    assert mixed["review_required"] is True
