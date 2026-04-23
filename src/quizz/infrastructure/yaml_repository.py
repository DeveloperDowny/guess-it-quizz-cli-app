"""YAML-backed repository implementation."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import yaml

from quizz.domain.models import AnswerSheet, QuestionSet
from quizz.domain.ports import QuizRepository

logger = logging.getLogger(__name__)


class YamlQuizRepository(QuizRepository):
    """Read and write question/answer data as YAML files."""

    def load_questions(self, file_path: Path) -> QuestionSet:
        """Load and validate a question set from a YAML file.

        Args:
            file_path: Path to questions YAML.

        Returns:
            QuestionSet: Parsed and validated questions.
        """

        payload = self._read_yaml_dict(file_path)
        question_set = QuestionSet.model_validate(payload)
        logger.info("Loaded %s questions from %s", len(question_set.questions), file_path)
        return question_set

    def load_answers(self, file_path: Path) -> AnswerSheet:
        """Load and validate an answer sheet from a YAML file.

        Args:
            file_path: Path to answers YAML.

        Returns:
            AnswerSheet: Parsed and validated answers.
        """

        payload = self._read_yaml_dict(file_path)
        answer_sheet = AnswerSheet.model_validate(payload)
        logger.info("Loaded %s answers from %s", len(answer_sheet.answers), file_path)
        return answer_sheet

    def save_answers(self, file_path: Path, answers: AnswerSheet) -> None:
        """Save an answer sheet as YAML.

        Args:
            file_path: Destination YAML path.
            answers: Answers to persist.
        """

        file_path.parent.mkdir(parents=True, exist_ok=True)
        with file_path.open("w", encoding="utf-8") as yaml_file:
            yaml.safe_dump(
                answers.model_dump(by_alias=True),
                yaml_file,
                sort_keys=False,
                allow_unicode=False,
            )
        logger.info("Saved %s answers to %s", len(answers.answers), file_path)

    def _read_yaml_dict(self, file_path: Path) -> dict[str, Any]:
        """Read YAML content and ensure dictionary shape."""

        if not file_path.exists():
            raise FileNotFoundError(f"YAML file not found: {file_path}")

        with file_path.open("r", encoding="utf-8") as yaml_file:
            payload = yaml.safe_load(yaml_file)

        if payload is None:
            raise ValueError(f"YAML file is empty: {file_path}")
        if not isinstance(payload, dict):
            raise ValueError(f"YAML top-level must be a mapping: {file_path}")

        return payload
