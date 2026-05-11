from data_dictionary_agent.agent_reporting import build_agent_report


def test_build_agent_report_contains_expected_sections():
    text = build_agent_report({
        "mode": "agent",
        "input": {"input_path": "demo.csv"},
        "plan": [{"step_name": "load_dataset", "status": "completed"}],
        "decisions": [{"decision": "x", "rationale": "y"}],
        "assumptions": [{"assumption": "a", "reason": "b"}],
        "caveats": [{"caveat": "c", "severity": "low"}],
        "review_items": [],
        "summary": {"source_file": "demo.csv", "row_count": 1, "column_count": 2, "config_used": False, "output_dir": "out", "output_files": {}},
    })
    assert "# Agent Report" in text
    assert "## Key decisions" in text
    assert "No review items" in text
