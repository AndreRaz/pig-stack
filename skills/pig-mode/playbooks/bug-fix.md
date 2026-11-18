# Playbook: Bug Fix

**Goal:** Prove the bug with runtime evidence, fix the root cause, and lock it with a regression check.

1. **Reproduce first:** Run the failing command, test, or app path before editing. With a cheap deterministic path, capture RED through `tdd`.
2. **Find the cause:** Form hypotheses and eliminate them with runtime evidence until one mechanism survives. Use `why` for regression history when the cause is a recent change.
3. **Fix the root:** Make the smallest change the evidence justifies. Revert any change that did not move the repro.
4. **Close:** Close Sequence once. The original repro must pass, plus the suite and a differential check on touched shared helpers. Commits follow odd-protocol section 6; when committing, the failing test lands with or before the fix.

**Reply:** what broke, root cause `file:line`, fix, failing-then-passing output, `Risk:` line.
