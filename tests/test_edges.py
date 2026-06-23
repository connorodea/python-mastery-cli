"""Edge-case coverage: model validation, config, progress analytics, ai_tutor
internals, curriculum validation branches, theme, and remaining utils paths."""

from __future__ import annotations

from datetime import date

import pytest

from python_mastery_cli import ai_tutor, config, curriculum, progress as prog, theme as th, utils
from python_mastery_cli.models import (
    CodeExample,
    Exercise,
    Lesson,
    Level,
    Project,
    QuestionType,
    QuizQuestion,
)


# --------------------------------------------------------------------------- #
# models — validation raises + properties + __str__
# --------------------------------------------------------------------------- #
def test_enum_str():
    assert str(Level.BEGINNER) == "beginner"
    assert str(QuestionType.FILL_BLANK) == "fill_blank"


def test_code_example_validation():
    with pytest.raises(ValueError):
        CodeExample(title=" ", code="x")
    with pytest.raises(ValueError):
        CodeExample(title="t", code="   ")
    ex = CodeExample(title="t", code="x=1", line_notes={1: "n"})
    assert ex.has_walkthrough is True
    assert CodeExample(title="t", code="x=1").has_walkthrough is False


def test_quiz_question_validation():
    with pytest.raises(ValueError):
        QuizQuestion(question="q", qtype="multiple_choice", options=["a"], correct_answer="a")
    with pytest.raises(ValueError):
        QuizQuestion(question="q", qtype="fill_blank", correct_answer="a", difficulty="nope")


def test_exercise_validation():
    with pytest.raises(ValueError):
        Exercise(id=" ", title="t", instructions="i")
    with pytest.raises(ValueError):
        Exercise(id="e", title="t", instructions="  ")


def test_lesson_validation_and_properties():
    with pytest.raises(ValueError):
        Lesson(id=" ", title="t", level=Level.BEGINNER, estimated_minutes=1, explanation="x")
    with pytest.raises(ValueError):
        Lesson(id="x", title=" ", level=Level.BEGINNER, estimated_minutes=1, explanation="x")
    with pytest.raises(ValueError):
        Lesson(id="x", title="t", level=Level.BEGINNER, estimated_minutes=0, explanation="x")
    lesson = Lesson(
        id="x", title="t", level="beginner", estimated_minutes=1, explanation="x",
        quiz_questions=[QuizQuestion(question="q", qtype="true_false", correct_answer="true")],
        mini_exercise=Exercise(id="x-ex", title="d", instructions="i"),
    )
    assert lesson.level is Level.BEGINNER
    assert lesson.quiz_count == 1
    assert lesson.has_exercise is True


def test_project_validation():
    with pytest.raises(ValueError):
        Project(id=" ", title="t", difficulty="easy", concepts=[], requirements=[], build_guide=["s"])
    with pytest.raises(ValueError):
        Project(id="p", title=" ", difficulty="easy", concepts=[], requirements=[], build_guide=["s"])
    with pytest.raises(ValueError):
        Project(id="p", title="t", difficulty="x", concepts=[], requirements=[], build_guide=["s"])
    with pytest.raises(ValueError):
        Project(id="p", title="t", difficulty="easy", concepts=[], requirements=[], build_guide=[])


# --------------------------------------------------------------------------- #
# config
# --------------------------------------------------------------------------- #
@pytest.fixture
def home(tmp_path, monkeypatch):
    monkeypatch.setenv("PYTHON_MASTERY_HOME", str(tmp_path))
    for var in ("OPENAI_API_KEY", "OPENAI_MODEL", "OPENAI_BASE_URL"):
        monkeypatch.delenv(var, raising=False)
    return tmp_path


def test_config_corrupt_file_returns_empty(home):
    config.config_path().write_text("{bad json", encoding="utf-8")
    assert config.load_config() == {}


def test_config_base_url_and_stored_key(home):
    assert config.has_stored_key() is False
    config.set_api_key("sk-1")
    assert config.has_stored_key() is True
    config.set_base_url("https://example.com")
    assert config.get_base_url() == "https://example.com"
    config.set_base_url(None)  # removal branch
    assert config.get_base_url() is None


def test_config_chmod_failure_is_non_fatal(home, monkeypatch):
    import pathlib

    def boom(self, *a, **k):
        raise OSError("no chmod here")

    monkeypatch.setattr(pathlib.Path, "chmod", boom)
    # Should still write the file without raising.
    config.set_model("gpt-x")
    assert config.get_model() == "gpt-x"


# --------------------------------------------------------------------------- #
# progress analytics
# --------------------------------------------------------------------------- #
def test_default_progress_path_without_env(monkeypatch):
    monkeypatch.delenv("PYTHON_MASTERY_HOME", raising=False)
    path = prog.default_progress_path()
    assert path.name == "progress.json"
    assert ".python_mastery_cli" in str(path)


def test_touch_streak_future_date_does_not_crash():
    p = prog.Progress(streak_count=5, last_active_date="2030-01-01")
    prog._touch_streak(p, today=date(2026, 6, 22))
    assert p.streak_count >= 1


def test_touch_streak_handles_bad_stored_date():
    p = prog.Progress(last_active_date="not-a-date")
    prog._touch_streak(p, today=date(2026, 6, 22))
    assert p.last_active_date == "2026-06-22"


def test_infer_current_level_all_complete():
    lessons = curriculum.get_all_lessons()
    p = prog.Progress(completed_lessons=[lesson.id for lesson in lessons])
    assert prog.infer_current_level(p, lessons) == "advanced"


def test_level_breakdown():
    lessons = curriculum.get_all_lessons()
    p = prog.Progress(completed_lessons=[lessons[0].id])
    bd = prog.level_breakdown(p, lessons)
    assert bd["beginner"][0] == 1
    assert all(done <= total for done, total in bd.values())


def test_parse_iso_date():
    assert prog.parse_iso_date(None) is None
    assert prog.parse_iso_date("bad") is None
    assert prog.parse_iso_date("2026-06-22") is not None


# --------------------------------------------------------------------------- #
# ai_tutor internals
# --------------------------------------------------------------------------- #
def test_ai_tutor_builds_real_client(monkeypatch):
    captured = {}

    class FakeOpenAI:
        def __init__(self, **kwargs):
            captured.update(kwargs)

    monkeypatch.setattr(ai_tutor, "OpenAI", FakeOpenAI)
    tutor = ai_tutor.AITutor(api_key="sk-x", base_url="https://h", model="m")
    client = tutor._get_client()
    assert isinstance(client, FakeOpenAI)
    assert captured["api_key"] == "sk-x"
    assert captured["base_url"] == "https://h"


def test_ai_tutor_without_sdk(monkeypatch):
    monkeypatch.setattr(ai_tutor, "OpenAI", None)
    tutor = ai_tutor.AITutor(api_key="sk-x")
    assert tutor.sdk_installed() is False
    assert "openai" in tutor.unavailable_reason().lower()
    with pytest.raises(ai_tutor.AITutorError):
        tutor._get_client()


def test_ai_tutor_available_reason_empty():
    tutor = ai_tutor.AITutor(api_key="sk-x", client=object())
    assert tutor.unavailable_reason() == ""


def test_ai_tutor_explain_code_line():
    class Rec:
        def __init__(self):
            self.calls = []

    import types

    calls = []

    def create(**kwargs):
        calls.append(kwargs)
        return types.SimpleNamespace(
            choices=[types.SimpleNamespace(message=types.SimpleNamespace(content="ok"))]
        )

    client = types.SimpleNamespace(chat=types.SimpleNamespace(completions=types.SimpleNamespace(create=create)))
    tutor = ai_tutor.AITutor(api_key="x", client=client)
    assert tutor.explain_code_line("x = 1", surrounding="x = 1\ny = 2") == "ok"
    assert calls  # the model was called


# --------------------------------------------------------------------------- #
# curriculum helpers + validation problem branches
# --------------------------------------------------------------------------- #
def test_curriculum_counts_and_lookups():
    assert curriculum.lesson_count() == 78
    assert curriculum.project_count() == 12
    assert curriculum.get_lessons_by_level("advanced")
    assert curriculum.get_project(curriculum.get_all_projects()[0].id) is not None


def test_validate_curriculum_reports_problems(monkeypatch):
    dup_lessons = [
        Lesson(id="d", title="A", level=Level.BEGINNER, estimated_minutes=1, explanation="x"),
        Lesson(id="d", title="B", level=Level.BEGINNER, estimated_minutes=1,
               explanation="x", next_lesson_id="missing"),
    ]
    dup_projects = [
        Project(id="p", title="P", difficulty="easy", concepts=[], requirements=[], build_guide=["s"]),
        Project(id="p", title="P2", difficulty="easy", concepts=[], requirements=[], build_guide=["s"]),
    ]
    monkeypatch.setattr(curriculum, "get_all_lessons", lambda: dup_lessons)
    monkeypatch.setattr(curriculum, "get_all_projects", lambda: dup_projects)
    problems = curriculum.validate_curriculum()
    joined = " ".join(problems)
    assert "Duplicate lesson id" in joined
    assert "missing" in joined
    assert "Duplicate project id" in joined


# --------------------------------------------------------------------------- #
# theme + extra utils
# --------------------------------------------------------------------------- #
def test_gradient_stops_single():
    assert th.gradient_stops("#ffffff", "#000000", 1) == ["#ffffff"]
    assert len(th.gradient_stops("#ffffff", "#000000", 5)) == 5


def test_utils_typography_and_widgets(capsys):
    utils.banner(subtitle="custom tagline")
    utils.eyebrow("hello", align="center")
    utils.hairline()
    utils.blank(2)
    utils.stat_strip([("Level", "Beginner"), ("Score", "10 pts")])
    bar = utils.progress_bar(3, 10)
    utils.console.print(bar)
    utils.heading("Title", kicker="Section")
    out = capsys.readouterr().out
    assert "custom tagline" in out
    assert "Title" in out
