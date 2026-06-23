"""Curriculum registry.

Each track module exposes a module-level list of content objects:

* ``beginner.BEGINNER_LESSONS``     -> list[Lesson]
* ``intermediate.INTERMEDIATE_LESSONS`` -> list[Lesson]
* ``advanced.ADVANCED_LESSONS``     -> list[Lesson]
* ``projects.PROJECTS``             -> list[Project]

This package stitches them together into a single ordered course, exposes lookup
helpers, and lazily fills in ``next_lesson_id`` so authors don't have to hand-chain
every lesson (an explicit ``next_lesson_id`` always wins).
"""

from __future__ import annotations

from functools import lru_cache
from typing import Optional

from ..models import Lesson, Project
from .advanced import ADVANCED_LESSONS
from .beginner import BEGINNER_LESSONS
from .intermediate import INTERMEDIATE_LESSONS
from .michigan_basics import MICHIGAN_BASICS_LESSONS
from .projects import PROJECTS


@lru_cache(maxsize=1)
def get_all_lessons() -> list[Lesson]:
    """Return every lesson in recommended learning order (beginner→advanced).

    Also auto-links ``next_lesson_id`` for any lesson that didn't set one, so the
    "Continue learning" flow always knows where to go next.
    """
    lessons: list[Lesson] = [
        *BEGINNER_LESSONS,
        *MICHIGAN_BASICS_LESSONS,
        *INTERMEDIATE_LESSONS,
        *ADVANCED_LESSONS,
    ]
    for current, following in zip(lessons, lessons[1:]):
        if current.next_lesson_id is None:
            current.next_lesson_id = following.id
    if lessons and lessons[-1].next_lesson_id is None:
        lessons[-1].next_lesson_id = None  # last lesson terminates the chain
    return lessons


@lru_cache(maxsize=1)
def _lesson_index() -> dict[str, Lesson]:
    return {lesson.id: lesson for lesson in get_all_lessons()}


def get_lessons_by_level(level: str) -> list[Lesson]:
    """Return lessons belonging to a single level (e.g. ``"beginner"``)."""
    return [lesson for lesson in get_all_lessons() if str(lesson.level) == level]


def get_lesson(lesson_id: str) -> Optional[Lesson]:
    """Look up a lesson by id, or ``None`` if it doesn't exist."""
    return _lesson_index().get(lesson_id)


@lru_cache(maxsize=1)
def get_all_projects() -> list[Project]:
    """Return every guided project."""
    return list(PROJECTS)


@lru_cache(maxsize=1)
def _project_index() -> dict[str, Project]:
    return {project.id: project for project in get_all_projects()}


def get_project(project_id: str) -> Optional[Project]:
    return _project_index().get(project_id)


def lesson_count() -> int:
    return len(get_all_lessons())


def project_count() -> int:
    return len(get_all_projects())


def validate_curriculum() -> list[str]:
    """Return a list of structural problems (empty list == healthy curriculum).

    Used by the test-suite and as a cheap self-check on startup.
    """
    problems: list[str] = []
    lessons = get_all_lessons()
    ids = [lesson.id for lesson in lessons]
    seen: set[str] = set()
    for lesson_id in ids:
        if lesson_id in seen:
            problems.append(f"Duplicate lesson id: {lesson_id}")
        seen.add(lesson_id)

    valid_ids = set(ids)
    for lesson in lessons:
        if lesson.next_lesson_id and lesson.next_lesson_id not in valid_ids:
            problems.append(
                f"Lesson {lesson.id} points to missing next_lesson_id "
                f"{lesson.next_lesson_id!r}"
            )

    project_ids: set[str] = set()
    for project in get_all_projects():
        if project.id in project_ids:
            problems.append(f"Duplicate project id: {project.id}")
        project_ids.add(project.id)
    return problems


__all__ = [
    "get_all_lessons",
    "get_lessons_by_level",
    "get_lesson",
    "get_all_projects",
    "get_project",
    "lesson_count",
    "project_count",
    "validate_curriculum",
]
