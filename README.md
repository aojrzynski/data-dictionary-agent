# data-dictionary-agent

A local-first, CLI-first project that profiles tabular datasets and emits deterministic trace artifacts.

## Why this exists

Before you can generate a useful data dictionary, you need grounded evidence about what is actually in the data. This milestone builds that evidence layer first, and now adds deterministic semantic role suggestions.

## Why not just ask an LLM?

LLMs can help explain findings, but they are not reliable as the source of truth for raw dataset structure. This project establishes deterministic profiling as the authority, then layers optional agent and LLM capabilities later.

## Authority boundary (v2 direction)

- Deterministic profiler: authoritative structural evidence
- Deterministic semantic inference: suggested roles only (not truth)
- Future agent mode: orchestration over deterministic evidence
- Future LLM descriptions: suggested wording only, never authoritative facts

## Quick start

```bash
pip install -e ".[dev]"
python -m data_dictionary_agent.cli --input sample_data/crm_contacts/contacts_clean.csv --output-dir outputs/crm_contacts_profile
```

## Example command

```bash
data-dictionary-agent --input sample_data/ecommerce_orders/orders.csv --output-dir outputs/orders_profile
```

## Output artifact

- `profiling_trace.json`: dataset-level structural profiling plus column-level semantic inference fields (`semantic_role`, `semantic_role_confidence`, `semantic_role_reasons`, `review_required`, `review_notes`).

## Limitations and non-goals (this milestone)

- No agent mode yet
- No LLM support yet
- No final data dictionary outputs yet
