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
pip install -e ".[dev]"
python -m data_dictionary_agent.cli \
  --input sample_data/crm_contacts/contacts_clean.csv \
  --output-dir outputs/crm_contacts_profile
```

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

- `src/data_dictionary_agent/` — CLI and pipeline layers
- `docs/` — usage and boundary docs
- `config/examples/` — sample config overrides
- `sample_data/` — sample datasets
- `tests/` — test suite

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
