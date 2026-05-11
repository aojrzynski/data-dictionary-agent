# How It Works

## Deterministic mode

1. CLI validates arguments and input path.
2. Intake reads CSV/XLSX/XLSM into a pandas DataFrame.
3. Profiling computes deterministic dataset and column physical facts.
4. Semantic inference adds deterministic semantic role suggestions.
5. Optional config overrides inject user-provided business context.
6. Dictionary builder creates first-pass dictionary entries.
7. Output writers emit `data_dictionary.md`, `data_dictionary.csv`, and `data_dictionary.json`.
8. Trace writer emits `profiling_trace.json`.
9. Suggested overrides writer emits `suggested_overrides.yaml`.

Pipeline:
`intake -> profiling -> semantic inference -> config overrides -> dictionary -> outputs -> suggested overrides`

## Agent mode

1. Planner builds a bounded run plan.
2. Deterministic pipeline executes using the same intake/profiling/inference/builders.
3. Agent runner reviews outputs and records decisions/review items.
4. Agent artifacts are written: `agent_trace.json` and `agent_report.md`.

Pipeline:
`planner -> deterministic pipeline -> output review -> decisions/review items -> agent_trace.json -> agent_report.md`

No LLM calls occur.
Agent mode is bounded local orchestration over deterministic tools.
