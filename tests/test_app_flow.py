"""End-to-end glue tests for the interactive flows in ``app.py``.

The interactive prompts are patched so a full lesson, a project, and a
line-by-line walkthrough can be driven deterministically and asserted on,
without a real terminal.
"""

from __future__ import annotations

import pytest

from python_mastery_cli import utils
from python_mastery_cli.app import PythonMasteryApp
from python_mastery_cli.models import (
    CodeExample,
    Exercise,
    Lesson,
    Level,
    Project,
    QuizQuestion,
)


@pytest.fixture
def synthetic_lesson() -> Lesson:
    return Lesson(
        id="t01",
        title="Synthetic Lesson",
        level=Level.BEGINNER,
        estimated_minutes=5,
        explanation="A made-up lesson used purely to exercise the flow.",
        key_terms={"Thing": "A test thing."},
        code_examples=[
            CodeExample(
                title="Tiny snippet",
                code="x = 1\nprint(x)",
                output="1",
                line_notes={1: "Assign 1 to x.", 2: "Print x."},
            )
        ],
        common_mistakes=["Forgetting this is a test."],
        practice_prompts=["What did you learn?"],
        quiz_questions=[
            QuizQuestion(
                question="Pick the first option.",
                qtype="multiple_choice",
                options=["right", "wrong"],
                correct_answer="right",
            ),
        ],
        mini_exercise=Exercise(
            id="t01-ex",
            title="Drill",
            instructions="Do the thing.",
            solution="print('done')",
        ),
        next_lesson_id=None,
    )


@pytest.fixture
def patched_prompts(monkeypatch):
    """Patch every interactive helper with deterministic, non-blocking answers."""

    def fake_confirm(prompt, *, default=False):
        t = str(prompt).lower()
        if "coding drill" in t:  # "Ready for the coding drill?"
            return True
        if "did you complete" in t:
            return True
        if "mark this project complete" in t:
            return True
        return False  # decline walkthroughs / solution reveals / extra hints

    def fake_menu(title, options, **kwargs):
        for i, option in enumerate(options, start=1):
            if "mark" in str(option).lower():
                return i
        return len(options)

    def fake_ask(prompt, *, default=None, choices=None):
        if choices:
            return choices[0]
        return default if default is not None else ""

    monkeypatch.setattr(utils, "confirm", fake_confirm)
    monkeypatch.setattr(utils, "menu", fake_menu)
    monkeypatch.setattr(utils, "ask", fake_ask)
    monkeypatch.setattr(utils, "pause", lambda *a, **k: None)
    monkeypatch.setattr(utils, "clear", lambda *a, **k: None)


def test_run_lesson_marks_everything_complete(tmp_path, synthetic_lesson, patched_prompts):
    app = PythonMasteryApp(progress_path=tmp_path / "p.json")
    app.run_lesson(synthetic_lesson)

    assert app.progress.is_lesson_complete("t01")
    assert app.progress.is_exercise_complete("t01-ex")
    assert "t01::quiz" in app.progress.completed_quizzes
    assert app.progress.total_score > 0
    # Progress was persisted to disk.
    assert (tmp_path / "p.json").exists()


def test_run_project_marks_complete(tmp_path, patched_prompts):
    project = Project(
        id="t-proj",
        title="Synthetic Project",
        difficulty="easy",
        concepts=["testing"],
        requirements=["Exist."],
        build_guide=["Step one."],
        starter_code="print('start')",
        milestones=["Done."],
        stretch_goals=["More."],
        solution="print('solved')",
    )
    app = PythonMasteryApp(progress_path=tmp_path / "p.json")
    app.run_project(project)
    assert app.progress.is_project_complete("t-proj")


def test_walkthrough_renders_without_error(monkeypatch):
    """Driving the walkthrough nav to 'q' should exit cleanly."""
    monkeypatch.setattr(utils.Prompt, "ask", classmethod(lambda cls, *a, **k: "q"))
    monkeypatch.setattr(utils, "clear", lambda *a, **k: None)
    monkeypatch.setattr(utils, "pause", lambda *a, **k: None)
    # Should simply return without raising.
    utils.walkthrough("x = 1\nprint(x)", {1: "assign", 2: "print"}, title="t")


def test_walkthrough_show_all_then_exit(monkeypatch):
    monkeypatch.setattr(utils.Prompt, "ask", classmethod(lambda cls, *a, **k: "a"))
    monkeypatch.setattr(utils, "clear", lambda *a, **k: None)
    monkeypatch.setattr(utils, "pause", lambda *a, **k: None)
    utils.walkthrough("a = 1\nb = 2", {1: "first"}, title="t")
