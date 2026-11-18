# Playbook: Perf Issue

**Goal:** Find the real limiter, fix it, and prove the gain with vetted numbers.

1. **Baseline:** Build a repeatable harness and vet it with `benchmark-checklist`.
2. **Profile:** Profile outside the timed runs and name the dominant limiter before editing.
3. **Fix:** Make the smallest change aimed at that limiter.
4. **Close:** Close Sequence once, then one interleaved A/B run of at least 5 iterations per side. Keep the change only when the median gap beats run-to-run variation and outputs stay correct.

**Reply:** before and after (median, range, runs), limiter, change summary, `Risk:` line.
