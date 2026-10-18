---name: principle-migrate-callers-then-delete-legacy-apis
description: "Migrate callers and delete the old API in the same wave."
version: 0.1.0
author: poteto (Hermes adaptation)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [engineering, workflow]
    related_skills: []
---

# Migrate Callers Then Delete Legacy APIs

Update tests to assert the new contract, and delete tests that only protect pre-refactor implementation details.

**When this applies:**
- No external users depend on backward compatibility
- The project can absorb coordinated breaking changes
- The new API is part of a simplification or refactor initiative
