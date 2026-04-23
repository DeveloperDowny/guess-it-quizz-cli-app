"""Domain ports for IO boundaries."""

from __future__ import annotations

from pathlib import Path
from typing import Protocol

from quizz.domain.models import AnswerSheet, QuestionSet


class QuizRepository(Protocol):
    """Persistence contract for quiz files."""

    def load_questions(self, file_path: Path) -> QuestionSet:
        """Load questions from a YAML file."""

    def load_answers(self, file_path: Path) -> AnswerSheet:
        """Load answers from a YAML file."""

    def save_answers(self, file_path: Path, answers: AnswerSheet) -> None:
        """Save answers to a YAML file."""
