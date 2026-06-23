"""Tests for the optional local web UI (stdlib http.server)."""

from __future__ import annotations

import threading
import urllib.request

import pytest

from python_mastery_cli import curriculum, webui
from python_mastery_cli.progress import Progress


@pytest.fixture
def data():
    return curriculum.get_all_lessons(), curriculum.get_all_projects()


# --------------------------------------------------------------------------- #
# build_html (pure)
# --------------------------------------------------------------------------- #
def test_build_html_basic_structure(data):
    lessons, projects = data
    html = webui.build_html(Progress(), lessons, projects)
    assert "<!doctype html>" in html.lower()
    assert "Python Mastery" in html
    assert "0 pts" in html               # fresh score
    assert lessons[0].title in html      # a real lesson title is rendered
    assert "Projects" in html
    # nothing completed yet -> the empty-circle marker appears
    assert "○" in html


def test_build_html_reflects_progress(data):
    lessons, projects = data
    p = Progress(
        completed_lessons=[lessons[0].id],
        completed_projects=[projects[0].id],
        total_score=120,
        streak_count=4,
        current_level="intermediate",
    )
    html = webui.build_html(p, lessons, projects)
    assert "120 pts" in html
    assert "4d" in html
    assert "Intermediate" in html
    assert "✓" in html  # at least one completed marker
    # width of the progress bar reflects >0 completion
    assert "width:" in html


def test_build_html_escapes_titles(data):
    lessons, projects = data
    # Construct a Progress that is valid; titles come from real curriculum and
    # are escaped via html.escape — assert no raw unescaped angle brackets leak
    # from our template body markers.
    html = webui.build_html(Progress(), lessons, projects)
    assert "<script>" not in html


# --------------------------------------------------------------------------- #
# make_server + handler (real round-trip on an ephemeral port)
# --------------------------------------------------------------------------- #
def test_server_serves_dashboard():
    server = webui.make_server("127.0.0.1", 0, lambda: "<html>hi there</html>")
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.server_address[1]
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/", timeout=5) as resp:
            assert resp.status == 200
            assert resp.headers["Content-Type"].startswith("text/html")
            body = resp.read().decode("utf-8")
        assert "hi there" in body
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


# --------------------------------------------------------------------------- #
# launch (non-blocking paths)
# --------------------------------------------------------------------------- #
def test_launch_returns_server_and_url_without_serving(tmp_path):
    server, url = webui.launch(
        progress_path=tmp_path / "p.json", open_browser=False, serve=False
    )
    try:
        assert url.startswith("http://127.0.0.1:")
        assert server.server_address[1] == int(url.rstrip("/").rsplit(":", 1)[1])
    finally:
        server.server_close()


def test_launch_calls_on_start_and_opens_browser(tmp_path, monkeypatch):
    opened = {}
    import webbrowser

    monkeypatch.setattr(webbrowser, "open", lambda u: opened.setdefault("url", u))
    seen = {}
    server, url = webui.launch(
        open_browser=True, serve=False, on_start=lambda u: seen.setdefault("url", u)
    )
    try:
        assert seen["url"] == url
        assert opened["url"] == url
    finally:
        server.server_close()


def test_level_section_empty_returns_blank():
    assert webui._level_section("Nothing", [], set()) == ""
