# Performance Issue Playbook

**Trigger:** Traced slowness. "X is slow", "Y takes too long", latency/throughput regression.

## Steps

1. **Measure baseline.** Before touching anything, get a number. `terminal` with `time`, `hyperfine`, `perf stat`, `curl -w '%{time_total}'`, or app-level timing. Record the exact command and result. No baseline = no fix. Vet the baseline and every later number (see Vet the Number below).

2. **Profile to find the hotspot.** Don't guess. Use the right tool:
   - Python: `cProfile`, `py-spy`, `line_profiler`
   - Node: `--prof`, `clinic`, `0x`
   - General: `perf record`, `strace -c`, `flamegraph`
   - DB: `EXPLAIN ANALYZE`
   
   The profile tells you *where* the time goes. Read it before forming hypotheses.

3. **Form hypotheses, test each.** From the profile, identify 1 to 3 candidate hotspots. Order fixes by the performance mantras, cheapest first, and stop when an earlier one meets the target: don't do it, do it but don't do it again, do it less, do it later, do it when they're not looking, do it concurrently, do it cheaper. For each:
   - State what you expect to improve and by how much.
   - Make the minimal change to test the hypothesis.
   - Measure. Did it move the number?
   - Keep what works, revert what doesn't.

4. **Implement the fix.** The winning hypothesis becomes the real change. Delegate via `delegate_task` if implementation is mechanical. Keep the change minimal. Perf fixes that restructure unrelated code are two PRs.

5. **Measure again.** Same command, same conditions as step 1. Record before/after. The improvement must be real, reproducible, and meaningful.

6. **Commit** with before/after numbers in the commit message.

## Vet the Number

Answer each with evidence from a run, not a guess (adapted from poteto's benchmark-checklist):

1. **Why not double?** Name the limiter (a core, a lock, disk, network, the load generator) from a profile in a run you don't report.
2. **Was it tuned?** Both sides run like production: release build, prod flags, warm or cold caches as prod sees them.
3. **Did it break limits?** Do the arithmetic. Removing a piece that takes 10% of the run can make it at most about 11% faster.
4. **Did it error?** Count failures and check outputs are correct, not just present.
5. **Does it reproduce?** At least 5 runs per side, alternated A, B, A, B. Report median and range. A gap smaller than run-to-run variation is no difference.
6. **Does it matter?** Measure the end-to-end path a user waits on next to any micro result.
7. **Did it even happen?** Confirm the work ran inside the timed region.

Report the verdict first (faster, slower, no measurable difference, inconclusive), then the number with unit, run count, range, and limiter. Inconclusive when the limiter is unknown, a side ran untuned, or 4 and 7 were not checked. For a quick ballpark the user asked for, one run is fine, but still check 4 and 7 and say it was one run.

## Key Rule

No fix without measurement. Before and after numbers are required, in the commit message, not just in your head. "It feels faster" is not evidence.
