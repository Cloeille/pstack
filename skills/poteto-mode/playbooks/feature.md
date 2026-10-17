# Feature Playbook

**Trigger:** New behavior or changed behavior requested.

## Steps

1. **Understand the subsystem.** Run `pstack:how` over every module the feature touches. Don't design until you know what's already there.

2. **Design exploration.** Run `pstack:architect` - explore approaches, pick one, document why. Output: a short design doc with the chosen approach and its trade-offs.

3. **Throughput checkpoint.** Before delegating, answer in writing:
   - What are the blocking first steps (must happen before anything else)?
   - What workstreams are independent and parallelizable?
   - What shared mutable state exists between workstreams?
   - What is the smallest safe decomposition into delegate-sized units?

4. **Delegate implementation.** Use `delegate_task` for each unit with specific scope: files to touch, interfaces to respect, tests to write. You write the contracts; subagents write the code.

5. **Review every diff.** Read what came back with `read_file`. Check: does it match the design? Does it introduce unrequested abstractions? Apply the ponytail ladder.

6. **Verify on matching surface.** Run the feature end-to-end - `terminal` for CLI, `browser_navigate` for UI. Not "tests pass" alone; the actual user-facing behavior works.

7. **Rebase into small ordered commits.** Each commit compiles, passes tests, and tells one story. Squash fixups.

8. **If contested** - design choice is non-obvious or risky - run `pstack:interrogate` before shipping. Let it attack your assumptions.

## Key Rule

You own the design. Delegate implementation, stay in the lead. A subagent writes code; you decide *what* code to write and whether the result ships.
