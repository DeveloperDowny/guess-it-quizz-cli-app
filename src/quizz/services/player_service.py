"""Use case service for collecting player responses."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Callable

from quizz.domain.models import AnswerEntry, AnswerSheet, Question, QuestionSet
from quizz.domain.ports import QuizRepository
from quizz.services.path_resolver import DefaultPathResolver

logger = logging.getLogger(__name__)

AnswerProvider = Callable[[Question, str, str], str]


class PlayerService:
    """Coordinate player answer collection and persistence."""

    def __init__(self, repository: QuizRepository, path_resolver: DefaultPathResolver) -> None:
        """Initialize the service.

        Args:
            repository: Persistence dependency.
            path_resolver: Centralized default path provider.
        """

        self._repository = repository
        self._path_resolver = path_resolver

    def run_session(
        self,
        *,
        questions_file_path: Path,
        impersonator: str,
        impersonatee: str,
        answer_provider: AnswerProvider,
        impersonator_answers_file_path: Path | None = None,
        impersonatee_answers_file_path: Path | None = None,
    ) -> tuple[Path, Path]:
        """Collect and persist self and impersonation answer sheets.

        Args:
            questions_file_path: Source questions YAML path.
            impersonator: Person answering while impersonating another player.
            impersonatee: Person being impersonated.
            answer_provider: Callback used to gather one answer per question.
            impersonator_answers_file_path: Optional output path override for
                impersonation answers.
            impersonatee_answers_file_path: Optional output path override for
                the impersonator's own answers.

        Returns:
            tuple[Path, Path]: (self answers path, impersonation answers path)
        """

        question_set = self._repository.load_questions(questions_file_path)

        impersonatee_output_path = (
            impersonatee_answers_file_path
            if impersonatee_answers_file_path is not None
            else self._path_resolver.default_player_answers_path(impersonator)
        )
        impersonator_output_path = (
            impersonator_answers_file_path
            if impersonator_answers_file_path is not None
            else self._path_resolver.default_impersonator_answers_path(impersonator, impersonatee)
        )

        impersonatee_sheet = self.collect_answer_sheet(
            question_set=question_set,
            respondent_name=impersonator,
            perspective_name=impersonator,
            answer_provider=answer_provider,
        )
        impersonator_sheet = self.collect_answer_sheet(
            question_set=question_set,
            respondent_name=impersonator,
            perspective_name=impersonatee,
            answer_provider=answer_provider,
        )

        self._repository.save_answers(impersonatee_output_path, impersonatee_sheet)
        self._repository.save_answers(impersonator_output_path, impersonator_sheet)

        logger.info(
            "Completed player session for impersonator=%s impersonatee=%s",
            impersonator,
            impersonatee,
        )
        return impersonatee_output_path, impersonator_output_path

    def collect_answer_sheet(
        self,
        *,
        question_set: QuestionSet,
        respondent_name: str,
        perspective_name: str,
        answer_provider: AnswerProvider,
    ) -> AnswerSheet:
        """Collect one validated answer per question.

        Args:
            question_set: Questions to ask.
            respondent_name: Name of the person answering.
            perspective_name: Name of the perspective being used.
            answer_provider: Callback to gather an answer.

        Returns:
            AnswerSheet: Validated answer sheet.

        Raises:
            ValueError: If answer provider returns an invalid option.
        """

        answers: list[AnswerEntry] = []
        for question in question_set.questions:
            selected_answer = answer_provider(question, respondent_name, perspective_name).strip()
            if selected_answer not in question.options:
                raise ValueError(
                    f"Invalid answer '{selected_answer}' for question {question.id}. "
                    f"Expected one of: {question.options}"
                )
            answers.append(AnswerEntry(question_id=question.id, answer=selected_answer))

        return AnswerSheet(answers=answers)
