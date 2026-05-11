from data_dictionary_agent.llm_client import request_llm_suggestions


class _Response:
    def __init__(self, output_text: str):
        self.output_text = output_text


def test_request_uses_response_format_when_supported():
    calls = []

    class _Responses:
        @staticmethod
        def create(**kwargs):
            calls.append(kwargs)
            return _Response('{"columns":[]}')

    client = type("C", (), {"responses": _Responses})()
    text, warnings, used, model = request_llm_suggestions("prompt", client=client)
    assert text == '{"columns":[]}'
    assert warnings == []
    assert used is True
    assert model == "gpt-4o-mini"
    assert "response_format" in calls[0]


def test_request_retries_without_response_format_on_type_error():
    calls = []

    class _Responses:
        @staticmethod
        def create(**kwargs):
            calls.append(kwargs)
            if "response_format" in kwargs:
                raise TypeError("unexpected keyword argument 'response_format'")
            return _Response('{"columns":[]}')

    client = type("C", (), {"responses": _Responses})()
    text, warnings, used, _ = request_llm_suggestions("prompt", client=client)
    assert text == '{"columns":[]}'
    assert used is True
    assert len(calls) == 2
    assert "response_format" in calls[0]
    assert "response_format" not in calls[1]
    assert any("retried without it" in w for w in warnings)


def test_request_falls_back_when_both_attempts_fail():
    class _Responses:
        @staticmethod
        def create(**kwargs):
            if "response_format" in kwargs:
                raise TypeError("unexpected keyword argument 'response_format'")
            raise RuntimeError("network down")

    client = type("C", (), {"responses": _Responses})()
    text, warnings, used, _ = request_llm_suggestions("prompt", client=client)
    assert text is None
    assert used is False
    assert any("LLM request failed; deterministic fallback suggestions were generated." in w for w in warnings)


def test_request_falls_back_when_no_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    text, warnings, used, _ = request_llm_suggestions("prompt", client=None)
    assert text is None
    assert used is False
    assert any("OPENAI_API_KEY was not set" in w for w in warnings)
