"""Central visual theme for the whole CLI.

Inspired by the clean, modern aesthetics of tools like Modal, Railway, Charm's
gum/glow, and the Vercel/Stripe CLIs: a single signature accent (mint green),
generous spacing, rounded borders, soft "cool grey" muted text, and gradient
titles. Everything visual is defined here so the look can be retuned in one place.
"""

from __future__ import annotations

import os

from rich import box
from rich.theme import Theme

# --------------------------------------------------------------------------- #
# Palette (truecolor; Rich downgrades gracefully on limited terminals)
# --------------------------------------------------------------------------- #
BRAND = "#5EE6A8"        # signature mint green (Modal-ish)
BRAND_DEEP = "#34C98C"   # deeper green for gradients/edges
MINT = "#9CF6CE"         # light mint highlight
CYAN = "#67D9E8"         # secondary accent
VIOLET = "#B49CFF"       # tertiary accent
GOLD = "#F4C75B"         # projects / highlights
CORAL = "#FF8E7B"        # errors / danger
TEXT = "#E8EAED"         # near-white body text
MUTED = "#8A909C"        # cool grey for secondary text
FAINT = "#5B616E"        # very dim, for hairlines/placeholders
SELECTED_BG = "#1b222b"  # subtle highlight behind the focused menu row

# Per-level accents (used for lessons, panels, progress).
LEVEL = {
    "beginner": BRAND,
    "intermediate": CYAN,
    "advanced": VIOLET,
    "project": GOLD,
}

# Box style used consistently across panels/tables for a soft, modern feel.
PANEL_BOX = box.ROUNDED

# Iconography (single-width glyphs / emoji used sparingly).
ICONS = {
    "snake": "🐍",
    "spark": "✦",
    "diamond": "◆",
    "dot": "•",
    "play": "▶",
    "book": "❯",
    "quiz": "?",
    "drill": "⌨",
    "project": "★",
    "robot": "✧",
    "chart": "▤",
    "reset": "↺",
    "exit": "⏻",
    "check": "✓",
    "cross": "✗",
    "flame": "🔥",
    "arrow": "→",
    "trophy": "🏆",
    "cursor": "▸",
    "todo": "○",
    "bar_full": "█",
    "bar_empty": "░",
}

# Plain ASCII fallbacks for every icon, used in accessible "plain" mode (no
# color + no emoji/box-drawing) — friendlier to screen readers, braille
# displays, and degraded/remote terminals.
ASCII_ICONS = {
    "snake": "", "spark": "*", "diamond": "*", "dot": "-", "play": ">",
    "book": ">", "quiz": "?", "drill": "#", "project": "*", "robot": "AI",
    "chart": "#", "reset": "~", "exit": "x", "check": "v", "cross": "x",
    "flame": "", "arrow": "->", "trophy": "*", "cursor": ">", "todo": "o",
    "bar_full": "#", "bar_empty": "-",
}

# Plain mode is toggled either by env var (set before launch) or the --plain
# flag (which calls set_plain at runtime). NO_COLOR is handled separately by
# Rich itself (color off); plain mode additionally swaps to ASCII glyphs.
_PLAIN = False


def set_plain(value: bool = True) -> None:
    """Enable/disable plain (ASCII, no-color) mode for the rest of the session."""
    global _PLAIN
    _PLAIN = value


def plain_mode() -> bool:
    """True when ASCII glyphs should be used (``--plain`` or PYTHON_MASTERY_PLAIN)."""
    return _PLAIN or bool(os.environ.get("PYTHON_MASTERY_PLAIN"))


def no_color_mode() -> bool:
    """True when colour should be off — plain mode or the NO_COLOR standard."""
    return plain_mode() or "NO_COLOR" in os.environ


def glyph(name: str) -> str:
    """Return an icon, ASCII-fied when in plain mode."""
    if plain_mode():
        return ASCII_ICONS.get(name, "")
    return ICONS.get(name, "")

# Named styles. Use these via markup (e.g. "[brand]hi[/brand]") or as styles.
THEME = Theme(
    {
        "brand": f"bold {BRAND}",
        "brand.deep": BRAND_DEEP,
        "mint": MINT,
        "title": f"bold {BRAND}",
        "subtitle": f"italic {MUTED}",
        "muted": MUTED,
        "faint": FAINT,
        "info": CYAN,
        "success": f"bold {BRAND}",
        "warning": f"bold {GOLD}",
        "danger": f"bold {CORAL}",
        "menu.key": f"bold {BRAND}",
        "menu.label": f"bold {TEXT}",
        "menu.desc": MUTED,
        "card.label": MUTED,
        "card.value": f"bold {TEXT}",
        "rule": BRAND_DEEP,
        # Level styles so "[beginner]…[/]" and border_style="beginner" both work.
        "beginner": LEVEL["beginner"],
        "intermediate": LEVEL["intermediate"],
        "advanced": LEVEL["advanced"],
        "project": LEVEL["project"],
        "prompt.choices": MUTED,
        "prompt.default": CYAN,
    }
)


def _hex_to_rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def gradient_stops(start: str, end: str, n: int) -> list[str]:
    """Return ``n`` hex colors linearly interpolated from ``start`` to ``end``."""
    if n <= 1:
        return [start]
    sr, sg, sb = _hex_to_rgb(start)
    er, eg, eb = _hex_to_rgb(end)
    stops = []
    for i in range(n):
        t = i / (n - 1)
        r = round(sr + (er - sr) * t)
        g = round(sg + (eg - sg) * t)
        b = round(sb + (eb - sb) * t)
        stops.append(f"#{r:02x}{g:02x}{b:02x}")
    return stops
