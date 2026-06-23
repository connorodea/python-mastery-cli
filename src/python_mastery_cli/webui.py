"""Optional local web UI — a minimal dashboard you can "spin up" on demand.

The terminal CLI is the default, interactive experience. ``python-mastery ui``
starts a tiny standard-library HTTP server on localhost and opens a clean,
read-only progress dashboard in the browser (stats, lessons by level, projects).
No extra dependencies — just ``http.server`` + ``webbrowser``.

The split is deliberate: study and answer quizzes in the CLI; glance at the web
view when you want a calm, at-a-glance picture of where you are.
"""

from __future__ import annotations

import http.server
import math
from html import escape
from string import Template
from typing import Callable, Optional

from . import curriculum, progress as prog, theme as th
from .models import Lesson, Project
from .progress import Progress

# A dark, minimal palette that mirrors the CLI's mint accent.
_BG = "#0d0f12"
_SURFACE = "#15181d"
_BORDER = "#262b33"

_PAGE = Template(
    """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="refresh" content="30">
<title>Python Mastery</title>
<style>
  :root { --bg:$bg; --surface:$surface; --border:$border; --mint:$mint;
          --cyan:$cyan; --violet:$violet; --gold:$gold; --text:$text; --muted:$muted; }
  * { box-sizing: border-box; }
  html { scroll-behavior:smooth; }
  body { margin:0; background:var(--bg); color:var(--text);
         font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
         line-height:1.55; -webkit-font-smoothing:antialiased;
         background-image:radial-gradient(900px 380px at 50% -120px, rgba(94,230,168,.10), transparent 70%); }
  .wrap { max-width:960px; margin:0 auto; padding:64px 24px 96px;
          animation:fadeup .5s ease both; }
  @keyframes fadeup { from { opacity:0; transform:translateY(10px); } to { opacity:1; transform:none; } }
  .eyebrow { letter-spacing:.34em; text-transform:uppercase; font-size:12px; color:var(--muted); }
  h1 { font-size:46px; margin:.18em 0 .08em; font-weight:800; letter-spacing:-.5px;
       background:linear-gradient(95deg,var(--mint),var(--cyan));
       -webkit-background-clip:text; background-clip:text; color:transparent; }
  .tagline { color:var(--muted); margin:0 0 36px; font-size:15px; }

  /* Hero: progress ring + stat cards */
  .hero { display:flex; gap:28px; align-items:center; flex-wrap:wrap;
          background:linear-gradient(180deg,rgba(255,255,255,.02),transparent);
          border:1px solid var(--border); border-radius:20px; padding:26px 28px; margin-bottom:40px; }
  .ring { flex:0 0 auto; filter:drop-shadow(0 0 14px rgba(94,230,168,.18)); }
  .ring .track { stroke:var(--border); stroke-width:11; fill:none; }
  .ring .fill { stroke-width:11; fill:none; stroke-linecap:round;
                transition:stroke-dashoffset 1s cubic-bezier(.4,0,.2,1); }
  .ring-pct { fill:var(--text); font-size:26px; font-weight:800; text-anchor:middle; }
  .ring-sub { fill:var(--muted); font-size:9px; letter-spacing:.22em; text-anchor:middle;
              text-transform:uppercase; }
  .stats { flex:1 1 360px; display:grid; grid-template-columns:repeat(auto-fit,minmax(110px,1fr)); gap:12px; }
  .stat { background:var(--surface); border:1px solid var(--border); border-radius:14px; padding:14px 16px;
          transition:transform .15s ease, border-color .15s ease; }
  .stat:hover { transform:translateY(-2px); border-color:var(--mint); }
  .stat .val { font-size:22px; font-weight:700; font-variant-numeric:tabular-nums; }
  .stat .lbl { letter-spacing:.18em; text-transform:uppercase; font-size:10px; color:var(--muted); margin-top:4px; }

  /* Level sections */
  .level { margin:30px 0; }
  .lvl-head { display:flex; align-items:baseline; gap:12px; margin-bottom:8px; }
  h2 { font-size:13px; letter-spacing:.22em; text-transform:uppercase; color:var(--text);
       margin:0; font-weight:700; }
  .badge { font-size:12px; color:var(--muted); font-variant-numeric:tabular-nums; }
  .minibar { height:6px; border-radius:999px; background:var(--border); overflow:hidden; margin:0 0 14px; }
  .minibar > span { display:block; height:100%; border-radius:999px;
                    background:linear-gradient(90deg,var(--mint),var(--cyan)); transition:width 1s ease; }
  ul { list-style:none; margin:0; padding:0; display:grid; gap:8px;
       grid-template-columns:repeat(auto-fill,minmax(280px,1fr)); }
  li { display:flex; align-items:center; gap:12px; padding:11px 15px; border:1px solid var(--border);
       border-radius:12px; background:var(--surface); transition:border-color .15s ease, transform .15s ease; }
  li:hover { border-color:var(--mint); transform:translateY(-1px); }
  .mark { width:18px; text-align:center; font-size:13px; }
  .done .mark { color:var(--mint); }
  .todo .mark { color:var(--muted); }
  .todo .title { color:var(--muted); }
  .meta { margin-left:auto; color:var(--muted); font-size:12px; font-variant-numeric:tabular-nums; }
  .note { color:var(--muted); font-size:13px; margin-top:48px; border-top:1px solid var(--border); padding-top:18px; }
  code { background:var(--surface); border:1px solid var(--border); border-radius:6px; padding:1px 6px; color:var(--mint); }
  a { color:var(--cyan); }
</style>
</head>
<body>
<div class="wrap">
$body
</div>
</body>
</html>
"""
)


def _rows(items: list, completed: set[str], meta_of: Callable) -> str:
    out = []
    for item in items:
        done = item.id in completed
        cls = "done" if done else "todo"
        mark = "✓" if done else "○"
        out.append(
            f'<li class="{cls}"><span class="mark">{mark}</span>'
            f'<span class="title">{escape(item.title)}</span>'
            f'<span class="meta">{escape(meta_of(item))}</span></li>'
        )
    return "".join(out)


def _level_section(title: str, lessons: list[Lesson], completed: set[str]) -> str:
    if not lessons:
        return ""
    done = sum(1 for lesson in lessons if lesson.id in completed)
    pct = done / len(lessons) * 100
    rows = _rows(lessons, completed, lambda lesson: f"~{lesson.estimated_minutes} min")
    return (
        '<section class="level">'
        f'<div class="lvl-head"><h2>{escape(title)}</h2>'
        f'<span class="badge">{done}/{len(lessons)}</span></div>'
        f'<div class="minibar"><span style="width:{pct:.0f}%"></span></div>'
        f"<ul>{rows}</ul></section>"
    )


def _progress_ring(pct: float) -> str:
    """An SVG donut showing overall completion, filled with the mint→cyan gradient."""
    radius = 52
    circ = 2 * math.pi * radius
    offset = circ * (1 - max(0.0, min(pct, 100.0)) / 100)
    return (
        '<svg class="ring" width="132" height="132" viewBox="0 0 120 120" role="img" '
        f'aria-label="{pct:.0f}% complete">'
        f'<circle class="track" cx="60" cy="60" r="{radius}"/>'
        f'<circle class="fill" cx="60" cy="60" r="{radius}" stroke="url(#ringgrad)" '
        f'stroke-dasharray="{circ:.1f}" stroke-dashoffset="{offset:.1f}" '
        'transform="rotate(-90 60 60)"/>'
        f'<text class="ring-pct" x="60" y="58">{pct:.0f}%</text>'
        '<text class="ring-sub" x="60" y="74">complete</text>'
        '<defs><linearGradient id="ringgrad" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0%" stop-color="{th.BRAND}"/>'
        f'<stop offset="100%" stop-color="{th.CYAN}"/></linearGradient></defs></svg>'
    )


def build_html(progress: Progress, lessons: list[Lesson], projects: list[Project]) -> str:
    """Render the full dashboard page as an HTML string (pure / testable)."""
    completed = set(progress.completed_lessons)
    completed_projects = set(progress.completed_projects)
    total = len(lessons)
    done = len(completed)
    pct = prog.completion_percentage(progress, total)

    stats = [
        ("Level", escape(progress.current_level.title())),
        ("Score", f"{progress.total_score} pts"),
        ("Streak", f"{progress.streak_count}d"),
        ("Lessons", f"{done}/{total}"),
        ("Projects", f"{len(completed_projects)}/{len(projects)}"),
    ]
    stat_html = "".join(
        f'<div class="stat"><div class="val">{val}</div><div class="lbl">{lbl}</div></div>'
        for lbl, val in stats
    )

    sections = "".join(
        _level_section(
            level.title(),
            [lesson for lesson in lessons if str(lesson.level) == level],
            completed,
        )
        for level in ("beginner", "intermediate", "advanced")
    )

    project_rows = _rows(projects, completed_projects, lambda project: project.difficulty)
    projects_html = (
        '<section class="level"><div class="lvl-head"><h2>Projects</h2>'
        f'<span class="badge">{len(completed_projects)}/{len(projects)}</span></div>'
        f"<ul>{project_rows}</ul></section>"
    )

    body = (
        '<div class="eyebrow">Interactive Python Course</div>'
        "<h1>🐍 Python Mastery</h1>"
        '<p class="tagline">Your live progress, beautifully — study in the terminal, '
        "glance here.</p>"
        f'<div class="hero">{_progress_ring(pct)}<div class="stats">{stat_html}</div></div>'
        f"{sections}{projects_html}"
        '<p class="note">Read-only dashboard (auto-refreshes). Run '
        "<code>python-mastery</code> in your terminal to study, take quizzes, and "
        "complete drills — this page reflects your saved progress.</p>"
    )
    return _PAGE.substitute(
        bg=_BG, surface=_SURFACE, border=_BORDER, mint=th.BRAND, cyan=th.CYAN,
        violet=th.VIOLET, gold=th.GOLD, text=th.TEXT, muted=th.MUTED, body=body,
    )


def _make_handler(html_provider: Callable[[], str]) -> type:
    """Build a request handler that serves the current dashboard on any GET."""

    class _DashboardHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self) -> None:  # noqa: N802 (http.server API)
            payload = html_provider().encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

        def log_message(self, *args) -> None:  # silence default stderr logging
            pass

    return _DashboardHandler


def make_server(host: str, port: int, html_provider: Callable[[], str]) -> http.server.HTTPServer:
    """Create (but do not start) an HTTP server bound to ``host:port``."""
    return http.server.HTTPServer((host, port), _make_handler(html_provider))


def launch(
    progress_path=None,
    *,
    host: str = "127.0.0.1",
    port: int = 0,
    open_browser: bool = True,
    serve: bool = True,
    on_start: Optional[Callable[[str], None]] = None,
) -> tuple[http.server.HTTPServer, str]:
    """Start the web UI. Returns ``(server, url)``.

    ``port=0`` picks a free port. ``on_start(url)`` is called once the server is
    bound (before serving) so the CLI can announce the address. With
    ``serve=True`` this blocks (Ctrl-C to stop); tests pass ``serve=False`` to get
    the bound server without blocking.
    """
    lessons = curriculum.get_all_lessons()
    projects = curriculum.get_all_projects()

    def provider() -> str:
        return build_html(prog.load_progress(progress_path), lessons, projects)

    server = make_server(host, port, provider)
    actual_port = server.server_address[1]
    url = f"http://{host}:{actual_port}/"

    if on_start is not None:
        on_start(url)
    if open_browser:
        import webbrowser

        webbrowser.open(url)

    if serve:  # pragma: no cover - blocking I/O loop, not unit-testable
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            server.server_close()
    return server, url
