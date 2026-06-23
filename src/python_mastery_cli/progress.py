"""Local progress tracking, persisted as JSON.

Progress is stored per-user in ``~/.python_mastery_cli/progress.json`` so that the
app keeps working when installed read-only into ``site-packages``. A pristine
template ships at ``python_mastery_cli/data/progress.json`` and is used to seed a
fresh profile the first time the app runs.

The :class:`Progress` dataclass is intentionally simple (sets of completed ids +
a few scalars) and round-trips losslessly to/from JSON.
"""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass, field
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Optional

# --------------------------------------------------------------------------- #
# Where progress lives
# --------------------------------------------------------------------------- #
TEMPLATE_PATH = Path(__file__).resolve().parent / "data" / "progress.json"


def default_progress_path() -> Path:
    """Resolve the user's progress file path.

    Honours ``PYTHON_MASTERY_HOME`` so tests (and power users) can redirect
    storage without monkeypatching.
    """
    home = os.environ.get("PYTHON_MASTERY_HOME")
    base = Path(home) if home else Path.home() / ".python_mastery_cli"
    return base / "progress.json"


@dataclass
class Progress:
    """A learner's saved state."""

    completed_lessons: list[str] = field(default_factory=list)
    completed_quizzes: list[str] = field(default_factory=list)
    completed_exercises: list[str] = field(default_factory=list)
    completed_projects: list[str] = field(default_factory=list)
    current_level: str = "beginner"
    total_score: int = 0
    streak_count: int = 0
    last_active_date: Optional[str] = None  # ISO date string, e.g. "2026-06-22"

    # ------------------------------------------------------------------ #
    # Serialization
    # ------------------------------------------------------------------ #
    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Progress":
        """Build a Progress from a (possibly partial/legacy) dict."""
        known = {f for f in cls.__dataclass_fields__}  # type: ignore[attr-defined]
        filtered = {k: v for k, v in data.items() if k in known}
        progress = cls(**filtered)
        # De-duplicate while preserving order in case a file was hand-edited.
        progress.completed_lessons = _dedupe(progress.completed_lessons)
        progress.completed_quizzes = _dedupe(progress.completed_quizzes)
        progress.completed_exercises = _dedupe(progress.completed_exercises)
        progress.completed_projects = _dedupe(progress.completed_projects)
        return progress

    # ------------------------------------------------------------------ #
    # Convenience views
    # ------------------------------------------------------------------ #
    def is_lesson_complete(self, lesson_id: str) -> bool:
        return lesson_id in self.completed_lessons

    def is_exercise_complete(self, exercise_id: str) -> bool:
        return exercise_id in self.completed_exercises

    def is_project_complete(self, project_id: str) -> bool:
        return project_id in self.completed_projects


def _dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


# --------------------------------------------------------------------------- #
# Load / save
# --------------------------------------------------------------------------- #
def load_progress(path: Optional[Path] = None) -> Progress:
    """Load progress from ``path`` (default: user file).

    Falls back to the shipped template and finally to a fresh profile. Corrupt
    JSON is handled gracefully rather than crashing the app.
    """
    path = path or default_progress_path()
    for candidate in (path, TEMPLATE_PATH):
        if candidate.exists():
            try:
                data = json.loads(candidate.read_text(encoding="utf-8"))
                return Progress.from_dict(data)
            except (json.JSONDecodeError, TypeError, ValueError):
                # Corrupt file: ignore and try the next candidate.
                continue
    return Progress()


def save_progress(progress: Progress, path: Optional[Path] = None) -> Path:
    """Persist progress to ``path`` (default: user file). Returns the path used."""
    path = path or default_progress_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(progress.to_dict(), indent=2) + "\n", encoding="utf-8")
    return path


# --------------------------------------------------------------------------- #
# Mutations (each returns the progress for fluent use)
# --------------------------------------------------------------------------- #
def _touch_streak(progress: Progress, today: Optional[date] = None) -> None:
    """Update the daily streak based on the gap since the last active day."""
    today = today or date.today()
    today_iso = today.isoformat()
    if progress.last_active_date == today_iso:
        return  # already counted today
    if progress.last_active_date:
        try:
            last = date.fromisoformat(progress.last_active_date)
        except ValueError:
            last = None
        if last is not None and today - last == timedelta(days=1):
            progress.streak_count += 1
        elif last is not None and today - last > timedelta(days=1):
            progress.streak_count = 1
        else:
            # Same day handled above; future/!=1-day-ago resets to a fresh day.
            progress.streak_count = max(progress.streak_count, 1)
    else:
        progress.streak_count = 1
    progress.last_active_date = today_iso


def mark_lesson_complete(progress: Progress, lesson_id: str, *, points: int = 10) -> Progress:
    """Mark a lesson complete, award points, and bump the streak (idempotent)."""
    _touch_streak(progress)
    if lesson_id not in progress.completed_lessons:
        progress.completed_lessons.append(lesson_id)
        progress.total_score += points
    return progress


def mark_quiz_complete(progress: Progress, quiz_id: str, *, score: int = 0) -> Progress:
    """Record a completed quiz and add its score (idempotent on the id)."""
    _touch_streak(progress)
    if quiz_id not in progress.completed_quizzes:
        progress.completed_quizzes.append(quiz_id)
    progress.total_score += max(score, 0)
    return progress


def mark_exercise_complete(progress: Progress, exercise_id: str, *, points: int = 15) -> Progress:
    """Mark a coding exercise complete and award points (idempotent)."""
    _touch_streak(progress)
    if exercise_id not in progress.completed_exercises:
        progress.completed_exercises.append(exercise_id)
        progress.total_score += points
    return progress


def mark_project_complete(progress: Progress, project_id: str, *, points: int = 50) -> Progress:
    """Mark a project complete and award points (idempotent)."""
    _touch_streak(progress)
    if project_id not in progress.completed_projects:
        progress.completed_projects.append(project_id)
        progress.total_score += points
    return progress


def reset_progress(path: Optional[Path] = None) -> Progress:
    """Reset to a fresh profile and persist it. Returns the new Progress."""
    fresh = Progress()
    save_progress(fresh, path)
    return fresh


# --------------------------------------------------------------------------- #
# Analytics
# --------------------------------------------------------------------------- #
def completion_percentage(progress: Progress, total_lessons: int) -> float:
    """Percentage of lessons completed (0.0–100.0)."""
    if total_lessons <= 0:
        return 0.0
    pct = len(progress.completed_lessons) / total_lessons * 100.0
    return round(min(pct, 100.0), 1)


def recommend_next_lesson(progress: Progress, lessons: list) -> Optional[object]:
    """Return the first lesson (in curriculum order) the learner hasn't finished.

    ``lessons`` is a list of :class:`~python_mastery_cli.models.Lesson`. Returns
    ``None`` once every lesson is complete.
    """
    completed = set(progress.completed_lessons)
    for lesson in lessons:
        if lesson.id not in completed:
            return lesson
    return None


def level_breakdown(progress: Progress, lessons: list) -> dict[str, tuple[int, int]]:
    """Map each level -> (completed_count, total_count) for the dashboard."""
    completed = set(progress.completed_lessons)
    breakdown: dict[str, list[int]] = {}
    for lesson in lessons:
        key = str(lesson.level)
        bucket = breakdown.setdefault(key, [0, 0])
        bucket[1] += 1
        if lesson.id in completed:
            bucket[0] += 1
    return {k: (v[0], v[1]) for k, v in breakdown.items()}


def infer_current_level(progress: Progress, lessons: list) -> str:
    """Infer the learner's current level from the next recommended lesson."""
    nxt = recommend_next_lesson(progress, lessons)
    if nxt is None:
        return "advanced"
    return str(nxt.level)


def parse_iso_date(value: Optional[str]) -> Optional[datetime]:
    """Best-effort parse of the stored ISO date (used only for display)."""
    if not value:
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None
