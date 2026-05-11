# Architecture

## CLI layer

`cli.py` parses command arguments and coordinates mode-specific execution.

## Intake layer

`intake.py` validates input path/file type and reads CSV/XLSX/XLSM via pandas.

## Deterministic profiling layer

`profiling.py` computes dataset and column physical facts deterministically.

## Deterministic semantic inference layer

`semantic_inference.py` adds suggested semantic roles and review flags from deterministic evidence.

## Config override layer

`config.py` loads and validates optional YAML business context.

## Dictionary builder layer

`dictionary_builder.py` transforms profile + semantic fields into first-pass dictionary entries with deterministic template descriptions, caveats, and override provenance.

## Output writer layer

`output_writers.py` writes:
- `data_dictionary.md`
- `data_dictionary.csv`
- `data_dictionary.json`
- `suggested_overrides.yaml`
- `agent_trace.json`
- `agent_report.md`

## Suggested overrides layer

`suggested_overrides.py` builds an editable YAML file for fields needing review.

## Trace writing layer

`trace_writer.py` remains focused on `profiling_trace.json`.

## Planner layer

`planner.py` builds a simple deterministic plan for agent-mode runs.

## Agent runner layer

`agent_runner.py` orchestrates the deterministic pipeline, collects decisions/review items, and writes agent artifacts.

## Agent reporting layer

`agent_reporting.py` turns the agent trace into a readable Markdown report.
