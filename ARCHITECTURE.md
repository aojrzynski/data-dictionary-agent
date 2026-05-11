# Architecture

## Overview

Data Dictionary Agent is a layered, local-first pipeline. Deterministic profiling and deterministic semantic inference establish observed evidence and likely roles. Optional config overrides add known business context. Optional bounded agent mode adds orchestration and traceable review artifacts. Optional LLM suggestions add wording help only.

## Pipeline summary

Core flow:
`intake -> profiling -> semantic inference -> config overrides -> dictionary builder -> outputs`

Optional flows:
- agent mode: `planner -> core flow orchestration -> review artifacts`
- LLM suggestions: `safe summary -> suggestions/fallback -> separate suggestion outputs`

## Deterministic mode pipeline

1. CLI validates arguments.
2. Intake reads supported tabular inputs.
3. Profiling computes deterministic physical facts.
4. Semantic inference computes deterministic role suggestions.
5. Optional config overrides apply business context.
6. Dictionary builder creates first-pass entries.
7. Output writers emit dictionary and review files.
8. Trace writer emits profiling evidence.

## Agent mode pipeline

1. Planner creates a bounded deterministic plan.
2. Agent runner executes deterministic pipeline steps.
3. Agent runner records decisions, assumptions, and review items.
4. Agent reporting produces human-readable summaries.
5. Agent artifacts are written as trace/report outputs.

## Optional LLM suggestion pipeline

1. Safe summary builder redacts/caps dataset information.
2. Optional LLM request generates wording suggestions.
3. If no API key or invalid response, deterministic fallback suggestions are generated.
4. Suggestions are written to separate LLM files and never overwrite dictionary outputs.

## Layer responsibilities

- **CLI layer (`cli.py`)**: parses arguments and selects execution mode.
- **Intake layer (`intake.py`)**: validates paths and reads CSV/XLSX/XLSM.
- **Profiling layer (`profiling.py`)**: computes deterministic physical profiling facts.
- **Semantic inference layer (`semantic_inference.py`)**: proposes deterministic semantic roles and review flags.
- **Config override layer (`config.py`)**: loads and validates optional YAML overrides.
- **Dictionary builder layer (`dictionary_builder.py`)**: merges evidence + inference + overrides into first-pass entries.
- **Suggested overrides layer (`suggested_overrides.py`)**: writes editable review suggestions.
- **Planner layer (`planner.py`)**: creates bounded agent run plans.
- **Agent runner layer (`agent_runner.py`)**: orchestrates deterministic steps and captures traceable review activity.
- **Agent reporting layer (`agent_reporting.py`)**: renders `agent_report.md` from run trace data.
- **LLM safe summary/suggestion layer (`llm_descriptions.py`, `llm_client.py`)**: prepares safe payloads and handles optional suggestion generation/fallback.
- **Output writer layer (`output_writers.py`)**: writes dictionary, review, agent, and optional LLM files.
- **Trace writing layer (`trace_writer.py`)**: writes `profiling_trace.json` as deterministic evidence.

## Authority boundary

Deterministic profiling evidence remains authoritative for observed data facts. Semantic inference, agent review items, and LLM wording suggestions are non-authoritative assistive layers. Config overrides provide human-owned context. Final publication decisions remain a human responsibility.

## Why the layers are separated

- Keeps evidence generation independent from narration.
- Makes output provenance explicit and testable.
- Allows optional features (agent mode, LLM suggestions) without changing core deterministic behavior.
- Supports review workflows where authoritative facts and suggested wording stay clearly separated.
