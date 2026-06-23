"""Tests for plain/accessible mode: NO_COLOR + --plain (no colour, ASCII glyphs)."""

from __future__ import annotations

import pytest

from python_mastery_cli import theme as th, utils


@pytest.fixture(autouse=True)
def _reset_plain():
    # Plain mode is global state — always restore it so it can't leak into other
    # tests (which assert on the fancy glyphs).
    yield
    th.set_plain(False)
    utils.console.no_color = th.no_color_mode()


# --------------------------------------------------------------------------- #
# theme: mode detection + glyphs
# --------------------------------------------------------------------------- #
def test_plain_mode_default_false(monkeypatch):
    monkeypatch.delenv("PYTHON_MASTERY_PLAIN", raising=False)
    th.set_plain(False)
    assert th.plain_mode() is False


def test_plain_mode_via_set():
    th.set_plain(True)
    assert th.plain_mode() is True


def test_plain_mode_via_env(monkeypatch):
    monkeypatch.setenv("PYTHON_MASTERY_PLAIN", "1")
    assert th.plain_mode() is True


def test_no_color_mode(monkeypatch):
    monkeypatch.delenv("NO_COLOR", raising=False)
    monkeypatch.delenv("PYTHON_MASTERY_PLAIN", raising=False)
    th.set_plain(False)
    assert th.no_color_mode() is False
    monkeypatch.setenv("NO_COLOR", "1")
    assert th.no_color_mode() is True


def test_glyph_fancy_vs_ascii():
    th.set_plain(False)
    assert th.glyph("check") == "✓"
    assert th.glyph("cursor") == "▸"
    th.set_plain(True)
    assert th.glyph("check") == "v"
    assert th.glyph("cursor") == ">"
    assert th.glyph("does-not-exist") == ""


# --------------------------------------------------------------------------- #
# utils: rendering degrades to plain
# --------------------------------------------------------------------------- #
def test_gradient_text_plain_has_no_per_char_spans():
    th.set_plain(True)
    assert utils.gradient_text("HI").spans == []      # plain: single base style
    th.set_plain(False)
    assert len(utils.gradient_text("HI").spans) == 2   # fancy: one span per char


def test_progress_bar_plain_uses_ascii():
    th.set_plain(True)
    plain = utils.progress_bar(5, 10).plain
    assert "#" in plain and "█" not in plain
    th.set_plain(False)
    assert "█" in utils.progress_bar(5, 10).plain


def test_force_plain_sets_console_no_color():
    th.set_plain(False)
    utils.console.no_color = False
    utils.force_plain()
    assert th.plain_mode() is True
    assert utils.console.no_color is True


def test_render_menu_plain_uses_ascii_cursor(capsys):
    th.set_plain(True)
    utils.console.print(utils._render_menu("Menu", ["A", "B"], None, None, selected=0))
    out = capsys.readouterr().out
    assert ">" in out and "▸" not in out


def test_banner_plain_drops_emoji(capsys):
    th.set_plain(True)
    utils.banner()
    out = capsys.readouterr().out
    assert "🐍" not in out
    assert "PYTHON MASTERY" in out
