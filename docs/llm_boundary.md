# LLM Boundary

Optional LLM description suggestions are a wording layer, not a truth layer.

## Rules in this project

- LLM suggestions are optional and off by default.
- Suggestions are written to separate files and do not overwrite `data_dictionary.md/.csv/.json`.
- Possible sensitive fields are redacted in `llm_safe_summary.json`.
- No full raw rows are sent to the LLM.
- Non-sensitive sample/top values are capped and truncated.
- If no API key is available, fallback suggestions are generated.
- LLM output is requested as JSON and then validated/parsing-checked.
- If LLM JSON parsing or validation fails, fallback suggestions are generated.

## Review expectations

- Treat LLM text as draft wording only.
- Keep deterministic profiling evidence as authoritative for observed data facts.
- Confirm business definitions with human owners before publication.
