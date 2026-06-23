"""Tests for the quiz grading and scoring engine."""

from __future__ import annotations

import pytest

from python_mastery_cli.models import QuestionType, QuizQuestion
from python_mastery_cli.quiz import QuizResult, grade_answer, points_for


# --------------------------------------------------------------------------- #
# Multiple choice
# --------------------------------------------------------------------------- #
def _mc() -> QuizQuestion:
    return QuizQuestion(
        question="Which prints text?",
        qtype="multiple_choice",
        options=["echo()", "print()", "log()"],
        correct_answer="print()",
        difficulty="easy",
    )


def test_multiple_choice_accepts_correct_number():
    assert grade_answer(_mc(), "2") is True


def test_multiple_choice_accepts_correct_text_case_insensitively():
    assert grade_answer(_mc(), "PRINT()") is True


def test_multiple_choice_rejects_wrong_number():
    assert grade_answer(_mc(), "1") is False


def test_multiple_choice_rejects_out_of_range_and_garbage():
    assert grade_answer(_mc(), "9") is False
    assert grade_answer(_mc(), "banana") is False
    assert grade_answer(_mc(), "") is False


# --------------------------------------------------------------------------- #
# True / False
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("answer", ["true", "True", "t", "yes", "y", "1"])
def test_true_false_truthy_variants(answer):
    q = QuizQuestion(question="x", qtype="true_false", correct_answer="true")
    assert grade_answer(q, answer) is True


@pytest.mark.parametrize("answer", ["false", "f", "no", "n", "0"])
def test_true_false_falsy_variants_against_true(answer):
    q = QuizQuestion(question="x", qtype="true_false", correct_answer="true")
    assert grade_answer(q, answer) is False


def test_true_false_correct_false():
    q = QuizQuestion(question="x", qtype="true_false", correct_answer="false")
    assert grade_answer(q, "false") is True
    assert grade_answer(q, "true") is False


# --------------------------------------------------------------------------- #
# Fill in the blank
# --------------------------------------------------------------------------- #
def test_fill_blank_is_case_and_whitespace_insensitive():
    q = QuizQuestion(question="x", qtype="fill_blank", correct_answer="interpreter")
    assert grade_answer(q, "Interpreter") is True
    assert grade_answer(q, "  interpreter  ") is True
    assert grade_answer(q, "'interpreter'") is True
    assert grade_answer(q, "compiler") is False


# --------------------------------------------------------------------------- #
# Short answer (keyword matching)
# --------------------------------------------------------------------------- #
def test_short_answer_exact_model_answer():
    q = QuizQuestion(
        question="x",
        qtype="short_answer",
        correct_answer="a list comprehension",
    )
    assert grade_answer(q, "A List Comprehension") is True


def test_short_answer_keyword_matching():
    q = QuizQuestion(
        question="x",
        qtype="short_answer",
        correct_answer="a list comprehension builds a list",
        keywords=["list", "comprehension"],
    )
    assert grade_answer(q, "it is a comprehension that makes a list") is True
    assert grade_answer(q, "it is a loop") is False


# --------------------------------------------------------------------------- #
# Scoring
# --------------------------------------------------------------------------- #
def test_points_for_difficulty():
    easy = QuizQuestion(question="x", qtype="fill_blank", correct_answer="a", difficulty="easy")
    medium = QuizQuestion(question="x", qtype="fill_blank", correct_answer="a", difficulty="medium")
    hard = QuizQuestion(question="x", qtype="fill_blank", correct_answer="a", difficulty="hard")
    assert points_for(easy) == 5
    assert points_for(medium) == 8
    assert points_for(hard) == 12


def test_quiz_result_percentage_and_pass():
    r = QuizResult(total=10, correct=7, score=40)
    assert r.percentage == 70.0
    assert r.passed is True

    r2 = QuizResult(total=10, correct=6)
    assert r2.percentage == 60.0
    assert r2.passed is False


def test_quiz_result_empty_is_zero():
    r = QuizResult()
    assert r.percentage == 0.0
    assert r.passed is False


def test_question_type_coercion_from_string():
    q = QuizQuestion(question="x", qtype="fill_blank", correct_answer="a")
    assert q.qtype is QuestionType.FILL_BLANK


def test_true_false_rejects_unparseable_answer():
    q = QuizQuestion(question="x", qtype="true_false", correct_answer="true")
    assert grade_answer(q, "maybe") is False


def test_short_answer_no_keywords_and_wrong_returns_false():
    q = QuizQuestion(question="x", qtype="short_answer", correct_answer="abc")
    assert grade_answer(q, "totally different") is False
