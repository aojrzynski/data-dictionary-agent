import json
import subprocess
import sys
from pathlib import Path

from data_dictionary_agent.trace_writer import write_profiling_trace


def test_trace_writer_writes_file(tmp_path: Path):
    profile = {"row_count": 1, "columns": []}
    output_path = write_profiling_trace(profile, tmp_path)
    assert output_path.exists()
    loaded = json.loads(output_path.read_text(encoding="utf-8"))
    assert loaded["row_count"] == 1


def test_cli_runs_and_creates_trace_and_dictionary_outputs(tmp_path: Path):
    out_dir = tmp_path / "profile"
    cmd = [
        sys.executable,
        "-m",
        "data_dictionary_agent.cli",
        "--input",
        "sample_data/crm_contacts/contacts_clean.csv",
        "--output-dir",
        str(out_dir),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    trace_path = out_dir / "profiling_trace.json"
    md_path = out_dir / "data_dictionary.md"
    csv_path = out_dir / "data_dictionary.csv"
    dict_json_path = out_dir / "data_dictionary.json"
    suggested_path = out_dir / "suggested_overrides.yaml"
    assert trace_path.exists()
    assert md_path.exists()
    assert csv_path.exists()
    assert dict_json_path.exists()
    assert suggested_path.exists()
    loaded = json.loads(trace_path.read_text(encoding="utf-8"))
    assert any(col.get("semantic_role") for col in loaded["columns"])
    dict_loaded = json.loads(dict_json_path.read_text(encoding="utf-8"))
    assert len(dict_loaded["columns"]) > 0


def test_cli_with_config_applies_override(tmp_path: Path):
    cfg = tmp_path / "cfg.yaml"
    cfg.write_text("""columns:
  email:
    display_name: Email Address
""", encoding="utf-8")
    out_dir = tmp_path / "profile_cfg"
    cmd = [sys.executable, "-m", "data_dictionary_agent.cli", "--input", "sample_data/crm_contacts/contacts_clean.csv", "--config", str(cfg), "--output-dir", str(out_dir)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    loaded = json.loads((out_dir / "data_dictionary.json").read_text(encoding="utf-8"))
    email = next(c for c in loaded["columns"] if c["column_name"] == "email")
    assert email["display_name"] == "Email Address"
    assert email["display_name_source"] == "config_override"
    assert "description_source" in email
    assert "semantic_role_source" in email


def test_cli_agent_mode_creates_agent_artifacts(tmp_path: Path):
    out_dir = tmp_path / "agent"
    cmd = [sys.executable, "-m", "data_dictionary_agent.cli", "--input", "sample_data/crm_contacts/contacts_clean.csv", "--config", "config/examples/crm_context.yaml", "--mode", "agent", "--output-dir", str(out_dir)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert (out_dir / "agent_trace.json").exists()
    assert (out_dir / "agent_report.md").exists()


def test_cli_default_mode_is_deterministic(tmp_path: Path):
    out_dir = tmp_path / "det"
    cmd = [sys.executable, "-m", "data_dictionary_agent.cli", "--input", "sample_data/crm_contacts/contacts_clean.csv", "--output-dir", str(out_dir)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0
    assert "mode: deterministic" in result.stdout


def test_cli_invalid_mode_rejected():
    parser = __import__("data_dictionary_agent.cli", fromlist=["build_parser"]).build_parser()
    try:
        parser.parse_args(["--input", "x.csv", "--mode", "bad"])
    except SystemExit as exc:
        assert exc.code != 0
        return
    raise AssertionError("Expected argparse to reject invalid mode")

def test_cli_llm_descriptions_writes_files_without_api_key(tmp_path, monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    out_dir = tmp_path / "llm"
    cmd = [sys.executable, "-m", "data_dictionary_agent.cli", "--input", "sample_data/crm_contacts/contacts_clean.csv", "--llm-descriptions", "--output-dir", str(out_dir)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert (out_dir / "llm_safe_summary.json").exists()
    assert (out_dir / "llm_description_suggestions.json").exists()
    assert (out_dir / "llm_description_suggestions.md").exists()


def test_cli_default_run_has_no_llm_files(tmp_path):
    out_dir = tmp_path / "no_llm"
    cmd = [sys.executable, "-m", "data_dictionary_agent.cli", "--input", "sample_data/crm_contacts/contacts_clean.csv", "--output-dir", str(out_dir)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0
    assert not (out_dir / "llm_safe_summary.json").exists()
