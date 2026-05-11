"""Deterministic semantic suggestion rules for profiled columns.

This module maps observed profile facts and column-name hints to likely
semantic roles. These are suggestions, not confirmed business definitions.
"""

from __future__ import annotations

import re
from typing import Any

GENERIC_NAMES = {"code", "type", "value", "date", "description", "flag"}
DATE_HINT_TOKENS = {"date", "created", "modified", "updated", "timestamp", "time", "datetime"}
MEASURE_HINTS = {
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
}
CATEGORY_HINTS = {"status", "type", "category", "source", "region", "country", "department", "criticality"}
FREE_TEXT_HINTS = {"notes", "comments", "description", "details", "summary"}
PERSON_CONTEXT_TOKENS = {"person", "contact", "customer", "employee"}


def _tokenise_column_name(normalised_name: str) -> list[str]:
    return [t for t in re.split(r"[^a-z0-9]+", normalised_name.lower()) if t]


def _is_identifier_name(name: str, tokens: list[str]) -> tuple[bool, bool]:
    has_generic_code = False
    if name.endswith("_id") or "id" in tokens:
        return True, has_generic_code
    if any(t in {"identifier", "ref", "reference", "key"} for t in tokens):
        return True, has_generic_code
    if "code" in tokens:
        has_generic_code = True
        return True, has_generic_code
    return False, has_generic_code


def _is_possible_sensitive_name(name: str, tokens: list[str]) -> bool:
    joined = "_".join(tokens)
    direct = {
        "email",
        "phone",
        "mobile",
        "first_name",
        "last_name",
        "full_name",
        "contact_name",
        "customer_name",
        "person_name",
        "employee_name",
        "address",
        "postcode",
        "zip",
        "dob",
        "date_of_birth",
        "ssn",
        "national_insurance",
        "ni_number",
        "name",
    }
    if joined in direct:
        return True
    if "name" in tokens and any(t in PERSON_CONTEXT_TOKENS for t in tokens):
        return True
    return False


def infer_semantic_metadata(column_profile: dict[str, Any]) -> dict[str, Any]:
    """Infer semantic hints from one column profile using deterministic rules."""
    name = str(column_profile.get("normalised_column_name") or column_profile.get("column_name", "")).lower()
    tokens = _tokenise_column_name(name)
    inferred_physical_type = column_profile.get("inferred_physical_type", "unknown")
    uniqueness_ratio = float(column_profile.get("uniqueness_ratio", 0.0) or 0.0)
    distinct_count = int(column_profile.get("distinct_count", 0) or 0)
    non_null_count = int(column_profile.get("non_null_count", 0) or 0)
    sample_values = [str(v) for v in column_profile.get("sample_values", [])]

    reasons: list[str] = []
    review_notes: list[str] = []

    role = "unknown"
    confidence = "low"

    if _is_possible_sensitive_name(name, tokens):
        role = "possible_sensitive"
        confidence = "medium"
        reasons.append("Column name suggests possible personal/contact data.")
        review_notes.append("Column name suggests possible personal/contact data. Review required before sharing externally.")
    elif inferred_physical_type == "boolean" or any(t in {"is", "has", "flag", "active", "enabled", "yes_no"} for t in tokens):
        role = "boolean_flag"
        confidence = "high" if inferred_physical_type == "boolean" else "medium"
        reasons.append("Values/pattern align with boolean semantics.")
    elif inferred_physical_type == "date_or_datetime" or any(t in DATE_HINT_TOKENS for t in tokens) or name.endswith("_at"):
        has_time = any(("T" in v or ":" in v) for v in sample_values)
        role = "datetime" if has_time else "date"
        confidence = "high" if inferred_physical_type == "date_or_datetime" else "medium"
        reasons.append(f"Physical type is {inferred_physical_type}.")
    else:
        is_identifier_name, has_generic_code = _is_identifier_name(name, tokens)
        if (
            is_identifier_name and inferred_physical_type in {"text", "integer", "decimal"}
        ) or any(any(ch.isalpha() for ch in v) and any(ch.isdigit() for ch in v) for v in sample_values):
            role = "identifier"
            if uniqueness_ratio >= 0.95:
                confidence = "high"
                reasons.append(f"Uniqueness ratio is {uniqueness_ratio}.")
            else:
                confidence = "medium"
                reasons.append("Column name/value pattern looks identifier-like.")
                review_notes.append("Identifier-like field is not highly unique; could be a foreign key or repeated reference.")
            if has_generic_code:
                review_notes.append("'code' is generic and may not be a strict identifier.")
        elif inferred_physical_type in {"integer", "decimal"} and any(t in MEASURE_HINTS for t in tokens):
            role = "numeric_measure"
            confidence = "high"
            reasons.append("Numeric physical type and measure-like column name.")
        elif inferred_physical_type == "text" and any(t in FREE_TEXT_HINTS for t in tokens):
            role = "free_text"
            confidence = "medium" if uniqueness_ratio >= 0.7 else "low"
            reasons.append("Column name suggests descriptive free-text content.")
        elif inferred_physical_type == "text" and (
            any(t in CATEGORY_HINTS for t in tokens)
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
    if role == "identifier" and "code" in tokens:
        review_required = True
    if name in GENERIC_NAMES:
        review_required = True
        review_notes.append("Generic column name may hide ambiguous business meaning.")
    if inferred_physical_type == "mixed_or_unknown":
        review_required = True
        review_notes.append("Physical type is mixed_or_unknown.")

    return {
        "semantic_role": role,
        "semantic_role_confidence": confidence,
        "semantic_role_reasons": reasons,
        "review_required": review_required,
        "review_notes": review_notes,
    }
