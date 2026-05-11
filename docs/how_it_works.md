# How It Works

1. CLI validates arguments and input path.
2. Intake reads CSV/XLSX/XLSM into a pandas DataFrame.
3. Profiling computes deterministic dataset and column physical facts.
4. Semantic inference adds deterministic semantic role suggestions.
5. Dictionary builder creates first-pass dictionary entries using deterministic templates.
6. Output writers emit `data_dictionary.md`, `data_dictionary.csv`, and `data_dictionary.json`.
7. Trace writer emits `profiling_trace.json`.

No LLM calls or agent orchestration occur in this milestone.

Pipeline: intake -> profiling -> semantic inference -> optional config overrides -> dictionary builder -> output writers -> suggested overrides.


## Pipelines
- Deterministic: intake -> profiling -> semantic inference -> config overrides -> dictionary -> outputs -> suggested overrides
- Agent: deterministic pipeline + planner/review/decision trace/report
