# Design: Player Answer Collection

## Overview

The player experience is implemented by the Typer entry point in [src/quizz/cli/player_app.py](src/quizz/cli/player_app.py) and orchestrated by [src/quizz/services/player_service.py](src/quizz/services/player_service.py).

## Architecture

- The CLI layer parses user options and delegates to the service layer.
- The service loads the question set from the repository, collects answers for both perspectives, and persists the resulting answer sheets.
- The YAML repository writes and reads answer data using the validated domain models.

```text
CLI app -> PlayerService -> QuizRepository
                 \-> PathResolver
```

## Components and Interfaces

- PlayerService.run_session(questions_file_path, impersonator, impersonatee, answer_provider, ...) -> tuple[Path, Path]
- PlayerService.collect_answer_sheet(question_set, respondent_name, perspective_name, answer_provider) -> AnswerSheet
- AnswerProvider: callable receiving (Question, respondent_name, perspective_name)

## Data Models

- QuestionSet contains ordered Question objects.
- AnswerSheet contains AnswerEntry records with question_id and answer.
- Each collected sheet is stored as YAML with the response format expected by the judge workflow.

## Error Handling

- Missing question files raise FileNotFoundError.
- Invalid YAML or schema validation errors propagate as ValidationError or ValueError.
- Invalid answer selections are rejected before persistence.

## Testing Strategy

- Unit tests cover default path selection and answer-sheet validation.
- Repository tests cover round tripping of YAML data.
- Integration-style service tests verify that both sheets are written correctly.
