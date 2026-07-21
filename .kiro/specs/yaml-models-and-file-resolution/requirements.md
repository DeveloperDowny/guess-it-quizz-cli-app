# Requirements: YAML Models and File Resolution

## Introduction

The application relies on validated domain models and shared file path conventions to load questions, load answer sheets, and resolve default output locations.

## Requirements

### Requirement 1: Model validation

**User Story:** As a developer or user, I want question and answer data to be validated consistently, so that invalid files fail fast.

#### Acceptance Criteria

1. WHEN a question set is loaded THE SYSTEM SHALL ensure question IDs are unique.
2. WHEN a question is validated THE SYSTEM SHALL strip surrounding whitespace and reject empty questions.
3. WHEN answer options are validated THE SYSTEM SHALL strip whitespace, reject empty options, and require unique options.
4. WHEN an answer sheet is validated THE SYSTEM SHALL reject duplicate question IDs within a single sheet.

### Requirement 2: YAML persistence

**User Story:** As a user, I want answer sheets to be stored and read as YAML, so that the application can round-trip the data.

#### Acceptance Criteria

1. WHEN answers are saved THE SYSTEM SHALL write YAML using the expected alias names for question-id.
2. WHEN YAML files are read THE SYSTEM SHALL reject empty or non-mapping payloads.
3. WHEN a requested YAML file does not exist THE SYSTEM SHALL raise an explicit file-not-found error.

### Requirement 3: File path resolution

**User Story:** As a user, I want sensible default locations for answer files, so that I do not need to pass every path explicitly.

#### Acceptance Criteria

1. WHEN a default player answers path is requested THE SYSTEM SHALL derive a slug from the player name.
2. WHEN a default impersonation path is requested THE SYSTEM SHALL include both the impersonator and impersonatee names.
3. WHEN names contain non-alphanumeric characters THE SYSTEM SHALL convert them to filesystem-safe hyphen-separated values.
