# LLM boundary

- Possible sensitive fields are redacted before LLM use.
- Non-sensitive fields may include a small capped set of sample/top values.
- Raw full rows are not sent.
- Large payloads are avoided by capping/truncation.
- The exact safe summary sent to the LLM path is written to `llm_safe_summary.json` for inspection.
- If LLM is unavailable or output is invalid, deterministic fallback suggestions are generated.
- LLM suggestions are optional wording help and are not authoritative.
