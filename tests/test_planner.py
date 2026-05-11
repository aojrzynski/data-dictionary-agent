from data_dictionary_agent.planner import build_agent_plan


def test_plan_has_required_steps_and_fields():
    plan = build_agent_plan({}, None, {"sheet": None, "config_path": None})
    names = [s["step_name"] for s in plan["steps"]]
    assert names == [
        "validate_input",
        "load_dataset",
        "profile_dataset",
        "infer_semantic_metadata",
        "apply_config_overrides",
        "build_dictionary",
        "build_suggested_overrides",
        "review_outputs",
        "write_outputs",
    ]
    assert all({"step_name", "purpose", "status", "notes"}.issubset(s.keys()) for s in plan["steps"])


def test_plan_notes_change_with_config_presence():
    no_cfg = build_agent_plan({}, None, {"sheet": None, "config_path": None})
    with_cfg = build_agent_plan({}, {"columns": {}}, {"sheet": "Sheet1", "config_path": "cfg.yaml"})
    apply1 = next(s for s in no_cfg["steps"] if s["step_name"] == "apply_config_overrides")
    apply2 = next(s for s in with_cfg["steps"] if s["step_name"] == "apply_config_overrides")
    assert "No config" in apply1["notes"][0]
    assert "Config file provided" in apply2["notes"][0]
