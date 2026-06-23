"""Optional AI tutor powered by the OpenAI API.

The tutor adds on-demand help on top of the static curriculum: re-explaining a
concept more simply, generating fresh examples, going deeper, and answering
free-form questions — always grounded in the lesson the learner is currently on.

Design goals
------------
* **Optional & graceful.** The whole app works with no key and no ``openai``
  package installed; the tutor simply reports that it isn't configured.
* **Testable.** All network behaviour funnels through :meth:`AITutor.complete`,
  and a client can be injected, so tests never touch the network.
* **Provider-flexible.** Defaults to OpenAI but honours ``OPENAI_BASE_URL`` so an
  OpenAI-compatible endpoint can be used instead.
"""

from __future__ import annotations

import re
from typing import Callable, Optional

from . import config
from .models import Lesson

try:  # openai is an optional-at-runtime dependency
    from openai import OpenAI

    _IMPORT_ERROR: Optional[Exception] = None
except Exception as exc:  # pragma: no cover - exercised only without the package
    OpenAI = None  # type: ignore[assignment]
    _IMPORT_ERROR = exc


SYSTEM_PROMPT = (
    "You are a warm, patient Python tutor embedded in a terminal-based learning "
    "app for a student progressing from beginner to advanced (they are preparing "
    "for a Master's in Data Science). Explain clearly and concisely in plain "
    "language. Prefer short, runnable examples over walls of text. Put all code "
    "in fenced ```python blocks. When helpful, point out one common mistake. "
    "Never invent library behaviour — if unsure, say so. Keep answers focused; "
    "this is a CLI, so avoid overly long responses."
)


class AITutorError(RuntimeError):
    """Raised for any tutor failure (missing key, package, or API error)."""


class AITutor:
    """A thin, well-behaved wrapper around the OpenAI chat completions API."""

    def __init__(
        self,
        *,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        client: object = None,
    ) -> None:
        self._model = model or config.get_model()
        self._api_key = api_key if api_key is not None else config.get_api_key()
        self._base_url = base_url if base_url is not None else config.get_base_url()
        self._client = client  # injectable for tests

    # ------------------------------------------------------------------ #
    # Availability
    # ------------------------------------------------------------------ #
    @property
    def model(self) -> str:
        return self._model

    @staticmethod
    def sdk_installed() -> bool:
        return OpenAI is not None

    def has_key(self) -> bool:
        return bool(self._api_key)

    def is_available(self) -> bool:
        """True only if we can actually make a request (package + key present)."""
        return self.sdk_installed() and self.has_key()

    def unavailable_reason(self) -> str:
        if not self.sdk_installed():
            return (
                "The 'openai' package isn't installed. Install it with:\n"
                "    pip install openai"
            )
        if not self.has_key():
            return (
                "No OpenAI API key found. Set one with:\n"
                "    python-mastery configure\n"
                "or export OPENAI_API_KEY=... in your shell."
            )
        return ""

    # ------------------------------------------------------------------ #
    # Core call
    # ------------------------------------------------------------------ #
    def _get_client(self):
        if self._client is not None:
            return self._client
        if OpenAI is None:
            raise AITutorError("The 'openai' package isn't installed (pip install openai).")
        if not self._api_key:
            raise AITutorError("No OpenAI API key configured (run: python-mastery configure).")
        kwargs: dict = {"api_key": self._api_key}
        if self._base_url:
            kwargs["base_url"] = self._base_url
        self._client = OpenAI(**kwargs)
        return self._client

    def complete(
        self,
        messages: list[dict],
        *,
        max_tokens: int = 1500,
        temperature: float = 0.4,
    ) -> str:
        """Send a chat request and return the assistant's text.

        Adapts to model-family differences automatically: newer models
        (gpt-5.x, o-series) require ``max_completion_tokens`` instead of
        ``max_tokens`` and may reject a custom ``temperature``. Rather than
        hard-code which family needs what, we try, read the API's complaint, and
        retry with the offending parameter fixed. All failures are wrapped in
        :class:`AITutorError` with a readable message.
        """
        client = self._get_client()
        params: dict = {
            "model": self._model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }

        last_error: Optional[Exception] = None
        # At most two distinct param fixes exist (max_tokens, temperature), so the
        # loop always returns or breaks well before exhausting its iterations; the
        # range bound is a pure safety backstop.
        for _ in range(4):  # pragma: no branch
            try:
                response = client.chat.completions.create(**params)
                return (response.choices[0].message.content or "").strip()
            except Exception as exc:  # noqa: BLE001 - inspect and adapt
                last_error = exc
                message = str(exc).lower()
                adjusted = False
                if "max_tokens" in message and "max_completion_tokens" in message and "max_tokens" in params:
                    params["max_completion_tokens"] = params.pop("max_tokens")
                    adjusted = True
                if "temperature" in message and "temperature" in params and (
                    "unsupported" in message
                    or "does not support" in message
                    or "only the default" in message
                ):
                    params.pop("temperature", None)
                    adjusted = True
                if not adjusted:
                    break
        raise AITutorError(str(last_error))

    # ------------------------------------------------------------------ #
    # Prompt construction
    # ------------------------------------------------------------------ #
    @staticmethod
    def lesson_context(lesson: Optional[Lesson]) -> str:
        if lesson is None:
            return ""
        terms = "; ".join(f"{k}: {v}" for k, v in (lesson.key_terms or {}).items())
        parts = [
            f"The student is currently on the lesson '{lesson.title}' "
            f"(level: {lesson.level}).",
            f"Lesson explanation:\n{lesson.explanation}",
        ]
        if terms:
            parts.append(f"Key terms: {terms}")
        return "\n\n".join(parts)

    def _ask(self, user_prompt: str, lesson: Optional[Lesson] = None) -> str:
        messages: list[dict] = [{"role": "system", "content": SYSTEM_PROMPT}]
        context = self.lesson_context(lesson)
        if context:
            messages.append({"role": "system", "content": context})
        messages.append({"role": "user", "content": user_prompt})
        return self.complete(messages)

    # ------------------------------------------------------------------ #
    # Public tutor actions
    # ------------------------------------------------------------------ #
    def explain_more(self, lesson: Lesson) -> str:
        return self._ask(
            "Re-explain this lesson's core concept in a simpler, more beginner-"
            "friendly way. Use a fresh real-world analogy and one tiny example.",
            lesson,
        )

    def another_example(self, lesson: Lesson) -> str:
        return self._ask(
            "Give me ONE more short, runnable Python example that illustrates this "
            "lesson's concept (different from any already shown), with 1-2 sentences "
            "explaining what it demonstrates.",
            lesson,
        )

    def go_deeper(self, lesson: Lesson) -> str:
        return self._ask(
            "Give a more in-depth, intermediate-level discussion of this concept: "
            "important edge cases, how it's used in real projects (data work where "
            "relevant), and one common gotcha. Keep it focused.",
            lesson,
        )

    def answer(self, question: str, lesson: Optional[Lesson] = None) -> str:
        return self._ask(
            f"The student asks: {question}\n\nAnswer clearly and practically. "
            "If code helps, include a short runnable snippet.",
            lesson,
        )

    def explain_code_line(self, line: str, surrounding: str = "") -> str:
        prompt = (
            f"Explain this single line of Python in plain language, including what "
            f"each part does:\n\n    {line}\n"
        )
        if surrounding:
            prompt += f"\nFor context, the surrounding code is:\n```python\n{surrounding}\n```"
        return self._ask(prompt)


# --------------------------------------------------------------------------- #
# Model selection helper (used at setup to honour "newest, cheapest")
# --------------------------------------------------------------------------- #
_EXCLUDE = ("embedding", "whisper", "tts", "audio", "image", "dall-e", "moderation",
            "realtime", "transcribe", "search", "vision-preview")


def recommend_cheap_model(available_ids: list[str]) -> Optional[str]:
    """Pick the newest, cheapest chat model from a list of model ids.

    Heuristic (no pricing is exposed by the API): prefer ``nano`` over ``mini``
    over everything else, and within a tier prefer the highest version number.
    Returns ``None`` if nothing suitable is found.
    """

    def version_score(model_id: str) -> float:
        match = re.search(r"(\d+(?:\.\d+)?)", model_id)
        return float(match.group(1)) if match else 0.0

    def tier_score(model_id: str) -> int:
        if "nano" in model_id:
            return 3
        if "mini" in model_id:
            return 2
        return 0  # full-size models aren't "cheap" — skip unless nothing else

    candidates = []
    for model_id in available_ids:
        lower = model_id.lower()
        if any(bad in lower for bad in _EXCLUDE):
            continue
        if not (lower.startswith("gpt") or lower.startswith("o")):
            continue
        tier = tier_score(lower)
        if tier == 0:
            continue  # only consider explicitly-cheap tiers
        candidates.append((tier, version_score(lower), model_id))

    if not candidates:
        return None
    candidates.sort(key=lambda c: (c[0], c[1]), reverse=True)
    return candidates[0][2]
