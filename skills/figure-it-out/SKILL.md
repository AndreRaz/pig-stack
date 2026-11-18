---
name: figure-it-out
description: "Trigger: figure-it-out, /figure-it-out, complex migration, custom playbook. Designs and runs an auditable ODD workflow when no standard playbook fits."
license: MIT
metadata:
  author: pig-stack
  version: "1.1"
  layer: "4"
disable-model-invocation: true
---

## Activation Contract

Load when `pig-mode` finds no matching playbook (large migrations, multi-stage conversions, unattended work), or when the user invokes `/figure-it-out`.

## Hard Rules

- State the falsifiable done predicate, quantified scope, and blockers before mutating code.
- Capture the baseline before changing behavior, so every check reads old value against new value.
- Track phases and specs in `odd/tasks/<feature>.md`. Add `show-me-your-work` only for unattended runs.
- Verify each unit before the next. `INCONCLUSIVE` is not a pass.
- Follow the ODD correction bounds. Never retry the same hypothesis twice.

## Decision Gates

| Situation | Action |
|---|---|
| Hard-to-reverse design choice | `architect` once. `arena` only if it returns an open prototype question. |
| Independent seams with ~100+ lines each | `swarm` with disjoint surfaces. |
| A fix repeats across units | `correct` after the run, not during it. |

## Execution Steps

1. Frame the predicate, scope, and `odd/tasks/<feature>.md`.
2. Build the baseline check.
3. Run each phase as hypothesis, smallest change, real check, one log row.
4. Run the Close Sequence once (`deslop`, full verification) and check the end-to-end predicate.

## Output Contract

Return: the phase list, tracking paths, per-unit verdicts, and open blockers.
