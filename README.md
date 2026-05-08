# data-dictionary-agent

A local-first, CLI-first tool that profiles tabular datasets and produces deterministic first-pass data dictionary outputs.

## Why this exists

Before formal documentation, teams need grounded evidence about what is actually in a dataset. This project keeps deterministic profiling as the evidence layer, adds deterministic semantic suggestions, and generates review-friendly dictionary artifacts.

## Authority boundary

- Deterministic profiler: authoritative structural evidence
- Deterministic semantic inference: suggested roles only (not truth)
- Deterministic dictionary outputs: first-pass documentation artifacts
- Future agent mode: not included yet
- Future LLM descriptions: not included yet

## Quick start

```bash
pip install -e ".[dev]"
python -m data_dictionary_agent.cli --input sample_data/crm_contacts/contacts_clean.csv --output-dir outputs/crm_contacts_profile
```

## Example command

```bash
data-dictionary-agent --input sample_data/ecommerce_orders/orders.csv --output-dir outputs/orders_profile
```

## Outputs

- `profiling_trace.json` (deterministic evidence and semantic suggestions)
- `data_dictionary.json` (structured dictionary)
- `data_dictionary.csv` (spreadsheet-friendly dictionary)
- `data_dictionary.md` (human-readable dictionary)

## Limitations

- No config override rules yet
- No agent mode yet
- No LLM-generated descriptions yet
- No formal sensitive-data compliance classification
