---
name: deslop
description: Remove AI-generated code slop from a diff before committing.
version: 1.0.0
author: cursor-team-kit (Cursor), ported for Hermes
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [cleanup, code quality]
    related_skills: [pstack:unslop]
---

# Remove AI code slop

Check the diff against main and remove AI-generated slop introduced in the branch. Get the diff with `terminal` (`git diff main...HEAD`), make the edits with `patch`.

## Focus Areas

- Extra comments that are unnecessary or inconsistent with local style
- Defensive checks or try/catch blocks that are abnormal for trusted code paths
- Casts to `any` used only to bypass type issues
- Deeply nested code that should be simplified with early returns
- Other patterns inconsistent with the file and surrounding codebase

## Guardrails

- Keep behavior unchanged unless fixing a clear bug.
- Prefer minimal, focused edits over broad rewrites.
- Keep the final summary concise (1-3 sentences).

`pstack:unslop` does the same job for prose. This skill is for code.
