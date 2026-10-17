# Autonomous Run Playbook

**Trigger:** Long task, user stepping away. "Run until done", "going to bed", "finish this".

## Steps

1. **State the exit condition as a checkable predicate.** Before starting, write it down explicitly: "Done when: all 47 migration files pass `pytest tests/migration/`" or "Done when: every `.jsx` file in `src/` uses the new import path and `npm test` passes." Vague goals ("make it better") get sent back to the user for clarification.

2. **Run the loop.** Each iteration:
   - Make the **smallest change** the evidence justifies.
   - Verify: does it advance toward the predicate? (`terminal` to run tests/checks.)
   - **Commit if it advanced.** Discard and try differently if it didn't.
   - Never make two unverified changes in a row.

3. **Handle side discoveries.** Broken tests, related bugs, flaky verifiers - fix them yourself as they appear. Don't log them for later; they'll block the predicate if you ignore them. Keep fixes in separate commits.

4. **Checkpoint every iteration.** After each commit, re-evaluate: how many units remain? Is the approach still converging? If you've made 3 iterations with no progress, step back and reassess the approach - don't keep grinding the same wall.

5. **Stop when the predicate is met.** Run the full check one final time. Report: what was done, how many iterations, what side-fixes were needed.

**Plateau is not a stop.** If you're stuck, change approach - different decomposition, different order, ask `pstack:interrogate` to challenge your assumptions. Only stop for: predicate met, or a blocker that genuinely requires user input (credentials, ambiguous requirements, external service down).

## Key Rule

Define done as a falsifiable predicate before starting. Every iteration either advances toward it (commit) or teaches you something (try differently). No open-ended wandering.
