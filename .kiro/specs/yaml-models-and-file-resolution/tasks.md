# Implementation Plan: YAML Models and File Resolution

- [x] 1. Implement domain model validation
  - Validate question prompts, option values, answer values, and uniqueness constraints.
  - _Requirements: 1.1, 1.2, 1.3, 1.4_

- [x] 2. Implement YAML repository behavior
  - Read and write YAML payloads while enforcing mapping and file existence checks.
  - _Requirements: 2.1, 2.2, 2.3_

- [x] 3. Implement default path resolution
  - Convert player names into filesystem-safe slugs and derive both player and impersonation paths.
  - _Requirements: 3.1, 3.2, 3.3_

- [x] 4. Cover the behavior with tests
  - Add tests for YAML round-tripping, path generation, and validation restrictions.
  - _Requirements: 1.1, 2.1, 3.1, 3.2_
