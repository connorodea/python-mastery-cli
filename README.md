# 🐍 Python Mastery CLI

> An interactive, terminal-based course that takes you from **absolute beginner**
> to **advanced practical Python developer** — lessons, runnable examples,
> line-by-line code walkthroughs, quizzes, coding drills, and guided projects,
> all with local progress tracking.

Built for self-paced, deliberate practice. Open your terminal, run one command,
and learn Python the way you'd learn an instrument: a little every day, with
immediate feedback and lots of repetition.

---

## What it does

`python-mastery-cli` turns your terminal into a structured Python classroom:

- **63 lessons** across three tracks — **Beginner (20)**, **Intermediate (24)**,
  and **Advanced (19)** — each with a plain-English explanation, a glossary of
  key terms, syntax-highlighted examples, common mistakes, comprehension prompts,
  a short quiz, and a hands-on coding drill.
- **Line-by-line code walkthroughs.** For any example (and any solution), step
  through the code one line at a time and read a plain-language explanation of
  what each line does — exactly when you need it.
- **12 guided mini-projects** — from a calculator CLI to a SQLite contact book and
  a mini data dashboard — each with requirements, a step-by-step build guide,
  starter code, milestones, stretch goals, and a complete reference solution.
- **Quizzes** with four question types (multiple choice, true/false,
  fill-in-the-blank, short-answer keyword matching), instant feedback, and scoring.
- **Local progress tracking** — completed lessons/quizzes/drills/projects, total
  score, daily streak, and a per-level progress breakdown.

The curriculum leans toward practical, data-oriented skills (pandas, matplotlib,
SQLite, CSV/JSON wrangling) — useful if you're heading into data science.

---

## Installation

Requires **Python 3.10+**.

```bash
# from the project root (where pyproject.toml lives)
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -e .                 # installs the `python-mastery` command
# or, with test dependencies:
pip install -e ".[dev]"
```

---

## Usage

Launch the full interactive experience:

```bash
python-mastery
```

You'll see a dashboard (progress, streak, next recommended lesson) and the main
menu:

```
1. Continue learning      5. Build mini-projects
2. Browse lessons         6. View progress
3. Take a quiz            7. Reset progress
4. Practice coding drills 8. Exit
```

### CLI commands

| Command | What it does |
| --- | --- |
| `python-mastery` | Launch the full interactive dashboard + menu |
| `python-mastery start` | Same as above (explicit) |
| `python-mastery lessons` | Browse and study lessons by level |
| `python-mastery quiz` | Take a lesson quiz or a mixed review quiz |
| `python-mastery projects` | Browse and build guided mini-projects |
| `python-mastery progress` | View your detailed progress report |
| `python-mastery reset-progress` | Wipe progress and start fresh (asks first) |
| `python-mastery configure` | Set up the AI tutor (OpenAI API key + model) |
| `python-mastery ask "<question>"` | Ask the AI tutor a one-off question |
| `python-mastery models` | List chat models available on your OpenAI account |
| `python-mastery --version` | Print the version |

### Studying a lesson

Each lesson walks you through, in order:

1. **Concept** — a clear, multi-paragraph explanation.
2. **Key terms** — a quick glossary.
3. **Examples** — syntax-highlighted, with optional output.
4. **Line-by-line walkthrough** *(on demand)* — step through any example one line
   at a time. While stepping: `Enter` = next, `b` = back, a number = jump to that
   line, `a` = show every annotation at once, `q` = quit.
5. **Common mistakes** to avoid.
6. **Comprehension prompts** — open reflection questions (not graded).
7. **Quiz** — graded, with explanations and a running score.
8. **Coding drill** — instructions, starter code, expected output, progressive
   hints, and a revealable solution. You write the code in your own editor and
   self-report completion (see below).

---

## 🤖 AI tutor (optional, powered by OpenAI)

On top of the static curriculum, an optional AI tutor gives you **on-demand,
context-aware help** — it always knows which lesson you're on.

**One-time setup:**

```bash
python-mastery configure        # paste your OpenAI API key when prompted
```

This stores your settings in `~/.python_mastery_cli/config.json` (`chmod 600`,
in your home directory — **never** inside the repo, so it can't be committed) and
**auto-selects the newest, cheapest model** available on your account (e.g.
`gpt-5.x-nano` / `gpt-4o-mini`). Override anytime:

```bash
python-mastery configure --model gpt-4o      # pick a specific model
python-mastery models                          # see what's available
```

Prefer not to store anything on disk? Use environment variables instead — they
take precedence over the config file:

```bash
export OPENAI_API_KEY="sk-..."
export OPENAI_MODEL="gpt-4o-mini"     # optional
export OPENAI_BASE_URL="https://..."  # optional: any OpenAI-compatible endpoint
```

**Where the tutor shows up:**

- **In a lesson** — after the examples you'll be offered: *Explain this more
  simply* · *Give me another example* · *Go deeper (in-depth discussion)* ·
  *Ask my own question*. Answers are grounded in the current lesson.
- **Main menu → "Ask the AI tutor"** — a free-form chat for any Python question,
  seeded with your next recommended lesson as context.
- **`python-mastery ask "..."`** — quick one-off questions from your shell.

**Notes:**

- The tutor degrades gracefully: with no key configured, the rest of the app
  works exactly as before and the menu item shows *(needs setup)*.
- Model differences (e.g. `gpt-5.x`/o-series requiring `max_completion_tokens`
  and a fixed `temperature`) are handled automatically.
- **Security:** treat any API key shared in plain text (chat, logs, screen-share)
  as compromised and **rotate it** at <https://platform.openai.com/api-keys>.
  Keys are never printed by the app and never written into the repository.

## Why coding drills aren't auto-run

The app **never executes code you write**. Running arbitrary user code from a
learning tool is a security and reliability risk (and platform-specific to
sandbox well). Instead, each drill gives you instructions, starter code, the
expected output, hints, and a reference solution, and lets you mark it complete
yourself. The focus stays on *understanding* — which is what actually builds
skill.

---

## How progress tracking works

Progress is stored as JSON in your home directory so the app keeps working even
when installed read-only into `site-packages`:

```
~/.python_mastery_cli/progress.json
```

You can redirect this (handy for testing or multiple profiles) with an
environment variable:

```bash
PYTHON_MASTERY_HOME=/tmp/my-profile python-mastery
```

A pristine template ships at `src/python_mastery_cli/data/progress.json` and is
used to seed a fresh profile. Tracked fields:

- `completed_lessons`, `completed_quizzes`, `completed_exercises`,
  `completed_projects`
- `current_level`, `total_score`, `streak_count`, `last_active_date`

Scoring: lessons +10, drills +15, projects +50, quiz answers +5/+8/+12 by
difficulty. The streak increments on consecutive days and resets after a gap.

---

## Project structure

```
python-mastery-cli/
├── pyproject.toml              # build config + the `python-mastery` entry point
├── README.md
├── .gitignore
├── src/
│   └── python_mastery_cli/
│       ├── __init__.py
│       ├── main.py             # Typer CLI (commands + entry point)
│       ├── app.py              # interactive controller (dashboard, lesson flow…)
│       ├── models.py           # dataclasses: Lesson, CodeExample, QuizQuestion…
│       ├── progress.py         # load/save/mark/reset + analytics
│       ├── quiz.py             # grading (pure) + interactive runner
│       ├── exercises.py        # coding-drill runner (hints, reveal, complete)
│       ├── config.py           # local settings + API key (chmod 600)
│       ├── ai_tutor.py         # optional OpenAI-powered tutor
│       ├── utils.py            # all Rich UI helpers + the walkthrough renderer
│       ├── curriculum/
│       │   ├── __init__.py     # registry: aggregates + validates content
│       │   ├── beginner.py     # 20 lessons
│       │   ├── intermediate.py # 24 lessons
│       │   ├── advanced.py     # 19 lessons
│       │   └── projects.py     # 12 guided projects
│       └── data/
│           └── progress.json   # pristine progress template
└── tests/
    ├── conftest.py
    ├── test_progress.py        # load/save, mutations, streaks, analytics
    ├── test_quiz.py            # grading for all 4 question types + scoring
    ├── test_curriculum.py      # content validation + recommendation logic
    ├── test_app_flow.py        # interactive lesson/project/walkthrough glue
    └── test_ai_tutor.py        # AI tutor + config (fully mocked, no network)
```

---

## How to add new lessons

1. Open the relevant track file in `src/python_mastery_cli/curriculum/`
   (`beginner.py`, `intermediate.py`, or `advanced.py`).
2. Append a `Lesson(...)` to that module's list (`BEGINNER_LESSONS`, etc.).
   Give it a unique `id`. Leave `next_lesson_id=None` — the registry
   auto-chains lessons in order.
3. Fill in the fields. A minimal lesson:

   ```python
   from ..models import CodeExample, Exercise, Lesson, Level, QuizQuestion

   Lesson(
       id="b21",
       title="A New Topic",
       level=Level.BEGINNER,
       estimated_minutes=10,
       explanation="Two or three short paragraphs that actually teach it...",
       key_terms={"Term": "Definition."},
       code_examples=[
           CodeExample(
               title="Demo",
               code="print('hi')",
               output="hi",
               # 1-indexed line numbers -> plain-language explanation:
               line_notes={1: "print() shows text on screen."},
           ),
       ],
       common_mistakes=["A typical pitfall."],
       practice_prompts=["A reflection question."],
       quiz_questions=[
           QuizQuestion(
               question="What does print do?",
               qtype="short_answer",
               correct_answer="shows text",
               keywords=["text"],
               explanation="It writes to standard output.",
               difficulty="easy",
           ),
       ],
       mini_exercise=Exercise(
           id="b21-ex",
           title="Try it",
           instructions="Print your name.",
           expected_output="Ada",
           hints=["Use print()."],
           solution="print('Ada')",
       ),
   )
   ```

4. Run the tests — `test_curriculum.py` validates ids are unique, the
   `next_lesson_id` chain is intact, all four question types are used, and that
   `line_notes` reference real lines.

To add a **project**, append a `Project(...)` to `PROJECTS` in `projects.py`.

> **Tip:** `line_notes` keys are 1-indexed line numbers *within the snippet*
> (after leading/trailing blank lines are trimmed). The model raises a clear
> error at import time if a note points at a line that doesn't exist.

---

## Development

```bash
pip install -e ".[dev]"
python -m compileall src      # byte-compile everything
pytest                        # run the test suite
```

---

## Future improvement ideas

- **Spaced repetition**: resurface quiz questions you got wrong on a schedule.
- **Optional sandboxed execution** of drills (e.g. a restricted subprocess) with
  automatic output comparison.
- **Achievements/badges** and a richer streak/calendar view.
- **Search** across lessons and key terms.
- **Export progress** to Markdown/HTML, and import/export profiles.
- **Pluggable curriculum packs** loaded from external files (YAML/JSON) so the
  course can grow without code changes.
- **Audio/voice** prompts, and a "review mode" that only shows incomplete items.

---

## License

MIT.
