# Design: Impersonation Judging

## Overview

The judging experience is implemented by [src/quizz/cli/judge_app.py](src/quizz/cli/judge_app.py) and [src/quizz/services/judge_service.py](src/quizz/services/judge_service.py).

## Architecture

- The CLI layer resolves the file paths for all five YAML inputs and invokes the service.
- The judge service converts the answer sheets to maps and evaluates each question in the canonical question order.
- The CLI layer renders scoreboard and breakdown output using the returned review objects.

```text
CLI app -> JudgeService -> QuestionSet + AnswerSheets
         \-> YAML repository for input loading
         \-> CLI rendering helpers
```

## Components and Interfaces

- JudgeService.evaluate(question_set, player_name, target_name, player_impersonation_sheet, target_actual_sheet) -> PlayerJudgement
- QuestionReview captures the guessed answer, correct answer, and whether the question matched.
- PlayerJudgement contains the aggregate score and the ordered per-question reviews.

## Data Models

- QuestionSet preserves the canonical order of questions.
- AnswerSheet is converted to a lookup keyed by question ID.
- Each review is evaluated independently and stored in list order matching the question set.

## Error Handling

- Missing YAML files raise FileNotFoundError.
- Invalid YAML or model validation errors raise ValidationError or ValueError.
- Questions missing from the answer sheet are treated as empty answers and therefore as non-matches.

## Testing Strategy

- Service tests validate exact-match scoring semantics.
- CLI tests validate the printed scoreboard and emoji-based breakdown output.
