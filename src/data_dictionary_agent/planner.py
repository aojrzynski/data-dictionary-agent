from __future__ import annotations

"""Plan builder for bounded agent-mode orchestration.

The planner records intended deterministic steps and context notes so runs are
auditable. It does not execute profiling or inference itself.
"""
from typing import Any


def build_agent_plan(input_metadata: dict[str, Any], config: dict[str, Any] | None, cli_options: dict[str, Any]) -> dict[str, Any]:
    """Create a deterministic run plan with human-readable step purposes."""
    config_provided = bool(cli_options.get("config_path"))
    sheet = cli_options.get("sheet")
    steps = [
        ("validate_input", "Validate that input path and options are valid."),
        ("load_dataset", "Load dataset and collect source metadata."),
        ("profile_dataset", "Build deterministic physical profile evidence."),
        ("infer_semantic_metadata", "Run deterministic semantic inference for each column."),
        ("apply_config_overrides", "Apply user-provided business context overrides if present."),
        ("build_dictionary", "Construct the data dictionary output."),
        ("build_suggested_overrides", "Generate suggested overrides for review-required fields."),
        ("review_outputs", "Summarize ambiguity, caveats, and human review needs."),
        ("write_outputs", "Write all deterministic and agent output artifacts."),
    ]

    plan_steps = []
    for step_name, purpose in steps:
        notes = []
        if step_name == "apply_config_overrides":
            notes.append("Config file provided." if config_provided else "No config file provided; using deterministic outputs only.")
        if step_name == "load_dataset" and sheet is None:
            notes.append("Excel sheet not explicitly provided; loader default rules apply.")
        plan_steps.append({"step_name": step_name, "purpose": purpose, "status": "planned", "notes": notes})

    return {"input_metadata": input_metadata, "config_provided": config_provided, "steps": plan_steps}
