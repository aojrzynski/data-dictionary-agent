# Example Commands

## Deterministic run

```bash
python -m data_dictionary_agent.cli \
  --input sample_data/crm_contacts/contacts_clean.csv \
  --output-dir outputs/crm_contacts_profile
```

## Deterministic run with config overrides

```bash
python -m data_dictionary_agent.cli \
  --input sample_data/crm_contacts/contacts_clean.csv \
  --config config/examples/crm_context.yaml \
  --output-dir outputs/crm_contacts_with_config
```

## Agent mode run

```bash
python -m data_dictionary_agent.cli \
  --input sample_data/crm_contacts/contacts_clean.csv \
  --config config/examples/crm_context.yaml \
  --mode agent \
  --output-dir outputs/crm_contacts_agent
```

## Deterministic run with optional LLM suggestions

```bash
python -m data_dictionary_agent.cli \
  --input sample_data/crm_contacts/contacts_clean.csv \
  --llm-descriptions \
  --output-dir outputs/crm_contacts_llm
```

## Agent mode run with optional LLM suggestions

```bash
python -m data_dictionary_agent.cli \
  --input sample_data/crm_contacts/contacts_clean.csv \
  --config config/examples/crm_context.yaml \
  --mode agent \
  --llm-descriptions \
  --output-dir outputs/crm_contacts_agent_llm
```

## Expected outputs

Deterministic outputs always include:
- `profiling_trace.json`
- `data_dictionary.md`
- `data_dictionary.csv`
- `data_dictionary.json`
- `suggested_overrides.yaml`

Agent mode also adds:
- `agent_trace.json`
- `agent_report.md`

`--llm-descriptions` also adds:
- `llm_safe_summary.json`
- `llm_description_suggestions.json`
- `llm_description_suggestions.md`
