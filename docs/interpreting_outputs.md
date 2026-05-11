# Interpreting Outputs

## Core deterministic artifacts

- `profiling_trace.json`: deterministic evidence (dataset structure, column profiling, semantic-signal inputs).
- `data_dictionary.json`: structured first-pass dictionary preserving list fields (`sample_values`, `top_values`, `review_notes`, `caveats`).
- `data_dictionary.csv`: flattened, spreadsheet-friendly dictionary output.
- `data_dictionary.md`: human-readable dictionary summary.
- `suggested_overrides.yaml`: editable review/config scaffold for business-context updates.

## Agent artifacts (agent mode)

- `agent_trace.json`: structured plan, decisions, evidence references, review items, and run summary.
- `agent_report.md`: readable summary of what was run and what still needs review.

## Optional LLM suggestion artifacts (`--llm-descriptions`)

- `llm_safe_summary.json`: redacted/capped summary payload used for suggestion generation.
- `llm_description_suggestions.json`: structured suggestion output.
- `llm_description_suggestions.md`: readable suggestion summary.

## Important caveats

- This is a first-pass dictionary workflow.
- Semantic roles are deterministic suggestions, not confirmed business truth.
- `possible_sensitive` is a review hint, not formal compliance classification.
- LLM description suggestions are optional wording help only.
- Deterministic profiling evidence remains authoritative for observed data facts.
