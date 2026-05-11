import pytest

from data_dictionary_agent.config import load_config


def test_valid_config_loads(tmp_path):
    path = tmp_path / "cfg.yaml"
    path.write_text("dataset:\n  name: x\ncolumns:\n  a:\n    semantic_role: unknown\n", encoding="utf-8")
    cfg = load_config(path)
    assert cfg["dataset"]["name"] == "x"


def test_missing_config_path_raises():
    with pytest.raises(FileNotFoundError):
        load_config("missing.yaml")


def test_invalid_yaml_raises(tmp_path):
    path = tmp_path / "bad.yaml"
    path.write_text("dataset: [", encoding="utf-8")
    with pytest.raises(ValueError, match="Invalid YAML"):
        load_config(path)


def test_invalid_semantic_role_raises(tmp_path):
    path = tmp_path / "bad_role.yaml"
    path.write_text("columns:\n  a:\n    semantic_role: nope\n", encoding="utf-8")
    with pytest.raises(ValueError, match="Invalid semantic_role"):
        load_config(path)


def test_empty_config_is_safe(tmp_path):
    path = tmp_path / "empty.yaml"
    path.write_text("", encoding="utf-8")
    assert load_config(path) == {"dataset": {}, "columns": {}}
