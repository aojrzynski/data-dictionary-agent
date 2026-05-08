# How It Works

1. CLI validates arguments and input path.
2. Intake reads CSV/XLSX/XLSM into a pandas DataFrame.
3. Profiling computes deterministic dataset and column facts.
4. Trace writer emits `profiling_trace.json`.

No LLM calls or agent orchestration occur in this milestone.
