"""Shared terminal-UI helpers built on top of `rich`.

This module centralises every bit of presentation logic so the rest of the app
can stay focused on behaviour. If you want to re-theme the whole course, this is
the only file you need to touch.
"""

from __future__ import annotations

import sys
from typing import Iterable, Optional, Sequence

from rich.align import Align
from rich.columns import Columns
from rich.console import Console, Group, RenderableType
from rich.live import Live
from rich.markdown import Markdown
from rich.markup import escape
from rich.padding import Padding
from rich.panel import Panel
from rich.prompt import Confirm, IntPrompt, Prompt
from rich.rule import Rule
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text

from . import keys, theme as th
from .models import CodeExample, Level

# A single shared console instance, themed once, used everywhere so styling,
# width detection, and recording all behave consistently.
console = Console(theme=th.THEME)

# Per-level accent colours (hex, so they compose in styles like "bold <hex>").
LEVEL_COLORS: dict[str, str] = {
    Level.BEGINNER.value: th.LEVEL["beginner"],
    Level.INTERMEDIATE.value: th.LEVEL["intermediate"],
    Level.ADVANCED.value: th.LEVEL["advanced"],
    Level.PROJECT.value: th.LEVEL["project"],
}


def level_color(level: Level | str) -> str:
    """Return the accent colour (hex) for a level, defaulting to the cyan accent.

    A hex value is returned (rather than a theme *style name*) so callers can
    safely compose it into styles such as ``f"bold {color}"`` — Rich cannot
    compose a bare theme-style name with modifiers.
    """
    key = level.value if isinstance(level, Level) else str(level)
    return LEVEL_COLORS.get(key, th.CYAN)


def gradient_text(text: str, *, start: str = th.BRAND, end: str = th.CYAN, bold: bool = True) -> Text:
    """Build a Rich Text whose characters fade from ``start`` to ``end``."""
    stops = th.gradient_stops(start, end, max(len(text), 1))
    rich_text = Text()
    for char, color in zip(text, stops):
        style = f"bold {color}" if bold else color
        rich_text.append(char, style=style)
    return rich_text


# --------------------------------------------------------------------------- #
# Typographic primitives — the building blocks of the Apple/Vercel-style look:
# letter-spaced "eyebrow" kickers, hairline rules, and lots of breathing room.
# --------------------------------------------------------------------------- #
def letterspace(text: str, *, gap: str = " ") -> str:
    """Add light letter-spacing (e.g. ``"LEVEL"`` -> ``"L E V E L"``)."""
    return gap.join(text)


def eyebrow(text: str, *, align: str = "left") -> None:
    """Print a small, uppercase, letter-spaced muted kicker label (Apple-style)."""
    label = Text(letterspace(text.upper()), style="muted")
    console.print(Align(label, align=align) if align != "left" else label)


def hairline(*, style: str = "faint") -> None:
    """Print a thin, quiet full-width divider."""
    console.print(Rule(style=style))


def blank(lines: int = 1) -> None:
    """Vertical breathing room."""
    for _ in range(lines):
        console.print()


def clear() -> None:
    """Clear the terminal (no-op-safe if the terminal can't be cleared)."""
    console.clear()


def banner(*, subtitle: Optional[str] = None) -> None:
    """Render a calm, boxless hero — gradient wordmark with generous whitespace.

    Boxless and centered (Apple/Vercel ethos): the negative space does the work,
    a single hairline grounds it, and the only colour is the gradient mark.
    """
    blank()
    console.print(Align.center(Text(letterspace("INTERACTIVE PYTHON COURSE"), style="muted")))
    blank()
    mark = Text(justify="center")
    mark.append(f"{th.ICONS['snake']}  ")
    mark.append_text(gradient_text("PYTHON MASTERY", start=th.MINT, end=th.CYAN))
    console.print(Align.center(mark))
    blank()
    console.print(
        Align.center(
            Text(
                subtitle or "Learn Python beautifully — from your first print() to production.",
                style="subtitle",
            )
        )
    )
    blank()
    meta = Text(justify="center")
    meta.append("63 lessons", style="muted")
    meta.append("   ·   ", style="faint")
    meta.append("12 projects", style="muted")
    meta.append("   ·   ", style="faint")
    meta.append("AI tutor", style="muted")
    console.print(Align.center(meta))
    blank()
    hairline()


def heading(text: str, *, color: str = th.BRAND, kicker: Optional[str] = None) -> None:
    """Print a section heading: optional eyebrow kicker, bold title, hairline.

    ``kicker`` renders a small letter-spaced label above the title (Apple-style).
    """
    console.print()
    if kicker:
        eyebrow(kicker)
    console.print(Text(text, style=f"bold {color}"))
    hairline()


def hint(text: str) -> None:
    """Print a subtle, dimmed footer hint (keyboard tips, etc.)."""
    console.print(f"[faint]{text}[/faint]")


def info(message: str) -> None:
    console.print(f"[info]{th.ICONS['dot']}[/info] {message}")


def success(message: str) -> None:
    console.print(f"[success]{th.ICONS['check']}[/success] {message}")


def warn(message: str) -> None:
    console.print(f"[warning]![/warning] {message}")


def error(message: str) -> None:
    console.print(f"[danger]{th.ICONS['cross']}[/danger] {message}")


def panel(
    body: RenderableType,
    *,
    title: Optional[str] = None,
    color: str = "brand.deep",
    subtitle: Optional[str] = None,
) -> None:
    """Print arbitrary content inside a titled, coloured panel."""
    console.print(
        Panel(
            body,
            title=f"[bold]{title}[/bold]" if title else None,
            subtitle=subtitle,
            border_style=color,
            box=th.PANEL_BOX,
            padding=(1, 2),
        )
    )


def stat_strip(stats: Sequence[tuple[str, str]], *, accent: str = th.BRAND) -> None:
    """Render a boxless row of stats: bold value over a letter-spaced label.

    ``stats`` is a sequence of ``(label, value)``. This is the minimal,
    premium dashboard look (Apple/Vercel) — no borders, just type and space.
    """
    cells = []
    for label, value in stats:
        cells.append(
            Group(
                Text(str(value), style="card.value"),
                Text(letterspace(label.upper()), style="card.label"),
            )
        )
    console.print(Padding(Columns(cells, equal=True, expand=True), (0, 1)))


def progress_bar(done: int, total: int, *, width: int = 28) -> Text:
    """A gradient block progress bar as Rich Text: ``████░░░░  60% (6/10)``.

    Each filled block is tinted along a mint→cyan gradient (matching the
    wordmark), so the bar reads as a smooth sweep rather than a flat block.
    """
    total_safe = max(total, 1)
    ratio = min(max(done / total_safe, 0.0), 1.0)
    filled = int(round(ratio * width))
    stops = th.gradient_stops(th.BRAND, th.CYAN, max(filled, 1))
    bar = Text()
    for index in range(filled):
        bar.append("█", style=stops[index])
    bar.append("░" * (width - filled), style="faint")
    bar.append(f"  {ratio * 100:4.0f}%  ", style="card.value")
    bar.append(f"({done}/{total})", style="muted")
    return bar


def render_code(example: CodeExample, *, color: str = "blue") -> None:
    """Render a syntax-highlighted code example plus optional expected output."""
    syntax = Syntax(
        example.code,
        "python",
        theme="monokai",
        line_numbers=True,
        word_wrap=True,
    )
    pieces: list[RenderableType] = [syntax]
    if example.output:
        pieces.append(Text("\nOutput:", style="bold dim"))
        pieces.append(Text(example.output, style="green"))
    body = Group(*pieces)
    subtitle_parts = []
    if example.explanation:
        subtitle_parts.append(example.explanation)
    if example.has_walkthrough:
        subtitle_parts.append("line-by-line walkthrough available")
    subtitle = f"[dim]{' • '.join(subtitle_parts)}[/dim]" if subtitle_parts else None
    panel(body, title=example.title, color=color, subtitle=subtitle)


def render_python(code: str, *, title: Optional[str] = None, color: str = "yellow") -> None:
    """Render a raw Python string as a highlighted panel (used for solutions)."""
    syntax = Syntax(code.strip("\n"), "python", theme="monokai", line_numbers=True, word_wrap=True)
    panel(syntax, title=title, color=color)


def render_markdown(text: str, *, title: Optional[str] = None, color: str = "blue") -> None:
    """Render Markdown (with fenced code blocks) inside a panel — used for AI answers."""
    panel(Markdown(text, code_theme="monokai"), title=title, color=color)


def walkthrough(
    code: str,
    line_notes: Optional[dict[int, str]] = None,
    *,
    title: str = "Line-by-line walkthrough",
    color: str = "blue",
) -> None:
    """Step through code one line at a time, explaining each line on demand.

    Navigation while stepping:

    * Enter / ``n`` — next line
    * ``b``         — previous line
    * a number      — jump to that line
    * ``a``         — show all notes at once, then exit
    * ``q``         — quit the walkthrough

    Works on any snippet: authored ``line_notes`` are shown when present, and
    blank/uncommented lines get a sensible default so the learner is never stuck.
    """
    line_notes = line_notes or {}
    lines = code.strip("\n").splitlines()
    total = len(lines)
    if total == 0:
        return

    idx = 0
    while True:
        clear()
        heading(title, color=color)
        syntax = Syntax(
            "\n".join(lines),
            "python",
            theme="monokai",
            line_numbers=True,
            word_wrap=True,
            highlight_lines={idx + 1},
        )
        panel(syntax, title=f"Line {idx + 1} of {total}", color=color)

        current = lines[idx]
        shown = escape(current) if current.strip() else "(blank line)"
        console.print(f"[bold {color}]→ Line {idx + 1}:[/bold {color}] [white]{shown}[/white]")
        note = line_notes.get(idx + 1)
        if note:
            console.print(f"   {note}")
        elif not current.strip():
            console.print("   [dim]A blank line — used to group related code and improve readability.[/dim]")
        else:
            console.print(
                "   [dim]No extra note here — read this line together with the ones around it.[/dim]"
            )

        nav = Prompt.ask(
            "[dim][Enter]=next  b=back  #=jump  a=all  q=quit[/dim]",
            default="n",
            show_default=False,
        ).strip().lower()

        if nav in ("q", "quit"):
            return
        if nav in ("b", "back"):
            idx = max(0, idx - 1)
            continue
        if nav in ("a", "all"):
            _show_all_notes(lines, line_notes, color=color)
            return
        if nav.isdigit():
            jump = int(nav) - 1
            if 0 <= jump < total:
                idx = jump
            continue
        # default: advance
        if idx + 1 >= total:
            success("End of walkthrough — you've reviewed every line.")
            pause()
            return
        idx += 1


def _show_all_notes(lines: list[str], line_notes: dict[int, str], *, color: str = th.BRAND) -> None:
    """Render the whole snippet with every annotated line listed beneath it."""
    table = Table(show_header=True, header_style=f"bold {color}", expand=True, border_style="dim")
    table.add_column("#", justify="right", style="dim", no_wrap=True)
    table.add_column("Code", style="white", no_wrap=False)
    table.add_column("Explanation")
    for i, line in enumerate(lines, start=1):
        note = line_notes.get(i, "")
        table.add_row(str(i), escape(line) if line.strip() else "[dim](blank)[/dim]", note or "[dim]—[/dim]")
    console.print(table)
    pause()


def bullet_list(items: Iterable[str], *, marker: str = "•", style: str = "") -> None:
    """Print a simple bullet list."""
    for item in items:
        prefix = f"[{style}]{marker}[/{style}]" if style else marker
        console.print(f"  {prefix} {item}")


def numbered_list(items: Sequence[str], *, style: str = "bold cyan") -> None:
    """Print a numbered list (1-indexed)."""
    for i, item in enumerate(items, start=1):
        console.print(f"  [{style}]{i:>2}.[/{style}] {item}")


def key_terms_table(terms: dict[str, str], *, color: str = th.BRAND) -> None:
    """Render a glossary of key terms as a two-column table."""
    if not terms:
        return
    table = Table(show_header=True, header_style=f"bold {color}", border_style="dim", expand=True)
    table.add_column("Term", style="bold", no_wrap=True)
    table.add_column("Meaning")
    for term, meaning in terms.items():
        table.add_row(term, meaning)
    console.print(table)


# --------------------------------------------------------------------------- #
# Input helpers (thin wrappers over rich.prompt so behaviour is consistent)
# --------------------------------------------------------------------------- #
def ask(prompt: str, *, default: Optional[str] = None, choices: Optional[list[str]] = None) -> str:
    # Rich treats an explicit default=None as a real default and returns it on
    # blank input. Omit it when None (so Rich re-prompts on an invalid choice and
    # returns "" for free text), and coerce any None result to "" so callers can
    # safely .strip()/grade the answer without an AttributeError.
    if default is None:
        result = Prompt.ask(prompt, choices=choices)
    else:
        result = Prompt.ask(prompt, default=default, choices=choices)
    return result if result is not None else ""


def ask_int(prompt: str, *, default: Optional[int] = None) -> int:
    return IntPrompt.ask(prompt, default=default)


def confirm(prompt: str, *, default: bool = False) -> bool:
    return Confirm.ask(prompt, default=default)


def pause(message: str = "Press Enter to continue") -> None:
    """Block until the user presses Enter (gracefully handles non-interactive)."""
    try:
        console.input(f"\n[dim]{message}…[/dim] ")
    except (EOFError, KeyboardInterrupt):
        console.print()


def _is_interactive() -> bool:
    """True when both stdin and stdout are real terminals (arrow keys usable)."""
    try:
        return sys.stdin.isatty() and sys.stdout.isatty()
    except (ValueError, OSError):  # pragma: no cover - closed/odd streams
        return False


def _resolve_nav(index: int, key: str, count: int) -> tuple[str, int]:
    """Pure keyboard-navigation logic → ``(action, new_index)``.

    Actions: ``move`` (highlight shifted), ``select``, ``interrupt`` (Ctrl-C),
    ``eof`` (Ctrl-D), or ``noop``. By convention the last option is Back/Exit, so
    ``q``/``Esc`` selects it.
    """
    if key in ("up", "k"):
        return "move", (index - 1) % count
    if key in ("down", "j"):
        return "move", (index + 1) % count
    if key in ("enter", "space"):
        return "select", index
    if key in ("q", "esc"):
        return "select", count - 1
    if key == "ctrl-c":
        return "interrupt", index
    if key == "eof":
        return "eof", index
    if key.isdigit() and key != "0":
        choice = int(key)
        if 1 <= choice <= count:
            return "select", choice - 1
    return "noop", index


def _render_menu(
    title: str,
    options: Sequence[str],
    descriptions: Optional[Sequence[Optional[str]]],
    icons: Optional[Sequence[str]],
    selected: int,
) -> Group:
    """Build the menu renderable with row ``selected`` highlighted (cursor)."""
    grid = Table.grid(padding=(0, 2))
    grid.add_column(width=2, justify="right", no_wrap=True)
    grid.add_column(width=2, justify="center", no_wrap=True)
    grid.add_column()
    for i, option in enumerate(options):
        chosen = i == selected
        key_txt = Text("▸" if chosen else str(i + 1), style="brand" if chosen else "menu.key")
        glyph = icons[i] if icons and i < len(icons) else th.ICONS["dot"]
        icon = Text(glyph, style="brand")
        desc = descriptions[i] if descriptions and i < len(descriptions) else None
        label = Text(option, style="brand" if chosen else "menu.label")
        cell: RenderableType = Group(label, Text(desc, style="menu.desc")) if desc else label
        grid.add_row(key_txt, icon, cell)
        grid.add_row("", "", "")
    return Group(
        Text(""),
        Text(letterspace(title.upper()), style="muted"),
        Text(""),
        Padding(grid, (0, 1)),
        Text("↑/↓ or j/k move · Enter select · digit jump · q back", style="faint"),
    )


def _select_interactive(
    title: str,
    options: Sequence[str],
    *,
    descriptions: Optional[Sequence[Optional[str]]] = None,
    icons: Optional[Sequence[str]] = None,
    read=None,
) -> int:
    """Arrow-key menu: returns the 1-indexed choice. ``read`` is injectable for tests."""
    reader = read or keys.read_key
    index = 0
    with Live(
        _render_menu(title, options, descriptions, icons, index),
        console=console,
        auto_refresh=False,
        transient=True,
    ) as live:
        while True:
            action, index = _resolve_nav(index, reader(), len(options))
            if action == "select":
                return index + 1
            if action == "interrupt":
                raise KeyboardInterrupt
            if action == "eof":
                raise EOFError
            live.update(_render_menu(title, options, descriptions, icons, index), refresh=True)


def menu(
    title: str,
    options: Sequence[str],
    *,
    color: str = "brand.deep",
    descriptions: Optional[Sequence[Optional[str]]] = None,
    icons: Optional[Sequence[str]] = None,
) -> int:
    """Render a menu and return the 1-indexed choice the user picked.

    In a real terminal this is keyboard-driven: ↑/↓ (or j/k) move a highlighted
    cursor, Enter selects, a digit jumps, and q/Esc picks the last option
    (Back/Exit). When stdin/stdout aren't a TTY (scripts, pipes, tests) it falls
    back to a numbered prompt. ``descriptions``/``icons`` enrich each row.
    """
    if _is_interactive():  # pragma: no cover - arrow-key path requires a real TTY
        return _select_interactive(title, options, descriptions=descriptions, icons=icons)

    grid = Table.grid(padding=(0, 2))
    grid.add_column(justify="right", no_wrap=True, width=2)  # number
    grid.add_column(justify="center", no_wrap=True, width=2)  # icon
    grid.add_column()                                         # label (+ optional desc)
    for i, option in enumerate(options, start=1):
        key = Text(f"{i}", style="menu.key")
        glyph = icons[i - 1] if icons and i - 1 < len(icons) else th.ICONS["dot"]
        icon = Text(glyph, style="brand")
        desc = descriptions[i - 1] if descriptions and i - 1 < len(descriptions) else None
        if desc:
            cell: RenderableType = Group(
                Text(option, style="menu.label"),
                Text(desc, style="menu.desc"),
            )
        else:
            cell = Text(option, style="menu.label")
        grid.add_row(key, icon, cell)
        grid.add_row("", "", "")  # breathing room between options

    console.print()
    eyebrow(title)
    console.print()
    console.print(Padding(grid, (0, 1)))
    hairline()
    valid = [str(i) for i in range(1, len(options) + 1)]
    raw = Prompt.ask(f"[brand]{th.ICONS['arrow']}[/brand] Select", choices=valid, show_choices=False)
    return int(raw)


def progress_bar_text(done: int, total: int, *, width: int = 30) -> str:
    """Build a textual progress bar like ``[#####-----] 50% (5/10)``."""
    total = max(total, 1)
    ratio = min(max(done / total, 0.0), 1.0)
    filled = int(round(ratio * width))
    bar = "#" * filled + "-" * (width - filled)
    return f"[{bar}] {ratio * 100:5.1f}% ({done}/{total})"
