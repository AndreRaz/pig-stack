---
name: statechart
description: "Trigger: statechart, /statechart, tla+ chart, state transitions. Translates a TLA+ model and invariants into a readable Mermaid statechart with shortest bug paths."
license: MIT
metadata:
  author: pig-stack
  version: "1.0"
  layer: "1"
---

## Activation Contract

Load when checking a TLA+ specification or translating complex state transitions and invariant violations into a visual Mermaid statechart.

## Hard Rules

- **Scratch execution:** Run TLA+/TLC checks in a scratch directory (`mktemp -d`), never leaving model artifacts in the workspace unless asked.
- **Never weaken invariants:** Write every user-observable rule as an `INVARIANT` or `PROPERTY`; keep `Done` no-op transitions for valid terminal states so `NoDeadlock` stays accurate.
- **Valid Mermaid syntax:** Quote any node label containing parentheses or brackets (`id["Label (Detail)"]`) and keep <= ~20 arrows by collapsing noise states without merging `breaks` and clean states.
- **Replay bugs against code:** When modeling real code, replay every reported counterexample path against the real implementation.

## Decision Gates

| Model Size (Distinct States) | Chart Strategy |
|---|---|
| <= 500 states | Render full Mermaid `stateDiagram-v2` / `flowchart` with colored phase groups and `breaks` markers. |
| > 500 states | Render only shortest paths to broken invariants and state counts. |

## Execution Steps

1. Author `SPEC.tla` + config in `mktemp -d` with named `Next` disjuncts and explicit invariants.
2. Run TLC; capture state count, deadlocks, and shortest counterexample traces.
3. Map states and steps into plain user-facing labels (no raw variable names) in a Mermaid diagram, marking broken states and shortest violation paths.
4. Replay any bug trace against real code (if modeling existing code) and clean up scratch dirs.

## Output Contract

Return: Mermaid diagram, state/rule summary, shortest counterexample path(s) in plain words, model omissions/bounds, and code replay evidence.
