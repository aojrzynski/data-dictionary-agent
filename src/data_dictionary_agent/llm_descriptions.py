from __future__ import annotations

"""Optional LLM wording suggestions built from safe deterministic summaries.

This module prepares redacted/capped metadata for LLM prompting and validates
responses. It never overwrites deterministic dictionary outputs.
"""
import json
from datetime import datetime, timezone

from data_dictionary_agent.llm_client import request_llm_suggestions


def _truncate(v: object, limit: int = 80) -> object:
    s = str(v)
    return s if len(s) <= limit else s[: limit - 3] + "..."


def build_llm_safe_summary(dictionary: dict, sample_limit: int = 3) -> dict:
    """Build a redacted summary payload safe for optional wording suggestions."""
    cols = []
    for c in dictionary.get("columns", []):
        sensitive = c.get("semantic_role") == "possible_sensitive" or bool(c.get("sensitivity_hint"))
        safe = {
            "column_name": c.get("column_name"), "display_name": c.get("display_name"), "physical_type": c.get("physical_type"),
            "semantic_role": c.get("semantic_role"), "semantic_role_confidence": c.get("semantic_role_confidence"), "null_ratio": c.get("null_ratio"),
            "distinct_count": c.get("distinct_count"), "uniqueness_ratio": c.get("uniqueness_ratio"), "current_description": c.get("description"),
            "description_source": c.get("description_source"), "review_required": c.get("review_required"), "review_notes": c.get("review_notes", []),
            "caveats": c.get("caveats", []), "allowed_values": c.get("allowed_values", []),
        }
        # Redact likely sensitive values before any optional LLM usage.
        if sensitive:
            safe["sample_values"] = ["[REDACTED_POSSIBLE_SENSITIVE]"]
            safe["top_values"] = []
            safe["redaction_reason"] = "Column is possible_sensitive or has a sensitivity hint."
        else:
            safe["sample_values"] = [_truncate(v) for v in (c.get("sample_values") or [])[:sample_limit]]
            safe["top_values"] = [{"value": _truncate(i.get("value")), "count": i.get("count")} for i in (c.get("top_values") or [])[:sample_limit]]
        cols.append(safe)
    return {"dataset": dictionary.get("dataset", {}), "columns": cols}


def _build_prompt(summary: dict) -> str:
    return (
        "You are drafting suggested data dictionary descriptions. Return JSON only with schema: "
        "{\"columns\":[{\"column_name\":\"...\",\"suggested_description\":\"...\",\"confidence\":\"high|medium|low\",\"notes\":[\"...\"]}]}. "
        "Use only provided metadata. Do not invent business meaning. Keep concise and cautious. Mark uncertainty. "
        "Do not claim PII/compliance classification. For possible_sensitive say possible personal/contact/sensitive field, not confirmed.\n"
        f"Metadata:\n{json.dumps(summary, indent=2, sort_keys=True)}"
    )


def build_deterministic_fallback_suggestions(dictionary: dict, reason: str) -> dict:
    columns = []
    for c in dictionary.get("columns", []):
        desc = c.get("description") or f"Field '{c.get('display_name') or c.get('column_name')}' with semantic role '{c.get('semantic_role')}'."
        columns.append({"column_name": c.get("column_name"), "suggested_description": desc, "confidence": "low", "notes": [reason]})
    return {"columns": columns}


def generate_llm_description_suggestions(dictionary: dict, model: str | None = None, client: object | None = None) -> tuple[dict, dict]:
    """Return (safe_summary, suggestions), using deterministic fallback on failure."""
    summary = build_llm_safe_summary(dictionary)
    prompt = _build_prompt(summary)
    text, warnings, llm_used, chosen_model = request_llm_suggestions(prompt, model=model, client=client)
    fallback = build_deterministic_fallback_suggestions(dictionary, "Deterministic fallback was used.")
    parsed = fallback
    source = "deterministic_fallback"
    llm_call_succeeded = llm_used
    # Validate response shape strictly; fallback keeps outputs predictable.
    if llm_used and text:
        try:
            candidate = json.loads(text)
            if isinstance(candidate, dict) and isinstance(candidate.get("columns"), list):
                parsed = candidate
                source = "llm_suggested"
            else:
                warnings.append("LLM response schema was invalid; deterministic fallback suggestions were generated.")
                llm_used = False
                source = "deterministic_fallback"
        except Exception:
            warnings.append("LLM response was not valid JSON; deterministic fallback suggestions were generated.")
            llm_used = False
            source = "deterministic_fallback"
    by_name = {c.get("column_name"): c for c in parsed.get("columns", []) if c.get("column_name")}
    out_cols = []
    for c in dictionary.get("columns", []):
        pick = by_name.get(c.get("column_name"))
        if not pick:
            pick = next(x for x in fallback["columns"] if x["column_name"] == c.get("column_name"))
            warnings.append(f"LLM response missing column {c.get('column_name')}; deterministic fallback used for that column.")
            col_source = "deterministic_fallback"
        else:
            col_source = source
        out_cols.append({
            "column_name": c.get("column_name"),
            "current_description": c.get("description", ""),
            "current_description_source": c.get("description_source", ""),
            "suggested_description": pick.get("suggested_description", ""),
            "suggestion_source": col_source,
            "review_required": True,
            "notes": pick.get("notes", []),
        })
    payload = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(), "llm_requested": True, "llm_call_succeeded": llm_call_succeeded, "llm_used": llm_used,
        "model": chosen_model, "source": source,
        "data_boundary": "Only safe summaries were used. Raw row-level data was not sent.", "warnings": warnings, "columns": out_cols,
    }
    return summary, payload
