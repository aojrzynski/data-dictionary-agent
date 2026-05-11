from __future__ import annotations

import uuid
from datetime import datetime, timezone
from pathlib import Path

from data_dictionary_agent.agent_reporting import build_agent_report
from data_dictionary_agent.config import load_config
from data_dictionary_agent.dictionary_builder import build_data_dictionary
from data_dictionary_agent.intake import load_dataset
from data_dictionary_agent.output_writers import (
    write_agent_report,
    write_agent_trace,
    write_dictionary_outputs,
    write_suggested_overrides_yaml,
)
from data_dictionary_agent.planner import build_agent_plan
from data_dictionary_agent.profiling import build_profile
from data_dictionary_agent.suggested_overrides import build_suggested_overrides
from data_dictionary_agent.trace_writer import write_profiling_trace


def run_agent(input_path: str, output_dir: str, sheet: str | None = None, config_path: str | None = None, sample_size: int = 5, top_values_limit: int = 5) -> dict:
    config = load_config(config_path)
    plan = build_agent_plan({"input_path": input_path}, config, {"sheet": sheet, "config_path": config_path})

    df, metadata = load_dataset(input_path, sheet=sheet)
    profile = build_profile(df, metadata, sample_size=sample_size, top_values_limit=top_values_limit)
    profiling_trace_path = write_profiling_trace(profile, output_dir)
    dictionary = build_data_dictionary(profile, config=config)
    dictionary_paths = write_dictionary_outputs(dictionary, output_dir)
    suggested = build_suggested_overrides(dictionary)
    suggested_path = write_suggested_overrides_yaml(suggested, output_dir)

    for step in plan["steps"]:
        step["status"] = "completed"

    review_items = []
    for c in dictionary.get("columns", []):
        needs = c.get("review_required") or c.get("semantic_role") in {"unknown", "possible_sensitive"} or c.get("semantic_role_confidence") == "low" or bool(c.get("caveats"))
        if needs:
            review_items.append({
                "column_name": c.get("column_name"),
                "reason": "; ".join(c.get("review_notes") or c.get("caveats") or ["Review required by deterministic rules."]),
                "suggested_action": "Confirm semantic role, description, and handling requirements.",
            })

    agent_trace_path = Path(output_dir) / "agent_trace.json"
    agent_report_path = Path(output_dir) / "agent_report.md"
    output_files = {
        "profiling_trace": str(profiling_trace_path),
        **{k: str(v) for k, v in dictionary_paths.items()},
        "suggested_overrides_yaml": str(suggested_path),
        "agent_trace": str(agent_trace_path),
        "agent_report": str(agent_report_path),
    }

    agent_trace = {
        "run_id": str(uuid.uuid4()),
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "mode": "agent",
        "input": {"input_path": input_path, "sheet": sheet, "config_path": config_path, "sample_size": sample_size, "top_values_limit": top_values_limit},
        "plan": plan["steps"],
        "decisions": [
            {"decision_id": "d1", "decision": "Config override usage", "rationale": "Config overrides were applied because --config was provided." if config_path else "Config overrides were not applied because --config was not provided.", "evidence": [config_path or "no config path"]},
            {"decision_id": "d2", "decision": "Suggested overrides generation", "rationale": "Suggested overrides were generated because review-required fields exist." if review_items else "Suggested overrides still emitted for consistency even when no review-required fields exist.", "evidence": [f"review_items={len(review_items)}"]},
            {"decision_id": "d3", "decision": "LLM behavior", "rationale": "No LLM descriptions were generated because LLM support is not enabled in this milestone.", "evidence": ["deterministic pipeline only"]},
        ],
        "assumptions": [
            {"assumption": "Deterministic profiling trace is authoritative evidence.", "reason": "Project boundary for milestone 5."}
        ],
        "caveats": [
            {"caveat": "First-pass dictionary only.", "severity": "medium"},
            {"caveat": "Semantic roles are suggestions.", "severity": "medium"},
            {"caveat": "Possible sensitive fields are hints, not compliance classification.", "severity": "high"},
            {"caveat": "Config overrides are user-provided context, not observed evidence.", "severity": "medium"},
            {"caveat": "No LLM was used.", "severity": "low"},
        ],
        "review_items": review_items,
        "summary": {
            "source_file": Path(input_path).name,
            "output_dir": output_dir,
            "row_count": profile.get("row_count", 0),
            "column_count": profile.get("column_count", 0),
            "columns_needing_review": len(review_items),
            "possible_sensitive_fields": sum(1 for c in dictionary.get("columns", []) if c.get("semantic_role") == "possible_sensitive"),
            "config_used": bool(config_path),
            "output_files": output_files,
        },
    }
    agent_trace["summary"]["output_files"] = output_files
    agent_report_text = build_agent_report(agent_trace)
    write_agent_trace(agent_trace, output_dir)
    write_agent_report(agent_report_text, output_dir)

    return {"profile": profile, "dictionary": dictionary, "suggested_overrides": suggested, "output_paths": output_files, "agent_trace": agent_trace, "agent_report_text": agent_report_text}
