"""Interactive-flow coverage for app.py (every menu/screen, prompts patched)."""

from __future__ import annotations

import pytest

from python_mastery_cli import app as app_module
from python_mastery_cli import exercises, quiz, utils
from python_mastery_cli.app import PythonMasteryApp
from python_mastery_cli.ai_tutor import AITutorError
from python_mastery_cli.models import (
    CodeExample,
    Exercise,
    Lesson,
    Level,
    Project,
    QuizQuestion,
)
from python_mastery_cli.quiz import QuizResult


class FakeTutor:
    def __init__(self, available=True):
        self._a = available

    def is_available(self):
        return self._a

    def unavailable_reason(self):
        return "run configure to enable the tutor"

    @property
    def model(self):
        return "fake-model"

    def explain_more(self, lesson):
        return "explain"

    def another_example(self, lesson):
        return "example"

    def go_deeper(self, lesson):
        return "deeper"

    def answer(self, question, lesson=None):
        return f"answer:{question}"


def _script(monkeypatch, *, menu=(), confirm=(), ask=()):
    mi, ci, ai = iter(menu), iter(confirm), iter(ask)
    monkeypatch.setattr(utils, "menu", lambda *a, **k: next(mi))
    monkeypatch.setattr(utils, "confirm", lambda *a, **k: next(ci))
    monkeypatch.setattr(utils, "ask", lambda *a, **k: next(ai))


@pytest.fixture
def app(tmp_path, monkeypatch):
    # Isolate config so the real stored API key never makes the tutor "available"
    # (which could otherwise trigger a live network call during a test).
    monkeypatch.setenv("PYTHON_MASTERY_HOME", str(tmp_path))
    for var in ("OPENAI_API_KEY", "OPENAI_MODEL", "OPENAI_BASE_URL"):
        monkeypatch.delenv(var, raising=False)
    monkeypatch.setattr(utils, "clear", lambda *a, **k: None)
    monkeypatch.setattr(utils, "pause", lambda *a, **k: None)
    monkeypatch.setattr(utils, "walkthrough", lambda *a, **k: None)
    return PythonMasteryApp(progress_path=tmp_path / "p.json")


def _synthetic_lesson():
    return Lesson(
        id="t01", title="Synthetic", level=Level.BEGINNER, estimated_minutes=5,
        explanation="x", key_terms={"a": "b"},
        code_examples=[CodeExample(title="ex", code="x=1\nprint(x)", line_notes={1: "a"})],
        common_mistakes=["m"], practice_prompts=["p"],
        quiz_questions=[QuizQuestion(question="q", qtype="true_false", correct_answer="true")],
        mini_exercise=Exercise(id="t01-ex", title="d", instructions="i", solution="s"),
    )


# --------------------------------------------------------------------------- #
# run() dispatch
# --------------------------------------------------------------------------- #
def test_run_dispatches_all_then_exits(app, monkeypatch):
    recorded = []
    names = [
        "continue_learning", "browse_lessons", "quiz_menu", "practice_drills",
        "build_projects", "ai_tutor_menu", "view_progress", "reset_progress_interactive",
    ]
    for name in names:
        monkeypatch.setattr(app, name, lambda n=name: recorded.append(n))
    monkeypatch.setattr(app, "show_dashboard", lambda: None)
    seq = iter([1, 2, 3, 4, 5, 6, 7, 8, 9])
    monkeypatch.setattr(utils, "menu", lambda *a, **k: next(seq))
    app.run()
    assert recorded == names


def test_run_handles_keyboard_interrupt(app, monkeypatch):
    monkeypatch.setattr(app, "show_dashboard", lambda: None)

    def boom():
        raise KeyboardInterrupt

    monkeypatch.setattr(app, "continue_learning", boom)
    seq = iter([1, 9])
    monkeypatch.setattr(utils, "menu", lambda *a, **k: next(seq))
    app.run()  # must not raise


def test_show_dashboard_renders(app):
    app.show_dashboard()  # fresh -> "up next"


def test_show_dashboard_all_complete(app):
    app.progress.completed_lessons = [lesson.id for lesson in app.lessons]
    app.show_dashboard()  # "all complete" branch


# --------------------------------------------------------------------------- #
# Continue / browse
# --------------------------------------------------------------------------- #
def test_continue_learning_runs_next(app, monkeypatch):
    seen = []
    monkeypatch.setattr(app, "run_lesson", lambda lesson: seen.append(lesson.id))
    app.continue_learning()
    assert seen == [app.lessons[0].id]


def test_continue_learning_all_done(app):
    app.progress.completed_lessons = [lesson.id for lesson in app.lessons]
    app.continue_learning()  # success + pause branch


def test_browse_lessons_back(app, monkeypatch):
    _script(monkeypatch, menu=[4])  # "Back to main menu"
    app.browse_lessons()


def test_browse_lessons_pick_lesson(app, monkeypatch):
    picked = []
    monkeypatch.setattr(app, "run_lesson", lambda lesson: picked.append(lesson.id))
    # choose beginner track, then first lesson
    _script(monkeypatch, menu=[1, 1])
    app.browse_lessons()
    assert picked


def test_browse_level_back(app, monkeypatch):
    beginners = [l for l in app.lessons if str(l.level) == "beginner"]
    _script(monkeypatch, menu=[len(beginners) + 1])  # Back
    app._browse_level("beginner")


# --------------------------------------------------------------------------- #
# Lesson + record
# --------------------------------------------------------------------------- #
def test_run_lesson_review_branch(app, monkeypatch):
    lesson = _synthetic_lesson()
    app.progress.completed_lessons.append(lesson.id)  # already done -> "Reviewed"
    _script(monkeypatch, menu=[], confirm=[False, False], ask=["", ""])
    # confirm: offer walkthrough? No; ready for drill? No.
    app.run_lesson(lesson)
    assert app.progress.is_lesson_complete(lesson.id)


# --------------------------------------------------------------------------- #
# Quizzes
# --------------------------------------------------------------------------- #
def test_quiz_menu_back(app, monkeypatch):
    _script(monkeypatch, menu=[3])
    app.quiz_menu()


def test_quiz_from_lesson(app, monkeypatch):
    monkeypatch.setattr(quiz, "run_quiz", lambda *a, **k: QuizResult(total=2, correct=2, score=10))
    _script(monkeypatch, menu=[1, 1])  # choose "from a lesson", then first quizzable lesson
    app.quiz_menu()
    assert any("::quiz" in q for q in app.progress.completed_quizzes)


def test_mixed_quiz(app, monkeypatch):
    monkeypatch.setattr(quiz, "run_quiz", lambda *a, **k: QuizResult(total=10, correct=8, score=40))
    _script(monkeypatch, menu=[2])
    app.quiz_menu()
    assert "mixed::review" in app.progress.completed_quizzes


def test_mixed_quiz_empty_pool(app):
    # Swap in a local quiz-less lesson list (do NOT mutate the shared cache).
    app.lessons = [
        Lesson(id="z", title="z", level=Level.BEGINNER, estimated_minutes=1, explanation="x")
    ]
    app._mixed_quiz()  # empty pool -> warn + return


# --------------------------------------------------------------------------- #
# Drills + projects
# --------------------------------------------------------------------------- #
def test_practice_drills_pick(app, monkeypatch):
    monkeypatch.setattr(exercises, "run_exercise", lambda *a, **k: True)
    _script(monkeypatch, menu=[1])
    app.practice_drills()
    assert app.progress.completed_exercises


def test_practice_drills_back(app, monkeypatch):
    drills = [l for l in app.lessons if l.has_exercise]
    _script(monkeypatch, menu=[len(drills) + 1])
    app.practice_drills()


def test_build_projects_back(app, monkeypatch):
    _script(monkeypatch, menu=[len(app.projects) + 1])
    app.build_projects()


def test_build_projects_pick(app, monkeypatch):
    seen = []
    monkeypatch.setattr(app, "run_project", lambda p: seen.append(p.id))
    _script(monkeypatch, menu=[1])
    app.build_projects()
    assert seen


def test_run_project_with_reveal_and_walkthrough(app, monkeypatch):
    project = Project(
        id="tp", title="P", difficulty="easy", concepts=["c"], requirements=["r"],
        build_guide=["s"], starter_code="print('a')", milestones=["m"],
        stretch_goals=["g"], solution="print('b')",
    )
    # starter walkthrough? no; reveal solution? yes; solution walkthrough? yes; mark complete? yes
    _script(monkeypatch, menu=[], confirm=[False, True, True, True])
    app.run_project(project)
    assert app.progress.is_project_complete("tp")


# --------------------------------------------------------------------------- #
# Progress + reset
# --------------------------------------------------------------------------- #
def test_view_progress(app):
    app.view_progress()


def test_reset_confirmed(app, monkeypatch):
    app.progress.total_score = 99
    _script(monkeypatch, confirm=[True])
    app.reset_progress_interactive()
    assert app.progress.total_score == 0


def test_reset_cancelled(app, monkeypatch):
    app.progress.total_score = 99
    _script(monkeypatch, confirm=[False])
    app.reset_progress_interactive()
    assert app.progress.total_score == 99


# --------------------------------------------------------------------------- #
# AI tutor flows
# --------------------------------------------------------------------------- #
def test_ai_tutor_menu_unavailable(app):
    app.tutor = FakeTutor(available=False)
    app.ai_tutor_menu()  # setup-help branch


def test_ai_tutor_menu_chat(app, monkeypatch):
    app.tutor = FakeTutor(available=True)
    _script(monkeypatch, ask=["what is a list", "q"])
    app.ai_tutor_menu()


def test_offer_lesson_tutor_all_actions(app, monkeypatch):
    app.tutor = FakeTutor(available=True)
    lesson = _synthetic_lesson()
    _script(
        monkeypatch,
        confirm=[True, True, True, True, True],  # keep offering until "Done"
        menu=[1, 2, 3, 4, 5],                     # explain, example, deeper, ask, done
        ask=["my question"],
    )
    app._offer_lesson_tutor(lesson)


def test_offer_lesson_tutor_skipped_when_unavailable(app):
    app.tutor = FakeTutor(available=False)
    app._offer_lesson_tutor(_synthetic_lesson())  # returns immediately


def test_tutor_run_error(app):
    def boom():
        raise AITutorError("rate limited")

    app._tutor_run(boom)  # error branch


def test_tutor_run_empty(app):
    app._tutor_run(lambda: "")  # warn branch


# --------------------------------------------------------------------------- #
# Walkthrough offers
# --------------------------------------------------------------------------- #
def test_offer_walkthroughs_single(app, monkeypatch):
    ex = CodeExample(title="e", code="x=1", line_notes={1: "a"})
    _script(monkeypatch, confirm=[True, False])  # walk once, then decline
    app._offer_walkthroughs([ex])


def test_offer_walkthroughs_multiple_pick_and_cancel(app, monkeypatch):
    examples = [CodeExample(title="e1", code="a=1"), CodeExample(title="e2", code="b=2")]
    # First round: confirm yes -> menu pick 1 -> walkthrough. Second round: yes -> cancel (3).
    _script(monkeypatch, confirm=[True, True], menu=[1, 3])
    app._offer_walkthroughs(examples)


def test_offer_walkthroughs_none(app):
    app._offer_walkthroughs([])  # empty -> returns


# --------------------------------------------------------------------------- #
# Remaining branches
# --------------------------------------------------------------------------- #
def test_dashboard_shows_flame_on_streak(app):
    app.progress.streak_count = 5  # flame branch
    app.show_dashboard()


def test_quiz_from_lesson_back(app, monkeypatch):
    quizzable = [l for l in app.lessons if l.quiz_questions]
    _script(monkeypatch, menu=[1, len(quizzable) + 1])  # enter, then Back
    app.quiz_menu()


def test_practice_drills_not_completed(app, monkeypatch):
    monkeypatch.setattr(exercises, "run_exercise", lambda *a, **k: False)
    _script(monkeypatch, menu=[1])
    app.practice_drills()
    assert not app.progress.completed_exercises


def test_practice_drills_shows_completed_marker(app, monkeypatch):
    drills = [l for l in app.lessons if l.has_exercise]
    app.progress.completed_exercises.append(drills[0].mini_exercise.id)
    _script(monkeypatch, menu=[len(drills) + 1])  # Back, just to render the list
    app.practice_drills()


def test_ai_tutor_menu_no_context_lesson(app, monkeypatch):
    app.progress.completed_lessons = [l.id for l in app.lessons]  # no "next" -> ctx None
    app.tutor = FakeTutor(available=True)
    _script(monkeypatch, ask=["q"])
    app.ai_tutor_menu()


def test_run_project_already_complete(app, monkeypatch):
    project = app.projects[0]
    app.progress.completed_projects.append(project.id)
    # decline starter walkthrough, decline reveal, then "mark complete" -> already done
    _script(monkeypatch, confirm=[False, False, True])
    app.run_project(project)


def test_record_lesson_completion_announces_next(app):
    # The first curriculum lesson links to a real next lesson -> "Recommended next".
    app._record_lesson_completion(app.lessons[0], None, False)
    assert app.progress.is_lesson_complete(app.lessons[0].id)


def test_practice_drills_none_available(app):
    app.lessons = []  # no drills -> warn + return
    app.practice_drills()


def test_run_lesson_minimal_content(app):
    # A bare lesson exercises the FALSE side of every "if lesson.X:" guard
    # (no key_terms / examples / mistakes / prompts / quiz / exercise).
    lesson = Lesson(id="bare", title="Bare", level=Level.BEGINNER,
                    estimated_minutes=1, explanation="just text")
    app.run_lesson(lesson)
    assert app.progress.is_lesson_complete("bare")


def test_run_project_minimal_and_declined(app, monkeypatch):
    project = Project(id="bare", title="Bare", difficulty="easy", concepts=[],
                      requirements=["r"], build_guide=["s"])  # no starter/milestones/stretch/solution
    _script(monkeypatch, confirm=[False])  # "Mark complete?" -> No
    app.run_project(project)
    assert not app.progress.is_project_complete("bare")


def test_offer_lesson_tutor_empty_question(app, monkeypatch):
    app.tutor = FakeTutor(available=True)
    # offer? yes -> menu 4 (ask) -> empty question (skipped) -> offer? no -> exit
    _script(monkeypatch, confirm=[True, False], menu=[4], ask=[""])
    app._offer_lesson_tutor(_synthetic_lesson())
