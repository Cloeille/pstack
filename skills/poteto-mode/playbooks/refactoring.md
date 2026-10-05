# Refactoring Playbook

**Trigger:** Behavior-preserving structural change. Rename, extract, reorganize, simplify.

## Steps

1. **Capture baseline behavior.** Before any change, record what "correct" looks like:
   - Run the test suite (`terminal`). Save the output.
   - If tests are sparse, identify key behaviors manually and verify them. Document inputs → expected outputs.
   - This baseline is your oracle for every step that follows.

2. **Plan the restructuring.** Write down the sequence of moves. Each move should be:
   - Small enough to verify in isolation.
   - Independently committable (compiles, tests pass).
   - Ordered so earlier moves don't depend on later ones.

3. **Execute in small verified steps.** For each move:
   - Make the change (`patch`, `write_file`, or `delegate_task` for mechanical transforms).
   - Run the test suite / verification immediately.
   - If anything breaks, fix it *in this step* before moving on.
   - Commit this step with a message describing the structural change.

4. **Verify behavior unchanged** after the full sequence. Same tests, same manual checks as step 1. Diff the outputs. Any behavioral difference is a bug - find it and fix it or revert.

5. **Commit each step separately.** The git history should tell the story: each commit is one structural move, all tests green. Reviewers can bisect to any commit and see correct behavior.

## Key Rule

Behavior must be identical before and after. A refactoring that changes behavior is not a refactoring - it's a feature or a bug. Verify after *every* step, not just at the end. The moment you skip verification is the moment you introduce a subtle regression you'll spend 3x longer finding.
