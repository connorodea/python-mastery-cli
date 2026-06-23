"""Interactive coding-exercise (drill) runner.

For safety we never execute user-submitted code (see the README). Instead the
runner walks the learner through a deliberate-practice loop:

    instructions → starter code → expected output → (optional) hints →
    (optional) reveal solution → self-reported completion

This keeps the focus on *understanding* the solution rather than on sandboxing
arbitrary input, and it works identically across every platform.
"""

from __future__ import annotations

from . import utils
from .models import Exercise


def show_exercise(exercise: Exercise, *, color: str = "green") -> None:
    """Render the static parts of an exercise (instructions, starter, output)."""
    utils.heading(f"Coding Drill — {exercise.title}", color=color)
    utils.panel(exercise.instructions, title="Your task", color=color)

    if exercise.starter_code:
        utils.render_python(exercise.starter_code, title="Starter code", color=color)
    if exercise.expected_output:
        utils.panel(
            f"[green]{exercise.expected_output}[/green]",
            title="Expected output",
            color="cyan",
        )


def _walk_hints(exercise: Exercise) -> None:
    """Reveal hints one at a time, only as the learner asks for them."""
    if not exercise.hints:
        utils.info("No hints for this drill — give it your best shot!")
        return
    shown = 0
    while shown < len(exercise.hints):
        utils.console.print(f"\n[bold yellow]Hint {shown + 1}:[/bold yellow] {exercise.hints[shown]}")
        shown += 1
        if shown < len(exercise.hints):
            if not utils.confirm("Show another hint?", default=False):
                break
    utils.info(f"({shown}/{len(exercise.hints)} hints shown)")


def run_exercise(exercise: Exercise, *, color: str = "green") -> bool:
    """Run the interactive exercise loop.

    Returns ``True`` if the learner marks the drill complete, ``False`` otherwise.
    Code is written by the learner in their own editor — this is a coaching loop,
    not a code executor.
    """
    show_exercise(exercise, color=color)
    utils.info(
        "Write your solution in your own editor/REPL, then come back. "
        "When your output matches the expected output, mark it complete."
    )

    while True:
        choice = utils.menu(
            "Coding Drill",
            [
                "Show / reveal another hint",
                "Reveal the full solution",
                "Mark this drill complete",
                "Skip for now",
            ],
            color=color,
        )
        if choice == 1:
            _walk_hints(exercise)
        elif choice == 2:
            if exercise.solution:
                utils.render_python(exercise.solution, title="Reference solution", color="yellow")
                utils.info("Compare it with your approach — there's often more than one good answer.")
                if utils.confirm("Walk through the solution line by line?", default=False):
                    utils.walkthrough(
                        exercise.solution,
                        title=f"{exercise.title} — solution, line by line",
                        color="yellow",
                    )
            else:
                utils.warn("No reference solution is provided for this drill.")
        elif choice == 3:
            if utils.confirm("Did you complete the drill yourself?", default=True):
                utils.success("Nice work — drill marked complete!")
                return True
            utils.info("No worries — finish it and come back.")
        else:  # choice == 4 (the menu only yields 1-4)
            utils.info("Skipped. You can return to this drill any time.")
            return False
