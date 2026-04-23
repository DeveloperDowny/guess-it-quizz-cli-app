"""Typer app for collecting player and impersonation answers."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Annotated

import typer
from pydantic import ValidationError

from quizz.config import get_settings
from quizz.domain.models import Question
from quizz.infrastructure.yaml_repository import YamlQuizRepository
from quizz.services.path_resolver import DefaultPathResolver
from quizz.services.player_service import PlayerService

logger = logging.getLogger(__name__)

app = typer.Typer(add_completion=False, no_args_is_help=True)


def _interactive_answer_provider(question: Question, respondent: str, perspective: str) -> str:
    """Prompt one participant to answer a question."""

    typer.echo("")
    typer.secho(
        f"{respondent}, answer as {perspective}:",
        fg=typer.colors.BRIGHT_CYAN,
        bold=True,
    )
    typer.echo(f"Q{question.id}. {question.question}")
    for index, option in enumerate(question.options, start=1):
        typer.echo(f"  {index}. {option}")

    while True:
        selected_index = typer.prompt("Choose option number", type=int)
        if 1 <= selected_index <= len(question.options):
            return question.options[selected_index - 1]
        typer.secho("Invalid option number. Please try again.", fg=typer.colors.YELLOW)


@app.command()
def play(
    impersonator: Annotated[
        str,
        typer.Option(
            "--impersonator",
            help="Person answering while impersonating another player.",
        ),
    ],
    impersonatee: Annotated[
        str,
        typer.Option(
            "--impersonatee",
            help="Person from whose perspective questions are answered.",
        ),
    ],
    questions_file_path: Annotated[
        Path | None,
        typer.Option(
            "--questions-file-path",
            help="Path to the questions YAML file.",
        ),
    ] = None,
    answers_file_path: Annotated[
        Path | None,
        typer.Option(
            "--answers-file-path",
            help="Alias for impersonatee answers file path.",
        ),
    ] = None,
    impersonator_answers_file_path: Annotated[
        Path | None,
        typer.Option(
            "--impersonator-answers-file-path",
            help="Output path for impersonator answers.",
        ),
    ] = None,
    impersonatee_answers_file_path: Annotated[
        Path | None,
        typer.Option(
            "--impersonatee-answers-file-path",
            "--impersnoatee-answers-file-path",
            help="Output path for impersonatee answers.",
        ),
    ] = None,
) -> None:
    """Collect the impersonator's own and impersonation answers."""

    settings = get_settings()
    repository = YamlQuizRepository()
    path_resolver = DefaultPathResolver(settings)
    service = PlayerService(repository=repository, path_resolver=path_resolver)

    selected_questions_path = questions_file_path or settings.questions_file_path
    selected_self_answers_path = impersonatee_answers_file_path or answers_file_path

    try:
        self_answers_path, impersonation_answers_path = service.run_session(
            questions_file_path=selected_questions_path,
            impersonator=impersonator,
            impersonatee=impersonatee,
            answer_provider=_interactive_answer_provider,
            impersonator_answers_file_path=impersonator_answers_file_path,
            impersonatee_answers_file_path=selected_self_answers_path,
        )
    except (FileNotFoundError, ValidationError, ValueError) as exc:
        logger.exception("Player app failed")
        typer.secho(f"Error: {exc}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from exc

    typer.secho("Answers captured successfully.", fg=typer.colors.GREEN)
    typer.echo(f"{impersonator} answers saved to: {self_answers_path}")
    typer.echo(f"{impersonator} impersonation answers saved to: {impersonation_answers_path}")


def run() -> None:
    """Run the player CLI app."""

    app()


if __name__ == "__main__":
    run()
