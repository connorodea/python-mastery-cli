"""Tests for the Typer CLI in main.py, using CliRunner with the app/tutor mocked."""

from __future__ import annotations

import types

import pytest
from typer.testing import CliRunner

from python_mastery_cli import ai_tutor, main

runner = CliRunner()

CALLS: list[str] = []


class FakeApp:
    """Stand-in for PythonMasteryApp that records which screen was opened."""

    def __init__(self, progress_path=None):
        CALLS.append("init")

    def run(self):
        CALLS.append("run")

    def show_dashboard(self):
        CALLS.append("dashboard")

    def browse_lessons(self):
        CALLS.append("browse")

    def quiz_menu(self):
        CALLS.append("quiz")

    def build_projects(self):
        CALLS.append("projects")

    def view_progress(self):
        CALLS.append("progress")

    def reset_progress_interactive(self):
        CALLS.append("reset")

    def ai_tutor_menu(self):
        CALLS.append("tutor")


def _client_with_models(*ids):
    data = [types.SimpleNamespace(id=i) for i in ids]
    return types.SimpleNamespace(models=types.SimpleNamespace(list=lambda: types.SimpleNamespace(data=data)))


class FakeTutorAvailable:
    def __init__(self, *args, **kwargs):
        pass

    def is_available(self):
        return True

    def unavailable_reason(self):
        return "configure"

    @property
    def model(self):
        return "gpt-4.1-nano"

    def _get_client(self):
        return _client_with_models("gpt-4o-mini", "gpt-4.1-nano", "whisper-1")

    def answer(self, question, lesson=None):
        return f"Answer to: {question}"


class FakeTutorUnavailable(FakeTutorAvailable):
    def is_available(self):
        return False


@pytest.fixture(autouse=True)
def _isolate(tmp_path, monkeypatch):
    CALLS.clear()
    monkeypatch.setenv("PYTHON_MASTERY_HOME", str(tmp_path))
    for var in ("OPENAI_API_KEY", "OPENAI_MODEL", "OPENAI_BASE_URL"):
        monkeypatch.delenv(var, raising=False)
    monkeypatch.setattr(main, "PythonMasteryApp", FakeApp)


# --------------------------------------------------------------------------- #
# Core navigation commands
# --------------------------------------------------------------------------- #
def test_no_args_launches_run():
    result = runner.invoke(main.app, [])
    assert result.exit_code == 0
    assert "run" in CALLS


def test_start_command():
    assert runner.invoke(main.app, ["start"]).exit_code == 0
    assert CALLS.count("run") == 1


def test_lessons_command():
    assert runner.invoke(main.app, ["lessons"]).exit_code == 0
    assert "browse" in CALLS


def test_quiz_command():
    assert runner.invoke(main.app, ["quiz"]).exit_code == 0
    assert "quiz" in CALLS


def test_projects_command():
    assert runner.invoke(main.app, ["projects"]).exit_code == 0
    assert "projects" in CALLS


def test_progress_command():
    assert runner.invoke(main.app, ["progress"]).exit_code == 0
    assert "progress" in CALLS


def test_reset_progress_command():
    assert runner.invoke(main.app, ["reset-progress"]).exit_code == 0
    assert "reset" in CALLS


def test_version_flag():
    result = runner.invoke(main.app, ["--version"])
    assert result.exit_code == 0
    assert "python-mastery-cli" in result.stdout


def test_launch_reports_curriculum_problems(monkeypatch):
    monkeypatch.setattr(main.curriculum, "validate_curriculum", lambda: ["boom"])
    result = runner.invoke(main.app, ["start"])
    assert result.exit_code == 0
    assert "boom" in result.stdout


# --------------------------------------------------------------------------- #
# AI tutor commands
# --------------------------------------------------------------------------- #
def test_configure_with_auto_model(monkeypatch):
    monkeypatch.setattr(ai_tutor, "AITutor", FakeTutorAvailable)
    result = runner.invoke(main.app, ["configure", "--api-key", "sk-test", "--auto-model"])
    assert result.exit_code == 0
    # Cheapest current model auto-selected and stored.
    assert main.cfg.get_api_key() == "sk-test"
    assert main.cfg.get_model() == "gpt-4.1-nano"


def test_configure_explicit_model_no_auto(monkeypatch):
    monkeypatch.setattr(ai_tutor, "AITutor", FakeTutorAvailable)
    result = runner.invoke(main.app, ["configure", "--api-key", "sk-x", "--model", "gpt-4o", "--no-auto-model"])
    assert result.exit_code == 0
    assert main.cfg.get_model() == "gpt-4o"


def test_configure_missing_key_aborts():
    result = runner.invoke(main.app, ["configure", "--api-key", "  "])
    assert result.exit_code == 1


def test_configure_auto_model_handles_api_error(monkeypatch):
    class Boom(FakeTutorAvailable):
        def _get_client(self):
            raise RuntimeError("network down")

    monkeypatch.setattr(ai_tutor, "AITutor", Boom)
    result = runner.invoke(main.app, ["configure", "--api-key", "sk-x"])
    assert result.exit_code == 0  # setup still succeeds
    assert main.cfg.get_api_key() == "sk-x"


def test_ask_command(monkeypatch):
    monkeypatch.setattr(ai_tutor, "AITutor", FakeTutorAvailable)
    result = runner.invoke(main.app, ["ask", "what", "is", "a", "list"])
    assert result.exit_code == 0
    assert "Answer to:" in result.stdout


def test_ask_unavailable(monkeypatch):
    monkeypatch.setattr(ai_tutor, "AITutor", FakeTutorUnavailable)
    result = runner.invoke(main.app, ["ask", "hi"])
    assert result.exit_code == 1


def test_ask_handles_tutor_error(monkeypatch):
    class Err(FakeTutorAvailable):
        def answer(self, question, lesson=None):
            raise ai_tutor.AITutorError("rate limited")

    monkeypatch.setattr(ai_tutor, "AITutor", Err)
    result = runner.invoke(main.app, ["ask", "hi"])
    assert result.exit_code == 1


def test_models_command(monkeypatch):
    monkeypatch.setattr(ai_tutor, "AITutor", FakeTutorAvailable)
    result = runner.invoke(main.app, ["models"])
    assert result.exit_code == 0
    assert "gpt-4o-mini" in result.stdout
    assert "cheapest" in result.stdout.lower()


def test_models_unavailable(monkeypatch):
    monkeypatch.setattr(ai_tutor, "AITutor", FakeTutorUnavailable)
    assert runner.invoke(main.app, ["models"]).exit_code == 1


def test_models_handles_api_error(monkeypatch):
    class Boom(FakeTutorAvailable):
        def _get_client(self):
            raise RuntimeError("nope")

    monkeypatch.setattr(ai_tutor, "AITutor", Boom)
    assert runner.invoke(main.app, ["models"]).exit_code == 1


def test_configure_prompts_for_key_when_omitted(monkeypatch):
    monkeypatch.setattr(ai_tutor, "AITutor", FakeTutorAvailable)
    result = runner.invoke(main.app, ["configure", "--no-auto-model"], input="sk-prompted\n")
    assert result.exit_code == 0
    assert main.cfg.get_api_key() == "sk-prompted"


def test_ask_empty_response(monkeypatch):
    class Empty(FakeTutorAvailable):
        def answer(self, question, lesson=None):
            return ""

    monkeypatch.setattr(ai_tutor, "AITutor", Empty)
    result = runner.invoke(main.app, ["ask", "hi"])
    assert result.exit_code == 0
    assert "empty response" in result.stdout.lower()


def test_configure_auto_model_no_cheap_found(monkeypatch):
    class NoCheap(FakeTutorAvailable):
        def _get_client(self):
            return _client_with_models("gpt-4o", "whisper-1")  # nothing cheap

    monkeypatch.setattr(ai_tutor, "AITutor", NoCheap)
    result = runner.invoke(main.app, ["configure", "--api-key", "sk-x"])
    assert result.exit_code == 0
    assert main.cfg.get_model() == main.cfg.DEFAULT_MODEL  # default retained


def test_lessons_command_eof_exits_cleanly(monkeypatch):
    # BUG repro: EOF inside a subcommand's menu used to abort (exit 1).
    class EOFApp(FakeApp):
        def browse_lessons(self):
            raise EOFError

    monkeypatch.setattr(main, "PythonMasteryApp", EOFApp)
    result = runner.invoke(main.app, ["lessons"])
    assert result.exit_code == 0
    assert "Exited" in result.stdout
