---name: how
description: "Explain how code works. Subsystem walkthroughs and."
version: 0.1.0
author: poteto (Hermes adaptation)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [engineering, workflow]
    related_skills: []
---

# How

Answer "how does X work?" with clear architectural explanations grounded in actual code.

## When to Use

When the user asks how a subsystem, feature, or mechanism works. Also invoked by other pstack skills (e.g. `pstack:architect`) to ground design in existing code.

## Modes

### Explain (default)

Explore the codebase and produce an explanation.

**Simple questions** (single module, one concept): do it in one pass - `search_files` to locate, `read_file` to understand, write the explanation.

**Complex questions** (multi-file subsystem, cross-cutting concern): decompose into 2-4 exploration angles, delegate each as a read-only subagent via `delegate_task`, then synthesize results into a single explanation.

### Critique

Explain first (as above), then spawn multiple `delegate_task` subagents to independently identify architectural issues. Each critic works from the explanation plus direct code access. Synthesize their findings into a problems section appended to the explanation.

## Exploration Technique

Explorers use `search_files` and `read_file` to trace code. The approach:

1. **Start broad** - glob for directories (`search_files` with `target="files"`), grep for key types/interfaces/exports. Understand the shape before the details.

2. **Follow the thread** - from entry points, trace callers and callees. Follow data flow: where is it created, transformed, consumed? Read actual code at each hop.

3. **Read actual code** - don't stop at file names or function signatures. Read the implementation. The interesting behavior lives in the body, not the type.

4. **Note surprises** - anything that violates the expected pattern is worth calling out. Implicit dependencies, side effects, hidden state, fallback paths.

## Output Format

Structure the explanation as:

- **Overview** - one paragraph, what this subsystem does and why it exists
- **Key Concepts** - types, abstractions, or domain terms needed to follow along
- **How It Works** - step-by-step walkthrough of the main flow, referencing files and functions
- **Where Things Live** - file/directory map of the relevant code
- **Gotchas** - surprises, implicit contracts, known quirks, easy mistakes

## Delegation Pattern

When decomposing for `delegate_task`:

```
Each subagent brief:
- Goal: "Trace how [specific aspect] works in [scope]"
- Constraint: read-only, no modifications
- Tools: search_files, read_file only
- Output: structured notes with file paths and line references
```

Synthesize by merging notes, resolving contradictions (re-read code if needed), and writing the unified explanation.
