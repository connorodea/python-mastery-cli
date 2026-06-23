"""Opt-in execution of short Python snippets for coding drills.

This is the feedback loop the drills otherwise lack: the learner runs *their own*
code and sees a real pass/fail against the expected output, instead of just
self-reporting "done". Execution is always user-initiated.

Safety model: code runs in a **separate Python subprocess** (never ``exec``'d in
this process) with a wall-clock **timeout**, and stdout/stderr are captured. A
subprocess + timeout is the pragmatic, dependency-free isolation for a local,
single-user learning tool — it bounds runaway loops and keeps a crash or bad
import from taking down the CLI. It is not a security sandbox; it runs real
Python the learner pasted on their own machine.
"""

from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass

DEFAULT_TIMEOUT = 10.0


@dataclass
class RunResult:
    """Outcome of running a snippet."""

    stdout: str
    stderr: str
    returncode: int
    timed_out: bool = False

    @property
    def ok(self) -> bool:
        return self.returncode == 0 and not self.timed_out


def run_code(code: str, *, timeout: float = DEFAULT_TIMEOUT) -> RunResult:
    """Run ``code`` in a fresh Python subprocess and capture its output."""
    try:
        proc = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return RunResult(proc.stdout, proc.stderr, proc.returncode)
    except subprocess.TimeoutExpired as exc:
        return RunResult(exc.stdout or "", exc.stderr or "", returncode=-1, timed_out=True)


def _normalize(text: str) -> str:
    """Trim trailing whitespace per line and surrounding blank lines."""
    return "\n".join(line.rstrip() for line in text.strip("\n").splitlines()).strip()


def output_matches(actual: str, expected: str) -> bool:
    """Compare program output to an expected string, ignoring trivial whitespace."""
    return _normalize(actual) == _normalize(expected)
