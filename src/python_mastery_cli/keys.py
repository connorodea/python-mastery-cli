"""Single-keypress reading for arrow-key menu navigation (Unix TTY, stdlib only).

``read_key()`` puts the terminal into cbreak mode, reads one keypress (decoding
arrow-key escape sequences), and restores the terminal — so menus can respond to
↑/↓ without the user pressing Enter. The pure ``decode_key`` helper does the
sequence→name mapping and is fully unit-tested; only the termios glue (which
needs a real TTY) is excluded from coverage.
"""

from __future__ import annotations

import sys

# Escape sequences for navigation keys, in both the common CSI ("\x1b[A") and
# the application-cursor ("\x1bOA") variants some terminals send.
_SEQUENCES = {
    "\x1b[A": "up", "\x1b[B": "down", "\x1b[C": "right", "\x1b[D": "left",
    "\x1bOA": "up", "\x1bOB": "down", "\x1bOC": "right", "\x1bOD": "left",
    "\x1b[H": "home", "\x1bOH": "home", "\x1b[F": "end", "\x1bOF": "end",
}


def decode_key(seq: str) -> str:
    """Map a raw key sequence to a normalised name (pure / testable)."""
    if seq in _SEQUENCES:
        return _SEQUENCES[seq]
    if seq in ("\r", "\n"):
        return "enter"
    if seq == "\x03":
        return "ctrl-c"
    if seq == "\x04":
        return "eof"
    if seq == "\x1b":
        return "esc"
    if seq == " ":
        return "space"
    return seq


def read_key() -> str:  # pragma: no cover - requires a real TTY in cbreak mode
    """Read and decode a single keypress from the terminal."""
    import select
    import termios
    import tty

    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)
        ch = sys.stdin.read(1)
        if ch == "\x1b":
            # Peek for an escape sequence; a lone Esc shouldn't block.
            ready, _, _ = select.select([sys.stdin], [], [], 0.05)
            if ready:
                ch += sys.stdin.read(2)
        return decode_key(ch)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
