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
<title>Python Mastery</title>
<style>
  :root { --bg:$bg; --surface:$surface; --border:$border; --mint:$mint;
          --cyan:$cyan; --violet:$violet; --gold:$gold; --text:$text; --muted:$muted; }
  * { box-sizing: border-box; }
  body { margin:0; background:var(--bg); color:var(--text);
         font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
         line-height:1.5; }
  .wrap { max-width:920px; margin:0 auto; padding:56px 24px 80px; }
  .eyebrow { letter-spacing:.32em; text-transform:uppercase; font-size:12px; color:var(--muted); }
  h1 { font-size:40px; margin:.2em 0 .1em; font-weight:800;
       background:linear-gradient(90deg,var(--mint),var(--cyan));
       -webkit-background-clip:text; background-clip:text; color:transparent; }
  .tagline { color:var(--muted); margin:0 0 36px; }
  .stats { display:grid; grid-template-columns:repeat(auto-fit,minmax(120px,1fr)); gap:14px; margin-bottom:28px; }
  .stat { background:var(--surface); border:1px solid var(--border); border-radius:14px; padding:16px 18px; }
  .stat .val { font-size:24px; font-weight:700; }
  .stat .lbl { letter-spacing:.18em; text-transform:uppercase; font-size:11px; color:var(--muted); margin-top:4px; }
  .bar { height:10px; border-radius:999px; background:var(--border); overflow:hidden; margin:8px 0 36px; }
  .bar > span { display:block; height:100%; background:linear-gradient(90deg,var(--mint),var(--cyan)); }
  h2 { font-size:13px; letter-spacing:.2em; text-transform:uppercase; color:var(--muted);
       margin:34px 0 12px; font-weight:600; }
  ul { list-style:none; margin:0; padding:0; }
  li { display:flex; align-items:center; gap:12px; padding:9px 14px; border:1px solid var(--border);
       border-radius:10px; margin-bottom:8px; background:var(--surface); }
  .mark { width:20px; text-align:center; }
  .done .mark { color:var(--mint); }
  .todo .mark { color:var(--muted); }
  .done .title { color:var(--text); }
  .todo .title { color:var(--muted); }
  .meta { margin-left:auto; color:var(--muted); font-size:13px; }
  .note { color:var(--muted); font-size:13px; margin-top:40px; border-top:1px solid var(--border); padding-top:18px; }
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


def _level_section(title: str, lessons: list[Lesson], completed: set[str]) -> str:
    if not lessons:
        return ""
    rows = []
    for lesson in lessons:
        done = lesson.id in completed
        cls = "done" if done else "todo"
        mark = "✓" if done else "○"
        rows.append(
            f'<li class="{cls}"><span class="mark">{mark}</span>'
            f'<span class="title">{escape(lesson.title)}</span>'
            f'<span class="meta">~{lesson.estimated_minutes} min</span></li>'
        )
    return f"<h2>{escape(title)}</h2><ul>{''.join(rows)}</ul>"


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

    project_rows = []
    for project in projects:
        is_done = project.id in completed_projects
        cls = "done" if is_done else "todo"
        mark = "✓" if is_done else "○"
        project_rows.append(
            f'<li class="{cls}"><span class="mark">{mark}</span>'
            f'<span class="title">{escape(project.title)}</span>'
            f'<span class="meta">{escape(project.difficulty)}</span></li>'
        )
    projects_html = f"<h2>Projects</h2><ul>{''.join(project_rows)}</ul>"

    body = (
        '<div class="eyebrow">Interactive Python Course</div>'
        "<h1>🐍 Python Mastery</h1>"
        '<p class="tagline">Your live progress. Study in the terminal — '
        "this is the calm, at-a-glance view.</p>"
        f'<div class="stats">{stat_html}</div>'
        f'<div class="bar"><span style="width:{pct:.0f}%"></span></div>'
        f"{sections}{projects_html}"
        '<p class="note">Read-only dashboard. Run <code>python-mastery</code> in your '
        "terminal to study, take quizzes, and complete drills — this page reflects "
        "your saved progress on each refresh.</p>"
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
    provider = lambda: build_html(prog.load_progress(progress_path), lessons, projects)

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
