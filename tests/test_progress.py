"""Tests for progress loading/saving, mutations, streaks, and analytics."""

from __future__ import annotations

from datetime import date

import pytest

from python_mastery_cli import progress as prog
from python_mastery_cli.models import Lesson, Level
from python_mastery_cli.progress import (
    Progress,
    completion_percentage,
    load_progress,
    mark_exercise_complete,
    mark_lesson_complete,
    mark_project_complete,
    mark_quiz_complete,
    recommend_next_lesson,
    reset_progress,
    save_progress,
)


@pytest.fixture
def tmp_progress_path(tmp_path):
    return tmp_path / "progress.json"


def _lesson(lesson_id: str, nxt: str | None = None) -> Lesson:
    return Lesson(
        id=lesson_id,
        title=f"Lesson {lesson_id}",
        level=Level.BEGINNER,
        estimated_minutes=5,
        explanation="x",
        next_lesson_id=nxt,
    )


# --------------------------------------------------------------------------- #
# Load / save round-trip
# --------------------------------------------------------------------------- #
def test_save_then_load_round_trips(tmp_progress_path):
    p = Progress(completed_lessons=["b01", "b02"], total_score=20, streak_count=3)
    returned = save_progress(p, tmp_progress_path)
    assert returned == tmp_progress_path
    assert tmp_progress_path.exists()

    loaded = load_progress(tmp_progress_path)
    assert loaded.completed_lessons == ["b01", "b02"]
    assert loaded.total_score == 20
    assert loaded.streak_count == 3


def test_load_missing_file_returns_fresh_progress(tmp_path):
    missing = tmp_path / "does_not_exist.json"
    loaded = load_progress(missing)
    # Falls back to the shipped template (all-empty) — never crashes.
    assert loaded.completed_lessons == []
    assert loaded.total_score == 0


def test_load_corrupt_file_does_not_crash(tmp_progress_path):
    tmp_progress_path.write_text("{ this is not valid json ", encoding="utf-8")
    loaded = load_progress(tmp_progress_path)
    assert isinstance(loaded, Progress)


def test_from_dict_ignores_unknown_keys_and_dedupes():
    p = Progress.from_dict(
        {
            "completed_lessons": ["b01", "b01", "b02"],
            "unknown_field": "ignored",
            "total_score": 5,
        }
    )
    assert p.completed_lessons == ["b01", "b02"]
    assert p.total_score == 5


# --------------------------------------------------------------------------- #
# Mutations
# --------------------------------------------------------------------------- #
def test_mark_lesson_complete_is_idempotent_and_scores():
    p = Progress()
    mark_lesson_complete(p, "b01", points=10)
    mark_lesson_complete(p, "b01", points=10)  # repeat must not double-count
    assert p.completed_lessons == ["b01"]
    assert p.total_score == 10


def test_mark_quiz_adds_score_each_time_but_records_once():
    p = Progress()
    mark_quiz_complete(p, "b01::quiz", score=15)
    mark_quiz_complete(p, "b01::quiz", score=5)
    assert p.completed_quizzes == ["b01::quiz"]
    # Quiz scores accumulate (you can earn more on a retake).
    assert p.total_score == 20


def test_mark_exercise_and_project_award_points():
    p = Progress()
    mark_exercise_complete(p, "b01-ex", points=15)
    mark_project_complete(p, "p01", points=50)
    assert p.completed_exercises == ["b01-ex"]
    assert p.completed_projects == ["p01"]
    assert p.total_score == 65


def test_reset_progress_writes_fresh_profile(tmp_progress_path):
    p = Progress(completed_lessons=["b01"], total_score=99)
    save_progress(p, tmp_progress_path)
    fresh = reset_progress(tmp_progress_path)
    assert fresh.completed_lessons == []
    assert fresh.total_score == 0
    reloaded = load_progress(tmp_progress_path)
    assert reloaded.total_score == 0


# --------------------------------------------------------------------------- #
# Streak logic (inject `today` for determinism)
# --------------------------------------------------------------------------- #
def test_streak_starts_at_one_on_first_activity():
    p = Progress()
    prog._touch_streak(p, today=date(2026, 6, 22))
    assert p.streak_count == 1
    assert p.last_active_date == "2026-06-22"


def test_streak_does_not_double_count_same_day():
    p = Progress()
    prog._touch_streak(p, today=date(2026, 6, 22))
    prog._touch_streak(p, today=date(2026, 6, 22))
    assert p.streak_count == 1


def test_streak_increments_on_consecutive_day():
    p = Progress(streak_count=4, last_active_date="2026-06-21")
    prog._touch_streak(p, today=date(2026, 6, 22))
    assert p.streak_count == 5


def test_streak_resets_after_gap():
    p = Progress(streak_count=9, last_active_date="2026-06-18")
    prog._touch_streak(p, today=date(2026, 6, 22))
    assert p.streak_count == 1


# --------------------------------------------------------------------------- #
# Analytics
# --------------------------------------------------------------------------- #
def test_completion_percentage():
    p = Progress(completed_lessons=["b01", "b02", "b03"])
    assert completion_percentage(p, 10) == 30.0
    assert completion_percentage(p, 0) == 0.0  # guards divide-by-zero


def test_completion_percentage_caps_at_100():
    p = Progress(completed_lessons=["b01", "b02"])
    assert completion_percentage(p, 1) == 100.0


def test_recommend_next_lesson_returns_first_incomplete():
    lessons = [_lesson("b01", "b02"), _lesson("b02", "b03"), _lesson("b03")]
    p = Progress(completed_lessons=["b01"])
    nxt = recommend_next_lesson(p, lessons)
    assert nxt is not None and nxt.id == "b02"


def test_recommend_next_lesson_returns_none_when_done():
    lessons = [_lesson("b01"), _lesson("b02")]
    p = Progress(completed_lessons=["b01", "b02"])
    assert recommend_next_lesson(p, lessons) is None


def test_load_progress_all_sources_missing(tmp_path, monkeypatch):
    # Neither the user file nor the shipped template is readable -> fresh profile.
    monkeypatch.setattr(prog, "TEMPLATE_PATH", tmp_path / "no_template.json")
    loaded = load_progress(tmp_path / "absent.json")
    assert isinstance(loaded, Progress)
    assert loaded.total_score == 0


def test_mark_exercise_complete_is_idempotent():
    p = Progress()
    mark_exercise_complete(p, "e1")
    mark_exercise_complete(p, "e1")  # already present -> skip-append branch
    assert p.completed_exercises == ["e1"]
    assert p.total_score == 15
