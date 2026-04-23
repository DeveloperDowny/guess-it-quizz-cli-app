# AGENTS.md

## Project Preferences
- use uv for initialization
- use uv_build as build-backend and for packaging and distribution
- Prefer clean architecture and separation of concerns.
- Keep code readable and maintainable with small, focused functions.
- Use type hints everywhere.
- Use Google-style docstrings.
- make things injectable so that testing becomes easier
- use TDD
- Use Pydantic models for structured data validation and serialization.
- Use pydantic-settings for env
- Prefer Typer for CLI applications.
- Add structured logging via `logger = logging.getLogger(__name__)`.
- Don't reinvent the wheel, first search pypi if any library can be helpful for a feature/sub-feature and use it if available


## Project Intent
- Build two CLI apps
### CLI App 1: Player app
- Flags
    - --questions-file-path
    - --answers-file-path
        - this becomes --impersonatee-answers-file-path for the impersonatee
    - --impersonator-answers-file-path
        - the answers the person answered impersonating the other person
    - --impersonator
        - the person who is answering impersonating the other person
    - --impersnoatee-answers-file-path
        - the answers given by impersonatee
    - --impersonatee
        - the person from whose perspective you are answering the questions
    - if impersonator-answers-file-path is empty use a default file path constructed by the value of --impersonator
        - same applies for impersonatee-answers-file-path
- the questions-file-path is a yaml of the following format
```yaml
questions:
  - id: 1
    question: "Which date idea you like the most?"
    options:
      - "Watching movies"
      - "Reading books"
      - "Trying out new cuisine"
      - "Trying out new places"
```
- the answers-file-path will be a yaml file of the following format
```yaml
answers:
    - question-id: 1
      answer: "Trying out new places"
```

### CLI App 2: Judge app
- Flags
    - questions-file-path
    - --player-1-name
    - --player-2-name
    - --player-1-answers-file-path
    - --player-1-impersonator-answers-file-path
    - --player-2-answers-file-path
    - --player-2-impersonator-answers-file-path
    - if file paths are not passed, use the default paths using --player-1-name and --player-2-name
    - the defaults should be in sync with the defaults used in CLI App 1 and should be stored centrally
- Point calculation for players
    - For e.g., point calculation for player-1 will following this:
        - match answers in --player-1-impersonator-answers-file-path and --player-2-answers-file-path
        - for each correct match, increment point
        - no negative points for mismatches
    - similarly for player-2 using respective files
- Behavior
    - Print points for each player in the format <no of matched answers>/<total questions>
    - Print question, along with all choices, highlight what was answers, highlight what was correct
        - Use emojis for highlighting