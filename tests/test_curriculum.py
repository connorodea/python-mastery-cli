"""Tests that validate the curriculum content and its data model invariants."""

from __future__ import annotations

import pytest

from python_mastery_cli import curriculum
from python_mastery_cli.models import (
    CodeExample,
    Exercise,
    Lesson,
    Level,
    QuestionType,
    QuizQuestion,
)
from python_mastery_cli.progress import Progress, recommend_next_lesson


# --------------------------------------------------------------------------- #
# Overall structure
# --------------------------------------------------------------------------- #
def test_curriculum_validates_clean():
    assert curriculum.validate_curriculum() == []


def test_expected_lesson_and_project_counts():
    lessons = curriculum.get_all_lessons()
    projects = curriculum.get_all_projects()
    assert len(lessons) == 80
    assert len(projects) == 13


def test_level_breakdown_counts():
    assert len(curriculum.get_lessons_by_level("beginner")) == 27
    assert len(curriculum.get_lessons_by_level("intermediate")) == 24
    assert len(curriculum.get_lessons_by_level("advanced")) == 29


def test_all_lesson_ids_unique():
    ids = [lesson.id for lesson in curriculum.get_all_lessons()]
    assert len(ids) == len(set(ids))


def test_all_project_ids_unique():
    ids = [p.id for p in curriculum.get_all_projects()]
    assert len(ids) == len(set(ids))


def test_lookup_helpers():
    first = curriculum.get_all_lessons()[0]
    assert curriculum.get_lesson(first.id) is first
    assert curriculum.get_lesson("does-not-exist") is None
    assert curriculum.get_project("does-not-exist") is None


# --------------------------------------------------------------------------- #
# Per-lesson content guarantees
# --------------------------------------------------------------------------- #
def test_every_lesson_has_teaching_content():
    for lesson in curriculum.get_all_lessons():
        assert lesson.explanation.strip(), f"{lesson.id} missing explanation"
        assert lesson.estimated_minutes > 0
        assert lesson.quiz_questions, f"{lesson.id} has no quiz questions"
        assert lesson.has_exercise, f"{lesson.id} has no mini exercise"
        assert lesson.mini_exercise.solution.strip(), f"{lesson.id} exercise lacks a solution"


def test_next_lesson_chain_is_wired():
    lessons = curriculum.get_all_lessons()
    # Every lesson except the last points at a real, existing lesson.
    for lesson in lessons[:-1]:
        assert lesson.next_lesson_id is not None
        assert curriculum.get_lesson(lesson.next_lesson_id) is not None
    assert lessons[-1].next_lesson_id is None


def test_all_four_question_types_are_used():
    used = {
        q.qtype
        for lesson in curriculum.get_all_lessons()
        for q in lesson.quiz_questions
    }
    assert used == set(QuestionType)


def test_line_by_line_walkthrough_data_is_present():
    # The "explain line by line" feature relies on annotated examples.
    annotated = sum(
        1
        for lesson in curriculum.get_all_lessons()
        for ex in lesson.code_examples
        if ex.has_walkthrough
    )
    assert annotated > 0


# --------------------------------------------------------------------------- #
# Drill reference-solution correctness (the "Run & check" feedback loop)
# --------------------------------------------------------------------------- #
# Self-contained drills (pure stdlib, no input(), a literal expected output):
# running the reference solution MUST reproduce its expected_output exactly and
# deterministically, or a learner who solves it correctly is wrongly told their
# output "doesn't match". Drills needing third-party libs, input(), or with
# illustrative/placeholder expected output are intentionally excluded here.
EXACT_OUTPUT_DRILLS = ["b21", "i02"]


@pytest.mark.parametrize("lesson_id", EXACT_OUTPUT_DRILLS)
def test_self_contained_drill_solution_matches_expected_output(lesson_id):
    from python_mastery_cli import runner

    exercise = curriculum.get_lesson(lesson_id).mini_exercise
    assert exercise is not None and exercise.expected_output
    result = runner.run_code(exercise.solution)
    assert result.ok, f"{lesson_id} solution errored: {result.stderr}"
    assert runner.output_matches(result.stdout, exercise.expected_output), (
        f"{lesson_id}: solution output {result.stdout!r} != "
        f"expected_output {exercise.expected_output!r}"
    )


# --------------------------------------------------------------------------- #
# Quiz answerability — the stored answer must be the one the grader accepts
# --------------------------------------------------------------------------- #
def test_multiple_choice_options_distinct_after_normalization():
    # grade_answer normalizes (lowercase, strip quotes) before comparing, so two
    # options that normalize to the same string are indistinguishable: selecting
    # a *wrong* distractor would grade as correct (e.g. "csv.DictReader" vs the
    # distractor "csv.dictreader"). Every MC question's options must stay distinct
    # under that same normalization.
    from python_mastery_cli.quiz import QuestionType, _normalize

    for lesson in curriculum.get_all_lessons():
        for q in lesson.quiz_questions:
            if q.qtype is QuestionType.MULTIPLE_CHOICE:
                norm = [_normalize(o) for o in q.options]
                assert len(set(norm)) == len(norm), (
                    f"{lesson.id}: MC options collide after normalization: {q.options}"
                )


def test_multiple_choice_correct_option_position_grades_true():
    # Selecting the (1-indexed) position of the correct option must grade correct,
    # and exactly one option must match the stored correct_answer.
    from python_mastery_cli.quiz import QuestionType, _normalize, grade_answer

    for lesson in curriculum.get_all_lessons():
        for q in lesson.quiz_questions:
            if q.qtype is QuestionType.MULTIPLE_CHOICE:
                matches = [i for i, o in enumerate(q.options, start=1)
                           if _normalize(o) == _normalize(q.correct_answer)]
                assert len(matches) == 1, f"{lesson.id}: correct_answer matches {matches} options"
                assert grade_answer(q, str(matches[0])) is True


def test_text_answer_questions_grade_their_own_correct_answer():
    # For the types answered by typing (true/false, fill-blank, short-answer),
    # the stored correct_answer must itself grade as correct.
    from python_mastery_cli.quiz import QuestionType, grade_answer

    text_types = {QuestionType.TRUE_FALSE, QuestionType.FILL_BLANK, QuestionType.SHORT_ANSWER}
    for lesson in curriculum.get_all_lessons():
        for q in lesson.quiz_questions:
            if q.qtype in text_types:
                assert grade_answer(q, q.correct_answer) is True, (
                    f"{lesson.id}: stored correct_answer {q.correct_answer!r} grades as wrong"
                )


# --------------------------------------------------------------------------- #
# Per-project content guarantees
# --------------------------------------------------------------------------- #
def test_every_project_has_a_build_guide_and_solution():
    for project in curriculum.get_all_projects():
        assert project.build_guide, f"{project.id} has no build guide"
        assert project.solution.strip(), f"{project.id} has no reference solution"
        assert project.difficulty in ("easy", "medium", "hard")


# --------------------------------------------------------------------------- #
# Recommendation logic against the real curriculum
# --------------------------------------------------------------------------- #
def test_recommend_next_lesson_on_fresh_progress_is_first_lesson():
    lessons = curriculum.get_all_lessons()
    nxt = recommend_next_lesson(Progress(), lessons)
    assert nxt is lessons[0]


def test_recommend_next_lesson_skips_completed():
    lessons = curriculum.get_all_lessons()
    p = Progress(completed_lessons=[lessons[0].id])
    nxt = recommend_next_lesson(p, lessons)
    assert nxt is lessons[1]


# --------------------------------------------------------------------------- #
# Model validation (lesson data validation)
# --------------------------------------------------------------------------- #
def test_multiple_choice_requires_answer_in_options():
    with pytest.raises(ValueError):
        QuizQuestion(
            question="x",
            qtype="multiple_choice",
            options=["a", "b"],
            correct_answer="c",  # not an option
        )


def test_true_false_rejects_bad_answer():
    with pytest.raises(ValueError):
        QuizQuestion(question="x", qtype="true_false", correct_answer="maybe")


def test_code_example_rejects_out_of_range_line_note():
    with pytest.raises(ValueError):
        CodeExample(title="t", code="print(1)", line_notes={5: "no such line"})


def test_lesson_rejects_empty_explanation():
    with pytest.raises(ValueError):
        Lesson(id="x", title="t", level=Level.BEGINNER, estimated_minutes=5, explanation="  ")


def test_exercise_rejects_bad_difficulty():
    with pytest.raises(ValueError):
        Exercise(id="x", title="t", instructions="do it", difficulty="impossible")
