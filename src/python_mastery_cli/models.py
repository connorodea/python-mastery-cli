"""Core data models for python-mastery-cli.

Everything the course displays — lessons, examples, quiz questions, coding
exercises, and projects — is represented by the dataclasses defined here. Keeping
the schema in one place means the curriculum modules, the quiz engine, the
exercise runner, and the tests all agree on the same shape of data.

Design notes
------------
* Plain ``dataclasses`` are used instead of Pydantic to keep the dependency
  surface small (only ``rich`` and ``typer`` are required to run the app).
* ``__post_init__`` validation keeps obviously-broken curriculum content from
  silently shipping; the ``test_curriculum`` suite leans on these invariants.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class Level(str, Enum):
    """The four tracks a lesson or project can belong to."""

    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    PROJECT = "project"

    def __str__(self) -> str:  # nicer display in f-strings / Rich
        return self.value


class QuestionType(str, Enum):
    """Supported quiz question formats."""

    MULTIPLE_CHOICE = "multiple_choice"
    TRUE_FALSE = "true_false"
    FILL_BLANK = "fill_blank"
    SHORT_ANSWER = "short_answer"

    def __str__(self) -> str:
        return self.value


# Difficulty labels reused across quizzes, exercises, and projects.
DIFFICULTIES = ("easy", "medium", "hard")


@dataclass
class CodeExample:
    """A runnable, syntax-highlighted snippet that demonstrates a concept.

    ``line_notes`` powers the interactive line-by-line walkthrough: it maps a
    1-indexed line number (counting lines of ``code`` after normalisation) to a
    plain-language explanation of what that line does. Not every line needs a
    note — the walkthrough simply shows the bare line when no note exists.
    """

    title: str
    code: str
    explanation: str = ""
    output: str = ""
    line_notes: dict[int, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.title.strip():
            raise ValueError("CodeExample.title must not be empty")
        if not self.code.strip():
            raise ValueError(f"CodeExample {self.title!r} has empty code")
        # Normalise leading/trailing blank lines so Rich renders snippets tightly.
        self.code = self.code.strip("\n")
        # Validate line_notes point at real lines (helps catch off-by-one authoring bugs).
        line_count = len(self.code.splitlines())
        for line_no in self.line_notes:
            if not (1 <= line_no <= line_count):
                raise ValueError(
                    f"CodeExample {self.title!r}: line_note references line "
                    f"{line_no}, but the snippet only has {line_count} lines"
                )

    @property
    def has_walkthrough(self) -> bool:
        return bool(self.line_notes)


@dataclass
class QuizQuestion:
    """A single quiz question.

    The ``correct_answer`` field is interpreted according to ``qtype``:

    * ``MULTIPLE_CHOICE`` — the exact text of the correct option (must appear in
      ``options``).
    * ``TRUE_FALSE`` — the string ``"true"`` or ``"false"``.
    * ``FILL_BLANK`` — the expected token; matched case-insensitively after
      trimming surrounding whitespace/quotes.
    * ``SHORT_ANSWER`` — a representative correct answer; grading additionally
      accepts any response that contains every keyword in ``keywords``.
    """

    question: str
    qtype: QuestionType
    correct_answer: str
    options: list[str] = field(default_factory=list)
    explanation: str = ""
    difficulty: str = "easy"
    keywords: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        # Allow callers to pass plain strings for ergonomics in curriculum files.
        # (QuestionType subclasses str, so this guard is always true in practice;
        # it stays as a safety net for any non-enum input.)
        if isinstance(self.qtype, str):  # pragma: no branch
            self.qtype = QuestionType(self.qtype)
        if self.difficulty not in DIFFICULTIES:
            raise ValueError(
                f"Question {self.question!r} has invalid difficulty "
                f"{self.difficulty!r}; expected one of {DIFFICULTIES}"
            )
        if self.qtype is QuestionType.MULTIPLE_CHOICE:
            if len(self.options) < 2:
                raise ValueError(
                    f"Multiple-choice question {self.question!r} needs >= 2 options"
                )
            if self.correct_answer not in self.options:
                raise ValueError(
                    f"Multiple-choice question {self.question!r}: correct_answer "
                    f"{self.correct_answer!r} is not one of the options"
                )
        if self.qtype is QuestionType.TRUE_FALSE:
            self.correct_answer = self.correct_answer.strip().lower()
            if self.correct_answer not in ("true", "false"):
                raise ValueError(
                    f"True/False question {self.question!r} needs a "
                    "correct_answer of 'true' or 'false'"
                )
            self.options = ["True", "False"]


@dataclass
class Exercise:
    """A hands-on coding drill.

    User code is never executed (see README — "Why exercises are not auto-run").
    Instead we present instructions, starter code, the expected output, optional
    progressive hints, and a revealable solution. Completion is self-reported.
    """

    id: str
    title: str
    instructions: str
    starter_code: str = ""
    expected_output: str = ""
    hints: list[str] = field(default_factory=list)
    solution: str = ""
    difficulty: str = "easy"

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ValueError("Exercise.id must not be empty")
        if not self.instructions.strip():
            raise ValueError(f"Exercise {self.id!r} has empty instructions")
        if self.difficulty not in DIFFICULTIES:
            raise ValueError(
                f"Exercise {self.id!r} has invalid difficulty {self.difficulty!r}"
            )


@dataclass
class Lesson:
    """A single teaching unit.

    A lesson bundles everything needed to learn one concept end-to-end: an
    explanation, a glossary of key terms, worked examples, common mistakes to
    avoid, practice prompts, a short quiz, and a mini coding exercise.
    """

    id: str
    title: str
    level: Level
    estimated_minutes: int
    explanation: str
    key_terms: dict[str, str] = field(default_factory=dict)
    code_examples: list[CodeExample] = field(default_factory=list)
    common_mistakes: list[str] = field(default_factory=list)
    practice_prompts: list[str] = field(default_factory=list)
    quiz_questions: list[QuizQuestion] = field(default_factory=list)
    mini_exercise: Optional[Exercise] = None
    next_lesson_id: Optional[str] = None

    def __post_init__(self) -> None:
        # Level subclasses str, so this is always true in practice (safety net).
        if isinstance(self.level, str):  # pragma: no branch
            self.level = Level(self.level)
        if not self.id.strip():
            raise ValueError("Lesson.id must not be empty")
        if not self.title.strip():
            raise ValueError(f"Lesson {self.id!r} has an empty title")
        if self.estimated_minutes <= 0:
            raise ValueError(f"Lesson {self.id!r} needs a positive estimated_minutes")
        if not self.explanation.strip():
            raise ValueError(f"Lesson {self.id!r} has an empty explanation")

    @property
    def quiz_count(self) -> int:
        return len(self.quiz_questions)

    @property
    def has_exercise(self) -> bool:
        return self.mini_exercise is not None


@dataclass
class Project:
    """A guided, build-it-yourself mini-project."""

    id: str
    title: str
    difficulty: str
    concepts: list[str]
    requirements: list[str]
    build_guide: list[str]
    starter_code: str = ""
    milestones: list[str] = field(default_factory=list)
    stretch_goals: list[str] = field(default_factory=list)
    solution: str = ""
    estimated_minutes: int = 60

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ValueError("Project.id must not be empty")
        if not self.title.strip():
            raise ValueError(f"Project {self.id!r} has an empty title")
        if self.difficulty not in DIFFICULTIES:
            raise ValueError(
                f"Project {self.id!r} has invalid difficulty {self.difficulty!r}"
            )
        if not self.build_guide:
            raise ValueError(f"Project {self.id!r} needs at least one build step")
