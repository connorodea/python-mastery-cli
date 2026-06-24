"""Reusable quiz logic: grading, scoring, and an interactive runner.

Grading is deliberately separated from presentation so it can be unit-tested
without a terminal (`grade_answer` is pure). The interactive `run_quiz` function
wires grading up to Rich prompts and returns a :class:`QuizResult`.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from . import utils
from .models import QuestionType, QuizQuestion

# Points awarded per correct answer, scaled by difficulty.
POINTS_BY_DIFFICULTY = {"easy": 5, "medium": 8, "hard": 12}


def _normalize(text: str) -> str:
    """Lowercase, strip whitespace and surrounding quotes for fuzzy matching."""
    return text.strip().strip("'\"`").lower()


def grade_answer(question: QuizQuestion, user_answer: str) -> bool:
    """Return True if ``user_answer`` is correct for ``question``.

    This is a pure function — no I/O — so it is easy to test exhaustively.

    * Multiple choice accepts either the option's number (1-indexed) or its text.
    * True/False accepts t/f/true/false/yes/no.
    * Fill-in-the-blank matches the normalized token.
    * Short answer is correct if it equals the model answer OR contains every
      configured keyword.
    """
    answer = _normalize(user_answer)
    if not answer:
        return False

    if question.qtype is QuestionType.MULTIPLE_CHOICE:
        # Accept a 1-indexed selection number... str.isdigit() alone is unsafe:
        # it accepts non-ASCII "digits" (e.g. "²", "③") that int() can't parse,
        # so require ASCII digits. Anything else falls through to a text match.
        if answer.isascii() and answer.isdigit():
            idx = int(answer) - 1
            if 0 <= idx < len(question.options):
                return _normalize(question.options[idx]) == _normalize(question.correct_answer)
            return False
        # ...or the literal option text.
        return answer == _normalize(question.correct_answer)

    if question.qtype is QuestionType.TRUE_FALSE:
        truthy = {"t", "true", "yes", "y", "1"}
        falsy = {"f", "false", "no", "n", "0"}
        if answer in truthy:
            user_bool = "true"
        elif answer in falsy:
            user_bool = "false"
        else:
            return False
        return user_bool == _normalize(question.correct_answer)

    if question.qtype is QuestionType.FILL_BLANK:
        return answer == _normalize(question.correct_answer)

    # SHORT_ANSWER
    if answer == _normalize(question.correct_answer):
        return True
    if question.keywords:
        return all(_normalize(kw) in answer for kw in question.keywords)
    return False


def points_for(question: QuizQuestion) -> int:
    return POINTS_BY_DIFFICULTY.get(question.difficulty, 5)


@dataclass
class QuizResult:
    """Summary of a completed quiz run."""

    total: int = 0
    correct: int = 0
    score: int = 0
    answered: int = 0
    details: list[tuple[str, bool]] = field(default_factory=list)  # (question, correct?)

    @property
    def percentage(self) -> float:
        if self.total == 0:
            return 0.0
        return round(self.correct / self.total * 100.0, 1)

    @property
    def passed(self) -> bool:
        # A 70% bar is a friendly "you've got the idea" threshold.
        return self.percentage >= 70.0


def _prompt_for(question: QuizQuestion) -> str:
    """Render a single question and collect the user's raw answer."""
    color = {"easy": "green", "medium": "yellow", "hard": "red"}.get(question.difficulty, "blue")
    utils.console.print(f"\n[bold]{question.question}[/bold]  [dim]({question.difficulty})[/dim]")

    if question.qtype is QuestionType.MULTIPLE_CHOICE:
        for i, option in enumerate(question.options, start=1):
            utils.console.print(f"   [bold {color}]{i}.[/bold {color}] {option}")
        choices = [str(i) for i in range(1, len(question.options) + 1)]
        return utils.ask("Your answer (number)", choices=choices)

    if question.qtype is QuestionType.TRUE_FALSE:
        return utils.ask("True or False", choices=["True", "False"])

    if question.qtype is QuestionType.FILL_BLANK:
        return utils.ask("Fill in the blank")

    return utils.ask("Your answer")


def run_quiz(
    questions: list[QuizQuestion],
    *,
    title: str = "Quiz",
    color: str = "blue",
) -> QuizResult:
    """Interactively run a quiz and return the :class:`QuizResult`.

    Shows correctness + explanation + a running score after each question.
    """
    result = QuizResult(total=len(questions))
    if not questions:
        utils.warn("This lesson has no quiz questions yet.")
        return result

    utils.heading(title, color=color)
    for number, question in enumerate(questions, start=1):
        utils.console.print(f"[dim]Question {number} of {len(questions)}[/dim]")
        raw = _prompt_for(question)
        correct = grade_answer(question, raw)
        result.answered += 1
        result.details.append((question.question, correct))

        if correct:
            gained = points_for(question)
            result.correct += 1
            result.score += gained
            utils.success(f"Correct!  (+{gained} pts)")
        else:
            utils.error(f"Not quite. Correct answer: [bold]{question.correct_answer}[/bold]")

        if question.explanation:
            utils.console.print(f"[dim]→ {question.explanation}[/dim]")
        utils.console.print(
            f"[dim]Running score: {result.correct}/{number} correct "
            f"({result.score} pts)[/dim]"
        )

    _summarize(result, color=color)
    return result


def _summarize(result: QuizResult, *, color: str = "blue") -> None:
    verdict = "Great work!" if result.passed else "Keep practicing — review and retry."
    style = "bold green" if result.passed else "bold yellow"
    body = (
        f"[bold]Score:[/bold] {result.correct}/{result.total} "
        f"({result.percentage:.0f}%)\n"
        f"[bold]Points earned:[/bold] {result.score}\n\n"
        f"[{style}]{verdict}[/{style}]"
    )
    utils.panel(body, title="Quiz Complete", color=color)
