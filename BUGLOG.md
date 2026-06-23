# Bug Log

A running tally of bugs found while hardening `python-mastery-cli`, the test(s)
written to reproduce each, the fix, and the files involved. Maintained by the
`/loop` test-and-fix cycle.

| # | Date | Bug | Reproducing test | Fix | Files |
|---|------|-----|------------------|-----|-------|
| — | 2026-06-22 | _No functional bugs found this iteration._ | — | — | — |

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
