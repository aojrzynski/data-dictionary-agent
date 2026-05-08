from __future__ import annotations

from typing import Any

GENERIC_NAMES = {"code", "type", "value", "date", "description", "flag"}
IDENTIFIER_HINTS = ("id", "_id", "identifier", "code", "ref", "reference", "key")
DATE_HINTS = ("date", "created", "modified", "updated", "timestamp", "time", "datetime", "_at")
MEASURE_HINTS = (
    "amount",
    "total",
    "price",
    "cost",
    "quantity",
    "count",
    "number",
    "score",
    "rate",
    "percent",
    "percentage",
    "value",
)
CATEGORY_HINTS = ("status", "type", "category", "source", "region", "country", "department", "criticality")
FREE_TEXT_HINTS = ("notes", "comments", "description", "details", "summary")
SENSITIVE_HINTS = (
    "email",
    "phone",
    "mobile",
    "name",
    "first_name",
    "last_name",
    "full_name",
    "address",
    "postcode",
    "zip",
    "dob",
    "date_of_birth",
    "ssn",
    "national_insurance",
    "ni_number",
)


def _contains_any(text: str, hints: tuple[str, ...]) -> bool:
    return any(h in text for h in hints)


def infer_semantic_metadata(column_profile: dict[str, Any]) -> dict[str, Any]:
    name = str(column_profile.get("normalised_column_name") or column_profile.get("column_name", "")).lower()
    inferred_physical_type = column_profile.get("inferred_physical_type", "unknown")
    uniqueness_ratio = float(column_profile.get("uniqueness_ratio", 0.0) or 0.0)
    distinct_count = int(column_profile.get("distinct_count", 0) or 0)
    non_null_count = int(column_profile.get("non_null_count", 0) or 0)
    sample_values = [str(v) for v in column_profile.get("sample_values", [])]

    reasons: list[str] = []
    review_notes: list[str] = []

    role = "unknown"
    confidence = "low"

    if _contains_any(name, SENSITIVE_HINTS):
        role = "possible_sensitive"
        confidence = "medium"
        reasons.append("Column name suggests possible personal/contact data.")
        review_notes.append("Column name suggests possible personal/contact data. Review required before sharing externally.")
    elif inferred_physical_type == "boolean" or _contains_any(name, ("is_", "has_", "flag", "active", "enabled", "yes_no")):
        role = "boolean_flag"
        confidence = "high" if inferred_physical_type == "boolean" else "medium"
        reasons.append("Values/pattern align with boolean semantics.")
    elif inferred_physical_type == "date_or_datetime" or _contains_any(name, DATE_HINTS):
        has_time = any(("T" in v or ":" in v) for v in sample_values)
        role = "datetime" if has_time else "date"
        confidence = "high" if inferred_physical_type == "date_or_datetime" else "medium"
        reasons.append(f"Physical type is {inferred_physical_type}.")
    elif (
        _contains_any(name, IDENTIFIER_HINTS)
        and inferred_physical_type in {"text", "integer", "decimal"}
    ) or any(any(ch.isalpha() for ch in v) and any(ch.isdigit() for ch in v) for v in sample_values):
        role = "identifier"
        if uniqueness_ratio >= 0.95:
            confidence = "high"
            reasons.append(f"Uniqueness ratio is {uniqueness_ratio}.")
        else:
            confidence = "medium"
            reasons.append("Column name/value pattern looks identifier-like.")
            review_notes.append("Identifier-like field is not highly unique; could be a foreign key or repeated reference.")
    elif inferred_physical_type in {"integer", "decimal"} and _contains_any(name, MEASURE_HINTS):
        role = "numeric_measure"
        confidence = "high"
        reasons.append("Numeric physical type and measure-like column name.")
    elif inferred_physical_type == "text" and _contains_any(name, FREE_TEXT_HINTS):
        role = "free_text"
        confidence = "medium" if uniqueness_ratio >= 0.7 else "low"
        reasons.append("Column name suggests descriptive free-text content.")
    elif inferred_physical_type == "text" and (
        _contains_any(name, CATEGORY_HINTS)
        or (non_null_count > 0 and distinct_count / non_null_count <= 0.2)
    ):
        role = "categorical"
        confidence = "high" if non_null_count > 0 and distinct_count / non_null_count <= 0.2 else "medium"
        reasons.append("Low distinct count or category-like name suggests categorical field.")

    if role == "unknown":
        reasons.append("No strong deterministic semantic signal detected.")

    review_required = False
    if confidence == "low" or role in {"unknown", "possible_sensitive"}:
        review_required = True
    if role == "identifier" and uniqueness_ratio < 0.95:
        review_required = True
    if name in GENERIC_NAMES:
        review_required = True
        review_notes.append("Generic column name may hide ambiguous business meaning.")
    if inferred_physical_type == "mixed_or_unknown":
        review_required = True
        review_notes.append("Physical type is mixed_or_unknown.")

    if not reasons:
        reasons.append("Semantic role inferred from deterministic profile evidence.")

    return {
        "semantic_role": role,
        "semantic_role_confidence": confidence,
        "semantic_role_reasons": reasons,
        "review_required": review_required,
        "review_notes": review_notes,
    }
