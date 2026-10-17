---name: architect
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

Sketch types, signatures, and module boundaries with pseudocode before implementing. Design it twice, pick the simpler public surface.

## When to Use

Before building a new subsystem, feature, or significant refactor. When the shape of the code matters more than getting something running fast.

## Phases

### A. Ground the Problem

Run `pstack:how` over relevant existing subsystems. Understand what's already there before designing something new. Read the code the new work will touch and integrate with.

### B. Sketch

Delegate 2+ structurally distinct design candidates via `delegate_task`. "Structurally distinct" means different module boundaries, different type hierarchies, or different data flow - not just naming variations.

Each candidate produces, in this order:

1. **Caller's usage first** - show how consuming code calls the new API. This is the design. Everything else serves it.
2. **Type sketch** - the types/interfaces needed, with fields and key methods. Pseudocode is fine.
3. **Function signatures** - public API with input/output types and brief behavior notes.
4. **Module map** - which files hold what, and dependency direction between them.
5. **Rationale** - why this shape, what tradeoff it makes, what it optimizes for.

Compare candidates on **interface depth**: how much does a caller need to know to use it correctly? Prefer the design that hides more complexity behind a simpler public surface.

Assume the next contributor is an agent that sees only the files it opened, copies the nearest example, and takes the shortest path that compiles. Reject candidates with these red flags:

- **Split ownership.** More than one module writes the same state. Give each piece of state one owner.
- **Two ways to do one task.** Keep one way, move callers off the others, delete them in the same change.
- **Importable internals.** Make internals unreachable from outside the module so an outside import fails the build.
- **Hand-synced list.** Keep one list and derive the others, or make the build fail when they disagree.
- **Shallow modules and pass-through methods.** A layer that forwards the same arguments without hiding complexity. Remove it.

Prefer the design where a change that looks right from one file is right for the whole repo.

### C. Agree (Optional)

If the user wants input, present a synthesized comparison:
- What both candidates share (the non-negotiable structure)
- Where they diverge (the actual design decision)
- Recommendation with reasoning

### D. Implement

Delegate code-writing against the chosen sketch via `delegate_task`. The sketch is the spec - implementation should match the types and signatures, not reinvent them.

### E. Scrap

If implementation reveals the sketch was wrong (types don't compose, edge case breaks the model, performance requires different structure), go back to phase B. Redesign with the new information. Sunk cost on the sketch is zero - that's the point of sketching.

## Key Rules

- **Design it twice.** At least 2 distinct candidates. One candidate means you picked the first idea that worked, not the best one.
- **Caller-first.** If you can't show clean usage code, the design isn't ready.
- **Simpler surface wins.** Between two designs that both work, prefer fewer public types, fewer required arguments, fewer concepts a caller must understand.
- **Sketches are disposable.** They exist to be compared and thrown away. Don't polish them.
