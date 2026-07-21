# Implementation Plan: Impersonation Judging

- [x] 1. Define scoring semantics
  - Compare impersonation answers to the target player's actual answers by question ID.
  - _Requirements: 1.1, 1.2, 1.3_

- [x] 2. Implement dual-player evaluation
  - Evaluate one player's impersonation against the other player's actual answers and repeat for both players.
  - _Requirements: 2.1, 2.2_

- [x] 3. Render the judge output
  - Print a scoreboard and a question breakdown with visual markers for guessed and correct answers.
  - _Requirements: 3.1, 3.2, 3.3_

- [x] 4. Cover the behavior with tests
  - Add service and CLI tests for scoring and output formatting.
  - _Requirements: 1.1, 3.1, 3.2_
