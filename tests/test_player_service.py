"""Tests for player session and answer collection."""

from __future__ import annotations

from pathlib import Path

import pytest

from quizz.config import AppSettings
from quizz.infrastructure.yaml_repository import YamlQuizRepository
from quizz.services.path_resolver import DefaultPathResolver
from quizz.services.player_service import PlayerService


QUESTION_YAML = """questions:
  - id: 1
    question: \"Favorite drink?\"
    options:
      - \"Tea\"
      - \"Coffee\"
  - id: 2
    question: \"Favorite pet?\"
    options:
      - \"Dog\"
      - \"Cat\"
"""


def test_run_session_saves_to_default_paths(tmp_path: Path) -> None:
    """Player service should save self and impersonation sheets to defaults."""

    questions_path = tmp_path / "questions.yaml"
    questions_path.write_text(QUESTION_YAML, encoding="utf-8")

    repository = YamlQuizRepository()
    resolver = DefaultPathResolver(AppSettings(data_dir=tmp_path / "data"))
    service = PlayerService(repository=repository, path_resolver=resolver)

    def answer_provider(question, respondent_name: str, perspective_name: str) -> str:  # noqa: ANN001
        del respondent_name
        if perspective_name == "Alice":
            return question.options[0]
        return question.options[1]

    impersonatee_path, impersonator_path = service.run_session(
        questions_file_path=questions_path,
        impersonator="Alice",
        impersonatee="Bob",
        answer_provider=answer_provider,
    )

    assert impersonatee_path == tmp_path / "data" / "alice_answers.yaml"
    assert impersonator_path == tmp_path / "data" / "alice_as_bob_answers.yaml"

    alice_sheet = repository.load_answers(impersonatee_path)
    alice_impersonation_sheet = repository.load_answers(impersonator_path)

    assert alice_sheet.to_map() == {1: "Tea", 2: "Dog"}
    assert alice_impersonation_sheet.to_map() == {1: "Coffee", 2: "Cat"}


def test_collect_answer_sheet_rejects_invalid_option(tmp_path: Path) -> None:
    """Service should reject answers that are not in the question options."""

    questions_path = tmp_path / "questions.yaml"
    questions_path.write_text(QUESTION_YAML, encoding="utf-8")

    repository = YamlQuizRepository()
    resolver = DefaultPathResolver(AppSettings(data_dir=tmp_path / "data"))
    service = PlayerService(repository=repository, path_resolver=resolver)

    question_set = repository.load_questions(questions_path)

    def invalid_provider(question, respondent_name: str, perspective_name: str) -> str:  # noqa: ANN001
        del question, respondent_name, perspective_name
        return "Invalid Option"

    with pytest.raises(ValueError):
        service.collect_answer_sheet(
            question_set=question_set,
            respondent_name="Bob",
            perspective_name="Bob",
            answer_provider=invalid_provider,
        )
