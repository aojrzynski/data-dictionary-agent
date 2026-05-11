# Hybrid Agent in This Repository

In this repo, **hybrid agent** means a bounded combination of evidence, inference, human context, and optional wording support.

It is not just “code plus LLM.”

## The hybrid parts

1. **Deterministic evidence**
   - Profiling captures observed data facts.
   - This is the authority for what is physically present in the dataset.

2. **Deterministic semantic inference**
   - Rule-based logic suggests likely semantic roles.
   - These are suggestions to review, not guaranteed business truth.

3. **Human config/context**
   - Optional YAML overrides add known business metadata.
   - This allows human owners to provide context deterministic profiling cannot infer.

4. **Bounded orchestration**
   - Agent mode plans and executes within fixed steps.
   - It records decisions and review items in trace/report artifacts.

5. **Safe LLM wording suggestions (optional)**
   - LLM suggestions draft wording from redacted/capped safe summaries.
   - Suggestions are separate, optional, and non-authoritative.

6. **Review artifacts**
   - `suggested_overrides.yaml`, `agent_trace.json`, and `agent_report.md` support review and refinement.

## Why this pattern is useful for data documentation

Data documentation needs both reliable evidence and readable descriptions.

This pattern helps by:
- keeping observed facts deterministic,
- making suggested interpretation explicit,
- allowing human context where needed,
- and using LLMs only for wording assistance under clear boundaries.
