---
name: arena
description: "Run N parallel candidates, cross-judge, graft, verify."
version: 0.1.0
author: poteto (Hermes adaptation)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [engineering, workflow, delegation]
    related_skills: [swarm, poteto-mode]
---

# Arena

Spawn N candidates at the same task, cross-judge them, pick one base, graft the strongest parts of the losers into it, verify the result. Use when one attempt at a non-trivial artifact would lock in the wrong shape.

Open a todo list with one entry per phase (Frame, Fan out, Cross-judge, Pick, Graft, Verify) before launching anything.

## Phase A: Frame

Every candidate gets the same prompt, so the prompt is the contract.

1. State the artifact each candidate is producing.
2. Derive the rubric. 3-6 concrete gradeable criteria for what success looks like on this task. The rubric is the picker's tool in Phase D. Candidates only see the task, never the rubric.
3. Pick the runners (see Runners below).
4. Give each candidate its own output location: `/tmp/arena-<slug>/candidate-<n>/`. If the artifact is a change to an existing repo, candidates must not edit the same working tree. Either they write a patch into their own directory, or they return the full artifact in their result, per `pstack:principle-separate-before-serializing-shared-state`.

### Runners

Hermes resolves the delegate model from `delegation.model` and `delegation.provider`. There is no per-task model field, so one `delegate_task` call runs every task in it on the same model. Get family diversity by pinning the delegation model per batch and calling `delegate_task` once per family.

Default: two candidates on different model families, using the two strongest models available in the profile as configured in `pstack:setup-pstack`. Example slugs only, not requirements: `anthropic/claude-sonnet-4.5` and `openai/gpt-5.1`. Use whatever `hermes model` reports for this profile.

Record the current pin before touching anything:

```bash
hermes config get delegation
```

Then, per family:

```bash
hermes config set delegation.model <slug>
hermes config set delegation.provider <provider>   # only when the slug needs a provider other than the parent's
```

The loader invalidates its config cache on file change, so the next `delegate_task` call in the same session reads the new pin. Restore the recorded values in Phase F.

- `inherit-parent` means clear the pin: `hermes config unset delegation.model` and `hermes config unset delegation.provider`. That batch then runs on the parent chat model.
- If the runtime rejects a configured slug, run that seat on its family default and say so in the synthesis note. Never invent a slug you have not confirmed.
- `inherit-parent` in the candidate set is legal. It just means the seats are not independent by model family, so say that in the note.
- Spawn more runners when the arena covers multiple design directions. Use the same model N times when the work is generation-bound rather than judgment-sensitive.
- Reasoning effort is global for delegates (`delegation.reasoning_effort`), set in `pstack:setup-pstack`. There is no per-seat reasoning level. Set the budget before the arena opens, generous enough for the hardest seat in it.
- If N exceeds `delegation.max_concurrent_children`, the tool refuses the call. Split into more batches, one per family per chunk.

## Phase B: Fan out

One `delegate_task` call per model family, `tasks=[...]` containing every candidate for that family. Run foreground (the default) so the call blocks and returns all results.

Each task brief is self-contained and carries:

- **Goal**: produce the artifact at its own output path.
- **Grounding**: the path to shared context every candidate needs, and nothing more, per `pstack:principle-guard-the-context-window`.
- **Output path**: its own `/tmp/arena-<slug>/candidate-<n>/` directory.
- **Rationale**: a short note naming the alternatives it considered and what it rejected, and why.

If a candidate produces no output, proceed with N-1 and note the dropout.

## Phase C: Cross-judge

Pick a judge from a model family different from the parent and from the candidate families. Same mechanism as Phase A: pin `delegation.model` to the judge slug, and restore the pin after.

The judge is read-only. Hermes has no tool-level read-only flag for delegates, so read-only is enforced by the brief: it gets the rubric and the candidate paths by label, is told to read candidates and write nothing, and returns per-criterion scores, a recommended base, and rationale in its final message. Do not let it write files into the candidate directories.

Spawn it only after every Phase B candidate finished. It runs in parallel with your own Phase D reading. Never spawn it while candidates are still writing.

## Phase D: Pick a base

Read every candidate end to end before picking. Score each against the rubric criterion by criterion, not on holistic feel, then compare with the cross-judge.

Agreement on the base confirms the pick. Disagreement means one of you is biased or the rubric was ambiguous. Read both rationales before deciding.

Pick the base a future maintainer can extend most easily without breaking invariants. When two feel tied, prefer the cleaner boundary or smaller API, per `pstack:principle-laziness-protocol`.

## Phase E: Graft

Walk each losing candidate once more for what is worth porting into the base. Usually one or two things per candidate, not most of it. Fold each graft in by hand, per `pstack:principle-redesign-from-first-principles`, so the result stays coherent under one mental model. Do not paste mechanically.

If the candidates converge on one shape, that is strong agreement. Note it and ship the consensus shape, no graft needed. If they wildly diverge, Phase A was under-specified. Reframe and re-run rather than averaging the divergence.

## Phase F: Verify

Verify the synthesized artifact like any other output, per `pstack:principle-prove-it-works`. Run it, test it, read the diff. If verification finds a problem the arena missed, either Phase A was wrong (reframe and re-run) or a candidate caught it and you skipped the graft (go back to Phase E). Do not paper over it.

Restore the delegation pin you recorded in Phase A, then run `hermes config get delegation` and confirm the values read back. Leaving a foreign model pinned silently reroutes every later delegate in the session.

## Outputs

One synthesized artifact, plus a short `arena-synthesis.md` beside it naming:

- the base and why it won
- the cross-judge's verdict, and any disagreement with your pick
- each graft with its source candidate
- what was rejected and why
- any convergence or dropouts
- the verification result and the evidence for it
