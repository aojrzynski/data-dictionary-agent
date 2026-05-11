# Data Dictionary Agent

Data Dictionary Agent is a local-first, CLI-first Python tool that profiles CSV/XLSX/XLSM datasets and produces first-pass data dictionary artifacts. It combines deterministic profiling, deterministic semantic inference, human-provided config context, bounded agent orchestration, and optional LLM wording suggestions without making the LLM the source of truth.

## Why this exists

Documenting datasets by hand is repetitive and often inconsistent.

This project gives you a practical first pass:
- profile what is actually in the data,
- infer likely column roles with deterministic rules,
- apply known business context with optional config overrides,
- and produce readable outputs you can review and refine.

It is designed for local runs, clear artifacts, and reviewable evidence.

## Why not just ask an LLM?

You can ask an LLM to draft documentation, but that alone has limits:
- it may invent details that are not in your data,
- it may miss distribution-level facts,
- and it may blur observed evidence with guessed interpretation.

This project keeps those boundaries clear:
- deterministic profiling captures observed facts,
- deterministic semantic inference suggests likely roles,
- optional LLM output is only wording help from a safe summary,
- and authoritative outputs remain deterministic/profile/config grounded.

## What this project demonstrates

- Local-first tabular intake (`.csv`, `.xlsx`, `.xlsm`)
- Deterministic physical profiling
- Deterministic semantic inference
- Optional YAML config overrides for business context
- Deterministic dictionary outputs (`.md`, `.csv`, `.json`)
- Suggested override workflow (`suggested_overrides.yaml`)
- Bounded agent mode with trace/report artifacts
- Optional LLM description suggestions with safe summaries and fallback generation

## Why this is a hybrid agent

In this repo, **hybrid agent** does not just mean “deterministic plus LLM.”

It means several bounded layers work together:
1. deterministic profiling produces observed evidence,
2. deterministic semantic inference suggests likely roles,
3. config overrides let a human provide known business context,
4. bounded agent mode plans, orchestrates, and records decisions/review items,
5. optional LLM suggestions help with wording only from safe summaries,
6. deterministic/profile/config artifacts remain the source of truth.

## Quick start

```bash
python -m venv .venv
source .venv/Scripts/activate
python -m pip install -e ".[dev]"
python -m data_dictionary_agent.cli \
  --input sample_data/crm_contacts/contacts_clean.csv \
  --output-dir outputs/crm_contacts_profile
```

macOS/Linux activation uses `source .venv/bin/activate`.

### Optional: enable real LLM suggestions

```bash
python -m pip install -e ".[dev,llm]"
export OPENAI_API_KEY="your-key"
export OPENAI_MODEL="gpt-4o-mini"  # optional
```

`--llm-descriptions` still works without an API key. In that case deterministic fallback suggestions are generated. LLM suggestion files stay separate and do not overwrite dictionary outputs.

## Example commands

### Deterministic

```bash
python -m data_dictionary_agent.cli \
  --input sample_data/crm_contacts/contacts_clean.csv \
  --output-dir outputs/crm_contacts_profile
```

### Deterministic with config

```bash
python -m data_dictionary_agent.cli \
  --input sample_data/crm_contacts/contacts_clean.csv \
  --config config/examples/crm_context.yaml \
  --output-dir outputs/crm_contacts_with_config
```

### Agent mode

```bash
python -m data_dictionary_agent.cli \
  --input sample_data/crm_contacts/contacts_clean.csv \
  --config config/examples/crm_context.yaml \
  --mode agent \
  --output-dir outputs/crm_contacts_agent
```

### Deterministic + LLM suggestions

```bash
python -m data_dictionary_agent.cli \
  --input sample_data/crm_contacts/contacts_clean.csv \
  --llm-descriptions \
  --output-dir outputs/crm_contacts_llm
```

### Agent + LLM suggestions

```bash
python -m data_dictionary_agent.cli \
  --input sample_data/crm_contacts/contacts_clean.csv \
  --config config/examples/crm_context.yaml \
  --mode agent \
  --llm-descriptions \
  --output-dir outputs/crm_contacts_agent_llm
```

## Output artifacts

### Evidence layer
- `profiling_trace.json`

### Dictionary layer
- `data_dictionary.md`
- `data_dictionary.csv`
- `data_dictionary.json`

### Review/config layer
- `suggested_overrides.yaml`

### Agent layer (when `--mode agent`)
- `agent_trace.json`
- `agent_report.md`

### Optional LLM suggestion layer (when `--llm-descriptions`)
- `llm_safe_summary.json`
- `llm_description_suggestions.json`
- `llm_description_suggestions.md`

## Authority boundary

- Deterministic profiling trace is authoritative evidence for observed data facts.
- Deterministic semantic inference is a suggestion layer.
- Config overrides are human-provided context.
- Dictionary files are first-pass documentation built from those inputs.
- LLM description suggestions are optional, off by default, written to separate files, and do not overwrite `data_dictionary.md/.csv/.json`.
- Possible sensitive fields are redacted in `llm_safe_summary.json`.
- No full raw rows are sent to the LLM.
- If no API key is available, fallback description suggestions are generated.

## Project structure

- `src/data_dictionary_agent/cli.py` — command-line entrypoint and run orchestration.
- `src/data_dictionary_agent/intake.py` — CSV/XLSX/XLSM loading and input validation.
- `src/data_dictionary_agent/profiling.py` — deterministic physical profiling logic.
- `src/data_dictionary_agent/semantic_inference.py` — deterministic semantic role suggestion rules.
- `src/data_dictionary_agent/config.py` — YAML config override loading/validation.
- `src/data_dictionary_agent/dictionary_builder.py` — first-pass dictionary entry construction.
- `src/data_dictionary_agent/suggested_overrides.py` — suggested review override artifact generation.
- `src/data_dictionary_agent/agent_runner.py` — bounded agent-mode execution and trace capture.
- `src/data_dictionary_agent/agent_reporting.py` — human-readable agent run reporting.
- `src/data_dictionary_agent/llm_descriptions.py` — safe summary creation and optional LLM/fallback suggestions.
- `src/data_dictionary_agent/output_writers.py` — writes dictionary and related output artifacts.
- `tests/` — automated test coverage for pipeline behavior.
- `docs/` — usage guides, boundaries, and release notes for maintainers.

## Run tests

```bash
python -m pytest
```

## Limitations and non-goals

- Not a formal sensitive-data classification system.
- Not a data catalog publishing platform.
- Not a framework-based orchestration project.
- Not an autonomous, open-ended agent.
- Not a replacement for governed business definitions.

## Further reading

- `ARCHITECTURE.md`
- `PROJECT_SCOPE.md`
- `docs/how_it_works.md`
- `docs/interpreting_outputs.md`
- `docs/hybrid_agent.md`
- `docs/llm_boundary.md`
- `docs/example_commands.md`
- `docs/config_overrides.md`
- `docs/agent_mode.md`
- `docs/release_checklist.md`
- `FUTURE_WORK.md`
