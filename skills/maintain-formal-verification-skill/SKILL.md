---
name: maintain-formal-verification-skill
description: "Trigger: maintain-formal-verification-skill, sync formal verification. Updates a formal model/harness after covered code changes and separates drift from bugs."
license: MIT
metadata:
  author: pig-stack
  version: "1.0"
  layer: "3"
---

## Activation Contract

Load when code covered by a project-local formal verification skill changed since its recorded sync commit.

## Hard Rules

- **Edit verification only:** Update models, harnesses, and the verify skill; never alter product code or weaken invariants to force a pass.
- **Distinguish drift from bugs:** Explicitly classify every failure as `verification drift` or `code bug` with a replayed counterexample.
- **Re-prove failure detection:** After updating a passing check, verify it still catches an injected break before advancing the sync commit.

## Decision Gates

| Check Outcome | Action |
|---|---|
| No covered behavior changed | Confirm `in sync`, advance sync commit if checked. |
| Model/harness stale against code | Update model from code (`drift`), re-run, test injected break (`updated`). |
| Counterexample replays on real code | Report `bug` with introducing commit and harm; do not advance sync commit as clean. |

## Execution Steps

1. Locate project-local formal verify skills and extract covered files, sync commit SHA, bounds, and command.
2. Run current check once as-is, then diff covered files since the sync commit.
3. Update model/harness from code semantics (not from desired output) when shape changed.
4. Re-run, test an injected break, and update the verify skill's sync commit and coverage list.

## Output Contract

Return per check: outcome (`in sync | updated | bug | blocked`), commits inspected, changes made, break-test proof, and uncovered gaps.
