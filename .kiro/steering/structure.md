# Project Structure

## Top-Level Layout

- src/quizz/cli/: CLI entry points for player and judge workflows
- src/quizz/domain/: domain models and repository interfaces
- src/quizz/services/: application services for session flow and scoring
- src/quizz/infrastructure/: YAML-backed repository implementation
- src/quizz/config.py: application settings and environment handling
- tests/: regression tests for each behavior area

## Key Modules

- src/quizz/cli/player_app.py: interactive player workflow CLI
- src/quizz/cli/judge_app.py: judge workflow CLI and rendering logic
- src/quizz/services/player_service.py: orchestration of answer capture and persistence
- src/quizz/services/judge_service.py: score evaluation and per-question reviews
- src/quizz/services/path_resolver.py: default path generation for answer files
- src/quizz/infrastructure/yaml_repository.py: YAML read/write implementation
- src/quizz/domain/models.py: validated question and answer schema models
