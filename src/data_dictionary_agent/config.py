from __future__ import annotations

"""Config loading and validation for optional dictionary overrides.

This module accepts user-provided context (display names, descriptions, roles)
and validates its structure. It does not mutate profiling evidence itself.
"""

from pathlib import Path
from typing import Any

import yaml

ALLOWED_SEMANTIC_ROLES = {
    "identifier",
    "date",
    "datetime",
    "numeric_measure",
    "categorical",
    "boolean_flag",
    "free_text",
    "possible_sensitive",
    "unknown",
}

ALLOWED_COLUMN_FIELDS = {
    "display_name",
    "description",
    "semantic_role",
    "semantic_role_confidence",
    "sensitivity_hint",
    "review_required",
    "review_notes",
    "caveats",
    "allowed_values",
    "business_rules",
    "owner",
    "domain",
    "source_system",
}


def _empty_config() -> dict[str, Any]:
    return {"dataset": {}, "columns": {}}


def load_config(path: str | Path | None) -> dict[str, Any]:
    """Load and validate optional YAML overrides for dataset and columns."""
    if not path:
        return _empty_config()
    config_path = Path(path)
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    try:
        raw = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ValueError(f"Invalid YAML config: {exc}") from exc

    if raw in (None, ""):
        return _empty_config()
    if not isinstance(raw, dict):
        raise ValueError("Invalid config structure: root must be a mapping with optional 'dataset' and 'columns'.")

    dataset = raw.get("dataset") or {}
    columns = raw.get("columns") or {}
    if not isinstance(dataset, dict):
        raise ValueError("Invalid config structure: 'dataset' must be a mapping.")
    if not isinstance(columns, dict):
        raise ValueError("Invalid config structure: 'columns' must be a mapping keyed by column name.")

    for col_name, overrides in columns.items():
        if not isinstance(overrides, dict):
            raise ValueError(f"Invalid column override for '{col_name}': expected mapping.")
        unknown_fields = set(overrides.keys()) - ALLOWED_COLUMN_FIELDS
        if unknown_fields:
            raise ValueError(f"Invalid column override fields for '{col_name}': {sorted(unknown_fields)}")
        role = overrides.get("semantic_role")
        if role is not None and role not in ALLOWED_SEMANTIC_ROLES:
            raise ValueError(f"Invalid semantic_role for '{col_name}': {role}. Allowed: {sorted(ALLOWED_SEMANTIC_ROLES)}")

    return {"dataset": dataset, "columns": columns}


def get_dataset_overrides(config: dict[str, Any] | None) -> dict[str, Any]:
    return dict((config or {}).get("dataset", {}))


def get_column_overrides(config: dict[str, Any] | None, column_name: str) -> dict[str, Any]:
    return dict((config or {}).get("columns", {}).get(column_name, {}))
