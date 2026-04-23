"""CLI output tests for the judge app."""

from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from quizz.cli.judge_app import app


RUNNER = CliRunner()

QUESTION_YAML = """questions:
  - id: 1
    question: \"Q1\"
    options:
      - \"A\"
      - \"B\"
  - id: 2
    question: \"Q2\"
    options:
      - \"X\"
      - \"Y\"
"""


def _write_answers(path: Path, q1: str, q2: str) -> None:
    """Write a two-answer YAML fixture file."""

    path.write_text(
        (
            "answers:\n"
            f"  - question-id: 1\n"
            f"    answer: \"{q1}\"\n"
            f"  - question-id: 2\n"
            f"    answer: \"{q2}\"\n"
        ),
        encoding="utf-8",
    )


def test_judge_cli_prints_scores_and_emoji_markers(tmp_path: Path) -> None:
    """Judge CLI should print score format and emoji-based highlights."""

    questions_path = tmp_path / "questions.yaml"
    questions_path.write_text(QUESTION_YAML, encoding="utf-8")

    p1_answers_path = tmp_path / "alice_answers.yaml"
    p2_answers_path = tmp_path / "bob_answers.yaml"
    p1_impersonation_path = tmp_path / "alice_as_bob_answers.yaml"
    p2_impersonation_path = tmp_path / "bob_as_alice_answers.yaml"

    _write_answers(p1_answers_path, q1="A", q2="Y")
    _write_answers(p2_answers_path, q1="B", q2="X")
    _write_answers(p1_impersonation_path, q1="B", q2="Y")
    _write_answers(p2_impersonation_path, q1="A", q2="X")

    result = RUNNER.invoke(
        app,
        [
            "judge",
            "--player-1-name",
            "Alice",
            "--player-2-name",
            "Bob",
            "--questions-file-path",
            str(questions_path),
            "--player-1-answers-file-path",
            str(p1_answers_path),
            "--player-1-impersonator-answers-file-path",
            str(p1_impersonation_path),
            "--player-2-answers-file-path",
            str(p2_answers_path),
            "--player-2-impersonator-answers-file-path",
            str(p2_impersonation_path),
        ],
    )

    assert result.exit_code == 0
    assert "Alice: 1/2" in result.stdout
    assert "Bob: 1/2" in result.stdout
    assert "🎭" in result.stdout
    assert "🎯" in result.stdout
