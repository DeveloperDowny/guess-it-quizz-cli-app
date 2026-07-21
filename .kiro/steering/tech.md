# Technical Overview

## Stack

- Python 3.11+
- Typer for CLI applications
- Pydantic v2 and pydantic-settings for validation and settings
- PyYAML for YAML parsing and serialization
- pytest for automated tests
- uv for dependency and script management

## Architectural Style

The codebase is organized around a small layered architecture:

- CLI layer in src/quizz/cli
- Domain models in src/quizz/domain
- Application services in src/quizz/services
- Infrastructure implementations in src/quizz/infrastructure

## Conventions

- CLI commands are implemented as Typer apps with explicit option names.
- Business rules live in services rather than the CLI layer.
- Repository abstractions are defined in the domain layer and implemented by infrastructure classes.
- Filesystem paths are resolved through a dedicated path resolver and application settings object.
