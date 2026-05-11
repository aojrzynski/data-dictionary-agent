# AGENTS

This repository now supports both deterministic mode and bounded agent mode.

## Deterministic mode

Deterministic mode is the base pipeline:
- intake for CSV/XLSX/XLSM,
- deterministic physical profiling,
- deterministic semantic inference,
- optional config overrides,
- deterministic data dictionary outputs,
- suggested override output for review.

## Agent mode

Agent mode adds bounded local orchestration around the same deterministic pipeline.

The agent plans and records:
- run steps,
- decisions,
- assumptions,
- review items,
- run summaries.

These artifacts are written to:
- `agent_trace.json`
- `agent_report.md`

## What the agent does not do

- No autonomous open-ended behavior.
- No framework-based orchestration.
- No replacement of deterministic evidence with generated text.

## How LLM suggestions fit in

Optional LLM description suggestions are a separate wording-assistance layer.

- They are off by default.
- They are written to separate files.
- They do not overwrite deterministic dictionary outputs.
- They are generated from safe summaries with redaction/capping.

## Authority

Deterministic profiling output remains authoritative evidence for observed data facts. Semantic inference, agent review notes, and optional LLM description suggestions are assistive and require human review.
