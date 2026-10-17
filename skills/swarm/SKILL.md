---name: swarm
description: "Fan out parallel workers via delegate_task, drain, report."
version: 0.1.0
author: poteto (Hermes adaptation)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [engineering, workflow]
    related_skills: []
---

# Swarm

Fan out N parallel `delegate_task` workers, collect results, consolidate into one report.

## When to Use

When a task decomposes into independent slices that can run concurrently: reviewing multiple files, checking multiple services, exploring multiple subsystems, running the same analysis with different parameters.

## Phases

### A. Frame

1. **Done predicate** - state what "complete" means before spawning anything.
2. **Shape** - pick one:
   - **Partition**: each worker covers a distinct slice (files, modules, endpoints). No overlap.
   - **Race**: all workers cover the same brief independently. Pick the best result.
   - **Mix**: some workers partition, some race. Use when part of the work benefits from redundancy.
3. **Set N** - number of workers. Match to the number of slices (partition) or desired redundancy (race).

### B. Fan Out

Spawn all workers in one `delegate_task` call with multiple tasks. Each brief is self-contained:

- **Goal**: what this worker produces
- **Scope/slice**: exactly what subset it covers (file list, module, endpoint)
- **How to verify**: how the worker checks its own work
- **Report format**: use `PASS / ISSUES / BLOCKED` with evidence (file paths, output, error messages). A worker that can prove a defect reports `ISSUES` and lists every issue it can prove, not only the first.
- **Exact targets**: when workers verify or measure commits, the brief names the exact SHAs. A measurement brief also names the method (sample count, what one sample is, order). The worker records both in its result.

Workers must not depend on each other's output.

### C. Aggregate

Read all results. Drop a result that does not record the SHAs and method its brief names, and rerun that worker once. After a second miss, record a gap. A gap does not count as a pass.

- **Partition**: every slice must have a result. Missing slice = gap, call it out.
- **Race**: apply selection rule (most thorough, most critical, consensus).
- Flag any `BLOCKED` workers - report what blocked them and whether it matters.

### D. Report

One consolidated report:
- **Summary**: pass/fail, coverage (N/N slices or N workers agreed)
- **Table**: worker | slice | status | key finding
- **Issues**: merged and deduplicated, ordered by severity
- **Gaps**: slices with no result or blocked workers
