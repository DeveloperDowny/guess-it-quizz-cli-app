"""Tests for YAML repository behavior."""

from __future__ import annotations

from pathlib import Path

from quizz.domain.models import AnswerEntry, AnswerSheet
from quizz.infrastructure.yaml_repository import YamlQuizRepository


QUESTION_YAML = """questions:
  - id: 1
    question: \"Q1?\"
    options:
      - \"A\"
      - \"B\"
  - id: 2
    question: \"Q2?\"
    options:
      - \"X\"
      - \"Y\"
"""


def test_load_questions_and_answers_roundtrip(tmp_path: Path) -> None:
    """Repository should load questions and roundtrip answer YAML."""

    repository = YamlQuizRepository()

    questions_path = tmp_path / "questions.yaml"
    questions_path.write_text(QUESTION_YAML, encoding="utf-8")

    question_set = repository.load_questions(questions_path)
    assert len(question_set.questions) == 2

    output_answers_path = tmp_path / "answers.yaml"
    expected_sheet = AnswerSheet(
        answers=[
            AnswerEntry(question_id=1, answer="B"),
            AnswerEntry(question_id=2, answer="X"),
        ]
    )

    repository.save_answers(output_answers_path, expected_sheet)
    loaded_sheet = repository.load_answers(output_answers_path)

    assert loaded_sheet == expected_sheet
