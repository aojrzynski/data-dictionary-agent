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
