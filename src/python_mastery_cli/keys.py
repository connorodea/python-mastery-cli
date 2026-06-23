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
    "\x1b[Z": "shift-tab",  # back-tab (move to previous)
}


def decode_key(seq: str) -> str:
    """Map a raw key sequence to a normalised name (pure / testable)."""
    if seq in _SEQUENCES:
        return _SEQUENCES[seq]
    if seq in ("\r", "\n"):
        return "enter"
    if seq == "\t":
        return "tab"
    if seq == "\x03":
        return "ctrl-c"
    if seq == "\x04":
        return "eof"
    if seq == "\x1b":
        return "esc"
    if seq == " ":
        return "space"
    return seq


def _read_sequence(read_bytes, more_pending) -> str:
    """Assemble and decode one keypress (pure / testable).

    ``read_bytes(n)`` returns up to ``n`` decoded chars; ``more_pending()``
    reports whether more bytes are immediately available. This is where the
    arrow-key bug lived: an escape sequence (``\\x1b[A``) must only pull its
    follow-up bytes when they are actually pending, and the *read* and the
    *pending check* must look at the same source (see ``read_key``).
    """
    ch = read_bytes(1)
    if ch == "\x1b" and more_pending():
        ch += read_bytes(2)
    return decode_key(ch)


def read_key() -> str:  # pragma: no cover - thin raw-TTY I/O glue (see _read_sequence)
    """Read and decode a single keypress from the terminal.

    Reads raw bytes via ``os.read`` on the file descriptor — NOT ``sys.stdin``.
    A buffered text read would pull a whole escape sequence into Python's
    internal buffer, so the follow-up ``select`` on the fd would see nothing
    pending and an arrow key would look like a lone Esc (and the buffered read
    could also block). ``os.read`` + ``select`` on the same fd agree, so arrow
    keys decode correctly.
    """
    import os
    import select
    import termios
    import tty

    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)
        return _read_sequence(
            lambda n: os.read(fd, n).decode("utf-8", "ignore"),
            lambda: bool(select.select([fd], [], [], 0.05)[0]),
        )
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
