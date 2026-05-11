from __future__ import annotations

from typing import Any


def build_suggested_overrides(dictionary: dict[str, Any]) -> dict[str, Any]:
    dataset = dictionary.get("dataset", {})
    out: dict[str, Any] = {
        "dataset": {
            "name": dataset.get("source_file", "").split(".")[0] if dataset.get("source_file") else "",
            "display_name": "",
            "description": "",
            "owner": "",
            "domain": "",
            "source_system": "",
        },
        "columns": {},
    }

    for c in dictionary.get("columns", []):
        include = (
            c.get("review_required")
            or c.get("description_source") == "blank_review_required"
            or c.get("semantic_role_confidence") == "low"
            or c.get("semantic_role") in {"unknown", "possible_sensitive"}
            or bool(c.get("caveats"))
        )
        if not include:
            continue
        notes = list(c.get("review_notes", []))
        out["columns"][c["column_name"]] = {
            "display_name": c.get("display_name", ""),
            "description": c.get("description", ""),
            "semantic_role": c.get("semantic_role", "unknown"),
            "review_required": True,
            "review_notes": notes,
            "suggested_action": "Add business definition and confirm semantic role.",
        }
        if c.get("semantic_role") == "possible_sensitive":
            out["columns"][c["column_name"]]["suggested_action"] = (
                "Confirm handling rules and whether this should be documented as personal/contact data."
            )

    if not out["columns"]:
        out["note"] = "No review items flagged by deterministic rules."
    return out
