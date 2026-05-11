# data-dictionary-agent

A local-first, CLI-first tool that profiles tabular datasets and produces deterministic first-pass data dictionary outputs.

## Authority boundary

- Profiling = observed evidence.
- Semantic inference = deterministic suggestions.
- Config overrides = user-provided business context.
- Dictionary outputs = first-pass documentation.
- Agent mode = bounded local orchestration and review over deterministic outputs.
- LLM description suggestions = optional wording suggestions only, not evidence or truth.

## Quick start

```bash
pip install -e ".[dev]"
python -m data_dictionary_agent.cli --input sample_data/crm_contacts/contacts_clean.csv --output-dir outputs/crm_contacts_profile
```

## Example commands

Deterministic:
```bash
python -m data_dictionary_agent.cli \
  --input sample_data/crm_contacts/contacts_clean.csv \
  --output-dir outputs/crm_contacts_profile
```

Deterministic + LLM suggestions:
```bash
python -m data_dictionary_agent.cli --input sample_data/crm_contacts/contacts_clean.csv --llm-descriptions --output-dir outputs/crm_contacts_llm
```

Agent mode:
```bash
python -m data_dictionary_agent.cli \
  --input sample_data/crm_contacts/contacts_clean.csv \
  --config config/examples/crm_context.yaml \
  --mode agent \
  --output-dir outputs/crm_contacts_agent
```

Agent + LLM suggestions:
```bash
python -m data_dictionary_agent.cli --input sample_data/crm_contacts/contacts_clean.csv --config config/examples/crm_context.yaml --mode agent --llm-descriptions --output-dir outputs/crm_contacts_agent_llm
```

## Outputs

Always:
- `profiling_trace.json`
- `data_dictionary.json`
- `data_dictionary.csv`
- `data_dictionary.md`
- `suggested_overrides.yaml`

Agent mode:
- `agent_trace.json`
- `agent_report.md`

When `--llm-descriptions` is used:
- `llm_safe_summary.json`
- `llm_description_suggestions.json`
- `llm_description_suggestions.md`

## Limitations

- No formal sensitive-data compliance classification.
- No framework-based orchestration.
- LLM suggestions require human review.
- LLM suggestions do not replace governed business definitions.
