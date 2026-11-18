---
name: teach
description: "Trigger: teach me, /teach, explain plainly, mental model. Combines how + why into a progressive, diagram-first explanation."
license: MIT
metadata:
  author: pig-stack
  version: "1.0"
  layer: "1"
---

## Activation Contract

Load when the user asks to deeply understand a change or subsystem rather than receiving a terse summary.

## Hard Rules

- **Ground in `how` and `why`:** Gather verified mechanics (`path:line`) and git rationale before writing explanations.
- **Visual progression:** Build understanding step by step using focused Mermaid diagrams (`flowchart`, `sequenceDiagram`, or `stateDiagram-v2`), quoting node labels that contain parentheses or brackets.
- **Unslopped clarity:** Use plain, concrete language (`unslop`); avoid hand-waving and jargon padding.

## Decision Gates

| Target | Depth |
|---|---|
| Single diff or PR | Focus on before/after boundaries, state changes, and tradeoffs. |
| Subsystem | Start with high-level data flow diagram, then zoom into invariants and failure modes. |

## Execution Steps

1. Run `how` (mechanics) and `why` (rationale) over the target scope within ODD evidence budgets.
2. Order concepts from domain shape and data flow down to edge cases.
3. Verify every symbol and `path:line` reference exists before presenting.

## Output Contract

Return: plain-language core idea, progressive Mermaid diagram(s), concrete `path:line` walkthrough, why key tradeoffs exist, and edge cases/gotchas.
