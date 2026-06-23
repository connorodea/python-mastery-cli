# Bug Log

A running tally of bugs found while hardening `python-mastery-cli`, the test(s)
written to reproduce each, the fix, and the files involved. Maintained by the
`/loop` test-and-fix cycle.

| # | Date | Bug | Reproducing test | Fix | Files |
|---|------|-----|------------------|-----|-------|
| 8 | 2026-06-23 | **Arrow keys broke menu navigation — pressing an arrow quit the program** (user-reported). `read_key()` read with the buffered `sys.stdin.read(1)` but checked for follow-up bytes with `select` on the *fd*; the terminal delivers `\x1b[A` as one chunk, the buffered read pulled `[A` into Python's buffer, so `select` saw nothing pending → an arrow decoded as a lone Esc → `_resolve_nav` mapped "esc" to "select last option" → **Exit** → program quit. (Also could block.) Confirmed via PTY: up-arrow returned `'esc'`. **This lived in the one `# pragma: no cover` (TTY-only) path.** | `test_read_sequence_arrow_assembles_full_escape` (+ lone-esc / plain-key / home); verified end-to-end through a real PTY | Read raw bytes with `os.read(fd, …)` so the read and `select` use the same source; extracted the assembly logic into a pure `_read_sequence()` (now unit-tested) and kept only the `os.read`/`termios` glue pragma'd. | `src/python_mastery_cli/keys.py`, `tests/test_keys.py` |
| 7 | 2026-06-23 | **`python-mastery ui --port <busy/invalid>` crashed with an unhandled exception.** A port already in use raised `OSError` and a port >65535 raised `OverflowError`, propagating out of the `ui` command (ugly traceback / exit 1 with no guidance). Plausible when running `ui` twice or typo'ing a port. | `test_ui_command_busy_port_exits_cleanly` | Wrapped the `launch()` call in the `ui` command in `try/except (OSError, OverflowError, ValueError)` → prints a friendly "could not start … try a different port" message and exits 1 cleanly. | `src/python_mastery_cli/main.py`, `tests/test_cli.py` |
| 6 | 2026-06-23 | **Interactive arrow-menu digit-jump mis-fired on menus with >9 options.** A digit key selected option N outright, so (a) options 10+ (e.g. the 27-item browse-by-level menu) were unreachable by number and (b) the first digit of a two-digit position instantly selected the wrong option. | `test_resolve_nav_digit_jumps_highlight_not_select`, `test_select_interactive_two_digits_no_misfire` | A digit now *moves the highlight* (Enter confirms) instead of selecting — unambiguous on long menus and no mis-fire. Also added Home/End → jump to first/last. | `src/python_mastery_cli/utils.py`, `src/python_mastery_cli/keys.py`, `tests/test_keys.py` |
| 4 | 2026-06-22 | **Pressing Enter (blank) at a prompt crashed the app** with `AttributeError: 'NoneType' object has no attribute 'strip'`. `utils.ask` forwarded `default=None` to Rich `Prompt.ask`, which treats `None` as a real default and returns it on blank input; downstream `grade_answer`/`.strip()` (quiz answer prompt, AI-tutor "You" prompt, "ask my own question") then crashed. Hit by simply hitting Return during a quiz. | `test_ask_blank_input_returns_empty_string_not_none`, `test_ask_with_explicit_default_is_passed_through` | `utils.ask` now omits the default when it is `None` (so Rich re-prompts on an invalid choice / returns `""` for free text) and coerces any `None` result to `""`. | `src/python_mastery_cli/utils.py`, `tests/test_utils.py` |
| 5 | 2026-06-22 | **`save_progress` crashed the app if `PYTHON_MASTERY_HOME` pointed at a file** (`FileExistsError` from `mkdir` on a non-dir parent). `_save()` runs on every action/exit, so a bad env var would crash continuously. | `test_save_does_not_crash_on_unwritable_home` | `app._save()` wraps the save in `try/except OSError` → warns and continues instead of crashing. | `src/python_mastery_cli/app.py`, `tests/test_app_interactive.py` |
| 2 | 2026-06-22 | **Type-corrupted `progress.json` crashes or silently corrupts state.** `Progress.from_dict` did no type validation: `total_score`/`streak_count` as a string or `null` → `TypeError` on the next score update; `completed_lessons: "b01"` → silently became `['b','0','1']`; a top-level JSON array/number → `AttributeError` (`.items()`), uncaught. Violated `load_progress`'s "survive a bad file" contract. | `test_from_dict_sanitizes_corrupt_types`, `test_from_dict_coerces_float_score_and_rejects_bool`, `test_from_dict_non_dict_returns_fresh`, `test_corrupt_typed_file_does_not_crash_on_mutation`, `test_load_progress_with_toplevel_json_array_is_safe` | Rewrote `from_dict` to sanitise every field: list fields keep only `str` items (else `[]`), scores coerce to `int` (bool/str/null → `0`), `current_level` must be a non-empty `str` (else `"beginner"`), `last_active_date` must be `str` (else `None`); non-dict input → fresh profile. | `src/python_mastery_cli/progress.py`, `tests/test_progress.py` |
| 3 | 2026-06-22 | **`load_progress(str_path)` / `save_progress(str_path)` crashed** with `AttributeError: 'str' object has no attribute 'exists'` — both assumed a `pathlib.Path`. | `test_load_progress_accepts_str_path` | Coerce `path = Path(path) if path is not None else default_progress_path()` in both functions. | `src/python_mastery_cli/progress.py`, `tests/test_progress.py` |
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

### 2026-06-22 — Iteration 3: data-robustness bug-hunting
- **Bugs found & fixed: 2** (Bug #2 type-corrupt `progress.json`; Bug #3 str-path).
- Method: fed `load_progress` valid-JSON-but-wrong-type files (string/null score,
  string/int `completed_*`, top-level array) and a `str` path; both crashed or
  corrupted state. Hardened `from_dict` + path coercion so a bad file always
  degrades to a safe fresh/sanitised profile.
- Added 6 reproducing tests (all failed pre-fix, pass post-fix).
- **Result: 205 tests, 100% line + 100% branch coverage.**

### 2026-06-23 — Arrow-key navigation fix (user-reported)
- **Bugs found & fixed: 1** (Bug #8 — arrows quit the program instead of navigating).
- Root cause (via systematic debugging + PTY reproduction): `read_key` mixed a
  buffered `sys.stdin.read` with `select` on the fd, so escape sequences were
  misread as a lone Esc → "select last" → Exit. Fixed with `os.read`; extracted
  pure `_read_sequence` for deterministic tests; the bug had hidden in the only
  `# pragma: no cover` (TTY-only) path.
- **Result: 255 tests, 100% line + 100% branch coverage.** Bug tally: 8 total.

### 2026-06-23 — Iteration 9: Tab / Shift-Tab navigation
- **Bugs found: 0** (honest scan — the obvious robustness defects are fixed and
  coverage is maxed; this was a genuine refinement, not invented work).
- Refinement: **Tab** moves the highlight forward and **Shift-Tab** moves it
  back — a near-universal menu affordance that was previously inert.
- Added 4 tests (decode Tab/Shift-Tab, resolve both, Tab/Shift-Tab in the loop).
- **Result: 252 tests, 100% line + 100% branch coverage.** Bug tally still 7.

### 2026-06-23 — Iteration 8: web-server robustness + menu polish
- **Bugs found & fixed: 1** (Bug #7 — `ui` crashed on a busy/invalid port).
- Method: probed the `ui` command's failure modes (port in use, port >65535).
- Aesthetic: the focused menu row now gets a subtle highlight background
  (`SELECTED_BG`) in addition to the ▸ cursor + bold-mint label.
- Added 1 reproducing test (failed pre-fix). 
- **Result: 249 tests, 100% line + 100% branch coverage.** Bug tally: 7 total.

### 2026-06-23 — Iteration 7: refine keyboard navigation
- **Bugs found & fixed: 1** (Bug #6 — digit-jump mis-fire on >9-option menus).
- Refinement: a digit now **moves** the highlight (Enter confirms) rather than
  selecting outright, matching "jump" semantics and fixing the browse-menu
  footgun. Added **Home/End** to jump to first/last option.
- Added 4 tests (decode Home/End, resolve digit→move + home/end, two-digit
  no-misfire, Home/End in the select loop).
- **Result: 248 tests, 100% line + 100% branch coverage.** Bug tally: 6 total.

### 2026-06-23 — Iteration 6: keyboard menu navigation
- **Bugs found: 0** (feature iteration).
- **Feature:** menus are now keyboard-navigable in a real terminal — ↑/↓ (or
  vim j/k) move a highlighted cursor, Enter selects, a digit jumps, and q/Esc
  picks the last option (Back/Exit). New `keys.py` (stdlib `termios`, no deps)
  reads single keypresses; `utils.menu()` auto-detects a TTY and uses an arrow
  loop, falling back to the numbered prompt for scripts/pipes/tests. All menus
  (main + browse/quiz/projects) get this automatically.
- Tests: `decode_key`, the pure `_resolve_nav` logic (all branches), the
  `_render_menu` renderable, and the full select loop driven by an injected key
  reader (no real TTY needed). Only the termios glue + the TTY dispatch are
  `# pragma: no cover`.
- Also (earlier this session): elevated the aesthetic — web SVG progress ring,
  hero card, per-level mini-bars, hover/glow/fade-in + auto-refresh; gradient CLI
  progress bar; lesson-header eyebrow.
- **Result: 242 tests, 100% line + 100% branch coverage.**

### 2026-06-22 — Iteration 5: optional web UI + coverage
- **Bugs found: 0** (feature iteration). Caught one self-inflicted import slip
  during development (`Progress` imported from `models` instead of `progress`) —
  fixed before commit; not a shipped defect.
- **Feature:** added `webui.py` — a minimal, read-only local web dashboard
  (`http.server`, stdlib only) and a `python-mastery ui` command. The CLI stays
  the default; the web view is opt-in (`ui [--port N] [--no-browser]`).
- Tests: pure `build_html`, a real threaded-server HTTP round-trip, `launch`
  non-blocking paths, and the `ui` command (launch patched). Blocking
  `serve_forever` marked `# pragma: no cover`.
- **Result: 215 tests, 100% line + 100% branch coverage.**

### 2026-06-22 — Iteration 4: real end-to-end CLI runs
- **Bugs found & fixed: 2** (Bug #4 blank-input crash — **high severity**, trivially
  hit by pressing Enter at a quiz; Bug #5 save crash on a misconfigured home).
- Method: drove a full lesson through the **real** CLI (real Rich prompts, not
  mocks) via piped input; fuzzed `grade_answer` with adversarial input (unicode,
  huge strings, leading zeros — 0 crashes); probed a home dir pointing at a file.
- Added 3 reproducing tests (failed pre-fix). Real lesson run is now clean.
- **Result: 208 tests, 100% line + 100% branch coverage.**
