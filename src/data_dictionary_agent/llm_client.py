from __future__ import annotations

import os


def request_llm_suggestions(prompt: str, model: str | None = None, client: object | None = None) -> tuple[str | None, list[str], bool, str]:
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

    try:
        response = client.responses.create(
            model=chosen_model,
            input=prompt,
            temperature=0,
        )
        return response.output_text, warnings, True, chosen_model
    except Exception as exc:
        warnings.append(f"LLM request failed; deterministic fallback suggestions were generated. Error: {exc}")
        return None, warnings, False, chosen_model
