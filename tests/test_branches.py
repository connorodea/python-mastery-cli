"""Branch-coverage hardening — exercise the *untested side* of conditionals.

These are not bug repros; they close one-directional branches that line coverage
can't see (the kind of place latent bugs hide).
"""

from __future__ import annotations

import types

import pytest

from python_mastery_cli import ai_tutor
from python_mastery_cli.ai_tutor import AITutor
from python_mastery_cli.models import CodeExample, Lesson, Level, QuestionType, QuizQuestion


def _client():
    calls: list[dict] = []

    def create(**kwargs):
        calls.append(kwargs)
        return types.SimpleNamespace(
            choices=[types.SimpleNamespace(message=types.SimpleNamespace(content="ok"))]
        )

    client = types.SimpleNamespace(
        chat=types.SimpleNamespace(completions=types.SimpleNamespace(create=create))
    )
    client.calls = calls
    return client


# --- ai_tutor branches -------------------------------------------------------
def test_lesson_context_without_key_terms():
    lesson = Lesson(id="x", title="T", level=Level.BEGINNER, estimated_minutes=1, explanation="e")
    assert "Key terms" not in AITutor.lesson_context(lesson)  # `if terms:` false branch


def test_answer_without_lesson_emits_no_context_system():
    client = _client()
    AITutor(api_key="x", client=client).answer("hi")  # lesson=None -> `if context:` false
    systems = [m for m in client.calls[0]["messages"] if m["role"] == "system"]
    assert len(systems) == 1  # only the persona, no lesson-context message


def test_explain_code_line_without_surrounding():
    client = _client()
    AITutor(api_key="x", client=client).explain_code_line("x = 1")  # `if surrounding:` false
    assert "surrounding code" not in client.calls[0]["messages"][-1]["content"].lower()


def test_build_client_without_base_url(monkeypatch):
    captured: dict = {}

    class FakeOpenAI:
        def __init__(self, **kwargs):
            captured.update(kwargs)

    monkeypatch.setattr(ai_tutor, "OpenAI", FakeOpenAI)
    AITutor(api_key="x")._get_client()  # `if self._base_url:` false branch
    assert "base_url" not in captured


# --- models branches ---------------------------------------------------------
def test_quiz_question_accepts_enum_qtype():
    # `if isinstance(self.qtype, str)` false branch (already an enum).
    q = QuizQuestion(question="q", qtype=QuestionType.FILL_BLANK, correct_answer="a")
    assert q.qtype is QuestionType.FILL_BLANK


def test_code_example_without_line_notes():
    # `for line_no in self.line_notes:` loop body never runs.
    ex = CodeExample(title="t", code="a = 1\nb = 2")
    assert ex.has_walkthrough is False
