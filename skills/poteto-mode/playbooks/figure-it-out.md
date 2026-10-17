# Figure It Out Playbook

**Trigger:** Large migration, ambitious multi-part change, or anything where no narrower playbook fits.

## Steps

1. **Frame the work.** Before writing code, answer three things in writing:
   - **Definition of done** - a falsifiable predicate. "All 200 endpoints return valid OpenAPI responses" not "API is cleaned up."
   - **Scope quantified** - how many files, modules, endpoints, records? Measure with `search_files` / `terminal`. Unknown scope = unknown timeline.
   - **Rigor level** - what verification is required at each step? (Test suite, manual check, type-checker, linter, benchmark.)

2. **Design the workflow.** Decompose into atomic landable units - each one compiles, passes tests, and can ship independently.
   - Order by **riskiest unknown first**. The thing most likely to invalidate the plan goes first; don't save it for last.
   - Build the **verification harness before the work**. If you need a test, a script, or a check to verify units, write it now. Working without a verifier is flying blind.
   - Use `pstack:architect` if the decomposition is non-obvious.

3. **Run the loop.** Each unit is an experiment:
   - **Hypothesis:** "Changing X will advance the predicate without breaking Y."
   - **Smallest change** that tests the hypothesis. Delegate via `delegate_task` for mechanical work.
   - **Measure:** run the verification harness.
   - **Keep or revert.** No half-landed units.
   - Commit with a message that links to the hypothesis.

4. **Log decisions throughout.** When you choose approach A over B, note why in a commit message or comment. Future-you (or the reviewer) needs the reasoning, not just the result.

## Key Rule

When no playbook fits, design one. Bias toward more rigor, not less - the cost of too much verification is minutes; the cost of too little is a rollback. Every unit lands clean or doesn't land.
