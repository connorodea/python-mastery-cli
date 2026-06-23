"""The interactive application controller.

`PythonMasteryApp` owns the run-loop and every screen the learner sees. It glues
together the curriculum, the quiz engine, the exercise runner, and progress
persistence. The Typer commands in ``main.py`` are thin wrappers that construct
this object and call one of its public methods.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from rich.table import Table
from rich.text import Text

from . import curriculum, exercises, progress as prog, quiz, theme as th, utils
from .ai_tutor import AITutor, AITutorError
from .models import Lesson, Project
from .utils import console


class PythonMasteryApp:
    """Stateful façade over the whole learning experience."""

    def __init__(self, progress_path: Optional[Path] = None) -> None:
        self.progress_path = progress_path
        self.lessons: list[Lesson] = curriculum.get_all_lessons()
        self.projects: list[Project] = curriculum.get_all_projects()
        self.progress = prog.load_progress(self.progress_path)
        self.tutor = AITutor()

    # ------------------------------------------------------------------ #
    # Persistence helper
    # ------------------------------------------------------------------ #
    def _save(self) -> None:
        self.progress.current_level = prog.infer_current_level(self.progress, self.lessons)
        try:
            prog.save_progress(self.progress, self.progress_path)
        except OSError as exc:
            # A bad PYTHON_MASTERY_HOME (e.g. pointing at a file) must not crash
            # the app on every action — warn and carry on.
            utils.warn(f"Could not save progress ({exc}).")

    # ------------------------------------------------------------------ #
    # Top-level loop
    # ------------------------------------------------------------------ #
    def run(self) -> None:
        """Launch the full interactive experience."""
        utils.clear()
        utils.banner()
        while True:
            self.show_dashboard()
            tutor_available = self.tutor.is_available()
            try:
                choice = utils.menu(
                    "Main menu",
                    [
                        "Continue learning",
                        "Browse lessons",
                        "Take a quiz",
                        "Practice coding drills",
                        "Build mini-projects",
                        "Ask the AI tutor",
                        "View progress",
                        "Reset progress",
                        "Exit",
                    ],
                    descriptions=[
                        "Pick up right where you left off",
                        "Jump to any lesson by level",
                        "Test yourself — 4 question types",
                        "Hands-on drills with hints & solutions",
                        "Build 12 real, practical projects",
                        "Live explanations & examples" if tutor_available else "Run 'configure' to enable",
                        "Streak, score, and per-level breakdown",
                        "Wipe progress and start fresh",
                        "Save and leave",
                    ],
                    icons=[
                        th.glyph("play"),
                        th.glyph("book"),
                        th.glyph("quiz"),
                        th.glyph("drill"),
                        th.glyph("project"),
                        th.glyph("robot"),
                        th.glyph("chart"),
                        th.glyph("reset"),
                        th.glyph("exit"),
                    ],
                )
                if choice == 9:
                    break
                action = {
                    1: self.continue_learning,
                    2: self.browse_lessons,
                    3: self.quiz_menu,
                    4: self.practice_drills,
                    5: self.build_projects,
                    6: self.ai_tutor_menu,
                    7: self.view_progress,
                    8: self.reset_progress_interactive,
                }.get(choice)
                if action:  # pragma: no branch - choices 1-8 always map; 9 breaks above
                    action()
            except KeyboardInterrupt:
                # Ctrl-C anywhere in the menu/action returns to the main menu.
                console.print("\n[dim]Returning to the main menu…[/dim]")
            except EOFError:
                # Ctrl-D / end of input — exit the loop gracefully.
                break
        self._save()
        console.print("\n[bold blue]Keep going — consistency beats intensity. See you soon![/bold blue]\n")

    # ------------------------------------------------------------------ #
    # Dashboard
    # ------------------------------------------------------------------ #
    def show_dashboard(self) -> None:
        total = len(self.lessons)
        done = len(self.progress.completed_lessons)
        nxt = prog.recommend_next_lesson(self.progress, self.lessons)
        streak = self.progress.streak_count
        flame = f"{th.glyph('flame')} " if streak >= 2 else ""

        # A boxless strip of stats — type and whitespace, no borders.
        utils.stat_strip(
            [
                ("Level", self.progress.current_level.title()),
                ("Score", f"{self.progress.total_score} pts"),
                ("Streak", f"{flame}{streak}d"),
                ("Lessons", f"{done}/{total}"),
                ("Projects", f"{len(self.progress.completed_projects)}/{len(self.projects)}"),
            ]
        )

        utils.blank()
        utils.eyebrow("Progress")
        console.print(utils.progress_bar(done, total))

        utils.blank()
        utils.eyebrow("Up next")
        if nxt is not None:
            line = Text()
            line.append(f"{th.glyph('play')}  ", style="brand")
            line.append(nxt.title, style="card.value")
            line.append(f"     {nxt.level} · ~{nxt.estimated_minutes} min", style="muted")
            console.print(line)
        else:
            console.print(
                Text(f"{th.glyph('trophy')}  All lessons complete — you've mastered the core course!", style="success")
            )
        utils.hairline()

    # ------------------------------------------------------------------ #
    # Continue / lessons
    # ------------------------------------------------------------------ #
    def continue_learning(self) -> None:
        nxt = prog.recommend_next_lesson(self.progress, self.lessons)
        if nxt is None:
            utils.success("You've completed every lesson! Try the projects or a mixed quiz.")
            utils.pause()
            return
        self.run_lesson(nxt)

    def browse_lessons(self) -> None:
        levels = ["beginner", "intermediate", "advanced"]
        choice = utils.menu(
            "Browse Lessons",
            [f"{lvl.title()} track" for lvl in levels] + ["Back to main menu"],
        )
        if choice == len(levels) + 1:
            return
        level = levels[choice - 1]
        self._browse_level(level)

    def _browse_level(self, level: str) -> None:
        lessons = curriculum.get_lessons_by_level(level)
        color = utils.level_color(level)
        completed = set(self.progress.completed_lessons)

        table = Table(title=f"{level.title()} Lessons", header_style=f"bold {color}", expand=True)
        table.add_column("#", justify="right", style="dim", no_wrap=True)
        table.add_column("Lesson")
        table.add_column("Time", justify="right")
        table.add_column("Done", justify="center")
        for i, lesson in enumerate(lessons, start=1):
            mark = f"[green]{th.glyph('check')}[/green]" if lesson.id in completed else f"[dim]{th.glyph('todo')}[/dim]"
            table.add_row(str(i), lesson.title, f"{lesson.estimated_minutes}m", mark)
        console.print(table)

        labels = [f"{lesson.title}" for lesson in lessons] + ["Back"]
        choice = utils.menu("Pick a lesson", labels, color=color)
        if choice == len(lessons) + 1:
            return
        self.run_lesson(lessons[choice - 1])

    # ------------------------------------------------------------------ #
    # The full lesson experience
    # ------------------------------------------------------------------ #
    def run_lesson(self, lesson: Lesson) -> None:
        color = utils.level_color(lesson.level)
        utils.clear()
        utils.heading(
            lesson.title,
            color=color,
            kicker=f"{lesson.level} · ~{lesson.estimated_minutes} min · {lesson.quiz_count} quiz",
        )

        # 1. Explanation
        utils.panel(lesson.explanation.strip(), title="Concept", color=color)

        # 2. Key terms
        if lesson.key_terms:
            utils.heading("Key terms", color=color)
            utils.key_terms_table(lesson.key_terms, color=color)

        # 3. Worked examples (with optional line-by-line walkthrough on demand)
        if lesson.code_examples:
            utils.heading("Examples", color=color)
            for example in lesson.code_examples:
                utils.render_code(example, color=color)
            self._offer_walkthroughs(lesson.code_examples, color=color)

        # 4. Common mistakes
        if lesson.common_mistakes:
            utils.heading("Common mistakes to avoid", color="red")
            utils.bullet_list(lesson.common_mistakes, marker="✗", style="red")

        # 4b. Optional AI tutor — deeper explanations / examples / Q&A on demand
        self._offer_lesson_tutor(lesson)

        utils.pause("Press Enter when you're ready for comprehension questions")

        # 5. Comprehension prompts (open reflection — not graded)
        if lesson.practice_prompts:
            utils.heading("Check your understanding", color=color)
            console.print("[dim]Answer out loud or in your editor — these are for reflection.[/dim]")
            for prompt in lesson.practice_prompts:
                utils.console.print(f"\n[bold]?[/bold] {prompt}")
                utils.ask("Your thoughts (Enter to continue)", default="")

        # 6. Graded quiz
        result = None
        if lesson.quiz_questions:
            result = quiz.run_quiz(lesson.quiz_questions, title=f"{lesson.title} — Quiz", color=color)

        # 7. Mini coding exercise
        exercise_done = False
        if lesson.mini_exercise is not None:
            if utils.confirm("\nReady for the coding drill?", default=True):
                exercise_done = exercises.run_exercise(lesson.mini_exercise, color=color)

        # 8. Record progress
        self._record_lesson_completion(lesson, result, exercise_done)
        utils.pause()

    def _record_lesson_completion(self, lesson: Lesson, result, exercise_done: bool) -> None:
        newly_complete = not self.progress.is_lesson_complete(lesson.id)
        prog.mark_lesson_complete(self.progress, lesson.id)

        if result is not None:
            prog.mark_quiz_complete(self.progress, f"{lesson.id}::quiz", score=result.score)
        if exercise_done and lesson.mini_exercise is not None:
            prog.mark_exercise_complete(self.progress, lesson.mini_exercise.id)

        self._save()

        if newly_complete:
            utils.success(f"Lesson complete: {lesson.title}  (+10 pts)")
        else:
            utils.info(f"Reviewed: {lesson.title}")

        nxt_id = lesson.next_lesson_id
        nxt = curriculum.get_lesson(nxt_id) if nxt_id else None
        if nxt is not None:
            console.print(f"[dim]Recommended next:[/dim] [bold cyan]{nxt.title}[/bold cyan]")

    # ------------------------------------------------------------------ #
    # Line-by-line walkthroughs (available throughout the app)
    # ------------------------------------------------------------------ #
    def _offer_walkthroughs(self, examples, *, color: str = "blue") -> None:
        """Let the learner step through any example line by line, as needed."""
        if not examples:
            return
        while utils.confirm("\nStep through an example line by line?", default=False):
            if len(examples) == 1:
                chosen = examples[0]
            else:
                labels = [
                    ex.title + (" [dim](annotated)[/dim]" if ex.has_walkthrough else "")
                    for ex in examples
                ] + ["Cancel"]
                choice = utils.menu("Which example?", labels, color=color)
                if choice == len(examples) + 1:
                    break
                chosen = examples[choice - 1]
            utils.walkthrough(
                chosen.code,
                chosen.line_notes,
                title=f"{chosen.title} — line by line",
                color=color,
            )

    @staticmethod
    def _offer_code_walkthrough(code: str, *, title: str, color: str = "blue") -> None:
        """Offer a line-by-line walkthrough of a raw code string (solutions, etc.)."""
        if code and utils.confirm("Walk through this code line by line?", default=False):
            utils.walkthrough(code, title=title, color=color)

    # ------------------------------------------------------------------ #
    # AI tutor (optional — powered by OpenAI)
    # ------------------------------------------------------------------ #
    def _tutor_run(self, action) -> None:
        """Run a tutor call with a spinner and render the Markdown answer."""
        try:
            with console.status("[bold blue]Asking the AI tutor…[/bold blue]", spinner="dots"):
                text = action()
        except AITutorError as exc:
            utils.error(f"AI tutor error: {exc}")
            return
        if text:
            utils.render_markdown(text, title="AI Tutor", color="blue")
        else:
            utils.warn("The tutor returned an empty response — try rephrasing.")

    def _show_tutor_setup_help(self) -> None:
        utils.panel(
            self.tutor.unavailable_reason()
            + "\n\nOnce configured, the tutor can re-explain concepts, generate "
            "fresh examples, go deeper, and answer your questions — grounded in "
            "the lesson you're on.",
            title="AI Tutor — not configured yet",
            color="yellow",
        )

    def _offer_lesson_tutor(self, lesson: Lesson) -> None:
        """During a lesson, let the learner pull extra help from the AI tutor."""
        if not self.tutor.is_available():
            return  # stay quiet during lessons if it isn't set up
        color = utils.level_color(lesson.level)
        while utils.confirm("\nWant the AI tutor to help with this lesson?", default=False):
            choice = utils.menu(
                f"AI Tutor — {self.tutor.model}",
                [
                    "Explain this more simply",
                    "Give me another example",
                    "Go deeper (in-depth discussion)",
                    "Ask my own question",
                    "Done",
                ],
                color=color,
            )
            if choice == 1:
                self._tutor_run(lambda: self.tutor.explain_more(lesson))
            elif choice == 2:
                self._tutor_run(lambda: self.tutor.another_example(lesson))
            elif choice == 3:
                self._tutor_run(lambda: self.tutor.go_deeper(lesson))
            elif choice == 4:
                question = utils.ask("What's your question?")
                if question.strip():
                    self._tutor_run(lambda: self.tutor.answer(question, lesson))
            else:
                break

    def ai_tutor_menu(self) -> None:
        """Standalone AI tutor chat reachable from the main menu."""
        utils.clear()
        utils.heading("AI Tutor", color="blue")
        if not self.tutor.is_available():
            self._show_tutor_setup_help()
            utils.pause()
            return

        # Ground answers in whatever the learner is working on next.
        context_lesson = prog.recommend_next_lesson(self.progress, self.lessons)
        ctx_note = f" (context: {context_lesson.title})" if context_lesson else ""
        utils.info(f"Model: [bold]{self.tutor.model}[/bold]{ctx_note}")
        console.print("[dim]Ask any Python question. Type 'q' to return to the menu.[/dim]")

        while True:
            question = utils.ask("\nYou")
            if question.strip().lower() in ("q", "quit", "exit", ""):
                break
            self._tutor_run(lambda q=question: self.tutor.answer(q, context_lesson))

    # ------------------------------------------------------------------ #
    # Quizzes
    # ------------------------------------------------------------------ #
    def quiz_menu(self) -> None:
        choice = utils.menu(
            "Quizzes",
            [
                "Quiz from a specific lesson",
                "Mixed review quiz (10 random questions)",
                "Back to main menu",
            ],
        )
        if choice == 3:
            return
        if choice == 1:
            self._quiz_from_lesson()
        else:
            self._mixed_quiz()

    def _quiz_from_lesson(self) -> None:
        quizzable = [lesson for lesson in self.lessons if lesson.quiz_questions]
        labels = [f"{lesson.title} [dim]({lesson.quiz_count} q)[/dim]" for lesson in quizzable] + ["Back"]
        choice = utils.menu("Pick a lesson to quiz on", labels)
        if choice == len(quizzable) + 1:
            return
        lesson = quizzable[choice - 1]
        result = quiz.run_quiz(lesson.quiz_questions, title=f"{lesson.title} — Quiz")
        prog.mark_quiz_complete(self.progress, f"{lesson.id}::quiz", score=result.score)
        self._save()
        utils.pause()

    def _mixed_quiz(self) -> None:
        # Deterministic-ish spread across the course: every Nth question.
        pool = [q for lesson in self.lessons for q in lesson.quiz_questions]
        if not pool:
            utils.warn("No quiz questions available yet.")
            utils.pause()
            return
        step = max(1, len(pool) // 10)
        selected = pool[::step][:10]
        result = quiz.run_quiz(selected, title="Mixed Review Quiz", color="magenta")
        prog.mark_quiz_complete(self.progress, "mixed::review", score=result.score)
        self._save()
        utils.pause()

    # ------------------------------------------------------------------ #
    # Coding drills
    # ------------------------------------------------------------------ #
    def practice_drills(self) -> None:
        drills = [(lesson, lesson.mini_exercise) for lesson in self.lessons if lesson.has_exercise]
        if not drills:
            utils.warn("No coding drills available yet.")
            utils.pause()
            return
        completed = set(self.progress.completed_exercises)
        labels = []
        for lesson, exercise in drills:
            mark = f"[green]{th.glyph('check')}[/green] " if exercise.id in completed else ""
            labels.append(f"{mark}{exercise.title} [dim]({lesson.level})[/dim]")
        labels.append("Back")
        choice = utils.menu("Coding Drills", labels)
        if choice == len(drills) + 1:
            return
        lesson, exercise = drills[choice - 1]
        if exercises.run_exercise(exercise, color=utils.level_color(lesson.level)):
            prog.mark_exercise_complete(self.progress, exercise.id)
            self._save()
        utils.pause()

    # ------------------------------------------------------------------ #
    # Projects
    # ------------------------------------------------------------------ #
    def build_projects(self) -> None:
        completed = set(self.progress.completed_projects)
        table = Table(title="Mini-Projects", header_style="bold yellow", expand=True)
        table.add_column("#", justify="right", style="dim")
        table.add_column("Project")
        table.add_column("Difficulty")
        table.add_column("Done", justify="center")
        for i, project in enumerate(self.projects, start=1):
            mark = f"[green]{th.glyph('check')}[/green]" if project.id in completed else f"[dim]{th.glyph('todo')}[/dim]"
            table.add_row(str(i), project.title, project.difficulty, mark)
        console.print(table)

        labels = [p.title for p in self.projects] + ["Back"]
        choice = utils.menu("Pick a project", labels, color="yellow")
        if choice == len(self.projects) + 1:
            return
        self.run_project(self.projects[choice - 1])

    def run_project(self, project: Project) -> None:
        utils.clear()
        utils.heading(project.title, color="yellow")
        console.print(
            f"[dim]Difficulty: {project.difficulty} • ~{project.estimated_minutes} min[/dim]"
        )

        utils.panel("  ".join(f"[bold]#{c}[/bold]" for c in project.concepts) or "—",
                    title="Concepts you'll practice", color="yellow")

        utils.heading("Requirements", color="yellow")
        utils.bullet_list(project.requirements, marker="•", style="yellow")

        utils.heading("Step-by-step build guide", color="yellow")
        utils.numbered_list(project.build_guide, style="bold yellow")

        if project.starter_code:
            utils.render_python(project.starter_code, title="Starter code", color="yellow")
            self._offer_code_walkthrough(project.starter_code, title=f"{project.title} — starter code", color="yellow")

        if project.milestones:
            utils.heading("Milestones", color="yellow")
            utils.bullet_list(project.milestones, marker="▸", style="green")

        if project.stretch_goals:
            utils.heading("Stretch goals", color="yellow")
            utils.bullet_list(project.stretch_goals, marker="★", style="magenta")

        # Solution is opt-in so learners try first.
        if project.solution and utils.confirm("\nReveal the reference solution?", default=False):
            utils.render_python(project.solution, title="Reference solution", color="yellow")
            self._offer_code_walkthrough(project.solution, title=f"{project.title} — solution", color="yellow")

        if utils.confirm("\nMark this project complete?", default=False):
            newly = not self.progress.is_project_complete(project.id)
            prog.mark_project_complete(self.progress, project.id)
            self._save()
            if newly:
                utils.success(f"Project complete: {project.title}  (+50 pts)")
            else:
                utils.info("Project already completed — nice to revisit it!")
        utils.pause()

    # ------------------------------------------------------------------ #
    # Progress views
    # ------------------------------------------------------------------ #
    def view_progress(self) -> None:
        utils.clear()
        utils.heading("Your Progress", color="blue")
        total = len(self.lessons)
        done = len(self.progress.completed_lessons)

        summary = Table.grid(padding=(0, 2))
        summary.add_column(style="bold")
        summary.add_column()
        summary.add_row("Total score", f"{self.progress.total_score} pts")
        summary.add_row("Current level", self.progress.current_level.title())
        summary.add_row("Lessons completed", f"{done}/{total} "
                        f"({prog.completion_percentage(self.progress, total):.0f}%)")
        summary.add_row("Quizzes completed", str(len(self.progress.completed_quizzes)))
        summary.add_row("Drills completed", str(len(self.progress.completed_exercises)))
        summary.add_row("Projects completed", f"{len(self.progress.completed_projects)}/{len(self.projects)}")
        summary.add_row("Current streak", f"{self.progress.streak_count} day(s)")
        summary.add_row("Last active", self.progress.last_active_date or "—")
        utils.panel(summary, title="Summary", color="blue")

        # Per-level breakdown with progress bars.
        breakdown = prog.level_breakdown(self.progress, self.lessons)
        table = Table(title="By level", header_style="bold blue", expand=True)
        table.add_column("Level")
        table.add_column("Progress")
        for level in ("beginner", "intermediate", "advanced"):
            comp, tot = breakdown.get(level, (0, 0))
            color = utils.level_color(level)
            table.add_row(f"[{color}]{level.title()}[/{color}]", utils.progress_bar_text(comp, tot))
        console.print(table)
        utils.pause()

    def reset_progress_interactive(self) -> None:
        utils.warn("This will erase all completed lessons, quizzes, drills, projects, and your score.")
        if utils.confirm("Are you absolutely sure you want to reset?", default=False):
            self.progress = prog.reset_progress(self.progress_path)
            utils.success("Progress reset. Fresh start!")
        else:
            utils.info("Reset cancelled — your progress is safe.")
        utils.pause()
