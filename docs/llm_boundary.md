# LLM boundary
Only safe summaries are sent to the LLM, never raw row-level data.
Possible sensitive fields are redacted in `llm_safe_summary.json`.
If LLM access is unavailable, deterministic fallback suggestions are generated.
LLM output is optional wording help and is not authoritative.
All suggestions require human review.
