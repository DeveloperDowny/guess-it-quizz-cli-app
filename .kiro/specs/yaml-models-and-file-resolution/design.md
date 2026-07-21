# Design: YAML Models and File Resolution

## Overview

The domain model layer in [src/quizz/domain/models.py](src/quizz/domain/models.py) and the YAML repository in [src/quizz/infrastructure/yaml_repository.py](src/quizz/infrastructure/yaml_repository.py) provide the foundational data contract for the rest of the application.

## Architecture

- Pydantic models enforce schema-level validation for questions, options, answer entries, and answer sheets.
- The YAML repository reads and writes these models to and from YAML files.
- The path resolver uses application settings and name slugs to derive default file locations without hard-coding paths.

## Components and Interfaces

- Question validates the prompt and option list.
- QuestionSet validates unique question IDs.
- AnswerEntry validates answer text and uses the question-id alias for serialization.
- AnswerSheet validates unique question IDs and exposes to_map().
- YamlQuizRepository.load_questions(), load_answers(), save_answers(), and \_read_yaml_dict()
- DefaultPathResolver.default_player_answers_path() and default_impersonator_answers_path()

## Data Models

- Questions are stored as a list of Question objects and validated as a set.
- Answers are stored as a list of AnswerEntry objects and normalized into a map by question ID during evaluation.

## Error Handling

- Empty or invalid YAML payloads raise ValueError.
- Missing files raise FileNotFoundError.
- Duplicate IDs or empty strings raise validation errors.

## Testing Strategy

- Tests cover YAML round-tripping, path slugging, and validation rules.
