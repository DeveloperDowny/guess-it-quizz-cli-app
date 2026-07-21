# Requirements: Impersonation Judging

## Introduction

The judge workflow evaluates how accurately one player impersonated another by comparing the impersonation answers against the target person's actual answers.

## Requirements

### Requirement 1: Score calculation

**User Story:** As a judge, I want the system to compare impersonation answers against actual answers, so that I can measure impersonation accuracy.

#### Acceptance Criteria

1. WHEN the judge evaluates a player's impersonation THE SYSTEM SHALL compare each question answer from the impersonation sheet with the target's actual answer.
2. WHEN the guessed answer and actual answer are identical THE SYSTEM SHALL count that question as a match.
3. WHEN the guessed answer is empty or differs from the target answer THE SYSTEM SHALL not count the question as a match.

### Requirement 2: Dual-player evaluation

**User Story:** As a judge, I want both players' impersonation accuracy to be scored in one run, so that I can compare them side by side.

#### Acceptance Criteria

1. WHEN judge mode runs THE SYSTEM SHALL evaluate both players using the same questions and their respective answer sheets.
2. WHEN scoring both players THE SYSTEM SHALL produce one result set per player with the same question ordering.

### Requirement 3: Output rendering

**User Story:** As a judge, I want the results rendered clearly, so that I can quickly see scores and the basis for each result.

#### Acceptance Criteria

1. WHEN the judge workflow completes THE SYSTEM SHALL print a scoreboard showing matched answers over total questions for both players.
2. WHEN the judge workflow completes THE SYSTEM SHALL render a question-by-question breakdown with emoji markers for guessed and correct answers.
3. WHEN a question is a match THE SYSTEM SHALL label it with a success marker, and WHEN it is not THE SYSTEM SHALL label it with a failure marker.
