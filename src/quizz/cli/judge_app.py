"""Typer app for judging impersonation accuracy."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Annotated

import typer
from pydantic import ValidationError

from quizz.config import get_settings
from quizz.infrastructure.yaml_repository import YamlQuizRepository
from quizz.services.judge_service import JudgeService, PlayerJudgement
from quizz.services.path_resolver import DefaultPathResolver

logger = logging.getLogger(__name__)

app = typer.Typer(add_completion=False, no_args_is_help=True)


@app.callback()
def judge_root() -> None:
    """Judge command group entrypoint."""

    return None


def _render_scoreboard(player_one: PlayerJudgement, player_two: PlayerJudgement) -> None:
    """Print match counts for both players."""

    typer.secho("Scores", fg=typer.colors.BRIGHT_CYAN, bold=True)
    typer.echo(
        f"{player_one.player_name}: "
        f"{player_one.matched_answers}/{player_one.total_questions}"
    )
    typer.echo(
        f"{player_two.player_name}: "
        f"{player_two.matched_answers}/{player_two.total_questions}"
    )


def _render_question_breakdown(player_one: PlayerJudgement, player_two: PlayerJudgement) -> None:
    """Print per-question details with emoji highlights."""

    typer.echo("")
    typer.secho("Question Breakdown", fg=typer.colors.BRIGHT_CYAN, bold=True)

    for index, (review_one, review_two) in enumerate(
        zip(player_one.reviews, player_two.reviews),
        start=1,
    ):
        question = review_one.question
        typer.echo("")
        typer.echo(f"Q{index}. {question.question}")
        for option_index, option in enumerate(question.options, start=1):
            markers: list[str] = []
            if option == review_one.guessed_answer:
                markers.append(f"🎭 {player_one.player_name} guessed")
            if option == review_one.correct_answer:
                markers.append(f"🎯 {player_one.target_name} answered")
            if option == review_two.guessed_answer:
                markers.append(f"🎭 {player_two.player_name} guessed")
            if option == review_two.correct_answer:
                markers.append(f"🎯 {player_two.target_name} answered")

            marker_text = f" {' | '.join(markers)}" if markers else ""
            typer.echo(f"  {option_index}. {option}{marker_text}")

        player_one_status = "✅" if review_one.is_match else "❌"
        player_two_status = "✅" if review_two.is_match else "❌"
        typer.echo(
            f"  {player_one_status} {player_one.player_name} impersonating "
            f"{player_one.target_name}"
        )
        typer.echo(
            f"  {player_two_status} {player_two.player_name} impersonating "
            f"{player_two.target_name}"
        )


@app.command()
def judge(
    player_1_name: Annotated[
        str,
        typer.Option("--player-1-name", help="Name of player 1."),
    ],
    player_2_name: Annotated[
        str,
        typer.Option("--player-2-name", help="Name of player 2."),
    ],
    questions_file_path: Annotated[
        Path | None,
        typer.Option(
            "--questions-file-path",
            help="Path to questions YAML file.",
        ),
    ] = None,
    player_1_answers_file_path: Annotated[
        Path | None,
        typer.Option(
            "--player-1-answers-file-path",
            help="Actual answers file for player 1.",
        ),
    ] = None,
    player_1_impersonator_answers_file_path: Annotated[
        Path | None,
        typer.Option(
            "--player-1-impersonator-answers-file-path",
            help="Player 1 answers while impersonating player 2.",
        ),
    ] = None,
    player_2_answers_file_path: Annotated[
        Path | None,
        typer.Option(
            "--player-2-answers-file-path",
            help="Actual answers file for player 2.",
        ),
    ] = None,
    player_2_impersonator_answers_file_path: Annotated[
        Path | None,
        typer.Option(
            "--player-2-impersonator-answers-file-path",
            help="Player 2 answers while impersonating player 1.",
        ),
    ] = None,
) -> None:
    """Score both players based on impersonation answer matches."""

    settings = get_settings()
    repository = YamlQuizRepository()
    path_resolver = DefaultPathResolver(settings)

    selected_questions_path = questions_file_path or settings.questions_file_path

    player_1_answers_path = (
        player_1_answers_file_path
        if player_1_answers_file_path is not None
        else path_resolver.default_player_answers_path(player_1_name)
    )
    player_2_answers_path = (
        player_2_answers_file_path
        if player_2_answers_file_path is not None
        else path_resolver.default_player_answers_path(player_2_name)
    )
    player_1_impersonator_path = (
        player_1_impersonator_answers_file_path
        if player_1_impersonator_answers_file_path is not None
        else path_resolver.default_impersonator_answers_path(player_1_name, player_2_name)
    )
    player_2_impersonator_path = (
        player_2_impersonator_answers_file_path
        if player_2_impersonator_answers_file_path is not None
        else path_resolver.default_impersonator_answers_path(player_2_name, player_1_name)
    )

    try:
        question_set = repository.load_questions(selected_questions_path)
        player_1_actual = repository.load_answers(player_1_answers_path)
        player_2_actual = repository.load_answers(player_2_answers_path)
        player_1_impersonation = repository.load_answers(player_1_impersonator_path)
        player_2_impersonation = repository.load_answers(player_2_impersonator_path)

        service = JudgeService()
        player_one_result = service.evaluate(
            question_set=question_set,
            player_name=player_1_name,
            target_name=player_2_name,
            player_impersonation_sheet=player_1_impersonation,
            target_actual_sheet=player_2_actual,
        )
        player_two_result = service.evaluate(
            question_set=question_set,
            player_name=player_2_name,
            target_name=player_1_name,
            player_impersonation_sheet=player_2_impersonation,
            target_actual_sheet=player_1_actual,
        )
    except (FileNotFoundError, ValidationError, ValueError) as exc:
        logger.exception("Judge app failed")
        typer.secho(f"Error: {exc}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from exc

    _render_scoreboard(player_one_result, player_two_result)
    _render_question_breakdown(player_one_result, player_two_result)


def run() -> None:
    """Run the judge CLI app."""

    app()


if __name__ == "__main__":
    run()
