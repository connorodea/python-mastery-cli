# Bug Log

A running tally of bugs found while hardening `python-mastery-cli`, the test(s)
written to reproduce each, the fix, and the files involved. Maintained by the
`/loop` test-and-fix cycle.

| # | Date | Bug | Reproducing test | Fix | Files |
|---|------|-----|------------------|-----|-------|
| 1 | 2026-06-22 | **Ctrl-D / EOF (and Ctrl-C) at a menu prompt aborted with exit code 1** instead of exiting gracefully. The `run()` loop only caught `KeyboardInterrupt` *inside* an action (not at the menu) and never caught `EOFError`; the `lessons`/`quiz`/`projects` subcommands had no handling either. Real-world repro: `printf '' \| python-mastery start` → `Aborted.` / `EXIT=1`. | `test_run_exits_gracefully_on_eof`, `test_run_keyboardinterrupt_at_menu_returns_then_exits`, `test_lessons_command_eof_exits_cleanly` | Wrapped the whole `run()` loop body in `try/except`: `EOFError` → save + goodbye + exit 0; `KeyboardInterrupt` → return to menu. Added a `_guard()` helper in `main.py` wrapping the interactive subcommands. Now exits 0 with a friendly message everywhere. | `src/python_mastery_cli/app.py`, `src/python_mastery_cli/main.py`, `tests/test_app_interactive.py`, `tests/test_cli.py` |

## Iteration log

### 2026-06-22 — Iteration 1: branch-coverage hardening
- **Bugs found: 0.** Enabled `--cov-branch` and found 23 partial branches (99%).
  Investigated every one — all were **test gaps or unreachable defensive
  branches**, not functional defects.
- Added 11 tests closing the coverable branches (`tests/test_branches.py` +
  additions to `test_app_interactive.py`, `test_runners.py`, `test_progress.py`):
  minimal-content lesson/project, empty tutor question, no-key-terms context,
  `explain_code_line` without surrounding, client build without `base_url`,
  idempotent exercise re-mark, reveal-then-decline-walkthrough.
- Refactored a dead `elif choice == 4` → `else` in `exercises.py` (the menu only
  yields 1–4, so the fall-through branch was unreachable).
- Marked genuinely-unreachable defensive branches with `# pragma: no branch`
  (with explanatory comments): the `isinstance(x, str)` guards in `models.py`
  (`Level`/`QuestionType` subclass `str`, so always true), the `if action:`
  dispatch guard in `app.py`, and the `next_lesson_id` auto-link guards in
  `curriculum/__init__.py`.
- Enforced **100% line + branch coverage** in `pyproject.toml`
  (`[tool.coverage] fail_under = 100`, `branch = true`).
- **Result: 196 tests, 100% line + 100% branch coverage.**

### 2026-06-22 — Iteration 2: runtime/exploratory bug-hunting
- **Bugs found & fixed: 1** (see Bug #1 above — graceful EOF/Ctrl-C exit).
- Method: ran the real CLI under failure conditions (empty stdin / Ctrl-D,
  Ctrl-C at menu, very narrow terminal `COLUMNS=20`, EOF on each subcommand).
- Narrow-terminal rendering: **no crash** (Rich reflows correctly).
- Added 3 reproducing tests; all now pass.
- **Result: 199 tests, 100% line + 100% branch coverage.**
