"""Tests for the Rich UI helpers in utils.py (rendering + input wrappers)."""

from __future__ import annotations



from python_mastery_cli import theme as th, utils
from python_mastery_cli.models import CodeExample, Level


def _answers(seq):
    """Return a classmethod-compatible Prompt.ask stub that pops from seq."""
    it = iter(seq)

    def _ask(cls, *args, **kwargs):
        return next(it)

    return classmethod(_ask)


# --------------------------------------------------------------------------- #
# Pure helpers
# --------------------------------------------------------------------------- #
def test_level_color_known_and_default():
    assert utils.level_color(Level.BEGINNER) == th.LEVEL["beginner"]
    assert utils.level_color("intermediate") == th.LEVEL["intermediate"]
    assert utils.level_color("advanced") == th.LEVEL["advanced"]
    assert utils.level_color(Level.PROJECT) == th.LEVEL["project"]
    assert utils.level_color("nonsense") == th.CYAN


def test_progress_bar_text_variants():
    assert "0/10" in utils.progress_bar_text(0, 10)
    assert "100.0%" in utils.progress_bar_text(10, 10)
    # total 0 guards divide-by-zero, and done>total caps at 100%.
    assert "0/1" in utils.progress_bar_text(0, 0)
    assert "100.0%" in utils.progress_bar_text(5, 1)


# --------------------------------------------------------------------------- #
# Rendering (just assert they run and emit something)
# --------------------------------------------------------------------------- #
def test_render_helpers_emit_output(capsys):
    utils.banner()
    utils.heading("Section", color="green")
    utils.info("info")
    utils.success("ok")
    utils.warn("careful")
    utils.error("boom")
    utils.panel("body", title="T", color="blue", subtitle="sub")
    utils.bullet_list(["a", "b"], marker="•", style="red")
    utils.numbered_list(["one", "two"])
    utils.key_terms_table({"k": "v"})
    utils.key_terms_table({})  # empty short-circuits
    out = capsys.readouterr().out
    assert "Section" in out
    assert "info" in out


def test_render_code_with_and_without_extras(capsys):
    plain = CodeExample(title="plain", code="print(1)")
    rich = CodeExample(
        title="rich",
        code="x = 1\nprint(x)",
        explanation="demo",
        output="1",
        line_notes={1: "assign", 2: "print"},
    )
    utils.render_code(plain)
    utils.render_code(rich)
    utils.render_python("a = 1", title="sol")
    utils.render_markdown("# Title\n\n```python\nprint(1)\n```", title="AI")
    out = capsys.readouterr().out
    assert "plain" in out and "rich" in out


# --------------------------------------------------------------------------- #
# Input wrappers
# --------------------------------------------------------------------------- #
def test_ask_confirm_int_wrappers(monkeypatch):
    monkeypatch.setattr(utils.Prompt, "ask", _answers(["hello"]))
    assert utils.ask("q") == "hello"
    monkeypatch.setattr(utils.Confirm, "ask", classmethod(lambda cls, *a, **k: True))
    assert utils.confirm("ok?") is True
    monkeypatch.setattr(utils.IntPrompt, "ask", classmethod(lambda cls, *a, **k: 7))
    assert utils.ask_int("n") == 7


def test_menu_returns_choice(monkeypatch):
    monkeypatch.setattr(utils.Prompt, "ask", _answers(["2"]))
    choice = utils.menu("Pick", ["a", "b", "c"])
    assert choice == 2


def test_pause_handles_normal_and_eof(monkeypatch):
    monkeypatch.setattr(utils.console, "input", lambda *a, **k: "")
    utils.pause()  # normal
    def boom(*a, **k):
        raise EOFError
    monkeypatch.setattr(utils.console, "input", boom)
    utils.pause()  # must not raise


# --------------------------------------------------------------------------- #
# Walkthrough navigation
# --------------------------------------------------------------------------- #
CODE = "x = 1\n\nprint(x)\ny = 2"
NOTES = {1: "assign 1 to x"}


def test_walkthrough_empty_returns_immediately(monkeypatch):
    monkeypatch.setattr(utils, "clear", lambda *a, **k: None)
    utils.walkthrough("", {})  # no lines -> early return


def test_walkthrough_step_to_end(monkeypatch):
    monkeypatch.setattr(utils, "clear", lambda *a, **k: None)
    monkeypatch.setattr(utils, "pause", lambda *a, **k: None)
    # Enter advances; reaching the last line triggers the end branch.
    monkeypatch.setattr(utils.Prompt, "ask", _answers(["n", "n", "n", "n"]))
    utils.walkthrough(CODE, NOTES, title="t")


def test_walkthrough_navigation_branches(monkeypatch):
    monkeypatch.setattr(utils, "clear", lambda *a, **k: None)
    monkeypatch.setattr(utils, "pause", lambda *a, **k: None)
    # back (clamped at 0), invalid jump, valid jump, unknown->advance, quit
    monkeypatch.setattr(utils.Prompt, "ask", _answers(["b", "99", "3", "zzz", "q"]))
    utils.walkthrough(CODE, NOTES, title="t")


def test_walkthrough_show_all(monkeypatch):
    monkeypatch.setattr(utils, "clear", lambda *a, **k: None)
    monkeypatch.setattr(utils, "pause", lambda *a, **k: None)
    monkeypatch.setattr(utils.Prompt, "ask", _answers(["a"]))
    utils.walkthrough(CODE, NOTES, title="t")


def test_walkthrough_non_ascii_digit_does_not_crash(monkeypatch):
    # The nav prompt is free text (no Rich choices), so the user can type a
    # non-ASCII "digit" like "²" (U+00B2). str.isdigit() is True for it but
    # int() raises ValueError — which crashed the walkthrough. It must now be
    # treated like any unknown key (advance), not crash.
    monkeypatch.setattr(utils, "clear", lambda *a, **k: None)
    monkeypatch.setattr(utils, "pause", lambda *a, **k: None)
    monkeypatch.setattr(utils.Prompt, "ask", _answers(["²", "q"]))
    utils.walkthrough(CODE, NOTES, title="t")  # previously raised ValueError


def test_clear_and_hint(capsys):
    utils.clear()
    utils.hint("a tip")
    assert "a tip" in capsys.readouterr().out


def test_menu_with_descriptions_and_icons(monkeypatch):
    monkeypatch.setattr(utils.Prompt, "ask", _answers(["1"]))
    choice = utils.menu("Title", ["A", "B"], descriptions=["da", "db"], icons=["x", "y"])
    assert choice == 1


def test_ask_blank_input_returns_empty_string_not_none(monkeypatch):
    # BUG #4 repro: on blank input Rich's Prompt.ask returns the default, and a
    # default of None used to leak straight through utils.ask -> downstream
    # .strip()/grading then crashed. utils.ask must coerce None -> "".
    monkeypatch.setattr(utils.Prompt, "ask", classmethod(lambda cls, *a, **k: None))
    result = utils.ask("Your answer?")
    assert result == ""
    assert result is not None


def test_ask_with_explicit_default_is_passed_through(monkeypatch):
    # The default!=None branch: utils.ask forwards the default to Rich.
    monkeypatch.setattr(utils.Prompt, "ask", classmethod(lambda cls, *a, **k: "x"))
    assert utils.ask("q", default="d") == "x"


def test_read_multiline_reads_until_sentinel(monkeypatch):
    lines = iter(["print(1)", "print(2)", "EOF", "ignored"])
    monkeypatch.setattr(utils.console, "input", lambda *a, **k: next(lines))
    assert utils.read_multiline() == "print(1)\nprint(2)"


def test_read_multiline_stops_on_eof(monkeypatch):
    def boom(*a, **k):
        raise EOFError
    monkeypatch.setattr(utils.console, "input", boom)
    assert utils.read_multiline() == ""
