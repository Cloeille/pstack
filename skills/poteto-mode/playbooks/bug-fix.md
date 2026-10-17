# Bug Fix Playbook

**Trigger:** Something is broken. User reports a symptom.

## Steps

1. **Reproduce it yourself.** Don't ask the user for more info yet - try to hit the bug with `terminal`, tests, or manual verification. If you can't reproduce, *then* ask. A bug you can't trigger is a bug you can't verify you fixed.

2. **Binary-search the cause.** Seed understanding with `pstack:how` over the affected subsystem. Then:
   - Form 2-3 hypotheses for root cause.
   - For each: find runtime evidence that confirms or eliminates it (`terminal` for logs/debugger, `search_files` for call sites, `read_file` to trace flow).
   - Eliminate until one survives. If none survive, your model is wrong - re-read.
   - **Grep every caller** of the function you're about to touch. The lazy fix is the root-cause fix: one guard in the shared path beats a guard in every caller.

3. **Plan the fix.** If it crosses a function/module boundary, run `pstack:architect` first. Otherwise, plan the minimal change traced to the evidence from step 2. Delegate implementation via `delegate_task` with specific scope and the evidence trail.

4. **Verify on the same surface** where you reproduced it. Same command, same input. The bug must be gone and nothing adjacent must break.

5. **Git history:** commit the failing reproduction *before* the fix commit. Reviewers should be able to check out the first commit and see it fail.

## Key Rule

Be scientific. Every shipped line traces to runtime evidence. "Might help" is not a fix - it's a second bug waiting for a page at 3am. If you can't explain *why* a line is necessary with evidence, delete it.
