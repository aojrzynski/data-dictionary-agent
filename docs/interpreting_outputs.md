# Interpreting Outputs

- `profiling_trace.json`: deterministic evidence (dataset structure, column profiling, semantic suggestion signals).
- `data_dictionary.json`: structured first-pass dictionary preserving lists (`sample_values`, `top_values`, `review_notes`, `caveats`).
- `data_dictionary.csv`: spreadsheet-friendly flattened dictionary for tools like Excel.
- `data_dictionary.md`: human-readable summary and column documentation for quick review.

## Important caveats

- This is a first-pass deterministic dictionary.
- Semantic roles are suggestions, not confirmed business truth.
- `possible_sensitive` is a hint, not formal compliance classification.
- Human review is required before formal publication.

`suggested_overrides.yaml` contains editable dataset/column fields for human confirmation.


## Agent outputs
- `agent_trace.json`: structured plan, decisions, evidence, review items, and run summary.
- `agent_report.md`: human-readable summary of what the agent did and what needs review.
