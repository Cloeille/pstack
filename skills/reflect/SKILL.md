---name: reflect
description: "Spawn three parallel review subagents over the active."
version: 0.1.0
author: poteto (Hermes adaptation)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [engineering, workflow]
    related_skills: []
---

# Reflect

Mine the current conversation for durable learnings, then route them into skill edits.

## When to invoke

Invoke when the user says "reflect" or "/reflect". Skip when the conversation is trivial, off-topic, or already covered by an existing skill the parent followed correctly. One-offs are not learnings.

## Process

### 1. Locate the active transcript

The parent finds its own conversation with the `session_search` tool, scoped to the current session (`session_id` from the system prompt, read with `around_message_id` to pull the full range). Never glob raw transcript files or reach into another profile's session history. If the lookup fails to resolve, write a tight digest of the session and pass that instead.

### 2. Spawn three reviewers in parallel

One `delegate_task` call with three tasks, agent mode (not read-only: reviewers need MCP access for context lookups such as tickets, chat threads, or observability traces referenced in the transcript. Read-only strips MCPs).

| Lens | Prompt template |
|---|---|
| Judgment | `references/judgment-reviewer.md` |
| Tooling | `references/tooling-reviewer.md` |
| Divergent | `references/divergent-reviewer.md` |

Every task in one `delegate_task` call runs on the Hermes-configured `delegation.model` (set by `pstack:setup-pstack`). There is no per-task model override, so the three lenses get their diversity from the prompt, not the model. For genuine model diversity, run the three lenses as three separate rounds, changing `delegation.model` between rounds.

Pass each template verbatim, substituting the transcript content or digest where marked. Reviewers return findings in their task result.

### 3. Synthesize

One `delegate_task` call, agent mode (not read-only: the synthesizer's quality check spot-verifies citations, which can require MCP access). It runs on the same `delegation.model` as the reviewers unless you deliberately changed it between rounds. Use `references/synthesizer.md` verbatim, with each reviewer's full output inlined where marked. The synthesizer returns a structured Accepted / Rejected / Backlog list.

### 4. Structural enforcement check

Sanity-check the synthesizer's Accepted list. For any item that would be enforced more reliably by a lint rule, script, metadata flag, or runtime check, move it from Accepted to Backlog. See the **encode-lessons-in-structure** principle skill.

### 5. Apply

Before applying any Accepted edit, present the synthesizer's full Accepted/Rejected/Backlog output to the user and wait for explicit approval. The user picks which subset to apply and may redirect routings. Skill changes affect every future agent in the org. Do not auto-apply.

Backlog items file to whatever devex / backlog tracker your team uses automatically. Only the Accepted list waits for approval.

For each approved Accepted item, follow the Routing field exactly:

- Trivial existing-skill edit (a one-line bullet, a tightened sentence, a stale fact corrected): parent does directly.
- Substantive existing-skill edit (a new section, a new pattern table, more than ~10 lines): hand to Hermes Agent's built-in `create-skill` skill and run its draft / test / iterate loop.
- `tune description: <skill path>` (the skill exists but didn't trigger when it should have): hand to `create-skill` and run its description-optimization loop.
- `new skill via create-skill: <kebab-name>`: hand creation to `create-skill`. Do not invent the shape ad hoc.

If your environment ships a SKILL.md validator, run it on every touched skill before declaring done. Skip this step if it doesn't.

### 6. Summarize for the user

Short list, no preamble:

- Edits applied: `<skill path>`. What changed, one line each.
- New skills created: `<skill path>`. One line each (rare).
- Backlog filed to the devex tracker: `<issue title>` (`<tags>`). One line each.
- Dropped: one line per rejected finding + reason from the synthesizer.
