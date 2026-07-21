# Requirements: Player Answer Collection

## Introduction

The player workflow lets one participant answer questions twice in a single session: first as themselves, then while impersonating another player. The implementation already supports this interactive flow and persists both answer sheets.

## Requirements

### Requirement 1: Interactive session capture

**User Story:** As a participant, I want to answer a set of questions twice in one run, so that I can capture both my own answers and my impersonation answers.

#### Acceptance Criteria

1. WHEN a player starts a session THE SYSTEM SHALL prompt for a questions file, impersonator name, and impersonatee name.
2. WHEN the session runs THE SYSTEM SHALL ask the participant one question at a time for both perspectives.
3. WHEN the participant chooses a valid option THE SYSTEM SHALL record the selected option for the current perspective.

### Requirement 2: Answer validation

**User Story:** As a participant, I want invalid answers to be rejected immediately, so that only valid choices are stored.

#### Acceptance Criteria

1. WHEN a provider returns an answer that is not one of the question options THE SYSTEM SHALL raise a validation error.
2. IF a question has no valid matching option THEN THE SYSTEM SHALL fail the session rather than saving an invalid sheet.

### Requirement 3: Persistence

**User Story:** As a participant, I want the captured answers saved to files, so that they can be used later by the judge workflow.

#### Acceptance Criteria

1. WHEN the session completes THE SYSTEM SHALL persist the self-answer sheet and the impersonation-answer sheet as YAML files.
2. IF no explicit output path is provided THE SYSTEM SHALL use the default path convention based on the impersonator name and impersonatee name.
3. WHEN the output directory does not exist THE SYSTEM SHALL create it before writing the YAML files.
