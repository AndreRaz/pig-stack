---
name: architect
description: "Trigger: architect, /architect, design this, module boundaries. Settles data shapes, types, state ownership, and interfaces before a cross-module change."
license: MIT
metadata:
  author: pig-stack
  version: "1.1"
  layer: "0"
---

## Activation Contract

Load when a change adds or alters a type, signature, or state owner that another module uses, or when the user invokes `/architect`.

## Hard Rules

- Read touched callers, shared helpers, and existing domain types before sketching.
- Sketch two concrete shapes. Pick the one where each piece of state has one owner and callers need to know least.
- Run once per change. A settled shape is not re-designed during implementation unless a check proves it wrong.
- Output the shape only. Do not implement and do not start other skills.
- When reading cannot settle the choice, say a runnable prototype is needed and name the question it must answer.

## Decision Gates

| Scope | Action |
|---|---|
| Change stays inside one module and its types | Skip. Return "no cross-module shape change". |
| Cross-module type, signature, or state owner changes | Two shapes, pick one, list edit surfaces and invariants. |
| Choice depends on runtime behavior reading cannot show | Return the prototype question instead of guessing. |

## Execution Steps

1. Map callers and invariants within one bounded read batch.
2. Sketch Option A and Option B with types, boundaries, state owner, and tradeoffs.
3. Pick the shape that removes invalid states and branches.
4. List the exact `Allowed edit surfaces`, the invariants to reuse, and the checks that prove the shape.

## Output Contract

Return: a two-row comparison table, the chosen types and signatures, the state owner, invariants, planned edit surfaces, or the open prototype question.
