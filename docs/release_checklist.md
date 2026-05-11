# Release Checklist

Manual release readiness checklist for maintainers.

## Commands

### Full tests

```bash
python -m pytest
```

### Deterministic smoke

```bash
python -m data_dictionary_agent.cli --input sample_data/crm_contacts/contacts_clean.csv --output-dir outputs/release_check_profile
```

### Config smoke

```bash
python -m data_dictionary_agent.cli --input sample_data/crm_contacts/contacts_clean.csv --config config/examples/crm_context.yaml --output-dir outputs/release_check_config
```

### Agent smoke

```bash
python -m data_dictionary_agent.cli --input sample_data/crm_contacts/contacts_clean.csv --config config/examples/crm_context.yaml --mode agent --output-dir outputs/release_check_agent
```

### LLM fallback smoke

```bash
python -m data_dictionary_agent.cli --input sample_data/crm_contacts/contacts_clean.csv --config config/examples/crm_context.yaml --llm-descriptions --output-dir outputs/release_check_llm
```

### Agent + LLM fallback smoke

```bash
python -m data_dictionary_agent.cli --input sample_data/crm_contacts/contacts_clean.csv --config config/examples/crm_context.yaml --mode agent --llm-descriptions --output-dir outputs/release_check_agent_llm
```

## Expected files checklist

For each run, confirm expected artifacts are present and readable:

- Deterministic base artifacts:
  - `profiling_trace.json`
  - `data_dictionary.md`
  - `data_dictionary.csv`
  - `data_dictionary.json`
  - `suggested_overrides.yaml`
- Agent artifacts (agent mode runs):
  - `agent_trace.json`
  - `agent_report.md`
- Optional LLM suggestion artifacts (`--llm-descriptions` runs):
  - `llm_safe_summary.json`
  - `llm_description_suggestions.json`
  - `llm_description_suggestions.md`

## Final manual checks

- Inspect generated artifacts for expected structure and readability.
- Check README links and key docs links.
- Confirm GitHub repo description text.
- Add/update GitHub topics/tags.
- Create release tag and GitHub release notes.
- Optional: prepare social/preview image.
