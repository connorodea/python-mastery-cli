"""Command-line entry point built with Typer.

Running ``python-mastery`` with no arguments launches the full interactive
experience. Sub-commands jump straight to a specific area of the app:

    python-mastery                 # full interactive dashboard + menu
    python-mastery start           # same as above (explicit)
    python-mastery lessons         # browse and study lessons
    python-mastery quiz            # take a quiz
    python-mastery projects        # build a mini-project
    python-mastery progress        # view your progress report
    python-mastery reset-progress  # wipe progress and start fresh
"""

from __future__ import annotations

from typing import Optional

import typer

from . import __version__, config as cfg, curriculum
from .app import PythonMasteryApp
from .utils import banner, console, error, info, render_markdown, success, warn

app = typer.Typer(
    add_completion=False,
    no_args_is_help=False,
    rich_markup_mode="rich",
    help="Learn Python from absolute beginner to advanced — right in your terminal.",
)


def _version_callback(value: bool) -> None:
    if value:
        console.print(f"python-mastery-cli [bold]v{__version__}[/bold]")
        raise typer.Exit()


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: Optional[bool] = typer.Option(
        None, "--version", "-v", callback=_version_callback, is_eager=True,
        help="Show the version and exit.",
    ),
) -> None:
    """If no sub-command is given, launch the full interactive course."""
    if ctx.invoked_subcommand is None:
        _launch().run()


def _launch() -> PythonMasteryApp:
    """Construct the app, surfacing any curriculum problems early."""
    problems = curriculum.validate_curriculum()
    if problems:
        console.print("[bold red]Curriculum validation problems detected:[/bold red]")
        for problem in problems:
            console.print(f"  [red]•[/red] {problem}")
    return PythonMasteryApp()


def _guard(fn) -> None:
    """Run an interactive flow, exiting cleanly on Ctrl-C / Ctrl-D (no ugly abort)."""
    try:
        fn()
    except (EOFError, KeyboardInterrupt):
        console.print("\n[dim]Exited — run [bold]python-mastery[/bold] for the full experience.[/dim]")


@app.command()
def start() -> None:
    """Launch the full interactive learning experience."""
    _launch().run()


@app.command()
def lessons() -> None:
    """Browse and study lessons by level."""
    application = _launch()
    banner()
    application.show_dashboard()
    _guard(application.browse_lessons)
    info("Tip: run [bold]python-mastery[/bold] for the full guided experience.")


@app.command()
def quiz() -> None:
    """Take a quiz on a lesson or a mixed review quiz."""
    application = _launch()
    banner()
    _guard(application.quiz_menu)
    info("Tip: run [bold]python-mastery[/bold] for the full guided experience.")


@app.command()
def projects() -> None:
    """Browse and build guided mini-projects."""
    application = _launch()
    banner()
    _guard(application.build_projects)
    info("Tip: run [bold]python-mastery[/bold] for the full guided experience.")


@app.command()
def progress() -> None:
    """View your detailed progress report."""
    application = _launch()
    application.view_progress()


@app.command(name="reset-progress")
def reset_progress() -> None:
    """Reset all progress and start fresh (asks for confirmation)."""
    application = _launch()
    application.reset_progress_interactive()


# --------------------------------------------------------------------------- #
# AI tutor commands (OpenAI)
# --------------------------------------------------------------------------- #
@app.command()
def configure(
    api_key: Optional[str] = typer.Option(
        None, "--api-key", help="OpenAI API key (omit to be prompted securely)."
    ),
    model: Optional[str] = typer.Option(
        None, "--model", help="Model id to use (e.g. gpt-4o-mini)."
    ),
    auto_model: bool = typer.Option(
        True, "--auto-model/--no-auto-model",
        help="Auto-pick the newest cheap model available on your account.",
    ),
) -> None:
    """Configure the OpenAI-powered AI tutor (saved to ~/.python_mastery_cli/config.json)."""
    from .ai_tutor import AITutor, recommend_cheap_model

    if api_key is None:
        api_key = typer.prompt("OpenAI API key", hide_input=True)
    api_key = (api_key or "").strip()
    if not api_key:
        error("No API key provided — nothing was saved.")
        raise typer.Exit(code=1)
    cfg.set_api_key(api_key)

    chosen = model
    if not chosen and auto_model:
        try:
            tutor = AITutor(api_key=api_key)
            client = tutor._get_client()
            ids = [m.id for m in client.models.list().data]
            pick = recommend_cheap_model(ids)
            if pick:
                chosen = pick
                info(f"Auto-selected the newest cheap model on your account: [bold]{pick}[/bold]")
            else:
                warn("Couldn't find a cheap model to auto-select; keeping the default.")
        except Exception as exc:  # network/auth issues shouldn't abort setup
            warn(f"Couldn't auto-detect models ({exc}). Keeping default model.")
    if chosen:
        cfg.set_model(chosen)

    success(f"AI tutor configured — model: [bold]{cfg.get_model()}[/bold].")
    info(f"Settings saved to {cfg.config_path()} (permissions 600, outside the repo).")
    console.print("[dim]Security tip: rotate any API key that has been shared in plain text.[/dim]")


@app.command()
def ask(
    question: list[str] = typer.Argument(..., help="Your Python question."),
) -> None:
    """Ask the AI tutor a one-off question and print the answer."""
    from .ai_tutor import AITutor, AITutorError

    tutor = AITutor()
    if not tutor.is_available():
        error(tutor.unavailable_reason())
        raise typer.Exit(code=1)
    text = ""
    try:
        with console.status("[bold blue]Asking the AI tutor…[/bold blue]", spinner="dots"):
            text = tutor.answer(" ".join(question))
    except AITutorError as exc:
        error(str(exc))
        raise typer.Exit(code=1)
    render_markdown(text or "_(empty response)_", title="AI Tutor", color="blue")


@app.command()
def models() -> None:
    """List the chat models available on your OpenAI account."""
    from .ai_tutor import AITutor, recommend_cheap_model

    tutor = AITutor()
    if not tutor.is_available():
        error(tutor.unavailable_reason())
        raise typer.Exit(code=1)
    try:
        client = tutor._get_client()
        ids = sorted(m.id for m in client.models.list().data)
    except Exception as exc:
        error(str(exc))
        raise typer.Exit(code=1)
    pick = recommend_cheap_model(ids)
    console.print("[bold]Available models:[/bold]")
    for model_id in ids:
        marker = "  [green]← cheapest current (recommended)[/green]" if model_id == pick else ""
        console.print(f"  • {model_id}{marker}")
    console.print(f"\nCurrently using: [bold]{cfg.get_model()}[/bold]")


if __name__ == "__main__":  # pragma: no cover
    app()
