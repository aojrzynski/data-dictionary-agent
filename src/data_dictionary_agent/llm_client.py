"""Thin wrapper for optional LLM calls used in description suggestion mode.

If credentials/client support are unavailable, deterministic fallback behavior
is surfaced to callers via warnings and status flags.
"""

from __future__ import annotations

import os


def _is_unsupported_response_format_error(exc: Exception) -> bool:
    if isinstance(exc, TypeError):
        return True
    msg = str(exc).lower()
    needles = (
        "unexpected keyword",
        "unknown parameter",
        "unsupported parameter",
        "response_format",
    )
    return any(n in msg for n in needles)


def request_llm_suggestions(prompt: str, model: str | None = None, client: object | None = None) -> tuple[str | None, list[str], bool, str]:
    """Request suggestion JSON text from an LLM, with safe fallback metadata."""
    warnings: list[str] = []
    chosen_model = model or os.getenv("OPENAI_MODEL") or "gpt-4o-mini"
    if client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            warnings.append("OPENAI_API_KEY was not set; deterministic fallback suggestions were generated.")
            return None, warnings, False, chosen_model
        try:
            from openai import OpenAI
        except Exception:
            warnings.append("openai package is not installed; deterministic fallback suggestions were generated.")
            return None, warnings, False, chosen_model
        client = OpenAI(api_key=api_key)

    base_kwargs = {
        "model": chosen_model,
        "input": prompt,
        "temperature": 0,
    }

    try:
        response = client.responses.create(**base_kwargs, response_format={"type": "json_object"})
        return response.output_text, warnings, True, chosen_model
    except Exception as exc:
        if not _is_unsupported_response_format_error(exc):
            warnings.append(f"LLM request failed; deterministic fallback suggestions were generated. Error: {exc}")
            return None, warnings, False, chosen_model

        warnings.append(
            "Structured JSON response request was not supported; retried without it and will validate the returned text."
        )
        try:
            response = client.responses.create(**base_kwargs)
            return response.output_text, warnings, True, chosen_model
        except Exception as retry_exc:
            warnings.append(f"LLM request failed; deterministic fallback suggestions were generated. Error: {retry_exc}")
            return None, warnings, False, chosen_model
