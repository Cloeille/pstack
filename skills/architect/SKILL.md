---
name: architect
description: "Design types and module structure before writing code."
version: 0.1.0
author: poteto (Hermes adaptation)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [engineering, workflow]
    related_skills: []
---

# Architect

Before writing code, trace every system the change touches, then sketch two different shapes for it (types, signatures, module boundaries) and pick the one where each piece of state has one owner, each task has one way to do it, and callers need to know least. Redesign instead of patching if workarounds repeat.

## When to Use

Before building a new subsystem, feature, or significant refactor, when the shape of the code matters more than getting something running fast.

For a large or contested design, run two or more candidates in parallel with `delegate_task`, each producing its own sketch, or stress-test the pick with `pstack:interrogate`, instead of sketching alone.
