# Interpreting Outputs

`profiling_trace.json` contains:

- Dataset metadata (rows, columns, names, source file info)
- Column-level physical profiling (nulls, distinct counts, inferred physical type, sample values, top values)
- Column-level semantic inference:
  - `semantic_role`
  - `semantic_role_confidence` (`high` / `medium` / `low`)
  - `semantic_role_reasons` (deterministic evidence)
  - `review_required` (whether manual review is recommended)
  - `review_notes` (why review is needed)

`possible_sensitive` is a lightweight hint based on deterministic patterns (primarily names), not a compliance classification or a confirmation of PII.

Treat this artifact as structural evidence and deterministic suggestions for future dictionary generation.
