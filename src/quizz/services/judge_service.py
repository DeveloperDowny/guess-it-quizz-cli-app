"""Use case service for scoring impersonation answers."""

from __future__ import annotations

from dataclasses import dataclass

from quizz.domain.models import AnswerSheet, Question, QuestionSet


@dataclass(frozen=True)
class QuestionReview:
    """Per-question scoring details for one player."""

    question: Question
    guessed_answer: str
    correct_answer: str
    is_match: bool


@dataclass(frozen=True)
class PlayerJudgement:
    """Aggregated scoring details for one player."""

    player_name: str
    target_name: str
    matched_answers: int
    total_questions: int
    reviews: list[QuestionReview]


class JudgeService:
    """Calculate impersonation match scores."""

    def evaluate(
        self,
        *,
        question_set: QuestionSet,
        player_name: str,
        target_name: str,
        player_impersonation_sheet: AnswerSheet,
        target_actual_sheet: AnswerSheet,
    ) -> PlayerJudgement:
        """Score one player's impersonation against target answers.

        Args:
            question_set: Canonical question definitions.
            player_name: Name of player being scored.
            target_name: Name of player being impersonated.
            player_impersonation_sheet: Answers by player while impersonating target.
            target_actual_sheet: Actual answers from target.

        Returns:
            PlayerJudgement: Match summary and per-question details.
        """

        guessed_map = player_impersonation_sheet.to_map()
        correct_map = target_actual_sheet.to_map()

        reviews: list[QuestionReview] = []
        for question in question_set.questions:
            guessed_answer = guessed_map.get(question.id, "")
            correct_answer = correct_map.get(question.id, "")
            is_match = bool(guessed_answer) and guessed_answer == correct_answer
            reviews.append(
                QuestionReview(
                    question=question,
                    guessed_answer=guessed_answer,
                    correct_answer=correct_answer,
                    is_match=is_match,
                )
            )

        matched_answers = sum(1 for review in reviews if review.is_match)
        return PlayerJudgement(
            player_name=player_name,
            target_name=target_name,
            matched_answers=matched_answers,
            total_questions=len(question_set.questions),
            reviews=reviews,
        )
