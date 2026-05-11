# Agent Mode

Agent mode adds bounded local orchestration over the same deterministic pipeline.

## What it does

- Runs the deterministic intake, profiling, semantic inference, config-merge, and dictionary flow.
- Records run plan steps, decisions, assumptions, caveats, and review items.
- Produces agent artifacts for traceability and human review.

## What it writes

- `agent_trace.json`
- `agent_report.md`

## What it does not do

- No autonomous open-ended behavior.
- No framework-based orchestration.
- No replacement of deterministic evidence with generated text.

## Run

```bash
python -m data_dictionary_agent.cli \
  --input sample_data/crm_contacts/contacts_clean.csv \
  --config config/examples/crm_context.yaml \
  --mode agent \
  --output-dir outputs/crm_contacts_agent
```

Optional LLM description suggestions can also be enabled with `--llm-descriptions`. They stay separate and non-authoritative.
