# data-dictionary-agent

A local-first, CLI-first tool that profiles tabular datasets and produces deterministic first-pass data dictionary outputs.

## Why this exists

Before formal documentation, teams need grounded evidence about what is actually in a dataset. This project keeps deterministic profiling as the evidence layer, adds deterministic semantic suggestions, and generates review-friendly dictionary artifacts.

## Authority boundary

- Profiling = observed evidence (authoritative for observed data facts).
- Semantic inference = deterministic suggestions.
- Config overrides = user-provided business context.
- Dictionary outputs = first-pass documentation.
- Agent mode = bounded local orchestration and review over deterministic outputs.
- LLM generation is not included yet.

## Quick start

```bash
pip install -e ".[dev]"
python -m data_dictionary_agent.cli --input sample_data/crm_contacts/contacts_clean.csv --output-dir outputs/crm_contacts_profile
```

## Config overrides

Use `--config path/to/config.yaml` to inject known business context (dataset metadata and column-level overrides) into dictionary generation without changing observed profiling facts.

```bash
python -m data_dictionary_agent.cli \
  --input sample_data/crm_contacts/contacts_clean.csv \
  --config config/examples/crm_context.yaml \
  --output-dir outputs/crm_contacts_with_config
```

## Agent mode

Use `--mode agent` for bounded deterministic orchestration and review artifacts (`agent_trace.json`, `agent_report.md`). No LLM is used.

```bash
python -m data_dictionary_agent.cli \
  --input sample_data/crm_contacts/contacts_clean.csv \
  --config config/examples/crm_context.yaml \
  --mode agent \
  --output-dir outputs/crm_contacts_agent
```

## Review workflow

Each run writes `suggested_overrides.yaml`, an editable file containing fields that likely need human confirmation. Typical workflow:
1. Run without config.
2. Review dictionary + `suggested_overrides.yaml`.
3. Fill in/edit config.
4. Rerun with `--config`.

## Outputs

- `profiling_trace.json` (deterministic evidence and semantic suggestions)
- `data_dictionary.json` (structured dictionary)
- `data_dictionary.csv` (spreadsheet-friendly dictionary)
- `data_dictionary.md` (human-readable dictionary)
- `suggested_overrides.yaml` (editable review suggestions)

Agent mode also writes:
- `agent_trace.json`
- `agent_report.md`

## Limitations

- No LLM-generated descriptions yet
- No formal sensitive-data compliance classification
- No framework-based orchestration yet
