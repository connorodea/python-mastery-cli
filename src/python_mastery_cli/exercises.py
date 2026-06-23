"""Interactive coding-exercise (drill) runner.

The learner can either self-report completion or — the real feedback loop — paste
their solution and have it **run and checked against the expected output**. Code
runs in a separate subprocess with a timeout (see ``runner.py``); it is always
opt-in (the learner chooses "Run & check my solution").

    instructions → starter code → expected output → run & check / hints /
    reveal solution → mark complete
"""

from __future__ import annotations

from . import runner, utils
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


def _run_and_check(exercise: Exercise, *, color: str = "green") -> bool:
    """Let the learner paste code, run it, and check it against expected output.

    Returns ``True`` only when the program's output matches ``expected_output``.
    """
    code = utils.read_multiline("Paste your solution")
    if not code.strip():
        utils.info("Nothing to run.")
        return False

    with utils.console.status("[bold]Running your code…[/bold]", spinner="dots"):
        result = runner.run_code(code)

    if result.timed_out:
        utils.error("Your code timed out (a possible infinite loop) and was stopped.")
        return False

    body = utils.escape(result.stdout.rstrip()) if result.stdout.strip() else "[dim](no output)[/dim]"
    utils.panel(body, title="Your output", color=color)
    if not result.ok and result.stderr.strip():
        utils.panel(f"[red]{utils.escape(result.stderr.rstrip())}[/red]", title="Error", color="red")

    if not exercise.expected_output:
        utils.info("No expected output is recorded for this drill — compare it yourself.")
        return False
    if runner.output_matches(result.stdout, exercise.expected_output):
        utils.success("✓ Output matches the expected output — nicely done!")
        return True
    utils.warn("Output doesn't match the expected output yet — keep at it.")
    utils.panel(utils.escape(exercise.expected_output), title="Expected output", color="cyan")
    return False


def run_exercise(exercise: Exercise, *, color: str = "green") -> bool:
    """Run the interactive exercise loop.

    Returns ``True`` if the drill is completed (verified by running the learner's
    code, or self-reported), ``False`` otherwise.
    """
    show_exercise(exercise, color=color)
    utils.info(
        "Solve it in your editor, then choose 'Run & check my solution' to verify "
        "your output — or mark it complete yourself."
    )

    while True:
        choice = utils.menu(
            "Coding Drill",
            [
                "Run & check my solution",
                "Show / reveal another hint",
                "Reveal the full solution",
                "Mark this drill complete",
                "Skip for now",
            ],
            color=color,
        )
        if choice == 1:
            if _run_and_check(exercise, color=color) and utils.confirm(
                "Mark this drill complete?", default=True
            ):
                utils.success("Nice work — drill marked complete!")
                return True
        elif choice == 2:
            _walk_hints(exercise)
        elif choice == 3:
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
        elif choice == 4:
            if utils.confirm("Did you complete the drill yourself?", default=True):
                utils.success("Nice work — drill marked complete!")
                return True
            utils.info("No worries — finish it and come back.")
        else:  # choice == 5 (the menu only yields 1-5)
            utils.info("Skipped. You can return to this drill any time.")
            return False
