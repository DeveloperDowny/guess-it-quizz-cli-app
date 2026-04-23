# Quizz

`quizz` provides two CLI apps:

- `quizz-player`: collect two sheets from the impersonator in one run.
- First sheet: the impersonator answers as self.
- Second sheet: the impersonator answers as the impersonatee.
- `quizz-judge`: score how accurately each player impersonated the other.

## Quick Start

1. Install dependencies:

```bash
uv sync --dev
```

2. Run the player app:

```bash
uv run quizz-player --impersonator alice --impersonatee bob
```

3. Run the judge app:

```bash
uv run quizz-judge --player-1-name alice --player-2-name bob
```

## Question File Format

```yaml
questions:
  - id: 1
    question: "Which date idea do you like the most?"
    options:
      - "Watching movies"
      - "Reading books"
      - "Trying out new cuisine"
      - "Trying out new places"
```

## Answer File Format

```yaml
answers:
  - question-id: 1
    answer: "Trying out new places"
```
