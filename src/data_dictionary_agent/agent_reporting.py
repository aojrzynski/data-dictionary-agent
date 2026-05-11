from __future__ import annotations


def build_agent_report(agent_trace: dict) -> str:
    summary = agent_trace.get("summary", {})
    input_info = agent_trace.get("input", {})
    lines = [
        f"# Agent Report: {summary.get('source_file', 'unknown source')}",
        "",
        "## Run summary",
        f"- Mode: {agent_trace.get('mode')}",
        f"- Source file: {input_info.get('input_path')}",
        f"- Rows: {summary.get('row_count', 0)}",
        f"- Columns: {summary.get('column_count', 0)}",
        f"- Config used: {summary.get('config_used')}",
        f"- Output directory: {summary.get('output_dir')}",
        "",
        "## What the agent did",
    ]
    for step in agent_trace.get("plan", []):
        lines.append(f"- {step.get('step_name')}: {step.get('status')}")

    lines.extend(["", "## Key decisions"])
    for d in agent_trace.get("decisions", []):
        lines.append(f"- **{d.get('decision')}** — {d.get('rationale')}")

    lines.extend(["", "## Fields needing review"])
    review_items = agent_trace.get("review_items", [])
    if not review_items:
        lines.append("- No review items were flagged.")
    for item in review_items:
        lines.append(f"- **{item.get('column_name')}**: {item.get('reason')} (Suggested action: {item.get('suggested_action')})")

    lines.extend(["", "## Assumptions and caveats"])
    for a in agent_trace.get("assumptions", []):
        lines.append(f"- Assumption: {a.get('assumption')} ({a.get('reason')})")
    for c in agent_trace.get("caveats", []):
        lines.append(f"- Caveat ({c.get('severity')}): {c.get('caveat')}")

    lines.extend(["", "## Output files"])
    for name, path in agent_trace.get("summary", {}).get("output_files", {}).items():
        lines.append(f"- {name}: {path}")
    return "\n".join(lines) + "\n"
