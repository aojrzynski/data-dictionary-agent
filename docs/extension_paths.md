# Extension Paths

Potential future extension points:

- `profiling.py` for richer deterministic profiling rules.
- `semantic_inference.py` for expanded deterministic role inference logic.
- `config.py` for stronger override validation and richer schema checks.
- `dictionary_builder.py` for additional output metadata and provenance fields.
- `agent_runner.py` / `planner.py` / `agent_reporting.py` for bounded reviewer-oriented orchestration patterns.
- `llm_descriptions.py` for richer safe-summary controls and wording suggestion policies.
- `output_writers.py` for additional export formats.

Any extension should keep the authority boundary explicit: deterministic evidence is authoritative, while suggestions remain review-oriented.
