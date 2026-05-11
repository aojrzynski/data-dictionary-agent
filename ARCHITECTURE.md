# Architecture

## CLI layer

`cli.py` parses command arguments and coordinates the end-to-end deterministic pipeline.

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

## Suggested overrides layer

`suggested_overrides.py` builds an editable YAML file for fields needing review.

## Trace writing layer

`trace_writer.py` remains focused on `profiling_trace.json`.
