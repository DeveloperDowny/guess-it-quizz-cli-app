"""Tests for impersonation scoring logic."""

from __future__ import annotations

from quizz.domain.models import AnswerEntry, AnswerSheet, Question, QuestionSet
from quizz.services.judge_service import JudgeService


def test_judge_service_scores_only_exact_matches() -> None:
    """Score should increment only when guessed and actual answers match."""

    question_set = QuestionSet(
        questions=[
            Question(id=1, question="Q1", options=["A", "B"]),
            Question(id=2, question="Q2", options=["X", "Y"]),
        ]
    )

    player_impersonation_sheet = AnswerSheet(
        answers=[
            AnswerEntry(question_id=1, answer="A"),
            AnswerEntry(question_id=2, answer="X"),
        ]
    )
    target_actual_sheet = AnswerSheet(
        answers=[
            AnswerEntry(question_id=1, answer="A"),
            AnswerEntry(question_id=2, answer="Y"),
        ]
    )

    service = JudgeService()
    result = service.evaluate(
        question_set=question_set,
        player_name="Alice",
        target_name="Bob",
        player_impersonation_sheet=player_impersonation_sheet,
        target_actual_sheet=target_actual_sheet,
    )

    assert result.matched_answers == 1
    assert result.total_questions == 2
    assert [review.is_match for review in result.reviews] == [True, False]
