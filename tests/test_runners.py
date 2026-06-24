"""Tests for the interactive quiz and exercise runners + the code runner."""

from __future__ import annotations

import pytest

from python_mastery_cli import exercises, quiz, runner, utils
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
        QuizQuestion(question="TF", qtype="true_false", correct_answer="true"),
        QuizQuestion(question="Fill", qtype="fill_blank", correct_answer="x", explanation="e"),
        QuizQuestion(question="Short", qtype="short_answer", correct_answer="list",
                     keywords=["list"], explanation="e2"),
    ]


def test_run_quiz_empty_returns_zero():
    assert quiz.run_quiz([], title="Empty").total == 0


def test_run_quiz_pass(monkeypatch):
    _iter_patch(monkeypatch, "ask", ["1", "false", "x", "a list"])
    result = quiz.run_quiz(_questions(), title="Q")
    assert result.total == 4 and result.correct == 3 and result.passed is True


def test_run_quiz_fail(monkeypatch):
    _iter_patch(monkeypatch, "ask", ["2", "false", "wrong", "nope"])
    result = quiz.run_quiz(_questions(), title="Q")
    assert result.correct <= 1 and result.passed is False


# --------------------------------------------------------------------------- #
# runner.py — real subprocess execution
# --------------------------------------------------------------------------- #
def test_runner_captures_stdout_and_is_ok():
    r = runner.run_code('print("hi")')
    assert r.stdout.strip() == "hi"
    assert r.ok is True


def test_runner_reports_errors():
    r = runner.run_code('raise ValueError("boom")')
    assert r.ok is False
    assert "ValueError" in r.stderr


def test_runner_times_out():
    r = runner.run_code("import time; time.sleep(5)", timeout=0.3)
    assert r.timed_out is True
    assert r.ok is False


def test_output_matches_normalizes_whitespace():
    assert runner.output_matches("hi\n", "hi") is True
    assert runner.output_matches("a   \nb  ", "a\nb") is True
    assert runner.output_matches("x", "y") is False


# --------------------------------------------------------------------------- #
# Exercise runner — static display + the menu loop (menu prompts patched)
# --------------------------------------------------------------------------- #
def test_show_exercise_with_and_without_extras(capsys):
    full = Exercise(id="e1", title="Full", instructions="do", starter_code="x=1",
                    expected_output="1", hints=["h"], solution="x=1")
    bare = Exercise(id="e2", title="Bare", instructions="do")
    exercises.show_exercise(full)
    exercises.show_exercise(bare)
    out = capsys.readouterr().out
    assert "Full" in out and "Bare" in out


def test_run_exercise_hints_reveal_then_mark_complete(monkeypatch):
    ex = Exercise(id="e1", title="Drill", instructions="do it", starter_code="...",
                  expected_output="42", hints=["h1", "h2", "h3"], solution="print(42)")
    # menu: hints (break early), hints again (walk all), reveal, mark complete
    _iter_patch(monkeypatch, "menu", [2, 2, 3, 4])
    _iter_patch(monkeypatch, "confirm", [False, True, True, True, True])
    monkeypatch.setattr(utils, "walkthrough", lambda *a, **k: None)
    assert exercises.run_exercise(ex) is True


def test_run_exercise_no_hints_no_solution_then_skip(monkeypatch):
    ex = Exercise(id="e2", title="Bare", instructions="do it")
    _iter_patch(monkeypatch, "menu", [2, 3, 5])  # hints(none), reveal(none), skip
    assert exercises.run_exercise(ex) is False


def test_run_exercise_decline_completion_then_skip(monkeypatch):
    ex = Exercise(id="e3", title="X", instructions="do", solution="pass")
    _iter_patch(monkeypatch, "menu", [4, 5])  # mark complete -> decline; then skip
    _iter_patch(monkeypatch, "confirm", [False])
    assert exercises.run_exercise(ex) is False


def test_run_exercise_reveal_then_decline_walkthrough_then_skip(monkeypatch):
    ex = Exercise(id="e", title="X", instructions="i", solution="print(1)")
    _iter_patch(monkeypatch, "menu", [3, 5])      # reveal, then skip
    _iter_patch(monkeypatch, "confirm", [False])  # decline the walkthrough offer
    assert exercises.run_exercise(ex) is False


# --------------------------------------------------------------------------- #
# Run & check my solution (the new feedback loop)
# --------------------------------------------------------------------------- #
def test_run_exercise_run_and_check_pass_then_complete(monkeypatch):
    ex = Exercise(id="rc", title="X", instructions="i", expected_output="42")
    _iter_patch(monkeypatch, "menu", [1])
    monkeypatch.setattr(utils, "read_multiline", lambda *a, **k: "print(42)")
    monkeypatch.setattr(runner, "run_code", lambda code, **k: runner.RunResult("42\n", "", 0))
    _iter_patch(monkeypatch, "confirm", [True])  # "Mark this drill complete?"
    assert exercises.run_exercise(ex) is True


def test_run_exercise_run_and_check_mismatch_then_skip(monkeypatch):
    ex = Exercise(id="rc", title="X", instructions="i", expected_output="42")
    _iter_patch(monkeypatch, "menu", [1, 5])  # run&check (mismatch) -> loop -> skip
    monkeypatch.setattr(utils, "read_multiline", lambda *a, **k: "print(99)")
    monkeypatch.setattr(runner, "run_code", lambda code, **k: runner.RunResult("99\n", "", 0))
    assert exercises.run_exercise(ex) is False


def test_run_and_check_empty_code(monkeypatch):
    ex = Exercise(id="e", title="X", instructions="i", expected_output="1")
    monkeypatch.setattr(utils, "read_multiline", lambda *a, **k: "   ")
    assert exercises._run_and_check(ex) is False


def test_run_and_check_timeout(monkeypatch):
    ex = Exercise(id="e", title="X", instructions="i", expected_output="1")
    monkeypatch.setattr(utils, "read_multiline", lambda *a, **k: "while True: pass")
    monkeypatch.setattr(runner, "run_code", lambda code, **k: runner.RunResult("", "", -1, timed_out=True))
    assert exercises._run_and_check(ex) is False


def test_run_and_check_error_output(monkeypatch):
    ex = Exercise(id="e", title="X", instructions="i", expected_output="1")
    monkeypatch.setattr(utils, "read_multiline", lambda *a, **k: "boom")
    monkeypatch.setattr(runner, "run_code", lambda code, **k: runner.RunResult("", "NameError: boom", 1))
    assert exercises._run_and_check(ex) is False  # no stdout + error shown


def test_run_and_check_no_expected_output(monkeypatch):
    ex = Exercise(id="e", title="X", instructions="i")  # no expected_output
    monkeypatch.setattr(utils, "read_multiline", lambda *a, **k: "print(1)")
    monkeypatch.setattr(runner, "run_code", lambda code, **k: runner.RunResult("1\n", "", 0))
    assert exercises._run_and_check(ex) is False


def test_run_code_handles_non_utf8_output():
    # BUG: non-UTF-8 bytes on stdout used to raise UnicodeDecodeError (only
    # TimeoutExpired was caught), crashing the drill. Must decode safely instead.
    r = runner.run_code(r'import sys; sys.stdout.buffer.write(b"\xff\xfe")')
    assert r.ok  # didn't crash


def test_run_code_does_not_read_external_stdin():
    # BUG: a drill calling input() inherited (stole) the CLI's stdin. It must
    # get a closed stdin (EOF) instead — never block on or consume the parent's.
    r = runner.run_code("print(input())")
    assert not r.ok
    assert "EOFError" in r.stderr
