"""Tests for the AI tutor and local config — fully mocked, no network calls."""

from __future__ import annotations

import types

import pytest

from python_mastery_cli import config
from python_mastery_cli.ai_tutor import AITutor, AITutorError, recommend_cheap_model
from python_mastery_cli.models import Lesson, Level


# --------------------------------------------------------------------------- #
# Fake OpenAI clients (duck-typed to the SDK's shape)
# --------------------------------------------------------------------------- #
def _response(content: str):
    return types.SimpleNamespace(
        choices=[types.SimpleNamespace(message=types.SimpleNamespace(content=content))]
    )


class RecordingClient:
    """Captures every create() call and returns canned content."""

    def __init__(self, content: str = "Mocked answer") -> None:
        self.calls: list[dict] = []
        self.content = content
        self.chat = types.SimpleNamespace(
            completions=types.SimpleNamespace(create=self._create)
        )

    def _create(self, **kwargs):
        self.calls.append(dict(kwargs))
        return _response(self.content)


class FussyClient:
    """Rejects max_tokens once (like gpt-5.x / o-series), then succeeds."""

    def __init__(self) -> None:
        self.calls: list[dict] = []
        self.chat = types.SimpleNamespace(
            completions=types.SimpleNamespace(create=self._create)
        )

    def _create(self, **kwargs):
        self.calls.append(dict(kwargs))
        if "max_tokens" in kwargs:
            raise RuntimeError(
                "Unsupported parameter: 'max_tokens' is not supported with this "
                "model. Use 'max_completion_tokens' instead."
            )
        if "temperature" in kwargs:
            raise RuntimeError("temperature: only the default (1) value is supported.")
        return _response("adapted answer")


@pytest.fixture
def isolated_home(tmp_path, monkeypatch):
    """Point config at an empty temp dir and clear env-var overrides."""
    monkeypatch.setenv("PYTHON_MASTERY_HOME", str(tmp_path))
    for var in ("OPENAI_API_KEY", "OPENAI_MODEL", "OPENAI_BASE_URL"):
        monkeypatch.delenv(var, raising=False)
    return tmp_path


def _lesson() -> Lesson:
    return Lesson(
        id="x01",
        title="Generators",
        level=Level.ADVANCED,
        estimated_minutes=10,
        explanation="Generators yield values lazily.",
        key_terms={"yield": "emit a value and pause"},
    )


# --------------------------------------------------------------------------- #
# Config
# --------------------------------------------------------------------------- #
def test_config_round_trips_and_is_chmod_600(isolated_home):
    assert config.get_api_key() is None
    assert config.get_model() == config.DEFAULT_MODEL

    path = config.set_api_key("sk-test-123")
    config.set_model("gpt-test")

    assert config.get_api_key() == "sk-test-123"
    assert config.get_model() == "gpt-test"
    assert path == config.config_path()
    # 0600 permissions on the secret-bearing file.
    assert (path.stat().st_mode & 0o777) == 0o600


def test_env_var_overrides_stored_key(isolated_home, monkeypatch):
    config.set_api_key("stored-key")
    monkeypatch.setenv("OPENAI_API_KEY", "env-key")
    assert config.get_api_key() == "env-key"


# --------------------------------------------------------------------------- #
# Availability
# --------------------------------------------------------------------------- #
def test_not_available_without_key(isolated_home):
    tutor = AITutor()
    assert tutor.is_available() is False
    assert "configure" in tutor.unavailable_reason().lower()


def test_available_with_injected_client_and_key():
    tutor = AITutor(api_key="x", client=RecordingClient())
    assert tutor.is_available() is True


def test_complete_raises_without_key_or_client(isolated_home):
    tutor = AITutor()
    with pytest.raises(AITutorError):
        tutor.complete([{"role": "user", "content": "hi"}])


# --------------------------------------------------------------------------- #
# Completion behaviour
# --------------------------------------------------------------------------- #
def test_complete_returns_text_and_sends_model():
    client = RecordingClient("hello there")
    tutor = AITutor(model="gpt-test", api_key="x", client=client)
    out = tutor.complete([{"role": "user", "content": "hi"}])
    assert out == "hello there"
    assert client.calls[0]["model"] == "gpt-test"


def test_complete_adapts_unsupported_params():
    client = FussyClient()
    tutor = AITutor(model="gpt-5.x-nano", api_key="x", client=client)
    out = tutor.complete([{"role": "user", "content": "hi"}], max_tokens=200, temperature=0.4)
    assert out == "adapted answer"
    final = client.calls[-1]
    assert "max_tokens" not in final
    assert final["max_completion_tokens"] == 200
    assert "temperature" not in final


# --------------------------------------------------------------------------- #
# Prompt construction
# --------------------------------------------------------------------------- #
def test_lesson_context_includes_title_and_explanation():
    ctx = AITutor.lesson_context(_lesson())
    assert "Generators" in ctx
    assert "lazily" in ctx
    assert "yield" in ctx


def test_lesson_context_none_is_empty():
    assert AITutor.lesson_context(None) == ""


def test_answer_builds_grounded_messages():
    client = RecordingClient("ok")
    tutor = AITutor(api_key="x", client=client)
    tutor.answer("What is yield?", _lesson())
    messages = client.calls[0]["messages"]
    roles = [m["role"] for m in messages]
    assert roles[0] == "system"  # tutor persona
    assert any("Generators" in m["content"] for m in messages)  # lesson context
    assert messages[-1]["role"] == "user"
    assert "What is yield?" in messages[-1]["content"]


def test_tutor_actions_invoke_the_model():
    client = RecordingClient("response")
    tutor = AITutor(api_key="x", client=client)
    assert tutor.explain_more(_lesson()) == "response"
    assert tutor.another_example(_lesson()) == "response"
    assert tutor.go_deeper(_lesson()) == "response"
    assert len(client.calls) == 3


# --------------------------------------------------------------------------- #
# Model recommendation heuristic
# --------------------------------------------------------------------------- #
def test_recommend_prefers_nano_then_newest():
    ids = [
        "gpt-4o",
        "gpt-4o-mini",
        "gpt-4.1-mini",
        "gpt-4.1-nano",
        "gpt-5.4-nano",
        "text-embedding-3-small",
        "whisper-1",
    ]
    assert recommend_cheap_model(ids) == "gpt-5.4-nano"


def test_recommend_falls_back_to_mini_when_no_nano():
    ids = ["gpt-4o", "gpt-4.1-mini", "gpt-4o-mini"]
    assert recommend_cheap_model(ids) == "gpt-4.1-mini"


def test_recommend_returns_none_when_nothing_cheap():
    assert recommend_cheap_model(["gpt-4o", "whisper-1", "dall-e-3"]) is None


def test_model_property():
    assert AITutor(model="m", api_key="x").model == "m"


def test_complete_raises_on_nonadaptable_error():
    class Bad:
        def __init__(self):
            self.chat = types.SimpleNamespace(
                completions=types.SimpleNamespace(create=self._c)
            )

        def _c(self, **kwargs):
            raise ValueError("boom")

    tutor = AITutor(api_key="x", client=Bad())
    with pytest.raises(AITutorError):
        tutor.complete([{"role": "user", "content": "hi"}])


def test_recommend_skips_non_openai_models():
    assert recommend_cheap_model(["mistral-7b", "gpt-4o-mini"]) == "gpt-4o-mini"
