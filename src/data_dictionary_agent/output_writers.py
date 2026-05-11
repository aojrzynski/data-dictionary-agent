from __future__ import annotations

import csv
import json
from pathlib import Path

import yaml


def _escape_md(value: object) -> str:
    return str(value).replace("|", "\\|")


def write_dictionary_json(dictionary: dict, output_dir: str | Path) -> Path:
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    output_path = out_dir / "data_dictionary.json"
    output_path.write_text(json.dumps(dictionary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return output_path


def write_suggested_overrides_yaml(suggested_overrides: dict, output_dir: str | Path) -> Path:
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    output_path = out_dir / "suggested_overrides.yaml"
    output_path.write_text(yaml.safe_dump(suggested_overrides, sort_keys=False), encoding="utf-8")
    return output_path


def write_dictionary_csv(dictionary: dict, output_dir: str | Path) -> Path:
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    output_path = out_dir / "data_dictionary.csv"
    columns = dictionary.get("columns", [])
    fieldnames = list(columns[0].keys()) if columns else []
    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in columns:
            formatted = dict(row)
            formatted["sample_values"] = " | ".join(str(v) for v in row.get("sample_values", []))
            formatted["top_values"] = "; ".join(
                f"{i.get('value')} ({i.get('count')})" for i in row.get("top_values", [])
            )
            formatted["review_notes"] = " | ".join(str(v) for v in row.get("review_notes", []))
            formatted["caveats"] = " | ".join(str(v) for v in row.get("caveats", []))
            writer.writerow(formatted)
    return output_path


def write_dictionary_markdown(dictionary: dict, output_dir: str | Path) -> Path:
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    output_path = out_dir / "data_dictionary.md"
    ds = dictionary.get("dataset", {})
    summary = dictionary.get("summary_counts", {})
    rows = dictionary.get("columns", [])
    review_rows = [r for r in rows if r["review_required"]]

    lines = [f"# Data Dictionary: {ds.get('source_file')}", "", "## Dataset summary"]
    lines += [
        f"- Source file: {ds.get('source_file')}",
        f"- File type: {ds.get('file_type')}",
        f"- Sheet: {ds.get('sheet')}",
        f"- Rows: {ds.get('rows')}",
        f"- Columns: {ds.get('columns')}",
        f"- Generated at: {ds.get('generated_at')}",
        "",
        "## Summary",
        f"- Columns needing review: {summary.get('columns_needing_review', 0)}",
        f"- Possible sensitive fields: {summary.get('possible_sensitive_fields', 0)}",
        f"- Identifier-like fields: {summary.get('identifier_like_fields', 0)}",
        f"- Date/datetime fields: {summary.get('date_datetime_fields', 0)}",
        f"- Numeric measures: {summary.get('numeric_measures', 0)}",
        f"- Categorical fields: {summary.get('categorical_fields', 0)}",
        "",
        "## Column dictionary",
        "",
        "| Column | Display name | Description | Physical type | Semantic role | Confidence | Nullable | Review required |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        lines.append(
            f"| {_escape_md(r['column_name'])} | {_escape_md(r['display_name'])} | {_escape_md(r['description'] or '(blank - review required)')} | {_escape_md(r['physical_type'])} | {_escape_md(r['semantic_role'])} | {_escape_md(r['semantic_role_confidence'])} | {r['nullable']} | {r['review_required']} |"
        )
    lines.extend(["", "## Fields needing review", ""])
    if not review_rows:
        lines.append("No fields require review based on current deterministic rules.")
    for r in review_rows:
        notes = " | ".join(r.get("review_notes", [])) or "No explicit notes provided."
        lines.append(f"- **{r['column_name']}**: {_escape_md(notes)}")
    lines.extend(["", "## Caveats", "", "- This is a first-pass deterministic dictionary.", "- Semantic roles are suggestions, not confirmed business definitions.", "- Possible sensitive fields are hints, not compliance classification.", "- Human review is required before formal publication."])
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output_path


def write_dictionary_outputs(dictionary: dict, output_dir: str | Path) -> dict[str, Path]:
    return {
        "data_dictionary_md": write_dictionary_markdown(dictionary, output_dir),
        "data_dictionary_csv": write_dictionary_csv(dictionary, output_dir),
        "data_dictionary_json": write_dictionary_json(dictionary, output_dir),
    }


def write_agent_trace(agent_trace: dict, output_dir: str | Path) -> Path:
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    output_path = out_dir / "agent_trace.json"
    output_path.write_text(json.dumps(agent_trace, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return output_path


def write_agent_report(agent_report_text: str, output_dir: str | Path) -> Path:
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    output_path = out_dir / "agent_report.md"
    output_path.write_text(agent_report_text, encoding="utf-8")
    return output_path


def write_llm_safe_summary(summary: dict, output_dir: str | Path) -> Path:
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    output_path = out_dir / "llm_safe_summary.json"
    output_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return output_path


def write_llm_description_suggestions_json(suggestions: dict, output_dir: str | Path) -> Path:
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    output_path = out_dir / "llm_description_suggestions.json"
    output_path.write_text(json.dumps(suggestions, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return output_path


def write_llm_description_suggestions_markdown(suggestions: dict, source_file: str, output_dir: str | Path) -> Path:
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    output_path = out_dir / "llm_description_suggestions.md"
    lines = [
        f"# LLM Description Suggestions: {source_file}","", "## Boundary",
        "- LLM suggestions are wording suggestions only.",
        "- Deterministic profiling remains the evidence source.",
        "- Config descriptions are user-provided context and are not overwritten.",
        "- Possible sensitive fields were redacted before LLM use.",
        "- Human review is required.","", "## Summary",
        f"- LLM requested: {suggestions.get('llm_requested')}",
        f"- LLM used: {suggestions.get('llm_used')}",
        f"- Model: {suggestions.get('model')}",
        f"- Columns suggested: {len(suggestions.get('columns', []))}",
        f"- Warnings: {' | '.join(suggestions.get('warnings', [])) if suggestions.get('warnings') else 'None'}", "", "## Suggestions", "",
        "| Column | Current description source | Suggested description | Suggestion source | Review required |",
        "|---|---|---|---|---|",
    ]
    for c in suggestions.get('columns', []):
        lines.append(f"| {_escape_md(c.get('column_name'))} | {_escape_md(c.get('current_description_source'))} | {_escape_md(c.get('suggested_description'))} | {_escape_md(c.get('suggestion_source'))} | {c.get('review_required')} |")
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output_path
