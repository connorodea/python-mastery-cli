"""Tests for the interactive quiz and exercise runners (prompts patched)."""

from __future__ import annotations

import pytest

from python_mastery_cli import exercises, quiz, utils
from python_mastery_cli.models import Exercise, QuizQuestion


def _iter_patch(monkeypatch, name, values):
    it = iter(values)
    monkeypatch.setattr(utils, name, lambda *a, **k: next(it))


@pytest.fixture(autouse=True)
def _quiet(monkeypatch):
    monkeypatch.setattr(utils, "pause", lambda *a, **k: None)
    monkeypatch.setattr(utils, "clear", lambda *a, **k: None)


# --------------------------------------------------------------------------- #
# Quiz runner
# --------------------------------------------------------------------------- #
def _questions():
    return [
        QuizQuestion(question="MC", qtype="multiple_choice", options=["a", "b"],
                     correct_answer="a", explanation="exp"),
        QuizQuestion(question="TF", qtype="true_false", correct_answer="true"),  # no explanation
        QuizQuestion(question="Fill", qtype="fill_blank", correct_answer="x", explanation="e"),
        QuizQuestion(question="Short", qtype="short_answer", correct_answer="list",
                     keywords=["list"], explanation="e2"),
    ]


def test_run_quiz_empty_returns_zero():
    result = quiz.run_quiz([], title="Empty")
    assert result.total == 0


def test_run_quiz_pass(monkeypatch):
    # 3/4 correct -> 75% -> passed. Answers exercise all four prompt types.
    _iter_patch(monkeypatch, "ask", ["1", "false", "x", "a list"])
    result = quiz.run_quiz(_questions(), title="Q")
    assert result.total == 4
    assert result.correct == 3
    assert result.passed is True


def test_run_quiz_fail(monkeypatch):
    _iter_patch(monkeypatch, "ask", ["2", "false", "wrong", "nope"])
    result = quiz.run_quiz(_questions(), title="Q")
    assert result.correct <= 1
    assert result.passed is False


# --------------------------------------------------------------------------- #
# Exercise runner
# --------------------------------------------------------------------------- #
def test_show_exercise_with_and_without_extras(capsys):
    full = Exercise(id="e1", title="Full", instructions="do", starter_code="x=1",
                    expected_output="1", hints=["h"], solution="x=1")
    bare = Exercise(id="e2", title="Bare", instructions="do")
    exercises.show_exercise(full)
    exercises.show_exercise(bare)
    out = capsys.readouterr().out
    assert "Full" in out and "Bare" in out


def test_run_exercise_full_path_marks_complete(monkeypatch):
    ex = Exercise(
        id="e1", title="Drill", instructions="do it",
        starter_code="...", expected_output="42",
        hints=["h1", "h2", "h3"], solution="print(42)",
    )
    # menu: hints (break early), hints again (walk through all), reveal, complete
    _iter_patch(monkeypatch, "menu", [1, 1, 2, 3])
    # confirms in order: another-hint? -> No (break); then Yes, Yes (walk all);
    # walkthrough solution? -> Yes; completed? -> Yes
    _iter_patch(monkeypatch, "confirm", [False, True, True, True, True])
    monkeypatch.setattr(utils, "walkthrough", lambda *a, **k: None)
    assert exercises.run_exercise(ex) is True


def test_run_exercise_no_hints_no_solution_then_skip(monkeypatch):
    ex = Exercise(id="e2", title="Bare", instructions="do it")
    _iter_patch(monkeypatch, "menu", [1, 2, 4])  # hints(none), reveal(none), skip
    assert exercises.run_exercise(ex) is False


def test_run_exercise_decline_completion_then_skip(monkeypatch):
    ex = Exercise(id="e3", title="X", instructions="do", solution="pass")
    _iter_patch(monkeypatch, "menu", [3, 4])  # mark complete -> decline; then skip
    _iter_patch(monkeypatch, "confirm", [False])  # "Did you complete...?" -> No
    assert exercises.run_exercise(ex) is False
