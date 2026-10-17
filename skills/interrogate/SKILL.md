---name: interrogate
description: "Multi-model adversarial code review via parallel."
version: 0.1.0
author: poteto (Hermes adaptation)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [engineering, workflow]
    related_skills: []
---

# Interrogate

Spawn multiple `delegate_task` subagents to adversarially review code changes. Adversarial signal comes from model diversity - independent reviewers finding the same issue means high confidence.

## When to Use

Before merging significant changes. When you want more than one perspective on correctness, security, or design. When the stakes of a bug are high.

## Procedure

### 1. Determine Scope

Identify what to review:
- A diff (`terminal` with `git diff`)
- Specific files (`search_files`, `read_file`)
- Recent work (`git log --oneline -10`, then diff the range)

Collect the relevant code and context.

### 2. State Intent

Write one sentence: what does this code change try to accomplish? This anchors every reviewer. Without it, reviewers invent their own assumptions.

### 3. Spawn Reviewers

Launch at least 2-3 parallel reviewers via `delegate_task`. Each gets the same prompt:

```
Review this code change.

Intent: [one sentence from step 2]

Code:
[the diff or file contents]

Review against this rubric:
- Correctness: does it do what intent says? Logic errors, off-by-ones, nil paths?
- Edge cases: empty inputs, concurrent access, large inputs, unicode, zero/negative values?
- Security: injection, auth bypass, secrets in code, unsafe deserialization?
- Performance: unnecessary allocations, O(n²) where O(n) works, missing indexes?
- Maintainability: unclear names, implicit coupling, missing error context?

For each finding:
- Quote the relevant code
- State the problem
- Rate severity: critical / warning / nit
- Suggest a fix (one-liner if possible)
```

### 4. Synthesize

Read all reviewer outputs. Consolidate:

- **Agreement** (2+ reviewers flagged it) → high confidence, include in verdict
- **Lone findings** → lower confidence, include as "worth reading" with the single reviewer's reasoning
- **Contradictions** → re-read the code yourself to break the tie

### Deliverable

One synthesized verdict with:
- Summary (ship / revise / block)
- High-confidence findings (with code quotes)
- Worth-reading findings
- What reviewers agreed was fine

**Do NOT auto-apply changes.** Present findings. The user decides.
