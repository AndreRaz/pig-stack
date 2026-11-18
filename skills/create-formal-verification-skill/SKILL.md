---
name: create-formal-verification-skill
description: "Trigger: create-formal-verification-skill, model-check, prove invariant. Generates and proves a formal property check for races, state machines, or parsers."
license: MIT
metadata:
  author: pig-stack
  version: "1.0"
  layer: "3"
---

## Activation Contract

Load when unit/integration tests cannot reach rare interleavings, retry races, state-machine invariants, or memory/parser bounds.

## Hard Rules

- **True to real code:** Model steps and names must map 1-to-1 to actual source symbols (`file:line`), recording the synced commit SHA.
- **Prove it can fail:** Demonstrate the check catching an injected scratch break in the real code, then revert the scratch break cleanly.
- **Never weaken failing properties:** If current code breaks the invariant, report the counterexample without diluting the spec.
- **Cheap to rerun:** Wrap the check in one reproducible command inside `.agents/skills/verify-formal-<area>/SKILL.md`.

## Decision Gates

| Property Class | Default Tool Choice |
|---|---|
| Concurrency / protocol / retry ordering | Model checker (TLA+ / TLC; read outputs with `statechart`) |
| Input space / parser / overflow invariants | Property-based testing, SMT verifier, or sanitizer harness |
| No formal verifier available for language | Generated property/fuzz suite against real code (disclose scope) |

## Execution Steps

1. Identify the highest-impact invariant from code (`file:line`) and select the lowest-cost suitable verifier.
2. Author the model/harness + invariant and run it against current code.
3. Prove detection on a temporary injected break, revert the break, and re-verify baseline pass (or report existing bug counterexample).
4. Write the project-local `verify-formal-*` skill with coverage paths, bounds, sync commit SHA, and rerun command.

## Output Contract

Return: target invariant, tool/bounds chosen, injected-break detection proof, current status, and generated skill path.
