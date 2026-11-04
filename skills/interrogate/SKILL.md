---
name: interrogate
description: "Use before merging to have adversaries break a change."
version: 0.2.0
author: poteto (Hermes adaptation)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [engineering, workflow]
    related_skills: [pstack:in-your-own-words, pstack:swarm]
---

# Interrogate

Adversaries try to break a change or a design. A finding survives only when a run proves it. Report the findings. Do not apply fixes.

## When to Use

Before merging significant changes, or to stress test a design you can prototype. Say "interrogate", "adversarial review", "challenge this", "stress test this code", "find blind spots", or "tear this apart".

## Frame

The scope is what the user names. Otherwise it is the branch diff from its merge base with the base branch, through the working tree (`terminal` with `git diff $(git merge-base HEAD origin/main)`). State the intent with `pstack:in-your-own-words`, from the user's message, the commits, and the PR description. Ask the user when the intent is unclear.

## Fan out

Spawn two or three adversaries in parallel with `delegate_task`. Give each its own scratch copy of the repo (a `git clone` or `git worktree add` under the scratch directory) with the scope's uncommitted changes applied, so repros never touch the real checkout. When the delegation config allows another model family, run adversaries on different families. Otherwise vary the angle each one attacks first. Give each adversary the scope, the intent, its copy's absolute path, and this brief:

> Break this change. Prove each finding with a run against the real code, such as a failing test, a repro script, or command output that shows the wrong behavior. For a design or plan, run a prototype or probe the current tree. Keep repros in your own copy. Report each finding with a title, the exact command, the output it printed, and the output the intent requires. Leave out anything you did not run. That covers style, naming, structure, and risks that need a future change to matter. No findings is a valid result.

If an adversary returns nothing, continue with the rest and note the dropout.

## Verify

Rerun each finding's command yourself with `terminal`. Keep a finding when the output shows the failure and the failure breaks the intent. Drop the rest. Merge findings that share a root cause.

Adversaries find different failures, so the verdict keeps every verified finding, not one adversary's list. Do not pick a winner.

## Output

- **Intent**: the restatement.
- **Findings**: for each verified finding, the command, its output, how it breaks the intent, and the adversaries that found it. Say "no verified findings" when none survive.
- **Dropped**: for each adversary, the count of dropped findings and why.
