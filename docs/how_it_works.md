# How It Works

## Deterministic mode

1. CLI validates arguments and input path.
2. Intake reads CSV/XLSX/XLSM into a pandas DataFrame.
3. Profiling computes deterministic dataset and column physical facts.
4. Semantic inference adds deterministic semantic role suggestions.
5. Optional config overrides inject user-provided business context.
6. Dictionary builder creates first-pass dictionary entries.
7. Output writers emit dictionary artifacts and suggested review overrides.
8. Trace writer emits `profiling_trace.json`.

Pipeline:
`intake -> profiling -> semantic inference -> config overrides -> dictionary -> outputs -> suggested overrides`

## Agent mode

1. Planner builds a bounded run plan.
2. The deterministic pipeline executes using the same intake/profiling/inference/builders.
3. Agent runner records decisions, assumptions, and review items.
4. Agent artifacts are written: `agent_trace.json` and `agent_report.md`.

Pipeline:
`planner -> deterministic pipeline -> review/decision capture -> agent_trace.json -> agent_report.md`

Agent mode is bounded local orchestration over deterministic tools.

## Optional LLM description suggestions

When `--llm-descriptions` is enabled:

1. A redacted/capped safe summary is created in `llm_safe_summary.json`.
2. The tool requests optional wording suggestions from the LLM.
3. If no API key is present or output is invalid, fallback suggestions are generated.
4. Suggestions are written to separate files and do not overwrite dictionary outputs.
