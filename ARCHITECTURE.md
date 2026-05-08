# Architecture

## CLI layer

`cli.py` parses command arguments, coordinates intake/profiling/trace writing, and handles user-facing success/error output.

## Intake layer

`intake.py` validates input path and file type, then reads CSV/Excel via pandas.

## Deterministic profiling layer

`profiling.py` computes dataset-level and column-level structural facts deterministically.

## Trace writing layer

`trace_writer.py` writes `profiling_trace.json` to the output directory with stable formatting.

## Future placeholder layers

- Future agent layer: orchestration and review workflows
- Future LLM layer: optional narrative suggestions from deterministic evidence
