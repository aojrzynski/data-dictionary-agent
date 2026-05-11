# Agent mode

Agent mode adds bounded local orchestration over deterministic evidence.

## What it does
- Runs the existing deterministic profiling + dictionary pipeline.
- Records plan steps, decisions, assumptions, caveats, and review items in `agent_trace.json`.
- Produces a readable `agent_report.md`.

## What it does not do
- No LLM usage.
- No autonomous/open-ended reasoning.
- No orchestration framework.

## Run
```bash
python -m data_dictionary_agent.cli \
  --input sample_data/crm_contacts/contacts_clean.csv \
  --config config/examples/crm_context.yaml \
  --mode agent \
  --output-dir outputs/crm_contacts_agent
```
