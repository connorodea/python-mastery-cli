"""User configuration (AI tutor settings + API key), stored locally.

Config lives alongside progress in ``~/.python_mastery_cli/config.json`` (override
the base directory with ``PYTHON_MASTERY_HOME``). The file is written with
``0600`` permissions because it may hold an API key, and it lives in the user's
home directory — never inside the repository, so it can't be committed.

Resolution order for every setting is: environment variable → config file →
built-in default. That means power users / CI can use env vars without writing
anything to disk, while casual users can ``python-mastery configure`` once.
"""

from __future__ import annotations

import json
import os
import stat
from pathlib import Path
from typing import Optional

# The cheapest broadly-available chat model is a safe default; `configure`
# (and the model auto-pick on first setup) can upgrade this to the newest
# cheap model available on the account.
DEFAULT_MODEL = "gpt-4o-mini"


def config_dir() -> Path:
    home = os.environ.get("PYTHON_MASTERY_HOME")
    return Path(home) if home else Path.home() / ".python_mastery_cli"


def config_path() -> Path:
    return config_dir() / "config.json"


def load_config() -> dict:
    """Load the config dict, returning ``{}`` if missing or unreadable."""
    path = config_path()
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, OSError, ValueError):
        return {}


def save_config(config: dict) -> Path:
    """Persist the config dict with owner-only (0600) permissions."""
    path = config_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    try:
        path.chmod(stat.S_IRUSR | stat.S_IWUSR)  # 0600 — keys are sensitive
    except OSError:
        # Some filesystems (e.g. certain mounts) reject chmod; not fatal.
        pass
    return path


# --------------------------------------------------------------------------- #
# Typed accessors
# --------------------------------------------------------------------------- #
def get_api_key() -> Optional[str]:
    """OpenAI API key from env (preferred) or stored config."""
    env = os.environ.get("OPENAI_API_KEY")
    if env:
        return env.strip()
    stored = load_config().get("openai_api_key")
    return stored.strip() if isinstance(stored, str) and stored.strip() else None


def get_model() -> str:
    return os.environ.get("OPENAI_MODEL") or load_config().get("model") or DEFAULT_MODEL


def get_base_url() -> Optional[str]:
    """Optional OpenAI-compatible base URL (e.g. a proxy or alt provider)."""
    return os.environ.get("OPENAI_BASE_URL") or load_config().get("base_url")


def set_api_key(key: str) -> Path:
    config = load_config()
    config["openai_api_key"] = key.strip()
    return save_config(config)


def set_model(model: str) -> Path:
    config = load_config()
    config["model"] = model.strip()
    return save_config(config)


def set_base_url(base_url: Optional[str]) -> Path:
    config = load_config()
    if base_url:
        config["base_url"] = base_url.strip()
    else:
        config.pop("base_url", None)
    return save_config(config)


def has_stored_key() -> bool:
    return bool(load_config().get("openai_api_key"))
