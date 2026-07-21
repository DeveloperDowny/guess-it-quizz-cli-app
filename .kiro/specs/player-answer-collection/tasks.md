# Implementation Plan: Player Answer Collection

- [x] 1. Define the player workflow contract
  - Capture the CLI options needed for the impersonator, impersonatee, and file paths.
  - _Requirements: 1.1, 3.1_

- [x] 2. Implement answer collection orchestration
  - Build the service flow that collects both self and impersonation sheets from the same question set.
  - _Requirements: 1.2, 1.3, 3.1_

- [x] 3. Validate answer selections
  - Reject answers that do not match one of the configured options.
  - _Requirements: 2.1, 2.2_

- [x] 4. Persist answer sheets to YAML
  - Write both answer sheets to disk using the YAML repository.
  - _Requirements: 3.1, 3.2, 3.3_

- [x] 5. Cover the behavior with tests
  - Add regression tests for default path behavior, invalid answers, and persistence.
  - _Requirements: 1.1, 2.1, 3.1, 3.2_
