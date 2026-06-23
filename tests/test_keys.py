"""Tests for keyboard navigation: key decoding + pure menu-nav logic + the
arrow-key select loop driven with an injected key reader (no real TTY needed)."""

from __future__ import annotations

import pytest

from python_mastery_cli import keys, utils


# --------------------------------------------------------------------------- #
# keys.decode_key
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "seq, expected",
    [
        ("\x1b[A", "up"),
        ("\x1b[B", "down"),
        ("\x1b[C", "right"),
        ("\x1b[D", "left"),
        ("\x1bOA", "up"),
        ("\x1b[H", "home"),
        ("\x1b[F", "end"),
        ("\x1bOH", "home"),
        ("\t", "tab"),
        ("\x1b[Z", "shift-tab"),
        ("\r", "enter"),
        ("\n", "enter"),
        ("\x03", "ctrl-c"),
        ("\x04", "eof"),
        ("\x1b", "esc"),
        (" ", "space"),
        ("k", "k"),
        ("7", "7"),
    ],
)
def test_decode_key(seq, expected):
    assert keys.decode_key(seq) == expected


# --------------------------------------------------------------------------- #
# utils._resolve_nav (pure)
# --------------------------------------------------------------------------- #
def test_resolve_nav_movement_wraps():
    assert utils._resolve_nav(0, "up", 3) == ("move", 2)
    assert utils._resolve_nav(0, "k", 3) == ("move", 2)
    assert utils._resolve_nav(0, "shift-tab", 3) == ("move", 2)
    assert utils._resolve_nav(2, "down", 3) == ("move", 0)
    assert utils._resolve_nav(2, "j", 3) == ("move", 0)
    assert utils._resolve_nav(2, "tab", 3) == ("move", 0)


def test_select_interactive_tab_cycles():
    # Tab forward, Shift-Tab back, then Enter.
    choice = utils._select_interactive("M", ["A", "B", "C"], read=_reader(["tab", "tab", "shift-tab", "enter"]))
    assert choice == 2  # 0 -> 1 -> 2 -> back to 1 -> select option 2


def test_resolve_nav_select_and_back():
    assert utils._resolve_nav(1, "enter", 3) == ("select", 1)
    assert utils._resolve_nav(1, "space", 3) == ("select", 1)
    assert utils._resolve_nav(1, "q", 3) == ("select", 2)   # last = Back/Exit
    assert utils._resolve_nav(1, "esc", 3) == ("select", 2)


def test_resolve_nav_digit_jumps_highlight_not_select():
    # A digit MOVES the cursor (then Enter confirms) — never selects outright,
    # so two-digit positions don't mis-fire and >9 menus stay usable.
    assert utils._resolve_nav(0, "3", 5) == ("move", 2)
    assert utils._resolve_nav(0, "9", 5) == ("noop", 0)     # out of range
    assert utils._resolve_nav(0, "0", 5) == ("noop", 0)     # 0 is not a valid 1-indexed pick


def test_resolve_nav_home_end():
    assert utils._resolve_nav(3, "home", 6) == ("move", 0)
    assert utils._resolve_nav(0, "end", 6) == ("move", 5)


def test_resolve_nav_signals_and_noop():
    assert utils._resolve_nav(1, "ctrl-c", 3) == ("interrupt", 1)
    assert utils._resolve_nav(1, "eof", 3) == ("eof", 1)
    assert utils._resolve_nav(1, "x", 3) == ("noop", 1)


# --------------------------------------------------------------------------- #
# utils._render_menu
# --------------------------------------------------------------------------- #
def test_render_menu_builds_renderable(capsys):
    group = utils._render_menu("Main", ["A", "B"], ["da", "db"], ["x", "y"], selected=1)
    utils.console.print(group)
    out = capsys.readouterr().out
    assert "A" in out and "B" in out
    assert "▸" in out  # the cursor on the selected row


# --------------------------------------------------------------------------- #
# utils._select_interactive (driven by an injected key reader)
# --------------------------------------------------------------------------- #
def _reader(seq):
    it = iter(seq)
    return lambda: next(it)


def test_select_interactive_enter_after_moves():
    choice = utils._select_interactive("M", ["A", "B", "C"], read=_reader(["down", "down", "enter"]))
    assert choice == 3


def test_select_interactive_up_wraps():
    # from index 0, 'k' wraps to last (index 2) -> enter selects option 3
    choice = utils._select_interactive("M", ["A", "B", "C"], read=_reader(["k", "enter"]))
    assert choice == 3


def test_select_interactive_digit_jump_then_enter():
    # digit moves the highlight; Enter confirms.
    choice = utils._select_interactive("M", ["A", "B", "C"], read=_reader(["2", "enter"]))
    assert choice == 2


def test_select_interactive_two_digits_no_misfire():
    # On a >9-item menu, pressing "1" then "2" must NOT select option 1; the
    # highlight ends on the last digit pressed and Enter confirms it.
    options = [chr(ord("A") + i) for i in range(12)]
    choice = utils._select_interactive("M", options, read=_reader(["1", "2", "enter"]))
    assert choice == 2  # landed on option 2 (index 1), not auto-selected on "1"


def test_select_interactive_home_end():
    choice = utils._select_interactive("M", ["A", "B", "C", "D"], read=_reader(["end", "enter"]))
    assert choice == 4
    choice = utils._select_interactive("M", ["A", "B", "C", "D"], read=_reader(["down", "home", "enter"]))
    assert choice == 1


def test_select_interactive_q_selects_last():
    choice = utils._select_interactive("M", ["A", "B", "C"], read=_reader(["q"]))
    assert choice == 3


def test_select_interactive_noop_then_select():
    # an unrecognised key is a no-op; navigation then proceeds normally
    choice = utils._select_interactive("M", ["A", "B"], read=_reader(["x", "down", "enter"]))
    assert choice == 2


def test_select_interactive_ctrl_c_raises():
    with pytest.raises(KeyboardInterrupt):
        utils._select_interactive("M", ["A", "B"], read=_reader(["ctrl-c"]))


def test_select_interactive_eof_raises():
    with pytest.raises(EOFError):
        utils._select_interactive("M", ["A", "B"], read=_reader(["eof"]))


def test_is_interactive_is_false_under_pytest():
    # pytest captures stdio, so these are not real TTYs.
    assert utils._is_interactive() is False
