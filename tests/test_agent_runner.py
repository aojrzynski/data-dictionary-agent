import json

from data_dictionary_agent.agent_runner import run_agent


def test_run_agent_creates_outputs(tmp_path):
    out_dir = tmp_path / "agent"
    result = run_agent("sample_data/crm_contacts/contacts_clean.csv", str(out_dir), config_path="config/examples/crm_context.yaml")
    for name in ["profiling_trace", "data_dictionary_md", "data_dictionary_csv", "data_dictionary_json", "suggested_overrides_yaml", "agent_trace", "agent_report"]:
        assert (out_dir / (result["output_paths"][name].split("/")[-1])).exists()

    trace = json.loads((out_dir / "agent_trace.json").read_text(encoding="utf-8"))
    assert trace["mode"] == "agent"
    for key in ["decisions", "assumptions", "caveats", "review_items", "summary"]:
        assert key in trace
    assert trace["summary"]["config_used"] is True
    assert "agent_trace" in trace["summary"]["output_files"]
    assert "agent_report" in trace["summary"]["output_files"]

    report_text = (out_dir / "agent_report.md").read_text(encoding="utf-8")
    assert "- agent_trace:" in report_text
    assert "- agent_report:" in report_text
